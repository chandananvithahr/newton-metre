# costimize-v2/ui/mechanical_tab.py
"""Mechanical parts tab — upload drawing, confirm processes, get should-cost breakdown."""

import streamlit as st
from engines.mechanical.cost_engine import calculate_mechanical_cost
from engines.mechanical.material_db import list_material_names
from engines.mechanical.process_db import list_process_names
from extractors.vision import analyze_drawing
from extractors.process_detector import detect_processes_from_extraction
from ui.components import (
    render_cost_table,
    render_historical_comparison,
    render_confidence_badge,
    render_validation_comparison,
    render_arbitration,
    render_clarifying_questions,
)
from engines.validation.orchestrator import orchestrate
from engines.validation.comparator import ConfidenceTier


def render():
    st.header("Mechanical Parts — Should-Cost Breakdown")

    # --- Upload ---
    uploaded = st.file_uploader("Upload engineering drawing", type=["png", "jpg", "jpeg", "pdf"], key="mech_upload")

    if uploaded:
        image_bytes = uploaded.read()
        st.session_state["mech_image_bytes"] = image_bytes
        st.image(image_bytes, caption=uploaded.name, width=400)

        if st.button("🔍 Analyze Drawing", key="mech_analyze"):
            with st.spinner("AI is extracting dimensions and processes..."):
                try:
                    extraction = analyze_drawing(image_bytes, uploaded.name)
                    st.session_state["mech_extraction"] = extraction
                    st.session_state["mech_processes"] = detect_processes_from_extraction(extraction)
                except Exception as e:
                    st.error(f"Extraction failed: {e}")
                    return

    # --- Extracted Data + Manual Override ---
    extraction = st.session_state.get("mech_extraction")
    if not extraction:
        st.caption("Upload a drawing to get started, or fill in dimensions manually below.")

    st.subheader("Dimensions")
    dims = extraction.get("dimensions", {}) if extraction else {}
    col1, col2, col3 = st.columns(3)
    with col1:
        od = st.number_input("Outer Diameter (mm)", value=float(dims.get("outer_diameter_mm") or 60), min_value=0.1, key="mech_od")
        id_mm = st.number_input("Inner Diameter (mm)", value=float(dims.get("inner_diameter_mm") or 0), min_value=0.0, key="mech_id")
    with col2:
        length = st.number_input("Length (mm)", value=float(dims.get("length_mm") or 100), min_value=0.1, key="mech_len")
        width = st.number_input("Width (mm)", value=float(dims.get("width_mm") or 0), min_value=0.0, key="mech_width")
    with col3:
        hole_count = st.number_input("Hole Count", value=int(dims.get("hole_count") or 0), min_value=0, key="mech_holes")
        thread_count = st.number_input("Thread Count", value=int(dims.get("thread_count") or 0), min_value=0, key="mech_threads")

    st.subheader("Material")
    materials = list_material_names()
    detected_mat = extraction.get("material") if extraction else None
    default_idx = 0
    if detected_mat:
        for i, m in enumerate(materials):
            if detected_mat.lower() in m.lower():
                default_idx = i
                break
    material_name = st.selectbox("Material", materials, index=default_idx, key="mech_mat")

    st.subheader("Manufacturing Processes")
    all_processes = list_process_names()
    suggested = st.session_state.get("mech_processes", [])
    selected_processes = []
    cols = st.columns(3)
    for i, (pid, pname) in enumerate(all_processes):
        col = cols[i % 3]
        checked = pid in suggested
        if col.checkbox(pname, value=checked, key=f"proc_{pid}"):
            selected_processes.append(pid)

    st.subheader("Order Details")
    col1, col2 = st.columns(2)
    with col1:
        quantity = st.number_input("Quantity", value=100, min_value=1, key="mech_qty")
    with col2:
        tight_tol = st.checkbox("Tight tolerances (< ±0.05mm)", key="mech_tol")

    confidence = extraction.get("confidence", "manual") if extraction else "manual"
    if confidence == "low":
        st.warning("⚠ AI confidence is LOW — please verify dimensions manually.")
    elif confidence == "medium":
        st.info("ℹ AI confidence is MEDIUM — review dimensions before calculating.")

    # --- Calculate ---
    if st.button("💰 Calculate Should-Cost", key="mech_calc", type="primary"):
        if not selected_processes:
            st.error("Select at least one manufacturing process.")
            return

        final_dims = {
            "outer_diameter_mm": od,
            "inner_diameter_mm": id_mm,
            "length_mm": length,
            "width_mm": width,
            "hole_count": hole_count,
            "thread_count": thread_count,
            "hole_diameter_mm": dims.get("hole_diameter_mm", 8),
            "thread_length_mm": dims.get("thread_length_mm", 20),
            "groove_count": dims.get("groove_count", 0),
            "surface_area_cm2": dims.get("surface_area_cm2", 100),
        }

        image_for_validation = st.session_state.get("mech_image_bytes")

        with st.spinner("Running physics engine + AI validation in parallel..."):
            validation = orchestrate(
                image_bytes=image_for_validation,
                dimensions=final_dims,
                material_name=material_name,
                selected_processes=selected_processes,
                quantity=quantity,
                has_tight_tolerances=tight_tol,
                user_answers=st.session_state.get("mech_user_answers"),
                round_number=st.session_state.get("mech_round", 1),
            )

        st.session_state["mech_validation"] = validation
        result = validation.physics_result
        st.session_state["mech_result"] = result

        # Historical PO lookup
        from history.po_matcher import find_matching_po
        match = find_matching_po(
            part_number="",
            part_description=f"{material_name} {od}mm {length}mm {' '.join(selected_processes)}",
        )
        st.session_state["mech_history_match"] = match

    # --- Display Results ---
    result = st.session_state.get("mech_result")
    if result:
        st.subheader("📊 Should-Cost Breakdown")

        lines = [
            {"item": f"Raw Material ({result.material_name})", "cost": result.material_cost,
             "detail": f"{result.raw_weight_kg + result.wastage_weight_kg:.2f} kg incl. wastage"},
        ]
        for pl in result.process_lines:
            lines.append({
                "item": pl.process_name,
                "cost": pl.machine_cost,
                "detail": f"{pl.time_min:.1f} min @ ₹{pl.machine_cost / (pl.time_min / 60) if pl.time_min > 0 else 0:.0f}/hr",
            })
        lines.extend([
            {"item": "Setup Cost (amortized)", "cost": result.total_setup_cost, "detail": f"Over {result.quantity} pcs"},
            {"item": "Tooling Cost", "cost": result.total_tooling_cost, "detail": ""},
            {"item": "Labour", "cost": result.total_labour_cost, "detail": ""},
            {"item": "Power", "cost": result.total_power_cost, "detail": ""},
            {"item": "Overhead (15%)", "cost": result.overhead, "detail": ""},
            {"item": "Profit Margin (20%)", "cost": result.profit, "detail": ""},
        ])

        render_cost_table(lines)

        col1, col2 = st.columns(2)
        col1.metric("Unit Cost", f"₹{result.unit_cost:,.2f}")
        col2.metric("Order Cost", f"₹{result.order_cost:,.2f}", delta=f"{result.quantity} pcs")

        # --- Validation Display ---
        validation = st.session_state.get("mech_validation")
        if validation:
            st.subheader("🔍 AI Validation")
            delta = validation.comparison.delta_pct if validation.comparison else 0
            render_confidence_badge(validation.confidence_tier, delta, validation.degraded)

            if validation.ai_result and validation.comparison:
                render_validation_comparison(
                    validation.physics_result.unit_cost,
                    validation.ai_result.unit_cost_inr,
                    validation.comparison.delta_pct,
                )

            # Arbitration result (7-15% gap)
            if validation.arbitration:
                render_arbitration(validation.arbitration)

            # Interactive questions (>15% gap)
            if validation.interactive and validation.interactive.questions:
                answers = render_clarifying_questions(validation.interactive)
                if st.button("🔄 Recalculate with corrections", key="mech_recalc"):
                    st.session_state["mech_user_answers"] = answers
                    current_round = st.session_state.get("mech_round", 1)
                    st.session_state["mech_round"] = current_round + 1
                    st.rerun()

        # Historical comparison
        history_match = st.session_state.get("mech_history_match")
        render_historical_comparison(result.unit_cost, history_match)

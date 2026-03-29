# costimize-v2/ui/cable_tab.py
"""Cable Assembly tab — upload BOM, get should-cost breakdown."""

import streamlit as st
from engines.cable.bom_parser import parse_cable_bom, count_wires_and_connectors
from engines.cable.cost_engine import calculate_cable_cost
from extractors.bom_extractor import extract_bom_from_pdf
from engines.pcb.bom_parser import BomLine
from scrapers.component_scraper import get_component_price
from ui.components import render_cost_table, render_historical_comparison


def render():
    st.header("Cable Assembly — Should-Cost Breakdown")

    uploaded = st.file_uploader("Upload Cable BOM", type=["csv", "xlsx", "xls", "pdf"], key="cable_upload")

    if uploaded:
        file_bytes = uploaded.read()
        ext = uploaded.name.split(".")[-1].lower()

        if ext == "pdf":
            if st.button("🔍 Extract BOM from PDF", key="cable_extract"):
                with st.spinner("AI is extracting BOM from PDF..."):
                    try:
                        raw = extract_bom_from_pdf(file_bytes)
                        bom_lines = [
                            BomLine(mpn=c.get("mpn", ""), description=c.get("description", ""),
                                    quantity=int(c.get("quantity", 1)), footprint=c.get("footprint", ""),
                                    value=c.get("value", ""))
                            for c in raw
                        ]
                        st.session_state["cable_bom"] = bom_lines
                    except Exception as e:
                        st.error(f"PDF extraction failed: {e}")
                        return
        else:
            try:
                bom_lines = parse_cable_bom(file_bytes, uploaded.name)
                st.session_state["cable_bom"] = bom_lines
                st.success(f"Parsed {len(bom_lines)} components")
            except Exception as e:
                st.error(f"BOM parse failed: {e}")
                return

    bom_lines = st.session_state.get("cable_bom", [])
    if bom_lines:
        st.subheader(f"Cable BOM ({len(bom_lines)} items)")

        component_prices = []
        for i, line in enumerate(bom_lines):
            cols = st.columns([2, 3, 1, 1])
            cols[0].text(line.mpn or "—")
            cols[1].text(line.description or "—")
            cols[2].text(str(line.quantity))

            price_key = f"cable_price_{i}"
            existing = st.session_state.get(price_key)
            if existing:
                cols[3].text(f"₹{existing['unit_price']:.2f}")
            else:
                cols[3].text("—")

            component_prices.append({
                "mpn": line.mpn,
                "description": line.description,
                "quantity": line.quantity,
                "unit_price": existing["unit_price"] if existing else 0,
                "source": existing["source"] if existing else "not_found",
            })

        if st.button("🔍 Fetch Component Prices", key="cable_fetch"):
            progress = st.progress(0, text="Scraping prices...")
            for i, line in enumerate(bom_lines):
                if line.mpn:
                    result = get_component_price(line.mpn)
                    st.session_state[f"cable_price_{i}"] = result
                    component_prices[i]["unit_price"] = result["unit_price"]
                    component_prices[i]["source"] = result["source"]
                progress.progress((i + 1) / len(bom_lines), text=f"Fetching {i+1}/{len(bom_lines)}...")
            st.rerun()

    st.subheader("Cable Details")
    auto_wires, auto_connectors = count_wires_and_connectors(bom_lines) if bom_lines else (0, 0)
    col1, col2, col3 = st.columns(3)
    with col1:
        wire_count = st.number_input("Number of Wires", value=max(auto_wires, 4), min_value=1, key="cable_wires")
    with col2:
        connector_count = st.number_input("Number of Connectors", value=max(auto_connectors, 2), min_value=1, key="cable_connectors")
    with col3:
        quantity = st.number_input("Quantity", value=500, min_value=1, key="cable_qty")

    if st.button("💰 Calculate Should-Cost", key="cable_calc", type="primary"):
        if not bom_lines:
            st.error("Upload a cable BOM first.")
            return

        result = calculate_cable_cost(
            component_prices=component_prices,
            wire_count=wire_count,
            connector_count=connector_count,
            quantity=quantity,
        )
        st.session_state["cable_result"] = result

        from history.po_matcher import find_matching_po
        match = find_matching_po(
            part_description="Cable assembly " + " ".join(line.description for line in bom_lines[:3]),
        )
        st.session_state["cable_history_match"] = match

    result = st.session_state.get("cable_result")
    if result:
        st.subheader("📊 Should-Cost Breakdown")

        lines = [
            {"item": "Components", "cost": result.total_components_cost,
             "detail": f"{len(result.component_lines)} items"},
            {"item": "Labour", "cost": result.labour_cost,
             "detail": f"{result.labour_time_min:.1f} min ({result.wire_count} wires, {result.connector_count} connectors)"},
            {"item": "Overhead (15%)", "cost": result.overhead, "detail": ""},
            {"item": "Profit (20%)", "cost": result.profit, "detail": ""},
        ]
        render_cost_table(lines)

        col1, col2 = st.columns(2)
        col1.metric("Unit Cost", f"₹{result.unit_cost:,.2f}")
        col2.metric("Order Cost", f"₹{result.order_cost:,.2f}", delta=f"{result.quantity} cables")

        history_match = st.session_state.get("cable_history_match")
        render_historical_comparison(result.unit_cost, history_match)

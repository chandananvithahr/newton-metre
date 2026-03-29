# costimize-v2/ui/pcb_tab.py
"""PCB Assembly tab — upload BOM, scrape prices, get should-cost breakdown."""

import streamlit as st
from engines.pcb.bom_parser import parse_bom_file
from engines.pcb.cost_engine import calculate_pcb_cost
from extractors.bom_extractor import extract_bom_from_pdf
from scrapers.component_scraper import get_component_price
from engines.pcb.bom_parser import BomLine
from ui.components import render_cost_table, render_historical_comparison


def render():
    st.header("PCB Assembly — Should-Cost Breakdown")

    uploaded = st.file_uploader("Upload BOM", type=["csv", "xlsx", "xls", "pdf"], key="pcb_upload")

    if uploaded:
        file_bytes = uploaded.read()
        ext = uploaded.name.split(".")[-1].lower()

        if ext == "pdf":
            if st.button("🔍 Extract BOM from PDF", key="pcb_extract"):
                with st.spinner("AI is extracting BOM from PDF..."):
                    try:
                        raw_components = extract_bom_from_pdf(file_bytes)
                        bom_lines = [
                            BomLine(
                                mpn=c.get("mpn", ""),
                                description=c.get("description", ""),
                                quantity=int(c.get("quantity", 1)),
                                footprint=c.get("footprint", ""),
                                value=c.get("value", ""),
                            )
                            for c in raw_components
                        ]
                        st.session_state["pcb_bom"] = bom_lines
                    except Exception as e:
                        st.error(f"PDF extraction failed: {e}")
                        return
        else:
            try:
                bom_lines = parse_bom_file("", file_bytes=file_bytes, filename=uploaded.name)
                st.session_state["pcb_bom"] = bom_lines
                st.success(f"Parsed {len(bom_lines)} components from BOM")
            except Exception as e:
                st.error(f"BOM parse failed: {e}")
                return

    bom_lines = st.session_state.get("pcb_bom", [])
    if bom_lines:
        st.subheader(f"BOM ({len(bom_lines)} components)")

        component_prices = []
        for i, line in enumerate(bom_lines):
            cols = st.columns([2, 3, 1, 1, 1])
            cols[0].text(line.mpn or "—")
            cols[1].text(line.description or "—")
            cols[2].text(str(line.quantity))
            cols[3].text(line.footprint or "—")

            price_key = f"pcb_price_{i}"
            existing = st.session_state.get(price_key)
            if existing:
                cols[4].text(f"₹{existing['unit_price']:.2f}")
            else:
                cols[4].text("—")

            component_prices.append({
                "mpn": line.mpn,
                "description": line.description,
                "quantity": line.quantity,
                "unit_price": existing["unit_price"] if existing else 0,
                "source": existing["source"] if existing else "not_found",
            })

        if st.button("🔍 Fetch Component Prices", key="pcb_fetch"):
            progress = st.progress(0, text="Scraping prices...")
            for i, line in enumerate(bom_lines):
                if line.mpn:
                    result = get_component_price(line.mpn)
                    st.session_state[f"pcb_price_{i}"] = result
                    component_prices[i]["unit_price"] = result["unit_price"]
                    component_prices[i]["source"] = result["source"]
                progress.progress((i + 1) / len(bom_lines), text=f"Fetching {i+1}/{len(bom_lines)}...")
            st.rerun()

    st.subheader("Board Specifications")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        board_length = st.number_input("Board Length (mm)", value=80.0, min_value=1.0, key="pcb_length")
    with col2:
        board_width = st.number_input("Board Width (mm)", value=60.0, min_value=1.0, key="pcb_width")
    with col3:
        layers = st.selectbox("Layers", [1, 2, 4, 6, 8], index=1, key="pcb_layers")
    with col4:
        surface_finish = st.selectbox("Surface Finish", ["HASL", "Lead-free HASL", "ENIG", "OSP"], key="pcb_finish")

    col1, col2, col3 = st.columns(3)
    with col1:
        quantity = st.number_input("Quantity (boards)", value=100, min_value=1, key="pcb_qty")
    with col2:
        smd_pads = st.number_input("Total SMD Pads", value=87, min_value=0, key="pcb_smd")
    with col3:
        tht_pins = st.number_input("Total THT Pins", value=6, min_value=0, key="pcb_tht")

    if st.button("💰 Calculate Should-Cost", key="pcb_calc", type="primary"):
        if not bom_lines:
            st.error("Upload a BOM first.")
            return

        result = calculate_pcb_cost(
            component_prices=component_prices,
            board_length_mm=board_length,
            board_width_mm=board_width,
            layers=layers,
            quantity=quantity,
            smd_pads=smd_pads,
            tht_pins=tht_pins,
            surface_finish=surface_finish,
        )
        st.session_state["pcb_result"] = result

        from history.po_matcher import find_matching_po
        match = find_matching_po(
            part_description="PCB assembly " + " ".join(line.description for line in bom_lines[:3]),
        )
        st.session_state["pcb_history_match"] = match

    result = st.session_state.get("pcb_result")
    if result:
        st.subheader("📊 Should-Cost Breakdown")

        lines = [
            {"item": "Components (BOM)", "cost": result.total_components_cost,
             "detail": f"{len(result.component_lines)} line items"},
            {"item": "Bare Board Fabrication", "cost": result.board_fab_cost,
             "detail": f"{layers}L, {board_length}×{board_width}mm"},
            {"item": f"SMT Assembly ({result.smd_pads} pads)", "cost": result.smd_cost, "detail": ""},
            {"item": f"THT Assembly ({result.tht_pins} pins)", "cost": result.tht_cost, "detail": ""},
            {"item": "Stencil (amortized)", "cost": result.stencil_cost_per_board, "detail": ""},
            {"item": "Testing", "cost": result.test_cost, "detail": ""},
            {"item": "Overhead (15%)", "cost": result.overhead, "detail": ""},
            {"item": "Profit (20%)", "cost": result.profit, "detail": ""},
        ]
        render_cost_table(lines)

        col1, col2 = st.columns(2)
        col1.metric("Unit Cost", f"₹{result.unit_cost:,.2f}")
        col2.metric("Order Cost", f"₹{result.order_cost:,.2f}", delta=f"{result.quantity} boards")

        history_match = st.session_state.get("pcb_history_match")
        render_historical_comparison(result.unit_cost, history_match)

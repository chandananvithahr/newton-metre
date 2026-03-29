# costimize-v2/app.py
"""AI.Procurve — Should-Cost Intelligence for Procurement"""

import streamlit as st
from history.po_parser import parse_po_file
from history.po_store import save_records, load_all_records

st.set_page_config(
    page_title="AI.Procurve — Should-Cost Intelligence",
    page_icon="⚙",
    layout="wide",
)

# --- Sidebar: Historical PO Upload ---
with st.sidebar:
    st.header("📂 Historical PO Data")
    po_file = st.file_uploader("Upload previous POs", type=["csv", "xlsx", "xls"], key="po_upload")
    if po_file:
        try:
            records = parse_po_file(po_file.read(), po_file.name)
            added = save_records(records)
            st.success(f"Added {added} new PO records ({len(records)} total parsed)")
        except Exception as e:
            st.error(f"PO parse failed: {e}")

    existing = load_all_records()
    st.caption(f"{len(existing)} historical PO records loaded")

# --- Main ---
st.title("AI.Procurve — Should-Cost Intelligence")
st.caption("Upload a drawing or BOM. Get instant cost breakdown for negotiations.")

tab1, tab2, tab3, tab4 = st.tabs(["⚙ Mechanical Parts", "🔌 PCB Assembly", "🔗 Cable Assembly", "🔍 Similar Parts"])

with tab1:
    from ui.mechanical_tab import render as render_mechanical
    render_mechanical()

with tab2:
    from ui.pcb_tab import render as render_pcb
    render_pcb()

with tab3:
    from ui.cable_tab import render as render_cable
    render_cable()

with tab4:
    from ui.similarity_tab import render as render_similarity
    render_similarity()

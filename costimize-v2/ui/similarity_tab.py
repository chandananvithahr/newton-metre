"""Similarity search tab — upload drawing, find similar parts with cost intelligence."""

import streamlit as st
from engines.similarity.ranker import PRESET_WEIGHTS


def render():
    st.header("Similar Parts — Drawing Similarity Search")
    st.caption(
        "Upload a drawing to find similar parts from your archive. "
        "Get historical costs, physics should-cost, and supplier info."
    )

    # --- Search Mode ---
    mode = st.radio("Mode", ["Search", "Ingest Drawings"], horizontal=True, key="sim_mode")

    if mode == "Search":
        _render_search()
    else:
        _render_ingest()


def _render_search():
    """Search for similar drawings."""
    uploaded = st.file_uploader(
        "Upload drawing to search",
        type=["png", "jpg", "jpeg", "pdf", "dxf"],
        key="sim_search_upload",
    )

    # Optional filters
    col1, col2, col3 = st.columns(3)
    with col1:
        from engines.mechanical.material_db import list_material_names
        materials = ["Any"] + list_material_names()
        material_filter = st.selectbox("Material filter", materials, key="sim_mat")
    with col2:
        role = st.selectbox("Ranking priority", ["default", "designer", "procurement", "qa"], key="sim_role")
    with col3:
        top_k = st.slider("Results", 1, 20, 5, key="sim_topk")

    if uploaded and st.button("🔍 Find Similar Parts", key="sim_search_btn", type="primary"):
        image_bytes = uploaded.read()
        st.image(image_bytes, caption=f"Query: {uploaded.name}", width=300)

        with st.spinner("Searching archive... (embedding + FAISS + ranking)"):
            try:
                from engines.similarity.searcher import DrawingSearcher
                searcher = DrawingSearcher()

                if searcher.index_count == 0:
                    st.warning("No drawings indexed yet. Switch to 'Ingest Drawings' mode first.")
                    return

                mat = "" if material_filter == "Any" else material_filter
                weights = PRESET_WEIGHTS.get(role)
                results = searcher.search(
                    image_bytes=image_bytes,
                    filename=uploaded.name,
                    material=mat,
                    top_k=top_k,
                    weights=weights,
                )
                st.session_state["sim_results"] = results
            except ImportError as e:
                st.error(f"Missing dependency: {e}. Run: pip install torch torchvision faiss-cpu")
                return
            except Exception as e:
                st.error(f"Search failed: {e}")
                return

    # Display results
    results = st.session_state.get("sim_results", [])
    if results:
        st.subheader(f"Top {len(results)} Similar Parts")
        for r in results:
            with st.expander(
                f"#{r.rank} — {r.title or r.file_name} "
                f"({r.combined_score:.1%} match)",
                expanded=(r.rank <= 3),
            ):
                col1, col2 = st.columns([1, 2])
                with col1:
                    # Thumbnail
                    try:
                        st.image(r.thumbnail_path, width=200)
                    except Exception:
                        st.caption("(thumbnail not available)")

                with col2:
                    st.markdown(f"**Part:** {r.part_number or 'N/A'}")
                    st.markdown(f"**Material:** {r.material}")
                    st.markdown(f"**Processes:** {', '.join(r.processes)}")

                    dims = r.dimensions
                    if dims:
                        dim_str = ", ".join(
                            f"{k.replace('_mm', '').replace('_', ' ')}: {v}mm"
                            for k, v in dims.items() if v and v > 0
                        )
                        st.markdown(f"**Dimensions:** {dim_str}")

                # Score breakdown
                st.markdown("**Match Breakdown:**")
                score_cols = st.columns(4)
                score_cols[0].metric("Visual", f"{r.visual_score:.1%}")
                score_cols[1].metric("Material", f"{r.material_score:.1%}")
                score_cols[2].metric("Dimension", f"{r.dimension_score:.1%}")
                score_cols[3].metric("Process", f"{r.process_score:.1%}")

                # Cost intelligence (THE DIFFERENTIATOR)
                if r.historical_costs or r.physics_should_cost_inr > 0:
                    st.markdown("---")
                    st.markdown("**Cost Intelligence:**")
                    cost_cols = st.columns(3)

                    if r.historical_costs:
                        latest = r.historical_costs[-1]
                        cost_cols[0].metric(
                            "Last PO",
                            f"₹{latest.get('unit_price_inr', 0):,.0f}",
                            delta=f"{latest.get('supplier', 'N/A')}",
                            delta_color="off",
                        )

                    if r.physics_should_cost_inr > 0:
                        cost_cols[1].metric(
                            "Physics Should-Cost",
                            f"₹{r.physics_should_cost_inr:,.0f}",
                        )

                    if r.historical_costs and r.physics_should_cost_inr > 0:
                        latest_cost = r.historical_costs[-1].get("unit_price_inr", 0)
                        if latest_cost > 0:
                            target = (latest_cost + r.physics_should_cost_inr) / 2
                            delta = (latest_cost - r.physics_should_cost_inr) / latest_cost * 100
                            cost_cols[2].metric(
                                "Target Price",
                                f"₹{target:,.0f}",
                                delta=f"{delta:.1f}% savings potential",
                            )

                if r.notes:
                    st.caption(f"Notes: {r.notes}")


def _render_ingest():
    """Bulk ingest drawings into the search index."""
    st.subheader("Ingest Drawings")
    st.caption("Upload drawings to build your searchable archive.")

    uploaded_files = st.file_uploader(
        "Upload drawings (batch)",
        type=["png", "jpg", "jpeg", "pdf", "dxf"],
        accept_multiple_files=True,
        key="sim_ingest_upload",
    )

    if uploaded_files and st.button("📥 Ingest All", key="sim_ingest_btn", type="primary"):
        try:
            from engines.similarity.searcher import DrawingSearcher
            searcher = DrawingSearcher()
        except ImportError as e:
            st.error(f"Missing dependency: {e}. Run: pip install torch torchvision faiss-cpu")
            return

        progress = st.progress(0, text="Ingesting drawings...")
        success = 0
        errors = []

        for i, f in enumerate(uploaded_files):
            try:
                file_bytes = f.read()
                drawing_id = f"DWG-{i:04d}-{f.name}"

                # Try AI extraction for metadata
                metadata = {}
                try:
                    from extractors.vision import analyze_drawing
                    metadata = analyze_drawing(file_bytes, f.name)
                except Exception:
                    metadata = {"title": f.name, "material": "unknown", "processes": []}

                searcher.ingest(
                    file_bytes=file_bytes,
                    filename=f.name,
                    drawing_id=drawing_id,
                    metadata=metadata,
                )
                success += 1
            except Exception as e:
                errors.append(f"{f.name}: {e}")

            progress.progress((i + 1) / len(uploaded_files), text=f"Processing {f.name}...")

        searcher.save()
        progress.empty()

        st.success(f"Ingested {success}/{len(uploaded_files)} drawings. Index size: {searcher.index_count}")
        if errors:
            with st.expander(f"{len(errors)} errors"):
                for e in errors:
                    st.error(e)

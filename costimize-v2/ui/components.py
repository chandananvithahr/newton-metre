# costimize-v2/ui/components.py
"""Shared Streamlit UI widgets."""

import streamlit as st


def render_cost_table(lines: list[dict]):
    """Render a cost breakdown table. Each dict has 'item' and 'cost' keys, optionally 'detail'."""
    for line in lines:
        cols = st.columns([3, 1, 2])
        cols[0].write(f"**{line['item']}**")
        cols[1].write(f"₹{line['cost']:,.2f}")
        if line.get("detail"):
            cols[2].caption(line["detail"])
    st.divider()


def render_historical_comparison(should_cost: float, history_match: dict | None):
    """Render historical PO comparison box."""
    if not history_match:
        st.info("No historical data. Upload previous POs in the sidebar to enable comparison.")
        return

    prev_cost = history_match["unit_price"]
    diff = prev_cost - should_cost
    diff_pct = (diff / prev_cost) * 100 if prev_cost > 0 else 0
    color = "🟢" if diff > 0 else "🔴"

    st.markdown(f"""
    **Historical Comparison** {color}

    | | |
    |---|---|
    | Your should-cost | ₹{should_cost:,.2f}/unit |
    | Last PO ({history_match.get('date', 'N/A')}) | ₹{prev_cost:,.2f}/unit |
    | Difference | ₹{abs(diff):,.2f} ({abs(diff_pct):.1f}% {'over' if diff > 0 else 'under'}) |
    | Supplier | {history_match.get('supplier', 'N/A')} |
    | Qty | {history_match.get('quantity', 'N/A')} pcs |
    """)


def render_confidence_badge(confidence_tier, delta_pct: float, degraded: bool = False):
    """Show colored confidence badge based on validation result."""
    if degraded or confidence_tier is None:
        st.caption("⚪ Validation skipped — no drawing image for AI comparison")
        return

    from engines.validation.comparator import ConfidenceTier

    badge_config = {
        ConfidenceTier.HIGH: ("🟢", "High Confidence", f"Physics and AI agree within {delta_pct:.1f}%"),
        ConfidenceTier.MEDIUM: ("🟡", "Review Suggested", f"{delta_pct:.1f}% gap — verify dimensions"),
        ConfidenceTier.LOW: ("🟠", "AI Arbitration", f"{delta_pct:.1f}% gap — agent analyzed discrepancies"),
        ConfidenceTier.INSUFFICIENT: ("🔴", "Needs Clarification", f"{delta_pct:.1f}% gap — please verify inputs"),
    }

    icon, label, detail = badge_config.get(
        confidence_tier, ("⚪", "Unknown", ""),
    )
    st.markdown(f"**{icon} {label}** — {detail}")


def render_validation_comparison(physics_cost: float, ai_cost: float, delta_pct: float):
    """Side-by-side physics vs AI cost comparison."""
    col1, col2, col3 = st.columns(3)
    col1.metric("Physics Engine", f"₹{physics_cost:,.2f}")
    col2.metric("AI Estimate", f"₹{ai_cost:,.2f}")
    col3.metric("Delta", f"{delta_pct:.1f}%",
                delta=f"₹{abs(physics_cost - ai_cost):,.2f}",
                delta_color="off")


def render_arbitration(arbitration):
    """Show AI arbitration reasoning in an expander."""
    with st.expander("🤖 AI Arbitration Analysis", expanded=True):
        st.write(f"**Recommended cost:** ₹{arbitration.recommended_cost:,.2f}")
        st.write(f"**Source preferred:** {arbitration.source_preferred}")
        st.write(f"**Reasoning:** {arbitration.overall_reasoning}")
        if arbitration.line_discrepancies:
            st.write("**Line-by-line discrepancies:**")
            for disc in arbitration.line_discrepancies:
                st.write(f"- **{disc.get('item', '?')}**: "
                         f"Physics ₹{disc.get('physics_value', '?')}, "
                         f"AI ₹{disc.get('ai_value', '?')} — {disc.get('reasoning', '')}")


def render_clarifying_questions(interactive_round) -> dict:
    """Render clarifying questions as Streamlit widgets. Returns user answers."""
    st.warning(f"⚠️ {interactive_round.reason}")
    answers = {}
    for q in interactive_round.questions:
        st.markdown(f"**{q.question}**")
        st.caption(f"Current: {q.current_value} | AI detected: {q.ai_detected}")
        if q.options:
            if q.field in ("add_processes", "remove_processes"):
                selected = st.multiselect(
                    "Select", options=list(q.options),
                    default=list(q.options),
                    key=f"q_{q.field}",
                )
                answers[q.field] = selected
            else:
                selected = st.selectbox(
                    "Select", options=list(q.options),
                    key=f"q_{q.field}",
                )
                answers[q.field] = selected
        else:
            val = st.text_input("Enter value", value=q.current_value, key=f"q_{q.field}")
            answers[q.field] = val
    return answers

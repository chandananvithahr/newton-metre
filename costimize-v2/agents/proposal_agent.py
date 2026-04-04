"""ProposalAgent — generates procurement proposals with comparative statements.

Combines quote comparison + negotiation results into a management-ready
procurement proposal: comparative statement, savings report, risk assessment,
and vendor recommendation.
"""
import logging
import time

from agents.llm import call_llm, parse_json_response
from agents.types import AgentResult, WorkflowContext

logger = logging.getLogger("agents.proposal")

PROPOSAL_PROMPT = """Generate a procurement proposal based on this data.

QUOTE COMPARISON:
{comparison_summary}

NEGOTIATION RESULTS:
{negotiation_summary}

SHOULD-COST: Rs {should_cost:.2f}/unit
QUANTITY: {quantity} units

Generate a management-ready procurement proposal. Return JSON:
{{
  "executive_summary": "2-3 sentence summary of recommendation",
  "comparative_statement": [
    {{
      "supplier": "name",
      "unit_price": 0.0,
      "total_cost": 0.0,
      "delivery_weeks": 0,
      "vs_should_cost_pct": 0.0,
      "notes": "any special terms"
    }}
  ],
  "savings_analysis": {{
    "vs_highest_quote": 0.0,
    "vs_should_cost": 0.0,
    "vs_last_po": 0.0,
    "annual_savings_estimate": 0.0
  }},
  "risk_assessment": [
    {{
      "risk": "description",
      "severity": "high/medium/low",
      "mitigation": "how to mitigate"
    }}
  ],
  "recommendation": "Final recommendation with justification"
}}

Return ONLY JSON."""


class ProposalAgent:
    """Generates management-ready procurement proposals."""

    @property
    def name(self) -> str:
        return "proposal"

    def validate_inputs(self, inputs: dict) -> tuple[bool, str]:
        has_comparison = "quote_comparison" in inputs
        if not has_comparison:
            return False, "Need 'quote_comparison' data"
        return True, ""

    def execute(self, context: WorkflowContext, inputs: dict) -> AgentResult:
        start = time.perf_counter()

        comparison = inputs.get("quote_comparison", {})
        negotiation = inputs.get("negotiation", {})
        cost_data = inputs.get("cost", {})
        should_cost = cost_data.get("unit_cost", 0)
        quantity = inputs.get("quantity", context.inputs.get("quantity", 1))

        comparison_summary = self._format_comparison(comparison)
        negotiation_summary = self._format_negotiation(negotiation)

        try:
            response = call_llm(
                messages=[
                    {"role": "system", "content": "You are a procurement analyst preparing a proposal for management review."},
                    {"role": "user", "content": PROPOSAL_PROMPT.format(
                        comparison_summary=comparison_summary,
                        negotiation_summary=negotiation_summary,
                        should_cost=should_cost,
                        quantity=quantity,
                    )},
                ],
                json_mode=True,
            )
            proposal = parse_json_response(response.content)
        except Exception as exc:
            logger.exception("Proposal generation failed")
            return AgentResult(
                agent_name=self.name,
                status="error",
                error=str(exc),
                duration_ms=(time.perf_counter() - start) * 1000,
                llm_calls=1,
            )

        elapsed = (time.perf_counter() - start) * 1000
        return AgentResult(
            agent_name=self.name,
            status="success",
            data=proposal,
            duration_ms=elapsed,
            llm_calls=1,
        )

    def _format_comparison(self, comparison: dict) -> str:
        table = comparison.get("comparison_table", [])
        if not table:
            return "No quote comparison data available."
        lines = []
        for row in table:
            lines.append(
                f"- {row.get('supplier', '?')}: Rs {row.get('unit_price', 0):.2f}/unit, "
                f"delivery {row.get('delivery_weeks', '?')} weeks, "
                f"delta vs should-cost: {row.get('delta_pct', 0):.1f}%"
            )
        return "\n".join(lines)

    def _format_negotiation(self, negotiation: dict) -> str:
        if not negotiation:
            return "No negotiation conducted yet."
        return (
            f"Negotiated with {negotiation.get('vendor_name', '?')}: "
            f"original Rs {negotiation.get('vendor_quote', 0):.2f}, "
            f"target Rs {negotiation.get('target_price', 0):.2f}"
        )

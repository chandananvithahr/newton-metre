"""NegotiationAgent — generates counter-offers using should-cost + memory.

Supports three modes:
- AUTO (Class C): generates and could send counter-offer directly
- HITL (Class B): generates counter-offer, human approves before send
- MANUAL (Class A): generates analysis + talking points for human negotiator

Uses MESO (Multiple Equivalent Simultaneous Offers) strategy from Pactum research.
"""
import logging
import time

from agents.llm import call_llm, parse_json_response
from agents.memory import WorkingMemory, EpisodicMemory, SemanticMemory
from agents.types import AgentResult, ExecutionMode, WorkflowContext

logger = logging.getLogger("agents.negotiation")

NEGOTIATION_SYSTEM_PROMPT = """You are a senior procurement negotiator at an Indian manufacturing company.
Your goal is to get the best price while maintaining a good supplier relationship.

RULES:
- Be professional and respectful
- Use data-driven arguments (should-cost, market rates, history)
- Never reveal your exact target price or concession budget
- Offer MESO (Multiple Equivalent Simultaneous Offers) when possible
- Reference specific technical details to show expertise
"""

COUNTER_OFFER_PROMPT = """Generate a counter-offer for this negotiation.

{working_memory}

{episodic_context}

{semantic_context}

SHOULD-COST BREAKDOWN (internal reference, DO NOT share with vendor):
- Should-cost: Rs {should_cost:.2f}/unit
- Vendor quoted: Rs {vendor_quote:.2f}/unit
- Overprice: {overprice_pct:.1f}%

PART DETAILS:
- Material: {material}
- Processes: {processes}
- Quantity: {quantity}

Generate a counter-offer email using MESO strategy (2-3 equivalent options).

Return JSON:
{{
  "email_subject": "Re: Quotation for [part]",
  "email_body": "Professional counter-offer email text",
  "options": [
    {{
      "description": "Option description",
      "unit_price": 0.0,
      "terms": "payment/delivery terms"
    }}
  ],
  "primary_argument": "The main negotiation argument used",
  "talking_points": ["point 1", "point 2"],
  "risk_notes": "Any risks to highlight"
}}

Return ONLY JSON."""

ANALYSIS_PROMPT = """Generate a negotiation analysis and talking points for the procurement team.

{working_memory}

{episodic_context}

{semantic_context}

SHOULD-COST: Rs {should_cost:.2f}/unit
VENDOR QUOTE: Rs {vendor_quote:.2f}/unit
QUANTITY: {quantity}

Generate strategic advice. Return JSON:
{{
  "recommended_target": 0.0,
  "opening_position": 0.0,
  "walk_away_price": 0.0,
  "talking_points": ["point 1", "point 2", "point 3"],
  "supplier_weaknesses": ["known weakness 1"],
  "concession_strategy": "what to offer in exchange for price reduction",
  "risk_assessment": "assessment of negotiation risks"
}}

Return ONLY JSON."""


class NegotiationAgent:
    """Generates counter-offers or analysis based on execution mode."""

    def __init__(self):
        self._episodic = EpisodicMemory()
        self._semantic = SemanticMemory()

    @property
    def name(self) -> str:
        return "negotiation"

    def validate_inputs(self, inputs: dict) -> tuple[bool, str]:
        has_quotes = "quote_comparison" in inputs or "quotes" in inputs
        if not has_quotes:
            return False, "Need 'quote_comparison' or 'quotes' data"
        return True, ""

    def execute(self, context: WorkflowContext, inputs: dict) -> AgentResult:
        start = time.perf_counter()

        comparison = inputs.get("quote_comparison", {})
        cost_data = inputs.get("cost", {})
        should_cost = cost_data.get("unit_cost", 0)
        extraction = inputs.get("extraction", {})
        quantity = inputs.get("quantity", context.inputs.get("quantity", 1))

        # Get the vendor to negotiate with (best quote or specified)
        vendor_quote = comparison.get("best_unit_price", 0)
        vendor_name = comparison.get("best_supplier", "Vendor")

        if not vendor_quote and "quotes" in inputs:
            quotes = inputs["quotes"]
            if quotes:
                vendor_quote = quotes[0].get("unit_price", 0)
                vendor_name = quotes[0].get("supplier", {}).get("name", "Vendor")

        # Build working memory
        target_price = should_cost * 1.05 if should_cost > 0 else vendor_quote * 0.85
        working_mem = WorkingMemory(
            target_price=target_price,
            initial_quote=vendor_quote,
            current_offer=vendor_quote,
            max_rounds=inputs.get("max_rounds", 3),
            concession_budget_pct=inputs.get("concession_budget_pct", 5.0),
        )

        # Recall past negotiations
        supplier_id = inputs.get("supplier_id", "")
        episodes = self._episodic.recall(
            company_id=context.company_id,
            supplier_id=supplier_id if supplier_id else None,
            part_family=extraction.get("part_type", ""),
        )
        episodic_context = self._episodic.to_prompt_context(episodes)

        # Get supplier patterns
        patterns = self._semantic.get_patterns(context.company_id, supplier_id) if supplier_id else []
        semantic_context = self._semantic.to_prompt_context(patterns)

        # Generate based on execution mode
        overprice_pct = (
            (vendor_quote - should_cost) / should_cost * 100
            if should_cost > 0 else 0
        )

        try:
            if context.execution_mode == ExecutionMode.MANUAL:
                # Class A: analysis + talking points only
                result_data = self._generate_analysis(
                    working_mem, episodic_context, semantic_context,
                    should_cost, vendor_quote, quantity,
                )
            else:
                # Class B/C: generate counter-offer
                result_data = self._generate_counter_offer(
                    working_mem, episodic_context, semantic_context,
                    should_cost, vendor_quote, overprice_pct,
                    extraction, quantity,
                )

            result_data["vendor_name"] = vendor_name
            result_data["vendor_quote"] = vendor_quote
            result_data["should_cost"] = should_cost
            result_data["target_price"] = target_price
            result_data["execution_mode"] = context.execution_mode.value
            llm_calls = 1

        except Exception as exc:
            logger.exception("Negotiation agent failed")
            return AgentResult(
                agent_name=self.name,
                status="error",
                error=str(exc),
                duration_ms=(time.perf_counter() - start) * 1000,
            )

        elapsed = (time.perf_counter() - start) * 1000
        return AgentResult(
            agent_name=self.name,
            status="success",
            data=result_data,
            duration_ms=elapsed,
            llm_calls=llm_calls,
        )

    def _generate_counter_offer(
        self,
        working_mem: WorkingMemory,
        episodic_context: str,
        semantic_context: str,
        should_cost: float,
        vendor_quote: float,
        overprice_pct: float,
        extraction: dict,
        quantity: int,
    ) -> dict:
        prompt = COUNTER_OFFER_PROMPT.format(
            working_memory=working_mem.to_prompt_context(),
            episodic_context=episodic_context,
            semantic_context=semantic_context,
            should_cost=should_cost,
            vendor_quote=vendor_quote,
            overprice_pct=overprice_pct,
            material=extraction.get("material", "as per drawing"),
            processes=", ".join(extraction.get("processes", [])),
            quantity=quantity,
        )

        response = call_llm(
            messages=[
                {"role": "system", "content": NEGOTIATION_SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            json_mode=True,
        )
        return parse_json_response(response.content)

    def _generate_analysis(
        self,
        working_mem: WorkingMemory,
        episodic_context: str,
        semantic_context: str,
        should_cost: float,
        vendor_quote: float,
        quantity: int,
    ) -> dict:
        prompt = ANALYSIS_PROMPT.format(
            working_memory=working_mem.to_prompt_context(),
            episodic_context=episodic_context,
            semantic_context=semantic_context,
            should_cost=should_cost,
            vendor_quote=vendor_quote,
            quantity=quantity,
        )

        response = call_llm(
            messages=[
                {"role": "system", "content": NEGOTIATION_SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            json_mode=True,
        )
        return parse_json_response(response.content)

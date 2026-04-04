"""MeetingAgent — generates pre-meeting briefs and post-meeting analysis.

Two modes:
1. Pre-meeting brief: supplier history + should-cost + talking points
2. Post-meeting analysis: extract commitments, prices, action items from notes
"""
import logging
import time

from agents.llm import call_llm, parse_json_response
from agents.memory import EpisodicMemory, SemanticMemory
from agents.types import AgentResult, WorkflowContext

logger = logging.getLogger("agents.meeting")

BRIEF_PROMPT = """Generate a pre-meeting negotiation brief.

MEETING WITH: {supplier_name}
AGENDA: {agenda}

SHOULD-COST DATA:
{cost_context}

{episodic_context}

{semantic_context}

Generate a comprehensive brief. Return JSON:
{{
  "supplier_overview": "Brief supplier background",
  "key_data_points": ["data point 1", "data point 2"],
  "recommended_positions": [
    {{
      "item": "topic",
      "our_position": "what we want",
      "expected_resistance": "what they'll push back on",
      "fallback": "our compromise position"
    }}
  ],
  "talking_points": ["point 1", "point 2", "point 3"],
  "questions_to_ask": ["question 1", "question 2"],
  "warning_flags": ["flag 1"]
}}

Return ONLY JSON."""

POST_MEETING_PROMPT = """Analyze these meeting notes and extract key outcomes.

MEETING NOTES:
{notes}

CONTEXT:
- Supplier: {supplier_name}
- Our target: Rs {target_price:.2f}/unit
- Pre-meeting should-cost: Rs {should_cost:.2f}/unit

Extract all commitments and action items. Return JSON:
{{
  "price_agreements": [
    {{
      "item": "description",
      "agreed_price": 0.0,
      "vs_target": "above/below/at target"
    }}
  ],
  "commitments": [
    {{
      "by": "party name",
      "commitment": "what was committed",
      "deadline": "when"
    }}
  ],
  "action_items": [
    {{
      "owner": "person/team",
      "action": "what needs to be done",
      "deadline": "when"
    }}
  ],
  "unresolved": ["issue 1", "issue 2"],
  "sentiment": "positive/neutral/negative",
  "summary": "2-3 sentence meeting summary"
}}

Return ONLY JSON."""


class MeetingAgent:
    """Generates pre-meeting briefs and post-meeting analysis."""

    def __init__(self):
        self._episodic = EpisodicMemory()
        self._semantic = SemanticMemory()

    @property
    def name(self) -> str:
        return "meeting"

    def validate_inputs(self, inputs: dict) -> tuple[bool, str]:
        has_brief = "supplier_name" in inputs or "supplier_id" in inputs
        has_notes = "meeting_notes" in inputs
        if not (has_brief or has_notes):
            return False, "Need 'supplier_name'/'supplier_id' for brief or 'meeting_notes' for analysis"
        return True, ""

    def execute(self, context: WorkflowContext, inputs: dict) -> AgentResult:
        start = time.perf_counter()

        if "meeting_notes" in inputs:
            result_data = self._analyze_meeting(context, inputs)
        else:
            result_data = self._generate_brief(context, inputs)

        elapsed = (time.perf_counter() - start) * 1000
        return AgentResult(
            agent_name=self.name,
            status="success" if "error" not in result_data else "error",
            data=result_data,
            error=result_data.get("error"),
            duration_ms=elapsed,
            llm_calls=1,
        )

    def _generate_brief(self, context: WorkflowContext, inputs: dict) -> dict:
        supplier_name = inputs.get("supplier_name", "Unknown Supplier")
        supplier_id = inputs.get("supplier_id", "")
        agenda = inputs.get("agenda", "Price negotiation")
        cost_data = inputs.get("cost", {})

        cost_context = f"Should-cost: Rs {cost_data.get('unit_cost', 0):.2f}/unit" if cost_data else "No should-cost data"

        # Recall history
        episodes = self._episodic.recall(context.company_id, supplier_id or None)
        episodic_context = self._episodic.to_prompt_context(episodes)

        patterns = self._semantic.get_patterns(context.company_id, supplier_id) if supplier_id else []
        semantic_context = self._semantic.to_prompt_context(patterns)

        try:
            response = call_llm(
                messages=[
                    {"role": "system", "content": "You are a procurement intelligence analyst."},
                    {"role": "user", "content": BRIEF_PROMPT.format(
                        supplier_name=supplier_name,
                        agenda=agenda,
                        cost_context=cost_context,
                        episodic_context=episodic_context,
                        semantic_context=semantic_context,
                    )},
                ],
                json_mode=True,
            )
            brief = parse_json_response(response.content)
            brief["type"] = "pre_meeting_brief"
            brief["supplier"] = supplier_name
            return brief
        except Exception as exc:
            return {"error": str(exc), "type": "pre_meeting_brief"}

    def _analyze_meeting(self, context: WorkflowContext, inputs: dict) -> dict:
        notes = inputs["meeting_notes"]
        supplier_name = inputs.get("supplier_name", "Unknown")
        target_price = inputs.get("target_price", 0)
        should_cost = inputs.get("cost", {}).get("unit_cost", 0)

        try:
            response = call_llm(
                messages=[
                    {"role": "system", "content": "You are a procurement meeting analyst."},
                    {"role": "user", "content": POST_MEETING_PROMPT.format(
                        notes=notes,
                        supplier_name=supplier_name,
                        target_price=target_price,
                        should_cost=should_cost,
                    )},
                ],
                json_mode=True,
            )
            analysis = parse_json_response(response.content)
            analysis["type"] = "post_meeting_analysis"
            analysis["supplier"] = supplier_name
            return analysis
        except Exception as exc:
            return {"error": str(exc), "type": "post_meeting_analysis"}

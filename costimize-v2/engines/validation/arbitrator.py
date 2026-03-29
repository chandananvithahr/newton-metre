"""AI arbitrator agent — resolves 7-15% gaps between physics and AI estimates.

Sends both breakdowns to Gemini, asks it to analyze line-by-line WHY they differ,
and recommend which to trust. This is an AI AGENT — it reasons about discrepancies.
"""
import json
from dataclasses import dataclass
from config import GEMINI_API_KEY
from engines.mechanical.cost_engine import MechanicalCostBreakdown
from extractors.gemini_estimator import GeminiCostEstimate


@dataclass(frozen=True)
class ArbitrationResult:
    """Result of AI arbitration between physics and AI estimates."""
    recommended_cost: float
    source_preferred: str           # "physics" | "ai" | "blended"
    line_discrepancies: tuple[dict, ...]  # {"item", "physics_value", "ai_value", "reasoning"}
    overall_reasoning: str
    confidence_note: str


ARBITRATION_PROMPT = """You are a senior manufacturing cost analyst arbitrating between two independent cost estimates for the same part.

PHYSICS ENGINE ESTIMATE: ₹{physics_cost:.2f}/unit
{physics_breakdown}

AI (GEMINI) ESTIMATE: ₹{ai_cost:.2f}/unit
{ai_breakdown}

DELTA: {delta_pct:.1f}%
QUANTITY: {quantity} units

Analyze:
1. Which specific cost lines differ most? Why?
2. Which estimate's assumptions are more realistic for Indian job shop manufacturing?
3. What is the most likely correct cost?

Consider:
- Indian machine hour rates (₹600-1500/hr depending on process)
- Material prices in INR
- Whether processes listed are appropriate for the part geometry
- Whether machining times are realistic

Return ONLY a JSON object:
{{
  "recommended_cost": <your best estimate as number>,
  "source_preferred": "physics" or "ai" or "blended",
  "line_discrepancies": [
    {{"item": "<cost line>", "physics_value": <num>, "ai_value": <num>, "reasoning": "<why they differ>"}},
    ...
  ],
  "overall_reasoning": "<2-3 sentence explanation>",
  "confidence_note": "<how confident you are in this arbitration>"
}}

Return ONLY JSON. No markdown fences."""


def _format_physics_breakdown(result: MechanicalCostBreakdown) -> str:
    """Format physics result as readable text for the arbitration prompt."""
    lines = [f"  Material ({result.material_name}): ₹{result.material_cost:.2f} "
             f"({result.raw_weight_kg:.3f} kg + {result.wastage_weight_kg:.3f} kg wastage)"]
    for pl in result.process_lines:
        lines.append(
            f"  {pl.process_name}: ₹{pl.machine_cost:.2f} "
            f"({pl.time_min:.1f} min machining + ₹{pl.tooling_cost:.2f} tooling)"
        )
    lines.append(f"  Setup (amortized): ₹{result.total_setup_cost:.2f}")
    lines.append(f"  Labour: ₹{result.total_labour_cost:.2f}")
    lines.append(f"  Power: ₹{result.total_power_cost:.2f}")
    lines.append(f"  Overhead (15%): ₹{result.overhead:.2f}")
    lines.append(f"  Profit (20%): ₹{result.profit:.2f}")
    return "\n".join(lines)


def _format_ai_breakdown(estimate: GeminiCostEstimate) -> str:
    """Format AI estimate as readable text for the arbitration prompt."""
    lines = [
        f"  Material ({estimate.detected_material}): ₹{estimate.material_cost_inr:.2f}",
        f"  Machining: ₹{estimate.machining_cost_inr:.2f}",
        f"  Finishing: ₹{estimate.finishing_cost_inr:.2f}",
        f"  Overhead: ₹{estimate.overhead_inr:.2f}",
        f"  Processes detected: {', '.join(estimate.detected_processes)}",
        f"  Reasoning: {estimate.reasoning[:300]}",
    ]
    return "\n".join(lines)


def arbitrate(
    physics_result: MechanicalCostBreakdown,
    ai_result: GeminiCostEstimate,
    quantity: int,
    delta_pct: float,
) -> ArbitrationResult:
    """AI agent: analyze WHY two estimates differ and recommend which to trust.

    Sends both breakdowns to Gemini for line-by-line analysis.
    Falls back to physics if Gemini fails.
    """
    if not GEMINI_API_KEY:
        return _fallback_to_physics(physics_result, "No Gemini API key for arbitration")

    import google.generativeai as genai
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = ARBITRATION_PROMPT.format(
        physics_cost=physics_result.unit_cost,
        physics_breakdown=_format_physics_breakdown(physics_result),
        ai_cost=ai_result.unit_cost_inr,
        ai_breakdown=_format_ai_breakdown(ai_result),
        delta_pct=delta_pct,
        quantity=quantity,
    )

    try:
        response = model.generate_content([prompt])
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
        data = json.loads(text)
    except Exception:
        return _fallback_to_physics(physics_result, "Arbitration API/parse failed")

    discrepancies = data.get("line_discrepancies", [])

    return ArbitrationResult(
        recommended_cost=float(data.get("recommended_cost", physics_result.unit_cost)),
        source_preferred=str(data.get("source_preferred", "physics")),
        line_discrepancies=tuple(discrepancies),
        overall_reasoning=str(data.get("overall_reasoning", "")),
        confidence_note=str(data.get("confidence_note", "")),
    )


def _fallback_to_physics(
    physics_result: MechanicalCostBreakdown,
    reason: str,
) -> ArbitrationResult:
    """Fallback: trust the physics engine when arbitration fails."""
    return ArbitrationResult(
        recommended_cost=physics_result.unit_cost,
        source_preferred="physics",
        line_discrepancies=(),
        overall_reasoning=f"Defaulting to physics engine. {reason}",
        confidence_note="Arbitration unavailable — using physics estimate",
    )

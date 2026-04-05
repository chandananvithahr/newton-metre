"""Gemini end-to-end cost estimator — independent AI cost estimate from drawing image.

Sends the drawing directly to Gemini with a cost-estimation prompt (NOT dimension
extraction). Returns a structured cost estimate for comparison against the physics engine.
Uses Gemini (not OpenAI) to ensure independence from the primary extraction pipeline.
"""
import json
import base64
from dataclasses import dataclass
from config import GEMINI_API_KEY


@dataclass(frozen=True)
class GeminiCostEstimate:
    """Structured cost estimate from Gemini AI."""
    unit_cost_inr: float
    material_cost_inr: float
    machining_cost_inr: float
    finishing_cost_inr: float
    overhead_inr: float
    detected_material: str
    detected_processes: tuple[str, ...]
    detected_dimensions: dict
    reasoning: str
    model_used: str


COST_ESTIMATION_PROMPT = """You are an expert cost estimator for Indian manufacturing job shops.
Analyze this engineering drawing and estimate the manufacturing cost per unit in INR (₹).

Use these Indian job shop rates:
- CNC Turning: ₹800/hr
- CNC Milling: ₹1000/hr
- Drilling: ₹600/hr
- Grinding: ₹1200/hr
- Heat Treatment: ₹500/hr
- Surface Treatment: ₹400/hr
- Labour: ₹250/hr
- Power: ₹8/kWh
- Overhead: 15% of subtotal
- Profit margin: 20% of (subtotal + overhead)

Steps:
1. Identify the material, dimensions, and all manufacturing processes from the drawing
2. Estimate raw material cost (weight × price/kg)
3. Estimate machining time for each process (use MRR-based calculation)
4. Calculate machine cost, tooling, labour, power for each process
5. Add overhead and profit

QUANTITY: {quantity} units (amortize setup costs over this quantity)
{material_hint}

Return ONLY a JSON object:
{{
  "unit_cost_inr": <total cost per unit as number>,
  "material_cost_inr": <raw material cost per unit>,
  "machining_cost_inr": <total machining cost per unit>,
  "finishing_cost_inr": <surface treatment + heat treatment cost per unit>,
  "overhead_inr": <overhead + profit per unit>,
  "detected_material": "<material name>",
  "detected_processes": ["turning", "milling", ...],
  "detected_dimensions": {{"outer_diameter_mm": <num>, "length_mm": <num>, "inner_diameter_mm": <num>}},
  "reasoning": "<brief explanation of how you calculated each cost line>"
}}

Return ONLY the JSON. No markdown fences, no extra text."""


def estimate_cost_from_drawing(
    image_bytes: bytes,
    quantity: int = 100,
    material_hint: str = "",
) -> GeminiCostEstimate:
    """Send drawing to Gemini for an independent cost estimate.

    Args:
        image_bytes: Raw image bytes (PNG/JPEG)
        quantity: Batch size for amortizing setup costs
        material_hint: Optional hint like "Material hint: EN8 Steel"

    Returns:
        GeminiCostEstimate frozen dataclass

    Raises:
        RuntimeError: If GEMINI_API_KEY is not set
        ValueError: If Gemini returns unparseable response
    """
    if not GEMINI_API_KEY:
        raise RuntimeError(
            "Gemini API key required for validation. Set GEMINI_API_KEY in .env"
        )

    import google.generativeai as genai
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.0-flash-lite")

    hint_text = f"Material hint from user: {material_hint}" if material_hint else ""
    prompt = COST_ESTIMATION_PROMPT.format(
        quantity=quantity,
        material_hint=hint_text,
    )

    response = model.generate_content(
        [prompt, {"mime_type": "image/png", "data": image_bytes}],
        generation_config={"max_output_tokens": 2000, "temperature": 0.0},
    )

    text = response.text.strip()
    # Strip markdown code fences if present
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()

    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Gemini returned unparseable response: {text[:200]}... Error: {e}"
        )

    processes = data.get("detected_processes", [])
    if isinstance(processes, str):
        processes = [processes]

    return GeminiCostEstimate(
        unit_cost_inr=float(data.get("unit_cost_inr", 0)),
        material_cost_inr=float(data.get("material_cost_inr", 0)),
        machining_cost_inr=float(data.get("machining_cost_inr", 0)),
        finishing_cost_inr=float(data.get("finishing_cost_inr", 0)),
        overhead_inr=float(data.get("overhead_inr", 0)),
        detected_material=str(data.get("detected_material", "unknown")),
        detected_processes=tuple(processes),
        detected_dimensions=data.get("detected_dimensions", {}),
        reasoning=str(data.get("reasoning", "")),
        model_used="gemini-2.0-flash-lite",
    )

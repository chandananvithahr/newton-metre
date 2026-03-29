"""AI vision extraction — sends engineering drawings to GPT-4o/Gemini, returns structured data."""
import json
import base64
from config import OPENAI_API_KEY, GEMINI_API_KEY

EXTRACTION_PROMPT = """You are an expert mechanical engineer analyzing an engineering drawing.
Extract the following with EXTREME PRECISION. Only extract what you can clearly see.

Return a JSON object with these fields:
{
  "part_type": "turning" or "milling" or "general",
  "dimensions": {
    "outer_diameter_mm": <number or null>,
    "inner_diameter_mm": <number or null>,
    "length_mm": <number or null>,
    "width_mm": <number or null>,
    "height_mm": <number or null>,
    "hole_diameter_mm": <number or null>,
    "hole_count": <integer or null>,
    "thread_count": <integer or null>,
    "thread_length_mm": <number or null>,
    "groove_count": <integer or null>,
    "surface_area_cm2": <number or null>
  },
  "material": "<material name as written in drawing, or null>",
  "tolerances": {
    "has_tight_tolerances": <true if any tolerance < ±0.05mm>,
    "tightest_tolerance_mm": <number or null>
  },
  "surface_finish": "<Ra value or description, or null>",
  "suggested_processes": ["turning", "drilling", ...],
  "confidence": "high" or "medium" or "low",
  "notes": "<any relevant observations>"
}

CRITICAL:
- Read dimension text EXACTLY as written — do NOT guess
- Look for dimension callouts, leaders, dimension lines
- Check title blocks, notes, annotations
- If unclear, set confidence to "low"
- For suggested_processes, identify ALL manufacturing processes needed based on features you see.
  Valid process IDs: turning, facing, boring, milling_face, milling_slot, milling_pocket,
  drilling, reaming, tapping, threading, grinding_cylindrical, grinding_surface,
  knurling, broaching, heat_treatment, surface_treatment_plating,
  surface_treatment_anodizing, surface_treatment_painting

Return ONLY the JSON object, no markdown fences or extra text."""


def analyze_drawing(image_bytes: bytes, filename: str = "drawing.png") -> dict:
    if OPENAI_API_KEY:
        try:
            return _analyze_with_openai(image_bytes)
        except Exception as e:
            if GEMINI_API_KEY:
                return _analyze_with_gemini(image_bytes)
            raise RuntimeError(f"OpenAI failed and no Gemini fallback: {e}")
    if GEMINI_API_KEY:
        return _analyze_with_gemini(image_bytes)
    raise RuntimeError("No API key configured. Set OPENAI_API_KEY or GEMINI_API_KEY in .env")


def _analyze_with_openai(image_bytes: bytes) -> dict:
    import openai
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    b64 = base64.b64encode(image_bytes).decode("utf-8")
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": [
            {"type": "text", "text": EXTRACTION_PROMPT},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}},
        ]}],
        max_tokens=2000,
    )
    text = response.choices[0].message.content.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return json.loads(text)


def _analyze_with_gemini(image_bytes: bytes) -> dict:
    import google.generativeai as genai
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([
        EXTRACTION_PROMPT,
        {"mime_type": "image/png", "data": image_bytes},
    ])
    text = response.text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return json.loads(text)

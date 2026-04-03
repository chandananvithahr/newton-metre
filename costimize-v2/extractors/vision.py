"""AI vision extraction — sends engineering drawings to GPT-4o/Gemini, returns structured data."""
import json
import base64
import logging
from typing import Literal, Optional
from pydantic import BaseModel, Field, field_validator
from config import OPENAI_API_KEY, GEMINI_API_KEY

logger = logging.getLogger("costimize")

_VALID_PROCESSES = frozenset({
    "turning", "facing", "boring", "milling_face", "milling_slot", "milling_pocket",
    "drilling", "reaming", "tapping", "threading", "grinding_cylindrical",
    "grinding_surface", "knurling", "broaching", "heat_treatment",
    "surface_treatment_plating", "surface_treatment_anodizing", "surface_treatment_painting",
})


class _Dimensions(BaseModel):
    outer_diameter_mm: Optional[float] = None
    inner_diameter_mm: Optional[float] = None
    length_mm: Optional[float] = None
    width_mm: Optional[float] = None
    height_mm: Optional[float] = None
    hole_diameter_mm: Optional[float] = None
    hole_count: Optional[int] = None
    thread_count: Optional[int] = None
    thread_length_mm: Optional[float] = None
    groove_count: Optional[int] = None
    surface_area_cm2: Optional[float] = None


class _Tolerances(BaseModel):
    has_tight_tolerances: bool = False
    tightest_tolerance_mm: Optional[float] = None


class _ExtractionResult(BaseModel):
    part_type: Literal["turning", "milling", "general"] = "general"
    dimensions: _Dimensions = Field(default_factory=_Dimensions)
    material: Optional[str] = None
    tolerances: _Tolerances = Field(default_factory=_Tolerances)
    surface_finish: Optional[str] = None
    suggested_processes: list[str] = Field(default_factory=list)
    confidence: Literal["high", "medium", "low"] = "low"
    notes: Optional[str] = None

    @field_validator("suggested_processes")
    @classmethod
    def _filter_processes(cls, v: list[str]) -> list[str]:
        valid = [p for p in v if p in _VALID_PROCESSES]
        invalid = set(v) - _VALID_PROCESSES
        if invalid:
            logger.warning("LLM returned unknown processes (stripped): %s", invalid)
        return valid


def _parse_and_validate(text: str) -> dict:
    """Strip markdown fences, parse JSON, validate schema. Returns plain dict."""
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    # Fix common AI JSON issues: trailing commas, single quotes
    import re
    text = re.sub(r',\s*([}\]])', r'\1', text)  # remove trailing commas
    try:
        raw = json.loads(text)
    except json.JSONDecodeError:
        # Try fixing single quotes
        text = text.replace("'", '"')
        raw = json.loads(text)
    validated = _ExtractionResult.model_validate(raw)
    return validated.model_dump()


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


MULTI_VIEW_PROMPT_PREFIX = """You are an expert mechanical engineer analyzing MULTIPLE SHEETS of an engineering drawing for the SAME part.
These sheets show different views (front view, side view, section view, detail view, isometric) of a single manufactured part.

CRITICAL FIRST STEP — check if all sheets belong to the SAME part:
- Look for part numbers, drawing numbers, title blocks on each sheet
- Check if geometries are compatible (a shaft shown in two views vs two completely different parts)
- If the sheets appear to show DIFFERENT, UNRELATED parts, respond ONLY with:
  {"mismatch": true, "reason": "<brief explanation of why they differ>"}

If all sheets show the SAME part, extract COMPLETE information by combining all views.
Use each view to fill in dimensions that may not be visible in other views.

""" + EXTRACTION_PROMPT


def analyze_multi_view_drawing(images: list[bytes]) -> dict:
    """Analyze multiple drawing sheets for the same part. Raises ValueError on mismatch."""
    if len(images) == 1:
        return analyze_drawing(images[0])

    if GEMINI_API_KEY:
        try:
            return _analyze_multi_with_gemini(images)
        except ValueError:
            raise  # re-raise mismatch errors
        except Exception as e:
            if OPENAI_API_KEY:
                return _analyze_multi_with_openai(images)
            raise RuntimeError(f"Gemini failed and no OpenAI fallback: {e}")
    if OPENAI_API_KEY:
        return _analyze_multi_with_openai(images)
    raise RuntimeError("No API key configured.")


def _analyze_multi_with_gemini(images: list[bytes]) -> dict:
    import google.generativeai as genai
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    parts = [MULTI_VIEW_PROMPT_PREFIX]
    for i, img in enumerate(images):
        parts.append(f"\n--- Sheet {i + 1} of {len(images)} ---\n")
        parts.append({"mime_type": "image/png", "data": img})
    response = model.generate_content(parts, generation_config={"max_output_tokens": 2000})
    text = response.text.strip()
    return _check_mismatch_and_parse(text)


def _analyze_multi_with_openai(images: list[bytes]) -> dict:
    import openai
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    content = [{"type": "text", "text": MULTI_VIEW_PROMPT_PREFIX}]
    for i, img in enumerate(images):
        b64 = base64.b64encode(img).decode("utf-8")
        content.append({"type": "text", "text": f"\n--- Sheet {i + 1} of {len(images)} ---"})
        content.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}})
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": content}],
        max_tokens=2000,
    )
    text = response.choices[0].message.content.strip()
    return _check_mismatch_and_parse(text)


def _check_mismatch_and_parse(text: str) -> dict:
    """Detect mismatch response or parse normal extraction."""
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    try:
        raw = json.loads(text)
    except json.JSONDecodeError:
        raise RuntimeError("Invalid JSON from AI")
    if raw.get("mismatch"):
        raise ValueError(f"Drawing mismatch: {raw.get('reason', 'Sheets appear to be from different parts.')}")
    validated = _ExtractionResult.model_validate(raw)
    return validated.model_dump()


def analyze_drawing(image_bytes: bytes, filename: str = "drawing.png") -> dict:
    if GEMINI_API_KEY:
        try:
            return _analyze_with_gemini(image_bytes)
        except Exception as e:
            if OPENAI_API_KEY:
                return _analyze_with_openai(image_bytes)
            raise RuntimeError(f"Gemini failed and no OpenAI fallback: {e}")
    if OPENAI_API_KEY:
        return _analyze_with_openai(image_bytes)
    raise RuntimeError("No API key configured. Set GEMINI_API_KEY or OPENAI_API_KEY in .env")


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
    return _parse_and_validate(text)


def _analyze_with_gemini(image_bytes: bytes) -> dict:
    import google.generativeai as genai
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        [EXTRACTION_PROMPT, {"mime_type": "image/png", "data": image_bytes}],
        generation_config={"max_output_tokens": 2000},
    )
    text = response.text.strip()
    return _parse_and_validate(text)


STEP_EXTRACTION_PROMPT = """You are an expert mechanical engineer analyzing a 3D CAD file (STEP format).
The geometry has been extracted by Open CASCADE — you will see exact measurements, not raw STEP text.

How to interpret the data:
- BOUNDING BOX → overall part envelope (length × width × height in mm)
- CYLINDRICAL FEATURES → shafts, bores, holes. Largest Ø = likely OD. Smallest = likely bore/hole.
  Multiple faces at the same Ø = a single stepped diameter. ×2 faces typically = one complete cylinder.
- FACE ANALYSIS → planar faces = flat surfaces, cylindrical = round features, toroidal = fillets/chamfers
- PART TYPE HINT → "Rotational" = turned part, "Prismatic" = milled or sheet metal
- VOLUME + WEIGHT → use to verify material. If weight suggests steel but user says aluminium, flag it.
- SURFACE AREA → drives coating/plating cost

For turned parts: OD and length come from bounding box + largest cylinder. Stepped diameters from multiple cylinder radii.
For milled parts: length/width/height from bounding box. Pocket/slot features from small planar face counts.

""" + EXTRACTION_PROMPT


def analyze_step_text(step_text: str) -> dict:
    """Analyze a STEP file that has been converted to structured text."""
    if GEMINI_API_KEY:
        try:
            return _analyze_step_with_gemini(step_text)
        except Exception as e:
            if OPENAI_API_KEY:
                return _analyze_step_with_openai(step_text)
            raise RuntimeError(f"Gemini failed and no OpenAI fallback: {e}")
    if OPENAI_API_KEY:
        return _analyze_step_with_openai(step_text)
    raise RuntimeError("No API key configured.")


def _analyze_step_with_openai(step_text: str) -> dict:
    import openai
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": f"{STEP_EXTRACTION_PROMPT}\n\n{step_text}"}],
        max_tokens=2000,
    )
    return _parse_and_validate(response.choices[0].message.content.strip())


def _analyze_step_with_gemini(step_text: str) -> dict:
    import google.generativeai as genai
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        f"{STEP_EXTRACTION_PROMPT}\n\n{step_text}",
        generation_config={"max_output_tokens": 2000},
    )
    return _parse_and_validate(response.text.strip())

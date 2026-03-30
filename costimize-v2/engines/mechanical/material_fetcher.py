"""Dynamic material lookup for unknown materials.

When a material isn't in our database:
1. Ask Gemini for density, machinability, UTS, yield, hardness, price (INR/kg)
2. Build a Material object for the physics engine
3. Persist to data/materials.json + data/dynamic_materials.json so next call is instant
"""
import json
import logging
from pathlib import Path

from engines.mechanical.material_db import Material, DATA_FILE

logger = logging.getLogger("costimize")

DYNAMIC_PROPS_FILE = Path(__file__).parent.parent.parent / "data" / "dynamic_materials.json"

_FETCH_PROMPT = """You are a materials engineering database for Indian manufacturing.
For the material: {name}

Return a JSON object with EXACTLY these fields (numbers only, no units):
{{
  "density_kg_per_m3": <density in kg/m3, e.g. 2700 for aluminum>,
  "machinability": <0.0 to 1.0 — 1.0=free-cutting brass, 0.6=mild steel, 0.4=SS304, 0.25=titanium>,
  "uts_mpa": <ultimate tensile strength in MPa>,
  "yield_mpa": <yield strength in MPa>,
  "hardness_bhn": <Brinell hardness number>,
  "elongation_pct": <elongation at break in %>,
  "aisi_equivalent": "<closest AISI/ISO grade, or empty string>",
  "price_per_kg_inr": <typical raw material price in Indian Rupees per kg, current market>
}}

Be precise. If the material name is ambiguous, use the most common engineering grade.
Return ONLY the JSON object, no markdown or extra text."""


def fetch_material_from_ai(name: str) -> Material:
    """Fetch material properties from Gemini for any unknown material.
    Saves result to DB so future calls skip the AI lookup.
    Raises RuntimeError if AI lookup fails.
    """
    from config import GEMINI_API_KEY, OPENAI_API_KEY

    logger.info("Dynamic material lookup: %s", name)

    props = None
    if GEMINI_API_KEY:
        try:
            props = _fetch_with_gemini(name, GEMINI_API_KEY)
        except Exception as e:
            logger.warning("Gemini material fetch failed for %s: %s", name, e)

    if props is None and OPENAI_API_KEY:
        try:
            props = _fetch_with_openai(name, OPENAI_API_KEY)
        except Exception as e:
            logger.warning("OpenAI material fetch failed for %s: %s", name, e)

    if props is None:
        raise RuntimeError(f"Could not fetch properties for material '{name}' — no AI available.")

    material = Material(
        name=name,
        price_per_kg_inr=float(props.get("price_per_kg_inr", 100)),
        density_kg_per_m3=float(props.get("density_kg_per_m3", 7850)),
        machinability=float(props.get("machinability", 0.5)),
        uts_mpa=float(props.get("uts_mpa", 0)),
        yield_mpa=float(props.get("yield_mpa", 0)),
        hardness_bhn=float(props.get("hardness_bhn", 0)),
        elongation_pct=float(props.get("elongation_pct", 0)),
        aisi_equivalent=str(props.get("aisi_equivalent", "")),
    )

    _persist_material(material, props)
    logger.info("Dynamic material saved: %s (%.0f kg/m³, machinability=%.2f, ₹%.0f/kg)",
                name, material.density_kg_per_m3, material.machinability, material.price_per_kg_inr)

    return material


def _fetch_with_gemini(name: str, api_key: str) -> dict:
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        _FETCH_PROMPT.format(name=name),
        generation_config={"max_output_tokens": 500},
    )
    return _parse_props(response.text.strip())


def _fetch_with_openai(name: str, api_key: str) -> dict:
    import openai
    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": _FETCH_PROMPT.format(name=name)}],
        max_tokens=500,
    )
    return _parse_props(response.choices[0].message.content.strip())


def _parse_props(text: str) -> dict:
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return json.loads(text)


def _persist_material(material: Material, props: dict) -> None:
    """Save to data/materials.json (price+density) and data/dynamic_materials.json (full props)."""
    # 1. Update materials.json (used by load_materials())
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        existing_names = {m["name"] for m in data["materials"]}
        if material.name not in existing_names:
            data["materials"].append({
                "name": material.name,
                "price_per_kg_inr": material.price_per_kg_inr,
                "density_kg_per_m3": material.density_kg_per_m3,
                "machinability": material.machinability,
            })
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            logger.info("Appended %s to materials.json", material.name)
    except Exception as e:
        logger.warning("Could not update materials.json: %s", e)

    # 2. Save full mechanical properties to dynamic_materials.json
    try:
        DYNAMIC_PROPS_FILE.parent.mkdir(parents=True, exist_ok=True)
        existing: dict = {}
        if DYNAMIC_PROPS_FILE.exists():
            existing = json.loads(DYNAMIC_PROPS_FILE.read_text(encoding="utf-8"))
        existing[material.name] = props
        DYNAMIC_PROPS_FILE.write_text(json.dumps(existing, indent=2), encoding="utf-8")
    except Exception as e:
        logger.warning("Could not update dynamic_materials.json: %s", e)

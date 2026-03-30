# costimize-v2/extractors/bom_extractor.py
"""Extract BOM from PDF using AI vision (GPT-4o / Gemini)."""

import json
import base64
from config import OPENAI_API_KEY, GEMINI_API_KEY

BOM_PROMPT = """You are analyzing a Bill of Materials (BOM) document.
Extract ALL components into a structured JSON array.

Return ONLY a JSON object:
{
  "components": [
    {
      "mpn": "<manufacturer part number>",
      "description": "<component description>",
      "quantity": <integer>,
      "footprint": "<package/footprint>",
      "value": "<component value like 10K, 100nF>"
    }
  ]
}

Extract EVERY line item. If a field is unclear, use empty string "".
Return ONLY the JSON object, no markdown fences."""


def extract_bom_from_pdf(pdf_bytes: bytes) -> list[dict]:
    """Send PDF to vision AI, return list of component dicts."""
    if OPENAI_API_KEY:
        try:
            return _extract_openai(pdf_bytes)
        except Exception:
            if GEMINI_API_KEY:
                return _extract_gemini(pdf_bytes)
            raise
    if GEMINI_API_KEY:
        return _extract_gemini(pdf_bytes)
    raise RuntimeError("No API key. Set OPENAI_API_KEY or GEMINI_API_KEY.")


def _extract_openai(pdf_bytes: bytes) -> list[dict]:
    import openai
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    b64 = base64.b64encode(pdf_bytes).decode("utf-8")
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": BOM_PROMPT},
                {"type": "image_url", "image_url": {"url": f"data:application/pdf;base64,{b64}"}},
            ],
        }],
        max_tokens=4000,
    )
    text = response.choices[0].message.content.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return json.loads(text).get("components", [])


def _extract_gemini(pdf_bytes: bytes) -> list[dict]:
    import google.generativeai as genai
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        [BOM_PROMPT, {"mime_type": "application/pdf", "data": pdf_bytes}],
        generation_config={"max_output_tokens": 4000},
    )
    text = response.text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return json.loads(text).get("components", [])

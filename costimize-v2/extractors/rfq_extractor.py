"""RFQ extractor — pulls structured line items from Request for Quotation PDFs."""
import json
import logging
from typing import Optional, Literal

from pydantic import BaseModel, Field, field_validator

logger = logging.getLogger("costimize")

_VALID_PROCESSES = frozenset({
    "turning", "facing", "boring", "milling_face", "milling_slot", "milling_pocket",
    "drilling", "reaming", "tapping", "threading", "grinding_cylindrical",
    "grinding_surface", "knurling", "broaching", "heat_treatment",
    "surface_treatment_plating", "surface_treatment_anodizing", "surface_treatment_painting",
})

_RFQ_EXTRACTION_PROMPT = """You are an expert procurement analyst for an Indian manufacturing company.
Extract structured data from this RFQ (Request for Quotation) document.

DOCUMENT TEXT:
---
{text}
---

Return ONLY a JSON object with this exact structure:
{{
  "rfq_number": "<RFQ/enquiry number from document, or null>",
  "customer": "<customer/company name, or null>",
  "date": "<date as written in document, or null>",
  "line_items": [
    {{
      "line_number": <sequential integer starting at 1>,
      "part_number": "<part number or item code, or null>",
      "description": "<full part description as written>",
      "quantity": <integer quantity required>,
      "material": "<material specification as written, e.g. SS304, MS, EN8, Al6061, or null>",
      "delivery_weeks": <integer delivery requirement in weeks, or null>,
      "dimensions": {{
        "outer_diameter_mm": <number or null — for shafts/cylinders>,
        "inner_diameter_mm": <number or null — for bores/holes>,
        "length_mm": <number or null>,
        "width_mm": <number or null>,
        "height_mm": <number or null>,
        "hole_count": <integer or null>,
        "thread_count": <integer or null>
      }},
      "suggested_processes": ["turning", "drilling", ...],
      "unit_price_expected": <number in INR if customer mentioned expected price, else null>,
      "notes": "<any special requirements: tolerances, surface finish, standards, inspection>"
    }}
  ],
  "confidence": "high" | "medium" | "low"
}}

EXTRACTION RULES:
- Extract ALL line items visible — do not skip any
- For dimensions: parse from description text (e.g. "50mm dia x 120mm L" → outer_diameter_mm: 50, length_mm: 120)
- For suggested_processes: infer from description (shaft → turning, plate → milling_face, hole pattern → drilling)
  Valid process IDs: turning, facing, boring, milling_face, milling_slot, milling_pocket,
  drilling, reaming, tapping, threading, grinding_cylindrical, grinding_surface,
  knurling, broaching, heat_treatment, surface_treatment_plating,
  surface_treatment_anodizing, surface_treatment_painting
- confidence "high": clear table with all columns visible
- confidence "medium": some info missing but main items clear
- confidence "low": document unclear, few items extracted, or not clearly an RFQ
- If no line items found, return empty array

Return ONLY the JSON object, no markdown fences or extra text."""


class _RFQDimensions(BaseModel):
    outer_diameter_mm: Optional[float] = None
    inner_diameter_mm: Optional[float] = None
    length_mm: Optional[float] = None
    width_mm: Optional[float] = None
    height_mm: Optional[float] = None
    hole_count: Optional[int] = None
    thread_count: Optional[int] = None


class _RFQLineItem(BaseModel):
    line_number: int
    part_number: Optional[str] = None
    description: str
    quantity: int = 1
    material: Optional[str] = None
    delivery_weeks: Optional[int] = None
    dimensions: _RFQDimensions = Field(default_factory=_RFQDimensions)
    suggested_processes: list[str] = Field(default_factory=list)
    unit_price_expected: Optional[float] = None
    notes: Optional[str] = None

    @field_validator("suggested_processes")
    @classmethod
    def _filter_processes(cls, v: list[str]) -> list[str]:
        valid = [p for p in v if p in _VALID_PROCESSES]
        invalid = set(v) - _VALID_PROCESSES
        if invalid:
            logger.warning("RFQ extractor stripped unknown processes: %s", invalid)
        return valid

    @field_validator("quantity")
    @classmethod
    def _clamp_quantity(cls, v: int) -> int:
        return max(1, v)


class _RFQDocument(BaseModel):
    rfq_number: Optional[str] = None
    customer: Optional[str] = None
    date: Optional[str] = None
    line_items: list[_RFQLineItem] = Field(default_factory=list)
    confidence: Literal["high", "medium", "low"] = "low"


def extract_rfq(pdf_bytes: bytes) -> dict:
    """Extract all pages text from PDF and return structured RFQ data.

    Returns dict matching _RFQDocument structure plus page_count.
    """
    text, page_count = _extract_all_text(pdf_bytes)

    if not text.strip():
        return {
            "rfq_number": None, "customer": None, "date": None,
            "line_items": [], "confidence": "low", "page_count": page_count,
        }

    try:
        result = _extract_with_gemini(text)
    except Exception as e:
        logger.warning("Gemini RFQ extraction failed: %s — trying OpenAI", e)
        try:
            result = _extract_with_openai(text)
        except Exception as e2:
            logger.error("Both RFQ extractors failed: %s", e2)
            return {
                "rfq_number": None, "customer": None, "date": None,
                "line_items": [], "confidence": "low", "page_count": page_count,
            }

    result["page_count"] = page_count
    return result


def _extract_all_text(pdf_bytes: bytes) -> tuple[str, int]:
    import fitz  # PyMuPDF

    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    page_count = len(doc)
    pages_text: list[str] = []
    for page in doc:
        pages_text.append(page.get_text())
    doc.close()
    full_text = "\n\n--- PAGE BREAK ---\n\n".join(pages_text)
    return full_text[:12000], page_count  # cap at 12K chars


def _parse_rfq(text: str) -> dict:
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    raw = json.loads(text)
    validated = _RFQDocument.model_validate(raw)
    return validated.model_dump()


def _extract_with_openai(text: str) -> dict:
    from config import OPENAI_API_KEY
    import openai

    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    prompt = _RFQ_EXTRACTION_PROMPT.format(text=text)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4000,
        response_format={"type": "json_object"},
    )
    return _parse_rfq(response.choices[0].message.content.strip())


def _extract_with_gemini(text: str) -> dict:
    from config import GEMINI_API_KEY
    import google.generativeai as genai

    genai.configure(api_key=GEMINI_API_KEY)
    # Use 1.5-pro for RFQ extraction — better at long structured tables than flash
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = _RFQ_EXTRACTION_PROMPT.format(text=text)
    response = model.generate_content(prompt, generation_config={"max_output_tokens": 4000})
    return _parse_rfq(response.text.strip())

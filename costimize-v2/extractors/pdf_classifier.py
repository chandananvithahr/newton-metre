"""PDF classifier — identifies document type from first two pages of text."""
import json
import logging
from typing import Literal

from pydantic import BaseModel

logger = logging.getLogger("costimize")

DocumentType = Literal["rfq", "drawing", "contract", "spec_sheet", "other"]

_CLASSIFY_PROMPT = """You are a document classification expert for an Indian manufacturing company.
Analyze the following text extracted from the first pages of a PDF and classify it.

Document text:
---
{text}
---

Classify this document. Return ONLY a JSON object:
{{
  "document_type": "rfq" | "drawing" | "contract" | "spec_sheet" | "other",
  "confidence": "high" | "medium" | "low",
  "reason": "<one sentence explaining your classification>"
}}

Classification rules:
- "rfq": Request for Quotation — contains line items with part descriptions, quantities needed, delivery dates. May say "RFQ", "Enquiry", "Request for Quote", "Quotation Request".
- "drawing": Engineering drawing or technical drawing — contains dimension callouts, tolerances, GD&T symbols, title blocks.
- "contract": Purchase order or contract — contains agreed prices, payment terms, legal clauses, signatures.
- "spec_sheet": Technical specification or datasheet — contains material specs, test requirements, standards (MIL-SPEC, IS, ASTM), property tables.
- "other": None of the above.

Return ONLY the JSON object, no markdown fences."""


class _ClassificationResult(BaseModel):
    document_type: DocumentType = "other"
    confidence: Literal["high", "medium", "low"] = "low"
    reason: str = ""


def classify_pdf(pdf_bytes: bytes) -> dict:
    """Extract text from first two pages and classify document type.

    Returns dict with keys: document_type, confidence, reason.
    Falls back to "other" with low confidence if classification fails.
    """
    text = _extract_first_pages_text(pdf_bytes, max_pages=2)
    if not text.strip():
        return {"document_type": "other", "confidence": "low", "reason": "No extractable text found"}

    try:
        return _classify_with_gemini(text)
    except Exception as e:
        logger.warning("Gemini classify failed: %s — trying OpenAI", e)
        try:
            return _classify_with_openai(text)
        except Exception as e2:
            logger.error("Both classifiers failed: %s", e2)
            return {"document_type": "other", "confidence": "low", "reason": "Classification failed"}


def _extract_first_pages_text(pdf_bytes: bytes, max_pages: int = 2) -> str:
    import fitz  # PyMuPDF

    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    pages_text: list[str] = []
    for i, page in enumerate(doc):
        if i >= max_pages:
            break
        pages_text.append(page.get_text())
    doc.close()
    return "\n".join(pages_text)[:4000]  # cap at 4K chars for the prompt


def _parse_classification(text: str) -> dict:
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    raw = json.loads(text)
    validated = _ClassificationResult.model_validate(raw)
    return validated.model_dump()


def _classify_with_openai(text: str) -> dict:
    from config import OPENAI_API_KEY
    import openai

    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    prompt = _CLASSIFY_PROMPT.format(text=text)
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # classification is cheap — use mini
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
    )
    return _parse_classification(response.choices[0].message.content.strip())


def _classify_with_gemini(text: str) -> dict:
    from config import GEMINI_API_KEY
    import google.generativeai as genai

    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.0-flash-lite")
    prompt = _CLASSIFY_PROMPT.format(text=text)
    response = model.generate_content(prompt, generation_config={"max_output_tokens": 200, "temperature": 0.0})
    return _parse_classification(response.text.strip())

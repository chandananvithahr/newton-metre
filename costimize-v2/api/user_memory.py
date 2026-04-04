"""Mem0-style user memory layer for the chat agent.

Extracts preferences and patterns from chat turns, persists them to
Supabase `user_memory` table, and injects them into future sessions.
The agent "remembers" returning users without them repeating themselves.

Design:
- Extraction runs AFTER a reply is sent (non-blocking, best-effort)
- Injection runs BEFORE building messages (fast Supabase lookup)
- upsert pattern: one row per user per key — confidence increases with repetition
- Never extracts PII or sensitive business data — only manufacturing preferences
"""

import logging
import json
import re
from typing import Optional

logger = logging.getLogger("costimize")

# Keys the extractor looks for
MEMORY_KEYS = [
    "preferred_material",
    "typical_batch_size",
    "preferred_region",
    "part_type",
    "tolerance_class",
    "surface_finish",
    "industry_sector",
    "currency_preference",
]

_EXTRACTION_PROMPT = """You are extracting user preferences from a manufacturing cost conversation.

Given the user message below, extract any of these preference keys if clearly stated:
- preferred_material: main material they work with (e.g. "EN8 steel", "Aluminum 6061", "SS304")
- typical_batch_size: typical production quantity (e.g. "500 units", "1000 pieces", "small batches")
- preferred_region: city/region for cost comparison (e.g. "Bangalore", "Pune", "Chennai")
- part_type: type of parts they work with (e.g. "turned parts", "sheet metal", "PCB assemblies")
- tolerance_class: typical tolerance requirement (e.g. "tight <0.05mm", "medium", "general")
- surface_finish: common surface treatment (e.g. "zinc plating", "anodizing", "bare")
- industry_sector: their industry (e.g. "defense", "automotive", "aerospace")
- currency_preference: preferred currency (e.g. "INR", "USD")

User message: {message}

Return JSON only. Include only keys that are clearly stated. Empty object {{}} if nothing extractable.
Example: {{"preferred_material": "EN8 steel", "typical_batch_size": "500 units"}}"""


def _call_llm_extract(message: str, gemini_key: str) -> dict:
    """Call Gemini Flash to extract preferences. Returns {} on any error."""
    try:
        import google.generativeai as genai
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel("gemini-2.0-flash-lite")
        prompt = _EXTRACTION_PROMPT.format(message=message[:500])
        response = model.generate_content(prompt)
        text = response.text.strip()
        # Strip markdown fences
        text = re.sub(r"^```(?:json)?\n?", "", text)
        text = re.sub(r"\n?```$", "", text)
        parsed = json.loads(text)
        # Only keep known keys with string values
        return {k: str(v) for k, v in parsed.items() if k in MEMORY_KEYS and v}
    except Exception as e:
        logger.debug("Memory extraction skipped: %s", e)
        return {}


def extract_and_save(
    user_id: str,
    message: str,
    sb,
    gemini_key: Optional[str],
) -> None:
    """Extract preferences from message and upsert into user_memory.

    Called after each successful chat reply. Best-effort — never raises.
    """
    if not gemini_key or not message.strip():
        return

    try:
        extracted = _call_llm_extract(message, gemini_key)
        if not extracted:
            return

        for key, value in extracted.items():
            # Upsert: if key exists, increment confidence (max 3); else insert at 2
            existing = (
                sb.table("user_memory")
                .select("id, confidence")
                .eq("user_id", user_id)
                .eq("key", key)
                .execute()
            )
            if existing.data:
                row = existing.data[0]
                new_confidence = min(3, row["confidence"] + 1)
                sb.table("user_memory").update({
                    "value": value,
                    "confidence": new_confidence,
                    "updated_at": "now()",
                }).eq("id", row["id"]).execute()
            else:
                sb.table("user_memory").insert({
                    "user_id": user_id,
                    "key": key,
                    "value": value,
                    "confidence": 2,
                    "source": "chat_extraction",
                }).execute()

        logger.debug("Saved %d memory keys for user %s", len(extracted), user_id[:8])

    except Exception as e:
        logger.debug("Memory save failed (non-critical): %s", e)


def load_user_context(user_id: str, sb) -> str:
    """Load user memory and format as context string.

    Returns empty string if no memory exists yet.
    """
    try:
        resp = (
            sb.table("user_memory")
            .select("key, value, confidence")
            .eq("user_id", user_id)
            .order("confidence", desc=True)
            .limit(10)
            .execute()
        )
        rows = resp.data or []
        if not rows:
            return ""

        lines = ["=== USER CONTEXT (remembered from past sessions) ==="]
        for row in rows:
            key_label = row["key"].replace("_", " ").title()
            lines.append(f"- {key_label}: {row['value']}")
        lines.append("Use this context to give personalized answers without asking again.")
        return "\n".join(lines)

    except Exception as e:
        logger.debug("Failed to load user memory: %s", e)
        return ""

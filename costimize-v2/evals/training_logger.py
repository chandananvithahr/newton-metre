"""Training data logger — logs every AI API call as future fine-tuning data.

Every cloud API interaction becomes a training example:
- Extraction: (image, model_output, user_correction) → fine-tune Qwen2.5-VL-7B
- Agent: (user_message, tool_calls, response, feedback) → fine-tune Qwen2.5-32B
- Similarity: (query, results, confirmed/rejected) → fine-tune DINOv2 embeddings

Data is stored in:
- Local JSONL files: costimize-v2/data/training/{extraction,agent,similarity}.jsonl
- Supabase tables (when available): training_extractions, training_conversations, training_similarity

Usage:
    from evals.training_logger import log_extraction, log_agent_turn, log_similarity_feedback

    # After extraction
    log_extraction(image_bytes, model_output, model_name="gemini-2.0-flash-lite")

    # After user corrects extraction
    log_extraction_correction(extraction_id, corrections={"material": "SS316"})

    # After agent conversation turn
    log_agent_turn(user_message, tool_calls, final_response, model_name="gemini-2.0-flash-lite")

    # After user confirms/rejects similarity result
    log_similarity_feedback(query_id, result_id, relevant=True)
"""
import json
import hashlib
import logging
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional

logger = logging.getLogger("costimize.training")

DATA_DIR = Path(__file__).parent.parent / "data" / "training"


def _ensure_dirs() -> None:
    """Create training data directories if they don't exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def _append_jsonl(filepath: Path, record: dict) -> None:
    """Append a JSON record to a JSONL file."""
    _ensure_dirs()
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, default=str, ensure_ascii=False) + "\n")


def _generate_id(prefix: str) -> str:
    """Generate a unique ID for a training record."""
    timestamp = str(time.time()).encode()
    return f"{prefix}_{hashlib.md5(timestamp).hexdigest()[:12]}"


# --- Extraction Training Data ---

@dataclass
class ExtractionRecord:
    """A single extraction training example."""
    record_id: str
    timestamp: float
    model_name: str
    image_hash: str  # MD5 of image bytes (for dedup)
    image_path: Optional[str]  # Path if saved to disk
    model_output: dict  # Raw extraction result
    user_corrections: Optional[dict]  # If user corrected any fields
    is_corrected: bool
    confidence: str
    latency_ms: float


def log_extraction(
    image_bytes: bytes,
    model_output: dict,
    model_name: str = "unknown",
    latency_ms: float = 0.0,
    save_image: bool = False,
) -> str:
    """Log an extraction API call. Returns the record ID."""
    record_id = _generate_id("ext")
    image_hash = hashlib.md5(image_bytes).hexdigest()

    image_path = None
    if save_image:
        images_dir = DATA_DIR / "images"
        images_dir.mkdir(exist_ok=True)
        image_path = str(images_dir / f"{image_hash}.png")
        with open(image_path, "wb") as f:
            f.write(image_bytes)

    record = ExtractionRecord(
        record_id=record_id,
        timestamp=time.time(),
        model_name=model_name,
        image_hash=image_hash,
        image_path=image_path,
        model_output=model_output,
        user_corrections=None,
        is_corrected=False,
        confidence=model_output.get("confidence", "unknown"),
        latency_ms=latency_ms,
    )

    _append_jsonl(DATA_DIR / "extraction.jsonl", asdict(record))
    logger.info("Logged extraction %s (model=%s, confidence=%s)",
                record_id, model_name, record.confidence)
    return record_id


def log_extraction_correction(
    record_id: str,
    corrections: dict,
) -> None:
    """Log user corrections to an extraction. Creates a gold-label training pair."""
    correction_record = {
        "record_id": record_id,
        "timestamp": time.time(),
        "corrections": corrections,
        "type": "correction",
    }
    _append_jsonl(DATA_DIR / "extraction.jsonl", correction_record)
    logger.info("Logged correction for %s: %s", record_id, list(corrections.keys()))


# --- Agent Training Data ---

@dataclass
class AgentTurnRecord:
    """A single agent conversation turn."""
    record_id: str
    conversation_id: str
    timestamp: float
    model_name: str
    user_message: str
    context: dict  # Page context (which estimate/page user is viewing)
    tool_calls: list[dict]  # [{name, args, result_summary}]
    final_response: str
    user_feedback: Optional[str]  # thumbs_up, thumbs_down, correction
    latency_ms: float


def log_agent_turn(
    user_message: str,
    tool_calls: list[dict],
    final_response: str,
    conversation_id: str = "",
    context: Optional[dict] = None,
    model_name: str = "unknown",
    latency_ms: float = 0.0,
) -> str:
    """Log an agent conversation turn. Returns the record ID."""
    record_id = _generate_id("agt")

    record = AgentTurnRecord(
        record_id=record_id,
        conversation_id=conversation_id or _generate_id("conv"),
        timestamp=time.time(),
        model_name=model_name,
        user_message=user_message,
        context=context or {},
        tool_calls=tool_calls,
        final_response=final_response,
        user_feedback=None,
        latency_ms=latency_ms,
    )

    _append_jsonl(DATA_DIR / "agent.jsonl", asdict(record))
    logger.info("Logged agent turn %s (tools=%s)",
                record_id, [tc.get("name") for tc in tool_calls])
    return record_id


def log_agent_feedback(
    record_id: str,
    feedback: str,  # "thumbs_up", "thumbs_down", or free text
) -> None:
    """Log user feedback on an agent response."""
    feedback_record = {
        "record_id": record_id,
        "timestamp": time.time(),
        "feedback": feedback,
        "type": "feedback",
    }
    _append_jsonl(DATA_DIR / "agent.jsonl", feedback_record)
    logger.info("Logged agent feedback for %s: %s", record_id, feedback)


# --- Similarity Training Data ---

@dataclass
class SimilarityFeedbackRecord:
    """User feedback on a similarity search result."""
    record_id: str
    timestamp: float
    query_drawing_id: str
    result_drawing_id: str
    relevance: str  # "confirmed", "rejected", "partial"
    similarity_score: float
    embedder_used: str
    user_comment: Optional[str]


def log_similarity_feedback(
    query_drawing_id: str,
    result_drawing_id: str,
    relevant: bool,
    similarity_score: float = 0.0,
    embedder_used: str = "unknown",
    comment: Optional[str] = None,
) -> str:
    """Log user feedback on a similarity search result. Returns the record ID."""
    record_id = _generate_id("sim")

    record = SimilarityFeedbackRecord(
        record_id=record_id,
        timestamp=time.time(),
        query_drawing_id=query_drawing_id,
        result_drawing_id=result_drawing_id,
        relevance="confirmed" if relevant else "rejected",
        similarity_score=similarity_score,
        embedder_used=embedder_used,
        user_comment=comment,
    )

    _append_jsonl(DATA_DIR / "similarity.jsonl", asdict(record))
    logger.info("Logged similarity feedback %s: %s→%s (%s)",
                record_id, query_drawing_id, result_drawing_id, record.relevance)
    return record_id


# --- Stats ---

def get_training_stats() -> dict:
    """Get counts of logged training data."""
    stats = {}
    for name in ("extraction", "agent", "similarity"):
        filepath = DATA_DIR / f"{name}.jsonl"
        if filepath.exists():
            with open(filepath) as f:
                lines = [l for l in f if l.strip()]
            total = len(lines)
            corrections = sum(1 for l in lines if '"type": "correction"' in l or '"type": "feedback"' in l)
            stats[name] = {"total": total, "with_feedback": corrections}
        else:
            stats[name] = {"total": 0, "with_feedback": 0}
    return stats


def print_training_stats() -> None:
    """Print training data collection progress."""
    stats = get_training_stats()
    print(f"\n{'='*50}")
    print(f"  TRAINING DATA COLLECTION STATUS")
    print(f"{'='*50}")
    for name, counts in stats.items():
        milestone = ""
        if name == "extraction":
            if counts["total"] >= 200:
                milestone = " → READY for Qwen2.5-VL-7B fine-tune"
            elif counts["total"] >= 50:
                milestone = f" → {200 - counts['total']} more for fine-tune"
        elif name == "agent":
            if counts["total"] >= 500:
                milestone = " → READY for Qwen2.5-32B fine-tune"
            elif counts["total"] >= 100:
                milestone = f" → {500 - counts['total']} more for fine-tune"
        elif name == "similarity":
            if counts["with_feedback"] >= 500:
                milestone = " → READY for DINOv2 fine-tune"
            elif counts["with_feedback"] >= 50:
                milestone = f" → {500 - counts['with_feedback']} more for fine-tune"

        print(f"  {name:15s}: {counts['total']:5d} records "
              f"({counts['with_feedback']} with feedback){milestone}")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    print_training_stats()

"""Persist validated cost estimates as JSON for future ML training.

Follows the same pattern as history/po_store.py — append-only JSON file.
"""
import json
from dataclasses import dataclass, asdict
from pathlib import Path


VALIDATION_DIR = Path(__file__).parent.parent.parent / "data" / "validation"
try:
    VALIDATION_DIR.mkdir(parents=True, exist_ok=True)
except PermissionError:
    # In containerized deployments, /app may be read-only — use /tmp instead
    VALIDATION_DIR = Path("/tmp/validation")
    VALIDATION_DIR.mkdir(parents=True, exist_ok=True)
VALIDATION_FILE = VALIDATION_DIR / "validated_estimates.json"


@dataclass(frozen=True)
class ValidatedEstimate:
    """A single validated cost estimate — training data for Phase 4 ML."""
    timestamp: str
    drawing_filename: str
    material_name: str
    dimensions: dict
    processes: tuple[str, ...]
    quantity: int
    physics_cost: float
    ai_cost: float | None
    final_cost: float
    confidence_tier: str
    delta_pct: float
    user_corrections: dict
    arbitration_reasoning: str | None


def save_validated_estimate(estimate: ValidatedEstimate) -> None:
    """Append a validated estimate to the JSON store. Dedup by timestamp + material."""
    existing = load_validated_estimates()
    existing_keys = {
        (r.get("timestamp", ""), r.get("material_name", ""), r.get("drawing_filename", ""))
        for r in existing
    }
    record = asdict(estimate)
    # Convert tuple to list for JSON serialization
    record["processes"] = list(record["processes"])
    key = (record["timestamp"], record["material_name"], record["drawing_filename"])
    if key not in existing_keys:
        existing.append(record)
        VALIDATION_FILE.write_text(
            json.dumps(existing, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )


def load_validated_estimates() -> list[dict]:
    """Load all validated estimates from JSON store."""
    if not VALIDATION_FILE.exists():
        return []
    try:
        return json.loads(VALIDATION_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def count_validated_estimates() -> int:
    """Count total validated estimates — useful for tracking ML readiness."""
    return len(load_validated_estimates())


def export_training_data() -> dict:
    """Export validated estimates in ML-ready format.

    Returns a summary with:
    - total_pairs: number of validated estimates
    - ml_ready: True if 50+ pairs (minimum for correction factors)
    - high_confidence_pairs: estimates where physics+AI agreed (cleanest training data)
    - cost_pairs: list of (physics_cost, ai_cost, final_cost) tuples for regression
    - material_distribution: count per material
    - process_distribution: count per process

    This is the training data pipeline: raw data → structured export → Phase 4 ML.
    """
    records = load_validated_estimates()
    high_conf = [r for r in records if r.get("confidence_tier") == "high"]

    material_counts: dict[str, int] = {}
    process_counts: dict[str, int] = {}
    cost_pairs = []

    for r in records:
        mat = r.get("material_name", "unknown")
        material_counts[mat] = material_counts.get(mat, 0) + 1

        for p in r.get("processes", []):
            process_counts[p] = process_counts.get(p, 0) + 1

        cost_pairs.append({
            "physics": r.get("physics_cost", 0),
            "ai": r.get("ai_cost"),
            "final": r.get("final_cost", 0),
            "material": mat,
            "confidence": r.get("confidence_tier", "unknown"),
        })

    return {
        "total_pairs": len(records),
        "ml_ready": len(records) >= 50,
        "high_confidence_pairs": len(high_conf),
        "cost_pairs": cost_pairs,
        "material_distribution": material_counts,
        "process_distribution": process_counts,
    }

# costimize-v2/history/po_store.py
"""Store and retrieve historical PO data as JSON."""

import json
from pathlib import Path

HISTORY_DIR = Path(__file__).parent.parent / "data" / "history"
HISTORY_DIR.mkdir(parents=True, exist_ok=True)
HISTORY_FILE = HISTORY_DIR / "po_records.json"


def load_all_records() -> list[dict]:
    if not HISTORY_FILE.exists():
        return []
    try:
        return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_records(records: list[dict]):
    existing = load_all_records()
    existing_keys = {
        (r.get("part_number", ""), r.get("supplier", ""), r.get("date", ""))
        for r in existing
    }
    new_records = [
        r for r in records
        if (r.get("part_number", ""), r.get("supplier", ""), r.get("date", "")) not in existing_keys
    ]
    all_records = existing + new_records
    HISTORY_FILE.write_text(json.dumps(all_records, indent=2, ensure_ascii=False), encoding="utf-8")
    return len(new_records)

# costimize-v2/history/po_matcher.py
"""Match current estimate to historical PO records."""

from history.po_store import load_all_records


def find_matching_po(part_number: str = "", part_description: str = "") -> dict | None:
    records = load_all_records()
    if not records:
        return None

    if part_number:
        pn_lower = part_number.lower().strip()
        matches = [r for r in records if r.get("part_number", "").lower().strip() == pn_lower]
        if matches:
            return _most_recent(matches)

    if part_description:
        desc_words = set(part_description.lower().split())
        best_match = None
        best_score = 0
        for record in records:
            record_desc = record.get("part_description", "").lower()
            record_words = set(record_desc.split())
            if not record_words:
                continue
            overlap = len(desc_words & record_words)
            score = overlap / max(len(desc_words), 1)
            if score > best_score and score >= 0.3:
                best_score = score
                best_match = record

        return best_match

    return None


def _most_recent(records: list[dict]) -> dict:
    sorted_records = sorted(records, key=lambda r: r.get("date", ""), reverse=True)
    return sorted_records[0]

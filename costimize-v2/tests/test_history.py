# costimize-v2/tests/test_history.py
import io
import json
import pandas as pd
from history.po_parser import parse_po_file
from history.po_store import load_all_records, save_records, HISTORY_FILE
from history.po_matcher import find_matching_po


def test_parse_po_excel():
    df = pd.DataFrame({
        "Part Number": ["SHAFT-001", "GEAR-002"],
        "Description": ["Steel shaft 60mm OD", "Spur gear module 2"],
        "Unit Price": [3450, 1200],
        "Qty": [200, 500],
        "Supplier": ["ABC Engg Pune", "XYZ Gears Mumbai"],
        "PO Date": ["2025-03-15", "2025-02-10"],
    })
    buf = io.BytesIO()
    df.to_excel(buf, index=False)
    buf.seek(0)
    records = parse_po_file(buf.read(), "po_history.xlsx")
    assert len(records) == 2
    assert records[0]["part_number"] == "SHAFT-001"
    assert records[0]["unit_price"] == 3450
    assert records[0]["supplier"] == "ABC Engg Pune"


def test_po_store_round_trip(tmp_path, monkeypatch):
    monkeypatch.setattr("history.po_store.HISTORY_FILE", tmp_path / "po_records.json")
    records = [
        {"part_number": "SHAFT-001", "part_description": "Steel shaft", "unit_price": 3450,
         "quantity": 200, "supplier": "ABC Engg", "date": "2025-03-15"},
    ]
    added = save_records(records)
    assert added == 1
    loaded = load_all_records()
    assert len(loaded) == 1
    assert loaded[0]["part_number"] == "SHAFT-001"


def test_po_matcher_exact_part_number(tmp_path, monkeypatch):
    monkeypatch.setattr("history.po_matcher.load_all_records",
                        lambda: [{"part_number": "SHAFT-001", "part_description": "Steel shaft 60mm",
                                  "unit_price": 3450, "quantity": 200, "supplier": "ABC Engg", "date": "2025-03-15"}])
    match = find_matching_po(part_number="SHAFT-001")
    assert match is not None
    assert match["unit_price"] == 3450


def test_po_matcher_description_fallback(tmp_path, monkeypatch):
    monkeypatch.setattr("history.po_matcher.load_all_records",
                        lambda: [{"part_number": "SHAFT-001", "part_description": "Steel shaft 60mm OD turning",
                                  "unit_price": 3450, "quantity": 200, "supplier": "ABC", "date": "2025-03"}])
    match = find_matching_po(part_description="Steel shaft 60mm machined")
    assert match is not None
    assert match["unit_price"] == 3450


def test_po_matcher_no_match(tmp_path, monkeypatch):
    monkeypatch.setattr("history.po_matcher.load_all_records", lambda: [])
    match = find_matching_po(part_number="NONEXISTENT")
    assert match is None

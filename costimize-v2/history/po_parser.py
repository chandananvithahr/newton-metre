# costimize-v2/history/po_parser.py
"""Parse historical PO files (Excel/CSV). Direct column mapping, no AI needed."""

import pandas as pd
from pathlib import Path

HEADER_MAP = {
    "part_description": ["part description", "description", "item description", "part name", "item", "component"],
    "part_number": ["part number", "part no", "part_no", "pn", "item number", "item no", "mpn"],
    "unit_price": ["unit price", "price", "rate", "unit rate", "cost", "unit cost", "price per unit"],
    "quantity": ["quantity", "qty", "qty.", "order qty", "order quantity"],
    "supplier": ["supplier", "vendor", "supplier name", "vendor name"],
    "date": ["date", "po date", "order date", "purchase date"],
}


def _match_column(columns: list[str], candidates: list[str]) -> str | None:
    lower_cols = {c.lower().strip(): c for c in columns}
    for candidate in candidates:
        if candidate in lower_cols:
            return lower_cols[candidate]
    return None


def parse_po_file(file_bytes: bytes, filename: str) -> list[dict]:
    import io
    ext = Path(filename).suffix.lower()
    if ext in (".xlsx", ".xls"):
        df = pd.read_excel(io.BytesIO(file_bytes))
    else:
        df = pd.read_csv(io.BytesIO(file_bytes))

    columns = list(df.columns)
    col_map = {field: _match_column(columns, candidates) for field, candidates in HEADER_MAP.items()}

    records = []
    for _, row in df.iterrows():
        desc = str(row.get(col_map["part_description"], "")).strip() if col_map["part_description"] else ""
        pn = str(row.get(col_map["part_number"], "")).strip() if col_map["part_number"] else ""

        try:
            price = float(row.get(col_map["unit_price"], 0)) if col_map["unit_price"] else 0
        except (ValueError, TypeError):
            price = 0

        try:
            qty = int(float(row.get(col_map["quantity"], 0))) if col_map["quantity"] else 0
        except (ValueError, TypeError):
            qty = 0

        supplier = str(row.get(col_map["supplier"], "")).strip() if col_map["supplier"] else ""
        date_val = row.get(col_map["date"], "") if col_map["date"] else ""
        date_str = str(date_val).strip() if date_val else ""

        if not desc and not pn:
            continue

        records.append({
            "part_description": desc,
            "part_number": pn,
            "unit_price": price,
            "quantity": qty,
            "supplier": supplier,
            "date": date_str,
        })

    return records

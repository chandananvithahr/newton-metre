# costimize-v2/engines/pcb/bom_parser.py
"""Parse PCB BOM from CSV/Excel files. Auto-detect column mapping."""

import pandas as pd
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class BomLine:
    mpn: str  # Manufacturer Part Number
    description: str
    quantity: int
    footprint: str
    value: str  # e.g., "10K", "100nF"


# Common header variations for auto-detection
HEADER_MAP = {
    "mpn": ["mpn", "manufacturer part number", "mfr part", "part number", "mfg part", "mfr_part_number", "manufacturer_part"],
    "description": ["description", "desc", "part description", "component", "name"],
    "quantity": ["quantity", "qty", "count", "amount", "qty."],
    "footprint": ["footprint", "package", "case", "size", "pkg"],
    "value": ["value", "val", "rating", "specification"],
}


def _match_column(columns: list[str], candidates: list[str]) -> str | None:
    """Find the first column name that matches any candidate (case-insensitive)."""
    lower_cols = {c.lower().strip(): c for c in columns}
    for candidate in candidates:
        if candidate in lower_cols:
            return lower_cols[candidate]
    return None


def parse_bom_file(file_path: str | Path, file_bytes: bytes | None = None, filename: str = "") -> list[BomLine]:
    """
    Parse a BOM file (CSV or Excel) and return normalized BOM lines.
    Accepts either a file path or raw bytes + filename.
    """
    if file_bytes:
        import io
        ext = Path(filename).suffix.lower()
        if ext in (".xlsx", ".xls"):
            df = pd.read_excel(io.BytesIO(file_bytes))
        else:
            df = pd.read_csv(io.BytesIO(file_bytes))
    else:
        ext = Path(file_path).suffix.lower()
        if ext in (".xlsx", ".xls"):
            df = pd.read_excel(file_path)
        else:
            df = pd.read_csv(file_path)

    columns = list(df.columns)

    # Auto-detect column mapping
    mpn_col = _match_column(columns, HEADER_MAP["mpn"])
    desc_col = _match_column(columns, HEADER_MAP["description"])
    qty_col = _match_column(columns, HEADER_MAP["quantity"])
    fp_col = _match_column(columns, HEADER_MAP["footprint"])
    val_col = _match_column(columns, HEADER_MAP["value"])

    lines = []
    for _, row in df.iterrows():
        mpn = str(row.get(mpn_col, "")).strip() if mpn_col else ""
        desc = str(row.get(desc_col, "")).strip() if desc_col else ""
        footprint = str(row.get(fp_col, "")).strip() if fp_col else ""
        value = str(row.get(val_col, "")).strip() if val_col else ""

        try:
            qty = int(float(row.get(qty_col, 1))) if qty_col else 1
        except (ValueError, TypeError):
            qty = 1

        if not mpn and not desc:
            continue  # skip empty rows

        lines.append(BomLine(mpn=mpn, description=desc, quantity=qty, footprint=footprint, value=value))

    return lines

# costimize-v2/engines/cable/bom_parser.py
"""Parse cable assembly BOM — connectors, wires, terminals, etc."""

from engines.pcb.bom_parser import parse_bom_file, BomLine


def parse_cable_bom(file_bytes: bytes, filename: str) -> list[BomLine]:
    """Parse cable BOM. Same format as PCB BOM — CSV/Excel with part numbers and quantities."""
    return parse_bom_file("", file_bytes=file_bytes, filename=filename)


def count_wires_and_connectors(bom_lines: list[BomLine]) -> tuple[int, int]:
    wire_count = 0
    connector_count = 0

    wire_keywords = ["wire", "cable", "awg", "conductor"]
    connector_keywords = ["connector", "plug", "socket", "header", "jst", "molex", "terminal"]

    for line in bom_lines:
        desc_lower = (line.description + " " + line.mpn).lower()
        if any(kw in desc_lower for kw in wire_keywords):
            wire_count += line.quantity
        elif any(kw in desc_lower for kw in connector_keywords):
            connector_count += line.quantity

    return wire_count, connector_count

"""Direct CAD file extraction — no PNG conversion, no quality loss.

DXF / DWG  → structured text via ezdxf entity traversal
STEP       → structured text via ISO-10303-21 parsing
"""
from __future__ import annotations

import re
import tempfile
from pathlib import Path


# ── DXF / DWG direct extraction ───────────────────────────────────────────────

def dxf_to_text(file_bytes: bytes, filename: str = "drawing.dxf") -> str:
    """Extract all engineering data from a DXF or DWG file using ezdxf.

    Traverses entities in modelspace and paper space to collect:
    - DIMENSION entities (exact numeric values)
    - TEXT / MTEXT (annotations, title block, notes, tolerances)
    - CIRCLE / ARC (radii → diameters)
    - LINE (lengths, though usually less reliable without context)

    Returns structured text the AI can read directly.
    """
    try:
        import ezdxf
    except ImportError as exc:
        raise RuntimeError("ezdxf not installed. Run: pip install ezdxf") from exc

    with tempfile.NamedTemporaryFile(
        suffix=Path(filename).suffix or ".dxf", delete=False
    ) as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    try:
        doc = ezdxf.readfile(tmp_path)
    finally:
        Path(tmp_path).unlink(missing_ok=True)

    sections: list[str] = ["=== DXF/DWG FILE CONTENTS ===", ""]

    # ── Header variables (units, limits) ──────────────────────────────────────
    header = doc.header
    insunits = header.get("$INSUNITS", None)
    unit_label = {
        0: "unitless", 1: "inches", 2: "feet", 4: "mm",
        5: "cm", 6: "m", 14: "dm",
    }.get(insunits, f"code {insunits}")
    sections.append(f"UNITS: {unit_label}")
    sections.append("")

    # ── Title block / drawing info from named layout or block TITLE ───────────
    title_texts: list[str] = []
    for block in doc.blocks:
        bname = block.name.upper()
        if any(k in bname for k in ("TITLE", "BORDER", "SHEET", "HEAD", "TB")):
            for e in block:
                if e.dxftype() in ("TEXT", "MTEXT") and hasattr(e, "dxf"):
                    val = (getattr(e.dxf, "text", None) or "").strip()
                    if val:
                        title_texts.append(val)

    if title_texts:
        sections.append("TITLE BLOCK / ANNOTATIONS:")
        for t in title_texts[:40]:
            sections.append(f"  {t}")
        sections.append("")

    # ── Modelspace entities ───────────────────────────────────────────────────
    msp = doc.modelspace()
    dimensions: list[str] = []
    texts: list[str] = []
    circles: list[str] = []
    leaders: list[str] = []

    for entity in msp:
        dtype = entity.dxftype()

        if dtype == "DIMENSION":
            try:
                val = entity.dxf.get("actual_measurement", None)
                dim_type = entity.dimtype & 7  # 0=linear,2=angular,3=diameter,4=radius
                type_label = {0: "linear", 2: "angular", 3: "diameter", 4: "radius"}.get(dim_type, "dim")
                override = entity.dxf.get("text", "")
                if val is not None:
                    entry = f"{type_label}: {val:.4f} {unit_label}"
                    if override and override != "<>":
                        entry += f"  [text: {override}]"
                    dimensions.append(entry)
                elif override and override != "<>":
                    dimensions.append(f"{type_label}: {override}")
            except Exception:
                pass

        elif dtype in ("TEXT", "MTEXT"):
            try:
                val = (getattr(entity.dxf, "text", None) or "").strip()
                # Strip ezdxf MTEXT control codes
                val = re.sub(r"\\[A-Za-z][^;]*;", "", val)
                val = re.sub(r"\{[^}]*\}", "", val).strip()
                if val and len(val) > 1:
                    texts.append(val)
            except Exception:
                pass

        elif dtype == "CIRCLE":
            try:
                r = entity.dxf.radius
                circles.append(f"circle  radius={r:.4f} {unit_label}  diameter={r*2:.4f} {unit_label}")
            except Exception:
                pass

        elif dtype == "ARC":
            try:
                r = entity.dxf.radius
                circles.append(f"arc  radius={r:.4f} {unit_label}  diameter={r*2:.4f} {unit_label}")
            except Exception:
                pass

        elif dtype in ("LEADER", "MULTILEADER"):
            try:
                val = entity.dxf.get("text_string", "").strip()
                if val:
                    leaders.append(val)
            except Exception:
                pass

    if dimensions:
        sections.append(f"DIMENSIONS ({len(dimensions)} found):")
        for d in dimensions:
            sections.append(f"  {d}")
        sections.append("")

    if circles:
        sections.append(f"CIRCLES / ARCS ({len(circles)} found):")
        for c in circles[:50]:
            sections.append(f"  {c}")
        sections.append("")

    if texts:
        sections.append(f"TEXT ANNOTATIONS ({len(texts)} found):")
        for t in texts[:60]:
            sections.append(f"  {t}")
        sections.append("")

    if leaders:
        sections.append(f"LEADERS ({len(leaders)} found):")
        for l in leaders[:20]:
            sections.append(f"  {l}")
        sections.append("")

    return "\n".join(sections)


# ── STEP direct extraction ─────────────────────────────────────────────────────

_RE_CYLINDER = re.compile(
    r"#\d+\s*=\s*CYLINDRICAL_SURFACE\s*\([^)]*\)\s*;", re.IGNORECASE
)
_RE_PRODUCT = re.compile(
    r"#\d+\s*=\s*PRODUCT\s*\(\s*'([^']*)',\s*'([^']*)'", re.IGNORECASE
)
_RE_MATERIAL = re.compile(
    r"#\d+\s*=\s*MATERIAL\s*\(\s*'([^']*)'", re.IGNORECASE
)
_RE_MEASURE = re.compile(
    r"#(\d+)\s*=\s*MEASURE_WITH_UNIT\s*\(\s*LENGTH_MEASURE\s*\(\s*([\d.eE+\-]+)\s*\)", re.IGNORECASE
)
_RE_PLANE_DIST = re.compile(
    r"CARTESIAN_POINT\s*\(\s*'[^']*'\s*,\s*\(([\d.\-eE+\s,]+)\)\s*\)", re.IGNORECASE
)
_RE_CIRCLE = re.compile(
    r"#(\d+)\s*=\s*CIRCLE\s*\([^,]*,\s*#\d+\s*,\s*([\d.eE+\-]+)\s*\)", re.IGNORECASE
)
_RE_DESCR = re.compile(
    r"#\d+\s*=\s*PRODUCT_DEFINITION_FORMATION\s*\(\s*'([^']*)',\s*'([^']*)'", re.IGNORECASE
)


def step_to_text(file_bytes: bytes) -> str:
    """Extract engineering data directly from a STEP (ISO-10303-21) file.

    STEP is plain ASCII. We parse entities to extract:
    - PRODUCT names and descriptions
    - MATERIAL declarations
    - CIRCLE entities (radius → diameter)
    - MEASURE_WITH_UNIT (explicit length values)
    - CARTESIAN_POINT coordinates (bounding box inference)
    """
    try:
        raw = file_bytes.decode("utf-8", errors="replace")
    except Exception as exc:
        raise ValueError(f"Could not decode STEP file: {exc}") from exc

    sections = ["=== STEP FILE (ISO-10303-21) ===", ""]

    # Products
    products = _RE_PRODUCT.findall(raw)
    if products:
        sections.append("PRODUCTS:")
        for pid, pname in products[:10]:
            label = f"  id={pid}" if pid.strip() else ""
            desc = pname.strip()
            if desc:
                sections.append(f"  - {pid.strip()} | {desc}")
        sections.append("")

    # Descriptions
    descs = _RE_DESCR.findall(raw)
    if descs:
        sections.append("PRODUCT DESCRIPTIONS:")
        for version, desc in descs[:5]:
            if desc.strip():
                sections.append(f"  - {desc.strip()}")
        sections.append("")

    # Materials
    materials = _RE_MATERIAL.findall(raw)
    if materials:
        sections.append("MATERIALS:")
        for m in materials[:10]:
            if m.strip():
                sections.append(f"  - {m.strip()}")
        sections.append("")

    # Circles (direct geometry: radius → diameter)
    circles = _RE_CIRCLE.findall(raw)
    if circles:
        sections.append(f"CIRCLES ({len(circles)} found — radius and implied diameter):")
        seen: set[str] = set()
        for _eid, radius_str in circles[:50]:
            try:
                r = float(radius_str)
                entry = f"  radius={r:.4f} mm  →  diameter={r * 2:.4f} mm"
                if entry not in seen:
                    sections.append(entry)
                    seen.add(entry)
            except ValueError:
                pass
        sections.append("")

    # Explicit length measures
    measures = _RE_MEASURE.findall(raw)
    if measures:
        sections.append(f"LENGTH MEASURES ({len(measures)} found):")
        seen_vals: set[str] = set()
        for _eid, val_str in measures[:50]:
            try:
                v = float(val_str)
                entry = f"  {v:.4f} mm"
                if entry not in seen_vals:
                    sections.append(entry)
                    seen_vals.add(entry)
            except ValueError:
                pass
        sections.append("")

    # Bounding box from Cartesian points
    coords = _RE_PLANE_DIST.findall(raw)
    if coords:
        xs, ys, zs = [], [], []
        for coord_str in coords[:200]:
            parts = [p.strip() for p in coord_str.split(",")]
            try:
                if len(parts) >= 3:
                    xs.append(float(parts[0]))
                    ys.append(float(parts[1]))
                    zs.append(float(parts[2]))
                elif len(parts) == 2:
                    xs.append(float(parts[0]))
                    ys.append(float(parts[1]))
            except ValueError:
                pass
        if xs and ys:
            dx = max(xs) - min(xs)
            dy = max(ys) - min(ys)
            dz = (max(zs) - min(zs)) if zs else 0
            sections.append("BOUNDING BOX (from Cartesian points):")
            sections.append(f"  X span: {dx:.4f} mm")
            sections.append(f"  Y span: {dy:.4f} mm")
            if dz > 0:
                sections.append(f"  Z span: {dz:.4f} mm")
            sections.append("")

    return "\n".join(sections)


# ── MIME / extension helpers ───────────────────────────────────────────────────

DXF_DWG_MIME = {
    "application/dxf", "application/acad", "image/vnd.dxf",
    "image/x-dwg", "image/vnd.dwg", "application/dwg", "application/x-dwg",
}
STEP_MIME = {
    "application/step", "application/stp", "model/step", "model/stp",
}
DXF_DWG_EXT = {".dxf", ".dwg"}
STEP_EXT = {".step", ".stp"}


def is_dxf_dwg(content_type: str | None, filename: str) -> bool:
    ext = Path(filename).suffix.lower()
    return ext in DXF_DWG_EXT or (content_type or "").lower() in DXF_DWG_MIME


def is_step(content_type: str | None, filename: str) -> bool:
    ext = Path(filename).suffix.lower()
    return ext in STEP_EXT or (content_type or "").lower() in STEP_MIME

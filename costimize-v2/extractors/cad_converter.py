"""CAD file extraction for cost estimation.

DXF / DWG  → structured text via ezdxf entity traversal (exact dimension values)
STEP       → structured text via pythonOCC geometry analysis (cadquery-ocp package)
             Falls back to ISO-10303-21 text parsing if OCC is not available.

No PNG conversion — all extraction is direct from file entities.
"""
from __future__ import annotations

import re
import tempfile
import logging
from pathlib import Path

logger = logging.getLogger("costimize")


# ── DXF / DWG direct extraction ───────────────────────────────────────────────

def dxf_to_text(file_bytes: bytes, filename: str = "drawing.dxf") -> str:
    """Extract engineering data directly from DXF/DWG using ezdxf entity traversal.

    Collects:
    - DIMENSION entities (exact numeric values with units)
    - TEXT / MTEXT (annotations, title block, tolerances, notes)
    - CIRCLE / ARC entities (radii → diameters)
    - LEADER annotations

    Returns structured text the AI reads directly — no PNG, no quality loss.
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

    # Units
    header = doc.header
    insunits = header.get("$INSUNITS", None)
    unit_label = {
        0: "unitless", 1: "inches", 2: "feet", 4: "mm",
        5: "cm", 6: "m", 14: "dm",
    }.get(insunits, f"code {insunits}")
    sections.append(f"UNITS: {unit_label}")
    sections.append("")

    # Title block texts from named blocks
    title_texts: list[str] = []
    for block in doc.blocks:
        bname = block.name.upper()
        if any(k in bname for k in ("TITLE", "BORDER", "SHEET", "HEAD", "TB")):
            for e in block:
                if e.dxftype() in ("TEXT", "MTEXT"):
                    val = (getattr(e.dxf, "text", None) or "").strip()
                    if val:
                        title_texts.append(val)
    if title_texts:
        sections.append("TITLE BLOCK / ANNOTATIONS:")
        for t in title_texts[:40]:
            sections.append(f"  {t}")
        sections.append("")

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
                dim_type = entity.dimtype & 7
                type_label = {0: "linear", 2: "angular", 3: "diameter", 4: "radius"}.get(dim_type, "dim")
                override = entity.dxf.get("text", "")
                if val is not None:
                    entry = f"{type_label}: {val:.4f} {unit_label}"
                    if override and override != "<>":
                        entry += f"  [label: {override}]"
                    dimensions.append(entry)
                elif override and override != "<>":
                    dimensions.append(f"{type_label}: {override}")
            except Exception:
                pass

        elif dtype in ("TEXT", "MTEXT"):
            try:
                val = (getattr(entity.dxf, "text", None) or "").strip()
                val = re.sub(r"\\[A-Za-z][^;]*;", "", val)
                val = re.sub(r"\{[^}]*\}", "", val).strip()
                if val and len(val) > 1:
                    texts.append(val)
            except Exception:
                pass

        elif dtype == "CIRCLE":
            try:
                r = entity.dxf.radius
                circles.append(f"circle  r={r:.4f} {unit_label}  d={r*2:.4f} {unit_label}")
            except Exception:
                pass

        elif dtype == "ARC":
            try:
                r = entity.dxf.radius
                circles.append(f"arc  r={r:.4f} {unit_label}  d={r*2:.4f} {unit_label}")
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


# ── STEP extraction via pythonOCC (primary) ───────────────────────────────────

def _step_to_text_occ(file_bytes: bytes) -> str:
    """Extract engineering geometry from STEP using Open CASCADE Technology.

    Requires cadquery-ocp: pip install cadquery-ocp

    Extracts:
    - Bounding box → part length × width × height
    - Cylindrical faces → all shaft/bore diameters (unique radii sorted)
    - Volume → material weight (volume × density)
    - Surface area → finishing cost driver
    - Feature count → shape complexity
    - STEP header → product name, description
    """
    # cadquery-ocp exposes Open CASCADE as OCP.* (not OCC.Core.*)
    from OCP.STEPControl import STEPControl_Reader
    from OCP.IFSelect import IFSelect_RetDone
    from OCP.TopExp import TopExp_Explorer
    from OCP.TopAbs import TopAbs_FACE
    from OCP.TopoDS import topods_Face
    from OCP.BRepAdaptor import BRepAdaptor_Surface
    from OCP.GeomAbs import (
        GeomAbs_Cylinder, GeomAbs_Plane, GeomAbs_Cone,
        GeomAbs_Torus, GeomAbs_Sphere,
    )
    from OCP.GProp import GProp_GProps
    from OCP.BRepGProp import BRepGProp
    from OCP.Bnd import Bnd_Box
    from OCP.BRepBndLib import BRepBndLib

    with tempfile.NamedTemporaryFile(suffix=".step", delete=False) as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    try:
        reader = STEPControl_Reader()
        status = reader.ReadFile(tmp_path)
        if status != IFSelect_RetDone:
            raise ValueError("STEP reader failed to parse file.")
        reader.TransferRoots()
        shape = reader.OneShape()
    finally:
        Path(tmp_path).unlink(missing_ok=True)

    sections = ["=== STEP FILE — pythonOCC GEOMETRY ANALYSIS ===", ""]

    # ── Bounding box ─────────────────────────────────────────────────────────
    bbox = Bnd_Box()
    BRepBndLib.Add_s(shape, bbox)
    xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
    dx = xmax - xmin
    dy = ymax - ymin
    dz = zmax - zmin
    # Sort so length ≥ width ≥ height
    dims = sorted([dx, dy, dz], reverse=True)
    sections.append("BOUNDING BOX:")
    sections.append(f"  length (longest) : {dims[0]:.4f} mm")
    sections.append(f"  width            : {dims[1]:.4f} mm")
    sections.append(f"  height           : {dims[2]:.4f} mm")
    sections.append("")

    # ── Volume and surface area ───────────────────────────────────────────────
    try:
        vol_props = GProp_GProps()
        BRepGProp.VolumeProperties_s(shape, vol_props)
        volume_mm3 = vol_props.Mass()
        sections.append("VOLUME:")
        sections.append(f"  {volume_mm3:.2f} mm³  ({volume_mm3 / 1000:.4f} cm³)")
        # Approximate weight for common materials
        sections.append("  Approx. weight:")
        for mat, density in [("Steel (7.85 g/cm³)", 7.85), ("Aluminium (2.7 g/cm³)", 2.7), ("Brass (8.5 g/cm³)", 8.5)]:
            w = (volume_mm3 / 1000) * density
            sections.append(f"    {mat}: {w:.1f} g")
        sections.append("")
    except Exception:
        pass

    try:
        surf_props = GProp_GProps()
        BRepGProp.SurfaceProperties_s(shape, surf_props)
        area_mm2 = surf_props.Mass()
        sections.append("SURFACE AREA:")
        sections.append(f"  {area_mm2:.2f} mm²  ({area_mm2 / 100:.2f} cm²)")
        sections.append("")
    except Exception:
        pass

    # ── Face type analysis ────────────────────────────────────────────────────
    cylinders: list[float] = []
    planes = 0
    cones = 0
    tori = 0
    spheres = 0
    other = 0

    explorer = TopExp_Explorer(shape, TopAbs_FACE)
    while explorer.More():
        face = topods_Face(explorer.Current())
        surf = BRepAdaptor_Surface(face)
        stype = surf.GetType()

        if stype == GeomAbs_Cylinder:
            try:
                r = surf.Cylinder().Radius()
                cylinders.append(round(r, 4))
            except Exception:
                pass
        elif stype == GeomAbs_Plane:
            planes += 1
        elif stype == GeomAbs_Cone:
            cones += 1
        elif stype == GeomAbs_Torus:
            tori += 1
        elif stype == GeomAbs_Sphere:
            spheres += 1
        else:
            other += 1

        explorer.Next()

    sections.append("FACE TYPE SUMMARY:")
    sections.append(f"  Cylindrical faces : {len(cylinders)}")
    sections.append(f"  Planar faces      : {planes}")
    sections.append(f"  Conical faces     : {cones}")
    sections.append(f"  Toroidal faces    : {tori}")
    sections.append(f"  Spherical faces   : {spheres}")
    sections.append(f"  Other             : {other}")
    sections.append("")

    # ── Cylindrical features — deduplicated and sorted ────────────────────────
    if cylinders:
        # Group by radius (within 0.01mm tolerance)
        unique_radii: dict[float, int] = {}
        for r in cylinders:
            matched = False
            for known in list(unique_radii.keys()):
                if abs(r - known) < 0.01:
                    unique_radii[known] += 1
                    matched = True
                    break
            if not matched:
                unique_radii[r] = 1

        sorted_radii = sorted(unique_radii.items(), key=lambda x: x[0], reverse=True)

        sections.append(f"CYLINDRICAL FEATURES ({len(sorted_radii)} unique radii):")
        sections.append("  (Sorted largest → smallest — largest likely shaft OD, smallest likely holes/bores)")
        for r, count in sorted_radii:
            d = r * 2
            sections.append(f"  radius={r:.4f} mm  diameter={d:.4f} mm  ×{count} face(s)")
        sections.append("")

        # Heuristic: outer diameter = largest cylinder
        max_r = sorted_radii[0][0]
        sections.append(f"LIKELY OUTER DIAMETER: {max_r * 2:.4f} mm")
        if len(sorted_radii) > 1:
            min_r = sorted_radii[-1][0]
            sections.append(f"LIKELY BORE / HOLE DIAMETER: {min_r * 2:.4f} mm")
        sections.append("")

    return "\n".join(sections)


# ── STEP fallback: ISO-10303-21 text parsing ──────────────────────────────────

_RE_PRODUCT = re.compile(r"#\d+\s*=\s*PRODUCT\s*\(\s*'([^']*)',\s*'([^']*)'", re.IGNORECASE)
_RE_MATERIAL = re.compile(r"#\d+\s*=\s*MATERIAL\s*\(\s*'([^']*)'", re.IGNORECASE)
_RE_MEASURE = re.compile(
    r"#(\d+)\s*=\s*MEASURE_WITH_UNIT\s*\(\s*LENGTH_MEASURE\s*\(\s*([\d.eE+\-]+)\s*\)",
    re.IGNORECASE,
)
_RE_CIRCLE = re.compile(
    r"#(\d+)\s*=\s*CIRCLE\s*\([^,]*,\s*#\d+\s*,\s*([\d.eE+\-]+)\s*\)", re.IGNORECASE
)
_RE_CARTESIAN = re.compile(
    r"CARTESIAN_POINT\s*\(\s*'[^']*'\s*,\s*\(([\d.\-eE+\s,]+)\)\s*\)", re.IGNORECASE
)
_RE_CYLINDER_SURF = re.compile(
    r"#(\d+)\s*=\s*CYLINDRICAL_SURFACE\s*\([^,]*,\s*#\d+\s*,\s*([\d.eE+\-]+)\s*\)",
    re.IGNORECASE,
)


def _step_to_text_fallback(file_bytes: bytes) -> str:
    """Fallback STEP extraction via ISO-10303-21 regex parsing (no OCC required)."""
    try:
        raw = file_bytes.decode("utf-8", errors="replace")
    except Exception as exc:
        raise ValueError(f"Could not decode STEP file: {exc}") from exc

    sections = ["=== STEP FILE (text parsing — OCC not available) ===", ""]

    products = _RE_PRODUCT.findall(raw)
    if products:
        sections.append("PRODUCTS:")
        for pid, pname in products[:10]:
            if pid.strip() or pname.strip():
                sections.append(f"  - {pid.strip()} | {pname.strip()}")
        sections.append("")

    materials = _RE_MATERIAL.findall(raw)
    if materials:
        sections.append("MATERIALS:")
        for m in materials[:10]:
            if m.strip():
                sections.append(f"  - {m.strip()}")
        sections.append("")

    # Cylindrical surfaces from text
    cyl_surfs = _RE_CYLINDER_SURF.findall(raw)
    circles = _RE_CIRCLE.findall(raw)
    all_radii = [float(r) for _, r in cyl_surfs] + [float(r) for _, r in circles]
    if all_radii:
        all_radii.sort(reverse=True)
        sections.append(f"CYLINDRICAL FEATURES ({len(all_radii)} found):")
        seen: set[str] = set()
        for r in all_radii[:30]:
            entry = f"  r={r:.4f} mm  d={r*2:.4f} mm"
            if entry not in seen:
                sections.append(entry)
                seen.add(entry)
        sections.append("")

    measures = _RE_MEASURE.findall(raw)
    if measures:
        vals = sorted({float(v) for _, v in measures}, reverse=True)
        sections.append(f"LENGTH MEASURES ({len(vals)} unique):")
        for v in vals[:30]:
            sections.append(f"  {v:.4f} mm")
        sections.append("")

    coords = _RE_CARTESIAN.findall(raw)
    if coords:
        xs, ys, zs = [], [], []
        for coord_str in coords[:300]:
            parts = [p.strip() for p in coord_str.split(",")]
            try:
                xs.append(float(parts[0]))
                ys.append(float(parts[1]))
                if len(parts) >= 3:
                    zs.append(float(parts[2]))
            except (ValueError, IndexError):
                pass
        if xs and ys:
            dx, dy = max(xs) - min(xs), max(ys) - min(ys)
            dz = (max(zs) - min(zs)) if zs else 0
            dims = sorted([dx, dy, dz], reverse=True)
            sections.append("BOUNDING BOX (estimated from Cartesian points):")
            sections.append(f"  length: {dims[0]:.4f} mm")
            sections.append(f"  width : {dims[1]:.4f} mm")
            if dims[2] > 0:
                sections.append(f"  height: {dims[2]:.4f} mm")
            sections.append("")

    return "\n".join(sections)


def step_to_text(file_bytes: bytes) -> str:
    """Extract STEP file data. Uses pythonOCC (cadquery-ocp) if available, falls back to text parsing."""
    try:
        return _step_to_text_occ(file_bytes)
    except ImportError:
        logger.warning("cadquery-ocp not available — using text fallback for STEP extraction")
        return _step_to_text_fallback(file_bytes)
    except Exception as exc:
        logger.warning("OCC STEP extraction failed (%s) — falling back to text parsing", exc)
        return _step_to_text_fallback(file_bytes)


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

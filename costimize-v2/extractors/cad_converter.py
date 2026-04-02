"""CAD file extraction for cost estimation.

DXF        → structured text via ezdxf entity traversal (exact dimension values)
DWG        → converted to DXF first (ODA File Converter → LibreDWG → error), then ezdxf
STEP       → structured text via pythonOCC geometry analysis (cadquery-ocp package)
             Falls back to ISO-10303-21 text parsing if OCC is not available.

No PNG conversion — all extraction is direct from file entities.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
import logging
from pathlib import Path

logger = logging.getLogger("costimize")


# ── DWG → DXF conversion ────────────────────────────────────────────────────

def _dwg_to_dxf_bytes(file_bytes: bytes) -> bytes:
    """Convert DWG binary to DXF bytes using available system converters.

    Tries in order:
    1. ezdxf odafc addon (wraps ODA File Converter)
    2. LibreDWG dwg2dxf CLI
    3. ODAFileConverter CLI directly
    Raises RuntimeError if no converter is available.
    """
    # Strategy 1: ezdxf odafc addon (cleanest)
    try:
        from ezdxf.addons import odafc
        if odafc.is_installed():
            with tempfile.NamedTemporaryFile(suffix=".dwg", delete=False) as tmp:
                tmp.write(file_bytes)
                dwg_path = tmp.name
            try:
                doc = odafc.readfile(dwg_path)
                dxf_path = dwg_path.replace(".dwg", ".dxf")
                doc.saveas(dxf_path)
                dxf_bytes = Path(dxf_path).read_bytes()
                Path(dxf_path).unlink(missing_ok=True)
                logger.info("DWG→DXF via ODA File Converter (ezdxf odafc)")
                return dxf_bytes
            finally:
                Path(dwg_path).unlink(missing_ok=True)
    except Exception as exc:
        logger.debug("odafc not available: %s", exc)

    # Strategy 2: LibreDWG dwg2dxf CLI
    if shutil.which("dwg2dxf"):
        with tempfile.NamedTemporaryFile(suffix=".dwg", delete=False) as tmp:
            tmp.write(file_bytes)
            dwg_path = tmp.name
        dxf_path = dwg_path.replace(".dwg", ".dxf")
        try:
            subprocess.run(
                ["dwg2dxf", "-o", dxf_path, dwg_path],
                check=True, capture_output=True, timeout=30,
            )
            dxf_bytes = Path(dxf_path).read_bytes()
            logger.info("DWG→DXF via LibreDWG dwg2dxf")
            return dxf_bytes
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as exc:
            logger.warning("dwg2dxf failed: %s", exc)
        finally:
            Path(dwg_path).unlink(missing_ok=True)
            Path(dxf_path).unlink(missing_ok=True)

    # Strategy 3: ODAFileConverter CLI directly
    oda_cmd = shutil.which("ODAFileConverter")
    if oda_cmd:
        with tempfile.TemporaryDirectory() as indir, tempfile.TemporaryDirectory() as outdir:
            dwg_path = Path(indir) / "input.dwg"
            dwg_path.write_bytes(file_bytes)
            try:
                subprocess.run(
                    [oda_cmd, indir, outdir, "ACAD2018", "DXF", "0", "1"],
                    check=True, capture_output=True, timeout=30,
                )
                dxf_files = list(Path(outdir).glob("*.dxf"))
                if dxf_files:
                    logger.info("DWG→DXF via ODAFileConverter CLI")
                    return dxf_files[0].read_bytes()
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
                logger.warning("ODAFileConverter failed: %s", exc)

    raise RuntimeError(
        "No DWG converter available. Install ODA File Converter "
        "(https://www.opendesign.com/guestfiles/oda_file_converter) "
        "or LibreDWG (apt install libredwg-tools). "
        "Alternatively, export as DXF from AutoCAD."
    )


# ── DXF / DWG direct extraction ───────────────────────────────────────────────

def dxf_to_text(file_bytes: bytes, filename: str = "drawing.dxf") -> str:
    """Extract engineering data directly from DXF/DWG using ezdxf entity traversal.

    For DWG files, converts to DXF first using available system converters.

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

    ext = Path(filename).suffix.lower()

    # DWG files need conversion first
    if ext == ".dwg":
        file_bytes = _dwg_to_dxf_bytes(file_bytes)
        filename = filename.rsplit(".", 1)[0] + ".dxf"

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
    """Extract engineering geometry from STEP using Open CASCADE (cadquery-ocp).

    API verified against CadQuery source (github.com/CadQuery/cadquery):
    - Static methods use _s suffix: BRepBndLib.Add_s(), BRepGProp.VolumeProperties_s()
    - Downcasts use TopoDS.Face_s() (not topods_Face)
    - Instance methods have no suffix: bbox.Get(), adaptor.GetType()
    """
    from OCP.STEPControl import STEPControl_Reader
    from OCP.IFSelect import IFSelect_RetDone
    from OCP.TopExp import TopExp_Explorer
    from OCP.TopAbs import TopAbs_FACE
    from OCP.TopoDS import TopoDS
    from OCP.BRepAdaptor import BRepAdaptor_Surface
    from OCP.GeomAbs import (
        GeomAbs_Cylinder, GeomAbs_Plane, GeomAbs_Cone,
        GeomAbs_Torus, GeomAbs_Sphere,
    )
    from OCP.GProp import GProp_GProps
    from OCP.BRepGProp import BRepGProp
    from OCP.Bnd import Bnd_Box
    from OCP.BRepBndLib import BRepBndLib

    # Write bytes to temp file for OCC reader
    with tempfile.NamedTemporaryFile(suffix=".step", delete=False) as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    try:
        reader = STEPControl_Reader()
        status = reader.ReadFile(tmp_path)
        if status != IFSelect_RetDone:
            raise ValueError("STEP reader failed to parse file.")

        # Transfer all roots (handles multi-root files)
        for i in range(reader.NbRootsForTransfer()):
            reader.TransferRoot(i + 1)  # 1-indexed

        # Collect all shapes
        shapes = []
        for i in range(reader.NbShapes()):
            shapes.append(reader.Shape(i + 1))  # 1-indexed

        if not shapes:
            raise ValueError("STEP file contained no geometry.")

        shape = shapes[0]  # Primary shape for analysis
    finally:
        Path(tmp_path).unlink(missing_ok=True)

    sections = ["=== STEP FILE — OCC GEOMETRY ANALYSIS ===", ""]

    if len(shapes) > 1:
        sections.append(f"NOTE: File contains {len(shapes)} shapes (assembly). Analyzing primary shape.")
        sections.append("")

    # ── Bounding box ─────────────────────────────────────────────────────────
    bbox = Bnd_Box()
    BRepBndLib.Add_s(shape, bbox, True)  # True = use triangulation (faster)
    xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
    dx = abs(xmax - xmin)
    dy = abs(ymax - ymin)
    dz = abs(zmax - zmin)
    dims = sorted([dx, dy, dz], reverse=True)
    sections.append("BOUNDING BOX:")
    sections.append(f"  length (longest) : {dims[0]:.3f} mm")
    sections.append(f"  width            : {dims[1]:.3f} mm")
    sections.append(f"  height (shortest): {dims[2]:.3f} mm")
    sections.append("")

    # ── Volume ────────────────────────────────────────────────────────────────
    try:
        vol_props = GProp_GProps()
        BRepGProp.VolumeProperties_s(shape, vol_props)
        volume_mm3 = vol_props.Mass()
        if volume_mm3 > 0:
            sections.append("VOLUME:")
            sections.append(f"  {volume_mm3:.2f} mm³  ({volume_mm3 / 1000:.4f} cm³)")
            sections.append("  Approx. weight:")
            for mat, density in [("Steel 7.85", 7.85), ("Aluminium 2.7", 2.7), ("Brass 8.5", 8.5), ("Titanium 4.5", 4.5)]:
                w = (volume_mm3 / 1000) * density
                sections.append(f"    {mat} g/cm³ → {w:.1f} g")
            sections.append("")
    except Exception:
        pass

    # ── Surface area ──────────────────────────────────────────────────────────
    try:
        surf_props = GProp_GProps()
        BRepGProp.SurfaceProperties_s(shape, surf_props)
        area_mm2 = surf_props.Mass()
        if area_mm2 > 0:
            sections.append(f"SURFACE AREA: {area_mm2:.2f} mm²  ({area_mm2 / 100:.2f} cm²)")
            sections.append("")
    except Exception:
        pass

    # ── Face type analysis ────────────────────────────────────────────────────
    cylinders: list[float] = []
    planes = 0
    cones = 0
    tori = 0
    spheres = 0
    other_faces = 0

    explorer = TopExp_Explorer(shape, TopAbs_FACE)
    while explorer.More():
        try:
            face = TopoDS.Face_s(explorer.Current())
            surf = BRepAdaptor_Surface(face)
            stype = surf.GetType()

            if stype == GeomAbs_Cylinder:
                r = surf.Cylinder().Radius()
                cylinders.append(round(r, 4))
            elif stype == GeomAbs_Plane:
                planes += 1
            elif stype == GeomAbs_Cone:
                cones += 1
            elif stype == GeomAbs_Torus:
                tori += 1
            elif stype == GeomAbs_Sphere:
                spheres += 1
            else:
                other_faces += 1
        except Exception:
            other_faces += 1
        explorer.Next()

    total_faces = len(cylinders) + planes + cones + tori + spheres + other_faces
    sections.append(f"FACE ANALYSIS ({total_faces} faces):")
    sections.append(f"  Planar      : {planes}")
    sections.append(f"  Cylindrical : {len(cylinders)}")
    if cones:
        sections.append(f"  Conical     : {cones}")
    if tori:
        sections.append(f"  Toroidal    : {tori}  (likely fillets/chamfers)")
    if spheres:
        sections.append(f"  Spherical   : {spheres}")
    if other_faces:
        sections.append(f"  Other/NURBS : {other_faces}  (freeform surfaces)")
    sections.append("")

    # ── Part type heuristic ───────────────────────────────────────────────────
    if total_faces > 0:
        cyl_ratio = len(cylinders) / total_faces
        plane_ratio = planes / total_faces
        if cyl_ratio > 0.3:
            sections.append("PART TYPE HINT: Rotational part (turned/cylindrical) — high cylinder face ratio")
        elif plane_ratio > 0.6:
            sections.append("PART TYPE HINT: Prismatic part (milled/sheet metal) — mostly planar faces")
        elif tori > 2:
            sections.append("PART TYPE HINT: Complex part with fillets — likely milled")
        sections.append("")

    # ── Cylindrical features — deduplicated and sorted ────────────────────────
    if cylinders:
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

        sections.append(f"CYLINDRICAL FEATURES ({len(sorted_radii)} unique diameters):")
        for r, count in sorted_radii:
            d = r * 2
            label = ""
            if r == sorted_radii[0][0]:
                label = "  ← likely OD"
            elif r == sorted_radii[-1][0] and len(sorted_radii) > 1:
                label = "  ← likely bore/hole"
            sections.append(f"  Ø{d:.3f} mm  (r={r:.3f})  ×{count} face(s){label}")
        sections.append("")

    # ── Aspect ratio → manufacturing hint ─────────────────────────────────────
    if dims[2] > 0:
        aspect = dims[0] / dims[2]
        if aspect > 5:
            sections.append(f"ASPECT RATIO: {aspect:.1f}:1 — long/thin part (shaft, rod, or sheet)")
        elif aspect < 1.5:
            sections.append(f"ASPECT RATIO: {aspect:.1f}:1 — compact/cubic part")
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

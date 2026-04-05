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
from typing import NamedTuple

logger = logging.getLogger("costimize")


# ── Regex patterns for TEXT-encoded dimensions ────────────────────────────────
# Matches "D50", "Ø50", "d=50", "DIA 50"  → diameter
_RE_TEXT_DIA = re.compile(
    r"^(?:D|Ø|O|DIA\.?\s*|DIAM\.?\s*)(\d+(?:\.\d+)?)\s*(?:mm)?$",
    re.IGNORECASE,
)
# Matches "R8", "r=8", "RAD 8" → radius
_RE_TEXT_RAD = re.compile(
    r"^(?:R|RAD\.?\s*)(\d+(?:\.\d+)?)\s*(?:mm)?$",
    re.IGNORECASE,
)
# Matches thread callouts: "M8", "M12x1.5", "M8 THRU"
_RE_TEXT_THREAD = re.compile(
    r"^(M\d+(?:x[\d.]+)?(?:\s*THRU)?(?:\s*DEEP\s*\d+)?)",
    re.IGNORECASE,
)
# Bare integer / decimal → likely linear dimension e.g. "40", "120.5"
_RE_TEXT_LINEAR = re.compile(r"^(\d+(?:\.\d+)?)$")

# Compound annotation patterns — "Thickness 15mm", "Height 20mm", "Depth 8mm"
# Used to pull named dimensions out of multi-value annotation strings
_RE_NAMED_DIM = re.compile(
    r"\b(?P<kind>thickness|height|depth|width|length|dia(?:meter)?|bore|od|id|thk)\s*[=:]*\s*"
    r"(?P<value>\d+(?:\.\d+)?)\s*(?:mm)?",
    re.IGNORECASE,
)
_NAMED_DIM_KIND_MAP = {
    "thickness": "thickness", "thk": "thickness",
    "height": "height", "depth": "depth",
    "width": "width", "length": "length",
    "dia": "diameter", "diameter": "diameter",
    "bore": "bore", "od": "outer_diameter", "id": "inner_diameter",
}


class _Entity(NamedTuple):
    etype: str
    x: float
    y: float
    value: float | str  # radius for circles; text string for TEXT


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

    # Strategy 2: LibreDWG dwg2dxf CLI (also checks dwg2dxf.exe on Windows)
    dwg2dxf_cmd = shutil.which("dwg2dxf") or shutil.which("dwg2dxf.exe")
    if dwg2dxf_cmd:
        with tempfile.NamedTemporaryFile(suffix=".dwg", delete=False) as tmp:
            tmp.write(file_bytes)
            dwg_path = tmp.name
        dxf_path = dwg_path.replace(".dwg", ".dxf")
        try:
            subprocess.run(
                [dwg2dxf_cmd, "-o", dxf_path, dwg_path],
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

def _detect_units(insunits: int | None, annotation_texts: list[str]) -> str:
    """Resolve drawing units.

    $INSUNITS=6 (meters) is the AutoCAD default when no units are set, but
    virtually all mechanical drawings in Indian manufacturing are in mm.
    If any annotation text contains 'mm' we trust that over the header value.
    """
    header_map = {
        0: "unitless", 1: "inches", 2: "feet", 4: "mm",
        5: "cm", 6: "m", 14: "dm",
    }
    header_unit = header_map.get(insunits or 0, f"code {insunits}")

    joined = " ".join(annotation_texts).lower()
    if "mm" in joined and header_unit != "mm":
        logger.debug(
            "Units header says '%s' but annotations contain 'mm' — overriding to mm",
            header_unit,
        )
        return "mm"
    return header_unit


def _parse_text_dimension(text: str) -> tuple[str, float] | None:
    """Parse a TEXT entity that encodes a dimension.

    Returns (kind, value_mm) or None if not a dimension annotation.
    kind is one of: 'diameter', 'radius', 'thread', 'linear'
    """
    t = text.strip()
    m = _RE_TEXT_DIA.match(t)
    if m:
        return ("diameter", float(m.group(1)))
    m = _RE_TEXT_RAD.match(t)
    if m:
        return ("radius", float(m.group(1)))
    m = _RE_TEXT_THREAD.match(t)
    if m:
        return ("thread", 0.0)  # value not numeric; caller uses raw text
    m = _RE_TEXT_LINEAR.match(t)
    if m:
        return ("linear", float(m.group(1)))
    return None


def _cluster_circles(
    circle_entities: list[tuple[float, float, float]],  # (x, y, r)
    main_bbox: tuple[float, float, float, float] | None,  # (xmin, xmax, ymin, ymax)
) -> tuple[list[tuple[float, float, float]], list[tuple[float, float, float]]]:
    """Split circles into (main_view, end_view) based on spatial position.

    Circles that fall well outside the main LINE bounding box are placed in
    the end/section view — they're a separate projected view, not geometry
    to double-count.
    """
    if main_bbox is None or not circle_entities:
        return circle_entities, []

    xmin, xmax, ymin, ymax = main_bbox
    margin_x = (xmax - xmin) * 0.5 if xmax > xmin else 50.0

    main: list[tuple[float, float, float]] = []
    end: list[tuple[float, float, float]] = []
    for cx, cy, r in circle_entities:
        if cx < xmin - margin_x or cx > xmax + margin_x:
            end.append((cx, cy, r))
        else:
            main.append((cx, cy, r))
    return main, end


def _detect_centerline(line_entities: list[tuple[float, float, float, float]]) -> bool:
    """Return True if a center line exists (long horizontal line with symmetric profile).

    A rotational (turned) part has a horizontal axis line with LINE entities at
    equal +d and -d offsets from it. A sheet metal bracket has asymmetric lines
    and must NOT be flagged as rotational.

    Algorithm:
    1. Find candidate horizontal lines near the profile centroid.
    2. For each candidate, collect the set of distinct y-values from all profile lines.
    3. Check that at least one pair of y-values is symmetric about the candidate y.
    """
    if not line_entities:
        return False
    ys_all = [y for x1, y1, x2, y2 in line_entities for y in (y1, y2)]
    if not ys_all:
        return False
    y_span = max(ys_all) - min(ys_all)
    if y_span == 0:
        return False
    centroid_y = sum(ys_all) / len(ys_all)

    # Unique y-levels present in the drawing
    unique_ys = sorted(set(round(y, 2) for y in ys_all))

    for x1, y1, x2, y2 in line_entities:
        length = abs(x2 - x1)
        if length == 0:
            continue
        if abs(y2 - y1) / length >= 0.05:  # must be nearly horizontal
            continue
        mid_y = (y1 + y2) / 2
        if abs(mid_y - centroid_y) >= y_span * 0.15:
            continue  # too far from centroid

        # Check for at least one symmetric pair about this mid_y
        tol = y_span * 0.05
        for y in unique_ys:
            if abs(y - mid_y) < tol:
                continue  # skip the centerline itself
            mirror = 2 * mid_y - y
            if any(abs(uy - mirror) < tol for uy in unique_ys):
                return True  # found symmetric pair → rotational

    return False


# GD&T symbol → canonical name mapping
# Covers both Unicode symbols (from CAD exports) and ASCII text equivalents
_GDT_SYMBOL_MAP: dict[str, str] = {
    # Form
    "○": "circularity", "⌭": "circularity", "⌒": "cylindricity",
    "—": "straightness", "□": "flatness",
    # Orientation
    "⊥": "perpendicularity", "∠": "angularity", "//": "parallelism", "⫽": "parallelism",
    # Location
    "⌖": "true_position", "◎": "concentricity", "⌯": "symmetry",
    # Runout
    "↗": "circular_runout", "⌰": "total_runout",
    # Profile
    "⌓": "profile_of_surface", "⌒": "profile_of_line",
    # ASCII fallbacks
    "PERP": "perpendicularity", "PARA": "parallelism", "CIRC": "circularity",
    "SYM": "symmetry", "POS": "true_position", "RUN": "circular_runout",
    "CYL": "cylindricity", "FLAT": "flatness", "STR": "straightness",
}

# All known GD&T canonical names
_ALL_GDT_NAMES = frozenset(_GDT_SYMBOL_MAP.values())

# Regex: Feature Control Frame text — e.g. "⊥|0.02|A" or "//|0.05|A|B"
_RE_FCF = re.compile(
    r"([⊥∠//⫽⌖◎⌯↗⌰⌓○⌭⌒—□]|PERP|PARA|CIRC|SYM|POS|RUN|CYL|FLAT|STR)"
    r"[\s|,]*([\d.]+)\s*(?:mm)?"
    r"(?:[\s|,]+([A-Z]))?",
    re.IGNORECASE,
)

# Layer name keywords that hint at which view an entity belongs to
_VIEW_LAYER_KEYWORDS: dict[str, str] = {
    "FRONT": "FRONT VIEW", "FVIEW": "FRONT VIEW",
    "TOP": "TOP VIEW", "PLAN": "TOP VIEW",
    "SIDE": "SIDE VIEW", "RIGHT": "RIGHT VIEW", "LEFT": "LEFT VIEW",
    "ISO": "ISOMETRIC VIEW", "ISOMETRIC": "ISOMETRIC VIEW",
    "SECTION": "SECTION VIEW", "SECT": "SECTION VIEW",
    "DETAIL": "DETAIL VIEW", "DET": "DETAIL VIEW",
    "AUX": "AUXILIARY VIEW",
}

# Cutting plane line type names that indicate section cuts
_CUTTING_PLANE_LINETYPES = frozenset({
    "DASHDOT", "DASHDOT2", "DASHDOTX2",
    "CENTER", "CENTER2", "CENTERX2",
    "PHANTOM", "PHANTOM2", "PHANTOMX2",
    "CHAIN",
})


def _get_paperspace_views(doc) -> list[dict]:
    """Parse paperspace viewports to get named views with modelspace bounding boxes.

    Each viewport is a window into modelspace. By extracting the center and
    dimensions of each viewport we can determine which modelspace entities
    belong to which named view (front, top, section, etc.).

    Returns list of dicts: {name, xmin, xmax, ymin, ymax}
    """
    views: list[dict] = []
    try:
        psp = doc.paperspace()
        for i, vp in enumerate(psp.query("VIEWPORT")):
            try:
                cx = vp.dxf.view_center_point.x
                cy = vp.dxf.view_center_point.y
                vh = vp.dxf.view_height
                # Compute modelspace width from paperspace aspect ratio
                ps_w = getattr(vp.dxf, "width", vh)
                ps_h = getattr(vp.dxf, "height", vh)
                vw = vh * (ps_w / ps_h) if ps_h and ps_h > 0 else vh
                # Try to get a meaningful view name from the layer
                layer = (vp.dxf.get("layer", "") or "").upper()
                name = f"VIEW_{i+1}"
                for kw, label in _VIEW_LAYER_KEYWORDS.items():
                    if kw in layer:
                        name = label
                        break
                views.append({
                    "name": name,
                    "xmin": cx - vw / 2,
                    "xmax": cx + vw / 2,
                    "ymin": cy - vh / 2,
                    "ymax": cy + vh / 2,
                })
            except Exception:
                continue
    except Exception:
        pass
    return views


def _assign_view(x: float, y: float, viewports: list[dict]) -> str | None:
    """Return the viewport name whose modelspace bounding box contains (x, y)."""
    for vp in viewports:
        if vp["xmin"] <= x <= vp["xmax"] and vp["ymin"] <= y <= vp["ymax"]:
            return vp["name"]
    return None


def _detect_section_views(msp) -> list[dict]:
    """Detect section views by finding HATCH entities and linking them to section labels.

    Algorithm:
    1. Find all HATCH entities (cross-hatching = cut material in section views).
    2. Find all TEXT entities containing section-label patterns ("A-A", "SECTION A-A").
    3. Find cutting plane lines (chain-dash linetypes).
    4. Spatially link each HATCH to the nearest section label.

    Returns list of dicts: {label, hatch_center, pattern, cutting_plane_found}
    """
    hatches: list[dict] = []
    section_label_texts: list[tuple[str, float, float]] = []  # (text, x, y)
    has_cutting_plane = False

    _RE_SECTION_LABEL = re.compile(
        r"(?:SECTION\s+)?([A-Z])\s*[-–]\s*([A-Z])\b|^([A-Z])-([A-Z])$",
        re.IGNORECASE,
    )

    for entity in msp:
        dtype = entity.dxftype()

        if dtype == "HATCH":
            try:
                pattern = entity.dxf.get("pattern_name", "ANSI31")
                # Approximate centroid from first boundary path
                cx, cy = 0.0, 0.0
                count = 0
                for path in entity.paths:
                    try:
                        for vertex in path.vertices:
                            cx += vertex[0]
                            cy += vertex[1]
                            count += 1
                    except Exception:
                        pass
                if count > 0:
                    hatches.append({
                        "cx": cx / count,
                        "cy": cy / count,
                        "pattern": pattern,
                        "label": None,
                    })
            except Exception:
                pass

        elif dtype in ("TEXT", "MTEXT"):
            try:
                val = (getattr(entity.dxf, "text", None) or "").strip()
                val = re.sub(r"\\[A-Za-z][^;]*;", "", val).strip()
                if _RE_SECTION_LABEL.search(val):
                    pos = entity.dxf.get("insert", None) or entity.dxf.get("insert", None)
                    if pos is not None:
                        section_label_texts.append((val, pos.x, pos.y))
            except Exception:
                pass

        elif dtype == "LINE":
            try:
                lt = (entity.dxf.get("linetype", "") or "").upper().replace(" ", "")
                if any(k in lt for k in _CUTTING_PLANE_LINETYPES):
                    has_cutting_plane = True
            except Exception:
                pass

    # Link each hatch to the nearest section label
    for hatch in hatches:
        if not section_label_texts:
            break
        best_label, best_dist = None, float("inf")
        for label_text, lx, ly in section_label_texts:
            dist = ((hatch["cx"] - lx) ** 2 + (hatch["cy"] - ly) ** 2) ** 0.5
            if dist < best_dist:
                best_dist = dist
                best_label = label_text
        if best_dist < 500:  # within 500 drawing units — same view cluster
            hatch["label"] = best_label

    for hatch in hatches:
        hatch["cutting_plane_found"] = has_cutting_plane

    return hatches


def _extract_gdt_from_texts(texts: list[str]) -> list[str]:
    """Extract GD&T symbol names from raw text annotations.

    Handles:
    - Unicode GD&T symbols (⊥, ○, ⌖, etc.) from CAD exports
    - Feature Control Frame patterns ("⊥|0.02|A")
    - ASCII text equivalents ("PERP", "PARA")
    - Note text ("perpendicularity 0.02 A")

    Returns list of canonical GD&T names (e.g. ["perpendicularity", "circularity"])
    """
    found: set[str] = set()

    # Extended name patterns in plain text
    _GDT_TEXT_PATTERNS = {
        r"\bperpendicular": "perpendicularity",
        r"\bparallelism\b|\bparallel\b": "parallelism",
        r"\bcircularity\b|\broundness\b": "circularity",
        r"\bcylindricity\b": "cylindricity",
        r"\bflatness\b": "flatness",
        r"\bstraightness\b": "straightness",
        r"\btrue.?position\b|\bposition.?tol": "true_position",
        r"\bconcentricity\b": "concentricity",
        r"\bsymmetry\b": "symmetry",
        r"\brunout\b": "circular_runout",
        r"\btotal.?runout\b": "total_runout",
        r"\bprofile.?surface\b": "profile_of_surface",
        r"\bangularity\b": "angularity",
    }

    for text in texts:
        # Direct symbol lookup
        for symbol, name in _GDT_SYMBOL_MAP.items():
            if symbol in text:
                found.add(name)

        # FCF pattern match
        for m in _RE_FCF.finditer(text):
            sym = m.group(1)
            canonical = _GDT_SYMBOL_MAP.get(sym, _GDT_SYMBOL_MAP.get(sym.upper()))
            if canonical:
                found.add(canonical)

        # Plain-text pattern match
        text_lower = text.lower()
        for pattern, name in _GDT_TEXT_PATTERNS.items():
            if re.search(pattern, text_lower):
                found.add(name)

    return sorted(found)


def _group_entities_by_layer(msp) -> dict[str, list[str]]:
    """Group entity types by layer, detecting named views from layer names.

    Many real-world drawings use layers like 'FRONT_VIEW', 'SECTION_AA', 'TOP'.
    This returns {view_label: [entity_type, ...]} for informational output.
    """
    layer_groups: dict[str, list[str]] = {}
    for entity in msp:
        try:
            layer = (entity.dxf.get("layer", "0") or "0").upper()
            dtype = entity.dxftype()
            # Only emit if layer has a view-significant name
            for kw, label in _VIEW_LAYER_KEYWORDS.items():
                if kw in layer:
                    layer_groups.setdefault(label, []).append(dtype)
                    break
        except Exception:
            pass
    return layer_groups


_RE_RAW_DXF_SKIP = re.compile(
    r'^(AC\d+|ANSI_|ACDB|ACAD_|ObjectDBX|DICTION|TABLE|VISUAL|SCALE|MLE'
    r'|BLOCK_|LTYPE|LAYER|STYLE|VIEW|UCS|APPID|DIMSTYLE|VPORT)',
    re.IGNORECASE,
)


def _dxf_raw_text_fallback(raw_dxf: str) -> str:
    """Last-resort DXF parser: scan raw DXF ENTITIES section for dimensions/annotations.

    Used when ezdxf can't parse a DXF (e.g. corrupt DWG-converted DXF with bad handles).
    Only scans the ENTITIES section to avoid DXF header noise.
    """
    sections: list[str] = ["=== DXF/DWG FILE CONTENTS (raw text fallback) ===", ""]

    # Find the ENTITIES section — everything before it is header/tables noise
    entities_start = raw_dxf.find("\nENTITIES\n")
    if entities_start < 0:
        entities_start = 0
    entities_end = raw_dxf.find("\nEOF\n", entities_start)
    if entities_end < 0:
        entities_end = len(raw_dxf)
    body = raw_dxf[entities_start:entities_end]

    lines = body.splitlines()
    dims: list[str] = []
    texts: list[str] = []
    dim_overrides: list[str] = []

    i = 0
    while i < len(lines) - 1:
        code = lines[i].strip()
        val = lines[i + 1].strip()
        # Group 42 = actual dimension measurement (only positive, >0.001 to skip near-zero)
        if code == "42":
            try:
                num = float(val)
                if num > 0.001:
                    dims.append(f"  linear: {num:.4f}")
            except ValueError:
                pass
        # Group 1 = primary text (TEXT entity content or dimension override)
        elif code == "1" and val and val not in ("<>", ""):
            if len(val) < 100 and not _RE_RAW_DXF_SKIP.match(val):
                texts.append(val)
        # Group 3 = extra text (MTEXT continuation)
        elif code == "3" and val and len(val) < 100 and not _RE_RAW_DXF_SKIP.match(val):
            texts.append(val)
        i += 2

    # Deduplicate texts
    seen_texts: set[str] = set()
    unique_texts = []
    for t in texts:
        clean = t.strip()
        if clean and clean not in seen_texts:
            seen_texts.add(clean)
            unique_texts.append(clean)

    if dims:
        sections.append(f"DIMENSIONS ({len(dims)} found):")
        sections.extend(dims[:50])
        sections.append("")

    if unique_texts:
        sections.append("ANNOTATIONS:")
        for t in unique_texts[:60]:
            sections.append(f"  {t}")
        sections.append("")

    sections.append("NOTE: Parsed via raw text fallback — ezdxf could not open this file.")
    return "\n".join(sections)


def dxf_to_text(file_bytes: bytes, filename: str = "drawing.dxf") -> str:
    """Extract engineering data directly from DXF/DWG using ezdxf entity traversal.

    For DWG files, converts to DXF first using available system converters.

    Improvements over naive entity dump:
    - Units: cross-checks $INSUNITS against annotation text; overrides header
      'meters' with 'mm' when annotations confirm mm (common AutoCAD default bug)
    - TEXT dimensions: parses "D50", "R8", "M12x1.5", bare "40" into typed
      dimension entries so the AI sees structured values, not raw strings
    - Spatial clustering: circles far outside the main LINE bounding box are
      identified as an end/section view — not double-counted as extra features
    - Center line detection: long horizontal line through profile centroid
      signals a rotational (turned) part
    - Paperspace viewports: each entity is tagged with its named view
    - Section view detection: HATCH + label linking + cutting plane lines
    - Layer grouping: named view layers (FRONT, TOP, SECTION) surfaced explicitly
    - GD&T extraction: Unicode symbols + FCF patterns + plain-text names

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
    except Exception as exc:
        # DWG-converted DXFs often have corrupt/invalid handles — use recovery mode
        try:
            from ezdxf import recover as ezdxf_recover
            doc, _ = ezdxf_recover.readfile(tmp_path)
            logger.warning("DXF read with recovery mode (tolerant parsing): %s", exc)
        except Exception as exc2:
            # Final fallback: raw text parsing for DXF files ezdxf can't handle at all
            logger.warning("ezdxf recovery failed, using raw text fallback: %s", exc2)
            try:
                raw_text = Path(tmp_path).read_bytes().decode("latin-1", errors="replace")
                return _dxf_raw_text_fallback(raw_text)
            except Exception:
                pass
            Path(tmp_path).unlink(missing_ok=True)
            raise RuntimeError(f"ezdxf failed to read file even in recovery mode: {exc2}") from exc2
    finally:
        Path(tmp_path).unlink(missing_ok=True)

    sections: list[str] = ["=== DXF/DWG FILE CONTENTS ===", ""]

    # ── Pass 1: collect all raw text for units cross-check ────────────────────
    msp = doc.modelspace()
    raw_texts: list[str] = []
    for e in msp:
        if e.dxftype() in ("TEXT", "MTEXT"):
            try:
                val = (getattr(e.dxf, "text", None) or "").strip()
                if val:
                    raw_texts.append(val)
            except Exception:
                pass

    # Units (with annotation override)
    insunits = doc.header.get("$INSUNITS", None)
    unit_label = _detect_units(insunits, raw_texts)
    sections.append(f"UNITS: {unit_label}")
    sections.append("")

    # ── Title block from named blocks ─────────────────────────────────────────
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

    # ── Pass 2: full entity traversal ─────────────────────────────────────────
    dim_entities: list[str] = []
    text_dims: list[str] = []        # parsed from TEXT entities
    annotation_texts: list[str] = [] # informational text (not parseable as dims)
    circle_raw: list[tuple[float, float, float]] = []  # (cx, cy, r)
    arc_raw: list[tuple[float, float, float]] = []
    line_raw: list[tuple[float, float, float, float]] = []  # (x1,y1,x2,y2)
    leaders: list[str] = []
    hatch_count = 0

    try:
        entity_list = list(msp)  # materialize — catches "Invalid handle 0" on corrupt DWG-converted DXFs
    except Exception as exc:
        logger.warning("Failed to iterate modelspace entities (likely corrupt DXF from DWG): %s", exc)
        entity_list = []

    for entity in entity_list:
        try:
            dtype = entity.dxftype()
        except Exception:
            continue

        if dtype == "DIMENSION":
            try:
                val = entity.dxf.get("actual_measurement", None)
                # -1 is DWG/DXF sentinel for "measurement not pre-computed" — discard
                if val is not None and val < 0:
                    val = None
                dim_type = entity.dimtype & 7
                type_label = {0: "linear", 2: "angular", 3: "diameter", 4: "radius"}.get(dim_type, "dim")
                override = entity.dxf.get("text", "")
                if val is not None:
                    entry = f"{type_label}: {val:.4f} {unit_label}"
                    if override and override != "<>":
                        entry += f"  [label: {override}]"
                    dim_entities.append(entry)
                elif override and override != "<>":
                    dim_entities.append(f"{type_label}: {override}")
            except Exception:
                pass

        elif dtype in ("TEXT", "MTEXT"):
            try:
                val = (getattr(entity.dxf, "text", None) or "").strip()
                val = re.sub(r"\\[A-Za-z][^;]*;", "", val)
                val = re.sub(r"\{[^}]*\}", "", val).strip()
                if not val or len(val) < 1:
                    continue
                parsed = _parse_text_dimension(val)
                if parsed:
                    kind, num = parsed
                    if kind == "thread":
                        text_dims.append(f"thread callout: {val}")
                    elif kind == "diameter":
                        text_dims.append(f"diameter: {num:.4f} {unit_label}  [from text \"{val}\"]")
                    elif kind == "radius":
                        text_dims.append(f"radius: {num:.4f} {unit_label}  [from text \"{val}\"]")
                    elif kind == "linear":
                        text_dims.append(f"linear: {num:.4f} {unit_label}  [from text \"{val}\"]")
                else:
                    if len(val) > 1:
                        annotation_texts.append(val)
            except Exception:
                pass

        elif dtype == "CIRCLE":
            try:
                c = entity.dxf.center
                circle_raw.append((c.x, c.y, entity.dxf.radius))
            except Exception:
                pass

        elif dtype == "ARC":
            try:
                c = entity.dxf.center
                arc_raw.append((c.x, c.y, entity.dxf.radius))
            except Exception:
                pass

        elif dtype == "LINE":
            try:
                s, e2 = entity.dxf.start, entity.dxf.end
                line_raw.append((s.x, s.y, e2.x, e2.y))
            except Exception:
                pass

        elif dtype in ("LEADER", "MULTILEADER"):
            try:
                val = entity.dxf.get("text_string", "").strip()
                if val:
                    leaders.append(val)
            except Exception:
                pass

        elif dtype == "HATCH":
            hatch_count += 1

    # ── Spatial & structural analysis ────────────────────────────────────────

    # Main LINE bounding box
    main_bbox: tuple[float, float, float, float] | None = None
    if line_raw:
        xs = [x for x1, y1, x2, y2 in line_raw for x in (x1, x2)]
        ys = [y for x1, y1, x2, y2 in line_raw for y in (y1, y2)]
        main_bbox = (min(xs), max(xs), min(ys), max(ys))

    # Cluster circles: main view vs end/section view
    main_circles, end_circles = _cluster_circles(circle_raw, main_bbox)

    # Center line → rotational symmetry hint
    has_centerline = _detect_centerline(line_raw)

    # Paperspace viewport → named view mapping
    viewports = _get_paperspace_views(doc)

    # Section views: HATCH + label linking
    section_views = _detect_section_views(msp)

    # Layer-based view grouping
    layer_groups = _group_entities_by_layer(msp)

    # GD&T symbols from all text
    all_text_for_gdt = annotation_texts + [d for d in text_dims] + leaders
    gdt_symbols = _extract_gdt_from_texts(all_text_for_gdt)

    # ── Build output ──────────────────────────────────────────────────────────

    # Named views from paperspace viewports
    if viewports:
        sections.append(f"NAMED VIEWS (from paperspace layout, {len(viewports)} viewports):")
        for vp in viewports:
            sections.append(
                f"  {vp['name']}: modelspace region "
                f"x=[{vp['xmin']:.1f}, {vp['xmax']:.1f}]  "
                f"y=[{vp['ymin']:.1f}, {vp['ymax']:.1f}]"
            )
        sections.append("")

    # Named views from layer names
    if layer_groups:
        sections.append("NAMED VIEWS (from layer names):")
        for view_label, etypes in layer_groups.items():
            from collections import Counter
            counts = Counter(etypes)
            summary = ", ".join(f"{k}×{v}" for k, v in counts.most_common(5))
            sections.append(f"  {view_label}: {summary}")
        sections.append("")

    # Section views
    if section_views:
        sections.append(f"SECTION VIEWS DETECTED ({len(section_views)} cross-section(s)):")
        for sv in section_views:
            label_str = f" — labelled '{sv['label']}'" if sv["label"] else " — label not found"
            cutting_str = " (cutting plane line present)" if sv["cutting_plane_found"] else ""
            sections.append(
                f"  Hatch centroid ({sv['cx']:.1f}, {sv['cy']:.1f}){label_str}{cutting_str}"
            )
            sections.append(
                "  NOTE: Internal features (bores, slots, undercuts) are visible in this section."
            )
        sections.append("")

    if dim_entities:
        sections.append(f"DIMENSIONS ({len(dim_entities)} found):")
        for d in dim_entities:
            sections.append(f"  {d}")
        sections.append("")

    if text_dims:
        sections.append(f"DIMENSION ANNOTATIONS — parsed from text labels ({len(text_dims)} found):")
        for d in text_dims:
            sections.append(f"  {d}")
        sections.append("")

    if gdt_symbols:
        sections.append(f"GD&T SYMBOLS DETECTED ({len(gdt_symbols)} found):")
        for sym in gdt_symbols:
            sections.append(f"  {sym}")
        sections.append("  NOTE: Each GD&T symbol increases precision machining cost.")
        sections.append("")

    if main_circles or arc_raw:
        label = "CIRCLES / ARCS — MAIN VIEW"
        if has_centerline:
            label += " (rotational part — these are half-profiles; OD = largest diameter)"
        entries = [f"circle  r={r:.4f} {unit_label}  d={r*2:.4f} {unit_label}" for _, _, r in main_circles]
        entries += [f"arc  r={r:.4f} {unit_label}  d={r*2:.4f} {unit_label}" for _, _, r in arc_raw]
        sections.append(f"{label} ({len(entries)} found):")
        for e in entries[:50]:
            sections.append(f"  {e}")
        sections.append("")

    if end_circles:
        sections.append(
            f"CIRCLES — END / SECTION VIEW "
            f"({len(end_circles)} found, spatially separate from main profile):"
        )
        for _, _, r in sorted(end_circles, key=lambda t: t[2], reverse=True)[:20]:
            sections.append(f"  circle  r={r:.4f} {unit_label}  d={r*2:.4f} {unit_label}")
        sections.append("")

    if hatch_count and not section_views:
        # Only emit generic hatch count if detailed section detection didn't catch them
        sections.append(
            f"HATCH PATTERNS: {hatch_count} found — cross-section / sectional view present"
        )
        sections.append("")

    if has_centerline:
        sections.append("PART TYPE HINT: Center line detected — likely a rotational (turned) part.")
        sections.append("  Profile lines represent HALF the cross-section, mirrored about the axis.")
        sections.append("")

    # Extract named dimensions from annotation text (e.g. "Thickness 15mm", "OD 150mm, Bore 50mm")
    named_dims: list[str] = []
    for ann in annotation_texts:
        for m in _RE_NAMED_DIM.finditer(ann):
            kind_raw = m.group("kind").lower()
            kind = _NAMED_DIM_KIND_MAP.get(kind_raw, kind_raw)
            val = float(m.group("value"))
            named_dims.append(f"  {kind}: {val:.4f} {unit_label}  [from annotation \"{ann[:60]}\"]")
    if named_dims:
        sections.append(f"NAMED DIMENSIONS (extracted from annotation text, {len(named_dims)} found):")
        for d in named_dims:
            sections.append(d)
        sections.append("")

    if annotation_texts:
        sections.append(f"TEXT ANNOTATIONS ({len(annotation_texts)} found):")
        for t in annotation_texts[:60]:
            sections.append(f"  {t}")
        sections.append("")

    if leaders:
        sections.append(f"LEADERS ({len(leaders)} found):")
        for ln in leaders[:20]:
            sections.append(f"  {ln}")
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

    # Product name → process hints mapping
    _PRODUCT_PROCESS_HINTS: list[tuple[re.Pattern, list[str]]] = [
        (re.compile(r"\b(shaft|rod|pin|axle|spindle|bush|bushing|sleeve|tube|cylinder)\b", re.I),
         ["turning"]),
        (re.compile(r"\b(bracket|plate|flange|cover|housing|block|body|frame|lid)\b", re.I),
         ["milling_face", "drilling"]),
        (re.compile(r"\b(bolt|screw|stud|fastener)\b", re.I),
         ["turning", "threading"]),
        (re.compile(r"\b(nut|washer)\b", re.I),
         ["turning", "drilling"]),
        (re.compile(r"\b(gear|sprocket|pulley)\b", re.I),
         ["turning", "milling_slot"]),
    ]

    products = _RE_PRODUCT.findall(raw)
    inferred_processes: set[str] = set()
    if products:
        sections.append("PRODUCTS:")
        for pid, pname in products[:10]:
            if pid.strip() or pname.strip():
                sections.append(f"  - {pid.strip()} | {pname.strip()}")
                combined = f"{pid} {pname}".lower()
                for pattern, procs in _PRODUCT_PROCESS_HINTS:
                    if pattern.search(combined):
                        inferred_processes.update(procs)
        sections.append("")

    if inferred_processes:
        sections.append("PROCESS HINTS (inferred from product names):")
        for p in sorted(inferred_processes):
            sections.append(f"  {p}")
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

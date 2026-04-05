"""Tests for CAD file extraction (DXF + STEP)."""
import pytest
from extractors.cad_converter import (
    _step_to_text_fallback,
    _detect_units,
    _parse_text_dimension,
    _detect_centerline,
    _cluster_circles,
    dxf_to_text,
    step_to_text,
    is_dxf_dwg,
    is_step,
)


# ── MIME / extension helpers ──────────────────────────────────────────────────

class TestFileTypeDetection:
    def test_dxf_by_extension(self):
        assert is_dxf_dwg(None, "part.dxf")
        assert is_dxf_dwg(None, "DRAWING.DWG")
        assert is_dxf_dwg("application/octet-stream", "file.dxf")

    def test_dxf_by_mime(self):
        assert is_dxf_dwg("application/dxf", "file.bin")
        assert is_dxf_dwg("image/vnd.dxf", "unknown")

    def test_not_dxf(self):
        assert not is_dxf_dwg(None, "file.pdf")
        assert not is_dxf_dwg("application/pdf", "file.pdf")

    def test_step_by_extension(self):
        assert is_step(None, "part.step")
        assert is_step(None, "SHAFT.STP")
        assert is_step("application/octet-stream", "file.step")

    def test_step_by_mime(self):
        assert is_step("application/step", "file.bin")
        assert is_step("model/step", "unknown")

    def test_not_step(self):
        assert not is_step(None, "file.pdf")
        assert not is_step("application/pdf", "file.pdf")


# ── STEP fallback (regex) extraction ─────────────────────────────────────────

# Minimal valid ISO-10303-21 STEP file for testing
SAMPLE_STEP = b"""ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('Test Part'),'2;1');
FILE_NAME('test.step','2024-01-01',('Author'),('Org'),'','','');
FILE_SCHEMA(('AUTOMOTIVE_DESIGN'));
ENDSEC;
DATA;
#1=PRODUCT('SHAFT-001','Steel Shaft','',(#2));
#2=PRODUCT_DEFINITION_CONTEXT('detail design',#3,'design');
#3=APPLICATION_CONTEXT('automotive');
#10=CARTESIAN_POINT('origin',(0.0,0.0,0.0));
#11=CARTESIAN_POINT('p1',(100.0,0.0,0.0));
#12=CARTESIAN_POINT('p2',(100.0,50.0,0.0));
#13=CARTESIAN_POINT('p3',(0.0,50.0,80.0));
#20=CYLINDRICAL_SURFACE('outer',#100,25.0);
#21=CYLINDRICAL_SURFACE('bore',#101,10.0);
#30=CIRCLE('c1',#102,25.0);
#31=CIRCLE('c2',#103,10.0);
#40=MEASURE_WITH_UNIT(LENGTH_MEASURE(100.0),#500);
#41=MEASURE_WITH_UNIT(LENGTH_MEASURE(50.0),#500);
#42=MEASURE_WITH_UNIT(LENGTH_MEASURE(25.0),#500);
ENDSEC;
END-ISO-10303-21;
"""


class TestStepFallback:
    def test_extracts_product_name(self):
        result = _step_to_text_fallback(SAMPLE_STEP)
        assert "SHAFT-001" in result
        assert "Steel Shaft" in result

    def test_extracts_cylindrical_surfaces(self):
        result = _step_to_text_fallback(SAMPLE_STEP)
        assert "CYLINDRICAL FEATURES" in result
        # Should find both r=25 (outer) and r=10 (bore) from CYLINDRICAL_SURFACE + CIRCLE
        assert "25.0000" in result
        assert "10.0000" in result

    def test_extracts_bounding_box(self):
        result = _step_to_text_fallback(SAMPLE_STEP)
        assert "BOUNDING BOX" in result
        assert "100.0000" in result  # length from cartesian points

    def test_extracts_length_measures(self):
        result = _step_to_text_fallback(SAMPLE_STEP)
        assert "LENGTH MEASURES" in result

    def test_empty_step_file(self):
        minimal = b"""ISO-10303-21;
HEADER;
ENDSEC;
DATA;
ENDSEC;
END-ISO-10303-21;
"""
        result = _step_to_text_fallback(minimal)
        assert "STEP FILE" in result
        # Should not crash on minimal file

    def test_binary_garbage_raises(self):
        # Non-decodable bytes should still work (errors='replace')
        result = _step_to_text_fallback(b"\x00\x01\x02\xff\xfe")
        assert "STEP FILE" in result


class TestStepToText:
    def test_falls_back_when_occ_missing(self):
        """step_to_text should use regex fallback if OCC not installed."""
        result = step_to_text(SAMPLE_STEP)
        # On CI/local without cadquery-ocp, should still extract data
        assert "STEP FILE" in result
        assert "SHAFT-001" in result

    def test_returns_nonempty(self):
        result = step_to_text(SAMPLE_STEP)
        assert len(result) > 50


# ── Unit detection ────────────────────────────────────────────────────────────

class TestDetectUnits:
    def test_mm_header_stays_mm(self):
        assert _detect_units(4, []) == "mm"

    def test_meters_header_overridden_by_mm_annotation(self):
        # $INSUNITS=6 (meters) but annotation says "All dims in mm"
        assert _detect_units(6, ["All dims in mm"]) == "mm"

    def test_meters_header_kept_without_annotation(self):
        assert _detect_units(6, []) == "m"

    def test_unitless_header_no_override(self):
        assert _detect_units(0, ["title block only"]) == "unitless"

    def test_none_insunits(self):
        result = _detect_units(None, [])
        assert isinstance(result, str)


# ── TEXT dimension parsing ────────────────────────────────────────────────────

class TestParseTextDimension:
    def test_diameter_D50(self):
        assert _parse_text_dimension("D50") == ("diameter", 50.0)

    def test_diameter_with_decimal(self):
        assert _parse_text_dimension("D12.5") == ("diameter", 12.5)

    def test_diameter_phi_symbol(self):
        assert _parse_text_dimension("Ø75") == ("diameter", 75.0)

    def test_radius_R8(self):
        assert _parse_text_dimension("R8") == ("radius", 8.0)

    def test_thread_M12(self):
        kind, _ = _parse_text_dimension("M12x1.5")
        assert kind == "thread"

    def test_thread_M8_thru(self):
        kind, _ = _parse_text_dimension("M8 THRU")
        assert kind == "thread"

    def test_bare_integer(self):
        assert _parse_text_dimension("40") == ("linear", 40.0)

    def test_bare_decimal(self):
        assert _parse_text_dimension("120.5") == ("linear", 120.5)

    def test_non_dimension_text(self):
        assert _parse_text_dimension("STEPPED SHAFT") is None

    def test_material_text(self):
        assert _parse_text_dimension("Material: EN8") is None

    def test_multi_word(self):
        assert _parse_text_dimension("All dims in mm") is None


# ── Center line detection ─────────────────────────────────────────────────────

class TestDetectCenterline:
    # Stepped shaft: horizontal lines at y=±25, ±17.5, ±12.5 with center at y=0
    SHAFT_LINES = [
        (0, 25, 0, -25),      # left end cap
        (0, -25, 40, -25),    # bottom step 1
        (40, -25, 40, -17.5), # step down
        (40, -17.5, 80, -17.5),
        (80, -17.5, 80, -12.5),
        (80, -12.5, 120, -12.5),
        (120, -12.5, 120, 12.5),
        (120, 12.5, 80, 12.5),
        (80, 12.5, 80, 17.5),
        (80, 17.5, 40, 17.5),
        (40, 17.5, 40, 25),
        (40, 25, 0, 25),
        (-10, 0, 130, 0),     # center line
    ]

    # L-bracket: no symmetric profile
    BRACKET_LINES = [
        (0, 0, 100, 0),
        (100, 0, 100, 60),
        (100, 60, 80, 60),
        (80, 60, 80, 20),
        (80, 20, 0, 20),
        (0, 20, 0, 0),
    ]

    def test_shaft_has_centerline(self):
        assert _detect_centerline(self.SHAFT_LINES) is True

    def test_bracket_no_centerline(self):
        assert _detect_centerline(self.BRACKET_LINES) is False

    def test_empty_lines(self):
        assert _detect_centerline([]) is False


# ── Spatial circle clustering ─────────────────────────────────────────────────

class TestClusterCircles:
    def test_end_view_separated(self):
        # Main profile spans x=0-120; circles at x=200 are the end view
        circles = [(10, 0, 25.0), (10, 0, 17.5), (200, 0, 25.0), (200, 0, 17.5)]
        main_bbox = (0.0, 120.0, -25.0, 25.0)
        main, end = _cluster_circles(circles, main_bbox)
        assert len(end) == 2
        assert all(cx == 200 for cx, _, _ in end)

    def test_all_in_main_view(self):
        circles = [(10, 10, 5.0), (30, 10, 5.0), (50, 10, 5.0)]
        main_bbox = (0.0, 80.0, 0.0, 20.0)
        main, end = _cluster_circles(circles, main_bbox)
        assert len(main) == 3
        assert len(end) == 0

    def test_no_bbox_returns_all_main(self):
        circles = [(10, 0, 5.0), (200, 0, 5.0)]
        main, end = _cluster_circles(circles, None)
        assert len(main) == 2
        assert len(end) == 0


# ── Integration: real DXF files ───────────────────────────────────────────────

class TestDxfToTextIntegration:
    def _load(self, name: str) -> bytes:
        from pathlib import Path
        p = Path(__file__).parent.parent.parent / "test-files" / "dxf" / name
        return p.read_bytes()

    def test_stepped_shaft_units_mm(self):
        result = dxf_to_text(self._load("stepped_shaft.dxf"), "stepped_shaft.dxf")
        assert "UNITS: mm" in result

    def test_stepped_shaft_parsed_dimensions(self):
        result = dxf_to_text(self._load("stepped_shaft.dxf"), "stepped_shaft.dxf")
        assert 'diameter: 50.0000 mm' in result
        assert 'diameter: 35.0000 mm' in result
        assert 'diameter: 25.0000 mm' in result
        assert 'linear: 40.0000 mm' in result

    def test_stepped_shaft_centerline_hint(self):
        result = dxf_to_text(self._load("stepped_shaft.dxf"), "stepped_shaft.dxf")
        assert "rotational" in result.lower()

    def test_bracket_no_rotational_hint(self):
        result = dxf_to_text(self._load("sheet_metal_bracket.dxf"), "sheet_metal_bracket.dxf")
        assert "rotational" not in result.lower()

    def test_flange_units_mm(self):
        result = dxf_to_text(self._load("flange_plate.dxf"), "flange_plate.dxf")
        assert "UNITS: mm" in result

"""Tests for CAD file extraction (DXF + STEP)."""
import pytest
from extractors.cad_converter import (
    _step_to_text_fallback,
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

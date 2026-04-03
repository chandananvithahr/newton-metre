"""Tests for the similarity search engine — preprocessor, ranker, indexer, searcher.

DINOv2 and FAISS are mocked since they may not be installed in test env.
Ranker tests are pure math (no mocks needed).
"""
import json
import numpy as np
import pytest
from unittest.mock import patch, MagicMock
from PIL import Image
from io import BytesIO

from engines.similarity.ranker import (
    compute_material_score,
    compute_dimension_score,
    compute_process_score,
    compute_tolerance_score,
    compute_finish_score,
    rank_candidates,
    RankingWeights,
    RankedResult,
    PRESET_WEIGHTS,
)
from engines.similarity.preprocessor import (
    preprocess_drawing,
    _enhance_drawing,
    save_thumbnail,
    EMBED_SIZE,
    THUMBNAIL_SIZE,
)


# ═══════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════

def _make_test_image(width: int = 400, height: int = 300) -> bytes:
    """Create a simple test image as bytes."""
    img = Image.new("RGB", (width, height), color=(255, 255, 255))
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def _make_candidate(
    drawing_id: str,
    material: str = "EN8 Steel",
    od: float = 60,
    length: float = 100,
    processes: list[str] | None = None,
    visual_score: float = 0.9,
) -> tuple[dict, float]:
    """Create a mock FAISS candidate."""
    return (
        {
            "drawing_id": drawing_id,
            "material": material,
            "dimensions": {"outer_diameter_mm": od, "length_mm": length},
            "processes": processes or ["turning"],
            "file_name": f"{drawing_id}.pdf",
            "thumbnail_path": f"thumbnails/{drawing_id}.png",
            "historical_costs": [{"date": "2024-03", "supplier": "ABC", "unit_price_inr": 850, "qty": 100}],
            "physics_should_cost_inr": 820,
            "part_number": f"PN-{drawing_id}",
            "title": f"Part {drawing_id}",
            "revision": "Rev 1",
            "designer": "Test",
            "project": "Test Project",
            "notes": "",
        },
        visual_score,
    )


# ═══════════════════════════════════════════════════════════════
# Preprocessor tests
# ═══════════════════════════════════════════════════════════════

class TestPreprocessor:
    def test_preprocess_png(self):
        img_bytes = _make_test_image()
        embed_img, thumb = preprocess_drawing(img_bytes, "test.png")
        assert embed_img.size == EMBED_SIZE
        assert thumb.size[0] <= THUMBNAIL_SIZE[0]
        assert thumb.size[1] <= THUMBNAIL_SIZE[1]

    def test_preprocess_jpg(self):
        img = Image.new("RGB", (500, 400), color=(200, 200, 200))
        buf = BytesIO()
        img.save(buf, format="JPEG")
        embed_img, thumb = preprocess_drawing(buf.getvalue(), "test.jpg")
        assert embed_img.size == EMBED_SIZE
        assert embed_img.mode == "RGB"

    def test_preprocess_unsupported_format(self):
        with pytest.raises(ValueError, match="Unsupported"):
            preprocess_drawing(b"data", "test.dwg")

    def test_enhance_drawing(self):
        img = Image.new("RGB", (100, 100), color=(128, 128, 128))
        enhanced = _enhance_drawing(img)
        assert enhanced.size == img.size
        assert enhanced.mode == img.mode

    def test_save_thumbnail(self, tmp_path):
        img = Image.new("RGB", (300, 300))
        path = save_thumbnail(img, "test-001", tmp_path)
        assert path.exists()
        assert path.name == "test-001.png"

    def test_preprocess_grayscale_input(self):
        """Grayscale images should be converted to RGB."""
        img = Image.new("L", (400, 300), color=128)
        buf = BytesIO()
        img.save(buf, format="PNG")
        embed_img, _ = preprocess_drawing(buf.getvalue(), "gray.png")
        assert embed_img.mode == "RGB"


# ═══════════════════════════════════════════════════════════════
# Ranker tests (pure math, no mocks)
# ═══════════════════════════════════════════════════════════════

class TestMaterialScore:
    def test_exact_match(self):
        assert compute_material_score("EN8 Steel", "EN8 Steel") == 1.0

    def test_same_family(self):
        assert compute_material_score("EN8 Steel", "EN24 Steel") == 0.5
        assert compute_material_score("Mild Steel IS2062", "EN8 Steel") == 0.5

    def test_different_family(self):
        assert compute_material_score("EN8 Steel", "Aluminum 6061") == 0.0

    def test_unknown_material(self):
        assert compute_material_score("Unobtanium", "EN8 Steel") == 0.0


class TestDimensionScore:
    def test_identical_dims(self):
        dims = {"outer_diameter_mm": 60, "length_mm": 100}
        assert compute_dimension_score(dims, dims) == 1.0

    def test_similar_dims(self):
        q = {"outer_diameter_mm": 60, "length_mm": 100}
        c = {"outer_diameter_mm": 55, "length_mm": 95}
        score = compute_dimension_score(q, c)
        assert 0.8 < score < 1.0

    def test_very_different_dims(self):
        q = {"outer_diameter_mm": 60, "length_mm": 100}
        c = {"outer_diameter_mm": 200, "length_mm": 500}
        score = compute_dimension_score(q, c)
        assert score < 0.5

    def test_both_zero(self):
        """Both zero on a key = skip (don't count), so only explicitly-set keys matter."""
        q = {"outer_diameter_mm": 0, "length_mm": 0}
        c = {"outer_diameter_mm": 0, "length_mm": 0}
        # All keys are zero → all skipped → no scores → neutral 0.5
        assert compute_dimension_score(q, c) == 0.5

    def test_missing_dims(self):
        score = compute_dimension_score({}, {})
        assert score == 0.5  # both empty = neutral

    def test_sheet_metal_dims(self):
        """Should handle width/height/thickness for sheet metal parts."""
        q = {"width_mm": 500, "height_mm": 300, "thickness_mm": 2.0}
        c = {"width_mm": 480, "height_mm": 310, "thickness_mm": 2.0}
        score = compute_dimension_score(q, c)
        assert 0.9 < score < 1.0


class TestProcessScore:
    def test_identical_processes(self):
        procs = {"turning", "milling", "drilling"}
        assert compute_process_score(procs, procs) == 1.0

    def test_partial_overlap(self):
        q = {"turning", "milling", "drilling"}
        c = {"turning", "milling", "grinding"}
        score = compute_process_score(q, c)
        assert score == pytest.approx(0.5)  # 2/4

    def test_no_overlap(self):
        q = {"turning", "milling"}
        c = {"grinding", "heat_treatment"}
        assert compute_process_score(q, c) == 0.0

    def test_empty_sets(self):
        assert compute_process_score(set(), set()) == 1.0

    def test_one_empty(self):
        assert compute_process_score({"turning"}, set()) == 0.0


class TestToleranceScore:
    def test_identical_tolerances(self):
        tol = {"general_tolerance_mm": 0.1, "tightest_tolerance_mm": 0.01}
        assert compute_tolerance_score(tol, tol) == 1.0

    def test_similar_tolerances(self):
        q = {"general_tolerance_mm": 0.1, "tightest_tolerance_mm": 0.01}
        c = {"general_tolerance_mm": 0.12, "tightest_tolerance_mm": 0.02}
        score = compute_tolerance_score(q, c)
        assert 0.5 < score < 1.0

    def test_both_empty(self):
        assert compute_tolerance_score({}, {}) == 0.5  # neutral

    def test_one_specified_one_not(self):
        q = {"general_tolerance_mm": 0.1}
        c = {}
        score = compute_tolerance_score(q, c)
        assert score == 0.0


class TestFinishScore:
    def test_identical_ra(self):
        assert compute_finish_score(1.6, 1.6) == 1.0

    def test_similar_ra(self):
        score = compute_finish_score(1.6, 3.2)
        assert score == pytest.approx(0.5)

    def test_both_unknown(self):
        assert compute_finish_score(0, 0) == 0.5  # neutral

    def test_one_specified(self):
        assert compute_finish_score(1.6, 0) == 0.0


class TestRankCandidates:
    def test_ranks_by_combined_score(self):
        candidates = [
            _make_candidate("A", material="EN8 Steel", od=60, visual_score=0.9),
            _make_candidate("B", material="Aluminum 6061", od=200, visual_score=0.95),
            _make_candidate("C", material="EN8 Steel", od=58, visual_score=0.85),
        ]
        results = rank_candidates(
            candidates,
            query_material="EN8 Steel",
            query_dimensions={"outer_diameter_mm": 60, "length_mm": 100},
            query_processes=["turning"],
            top_k=3,
        )
        assert len(results) == 3
        # C or A should rank higher than B (material+dimension match outweighs visual)
        assert results[0].drawing_id in ("A", "C")
        # Scores should be descending
        assert results[0].combined_score >= results[1].combined_score

    def test_respects_top_k(self):
        candidates = [_make_candidate(f"D{i}", visual_score=0.9 - i * 0.01) for i in range(10)]
        results = rank_candidates(
            candidates, "EN8 Steel", {}, [], top_k=3,
        )
        assert len(results) == 3

    def test_custom_weights(self):
        candidates = [
            _make_candidate("A", material="EN8 Steel", od=60, visual_score=0.7),
            _make_candidate("B", material="Aluminum 6061", od=60, visual_score=0.99),
        ]
        # Procurement weights: material matters more
        results = rank_candidates(
            candidates, "EN8 Steel",
            {"outer_diameter_mm": 60, "length_mm": 100},
            ["turning"],
            weights=PRESET_WEIGHTS["procurement"],
        )
        # A should win because material match (1.0 vs 0.0) overcomes visual gap
        assert results[0].drawing_id == "A"

    def test_empty_candidates(self):
        results = rank_candidates([], "EN8 Steel", {}, [])
        assert results == []

    def test_result_has_score_breakdown(self):
        candidates = [_make_candidate("X", visual_score=0.8)]
        results = rank_candidates(
            candidates, "EN8 Steel",
            {"outer_diameter_mm": 60, "length_mm": 100},
            ["turning"],
        )
        r = results[0]
        assert isinstance(r, RankedResult)
        assert 0 <= r.visual_score <= 1
        assert 0 <= r.material_score <= 1
        assert 0 <= r.dimension_score <= 1
        assert 0 <= r.process_score <= 1
        assert 0 <= r.tolerance_score <= 1
        assert 0 <= r.finish_score <= 1
        assert r.combined_score > 0


class TestPresetWeights:
    def test_default_weights_sum_to_1(self):
        w = PRESET_WEIGHTS["default"]
        total = w.visual + w.material + w.dimension + w.process + w.tolerance + w.finish
        assert total == pytest.approx(1.0)

    def test_all_presets_sum_to_1(self):
        for name, w in PRESET_WEIGHTS.items():
            total = w.visual + w.material + w.dimension + w.process + w.tolerance + w.finish
            assert total == pytest.approx(1.0), f"Preset '{name}' sums to {total}"

    def test_all_presets_exist(self):
        assert "default" in PRESET_WEIGHTS
        assert "designer" in PRESET_WEIGHTS
        assert "procurement" in PRESET_WEIGHTS
        assert "qa" in PRESET_WEIGHTS

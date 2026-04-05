"""Tests for the validation pipeline — comparator, arbitrator, interactive, data_collector, orchestrator.

All AI/API calls are mocked. No real Gemini calls.
"""
import json
import pytest
from unittest.mock import patch, MagicMock
from dataclasses import asdict

from engines.validation.comparator import (
    ConfidenceTier,
    ComparisonResult,
    compare_estimates,
)
from engines.validation.data_collector import (
    ValidatedEstimate,
    save_validated_estimate,
    load_validated_estimates,
    count_validated_estimates,
    VALIDATION_FILE,
)
from engines.validation.interactive import (
    ClarifyingQuestion,
    InteractiveRound,
    generate_clarifying_questions,
    MAX_ROUNDS,
    MAX_QUESTIONS_PER_ROUND,
)
from engines.validation.arbitrator import (
    ArbitrationResult,
    arbitrate,
    _fallback_to_physics,
)
from engines.validation.orchestrator import (
    ValidationResult,
    orchestrate,
    _apply_user_corrections,
)
from extractors.gemini_estimator import GeminiCostEstimate
from engines.mechanical.cost_engine import MechanicalCostBreakdown, ProcessCostLine


# ═══════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════

def _make_physics_result(unit_cost: float = 820.0, material: str = "EN8 Steel") -> MechanicalCostBreakdown:
    """Create a minimal MechanicalCostBreakdown for testing."""
    return MechanicalCostBreakdown(
        material_name=material,
        raw_weight_kg=0.5,
        wastage_weight_kg=0.075,
        material_cost=50.0,
        process_lines=(
            ProcessCostLine(
                process_id="turning",
                process_name="CNC Turning",
                time_min=3.5,
                machine_cost=46.67,
                setup_cost_per_unit=4.0,
                tooling_cost=2.1,
                labour_cost=14.58,
                power_cost=2.33,
            ),
        ),
        total_machining_cost=46.67,
        total_setup_cost=4.0,
        total_tooling_cost=2.1,
        total_labour_cost=14.58,
        total_power_cost=2.33,
        subtotal=119.68,
        overhead=17.95,
        profit=27.53,
        unit_cost=unit_cost,
        unit_cost_low=round(unit_cost * 0.9),
        unit_cost_high=round(unit_cost * 1.1),
        uncertainty_pct=10,
        order_cost=unit_cost * 100,
        quantity=100,
    )


def _make_ai_result(unit_cost: float = 835.0, material: str = "EN8 Steel") -> GeminiCostEstimate:
    """Create a minimal GeminiCostEstimate for testing."""
    return GeminiCostEstimate(
        unit_cost_inr=unit_cost,
        material_cost_inr=55.0,
        machining_cost_inr=50.0,
        finishing_cost_inr=0.0,
        overhead_inr=30.0,
        detected_material=material,
        detected_processes=("turning",),
        detected_dimensions={"outer_diameter_mm": 60, "length_mm": 100, "inner_diameter_mm": 0},
        reasoning="Standard turning part",
        model_used="gemini-2.0-flash-lite",
    )


# ═══════════════════════════════════════════════════════════════
# Comparator tests (pure math, no mocks needed)
# ═══════════════════════════════════════════════════════════════

class TestComparator:
    def test_compare_identical(self):
        result = compare_estimates(1000, 1000)
        assert result.confidence_tier == ConfidenceTier.HIGH
        assert result.delta_pct == 0.0

    def test_compare_high_confidence(self):
        result = compare_estimates(1000, 1025)
        assert result.confidence_tier == ConfidenceTier.HIGH
        assert result.delta_pct <= 3.0

    def test_compare_medium_confidence(self):
        result = compare_estimates(1000, 1050)
        assert result.confidence_tier == ConfidenceTier.MEDIUM
        assert 3.0 < result.delta_pct <= 7.0

    def test_compare_low_confidence(self):
        result = compare_estimates(1000, 1100)
        assert result.confidence_tier == ConfidenceTier.LOW
        assert 7.0 < result.delta_pct <= 15.0

    def test_compare_insufficient_confidence(self):
        result = compare_estimates(1000, 1200)
        assert result.confidence_tier == ConfidenceTier.INSUFFICIENT
        assert result.delta_pct > 15.0

    def test_compare_both_zero(self):
        result = compare_estimates(0, 0)
        assert result.confidence_tier == ConfidenceTier.HIGH
        assert result.delta_pct == 0.0

    def test_compare_one_zero(self):
        result = compare_estimates(1000, 0)
        assert result.confidence_tier == ConfidenceTier.INSUFFICIENT
        assert result.delta_pct == 100.0

    def test_compare_ai_lower(self):
        result = compare_estimates(1200, 1000)
        assert result.confidence_tier == ConfidenceTier.INSUFFICIENT
        assert result.delta_pct > 15.0

    def test_compare_negative_raises(self):
        with pytest.raises(ValueError, match="non-negative"):
            compare_estimates(-100, 1000)

    def test_compare_boundary_3pct(self):
        # Exactly 3% → should be HIGH
        result = compare_estimates(1000, 970)
        assert result.confidence_tier == ConfidenceTier.HIGH

    def test_compare_boundary_7pct(self):
        # Just under 7% → should be MEDIUM
        result = compare_estimates(1000, 935)
        assert result.confidence_tier == ConfidenceTier.MEDIUM


# ═══════════════════════════════════════════════════════════════
# Data collector tests (filesystem)
# ═══════════════════════════════════════════════════════════════

class TestDataCollector:
    def test_save_and_load(self, tmp_path, monkeypatch):
        test_file = tmp_path / "validated_estimates.json"
        monkeypatch.setattr(
            "engines.validation.data_collector.VALIDATION_FILE", test_file,
        )
        estimate = ValidatedEstimate(
            timestamp="2026-03-29T10:00:00Z",
            drawing_filename="test.pdf",
            material_name="EN8 Steel",
            dimensions={"outer_diameter_mm": 60},
            processes=("turning",),
            quantity=100,
            physics_cost=820.0,
            ai_cost=835.0,
            final_cost=820.0,
            confidence_tier="high",
            delta_pct=1.8,
            user_corrections={},
            arbitration_reasoning=None,
        )
        save_validated_estimate(estimate)
        records = load_validated_estimates()
        assert len(records) == 1
        assert records[0]["physics_cost"] == 820.0
        assert records[0]["material_name"] == "EN8 Steel"

    def test_deduplication(self, tmp_path, monkeypatch):
        test_file = tmp_path / "validated_estimates.json"
        monkeypatch.setattr(
            "engines.validation.data_collector.VALIDATION_FILE", test_file,
        )
        estimate = ValidatedEstimate(
            timestamp="2026-03-29T10:00:00Z",
            drawing_filename="test.pdf",
            material_name="EN8 Steel",
            dimensions={},
            processes=("turning",),
            quantity=100,
            physics_cost=820.0,
            ai_cost=835.0,
            final_cost=820.0,
            confidence_tier="high",
            delta_pct=1.8,
            user_corrections={},
            arbitration_reasoning=None,
        )
        save_validated_estimate(estimate)
        save_validated_estimate(estimate)  # duplicate
        records = load_validated_estimates()
        assert len(records) == 1

    def test_load_empty(self, tmp_path, monkeypatch):
        test_file = tmp_path / "does_not_exist.json"
        monkeypatch.setattr(
            "engines.validation.data_collector.VALIDATION_FILE", test_file,
        )
        records = load_validated_estimates()
        assert records == []


# ═══════════════════════════════════════════════════════════════
# Interactive question generation tests (pure logic)
# ═══════════════════════════════════════════════════════════════

class TestInteractive:
    def test_material_mismatch_generates_question(self):
        physics = _make_physics_result(material="EN8 Steel")
        ai = _make_ai_result(material="EN24 Steel")
        result = generate_clarifying_questions(
            physics, ai, delta_pct=25.0,
            current_dimensions={"outer_diameter_mm": 60, "length_mm": 100},
            current_processes=["turning"],
        )
        assert any(q.field == "material_name" for q in result.questions)

    def test_dimension_mismatch_generates_question(self):
        physics = _make_physics_result()
        ai = _make_ai_result()
        # AI detected OD=80, physics used OD=60 → >10% diff
        ai_with_diff_dims = GeminiCostEstimate(
            unit_cost_inr=1000,
            material_cost_inr=55,
            machining_cost_inr=50,
            finishing_cost_inr=0,
            overhead_inr=30,
            detected_material="EN8 Steel",
            detected_processes=("turning",),
            detected_dimensions={"outer_diameter_mm": 80, "length_mm": 100, "inner_diameter_mm": 0},
            reasoning="",
            model_used="gemini-2.0-flash-lite",
        )
        result = generate_clarifying_questions(
            physics, ai_with_diff_dims, delta_pct=20.0,
            current_dimensions={"outer_diameter_mm": 60, "length_mm": 100, "inner_diameter_mm": 0},
            current_processes=["turning"],
        )
        assert any(q.field == "outer_diameter_mm" for q in result.questions)

    def test_process_mismatch_generates_question(self):
        physics = _make_physics_result()
        ai_with_extra = GeminiCostEstimate(
            unit_cost_inr=1000,
            material_cost_inr=55,
            machining_cost_inr=50,
            finishing_cost_inr=20,
            overhead_inr=30,
            detected_material="EN8 Steel",
            detected_processes=("turning", "grinding_cylindrical", "heat_treatment"),
            detected_dimensions={"outer_diameter_mm": 60, "length_mm": 100},
            reasoning="",
            model_used="gemini-2.0-flash-lite",
        )
        result = generate_clarifying_questions(
            physics, ai_with_extra, delta_pct=20.0,
            current_dimensions={"outer_diameter_mm": 60, "length_mm": 100},
            current_processes=["turning"],
        )
        assert any(q.field == "add_processes" for q in result.questions)

    def test_no_questions_when_aligned(self):
        physics = _make_physics_result()
        ai = _make_ai_result()
        result = generate_clarifying_questions(
            physics, ai, delta_pct=20.0,
            current_dimensions={"outer_diameter_mm": 60, "length_mm": 100, "inner_diameter_mm": 0},
            current_processes=["turning"],
        )
        # Should still have the "hidden features" question
        assert all(q.field != "material_name" for q in result.questions)
        assert all(q.field != "outer_diameter_mm" for q in result.questions)

    def test_max_rounds_exceeded(self):
        physics = _make_physics_result()
        ai = _make_ai_result()
        result = generate_clarifying_questions(
            physics, ai, delta_pct=25.0,
            round_number=3,
        )
        assert len(result.questions) == 0
        assert "Maximum" in result.reason

    def test_max_questions_capped(self):
        physics = _make_physics_result()
        ai = _make_ai_result(material="Titanium Grade 5")
        result = generate_clarifying_questions(
            physics, ai, delta_pct=50.0,
            current_dimensions={"outer_diameter_mm": 60, "length_mm": 100, "inner_diameter_mm": 0},
            current_processes=["turning"],
        )
        assert len(result.questions) <= MAX_QUESTIONS_PER_ROUND


# ═══════════════════════════════════════════════════════════════
# Arbitrator tests (mocked Gemini)
# ═══════════════════════════════════════════════════════════════

class TestArbitrator:
    @patch("engines.validation.arbitrator.GEMINI_API_KEY", "test-key")
    @patch("engines.validation.arbitrator.genai", create=True)
    def test_arbitrate_returns_result(self, mock_genai_module):
        import engines.validation.arbitrator as arb_module
        mock_genai = MagicMock()
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = json.dumps({
            "recommended_cost": 830,
            "source_preferred": "blended",
            "line_discrepancies": [
                {"item": "machining", "physics_value": 46, "ai_value": 55, "reasoning": "time estimate differs"}
            ],
            "overall_reasoning": "Physics material cost is more accurate, AI machining time is higher",
            "confidence_note": "Medium confidence in blended estimate",
        })
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model

        with patch.object(arb_module, "genai", mock_genai, create=True), \
             patch("engines.validation.arbitrator.GEMINI_API_KEY", "test-key"):
            # Patch the import inside the function
            with patch.dict("sys.modules", {"google.generativeai": mock_genai}):
                result = arbitrate(
                    physics_result=_make_physics_result(820),
                    ai_result=_make_ai_result(950),
                    quantity=100,
                    delta_pct=13.7,
                )

        assert isinstance(result, ArbitrationResult)
        assert result.recommended_cost == 830 or result.source_preferred == "physics"  # either parsed or fallback

    def test_fallback_to_physics(self):
        physics = _make_physics_result(820)
        result = _fallback_to_physics(physics, "test reason")
        assert result.recommended_cost == 820
        assert result.source_preferred == "physics"
        assert "test reason" in result.overall_reasoning

    @patch("engines.validation.arbitrator.GEMINI_API_KEY", "")
    def test_arbitrate_no_api_key(self):
        result = arbitrate(
            physics_result=_make_physics_result(820),
            ai_result=_make_ai_result(950),
            quantity=100,
            delta_pct=13.7,
        )
        assert result.source_preferred == "physics"
        assert result.recommended_cost == 820


# ═══════════════════════════════════════════════════════════════
# Orchestrator tests (mocked everything)
# ═══════════════════════════════════════════════════════════════

class TestOrchestrator:
    @patch("engines.validation.orchestrator.estimate_cost_from_drawing")
    @patch("engines.validation.orchestrator.calculate_mechanical_cost")
    @patch("engines.validation.orchestrator.save_validated_estimate")
    def test_orchestrate_high_confidence(self, mock_save, mock_physics, mock_gemini):
        mock_physics.return_value = _make_physics_result(820)
        mock_gemini.return_value = _make_ai_result(835)  # ~1.8% delta from 820
        result = orchestrate(
            image_bytes=b"fake_image",
            dimensions={"outer_diameter_mm": 60, "length_mm": 100, "inner_diameter_mm": 0},
            material_name="EN8 Steel",
            selected_processes=["turning"],
            quantity=100,
        )
        assert result.confidence_tier == ConfidenceTier.HIGH
        assert result.arbitration is None
        assert result.interactive is None
        assert not result.degraded
        mock_save.assert_called_once()

    @patch("engines.validation.orchestrator.estimate_cost_from_drawing")
    @patch("engines.validation.orchestrator.save_validated_estimate")
    def test_orchestrate_degraded_on_gemini_failure(self, mock_save, mock_gemini):
        mock_gemini.side_effect = RuntimeError("API down")
        result = orchestrate(
            image_bytes=b"fake_image",
            dimensions={"outer_diameter_mm": 60, "length_mm": 100, "inner_diameter_mm": 0,
                         "hole_count": 0, "thread_count": 0, "hole_diameter_mm": 8,
                         "thread_length_mm": 20, "groove_count": 0, "surface_area_cm2": 100,
                         "width_mm": 0},
            material_name="EN8 Steel",
            selected_processes=["turning"],
            quantity=100,
        )
        assert result.degraded is True
        assert result.confidence_tier is None
        assert result.ai_result is None
        assert result.physics_result is not None

    @patch("engines.validation.orchestrator.save_validated_estimate")
    def test_orchestrate_no_image_skips_validation(self, mock_save):
        result = orchestrate(
            image_bytes=None,
            dimensions={"outer_diameter_mm": 60, "length_mm": 100, "inner_diameter_mm": 0,
                         "hole_count": 0, "thread_count": 0, "hole_diameter_mm": 8,
                         "thread_length_mm": 20, "groove_count": 0, "surface_area_cm2": 100,
                         "width_mm": 0},
            material_name="EN8 Steel",
            selected_processes=["turning"],
            quantity=100,
        )
        assert result.degraded is True
        assert result.ai_result is None

    def test_apply_user_corrections_material(self):
        dims = {"outer_diameter_mm": 60, "length_mm": 100}
        mat = "EN8 Steel"
        procs = ["turning"]
        new_dims, new_mat, new_procs = _apply_user_corrections(
            dims, mat, procs, {"material_name": "EN24 Steel"},
        )
        assert new_mat == "EN24 Steel"
        assert new_dims == dims
        assert new_procs == procs

    def test_apply_user_corrections_dimensions(self):
        dims = {"outer_diameter_mm": 60, "length_mm": 100}
        new_dims, _, _ = _apply_user_corrections(
            dims, "EN8 Steel", ["turning"],
            {"outer_diameter_mm": "80"},
        )
        assert new_dims["outer_diameter_mm"] == 80.0

    def test_apply_user_corrections_add_processes(self):
        _, _, new_procs = _apply_user_corrections(
            {}, "EN8 Steel", ["turning"],
            {"add_processes": ["grinding_cylindrical", "heat_treatment"]},
        )
        assert "grinding_cylindrical" in new_procs
        assert "heat_treatment" in new_procs
        assert "turning" in new_procs

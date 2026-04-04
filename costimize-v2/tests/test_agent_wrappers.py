"""Tests for wrapper agents: ExtractionAgent, CostAgent, SimilarityAgent."""
import pytest
from unittest.mock import patch, MagicMock
from dataclasses import dataclass

from agents.types import AgentResult, WorkflowContext, WorkflowState, ExecutionMode
from agents.extraction_agent import ExtractionAgent
from agents.cost_agent import CostAgent, _detect_part_type
from agents.similarity_agent import SimilarityAgent
from agents.base import BaseAgent


def _ctx():
    return WorkflowContext(
        workflow_id="w1", user_id="u1", company_id="c1",
        workflow_type="estimate", execution_mode=ExecutionMode.HITL,
        state=WorkflowState.EXECUTING,
    )


# --- ExtractionAgent ---

class TestExtractionAgent:
    def test_satisfies_protocol(self):
        assert isinstance(ExtractionAgent(), BaseAgent)

    def test_name(self):
        assert ExtractionAgent().name == "extraction"

    def test_validate_with_image(self):
        ok, _ = ExtractionAgent().validate_inputs({"image_bytes": b"png"})
        assert ok

    def test_validate_with_step(self):
        ok, _ = ExtractionAgent().validate_inputs({"step_text": "STEP data"})
        assert ok

    def test_validate_with_images(self):
        ok, _ = ExtractionAgent().validate_inputs({"images": [b"a", b"b"]})
        assert ok

    def test_validate_missing_input(self):
        ok, reason = ExtractionAgent().validate_inputs({})
        assert not ok
        assert "image_bytes" in reason

    @patch("extractors.vision.analyze_drawing")
    def test_execute_image(self, mock_analyze):
        mock_analyze.return_value = {
            "material": "SS304",
            "dimensions": {"outer_diameter_mm": 50},
            "processes": ["turning"],
        }
        agent = ExtractionAgent()
        result = agent.execute(_ctx(), {"image_bytes": b"fake_png"})
        assert result.status == "success"
        assert result.data["material"] == "SS304"
        assert result.duration_ms > 0

    @patch("extractors.vision.analyze_step_text")
    def test_execute_step(self, mock_step):
        mock_step.return_value = {"material": "AL6061", "dimensions": {}}
        result = ExtractionAgent().execute(_ctx(), {"step_text": "STEP"})
        assert result.status == "success"
        assert result.data["material"] == "AL6061"

    @patch("extractors.vision.analyze_drawing", side_effect=RuntimeError("API down"))
    def test_execute_error(self, _):
        result = ExtractionAgent().execute(_ctx(), {"image_bytes": b"x"})
        assert result.status == "error"
        assert "API down" in result.error


# --- CostAgent ---

class TestPartTypeDetection:
    def test_explicit_override(self):
        assert _detect_part_type({"part_type": "pcb"}) == "pcb"

    def test_from_extraction_sheet_metal(self):
        assert _detect_part_type({"extraction": {"part_type": "Sheet Metal bracket"}}) == "sheet_metal"

    def test_from_extraction_pcb(self):
        assert _detect_part_type({"extraction": {"part_type": "PCB assembly"}}) == "pcb"

    def test_from_processes(self):
        assert _detect_part_type({"extraction": {"part_type": "", "processes": ["laser_cutting"]}}) == "sheet_metal"

    def test_default_mechanical(self):
        assert _detect_part_type({"extraction": {"part_type": "shaft"}}) == "mechanical"

    def test_empty_extraction(self):
        assert _detect_part_type({"extraction": {}}) == "mechanical"


class TestCostAgent:
    def test_satisfies_protocol(self):
        assert isinstance(CostAgent(), BaseAgent)

    def test_name(self):
        assert CostAgent().name == "cost"

    def test_validate_with_extraction(self):
        ok, _ = CostAgent().validate_inputs({"extraction": {"material": "SS304"}})
        assert ok

    def test_validate_with_dimensions(self):
        ok, _ = CostAgent().validate_inputs({"dimensions": {"outer_diameter_mm": 50}})
        assert ok

    def test_validate_missing(self):
        ok, reason = CostAgent().validate_inputs({})
        assert not ok

    @patch("engines.mechanical.cost_engine.calculate_mechanical_cost")
    def test_execute_mechanical(self, mock_calc):
        mock_breakdown = MagicMock()
        mock_calc.return_value = mock_breakdown

        with patch("agents.cost_agent._breakdown_to_dict", return_value={"unit_cost": 250.0}):
            result = CostAgent().execute(_ctx(), {
                "extraction": {
                    "material": "Mild Steel IS2062",
                    "dimensions": {"outer_diameter_mm": 50, "length_mm": 100},
                    "processes": ["turning"],
                    "part_type": "shaft",
                },
                "quantity": 10,
            })
        assert result.status == "success"
        assert result.data["unit_cost"] == 250.0
        assert result.data["part_type"] == "mechanical"

    @patch("engines.sheet_metal.cost_engine.calculate_sheet_metal_cost")
    def test_execute_sheet_metal(self, mock_calc):
        mock_calc.return_value = MagicMock()
        with patch("agents.cost_agent._breakdown_to_dict", return_value={"unit_cost": 180.0}):
            result = CostAgent().execute(_ctx(), {
                "part_type": "sheet_metal",
                "extraction": {
                    "material": "Mild Steel CR",
                    "dimensions": {"thickness_mm": 2, "length_mm": 200, "width_mm": 150,
                                   "cutting_length_mm": 700, "pierce_count": 4},
                },
                "quantity": 50,
            })
        assert result.status == "success"
        assert result.data["part_type"] == "sheet_metal"

    def test_execute_unknown_part_type(self):
        result = CostAgent().execute(_ctx(), {
            "part_type": "unknown_type",
            "extraction": {},
        })
        assert result.status == "error"
        assert "Unknown part type" in result.error


# --- SimilarityAgent ---

class TestSimilarityAgent:
    def test_satisfies_protocol(self):
        assert isinstance(SimilarityAgent(), BaseAgent)

    def test_name(self):
        assert SimilarityAgent().name == "similarity"

    def test_validate_with_image(self):
        ok, _ = SimilarityAgent().validate_inputs({"image_bytes": b"x"})
        assert ok

    def test_validate_with_extraction(self):
        ok, _ = SimilarityAgent().validate_inputs({"extraction": {"material": "SS"}})
        assert ok

    def test_validate_missing(self):
        ok, reason = SimilarityAgent().validate_inputs({})
        assert not ok

    @patch("engines.similarity.searcher.DrawingSearcher")
    def test_execute_returns_matches(self, MockSearcher):
        mock_result = MagicMock()
        mock_result.drawing_id = "d1"
        mock_result.combined_score = 0.95
        mock_result.material = "SS304"
        MockSearcher.return_value.search.return_value = [mock_result]

        result = SimilarityAgent().execute(_ctx(), {
            "image_bytes": b"fake",
            "extraction": {"material": "SS304", "dimensions": {}, "processes": []},
        })
        assert result.status == "success"
        assert result.data["match_count"] == 1
        assert result.data["matches"][0]["drawing_id"] == "d1"

    @patch("engines.similarity.searcher.DrawingSearcher", side_effect=ImportError("no torch"))
    def test_execute_graceful_degradation(self, _):
        """Similarity is non-critical — should return error on import failure."""
        result = SimilarityAgent().execute(_ctx(), {
            "image_bytes": b"fake",
            "extraction": {},
        })
        assert result.status == "error"

"""Tests for RFQAgent — RFQ document construction and email generation."""
import pytest
from unittest.mock import patch, MagicMock

from agents.types import AgentResult, WorkflowContext, WorkflowState, ExecutionMode
from agents.rfq_agent import RFQAgent, _check_forbidden_content, _format_dimensions
from agents.base import BaseAgent


def _ctx():
    return WorkflowContext(
        workflow_id="w1", user_id="u1", company_id="c1",
        workflow_type="rfq", execution_mode=ExecutionMode.HITL,
        state=WorkflowState.EXECUTING,
        inputs={"quantity": 100},
    )


class TestRFQAgentProtocol:
    def test_satisfies_protocol(self):
        assert isinstance(RFQAgent(), BaseAgent)

    def test_name(self):
        assert RFQAgent().name == "rfq"


class TestRFQValidation:
    def test_valid_with_extraction(self):
        ok, _ = RFQAgent().validate_inputs({"extraction": {"material": "SS304"}})
        assert ok

    def test_invalid_without_extraction(self):
        ok, reason = RFQAgent().validate_inputs({"some_other": "data"})
        assert not ok
        assert "extraction" in reason


class TestForbiddenContentCheck:
    def test_clean_email(self):
        assert _check_forbidden_content("Dear supplier, please quote for this part.") == []

    def test_detects_should_cost(self):
        violations = _check_forbidden_content("Our should-cost estimate is Rs 500.")
        assert "should-cost" in violations

    def test_detects_target_price(self):
        violations = _check_forbidden_content("Our target price is below Rs 400.")
        assert "target price" in violations

    def test_detects_internal(self):
        violations = _check_forbidden_content("For internal use, our budget is Rs 1000.")
        assert "internal" in violations
        assert "budget" in violations

    def test_case_insensitive(self):
        violations = _check_forbidden_content("Our SHOULD COST is low.")
        assert len(violations) > 0


class TestFormatDimensions:
    def test_empty(self):
        assert _format_dimensions({}) == "As per drawing"

    def test_basic(self):
        result = _format_dimensions({"outer_diameter_mm": 50, "length_mm": 100})
        assert "Outer Diameter" in result
        assert "50mm" in result
        assert "Length" in result


class TestRFQExecution:
    @patch("agents.rfq_agent.call_llm")
    def test_generates_email_draft(self, mock_llm):
        mock_llm.return_value = MagicMock(
            content='{"subject": "RFQ: Shaft - SS304", "body": "Dear Vendor, please quote.", "attachments_needed": ["drawing.pdf"]}'
        )

        result = RFQAgent().execute(_ctx(), {
            "extraction": {
                "material": "SS304",
                "dimensions": {"outer_diameter_mm": 50, "length_mm": 100},
                "processes": ["turning", "grinding"],
                "part_type": "Shaft",
            },
            "cost": {"unit_cost": 350.0},
            "similarity": {"matches": []},
            "target_suppliers": [{"name": "ABC Metals", "email": "abc@example.com"}],
            "quantity": 100,
        })

        assert result.status == "success"
        assert result.data["draft_count"] == 1
        assert result.data["email_drafts"][0]["subject"] == "RFQ: Shaft - SS304"
        assert result.data["rfq_document"]["material"] == "SS304"
        assert result.data["rfq_document"]["quantity"] == 100
        assert result.llm_calls == 1

    @patch("agents.rfq_agent.call_llm")
    def test_multiple_suppliers(self, mock_llm):
        mock_llm.return_value = MagicMock(
            content='{"subject": "RFQ", "body": "Dear supplier", "attachments_needed": []}'
        )

        result = RFQAgent().execute(_ctx(), {
            "extraction": {"material": "AL6061", "dimensions": {}, "processes": []},
            "target_suppliers": [
                {"name": "Vendor A"},
                {"name": "Vendor B"},
                {"name": "Vendor C"},
            ],
        })

        assert result.data["draft_count"] == 3
        assert result.llm_calls == 3

    @patch("agents.rfq_agent.call_llm")
    def test_should_cost_not_in_rfq_document_for_supplier(self, mock_llm):
        """Should-cost is stored internally but NEVER in email body."""
        mock_llm.return_value = MagicMock(
            content='{"subject": "RFQ", "body": "Dear supplier, please quote.", "attachments_needed": []}'
        )

        result = RFQAgent().execute(_ctx(), {
            "extraction": {"material": "SS304", "dimensions": {}, "processes": []},
            "cost": {"unit_cost": 500.0},
        })

        # Internal reference exists
        assert result.data["rfq_document"]["should_cost_ref"] == 500.0
        # But email body doesn't contain it
        body = result.data["email_drafts"][0]["body"]
        assert "500" not in body

    @patch("agents.rfq_agent.call_llm", side_effect=RuntimeError("LLM down"))
    def test_llm_failure_graceful(self, _):
        result = RFQAgent().execute(_ctx(), {
            "extraction": {"material": "SS304", "dimensions": {}, "processes": []},
            "target_suppliers": [{"name": "Vendor"}],
        })

        assert result.status == "success"  # Agent doesn't fail, drafts have errors
        assert "error" in result.data["email_drafts"][0]

    @patch("agents.rfq_agent.call_llm")
    def test_uses_default_suppliers(self, mock_llm):
        """If no target_suppliers provided, uses default."""
        mock_llm.return_value = MagicMock(
            content='{"subject": "RFQ", "body": "text", "attachments_needed": []}'
        )
        result = RFQAgent().execute(_ctx(), {
            "extraction": {"material": "Steel", "dimensions": {}, "processes": []},
        })
        assert result.data["draft_count"] == 1

    @patch("agents.rfq_agent.call_llm")
    def test_with_similarity_context(self, mock_llm):
        mock_llm.return_value = MagicMock(
            content='{"subject": "RFQ", "body": "text", "attachments_needed": []}'
        )
        result = RFQAgent().execute(_ctx(), {
            "extraction": {"material": "SS304", "dimensions": {}, "processes": []},
            "similarity": {
                "matches": [
                    {"drawing_id": "d1", "material": "SS304"},
                    {"drawing_id": "d2", "material": "SS316"},
                ]
            },
        })
        assert result.status == "success"

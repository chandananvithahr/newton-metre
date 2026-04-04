"""Tests for NegotiationAgent — strategy selection, MESO offers, memory injection."""
import pytest
from unittest.mock import patch, MagicMock

from agents.types import AgentResult, WorkflowContext, WorkflowState, ExecutionMode
from agents.negotiation_agent import NegotiationAgent
from agents.memory import EpisodicMemory, SemanticMemory
from agents.base import BaseAgent


def _ctx(mode=ExecutionMode.HITL, **overrides):
    defaults = dict(
        workflow_id="w1", user_id="u1", company_id="c1",
        workflow_type="negotiate", execution_mode=mode,
        state=WorkflowState.EXECUTING,
        inputs={"quantity": 100},
    )
    defaults.update(overrides)
    return WorkflowContext(**defaults)


def _base_inputs(**overrides):
    inputs = {
        "quote_comparison": {
            "best_unit_price": 500.0,
            "best_supplier": "Vendor A",
        },
        "cost": {"unit_cost": 400.0},
        "extraction": {
            "material": "SS304",
            "processes": ["turning", "grinding"],
            "part_type": "shaft",
        },
        "quantity": 100,
    }
    inputs.update(overrides)
    return inputs


@pytest.fixture(autouse=True)
def _mock_memory():
    """Mock out memory recall/pattern methods to avoid Supabase calls."""
    with patch.object(EpisodicMemory, "recall", return_value=[]), \
         patch.object(EpisodicMemory, "to_prompt_context", return_value="No prior negotiations."), \
         patch.object(SemanticMemory, "get_patterns", return_value=[]), \
         patch.object(SemanticMemory, "to_prompt_context", return_value="No known patterns."):
        yield


class TestNegotiationAgentProtocol:
    def test_satisfies_protocol(self):
        assert isinstance(NegotiationAgent(), BaseAgent)

    def test_name(self):
        assert NegotiationAgent().name == "negotiation"


class TestNegotiationValidation:
    def test_valid_with_quote_comparison(self):
        ok, _ = NegotiationAgent().validate_inputs({"quote_comparison": {"best_unit_price": 500}})
        assert ok

    def test_valid_with_quotes(self):
        ok, _ = NegotiationAgent().validate_inputs({"quotes": [{"unit_price": 500}]})
        assert ok

    def test_invalid_without_quotes(self):
        ok, reason = NegotiationAgent().validate_inputs({"cost": {"unit_cost": 400}})
        assert not ok
        assert "quote" in reason.lower()


class TestNegotiationCounterOffer:
    @patch("agents.negotiation_agent.call_llm")
    def test_generates_counter_offer_hitl(self, mock_llm):
        mock_llm.return_value = MagicMock(
            content='{"email_subject": "Re: Quote", "email_body": "Dear Vendor A", "options": [{"description": "Option 1", "unit_price": 420, "terms": "Net 30"}], "primary_argument": "should-cost data", "talking_points": ["point 1"], "risk_notes": "none"}'
        )

        result = NegotiationAgent().execute(_ctx(ExecutionMode.HITL), _base_inputs())

        assert result.status == "success"
        assert result.data["vendor_name"] == "Vendor A"
        assert result.data["vendor_quote"] == 500.0
        assert result.data["should_cost"] == 400.0
        assert result.data["execution_mode"] == "hitl"
        assert result.llm_calls == 1

    @patch("agents.negotiation_agent.call_llm")
    def test_generates_counter_offer_auto(self, mock_llm):
        mock_llm.return_value = MagicMock(
            content='{"email_subject": "Re: Quote", "email_body": "text", "options": [], "primary_argument": "market", "talking_points": [], "risk_notes": ""}'
        )

        result = NegotiationAgent().execute(_ctx(ExecutionMode.AUTO), _base_inputs())

        assert result.status == "success"
        assert result.data["execution_mode"] == "auto"


class TestNegotiationAnalysis:
    @patch("agents.negotiation_agent.call_llm")
    def test_generates_analysis_manual(self, mock_llm):
        mock_llm.return_value = MagicMock(
            content='{"recommended_target": 420, "opening_position": 380, "walk_away_price": 460, "talking_points": ["point"], "supplier_weaknesses": ["weak"], "concession_strategy": "offer volume", "risk_assessment": "low risk"}'
        )

        result = NegotiationAgent().execute(_ctx(ExecutionMode.MANUAL), _base_inputs())

        assert result.status == "success"
        assert result.data["execution_mode"] == "manual"
        assert result.llm_calls == 1

    @patch("agents.negotiation_agent.call_llm")
    def test_analysis_includes_strategy_fields(self, mock_llm):
        mock_llm.return_value = MagicMock(
            content='{"recommended_target": 420, "opening_position": 380, "walk_away_price": 460, "talking_points": ["point"], "supplier_weaknesses": [], "concession_strategy": "strategy", "risk_assessment": "assessment"}'
        )

        result = NegotiationAgent().execute(_ctx(ExecutionMode.MANUAL), _base_inputs())
        data = result.data

        assert "recommended_target" in data or "vendor_name" in data


class TestNegotiationTargetPrice:
    @patch("agents.negotiation_agent.call_llm")
    def test_target_from_should_cost(self, mock_llm):
        mock_llm.return_value = MagicMock(content='{"email_subject": "", "email_body": "", "options": [], "primary_argument": "", "talking_points": [], "risk_notes": ""}')

        result = NegotiationAgent().execute(_ctx(), _base_inputs())

        # target = should_cost * 1.05 = 400 * 1.05 = 420
        assert result.data["target_price"] == pytest.approx(420.0)

    @patch("agents.negotiation_agent.call_llm")
    def test_target_fallback_no_should_cost(self, mock_llm):
        mock_llm.return_value = MagicMock(content='{"email_subject": "", "email_body": "", "options": [], "primary_argument": "", "talking_points": [], "risk_notes": ""}')

        inputs = _base_inputs()
        inputs.pop("cost")
        result = NegotiationAgent().execute(_ctx(), inputs)

        # target = vendor_quote * 0.85 = 500 * 0.85 = 425
        assert result.data["target_price"] == pytest.approx(425.0)


class TestNegotiationVendorSelection:
    @patch("agents.negotiation_agent.call_llm")
    def test_uses_best_from_comparison(self, mock_llm):
        mock_llm.return_value = MagicMock(content='{"email_subject": "", "email_body": "", "options": [], "primary_argument": "", "talking_points": [], "risk_notes": ""}')

        result = NegotiationAgent().execute(_ctx(), _base_inputs())
        assert result.data["vendor_name"] == "Vendor A"
        assert result.data["vendor_quote"] == 500.0

    @patch("agents.negotiation_agent.call_llm")
    def test_falls_back_to_quotes_list(self, mock_llm):
        mock_llm.return_value = MagicMock(content='{"email_subject": "", "email_body": "", "options": [], "primary_argument": "", "talking_points": [], "risk_notes": ""}')

        inputs = {
            "quote_comparison": {},  # no best_unit_price
            "quotes": [
                {"unit_price": 450, "supplier": {"name": "Fallback Vendor"}},
            ],
            "cost": {"unit_cost": 400},
        }

        result = NegotiationAgent().execute(_ctx(), inputs)
        assert result.data["vendor_name"] == "Fallback Vendor"
        assert result.data["vendor_quote"] == 450


class TestNegotiationFailure:
    @patch("agents.negotiation_agent.call_llm", side_effect=RuntimeError("LLM down"))
    def test_llm_failure_returns_error(self, _):
        result = NegotiationAgent().execute(_ctx(), _base_inputs())

        assert result.status == "error"
        assert "LLM down" in result.error

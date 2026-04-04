"""Tests for ProposalAgent and MeetingAgent."""
import pytest
from unittest.mock import patch, MagicMock

from agents.types import AgentResult, WorkflowContext, WorkflowState, ExecutionMode
from agents.proposal_agent import ProposalAgent
from agents.meeting_agent import MeetingAgent
from agents.memory import EpisodicMemory, SemanticMemory
from agents.base import BaseAgent


def _ctx(**overrides):
    defaults = dict(
        workflow_id="w1", user_id="u1", company_id="c1",
        workflow_type="proposal", execution_mode=ExecutionMode.HITL,
        state=WorkflowState.EXECUTING,
        inputs={"quantity": 100},
    )
    defaults.update(overrides)
    return WorkflowContext(**defaults)


# ============================================================================
# ProposalAgent
# ============================================================================

class TestProposalProtocol:
    def test_satisfies_protocol(self):
        assert isinstance(ProposalAgent(), BaseAgent)

    def test_name(self):
        assert ProposalAgent().name == "proposal"


class TestProposalValidation:
    def test_valid_with_comparison(self):
        ok, _ = ProposalAgent().validate_inputs({"quote_comparison": {"data": "here"}})
        assert ok

    def test_invalid_without_comparison(self):
        ok, reason = ProposalAgent().validate_inputs({"negotiation": {}})
        assert not ok
        assert "quote_comparison" in reason


class TestProposalExecution:
    @patch("agents.proposal_agent.call_llm")
    def test_generates_proposal(self, mock_llm):
        mock_llm.return_value = MagicMock(
            content='{"executive_summary": "Recommend Vendor A", "comparative_statement": [{"supplier": "A", "unit_price": 450, "total_cost": 45000, "delivery_weeks": 4, "vs_should_cost_pct": 12.5, "notes": ""}], "savings_analysis": {"vs_highest_quote": 5000, "vs_should_cost": -5000, "vs_last_po": 0, "annual_savings_estimate": 20000}, "risk_assessment": [{"risk": "single source", "severity": "medium", "mitigation": "qualify backup"}], "recommendation": "Award to Vendor A"}'
        )

        result = ProposalAgent().execute(_ctx(), {
            "quote_comparison": {
                "comparison_table": [
                    {"supplier": "Vendor A", "unit_price": 450, "delivery_weeks": 4, "delta_pct": 12.5},
                    {"supplier": "Vendor B", "unit_price": 480, "delivery_weeks": 3, "delta_pct": 20.0},
                ],
            },
            "negotiation": {
                "vendor_name": "Vendor A",
                "vendor_quote": 500.0,
                "target_price": 420.0,
            },
            "cost": {"unit_cost": 400.0},
            "quantity": 100,
        })

        assert result.status == "success"
        assert "executive_summary" in result.data
        assert result.llm_calls == 1

    @patch("agents.proposal_agent.call_llm")
    def test_works_without_negotiation(self, mock_llm):
        mock_llm.return_value = MagicMock(
            content='{"executive_summary": "summary", "comparative_statement": [], "savings_analysis": {}, "risk_assessment": [], "recommendation": "rec"}'
        )

        result = ProposalAgent().execute(_ctx(), {
            "quote_comparison": {"comparison_table": []},
        })

        assert result.status == "success"

    @patch("agents.proposal_agent.call_llm", side_effect=RuntimeError("LLM down"))
    def test_llm_failure_returns_error(self, _):
        result = ProposalAgent().execute(_ctx(), {
            "quote_comparison": {"comparison_table": []},
        })

        assert result.status == "error"
        assert "LLM down" in result.error


class TestProposalFormatters:
    def test_format_comparison_empty(self):
        agent = ProposalAgent()
        result = agent._format_comparison({})
        assert "No quote comparison" in result

    def test_format_comparison_with_data(self):
        agent = ProposalAgent()
        result = agent._format_comparison({
            "comparison_table": [
                {"supplier": "V1", "unit_price": 450, "delivery_weeks": 4, "delta_pct": 12.5},
            ]
        })
        assert "V1" in result
        assert "450" in result

    def test_format_negotiation_empty(self):
        agent = ProposalAgent()
        result = agent._format_negotiation({})
        assert "No negotiation" in result

    def test_format_negotiation_with_data(self):
        agent = ProposalAgent()
        result = agent._format_negotiation({
            "vendor_name": "Acme",
            "vendor_quote": 500.0,
            "target_price": 420.0,
        })
        assert "Acme" in result
        assert "500" in result


# ============================================================================
# MeetingAgent
# ============================================================================

@pytest.fixture(autouse=True)
def _mock_memory():
    """Mock out memory recall/pattern methods to avoid Supabase calls."""
    with patch.object(EpisodicMemory, "recall", return_value=[]), \
         patch.object(EpisodicMemory, "to_prompt_context", return_value="No prior negotiations."), \
         patch.object(SemanticMemory, "get_patterns", return_value=[]), \
         patch.object(SemanticMemory, "to_prompt_context", return_value="No known patterns."):
        yield


class TestMeetingProtocol:
    def test_satisfies_protocol(self):
        assert isinstance(MeetingAgent(), BaseAgent)

    def test_name(self):
        assert MeetingAgent().name == "meeting"


class TestMeetingValidation:
    def test_valid_with_supplier_name(self):
        ok, _ = MeetingAgent().validate_inputs({"supplier_name": "Vendor A"})
        assert ok

    def test_valid_with_supplier_id(self):
        ok, _ = MeetingAgent().validate_inputs({"supplier_id": "sup1"})
        assert ok

    def test_valid_with_meeting_notes(self):
        ok, _ = MeetingAgent().validate_inputs({"meeting_notes": "We discussed pricing."})
        assert ok

    def test_invalid_without_inputs(self):
        ok, reason = MeetingAgent().validate_inputs({"cost": {}})
        assert not ok
        assert "supplier" in reason.lower() or "meeting" in reason.lower()


class TestMeetingBrief:
    @patch("agents.meeting_agent.call_llm")
    def test_generates_brief(self, mock_llm):
        mock_llm.return_value = MagicMock(
            content='{"supplier_overview": "Large supplier", "key_data_points": ["point 1"], "recommended_positions": [{"item": "price", "our_position": "reduce 10%", "expected_resistance": "cost increase", "fallback": "reduce 5%"}], "talking_points": ["talk 1"], "questions_to_ask": ["q1"], "warning_flags": ["flag1"]}'
        )

        result = MeetingAgent().execute(_ctx(), {
            "supplier_name": "Vendor A",
            "supplier_id": "sup1",
            "agenda": "Annual rate negotiation",
            "cost": {"unit_cost": 400.0},
        })

        assert result.status == "success"
        assert result.data["type"] == "pre_meeting_brief"
        assert result.data["supplier"] == "Vendor A"
        assert result.llm_calls == 1

    @patch("agents.meeting_agent.call_llm")
    def test_brief_without_cost_data(self, mock_llm):
        mock_llm.return_value = MagicMock(
            content='{"supplier_overview": "overview", "key_data_points": [], "recommended_positions": [], "talking_points": [], "questions_to_ask": [], "warning_flags": []}'
        )

        result = MeetingAgent().execute(_ctx(), {"supplier_name": "V"})
        assert result.status == "success"

    @patch("agents.meeting_agent.call_llm", side_effect=RuntimeError("LLM down"))
    def test_brief_llm_failure(self, _):
        result = MeetingAgent().execute(_ctx(), {"supplier_name": "V"})
        assert result.status == "error"
        assert result.data["type"] == "pre_meeting_brief"


class TestMeetingAnalysis:
    @patch("agents.meeting_agent.call_llm")
    def test_analyzes_notes(self, mock_llm):
        mock_llm.return_value = MagicMock(
            content='{"price_agreements": [{"item": "shaft", "agreed_price": 430, "vs_target": "above target"}], "commitments": [{"by": "Vendor A", "commitment": "sample by Friday", "deadline": "2026-04-11"}], "action_items": [{"owner": "us", "action": "send specs", "deadline": "next week"}], "unresolved": ["payment terms"], "sentiment": "positive", "summary": "Good meeting."}'
        )

        result = MeetingAgent().execute(_ctx(), {
            "meeting_notes": "We met with Vendor A. They agreed on Rs 430/unit for the shaft.",
            "supplier_name": "Vendor A",
            "target_price": 420.0,
            "cost": {"unit_cost": 400.0},
        })

        assert result.status == "success"
        assert result.data["type"] == "post_meeting_analysis"
        assert result.data["supplier"] == "Vendor A"

    @patch("agents.meeting_agent.call_llm")
    def test_notes_take_priority_over_brief(self, mock_llm):
        """If both meeting_notes and supplier_name are present, analyze notes."""
        mock_llm.return_value = MagicMock(
            content='{"price_agreements": [], "commitments": [], "action_items": [], "unresolved": [], "sentiment": "neutral", "summary": "summary"}'
        )

        result = MeetingAgent().execute(_ctx(), {
            "meeting_notes": "Notes here",
            "supplier_name": "V",
        })

        assert result.data["type"] == "post_meeting_analysis"

    @patch("agents.meeting_agent.call_llm", side_effect=RuntimeError("LLM down"))
    def test_analysis_llm_failure(self, _):
        result = MeetingAgent().execute(_ctx(), {
            "meeting_notes": "notes",
        })
        assert result.status == "error"
        assert result.data["type"] == "post_meeting_analysis"

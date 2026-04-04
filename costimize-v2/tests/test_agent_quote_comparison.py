"""Tests for QuoteComparisonAgent — quote normalization, benchmarking, anomaly detection."""
import pytest
from unittest.mock import patch, MagicMock

from agents.types import AgentResult, WorkflowContext, WorkflowState, ExecutionMode
from agents.quote_comparison_agent import QuoteComparisonAgent
from agents.base import BaseAgent


def _ctx(**overrides):
    defaults = dict(
        workflow_id="w1", user_id="u1", company_id="c1",
        workflow_type="compare_quotes", execution_mode=ExecutionMode.HITL,
        state=WorkflowState.EXECUTING,
        inputs={"quantity": 100},
    )
    defaults.update(overrides)
    return WorkflowContext(**defaults)


def _structured_quotes():
    return [
        {
            "supplier": {"name": "Vendor A"},
            "unit_price": 450.0,
            "delivery_weeks": 4,
            "tooling_charges": 500,
            "payment_terms": "Net 30",
        },
        {
            "supplier": {"name": "Vendor B"},
            "unit_price": 480.0,
            "delivery_weeks": 3,
            "tooling_charges": 0,
            "payment_terms": "Net 45",
        },
        {
            "supplier": {"name": "Vendor C"},
            "unit_price": 520.0,
            "delivery_weeks": 6,
            "tooling_charges": 1000,
            "payment_terms": "Advance 50%",
        },
    ]


class TestQuoteComparisonProtocol:
    def test_satisfies_protocol(self):
        assert isinstance(QuoteComparisonAgent(), BaseAgent)

    def test_name(self):
        assert QuoteComparisonAgent().name == "quote_comparison"


class TestQuoteComparisonValidation:
    def test_valid_with_quotes(self):
        ok, _ = QuoteComparisonAgent().validate_inputs({"quotes": [{"unit_price": 100}]})
        assert ok

    def test_invalid_without_quotes(self):
        ok, reason = QuoteComparisonAgent().validate_inputs({"cost": {"unit_cost": 500}})
        assert not ok
        assert "quotes" in reason.lower()


class TestQuoteComparisonExecution:
    def test_structured_quotes_comparison(self):
        agent = QuoteComparisonAgent()
        result = agent.execute(_ctx(), {
            "quotes": _structured_quotes(),
            "cost": {"unit_cost": 400.0},
            "quantity": 100,
        })

        assert result.status == "success"
        assert result.agent_name == "quote_comparison"
        assert result.llm_calls == 0  # no raw text extraction needed

        data = result.data
        assert data["quote_count"] == 3
        assert len(data["comparison_table"]) == 3

    def test_ranks_by_total_cost(self):
        agent = QuoteComparisonAgent()
        result = agent.execute(_ctx(), {
            "quotes": _structured_quotes(),
            "cost": {"unit_cost": 400.0},
            "quantity": 100,
        })

        table = result.data["comparison_table"]
        # Vendor A: 450*100 + 500 = 45500
        # Vendor B: 480*100 + 0 = 48000
        # Vendor C: 520*100 + 1000 = 53000
        assert table[0]["supplier"] == "Vendor A"
        assert table[0]["rank"] == 1
        assert table[1]["supplier"] == "Vendor B"
        assert table[2]["supplier"] == "Vendor C"

    def test_delta_vs_should_cost(self):
        agent = QuoteComparisonAgent()
        result = agent.execute(_ctx(), {
            "quotes": [{"supplier": {"name": "V1"}, "unit_price": 500.0}],
            "cost": {"unit_cost": 400.0},
        })

        row = result.data["comparison_table"][0]
        assert row["delta_vs_should_cost"] == 100.0
        assert row["delta_pct"] == 25.0

    def test_recommendation_contains_best_supplier(self):
        agent = QuoteComparisonAgent()
        result = agent.execute(_ctx(), {
            "quotes": _structured_quotes(),
            "cost": {"unit_cost": 400.0},
            "quantity": 100,
        })

        assert "Vendor A" in result.data["recommendation"]
        assert result.data["best_supplier"] == "Vendor A"
        assert result.data["best_unit_price"] == 450.0

    def test_no_should_cost_still_works(self):
        agent = QuoteComparisonAgent()
        result = agent.execute(_ctx(), {
            "quotes": _structured_quotes(),
            "quantity": 100,
        })

        assert result.status == "success"
        table = result.data["comparison_table"]
        assert all(row["delta_pct"] == 0 for row in table)


class TestQuoteComparisonAnomalies:
    def test_flags_overpriced(self):
        agent = QuoteComparisonAgent()
        result = agent.execute(_ctx(), {
            "quotes": [{"supplier": {"name": "Expensive Co"}, "unit_price": 600.0}],
            "cost": {"unit_cost": 400.0},
        })

        anomalies = result.data["anomalies"]
        assert len(anomalies) >= 1
        assert anomalies[0]["type"] == "overpriced"
        assert "Expensive Co" in anomalies[0]["supplier"]

    def test_flags_suspicious_low(self):
        agent = QuoteComparisonAgent()
        result = agent.execute(_ctx(), {
            "quotes": [{"supplier": {"name": "Cheap Co"}, "unit_price": 200.0}],
            "cost": {"unit_cost": 400.0},
        })

        anomalies = result.data["anomalies"]
        assert len(anomalies) >= 1
        assert anomalies[0]["type"] == "suspicious"

    def test_no_anomalies_in_normal_range(self):
        agent = QuoteComparisonAgent()
        result = agent.execute(_ctx(), {
            "quotes": [{"supplier": {"name": "Normal"}, "unit_price": 420.0}],
            "cost": {"unit_cost": 400.0},
        })

        assert result.data["anomalies"] == []

    def test_po_history_price_increase_flag(self):
        agent = QuoteComparisonAgent()
        result = agent.execute(_ctx(), {
            "quotes": [{"supplier": {"name": "V1"}, "unit_price": 500.0}],
            "cost": {"unit_cost": 400.0},
            "po_history": [{"unit_price": 350.0}],
        })

        anomalies = result.data["anomalies"]
        price_increase = [a for a in anomalies if a["type"] == "price_increase"]
        assert len(price_increase) >= 1

    def test_po_history_delta_in_rows(self):
        agent = QuoteComparisonAgent()
        result = agent.execute(_ctx(), {
            "quotes": [{"supplier": {"name": "V1"}, "unit_price": 400.0}],
            "cost": {"unit_cost": 400.0},
            "po_history": [{"unit_price": 350.0}],
        })

        row = result.data["comparison_table"][0]
        assert "delta_vs_last_po" in row


class TestQuoteComparisonEdgeCases:
    def test_empty_quotes_returns_error(self):
        agent = QuoteComparisonAgent()
        result = agent.execute(_ctx(), {"quotes": []})

        assert result.status == "error"
        assert "No valid quotes" in result.error

    def test_quote_with_total_but_no_unit_price(self):
        agent = QuoteComparisonAgent()
        result = agent.execute(_ctx(), {
            "quotes": [{"supplier_name": "V1", "total_quoted": 50000.0}],
            "quantity": 100,
        })

        assert result.status == "success"
        row = result.data["comparison_table"][0]
        assert row["unit_price"] == 500.0

    def test_fallback_vendor_name(self):
        agent = QuoteComparisonAgent()
        result = agent.execute(_ctx(), {
            "quotes": [{"unit_price": 100.0}],
        })

        row = result.data["comparison_table"][0]
        assert "Vendor 1" in row["supplier"]

    @patch("agents.quote_comparison_agent.call_llm")
    def test_raw_text_extraction(self, mock_llm):
        mock_llm.return_value = MagicMock(
            content='{"supplier_name": "Extracted Co", "unit_price": 350.0, "total_quoted": 35000, "delivery_weeks": 3, "currency": "INR", "lines": [], "payment_terms": "Net 30", "tooling_charges": 0, "moq": 0, "validity_days": 30}'
        )

        agent = QuoteComparisonAgent()
        result = agent.execute(_ctx(), {
            "quotes": [{"raw_text": "Quote from Extracted Co: Rs 350 per unit..."}],
            "cost": {"unit_cost": 400.0},
        })

        assert result.status == "success"
        assert result.llm_calls == 1

    @patch("agents.quote_comparison_agent.call_llm", side_effect=RuntimeError("LLM down"))
    def test_raw_text_extraction_failure_skips_quote(self, _):
        agent = QuoteComparisonAgent()
        result = agent.execute(_ctx(), {
            "quotes": [{"raw_text": "unparseable text"}],
        })

        # No valid quotes after extraction failure
        assert result.status == "error"

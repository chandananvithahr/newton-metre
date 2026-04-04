"""Tests for negotiation memory — WorkingMemory, EpisodicMemory, SemanticMemory."""
import os
import sys
import pytest
from unittest.mock import patch, MagicMock

from agents.memory import (
    WorkingMemory,
    NegotiationEpisode,
    EpisodicMemory,
    SemanticMemory,
    SupplierPattern,
)


# Ensure api.deps can import without real env vars
_FAKE_ENV = {
    "SUPABASE_URL": "https://fake.supabase.co",
    "SUPABASE_SERVICE_ROLE_KEY": "fake-key",
    "SUPABASE_ANON_KEY": "fake-anon-key",
}


def _mock_supabase_admin():
    """Create a mock that simulates Supabase client chaining."""
    mock_db = MagicMock()
    # Default: empty result
    mock_result = MagicMock()
    mock_result.data = []
    # Make all chained calls return mock objects that end with .execute() -> mock_result
    mock_db.table.return_value.select.return_value.eq.return_value.order.return_value.limit.return_value.execute.return_value = mock_result
    mock_db.table.return_value.select.return_value.eq.return_value.eq.return_value.order.return_value.execute.return_value = mock_result
    mock_db.table.return_value.select.return_value.eq.return_value.order.return_value.limit.return_value.eq.return_value.execute.return_value = mock_result
    mock_db.table.return_value.select.return_value.eq.return_value.eq.return_value.eq.return_value.limit.return_value.execute.return_value = mock_result
    mock_db.table.return_value.insert.return_value.execute.return_value = mock_result
    mock_db.table.return_value.update.return_value.eq.return_value.execute.return_value = mock_result
    return mock_db


class TestWorkingMemoryImmutability:
    def test_frozen(self):
        wm = WorkingMemory(target_price=100, initial_quote=150, current_offer=150)
        with pytest.raises(AttributeError):
            wm.target_price = 200

    def test_default_values(self):
        wm = WorkingMemory(target_price=100, initial_quote=150, current_offer=150)
        assert wm.concession_budget_pct == 5.0
        assert wm.max_rounds == 3
        assert wm.current_round == 1
        assert wm.arguments_used == ()
        assert wm.concessions_made == ()


class TestWorkingMemoryConcessions:
    def test_full_budget_available(self):
        wm = WorkingMemory(target_price=100, initial_quote=150, current_offer=150)
        assert wm.concession_remaining_pct == 5.0

    def test_budget_after_concession(self):
        wm = WorkingMemory(
            target_price=100, initial_quote=150, current_offer=140,
            concessions_made=({"pct": 2.0, "desc": "delivery flexibility"},),
        )
        assert wm.concession_remaining_pct == 3.0

    def test_budget_exhausted(self):
        wm = WorkingMemory(
            target_price=100, initial_quote=150, current_offer=130,
            concession_budget_pct=5.0,
            concessions_made=({"pct": 3.0}, {"pct": 2.5}),
        )
        assert wm.concession_remaining_pct == 0

    def test_rounds_remaining(self):
        wm = WorkingMemory(
            target_price=100, initial_quote=150, current_offer=140,
            max_rounds=3, current_round=2,
        )
        assert wm.rounds_remaining == 1

    def test_no_rounds_remaining(self):
        wm = WorkingMemory(
            target_price=100, initial_quote=150, current_offer=130,
            max_rounds=3, current_round=3,
        )
        assert wm.rounds_remaining == 0


class TestWorkingMemoryWithRound:
    def test_advances_round(self):
        wm = WorkingMemory(target_price=100, initial_quote=150, current_offer=150)
        wm2 = wm.with_round(new_offer=140, argument_used="market_rate")

        assert wm2.current_round == 2
        assert wm2.current_offer == 140
        assert "market_rate" in wm2.arguments_used
        # Original unchanged
        assert wm.current_round == 1
        assert wm.current_offer == 150

    def test_accumulates_arguments(self):
        wm = WorkingMemory(target_price=100, initial_quote=150, current_offer=150)
        wm2 = wm.with_round(140, "arg1")
        wm3 = wm2.with_round(130, "arg2")

        assert wm3.arguments_used == ("arg1", "arg2")
        assert wm3.current_round == 3

    def test_no_argument_used(self):
        wm = WorkingMemory(target_price=100, initial_quote=150, current_offer=150)
        wm2 = wm.with_round(140)
        assert wm2.arguments_used == ()


class TestWorkingMemoryPromptContext:
    def test_contains_key_data(self):
        wm = WorkingMemory(target_price=100, initial_quote=150, current_offer=140)
        ctx = wm.to_prompt_context()

        assert "100.00" in ctx
        assert "140.00" in ctx
        assert "Round: 1/3" in ctx
        assert "NEGOTIATION STATE" in ctx

    def test_gap_percentage(self):
        wm = WorkingMemory(target_price=100, initial_quote=150, current_offer=120)
        ctx = wm.to_prompt_context()
        assert "20.0%" in ctx


class TestNegotiationEpisode:
    def test_frozen(self):
        ep = NegotiationEpisode(
            episode_id="e1", supplier_name="Vendor A", part_family="shaft",
            initial_quote=500, should_cost=400, final_price=430,
            rounds=3, outcome="success",
        )
        with pytest.raises(AttributeError):
            ep.final_price = 450

    def test_defaults(self):
        ep = NegotiationEpisode(
            episode_id="e1", supplier_name="V", part_family="p",
            initial_quote=0, should_cost=0, final_price=0,
            rounds=0, outcome="unknown",
        )
        assert ep.arguments_used == ()
        assert ep.arguments_failed == ()


class TestEpisodicMemoryRecall:
    def test_recall_returns_episodes(self):
        mock_db = _mock_supabase_admin()
        mock_result = MagicMock()
        mock_result.data = [
            {
                "id": "ep1",
                "supplier_id": "sup1",
                "part_family": "shaft",
                "initial_quote": 500,
                "should_cost": 400,
                "final_price": 430,
                "rounds": 3,
                "outcome": "success",
                "arguments_used": [{"argument": "market_rate", "effectiveness": 4}],
                "arguments_failed": [],
            }
        ]
        mock_db.table.return_value.select.return_value.eq.return_value.order.return_value.limit.return_value.execute.return_value = mock_result

        with patch.dict(os.environ, _FAKE_ENV), \
             patch("api.deps.create_client", return_value=mock_db):
            episodes = EpisodicMemory().recall("c1")

        assert len(episodes) == 1
        assert episodes[0].episode_id == "ep1"
        assert episodes[0].final_price == 430.0

    def test_recall_graceful_on_failure(self):
        with patch.dict(os.environ, _FAKE_ENV), \
             patch("api.deps.create_client", side_effect=Exception("DB down")):
            # Clear the lru_cache so our mock takes effect
            from api.deps import get_supabase_admin
            get_supabase_admin.cache_clear()
            episodes = EpisodicMemory().recall("c1")

        assert episodes == []

    def test_save_episode(self):
        mock_db = _mock_supabase_admin()
        mock_result = MagicMock()
        mock_result.data = [{"id": "new-ep-1"}]
        mock_db.table.return_value.insert.return_value.execute.return_value = mock_result

        with patch.dict(os.environ, _FAKE_ENV), \
             patch("api.deps.create_client", return_value=mock_db):
            from api.deps import get_supabase_admin
            get_supabase_admin.cache_clear()
            ep_id = EpisodicMemory().save("c1", {"supplier_id": "s1", "outcome": "success"})

        assert ep_id == "new-ep-1"

    def test_save_graceful_on_failure(self):
        with patch.dict(os.environ, _FAKE_ENV), \
             patch("api.deps.create_client", side_effect=Exception("DB down")):
            from api.deps import get_supabase_admin
            get_supabase_admin.cache_clear()
            ep_id = EpisodicMemory().save("c1", {})

        assert ep_id == ""


class TestEpisodicMemoryPromptContext:
    def test_empty_episodes(self):
        ctx = EpisodicMemory().to_prompt_context([])
        assert "No prior negotiations" in ctx

    def test_formats_episodes(self):
        episodes = [
            NegotiationEpisode(
                episode_id="e1", supplier_name="V", part_family="shaft",
                initial_quote=500, should_cost=400, final_price=430,
                rounds=3, outcome="success",
                arguments_used=({"argument": "should_cost_data", "effectiveness": 4},),
            )
        ]
        ctx = EpisodicMemory().to_prompt_context(episodes)
        assert "PAST NEGOTIATIONS" in ctx
        assert "shaft" in ctx
        assert "500" in ctx
        assert "430" in ctx
        assert "should_cost_data" in ctx

    def test_limits_to_5_episodes(self):
        episodes = [
            NegotiationEpisode(
                episode_id=f"e{i}", supplier_name="V", part_family=f"part{i}",
                initial_quote=100, should_cost=80, final_price=90,
                rounds=2, outcome="success",
            )
            for i in range(10)
        ]
        ctx = EpisodicMemory().to_prompt_context(episodes)
        assert "part4" in ctx
        assert "part5" not in ctx


class TestSupplierPattern:
    def test_frozen(self):
        p = SupplierPattern(
            pattern_type="typical_discount",
            pattern_data={"avg_discount_pct": 12.5},
            evidence_count=5,
            is_preliminary=False,
        )
        with pytest.raises(AttributeError):
            p.evidence_count = 10

    def test_preliminary_flag(self):
        p = SupplierPattern(
            pattern_type="test", pattern_data={},
            evidence_count=2, is_preliminary=True,
        )
        assert p.is_preliminary


class TestSemanticMemoryGetPatterns:
    def test_loads_patterns(self):
        mock_db = _mock_supabase_admin()
        mock_result = MagicMock()
        mock_result.data = [
            {
                "pattern_type": "typical_discount",
                "pattern_data": {"avg_discount_pct": 12.5},
                "evidence_count": 5,
            },
            {
                "pattern_type": "negotiation_rounds",
                "pattern_data": {"avg_rounds": 3},
                "evidence_count": 2,
            },
        ]
        mock_db.table.return_value.select.return_value.eq.return_value.eq.return_value.order.return_value.execute.return_value = mock_result

        with patch.dict(os.environ, _FAKE_ENV), \
             patch("api.deps.create_client", return_value=mock_db):
            from api.deps import get_supabase_admin
            get_supabase_admin.cache_clear()
            patterns = SemanticMemory().get_patterns("c1", "sup1")

        assert len(patterns) == 2
        assert patterns[0].pattern_type == "typical_discount"
        assert patterns[0].evidence_count == 5
        assert not patterns[0].is_preliminary
        assert patterns[1].is_preliminary  # evidence_count < 3

    def test_graceful_on_failure(self):
        with patch.dict(os.environ, _FAKE_ENV), \
             patch("api.deps.create_client", side_effect=Exception("DB down")):
            from api.deps import get_supabase_admin
            get_supabase_admin.cache_clear()
            patterns = SemanticMemory().get_patterns("c1", "sup1")

        assert patterns == []


class TestSemanticMemoryUpdateFromEpisode:
    def test_inserts_new_patterns(self):
        mock_db = _mock_supabase_admin()

        with patch.dict(os.environ, _FAKE_ENV), \
             patch("api.deps.create_client", return_value=mock_db):
            from api.deps import get_supabase_admin
            get_supabase_admin.cache_clear()

            episode = NegotiationEpisode(
                episode_id="e1", supplier_name="V", part_family="shaft",
                initial_quote=500, should_cost=400, final_price=430,
                rounds=3, outcome="success",
            )
            SemanticMemory().update_from_episode("c1", "sup1", episode)

        assert mock_db.table.return_value.insert.called

    def test_graceful_on_failure(self):
        with patch.dict(os.environ, _FAKE_ENV), \
             patch("api.deps.create_client", side_effect=Exception("DB down")):
            from api.deps import get_supabase_admin
            get_supabase_admin.cache_clear()

            episode = NegotiationEpisode(
                episode_id="e1", supplier_name="V", part_family="shaft",
                initial_quote=500, should_cost=400, final_price=430,
                rounds=3, outcome="success",
            )
            # Should not raise
            SemanticMemory().update_from_episode("c1", "sup1", episode)


class TestSemanticMemoryPromptContext:
    def test_empty_patterns(self):
        ctx = SemanticMemory().to_prompt_context([])
        assert "No known patterns" in ctx

    def test_typical_discount_pattern(self):
        patterns = [
            SupplierPattern(
                pattern_type="typical_discount",
                pattern_data={"avg_discount_pct": 12.5},
                evidence_count=5,
                is_preliminary=False,
            )
        ]
        ctx = SemanticMemory().to_prompt_context(patterns)
        assert "SUPPLIER INTELLIGENCE" in ctx
        assert "12.5%" in ctx
        assert "based on 5 negotiations" in ctx

    def test_negotiation_rounds_pattern(self):
        patterns = [
            SupplierPattern(
                pattern_type="negotiation_rounds",
                pattern_data={"avg_rounds": 3},
                evidence_count=2,
                is_preliminary=True,
            )
        ]
        ctx = SemanticMemory().to_prompt_context(patterns)
        assert "3 rounds" in ctx
        assert "preliminary" in ctx

    def test_unknown_pattern_type(self):
        patterns = [
            SupplierPattern(
                pattern_type="custom_pattern",
                pattern_data={"key": "value"},
                evidence_count=1,
                is_preliminary=True,
            )
        ]
        ctx = SemanticMemory().to_prompt_context(patterns)
        assert "custom_pattern" in ctx

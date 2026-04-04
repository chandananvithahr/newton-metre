"""Three-layer negotiation memory system.

- WorkingMemory: in-process state for the current negotiation
- EpisodicMemory: per-negotiation outcomes (Supabase persistence)
- SemanticMemory: supplier patterns extracted across episodes

Each layer implements to_prompt_context() for LLM injection.
"""
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone

logger = logging.getLogger("agents.memory")


# --- Working Memory (in-process, per-negotiation) ---

@dataclass(frozen=True)
class WorkingMemory:
    """Current negotiation state. Held in-process, not persisted."""
    target_price: float
    initial_quote: float
    current_offer: float
    concession_budget_pct: float = 5.0
    max_rounds: int = 3
    current_round: int = 1
    arguments_available: tuple[str, ...] = ()
    arguments_used: tuple[str, ...] = ()
    concessions_made: tuple[dict, ...] = ()

    @property
    def concession_remaining_pct(self) -> float:
        """How much more we can concede (percentage of should-cost)."""
        total_conceded = sum(c.get("pct", 0) for c in self.concessions_made)
        return max(0, self.concession_budget_pct - total_conceded)

    @property
    def rounds_remaining(self) -> int:
        return max(0, self.max_rounds - self.current_round)

    def with_round(self, new_offer: float, argument_used: str | None = None) -> "WorkingMemory":
        """Advance to next round with a new offer."""
        used = list(self.arguments_used)
        if argument_used:
            used.append(argument_used)
        return WorkingMemory(
            target_price=self.target_price,
            initial_quote=self.initial_quote,
            current_offer=new_offer,
            concession_budget_pct=self.concession_budget_pct,
            max_rounds=self.max_rounds,
            current_round=self.current_round + 1,
            arguments_available=self.arguments_available,
            arguments_used=tuple(used),
            concessions_made=self.concessions_made,
        )

    def to_prompt_context(self) -> str:
        return (
            f"NEGOTIATION STATE:\n"
            f"- Target price: Rs {self.target_price:.2f}\n"
            f"- Vendor's current quote: Rs {self.current_offer:.2f}\n"
            f"- Gap: {((self.current_offer - self.target_price) / self.target_price * 100):.1f}%\n"
            f"- Round: {self.current_round}/{self.max_rounds}\n"
            f"- Concession budget remaining: {self.concession_remaining_pct:.1f}%\n"
            f"- Arguments used so far: {', '.join(self.arguments_used) or 'none'}\n"
        )


# --- Episodic Memory (per-negotiation, Supabase) ---

@dataclass(frozen=True)
class NegotiationEpisode:
    """Record of a past negotiation."""
    episode_id: str
    supplier_name: str
    part_family: str
    initial_quote: float
    should_cost: float
    final_price: float
    rounds: int
    outcome: str
    arguments_used: tuple[dict, ...] = ()
    arguments_failed: tuple[dict, ...] = ()


class EpisodicMemory:
    """Recall past negotiations from Supabase."""

    def recall(
        self,
        company_id: str,
        supplier_id: str | None = None,
        part_family: str | None = None,
        limit: int = 10,
    ) -> list[NegotiationEpisode]:
        """Load past negotiation episodes with optional filters."""
        try:
            from api.deps import get_supabase_admin
            db = get_supabase_admin()
            query = (
                db.table("negotiation_episodes")
                .select("*")
                .eq("company_id", company_id)
                .order("created_at", desc=True)
                .limit(limit)
            )
            if supplier_id:
                query = query.eq("supplier_id", supplier_id)
            if part_family:
                query = query.eq("part_family", part_family)

            result = query.execute()
            return [self._row_to_episode(row) for row in (result.data or [])]
        except Exception as exc:
            logger.warning("Failed to recall episodes: %s", exc)
            return []

    def save(self, company_id: str, episode_data: dict) -> str:
        """Save a negotiation episode."""
        try:
            from api.deps import get_supabase_admin
            db = get_supabase_admin()
            episode_data["company_id"] = company_id
            result = db.table("negotiation_episodes").insert(episode_data).execute()
            return result.data[0]["id"] if result.data else ""
        except Exception as exc:
            logger.warning("Failed to save episode: %s", exc)
            return ""

    def _row_to_episode(self, row: dict) -> NegotiationEpisode:
        return NegotiationEpisode(
            episode_id=row["id"],
            supplier_name=row.get("supplier_id", ""),
            part_family=row.get("part_family", ""),
            initial_quote=float(row.get("initial_quote", 0)),
            should_cost=float(row.get("should_cost", 0)),
            final_price=float(row.get("final_price", 0)),
            rounds=row.get("rounds", 0),
            outcome=row.get("outcome", "unknown"),
            arguments_used=tuple(row.get("arguments_used", [])),
            arguments_failed=tuple(row.get("arguments_failed", [])),
        )

    def to_prompt_context(self, episodes: list[NegotiationEpisode]) -> str:
        if not episodes:
            return "No prior negotiations with this supplier on record."
        lines = ["PAST NEGOTIATIONS WITH THIS SUPPLIER:"]
        for ep in episodes[:5]:
            saving_pct = (
                (ep.initial_quote - ep.final_price) / ep.initial_quote * 100
                if ep.initial_quote > 0 else 0
            )
            lines.append(
                f"- {ep.part_family}: quoted Rs {ep.initial_quote:.0f}, "
                f"settled Rs {ep.final_price:.0f} ({saving_pct:.1f}% reduction) "
                f"in {ep.rounds} rounds. Outcome: {ep.outcome}"
            )
            if ep.arguments_used:
                effective = [a.get("argument", "") for a in ep.arguments_used
                             if a.get("effectiveness", 0) >= 3]
                if effective:
                    lines.append(f"  Effective arguments: {', '.join(effective)}")
        return "\n".join(lines)


# --- Semantic Memory (supplier patterns, Supabase) ---

@dataclass(frozen=True)
class SupplierPattern:
    """A learned pattern about a supplier's behavior."""
    pattern_type: str
    pattern_data: dict
    evidence_count: int
    is_preliminary: bool  # True if evidence_count < 3


class SemanticMemory:
    """Supplier intelligence patterns — the compounding moat."""

    def get_patterns(
        self,
        company_id: str,
        supplier_id: str,
    ) -> list[SupplierPattern]:
        """Load supplier patterns."""
        try:
            from api.deps import get_supabase_admin
            db = get_supabase_admin()
            result = (
                db.table("supplier_intelligence")
                .select("*")
                .eq("company_id", company_id)
                .eq("supplier_id", supplier_id)
                .order("evidence_count", desc=True)
                .execute()
            )
            return [
                SupplierPattern(
                    pattern_type=row["pattern_type"],
                    pattern_data=row["pattern_data"],
                    evidence_count=row["evidence_count"],
                    is_preliminary=row["evidence_count"] < 3,
                )
                for row in (result.data or [])
            ]
        except Exception as exc:
            logger.warning("Failed to load patterns: %s", exc)
            return []

    def update_from_episode(
        self,
        company_id: str,
        supplier_id: str,
        episode: NegotiationEpisode,
    ) -> None:
        """Extract and update patterns after a completed negotiation."""
        try:
            from api.deps import get_supabase_admin
            db = get_supabase_admin()

            # Pattern: typical discount this supplier gives
            if episode.initial_quote > 0 and episode.final_price > 0:
                discount_pct = (
                    (episode.initial_quote - episode.final_price) / episode.initial_quote * 100
                )
                self._upsert_pattern(
                    db, company_id, supplier_id,
                    "typical_discount",
                    {"avg_discount_pct": discount_pct, "last_part": episode.part_family},
                )

            # Pattern: typical rounds to settle
            if episode.rounds > 0:
                self._upsert_pattern(
                    db, company_id, supplier_id,
                    "negotiation_rounds",
                    {"avg_rounds": episode.rounds, "last_part": episode.part_family},
                )

        except Exception as exc:
            logger.warning("Failed to update patterns: %s", exc)

    def _upsert_pattern(
        self, db, company_id: str, supplier_id: str,
        pattern_type: str, pattern_data: dict,
    ) -> None:
        """Insert or update a pattern, incrementing evidence count."""
        existing = (
            db.table("supplier_intelligence")
            .select("id, evidence_count")
            .eq("company_id", company_id)
            .eq("supplier_id", supplier_id)
            .eq("pattern_type", pattern_type)
            .limit(1)
            .execute()
        )

        if existing.data:
            row = existing.data[0]
            db.table("supplier_intelligence").update({
                "pattern_data": pattern_data,
                "evidence_count": row["evidence_count"] + 1,
                "last_updated": datetime.now(timezone.utc).isoformat(),
            }).eq("id", row["id"]).execute()
        else:
            db.table("supplier_intelligence").insert({
                "company_id": company_id,
                "supplier_id": supplier_id,
                "pattern_type": pattern_type,
                "pattern_data": pattern_data,
                "evidence_count": 1,
            }).execute()

    def to_prompt_context(self, patterns: list[SupplierPattern]) -> str:
        if not patterns:
            return "No known patterns for this supplier yet."
        lines = ["SUPPLIER INTELLIGENCE:"]
        for p in patterns:
            reliability = "preliminary" if p.is_preliminary else f"based on {p.evidence_count} negotiations"
            if p.pattern_type == "typical_discount":
                lines.append(
                    f"- This supplier typically gives {p.pattern_data.get('avg_discount_pct', 0):.1f}% "
                    f"discount from initial quote ({reliability})"
                )
            elif p.pattern_type == "negotiation_rounds":
                lines.append(
                    f"- Typically settles in {p.pattern_data.get('avg_rounds', 0)} rounds ({reliability})"
                )
            else:
                lines.append(f"- {p.pattern_type}: {p.pattern_data} ({reliability})")
        return "\n".join(lines)

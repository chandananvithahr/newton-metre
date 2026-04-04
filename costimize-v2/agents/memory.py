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


# --- Graph Queries (cross-supplier relational intelligence) ---

class SupplierGraphQuery:
    """Relational queries across suppliers, episodes, and intelligence patterns.

    Answers questions like:
    - "Which suppliers give best prices for SS304 turned parts?"
    - "Which vendors improved terms after round 2?"
    - "What's our average cost for turned aluminum parts?"
    - "Who has the highest discount rate on machined parts?"
    """

    def best_suppliers_for(
        self,
        company_id: str,
        part_family: str | None = None,
        max_price: float | None = None,
        limit: int = 5,
    ) -> list[dict]:
        """Return suppliers ranked by best final price for a given part family.

        Returns list of dicts: {supplier_id, supplier_name, avg_final_price,
                                avg_discount_pct, episode_count, avg_rounds}
        """
        try:
            from api.deps import get_supabase_admin
            db = get_supabase_admin()

            query = (
                db.table("negotiation_episodes")
                .select("supplier_id, final_price, initial_quote, rounds, part_family, suppliers(name)")
                .eq("company_id", company_id)
                .eq("outcome", "accepted")
                .not_.is_("final_price", "null")
            )
            if part_family:
                query = query.ilike("part_family", f"%{part_family}%")
            if max_price:
                query = query.lte("final_price", max_price)

            result = query.limit(200).execute()
            rows = result.data or []

            # Aggregate by supplier
            agg: dict[str, dict] = {}
            for row in rows:
                sid = row["supplier_id"]
                if not sid:
                    continue
                if sid not in agg:
                    agg[sid] = {
                        "supplier_id": sid,
                        "supplier_name": row.get("suppliers", {}).get("name", sid) if row.get("suppliers") else sid,
                        "prices": [],
                        "discounts": [],
                        "rounds": [],
                    }
                agg[sid]["prices"].append(float(row["final_price"] or 0))
                if row.get("initial_quote") and row["initial_quote"] > 0:
                    disc = (float(row["initial_quote"]) - float(row["final_price"] or 0)) / float(row["initial_quote"]) * 100
                    agg[sid]["discounts"].append(disc)
                agg[sid]["rounds"].append(row.get("rounds", 0))

            results = []
            for sid, data in agg.items():
                prices = data["prices"]
                results.append({
                    "supplier_id": sid,
                    "supplier_name": data["supplier_name"],
                    "avg_final_price": round(sum(prices) / len(prices), 2),
                    "avg_discount_pct": round(sum(data["discounts"]) / len(data["discounts"]), 1) if data["discounts"] else 0.0,
                    "episode_count": len(prices),
                    "avg_rounds": round(sum(data["rounds"]) / len(data["rounds"]), 1),
                })

            # Sort by avg final price ascending (cheapest first)
            results.sort(key=lambda x: x["avg_final_price"])
            return results[:limit]

        except Exception as exc:
            logger.warning("Graph query failed: %s", exc)
            return []

    def suppliers_who_improved(
        self,
        company_id: str,
        min_improvement_rounds: int = 2,
        limit: int = 5,
    ) -> list[dict]:
        """Return suppliers who consistently improve terms after multiple rounds.

        Returns list of dicts: {supplier_id, supplier_name, avg_discount_pct,
                                 avg_rounds, episode_count}
        Filters to suppliers whose avg_rounds >= min_improvement_rounds.
        """
        try:
            from api.deps import get_supabase_admin
            db = get_supabase_admin()

            result = (
                db.table("negotiation_episodes")
                .select("supplier_id, final_price, initial_quote, rounds, suppliers(name)")
                .eq("company_id", company_id)
                .eq("outcome", "accepted")
                .gte("rounds", min_improvement_rounds)
                .not_.is_("final_price", "null")
                .limit(200)
                .execute()
            )
            rows = result.data or []

            agg: dict[str, dict] = {}
            for row in rows:
                sid = row["supplier_id"]
                if not sid:
                    continue
                if sid not in agg:
                    agg[sid] = {
                        "supplier_id": sid,
                        "supplier_name": row.get("suppliers", {}).get("name", sid) if row.get("suppliers") else sid,
                        "discounts": [],
                        "rounds": [],
                    }
                if row.get("initial_quote") and float(row["initial_quote"]) > 0:
                    disc = (float(row["initial_quote"]) - float(row["final_price"] or 0)) / float(row["initial_quote"]) * 100
                    agg[sid]["discounts"].append(disc)
                agg[sid]["rounds"].append(row.get("rounds", 1))

            results = []
            for sid, data in agg.items():
                if not data["discounts"]:
                    continue
                results.append({
                    "supplier_id": sid,
                    "supplier_name": data["supplier_name"],
                    "avg_discount_pct": round(sum(data["discounts"]) / len(data["discounts"]), 1),
                    "avg_rounds": round(sum(data["rounds"]) / len(data["rounds"]), 1),
                    "episode_count": len(data["discounts"]),
                })

            results.sort(key=lambda x: x["avg_discount_pct"], reverse=True)
            return results[:limit]

        except Exception as exc:
            logger.warning("Graph query (improved) failed: %s", exc)
            return []

    def portfolio_summary(self, company_id: str) -> dict:
        """Aggregate statistics across all negotiations.

        Returns: {total_episodes, total_savings_inr, avg_discount_pct,
                  avg_rounds, top_part_families, accepted_rate}
        """
        try:
            from api.deps import get_supabase_admin
            db = get_supabase_admin()

            result = (
                db.table("negotiation_episodes")
                .select("final_price, initial_quote, rounds, outcome, part_family")
                .eq("company_id", company_id)
                .limit(500)
                .execute()
            )
            rows = result.data or []
            if not rows:
                return {}

            total = len(rows)
            accepted = [r for r in rows if r.get("outcome") == "accepted"]
            savings = []
            rounds_list = []
            family_counts: dict[str, int] = {}

            for r in accepted:
                if r.get("initial_quote") and r.get("final_price"):
                    savings.append(float(r["initial_quote"]) - float(r["final_price"]))
                rounds_list.append(r.get("rounds", 0))
                fam = r.get("part_family", "unknown")
                family_counts[fam] = family_counts.get(fam, 0) + 1

            top_families = sorted(family_counts.items(), key=lambda x: x[1], reverse=True)[:3]

            return {
                "total_episodes": total,
                "accepted_rate": round(len(accepted) / total * 100, 1) if total else 0,
                "total_savings_inr": round(sum(savings), 2),
                "avg_savings_per_deal_inr": round(sum(savings) / len(savings), 2) if savings else 0,
                "avg_rounds": round(sum(rounds_list) / len(rounds_list), 1) if rounds_list else 0,
                "top_part_families": [f for f, _ in top_families],
            }

        except Exception as exc:
            logger.warning("Portfolio summary failed: %s", exc)
            return {}

    def to_prompt_context(
        self,
        company_id: str,
        part_family: str | None = None,
        max_price: float | None = None,
    ) -> str:
        """Generate context string for chat injection about supplier graph intelligence."""
        lines = []

        best = self.best_suppliers_for(company_id, part_family=part_family, max_price=max_price)
        if best:
            lines.append("=== SUPPLIER INTELLIGENCE (from negotiation history) ===")
            scope = f" for {part_family}" if part_family else ""
            lines.append(f"Best suppliers{scope} by negotiated price:")
            for s in best:
                lines.append(
                    f"  - {s['supplier_name']}: avg ₹{s['avg_final_price']:.0f} "
                    f"({s['avg_discount_pct']:.1f}% avg discount, "
                    f"{s['episode_count']} deals, {s['avg_rounds']} avg rounds)"
                )

        improved = self.suppliers_who_improved(company_id)
        if improved:
            if not lines:
                lines.append("=== SUPPLIER INTELLIGENCE (from negotiation history) ===")
            lines.append("Suppliers who respond well to multi-round negotiation:")
            for s in improved[:3]:
                lines.append(
                    f"  - {s['supplier_name']}: {s['avg_discount_pct']:.1f}% avg discount "
                    f"over {s['avg_rounds']:.1f} rounds ({s['episode_count']} deals)"
                )

        summary = self.portfolio_summary(company_id)
        if summary:
            if not lines:
                lines.append("=== SUPPLIER INTELLIGENCE (from negotiation history) ===")
            lines.append(
                f"Portfolio: {summary['total_episodes']} negotiations, "
                f"₹{summary['total_savings_inr']:.0f} total savings, "
                f"{summary['accepted_rate']}% acceptance rate"
            )

        return "\n".join(lines) if lines else ""

"""QuoteComparisonAgent — normalizes vendor quotes and benchmarks against should-cost.

Accepts raw quote data (or pre-extracted), normalizes to common format,
and compares line-by-line against should-cost + PO history. Flags anomalies
and ranks vendors.
"""
import logging
import time

from agents.llm import call_llm, parse_json_response
from agents.types import AgentResult, WorkflowContext

logger = logging.getLogger("agents.quote_comparison")

QUOTE_EXTRACTION_PROMPT = """Extract structured pricing from this vendor quote text.

Quote text:
{quote_text}

Return JSON:
{{
  "supplier_name": "vendor name",
  "lines": [
    {{
      "description": "line item description",
      "unit_price": 0.0,
      "quantity": 0,
      "total": 0.0
    }}
  ],
  "total_quoted": 0.0,
  "currency": "INR",
  "delivery_weeks": 0,
  "payment_terms": "payment terms text",
  "tooling_charges": 0.0,
  "moq": 0,
  "validity_days": 30
}}

Return ONLY JSON."""


class QuoteComparisonAgent:
    """Normalizes vendor quotes and benchmarks against should-cost."""

    @property
    def name(self) -> str:
        return "quote_comparison"

    def validate_inputs(self, inputs: dict) -> tuple[bool, str]:
        has_quotes = "quotes" in inputs
        if not has_quotes:
            return False, "Need 'quotes' — list of vendor quote dicts"
        return True, ""

    def execute(self, context: WorkflowContext, inputs: dict) -> AgentResult:
        start = time.perf_counter()
        llm_calls = 0

        quotes = inputs.get("quotes", [])
        should_cost = inputs.get("cost", {}).get("unit_cost", 0)
        po_history = inputs.get("po_history", [])
        quantity = inputs.get("quantity", context.inputs.get("quantity", 1))

        # Normalize each quote
        normalized_quotes = []
        for quote in quotes:
            if "unit_price" in quote:
                # Already structured
                normalized_quotes.append(quote)
            elif "raw_text" in quote:
                # Extract via LLM
                extracted = self._extract_quote(quote["raw_text"])
                llm_calls += 1
                if extracted:
                    extracted["supplier"] = quote.get("supplier", {})
                    normalized_quotes.append(extracted)
            else:
                normalized_quotes.append(quote)

        if not normalized_quotes:
            return AgentResult(
                agent_name=self.name,
                status="error",
                error="No valid quotes to compare",
                llm_calls=llm_calls,
            )

        # Compare against should-cost
        comparison = self._compare(normalized_quotes, should_cost, quantity, po_history)

        elapsed = (time.perf_counter() - start) * 1000
        return AgentResult(
            agent_name=self.name,
            status="success",
            data=comparison,
            duration_ms=elapsed,
            llm_calls=llm_calls,
        )

    def _extract_quote(self, raw_text: str) -> dict | None:
        """Extract structured data from raw quote text via LLM."""
        try:
            response = call_llm(
                messages=[
                    {"role": "system", "content": "You are a procurement data extractor."},
                    {"role": "user", "content": QUOTE_EXTRACTION_PROMPT.format(quote_text=raw_text)},
                ],
                json_mode=True,
            )
            return parse_json_response(response.content)
        except Exception as exc:
            logger.warning("Quote extraction failed: %s", exc)
            return None

    def _compare(
        self,
        quotes: list[dict],
        should_cost: float,
        quantity: int,
        po_history: list[dict],
    ) -> dict:
        """Compare normalized quotes against should-cost and history."""
        comparison_rows = []
        anomalies = []

        for i, quote in enumerate(quotes):
            unit_price = quote.get("unit_price") or quote.get("total_quoted", 0) / max(quantity, 1)
            supplier_name = (
                quote.get("supplier", {}).get("name")
                or quote.get("supplier_name", f"Vendor {i + 1}")
            )
            delivery = quote.get("delivery_weeks", 0)
            tooling = quote.get("tooling_charges", 0)
            total_cost = unit_price * quantity + tooling

            # vs should-cost
            delta_vs_should_cost = 0
            delta_pct = 0
            if should_cost > 0:
                delta_vs_should_cost = unit_price - should_cost
                delta_pct = (delta_vs_should_cost / should_cost) * 100

            row = {
                "supplier": supplier_name,
                "unit_price": unit_price,
                "total_cost": total_cost,
                "delivery_weeks": delivery,
                "tooling": tooling,
                "payment_terms": quote.get("payment_terms", ""),
                "delta_vs_should_cost": round(delta_vs_should_cost, 2),
                "delta_pct": round(delta_pct, 1),
            }
            comparison_rows.append(row)

            # Flag anomalies
            if delta_pct > 20:
                anomalies.append({
                    "supplier": supplier_name,
                    "type": "overpriced",
                    "detail": f"Unit price Rs {unit_price:.2f} is {delta_pct:.0f}% above should-cost",
                })
            elif delta_pct < -20:
                anomalies.append({
                    "supplier": supplier_name,
                    "type": "suspicious",
                    "detail": f"Unit price Rs {unit_price:.2f} is {abs(delta_pct):.0f}% below should-cost — verify quality",
                })

        # vs PO history
        if po_history:
            last_po_price = po_history[0].get("unit_price", 0) if po_history else 0
            if last_po_price > 0:
                for row in comparison_rows:
                    po_delta = (row["unit_price"] - last_po_price) / last_po_price * 100
                    row["delta_vs_last_po"] = round(po_delta, 1)
                    if po_delta > 15:
                        anomalies.append({
                            "supplier": row["supplier"],
                            "type": "price_increase",
                            "detail": f"Rs {row['unit_price']:.2f} is {po_delta:.0f}% above last PO (Rs {last_po_price:.2f})",
                        })

        # Rank by total value (lower is better)
        ranked = sorted(comparison_rows, key=lambda r: r["total_cost"])
        for i, row in enumerate(ranked):
            row["rank"] = i + 1

        # Recommendation
        best = ranked[0] if ranked else None
        recommendation = ""
        if best:
            recommendation = (
                f"Recommend {best['supplier']} at Rs {best['unit_price']:.2f}/unit "
                f"(total Rs {best['total_cost']:.2f} for {quantity} units)"
            )
            if should_cost > 0:
                saving = (should_cost - best['unit_price']) / should_cost * 100
                if saving > 0:
                    recommendation += f" — {saving:.1f}% below should-cost"

        return {
            "comparison_table": ranked,
            "anomalies": anomalies,
            "recommendation": recommendation,
            "should_cost_ref": should_cost,
            "quote_count": len(quotes),
            "best_supplier": best["supplier"] if best else None,
            "best_unit_price": best["unit_price"] if best else None,
        }

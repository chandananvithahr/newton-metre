"""MPN (Manufacturer Part Number) lookup — price intelligence for off-the-shelf parts.

70% of procurement spend is MPN-based items (connectors, fasteners, bearings, electronics).
This endpoint provides:
  - AI-powered part description + market price estimate (Gemini)
  - Live price scraping from DigiKey / Mouser (best-effort, non-blocking)
  - Negotiation intelligence: how much room exists vs market rate
"""
import json
import logging

from fastapi import APIRouter, Depends, HTTPException, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from api.deps import get_current_user_id
from api.cost_tracker import check_budget, check_user_budget, log_usage

logger = logging.getLogger(__name__)

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


def _ai_lookup(mpn: str, quantity: int) -> dict:
    """Use Gemini to look up MPN description, specs, and market price estimate."""
    try:
        from config import GEMINI_API_KEY
        if not GEMINI_API_KEY:
            return {}

        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"""You are a procurement expert for Indian manufacturing companies.

Look up this manufacturer part number: {mpn}
Quantity needed: {quantity} units

Respond ONLY with a JSON object (no markdown, no explanation):
{{
  "description": "brief technical description of this part",
  "category": "one of: connector, fastener, bearing, capacitor, resistor, IC, sensor, relay, switch, cable, motor, pneumatic, hydraulic, other",
  "key_specs": ["spec1", "spec2", "spec3"],
  "typical_suppliers_india": ["supplier1", "supplier2", "supplier3"],
  "unit_price_inr_estimate": <number, typical unit price in Indian Rupees for qty {quantity}>,
  "unit_price_inr_low": <number, low end of price range>,
  "unit_price_inr_high": <number, high end of price range>,
  "negotiation_headroom_pct": <number, typical discount achievable in %, e.g. 8>,
  "lead_time_weeks": <number, typical lead time>,
  "notes": "any important procurement notes"
}}

If you don't recognize this exact MPN, estimate based on the part number format and category."""

        response = model.generate_content(
            prompt,
            generation_config={"max_output_tokens": 500, "temperature": 0.1},
        )
        text = response.text.strip()
        # Strip markdown fences if present
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        return json.loads(text.strip())
    except Exception as e:
        logger.warning("AI MPN lookup failed for %s: %s", mpn, e)
        return {}


def _scraper_lookup(mpn: str, quantity: int) -> dict:
    """Try live price scraping. Returns empty dict on failure."""
    try:
        from scrapers.component_scraper import get_component_price
        result = get_component_price(mpn, quantity)
        if result and result.get("source") != "not_found":
            return result
        return {}
    except Exception as e:
        logger.warning("Scraper lookup failed for %s: %s", mpn, e)
        return {}


@router.get("/mpn/lookup")
@limiter.limit("20/minute")
async def lookup_mpn(
    request: Request,
    mpn: str,
    qty: int = 1,
    user_id: str = Depends(get_current_user_id),
):
    if not mpn or len(mpn.strip()) < 2:
        raise HTTPException(status_code=400, detail="MPN must be at least 2 characters.")
    if qty < 1:
        qty = 1
    if qty > 100000:
        qty = 100000

    if not check_budget():
        raise HTTPException(status_code=429, detail="Service temporarily at capacity.")
    if not check_user_budget(user_id):
        raise HTTPException(
            status_code=429,
            detail="You've used your $0.50 credit for this period. Credits refresh every 48 hours.",
        )

    mpn = mpn.strip().upper()

    # AI lookup is primary — reliable description + price estimate
    ai_data = _ai_lookup(mpn, qty)

    # Scraper is best-effort — live price if available
    scraper_data = _scraper_lookup(mpn, qty)

    if not ai_data and not scraper_data:
        raise HTTPException(
            status_code=404,
            detail=f"Could not find pricing data for {mpn}. Check the part number and try again.",
        )

    # Build supplier options list
    supplier_options = []

    # Add scraped live price if available
    if scraper_data and scraper_data.get("unit_price", 0) > 0:
        raw_price = scraper_data["unit_price"]
        currency = scraper_data.get("currency", "USD")
        # Convert USD to INR if needed (approx rate)
        price_inr = raw_price * 83.5 if currency == "USD" else raw_price
        supplier_options.append({
            "name": scraper_data.get("source", "Online"),
            "unit_price_inr": round(price_inr, 2),
            "in_stock": scraper_data.get("in_stock", True),
            "source": "live",
        })

    # Add typical Indian suppliers from AI
    if ai_data:
        typical_suppliers = ai_data.get("typical_suppliers_india", [])
        ai_price = ai_data.get("unit_price_inr_estimate", 0)
        for i, supplier in enumerate(typical_suppliers[:3]):
            # Vary price slightly per supplier (±5%)
            variation = 1.0 + (i - 1) * 0.05
            supplier_options.append({
                "name": supplier,
                "unit_price_inr": round(ai_price * variation, 2) if ai_price else None,
                "in_stock": True,
                "source": "estimate",
            })

    log_usage(user_id, "mpn_lookup", 0.003, {"mpn": mpn, "qty": qty})

    return {
        "mpn": mpn,
        "quantity": qty,
        "description": ai_data.get("description", f"Part {mpn}"),
        "category": ai_data.get("category", "other"),
        "key_specs": ai_data.get("key_specs", []),
        "unit_price_inr": ai_data.get("unit_price_inr_estimate"),
        "unit_price_inr_low": ai_data.get("unit_price_inr_low"),
        "unit_price_inr_high": ai_data.get("unit_price_inr_high"),
        "order_cost_inr": round(
            (ai_data.get("unit_price_inr_estimate") or 0) * qty, 2
        ) or None,
        "negotiation_headroom_pct": ai_data.get("negotiation_headroom_pct", 8),
        "lead_time_weeks": ai_data.get("lead_time_weeks"),
        "notes": ai_data.get("notes", ""),
        "supplier_options": supplier_options,
    }

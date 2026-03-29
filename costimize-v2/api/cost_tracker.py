"""Daily API cost tracking with $20/day hard cap."""
from datetime import date

from api.deps import get_supabase_admin

DAILY_BUDGET_USD = 20.0
ALERT_THRESHOLD_USD = 15.0


def get_daily_cost() -> float:
    """Get total API cost for today in USD."""
    sb = get_supabase_admin()
    today = date.today().isoformat()
    result = (
        sb.table("usage_log")
        .select("api_cost_usd")
        .gte("created_at", f"{today}T00:00:00Z")
        .execute()
    )
    return sum(row["api_cost_usd"] for row in result.data) if result.data else 0.0


def check_budget() -> bool:
    """Returns True if under budget, False if over."""
    return get_daily_cost() < DAILY_BUDGET_USD


def log_usage(
    user_id: str,
    action: str,
    api_cost_usd: float,
    details: dict | None = None,
) -> None:
    """Log an API usage event."""
    sb = get_supabase_admin()
    sb.table("usage_log").insert(
        {
            "user_id": user_id,
            "action": action,
            "api_cost_usd": api_cost_usd,
            "details": details or {},
        }
    ).execute()

"""API cost tracking — global $2/day cap + per-user $0.50/48-hour cap."""
from datetime import date, datetime, timezone, timedelta

from api.deps import get_supabase_admin

DAILY_BUDGET_USD = 2.0           # global hard cap (~$20 per 10 days for 300 users)
USER_BUDGET_USD = 0.50           # per user per 48 hours
USER_BUDGET_WINDOW_HOURS = 48


def get_daily_cost() -> float:
    """Get total API cost for today in USD (global)."""
    sb = get_supabase_admin()
    today = date.today().isoformat()
    result = (
        sb.table("usage_log")
        .select("api_cost_usd")
        .gte("created_at", f"{today}T00:00:00Z")
        .execute()
    )
    return sum(row["api_cost_usd"] for row in result.data) if result.data else 0.0


def get_user_cost_48h(user_id: str) -> float:
    """Get total API cost for a user in the last 48 hours."""
    sb = get_supabase_admin()
    since = (datetime.now(timezone.utc) - timedelta(hours=USER_BUDGET_WINDOW_HOURS)).isoformat()
    result = (
        sb.table("usage_log")
        .select("api_cost_usd")
        .eq("user_id", user_id)
        .gte("created_at", since)
        .execute()
    )
    return sum(row["api_cost_usd"] for row in result.data) if result.data else 0.0


def check_budget() -> bool:
    """Returns True if under global daily budget, False if over."""
    return get_daily_cost() < DAILY_BUDGET_USD


def check_user_budget(user_id: str) -> bool:
    """Returns True if user is under their $0.50/48h quota, False if over."""
    return get_user_cost_48h(user_id) < USER_BUDGET_USD


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

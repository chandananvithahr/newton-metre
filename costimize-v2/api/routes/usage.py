"""GET /api/usage -- user stats. GET /api/admin/usage -- daily cost tracking."""
import os
from datetime import date

from fastapi import APIRouter, Depends, HTTPException

from api.deps import get_current_user_id, get_supabase_admin
from api.schemas import UsageResponse, AdminUsageResponse

router = APIRouter()

ADMIN_SECRET = os.getenv("ADMIN_SECRET", "")


@router.get("/usage", response_model=UsageResponse)
async def get_user_usage(
    user_id: str = Depends(get_current_user_id),
):
    sb = get_supabase_admin()

    profile = (
        sb.table("profiles")
        .select("created_at")
        .eq("id", user_id)
        .single()
        .execute()
    )

    estimates = (
        sb.table("estimates")
        .select("id", count="exact")
        .eq("user_id", user_id)
        .execute()
    )

    similarity = (
        sb.table("usage_log")
        .select("id", count="exact")
        .eq("user_id", user_id)
        .in_("action", ["similarity_embed", "similarity_search"])
        .execute()
    )

    return UsageResponse(
        total_estimates=estimates.count or 0,
        total_similarity=similarity.count or 0,
        joined=profile.data["created_at"] if profile.data else "",
    )


@router.get("/admin/usage", response_model=AdminUsageResponse)
async def get_admin_usage(secret: str = ""):
    if not ADMIN_SECRET or secret != ADMIN_SECRET:
        raise HTTPException(status_code=403, detail="Forbidden")

    sb = get_supabase_admin()
    today = date.today().isoformat()

    cost_result = (
        sb.table("usage_log")
        .select("api_cost_usd")
        .gte("created_at", f"{today}T00:00:00Z")
        .execute()
    )
    today_cost = sum(r["api_cost_usd"] for r in (cost_result.data or []))

    est_result = (
        sb.table("usage_log")
        .select("id", count="exact")
        .eq("action", "estimate")
        .gte("created_at", f"{today}T00:00:00Z")
        .execute()
    )

    signup_result = (
        sb.table("profiles")
        .select("id", count="exact")
        .gte("created_at", f"{today}T00:00:00Z")
        .execute()
    )

    return AdminUsageResponse(
        today_cost_usd=today_cost,
        estimates_today=est_result.count or 0,
        signups_today=signup_result.count or 0,
    )

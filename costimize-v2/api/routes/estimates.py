"""GET /api/estimates -- user's estimate history."""
from fastapi import APIRouter, Depends, HTTPException

from api.deps import get_current_user_id, get_supabase_admin
from api.schemas import EstimateHistoryItem

router = APIRouter()


@router.get("/estimates", response_model=list[EstimateHistoryItem])
async def list_estimates(
    user_id: str = Depends(get_current_user_id),
):
    sb = get_supabase_admin()
    result = (
        sb.table("estimates")
        .select("id, part_type, total_cost, confidence_tier, currency, created_at")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .limit(50)
        .execute()
    )

    return [
        EstimateHistoryItem(
            id=str(row["id"]),
            part_type=row["part_type"],
            total_cost=float(row["total_cost"]),
            confidence_tier=row.get("confidence_tier"),
            currency=row["currency"],
            created_at=row["created_at"],
        )
        for row in (result.data or [])
    ]


@router.get("/estimates/{estimate_id}")
async def get_estimate(
    estimate_id: str,
    user_id: str = Depends(get_current_user_id),
):
    sb = get_supabase_admin()
    result = (
        sb.table("estimates")
        .select("*")
        .eq("id", estimate_id)
        .eq("user_id", user_id)
        .single()
        .execute()
    )

    if not result.data:
        raise HTTPException(status_code=404, detail="Estimate not found")

    return result.data

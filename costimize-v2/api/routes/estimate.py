"""POST /api/estimate -- run physics engine + validation, return cost breakdown."""
from fastapi import APIRouter, Depends, HTTPException

from api.deps import get_current_user_id, get_supabase_admin
from api.cost_tracker import check_budget, log_usage
from api.schemas import EstimateRequest, EstimateResponse

router = APIRouter()


@router.post("/estimate", response_model=EstimateResponse)
async def create_estimate(
    body: EstimateRequest,
    user_id: str = Depends(get_current_user_id),
) -> EstimateResponse:
    if not check_budget():
        raise HTTPException(
            status_code=429,
            detail="Service temporarily at capacity. Please try again tomorrow.",
        )

    extracted = body.extracted_data
    dims = extracted.get("dimensions", {})
    material = extracted.get("material", "Mild Steel")
    processes = extracted.get("suggested_processes", ["turning"])
    has_tight = extracted.get("tolerances", {}).get("has_tight_tolerances", False)

    try:
        from engines.validation.orchestrator import orchestrate

        result = orchestrate(
            image_bytes=None,
            dimensions=dims,
            material_name=material,
            selected_processes=processes,
            quantity=body.quantity,
            has_tight_tolerances=has_tight,
        )
    except Exception:
        raise HTTPException(
            status_code=500, detail="Cost calculation failed. Please verify the extracted data.",
        )

    breakdown = result.physics_result
    confidence = result.confidence_tier.value if result.confidence_tier else None

    process_lines = [
        {
            "process_id": pl.process_id,
            "process_name": pl.process_name,
            "time_min": pl.time_min,
            "machine_cost": pl.machine_cost,
            "setup_cost_per_unit": pl.setup_cost_per_unit,
            "tooling_cost": pl.tooling_cost,
            "labour_cost": pl.labour_cost,
            "power_cost": pl.power_cost,
        }
        for pl in breakdown.process_lines
    ]

    # Persist to Supabase
    sb = get_supabase_admin()
    sb.table("estimates").insert(
        {
            "user_id": user_id,
            "part_type": "mechanical",
            "extracted_data": extracted,
            "cost_breakdown": {
                "material_name": breakdown.material_name,
                "material_cost": breakdown.material_cost,
                "process_lines": process_lines,
                "total_machining_cost": breakdown.total_machining_cost,
                "total_setup_cost": breakdown.total_setup_cost,
                "total_tooling_cost": breakdown.total_tooling_cost,
                "total_labour_cost": breakdown.total_labour_cost,
                "total_power_cost": breakdown.total_power_cost,
                "subtotal": breakdown.subtotal,
                "overhead": breakdown.overhead,
                "profit": breakdown.profit,
            },
            "total_cost": breakdown.unit_cost,
            "confidence_tier": confidence,
        }
    ).execute()

    log_usage(
        user_id, "estimate", 0.01, {"material": material, "processes": processes}
    )

    return EstimateResponse(
        material_name=breakdown.material_name,
        material_cost=breakdown.material_cost,
        process_lines=process_lines,
        total_machining_cost=breakdown.total_machining_cost,
        total_setup_cost=breakdown.total_setup_cost,
        total_tooling_cost=breakdown.total_tooling_cost,
        total_labour_cost=breakdown.total_labour_cost,
        total_power_cost=breakdown.total_power_cost,
        subtotal=breakdown.subtotal,
        overhead=breakdown.overhead,
        profit=breakdown.profit,
        unit_cost=breakdown.unit_cost,
        order_cost=breakdown.order_cost,
        quantity=breakdown.quantity,
        confidence_tier=confidence,
    )

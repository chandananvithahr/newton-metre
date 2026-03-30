"""POST /api/estimate -- run physics engine + validation, return cost breakdown."""
import logging

from fastapi import APIRouter, Depends, HTTPException, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from api.deps import get_current_user_id, get_supabase_admin
from api.cost_tracker import check_budget, log_usage
from api.schemas import EstimateRequest, EstimateResponse
from engines.mechanical.material_db import list_material_names

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)
logger = logging.getLogger("costimize")

ALLOWED_MATERIALS = list_material_names()
_MATERIAL_SET = set(ALLOWED_MATERIALS)


def _resolve_material(name: str) -> str | None:
    """Match material name exactly or by prefix. Returns canonical name or None."""
    if name in _MATERIAL_SET:
        return name
    # Try case-insensitive prefix match (e.g. "Mild Steel" → "Mild Steel IS2062")
    name_lower = name.lower()
    for mat in ALLOWED_MATERIALS:
        if mat.lower().startswith(name_lower) or name_lower.startswith(mat.lower()):
            return mat
    return None


@router.post("/estimate", response_model=EstimateResponse)
@limiter.limit("20/minute")
async def create_estimate(
    request: Request,
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
    raw_material = extracted.get("material", "Mild Steel IS2062")
    processes = extracted.get("suggested_processes", ["turning"])
    has_tight = extracted.get("tolerances", {}).get("has_tight_tolerances", False)

    # Validate material against known allowlist to prevent prompt injection
    material = _resolve_material(raw_material)
    if material is None:
        logger.warning("Unknown material rejected: %s (user: %s)", raw_material, user_id)
        raise HTTPException(
            status_code=400,
            detail=f"Unknown material '{raw_material}'. Allowed: {', '.join(sorted(ALLOWED_MATERIALS))}",
        )

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

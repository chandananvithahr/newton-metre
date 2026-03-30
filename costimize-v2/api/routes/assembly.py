"""POST /api/estimate/assembly -- cost multi-component assembly + joining process."""
import logging

from fastapi import APIRouter, Depends, HTTPException, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from api.cost_tracker import check_budget, log_usage
from api.deps import get_current_user_id, get_supabase_admin
from api.schemas import AssemblyEstimateRequest, AssemblyEstimateResponse, ComponentCostResult
from engines.assembly.joining_cost import calculate_joining_cost
from engines.mechanical.material_db import list_material_names

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)
logger = logging.getLogger("costimize")

ALLOWED_MATERIALS = list_material_names()
_MATERIAL_SET = set(ALLOWED_MATERIALS)
OVERHEAD_RATE = 0.15
PROFIT_RATE = 0.20


def _resolve_material(name: str) -> str | None:
    if name in _MATERIAL_SET:
        return name
    name_lower = name.lower()
    for mat in ALLOWED_MATERIALS:
        if mat.lower().startswith(name_lower) or name_lower.startswith(mat.lower()):
            return mat
    return None


@router.post("/estimate/assembly", response_model=AssemblyEstimateResponse)
@limiter.limit("10/minute")
async def create_assembly_estimate(
    request: Request,
    body: AssemblyEstimateRequest,
    user_id: str = Depends(get_current_user_id),
) -> AssemblyEstimateResponse:
    if not check_budget():
        raise HTTPException(
            status_code=429,
            detail="Service temporarily at capacity. Please try again tomorrow.",
        )
    if len(body.components) < 2:
        raise HTTPException(status_code=400, detail="Assembly requires at least 2 components.")
    if len(body.components) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 components per assembly.")

    from engines.mechanical.cost_engine import calculate_mechanical_cost

    component_results: list[ComponentCostResult] = []
    total_subtotal = 0.0

    for comp in body.components:
        extracted = comp.extracted_data
        dims = extracted.get("dimensions", {})
        raw_material = extracted.get("material") or "Mild Steel IS2062"
        processes = extracted.get("suggested_processes") or ["turning"]
        has_tight = (extracted.get("tolerances") or {}).get("has_tight_tolerances", False)

        material = _resolve_material(raw_material)
        if material is None:
            raise HTTPException(
                status_code=400,
                detail=f"Component '{comp.name}': unknown material '{raw_material}'.",
            )

        try:
            bd = calculate_mechanical_cost(
                dimensions=dims,
                material_name=material,
                selected_processes=processes,
                quantity=body.quantity,
                has_tight_tolerances=has_tight,
            )
        except Exception:
            logger.exception("Assembly component cost failed: %s", comp.name)
            raise HTTPException(
                status_code=500,
                detail=f"Cost calculation failed for component '{comp.name}'.",
            )

        component_results.append(
            ComponentCostResult(
                name=comp.name,
                material_name=bd.material_name,
                material_cost=round(bd.material_cost, 2),
                machining_cost=round(bd.total_machining_cost, 2),
                setup_cost=round(bd.total_setup_cost, 2),
                tooling_cost=round(bd.total_tooling_cost, 2),
                labour_cost=round(bd.total_labour_cost, 2),
                power_cost=round(bd.total_power_cost, 2),
                subtotal=round(bd.subtotal, 2),
                unit_cost=round(bd.unit_cost, 2),
            )
        )
        total_subtotal += bd.subtotal

    try:
        joining = calculate_joining_cost(body.joining_method, body.num_joints)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    # Apply overhead + profit once across entire assembly (components + joining)
    assembly_subtotal = round(total_subtotal + joining.total_joining_cost, 2)
    overhead = round(assembly_subtotal * OVERHEAD_RATE, 2)
    profit = round((assembly_subtotal + overhead) * PROFIT_RATE, 2)
    unit_cost = round(assembly_subtotal + overhead + profit, 2)
    order_cost = round(unit_cost * body.quantity, 2)

    try:
        sb = get_supabase_admin()
        sb.table("estimates").insert(
            {
                "user_id": user_id,
                "part_type": "assembly",
                "extracted_data": {
                    "components": [c.model_dump() for c in body.components],
                    "joining_method": body.joining_method,
                    "num_joints": body.num_joints,
                },
                "cost_breakdown": {
                    "components": [c.model_dump() for c in component_results],
                    "joining_cost": joining.total_joining_cost,
                    "joining_method": joining.method_label,
                    "assembly_subtotal": assembly_subtotal,
                    "overhead": overhead,
                    "profit": profit,
                },
                "total_cost": unit_cost,
                "confidence_tier": None,
            }
        ).execute()
    except Exception:
        logger.exception("Failed to persist assembly estimate for user %s", user_id)

    log_usage(
        user_id,
        "assembly_estimate",
        0.02,
        {"num_components": len(body.components), "joining": body.joining_method},
    )

    return AssemblyEstimateResponse(
        components=component_results,
        joining_cost=joining.total_joining_cost,
        joining_method_label=joining.method_label,
        joining_material_cost=joining.material_cost,
        joining_machine_cost=joining.machine_cost,
        joining_labour_cost=joining.labour_cost,
        assembly_subtotal=assembly_subtotal,
        overhead=overhead,
        profit=profit,
        unit_cost=unit_cost,
        order_cost=order_cost,
        quantity=body.quantity,
    )

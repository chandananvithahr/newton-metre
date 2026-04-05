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


# Keyword aliases → canonical name. AI often returns variations like "AL6061", "SS 304", "MS".
_MATERIAL_ALIASES: list[tuple[list[str], str]] = [
    # Specific/exotic materials first — prevents short keywords from shadowing them
    (["inconel", "inconel 718", "in718", "alloy 718", "uns n07718", "nickel alloy"], "Inconel 718"),
    (["titanium", "grade 5", "gr5", "gr.5", "ti-6al-4v", "ti6al4v"], "Titanium Grade 5"),
    # "ti " and " ti" removed — match inside "stainless", "ductile" etc.
    (["sg iron", "sgi", "fcd500", "fcd 500", "ductile iron", "nodular iron", "spheroidal graphite"], "SG Iron FCD500"),
    (["20mncr5", "20 mncr5", "5120", "aisi 5120", "case hardening steel"], "20MnCr5 Steel"),
    # Aluminium alloys
    (["al6061", "al 6061", "al-6061", "6061", "aluminum alloy", "aluminium alloy", "aluminum", "aluminium", "alloy al"], "Aluminum 6061"),
    (["al7075", "al 7075", "al-7075", "aluminum 7075", "aluminium 7075", "7075-t6"], "Aluminum 7075-T6"),
    # "7075" alone removed — false-matches part numbers containing those digits
    # Stainless steels
    (["stainless steel", "ss304", "ss 304", "aisi 304", "aisi304", "inox"], "Stainless Steel 304"),
    # "304" alone removed — matches PCD values, part numbers etc.
    (["ss316", "ss 316", "aisi 316", "aisi316", "stainless 316"], "Stainless Steel 316"),
    # "316" alone removed for same reason
    # Carbon and alloy steels
    (["en8", "en 8", "carbon steel en8", "080m40"], "EN8 Steel"),
    (["en24", "en 24", "817m40", "alloy steel en24"], "EN24 Steel"),
    (["en19", "en 19", "4140", "aisi 4140", "aisi4140", "40cr1mo28", "alloy steel en19"], "EN19 Steel"),
    (["mild steel", "is2062", "is 2062", "low carbon steel", "carbon steel"], "Mild Steel IS2062"),
    # "ms ", " ms" removed — "ms" matches inside "AMS", "dims", "cms" etc.
    # Other metals
    (["brass", "is319", "is 319", "cu zn", "cuzn"], "Brass IS319"),
    (["cast iron", "grey iron", "gray iron"], "Cast Iron"),
    # "ci " removed — matches "ci" inside "critical", "circuit", etc.
    (["copper", "electrolytic copper"], "Copper"),
    # "cu ", " cu" removed — matches inside "acute", "accumulate", "vacuum" etc.
]


def _resolve_material(name: str) -> str | None:
    """Match material name exactly, by prefix, or by keyword alias. Returns canonical name or None."""
    if name in _MATERIAL_SET:
        return name
    name_lower = name.lower().strip()
    # Prefix match (e.g. "Mild Steel" → "Mild Steel IS2062")
    for mat in ALLOWED_MATERIALS:
        if mat.lower().startswith(name_lower) or name_lower.startswith(mat.lower()):
            return mat
    # Keyword alias match (e.g. "Aluminum Alloy AL6061" → "Aluminum 6061")
    for keywords, canonical in _MATERIAL_ALIASES:
        for kw in keywords:
            if kw in name_lower:
                return canonical
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
    raw_dims = extracted.get("dimensions", {})
    # Coerce all dimension values to float — AI sometimes returns strings
    dims = {k: float(v) for k, v in raw_dims.items() if v is not None and v != ""}
    raw_material = extracted.get("material", "Mild Steel IS2062")
    processes = extracted.get("suggested_processes", ["turning"])
    # Ensure processes is a list, not a string
    if isinstance(processes, str):
        processes = [processes]
    has_tight = extracted.get("tolerances", {}).get("has_tight_tolerances", False)

    # Resolve material: exact/alias match first, then dynamic AI lookup
    material = _resolve_material(raw_material)
    dynamic_material_obj = None
    if material is None:
        logger.info("Unknown material '%s' — attempting dynamic lookup (user: %s)", raw_material, user_id)
        try:
            from engines.mechanical.material_fetcher import fetch_material_from_ai
            dynamic_material_obj = fetch_material_from_ai(raw_material)
            material = dynamic_material_obj.name  # use the original name
        except Exception as e:
            logger.warning("Dynamic material lookup failed for '%s': %s", raw_material, e)
            raise HTTPException(
                status_code=400,
                detail=f"Unknown material '{raw_material}' and automatic lookup failed. Please select a material manually.",
            )

    gdt_symbols = body.gdt_symbols or []
    surface_treatment_id = body.surface_treatment_id
    heat_treatment_id = body.heat_treatment_id
    machine_tier = body.machine_tier or "cnc_3axis"

    try:
        from engines.validation.orchestrator import orchestrate

        result = orchestrate(
            image_bytes=None,
            dimensions=dims,
            material_name=material,
            selected_processes=processes,
            quantity=body.quantity,
            has_tight_tolerances=has_tight,
            material_override=dynamic_material_obj,
            is_dynamic_material=dynamic_material_obj is not None,
            gdt_symbols=gdt_symbols,
            surface_treatment_id=surface_treatment_id,
            heat_treatment_id=heat_treatment_id,
            machine_tier=machine_tier,
        )
    except ValueError as e:
        # Dimension validation or other input errors — return 400 with clear message
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception("orchestrate() failed for user %s: %s", user_id, e)
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
                "unit_cost_low": breakdown.unit_cost_low,
                "unit_cost_high": breakdown.unit_cost_high,
                "uncertainty_pct": breakdown.uncertainty_pct,
                "supplier_quote": body.supplier_quote,
            },
            "total_cost": breakdown.unit_cost,
            "confidence_tier": confidence,
        }
    ).execute()

    # Link cost summary to the matching drawing in similarity index (non-blocking)
    if body.filename:
        try:
            drawing_row = (
                sb.table("drawings")
                .select("id, metadata")
                .eq("user_id", user_id)
                .eq("file_url", body.filename)
                .order("created_at", desc=True)
                .limit(1)
                .execute()
            )
            if drawing_row.data:
                d = drawing_row.data[0]
                meta = d.get("metadata") or {}
                meta["cost_summary"] = {
                    "unit_cost": round(breakdown.unit_cost, 2),
                    "unit_cost_low": round(breakdown.unit_cost_low, 2),
                    "unit_cost_high": round(breakdown.unit_cost_high, 2),
                    "material_cost": round(breakdown.material_cost, 2),
                    "total_machining_cost": round(breakdown.total_machining_cost, 2),
                    "confidence_tier": confidence,
                    "quantity": body.quantity,
                }
                sb.table("drawings").update({"metadata": meta}).eq("id", d["id"]).execute()
        except Exception as e:
            logger.warning("Failed to link cost to drawing '%s': %s", body.filename, e)

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
        surface_treatment_cost=breakdown.surface_treatment_cost,
        heat_treatment_cost=breakdown.heat_treatment_cost,
        machine_tier=breakdown.machine_tier,
        subtotal=breakdown.subtotal,
        overhead=breakdown.overhead,
        profit=breakdown.profit,
        unit_cost=breakdown.unit_cost,
        unit_cost_low=breakdown.unit_cost_low,
        unit_cost_high=breakdown.unit_cost_high,
        uncertainty_pct=breakdown.uncertainty_pct,
        order_cost=breakdown.order_cost,
        quantity=breakdown.quantity,
        confidence_tier=confidence,
    )

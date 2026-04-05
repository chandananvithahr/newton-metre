"""GET /api/treatments — list available surface and heat treatments."""
from fastapi import APIRouter

from engines.mechanical.surface_treatment_db import SURFACE_TREATMENTS
from engines.mechanical.heat_treatment_db import HEAT_TREATMENTS
from config import MACHINE_TIERS

router = APIRouter()


@router.get("/treatments/surface")
async def list_surface_treatments():
    """List all 40 surface treatments with metadata for frontend dropdowns."""
    return [
        {
            "id": tid,
            "name": t.name,
            "category": t.category,
            "rate_per_sq_dm": t.rate_per_sq_dm,
            "applicable_materials": t.applicable_materials,
            "industry": t.industry,
            "mil_spec": t.mil_spec,
            "thickness_um": t.thickness_um,
        }
        for tid, t in SURFACE_TREATMENTS.items()
    ]


@router.get("/treatments/heat")
async def list_heat_treatments():
    """List all 15 heat treatments with metadata for frontend dropdowns."""
    return [
        {
            "id": tid,
            "name": t.name,
            "rate_per_kg": t.rate_per_kg,
            "applicable_materials": t.applicable_materials,
            "industry": t.industry,
            "mil_spec": t.mil_spec,
            "cycle_time_hr": t.cycle_time_hr,
            "temperature_c": t.temperature_c,
        }
        for tid, t in HEAT_TREATMENTS.items()
    ]


@router.get("/treatments/machine-tiers")
async def list_machine_tiers():
    """List available machine tiers with rate multipliers."""
    return {
        tier_id: {
            "rate_multiplier": tier["rate_mult"],
            "speed_multiplier": tier["speed_mult"],
            "setup_multiplier": tier["setup_mult"],
        }
        for tier_id, tier in MACHINE_TIERS.items()
    }

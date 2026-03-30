"""GET /api/material-price -- return live INR price per kg for a material."""
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from api.deps import get_current_user_id
from api.schemas import MaterialPriceResponse
from engines.mechanical.material_db import list_material_names

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

_KNOWN_MATERIALS = set(list_material_names())


@router.get("/material-price", response_model=MaterialPriceResponse)
@limiter.limit("30/minute")
async def get_material_price_endpoint(
    request: Request,
    name: str = Query(..., min_length=1, max_length=100),
    user_id: str = Depends(get_current_user_id),
) -> MaterialPriceResponse:
    """Return INR/kg price for the given material name.

    Priority: physics DB → 24h cache → DEFAULT_PRICES fallback.
    If the material is not recognised at all, 422 is raised by Query validation
    only if min_length fails; unknown names get the scraper's default fallback.
    """
    if not name.strip():
        raise HTTPException(status_code=400, detail="Material name cannot be blank.")

    from scrapers.material_scraper import get_material_price, DEFAULT_PRICES

    source = "database" if name in _KNOWN_MATERIALS else (
        "cache" if name in DEFAULT_PRICES else "estimated"
    )
    price = get_material_price(name)
    return MaterialPriceResponse(name=name, price_inr=price, source=source)

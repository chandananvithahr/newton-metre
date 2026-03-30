"""RFQ routes — POST /api/rfq/extract and POST /api/rfq/estimate."""
import logging

from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from slowapi import Limiter
from slowapi.util import get_remote_address

from api.deps import get_current_user_id
from api.cost_tracker import check_budget, check_user_budget, log_usage
from api.schemas import (
    RFQExtractResponse,
    RFQLineItemResult,
    RFQEstimateRequest,
    RFQEstimateResponse,
    RFQLineItemEstimate,
)

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)
logger = logging.getLogger("costimize")

MAX_PDF_SIZE_BYTES = 20 * 1024 * 1024  # 20 MB — RFQ PDFs can be large


@router.post("/rfq/extract", response_model=RFQExtractResponse)
@limiter.limit("5/minute")
async def extract_rfq(
    request: Request,
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user_id),
) -> RFQExtractResponse:
    if not check_budget():
        raise HTTPException(
            status_code=429,
            detail="Service temporarily at capacity. Please try again tomorrow.",
        )

    if not check_user_budget(user_id):
        raise HTTPException(
            status_code=429,
            detail="You've used your $0.50 credit for this period. Credits refresh every 48 hours.",
        )

    if file.content_type and file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are accepted for RFQ extraction.",
        )

    pdf_bytes = await file.read()
    if len(pdf_bytes) > MAX_PDF_SIZE_BYTES:
        raise HTTPException(status_code=400, detail="File too large. Maximum 20MB.")

    # Step 1: classify
    try:
        from extractors.pdf_classifier import classify_pdf
        classification = classify_pdf(pdf_bytes)
    except Exception as e:
        logger.error("PDF classification error: %s", e)
        classification = {"document_type": "other", "confidence": "low", "reason": str(e)}

    # Step 2: extract RFQ line items
    try:
        from extractors.rfq_extractor import extract_rfq as _extract
        rfq_data = _extract(pdf_bytes)
    except Exception as e:
        logger.error("RFQ extraction error: %s", e)
        raise HTTPException(
            status_code=500,
            detail="Failed to extract RFQ data. Please ensure the PDF is readable.",
        )

    log_usage(user_id, "rfq_extract", 0.01, {"filename": file.filename, "pages": rfq_data.get("page_count", 0)})

    line_items = [
        RFQLineItemResult(
            line_number=item["line_number"],
            part_number=item.get("part_number"),
            description=item.get("description", ""),
            quantity=item.get("quantity", 1),
            material=item.get("material"),
            delivery_weeks=item.get("delivery_weeks"),
            dimensions=item.get("dimensions") or {},
            suggested_processes=item.get("suggested_processes") or [],
            unit_price_expected=item.get("unit_price_expected"),
            notes=item.get("notes"),
        )
        for item in rfq_data.get("line_items", [])
    ]

    return RFQExtractResponse(
        rfq_number=rfq_data.get("rfq_number"),
        customer=rfq_data.get("customer"),
        date=rfq_data.get("date"),
        document_type=classification.get("document_type", "other"),
        line_items=line_items,
        confidence=rfq_data.get("confidence", "low"),
        page_count=rfq_data.get("page_count", 0),
    )


@router.post("/rfq/estimate", response_model=RFQEstimateResponse)
@limiter.limit("5/minute")
async def estimate_rfq(
    request: Request,
    body: RFQEstimateRequest,
    user_id: str = Depends(get_current_user_id),
) -> RFQEstimateResponse:
    if not check_budget():
        raise HTTPException(
            status_code=429,
            detail="Service temporarily at capacity. Please try again tomorrow.",
        )

    if not check_user_budget(user_id):
        raise HTTPException(
            status_code=429,
            detail="You've used your $0.50 credit for this period. Credits refresh every 48 hours.",
        )

    if not body.line_items:
        raise HTTPException(status_code=400, detail="No line items provided.")

    if len(body.line_items) > 50:
        raise HTTPException(status_code=400, detail="Maximum 50 line items per RFQ.")

    from engines.mechanical.cost_engine import calculate_mechanical_cost
    from engines.mechanical.material_db import resolve_material

    estimated_items: list[RFQLineItemEstimate] = []
    total_order_cost = 0.0

    for item in body.line_items:
        try:
            dims = item.dimensions or {}
            # Build extracted_data compatible with the mechanical engine
            extracted_data = {
                "part_type": _infer_part_type(dims, item.suggested_processes),
                "dimensions": {
                    "outer_diameter_mm": dims.get("outer_diameter_mm"),
                    "length_mm": dims.get("length_mm"),
                    "width_mm": dims.get("width_mm"),
                    "height_mm": dims.get("height_mm"),
                    "inner_diameter_mm": dims.get("inner_diameter_mm"),
                    "hole_count": dims.get("hole_count"),
                    "thread_count": dims.get("thread_count"),
                },
                "material": item.material,
                "tolerances": {"has_tight_tolerances": False},
                "suggested_processes": item.suggested_processes,
                "confidence": "medium",
            }

            resolved = resolve_material(item.material or "mild_steel")
            result = calculate_mechanical_cost(extracted_data, resolved, quantity=item.quantity)

            # Apply overhead (15%) + profit (20%) — same as single estimate route
            overhead = result.subtotal * 0.15
            profit = (result.subtotal + overhead) * 0.20
            unit_cost = result.subtotal + overhead + profit
            order_cost = unit_cost * item.quantity

            total_order_cost += order_cost
            estimated_items.append(RFQLineItemEstimate(
                line_number=item.line_number,
                part_number=item.part_number,
                description=item.description,
                quantity=item.quantity,
                material=item.material,
                unit_cost=round(unit_cost, 2),
                order_cost=round(order_cost, 2),
                confidence_tier="medium",
                error=None,
            ))

        except Exception as e:
            logger.warning("Failed to estimate RFQ line %d: %s", item.line_number, e)
            estimated_items.append(RFQLineItemEstimate(
                line_number=item.line_number,
                part_number=item.part_number,
                description=item.description,
                quantity=item.quantity,
                material=item.material,
                unit_cost=0.0,
                order_cost=0.0,
                confidence_tier=None,
                error="Could not estimate — dimensions may be missing or unclear",
            ))

    log_usage(user_id, "rfq_estimate", 0.01, {"line_item_count": len(body.line_items)})

    return RFQEstimateResponse(
        line_items=estimated_items,
        total_order_cost=round(total_order_cost, 2),
        currency="INR",
    )


def _infer_part_type(dims: dict, processes: list[str]) -> str:
    """Infer part_type from dimensions and processes for the mechanical engine."""
    has_od = dims.get("outer_diameter_mm") is not None
    has_turning = any(p in ("turning", "facing", "boring") for p in processes)

    if has_od or has_turning:
        return "turning"
    return "milling"

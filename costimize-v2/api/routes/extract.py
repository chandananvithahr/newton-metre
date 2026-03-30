"""POST /api/extract -- upload drawing, AI extracts dimensions + processes."""
from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from slowapi import Limiter
from slowapi.util import get_remote_address

from api.deps import get_current_user_id
from api.cost_tracker import check_budget, log_usage
from api.schemas import ExtractionResponse

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB

ALLOWED_CONTENT_TYPES = {
    "image/png", "image/jpeg", "image/jpg", "image/webp",
    "application/pdf", "image/tiff",
}


@router.post("/extract", response_model=ExtractionResponse)
@limiter.limit("10/minute")
async def extract_drawing(
    request: Request,
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user_id),
) -> ExtractionResponse:
    if not check_budget():
        raise HTTPException(
            status_code=429,
            detail="Service temporarily at capacity. Please try again tomorrow.",
        )

    if file.content_type and file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{file.content_type}'. Accepted: PDF, PNG, JPEG, TIFF, WebP.",
        )

    image_bytes = await file.read()
    if len(image_bytes) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(status_code=400, detail="File too large. Maximum 10MB.")

    try:
        from extractors.vision import analyze_drawing

        result = analyze_drawing(image_bytes, file.filename or "drawing.png")
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to analyze drawing. Please try a clearer image.",
        )

    log_usage(user_id, "extract", 0.03, {"filename": file.filename})

    return ExtractionResponse(
        dimensions=result.get("dimensions", {}),
        material=result.get("material"),
        tolerances=result.get("tolerances", {}),
        suggested_processes=result.get("suggested_processes", []),
        confidence=result.get("confidence", "low"),
        notes=result.get("notes", ""),
    )

"""POST /api/extract -- upload drawing, AI extracts dimensions + processes."""
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from api.deps import get_current_user_id
from api.cost_tracker import check_budget, log_usage
from api.schemas import ExtractionResponse

router = APIRouter()

MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB


@router.post("/extract", response_model=ExtractionResponse)
async def extract_drawing(
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user_id),
) -> ExtractionResponse:
    if not check_budget():
        raise HTTPException(
            status_code=429,
            detail="Service temporarily at capacity. Please try again tomorrow.",
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

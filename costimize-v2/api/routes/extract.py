"""POST /api/extract -- upload drawing, AI extracts dimensions + processes."""
import logging
from pathlib import Path
from typing import List
from fastapi import APIRouter, BackgroundTasks, Depends, File, HTTPException, Request, UploadFile
from slowapi import Limiter
from slowapi.util import get_remote_address

from api.deps import get_current_user_id, get_supabase_admin
from api.cost_tracker import check_budget, check_user_budget, log_usage
from api.schemas import ExtractionResponse

logger = logging.getLogger(__name__)

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

MAX_FILE_SIZE_BYTES = 20 * 1024 * 1024  # 20 MB (CAD files can be larger)
MAX_SHEETS = 5

ALLOWED_CONTENT_TYPES = {
    "image/png", "image/jpeg", "image/jpg", "image/webp",
    "application/pdf", "image/tiff",
    # DXF / DWG
    "application/dxf", "application/acad", "image/vnd.dxf",
    "image/x-dwg", "image/vnd.dwg", "application/dwg", "application/x-dwg",
    # STEP
    "application/step", "application/stp", "model/step", "model/stp",
    # Generic binary — client may send CAD files as octet-stream; we detect by extension
    "application/octet-stream",
}

ALLOWED_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".webp", ".pdf", ".tiff",
    ".dxf", ".dwg", ".step", ".stp",
}


def _auto_embed_drawing(image_bytes: bytes, filename: str, user_id: str) -> None:
    """Background task: embed the drawing into the similarity index.

    Silently skips on any failure — the user shouldn't be blocked by this.
    """
    try:
        from engines.similarity.preprocessor import preprocess_drawing
        from engines.similarity.embedder import embed_image

        embed_img, _thumbnail = preprocess_drawing(image_bytes, filename)
        embedding = embed_image(embed_img)

        # Generate text description for BM25 hybrid search
        from api.routes.similarity import _describe_drawing
        text_description = _describe_drawing(image_bytes)

        metadata = {"filename": filename, "source": "auto_embed"}
        if text_description:
            metadata["description"] = text_description[:200]

        sb = get_supabase_admin()
        sb.table("drawings").insert({
            "user_id": user_id,
            "file_url": filename,
            "embedding": embedding.tolist(),
            "text_description": text_description,
            "metadata": metadata,
        }).execute()

        logger.info("Auto-embedded drawing '%s' for user %s", filename, user_id)
    except Exception as e:
        logger.warning("Auto-embed failed for '%s': %s", filename, e)


@router.post("/extract", response_model=ExtractionResponse)
@limiter.limit("10/minute")
async def extract_drawing(
    request: Request,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user_id),
) -> ExtractionResponse:
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

    filename = file.filename or "drawing.bin"
    ext = Path(filename).suffix.lower()

    if ext not in ALLOWED_EXTENSIONS and (file.content_type and file.content_type not in ALLOWED_CONTENT_TYPES):
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Accepted: PDF, PNG, JPEG, TIFF, WebP, DXF, DWG, STEP/STP.",
        )

    raw_bytes = await file.read()
    if len(raw_bytes) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(status_code=400, detail="File too large. Maximum 20MB.")

    try:
        from extractors.vision import analyze_drawing, analyze_step_text
        from extractors.cad_converter import dxf_to_text, step_to_text, is_dxf_dwg, is_step

        if is_dxf_dwg(file.content_type, filename):
            try:
                cad_text = dxf_to_text(raw_bytes, filename)
                result = analyze_step_text(cad_text)   # same text AI path
            except (RuntimeError, Exception) as dwg_err:
                import logging
                logging.getLogger(__name__).warning("DXF/DWG native extraction failed (%s), falling back to AI vision", dwg_err)
                # Fallback: send raw bytes to AI vision (GPT-4o handles many binary formats)
                result = analyze_drawing(raw_bytes, filename)
        elif is_step(file.content_type, filename):
            cad_text = step_to_text(raw_bytes)
            result = analyze_step_text(cad_text)
        else:
            result = analyze_drawing(raw_bytes, filename)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        import logging
        logging.getLogger(__name__).exception("Extract RuntimeError: %s", e)
        raise HTTPException(status_code=500, detail="Failed to analyze drawing. Please try a clearer image.")
    except Exception as e:
        import logging
        logging.getLogger(__name__).exception("Extract failed: %s", e)
        raise HTTPException(
            status_code=500, detail="Failed to analyze drawing. Please try a clearer image.",
        )

    log_usage(user_id, "extract", 0.002, {"filename": file.filename})

    # Auto-embed into similarity index (background — doesn't block response)
    background_tasks.add_task(_auto_embed_drawing, raw_bytes, filename, user_id)

    material = result.get("material")
    overall_confidence = result.get("confidence", "low")
    material_confidence = "low" if material is None else overall_confidence

    return ExtractionResponse(
        dimensions=result.get("dimensions", {}),
        material=material,
        material_confidence=material_confidence,
        tolerances=result.get("tolerances", {}),
        suggested_processes=result.get("suggested_processes", []),
        confidence=overall_confidence,
        notes=result.get("notes", ""),
    )


@router.post("/extract/multi", response_model=ExtractionResponse)
@limiter.limit("5/minute")
async def extract_multi_view_drawing(
    request: Request,
    files: List[UploadFile] = File(...),
    user_id: str = Depends(get_current_user_id),
) -> ExtractionResponse:
    """Accept 2-5 sheets of the same part drawing and return a combined extraction.
    Returns HTTP 422 if sheets appear to be from different parts."""

    if not check_budget():
        raise HTTPException(status_code=429, detail="Service temporarily at capacity. Please try again tomorrow.")
    if not check_user_budget(user_id):
        raise HTTPException(status_code=429, detail="You've used your $0.50 credit for this period. Credits refresh every 48 hours.")
    if len(files) < 2:
        raise HTTPException(status_code=400, detail="Upload at least 2 sheets for multi-view extraction.")
    if len(files) > MAX_SHEETS:
        raise HTTPException(status_code=400, detail=f"Maximum {MAX_SHEETS} sheets per part.")

    images: list[bytes] = []
    for f in files:
        if f.content_type and f.content_type not in ALLOWED_CONTENT_TYPES:
            raise HTTPException(status_code=400, detail=f"Unsupported file type '{f.content_type}' in {f.filename}.")
        data = await f.read()
        if len(data) > MAX_FILE_SIZE_BYTES:
            raise HTTPException(status_code=400, detail=f"{f.filename} exceeds 10MB limit.")
        images.append(data)

    try:
        from extractors.vision import analyze_multi_view_drawing
        result = analyze_multi_view_drawing(images)
    except ValueError as e:
        # Drawing mismatch detected by AI
        raise HTTPException(status_code=422, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to analyze drawings. Please try clearer images.")

    log_usage(user_id, "extract_multi", 0.004, {"sheet_count": len(files)})

    material = result.get("material")
    overall_confidence = result.get("confidence", "low")
    material_confidence = "low" if material is None else overall_confidence

    return ExtractionResponse(
        dimensions=result.get("dimensions", {}),
        material=material,
        material_confidence=material_confidence,
        tolerances=result.get("tolerances", {}),
        suggested_processes=result.get("suggested_processes", []),
        confidence=overall_confidence,
        notes=result.get("notes", ""),
    )

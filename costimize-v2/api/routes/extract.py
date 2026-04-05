"""POST /api/extract -- upload drawing, AI extracts dimensions + processes."""
import io
import logging
import zipfile
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
MAX_ZIP_SIZE_BYTES = 50 * 1024 * 1024   # 50 MB for assembly ZIPs
MAX_ZIP_FILES = 20                       # max drawing files inside ZIP
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


def _extract_single_file(raw_bytes: bytes, filename: str, content_type: str | None = None) -> dict:
    """Core extraction logic for a single drawing file.

    Returns the raw result dict from the AI extractor.
    Raises ValueError for bad input, RuntimeError for AI failures.
    """
    from extractors.vision import analyze_cad_file
    return analyze_cad_file(raw_bytes, filename)


def _result_to_response(result: dict) -> ExtractionResponse:
    """Convert raw extraction dict to ExtractionResponse."""
    material = result.get("material")
    overall_confidence = result.get("confidence", "low")
    material_confidence = "low" if material is None else overall_confidence
    return ExtractionResponse(
        dimensions=result.get("dimensions", {}),
        material=material,
        material_confidence=material_confidence,
        tolerances=result.get("tolerances", {}),
        suggested_processes=result.get("suggested_processes", []),
        gdt_symbols=result.get("gdt_symbols", []),
        confidence=overall_confidence,
        notes=result.get("notes", ""),
    )


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
        result = _extract_single_file(raw_bytes, filename, file.content_type)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        logger.exception("Extract RuntimeError: %s", e)
        raise HTTPException(status_code=500, detail="Failed to analyze drawing. Please try a clearer image.")
    except Exception as e:
        logger.exception("Extract failed: %s", e)
        raise HTTPException(
            status_code=500, detail="Failed to analyze drawing. Please try a clearer image.",
        )

    log_usage(user_id, "extract", 0.002, {"filename": file.filename})

    # Auto-embed into similarity index (background — doesn't block response)
    background_tasks.add_task(_auto_embed_drawing, raw_bytes, filename, user_id)

    return _result_to_response(result)


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

    return _result_to_response(result)


@router.post("/extract/assembly-zip", response_model=list[ExtractionResponse])
@limiter.limit("3/minute")
async def extract_assembly_zip(
    request: Request,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user_id),
) -> list[ExtractionResponse]:
    """Extract dimensions from every drawing inside a ZIP file.

    Accepts a ZIP containing PDF/PNG/JPEG/DXF/STEP files — one per component.
    Returns an array of ExtractionResponse objects, one per file.
    Files that fail extraction are included with confidence="failed" and error in notes.
    """
    if not check_budget():
        raise HTTPException(status_code=429, detail="Service temporarily at capacity. Please try again tomorrow.")
    if not check_user_budget(user_id):
        raise HTTPException(status_code=429, detail="You've used your $0.50 credit for this period. Credits refresh every 48 hours.")

    raw_bytes = await file.read()
    if len(raw_bytes) > MAX_ZIP_SIZE_BYTES:
        raise HTTPException(status_code=400, detail="ZIP too large. Maximum 50MB.")

    try:
        zf = zipfile.ZipFile(io.BytesIO(raw_bytes))
    except zipfile.BadZipFile:
        raise HTTPException(status_code=400, detail="Invalid ZIP file.")

    # Filter to drawing files only (skip directories, __MACOSX, hidden files)
    drawing_entries = []
    for info in zf.infolist():
        if info.is_dir():
            continue
        name = info.filename
        if name.startswith("__MACOSX") or "/." in name or name.startswith("."):
            continue
        ext = Path(name).suffix.lower()
        if ext in ALLOWED_EXTENSIONS:
            drawing_entries.append(info)

    if not drawing_entries:
        raise HTTPException(status_code=400, detail="ZIP contains no supported drawing files (PDF, PNG, JPEG, DXF, STEP).")
    if len(drawing_entries) > MAX_ZIP_FILES:
        raise HTTPException(status_code=400, detail=f"Too many files. Maximum {MAX_ZIP_FILES} drawings per ZIP.")

    responses: list[ExtractionResponse] = []
    for info in drawing_entries:
        member_bytes = zf.read(info.filename)
        fname = Path(info.filename).name  # strip directory path
        try:
            result = _extract_single_file(member_bytes, fname)
            resp = _result_to_response(result)
            # Tag the filename in notes so frontend can match components
            resp = ExtractionResponse(
                dimensions=resp.dimensions,
                material=resp.material,
                material_confidence=resp.material_confidence,
                tolerances=resp.tolerances,
                suggested_processes=resp.suggested_processes,
                gdt_symbols=resp.gdt_symbols,
                confidence=resp.confidence,
                notes=f"[{fname}] {resp.notes}" if resp.notes else fname,
            )
        except Exception as e:
            logger.warning("Assembly ZIP: failed to extract '%s': %s", fname, e)
            resp = ExtractionResponse(
                dimensions={},
                material=None,
                material_confidence="low",
                tolerances={},
                suggested_processes=[],
                gdt_symbols=[],
                confidence="failed",
                notes=f"[{fname}] Extraction failed: {e}",
            )
        responses.append(resp)

    # Auto-embed each drawing in background
    for info in drawing_entries:
        member_bytes = zf.read(info.filename)
        fname = Path(info.filename).name
        background_tasks.add_task(_auto_embed_drawing, member_bytes, fname, user_id)

    log_usage(user_id, "extract_assembly_zip", 0.002 * len(drawing_entries), {
        "filename": file.filename, "drawing_count": len(drawing_entries),
    })

    return responses

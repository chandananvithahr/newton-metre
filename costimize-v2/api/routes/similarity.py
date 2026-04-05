"""Similarity search routes -- embed drawings + find matches.

Supports:
  - /similarity/embed: Upload drawing → 768-dim Gemini embedding + text description → Supabase
  - /similarity/search: Upload drawing → hybrid search (vector + BM25 text) → ranked matches
"""
import logging

from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from slowapi import Limiter
from slowapi.util import get_remote_address

from api.deps import get_current_user_id, get_supabase_admin
from api.cost_tracker import check_budget, check_user_budget, log_usage
from api.schemas import SimilarityEmbedResponse, SimilaritySearchResponse, SimilarityMatch

logger = logging.getLogger(__name__)

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB


def _describe_drawing(image_bytes: bytes) -> str:
    """Get a text description of the drawing for BM25 search.

    Uses the same Gemini Flash call that the embedder uses internally.
    Returns empty string on failure (non-blocking).
    """
    try:
        from config import GEMINI_API_KEY
        if not GEMINI_API_KEY:
            return ""

        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-2.0-flash-lite")

        response = model.generate_content(
            [
                "Describe this engineering drawing in 50-100 words. Focus on: shape, features "
                "(holes, slots, threads, chamfers), material clues, manufacturing processes visible, "
                "dimensions/proportions, and complexity. Be technical and precise.",
                {"mime_type": "image/png", "data": image_bytes},
            ],
            generation_config={"max_output_tokens": 300, "temperature": 0.0},
        )
        return response.text.strip()
    except Exception as e:
        logger.warning("Failed to generate text description: %s", e)
        return ""


@router.post("/similarity/embed", response_model=SimilarityEmbedResponse)
@limiter.limit("15/minute")
async def embed_drawing(
    request: Request,
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user_id),
):
    if not check_budget():
        raise HTTPException(status_code=429, detail="Service temporarily at capacity.")

    if not check_user_budget(user_id):
        raise HTTPException(
            status_code=429,
            detail="You've used your $0.50 credit for this period. Credits refresh every 48 hours.",
        )

    image_bytes = await file.read()
    if len(image_bytes) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(status_code=400, detail="File too large. Maximum 10MB.")

    try:
        from engines.similarity.preprocessor import preprocess_drawing
        from engines.similarity.embedder import embed_image

        embed_img, thumbnail = preprocess_drawing(image_bytes, file.filename or "drawing.png")
        embedding = embed_image(embed_img)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to process drawing. Please try a different image.")

    # Generate text description for BM25 hybrid search (non-blocking on failure)
    text_description = _describe_drawing(image_bytes)

    # Extract structured metadata (material, dimensions, processes) for ranker
    metadata = {"filename": file.filename}
    if text_description:
        metadata["description"] = text_description[:200]

    try:
        from extractors.vision import analyze_drawing
        extracted = analyze_drawing(image_bytes, file.filename or "drawing.png")
        dims = extracted.get("dimensions", {})
        # Store only non-null dimension values
        metadata["dimensions"] = {k: v for k, v in dims.items() if v}
        metadata["material"] = extracted.get("material") or ""
        metadata["processes"] = extracted.get("suggested_processes", [])
        tol = extracted.get("tolerances", {})
        if tol.get("tightest_tolerance_mm"):
            metadata["tolerances"] = {"tightest_tolerance_mm": tol["tightest_tolerance_mm"]}
        metadata["surface_finish_ra"] = 0.0  # TODO: extract Ra from drawing
    except Exception as e:
        logger.warning("Metadata extraction failed for %s (non-blocking): %s", file.filename, e)
        # Non-blocking: embed works without metadata, ranker falls back to defaults

    sb = get_supabase_admin()
    result = sb.table("drawings").insert({
        "user_id": user_id,
        "file_url": file.filename,
        "embedding": embedding.tolist(),
        "text_description": text_description,
        "metadata": metadata,
    }).execute()

    drawing_id = result.data[0]["id"] if result.data else "unknown"

    log_usage(user_id, "similarity_embed", 0.005, {"filename": file.filename})

    return SimilarityEmbedResponse(
        drawing_id=drawing_id,
        message="Drawing embedded successfully",
    )


@router.post("/similarity/search", response_model=SimilaritySearchResponse)
@limiter.limit("15/minute")
async def search_similar(
    request: Request,
    file: UploadFile = File(...),
    role: str = "default",
    user_id: str = Depends(get_current_user_id),
):
    if not check_budget():
        raise HTTPException(status_code=429, detail="Service temporarily at capacity.")

    if not check_user_budget(user_id):
        raise HTTPException(
            status_code=429,
            detail="You've used your $0.50 credit for this period. Credits refresh every 48 hours.",
        )

    image_bytes = await file.read()
    if len(image_bytes) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(status_code=400, detail="File too large. Maximum 10MB.")

    try:
        from engines.similarity.preprocessor import preprocess_drawing
        from engines.similarity.embedder import embed_image

        embed_img, thumbnail = preprocess_drawing(image_bytes, file.filename or "drawing.png")
        query_embedding = embed_image(embed_img)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to process drawing for search.")

    # Extract query drawing metadata for ranker
    query_material = ""
    query_dimensions: dict = {}
    query_processes: list[str] = []
    query_tolerances: dict = {}
    try:
        from extractors.vision import analyze_drawing
        extracted = analyze_drawing(image_bytes, file.filename or "drawing.png")
        query_material = extracted.get("material") or ""
        query_dimensions = {k: v for k, v in extracted.get("dimensions", {}).items() if v}
        query_processes = extracted.get("suggested_processes", [])
        tol = extracted.get("tolerances", {})
        if tol.get("tightest_tolerance_mm"):
            query_tolerances = {"tightest_tolerance_mm": tol["tightest_tolerance_mm"]}
    except Exception as e:
        logger.warning("Query metadata extraction failed (ranker will use defaults): %s", e)

    # Generate text description for hybrid BM25 search
    query_text = _describe_drawing(image_bytes)

    sb = get_supabase_admin()

    # Fetch 20 candidates from Supabase (over-fetch for re-ranking)
    fetch_count = 20

    if query_text:
        result = sb.rpc("match_drawings_hybrid", {
            "query_embedding": query_embedding.tolist(),
            "query_text": query_text,
            "match_count": fetch_count,
            "p_user_id": user_id,
            "vector_weight": 0.7,
            "text_weight": 0.3,
        }).execute()
    else:
        result = sb.rpc("match_drawings", {
            "query_embedding": query_embedding.tolist(),
            "match_threshold": 0.2,
            "match_count": fetch_count,
            "p_user_id": user_id,
        }).execute()

    rows = result.data or []

    if not rows:
        log_usage(user_id, "similarity_search", 0.005, {"matches_found": 0})
        return SimilaritySearchResponse(matches=[])

    # Re-rank with multi-signal ranker (visual + material + dimension + process + tolerance + finish)
    from engines.similarity.ranker import rank_candidates, PRESET_WEIGHTS

    weights = PRESET_WEIGHTS.get(role, PRESET_WEIGHTS["default"])

    candidates = []
    for row in rows:
        meta = row.get("metadata") or {}
        meta["drawing_id"] = row["id"]
        meta["text_description"] = row.get("text_description", "")
        candidates.append((meta, row["similarity"]))

    ranked = rank_candidates(
        candidates=candidates,
        query_material=query_material,
        query_dimensions=query_dimensions,
        query_processes=query_processes,
        query_tolerances=query_tolerances,
        top_k=10,
        weights=weights,
    )

    matches = [
        SimilarityMatch(
            drawing_id=r.drawing_id,
            score=r.combined_score,
            metadata={
                **r.metadata,
                "score_breakdown": {
                    "visual": r.visual_score,
                    "material": r.material_score,
                    "dimension": r.dimension_score,
                    "process": r.process_score,
                    "tolerance": r.tolerance_score,
                    "finish": r.finish_score,
                },
            },
        )
        for r in ranked
    ]

    log_usage(user_id, "similarity_search", 0.005, {"matches_found": len(matches), "role": role})

    return SimilaritySearchResponse(matches=matches)


@router.get("/similarity/library")
async def list_library(
    user_id: str = Depends(get_current_user_id),
):
    """List all drawings indexed in the user's company brain library."""
    sb = get_supabase_admin()
    result = sb.table("drawings").select(
        "id, file_url, text_description, metadata, created_at"
    ).eq("user_id", user_id).order("created_at", desc=False).limit(200).execute()

    drawings = []
    for row in (result.data or []):
        filename = (
            row.get("file_url")
            or (row.get("metadata") or {}).get("filename")
            or "drawing"
        )
        drawings.append({
            "id": row["id"],
            "filename": filename,
            "description": (row.get("text_description") or "")[:200],
            "created_at": row["created_at"],
        })

    return {"total": len(drawings), "drawings": drawings}

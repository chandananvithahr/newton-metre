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
        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(
            [
                "Describe this engineering drawing in 50-100 words. Focus on: shape, features "
                "(holes, slots, threads, chamfers), material clues, manufacturing processes visible, "
                "dimensions/proportions, and complexity. Be technical and precise.",
                {"mime_type": "image/png", "data": image_bytes},
            ],
            generation_config={"max_output_tokens": 300},
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

    sb = get_supabase_admin()
    result = sb.table("drawings").insert({
        "user_id": user_id,
        "file_url": file.filename,
        "embedding": embedding.tolist(),
        "text_description": text_description,
        "metadata": {"filename": file.filename},
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

    # Generate text description for hybrid BM25 search
    query_text = _describe_drawing(image_bytes)

    sb = get_supabase_admin()

    # Use hybrid search (vector + BM25) when we have a text description, else vector-only
    if query_text:
        result = sb.rpc("match_drawings_hybrid", {
            "query_embedding": query_embedding.tolist(),
            "query_text": query_text,
            "match_count": 10,
            "p_user_id": user_id,
            "vector_weight": 0.7,
            "text_weight": 0.3,
        }).execute()
    else:
        result = sb.rpc("match_drawings", {
            "query_embedding": query_embedding.tolist(),
            "match_threshold": 0.3,
            "match_count": 10,
            "p_user_id": user_id,
        }).execute()

    matches = [
        SimilarityMatch(
            drawing_id=row["id"],
            score=row["similarity"],
            metadata=row.get("metadata", {}),
        )
        for row in (result.data or [])
    ]

    log_usage(user_id, "similarity_search", 0.005, {"matches_found": len(matches)})

    return SimilaritySearchResponse(matches=matches)

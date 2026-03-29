"""Similarity search routes -- embed drawings + find matches."""
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from api.deps import get_current_user_id, get_supabase_admin
from api.cost_tracker import check_budget, log_usage
from api.schemas import SimilarityEmbedResponse, SimilaritySearchResponse, SimilarityMatch

router = APIRouter()


@router.post("/similarity/embed", response_model=SimilarityEmbedResponse)
async def embed_drawing(
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user_id),
):
    if not check_budget():
        raise HTTPException(status_code=429, detail="Service temporarily at capacity.")

    image_bytes = await file.read()
    if len(image_bytes) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large. Maximum 10MB.")

    try:
        from engines.similarity.preprocessor import preprocess_drawing
        from engines.similarity.embedder import DrawingEmbedder

        processed = preprocess_drawing(image_bytes, file.filename or "drawing.png")
        embedder = DrawingEmbedder()
        embedding = embedder.embed(processed.clean_image)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to process drawing. Please try a different image.")

    sb = get_supabase_admin()
    result = sb.table("drawings").insert({
        "user_id": user_id,
        "file_url": file.filename,
        "embedding": embedding.tolist(),
        "metadata": {"filename": file.filename},
    }).execute()

    drawing_id = result.data[0]["id"] if result.data else "unknown"

    log_usage(user_id, "similarity_embed", 0.005, {"filename": file.filename})

    return SimilarityEmbedResponse(
        drawing_id=drawing_id,
        message="Drawing embedded successfully",
    )


@router.post("/similarity/search", response_model=SimilaritySearchResponse)
async def search_similar(
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user_id),
):
    if not check_budget():
        raise HTTPException(status_code=429, detail="Service temporarily at capacity.")

    image_bytes = await file.read()

    try:
        from engines.similarity.preprocessor import preprocess_drawing
        from engines.similarity.embedder import DrawingEmbedder

        processed = preprocess_drawing(image_bytes, file.filename or "drawing.png")
        embedder = DrawingEmbedder()
        query_embedding = embedder.embed(processed.clean_image)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to process drawing for search.")

    sb = get_supabase_admin()
    result = sb.rpc("match_drawings", {
        "query_embedding": query_embedding.tolist(),
        "match_threshold": 0.5,
        "match_count": 5,
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

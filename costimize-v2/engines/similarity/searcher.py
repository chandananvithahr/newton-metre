"""Drawing similarity searcher — the main search API.

Combines: preprocessor → embedder → FAISS search → multi-signal ranking.

Usage:
    searcher = DrawingSearcher()
    results = searcher.search(image_bytes, "drawing.pdf",
                              material="EN8 Steel",
                              dimensions={"outer_diameter_mm": 55},
                              processes=["turning", "milling"])
"""
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image

from engines.similarity.indexer import SimilarityIndex, DrawingRecord
from engines.similarity.ranker import (
    RankedResult,
    RankingWeights,
    PRESET_WEIGHTS,
    rank_candidates,
)


@dataclass(frozen=True)
class SearchResult:
    """A similarity search result with cost intelligence."""
    rank: int
    drawing_id: str
    file_name: str
    thumbnail_path: str
    combined_score: float
    visual_score: float
    material_score: float
    dimension_score: float
    process_score: float

    # Cost intelligence (the Costimize differentiator)
    material: str
    dimensions: dict
    processes: tuple[str, ...]
    historical_costs: tuple[dict, ...]
    physics_should_cost_inr: float

    # Design context
    part_number: str
    title: str
    revision: str
    designer: str
    project: str
    notes: str


class DrawingSearcher:
    """Main search interface for drawing similarity."""

    def __init__(self, index_dir: Path | None = None):
        from engines.similarity.indexer import INDEX_DIR
        self._index = SimilarityIndex(index_dir or INDEX_DIR)

    @property
    def index_count(self) -> int:
        return self._index.count

    def ingest(
        self,
        file_bytes: bytes,
        filename: str,
        drawing_id: str,
        metadata: dict,
        cost_context: dict | None = None,
        design_context: dict | None = None,
    ) -> None:
        """Ingest a drawing into the search index.

        Args:
            file_bytes: Raw file bytes
            filename: Original filename
            drawing_id: Unique ID for this drawing
            metadata: Extracted metadata (from vision.py or manual)
            cost_context: Historical cost data
            design_context: Design revision info
        """
        from engines.similarity.preprocessor import preprocess_drawing, save_thumbnail
        from engines.similarity.embedder import embed_image
        from engines.similarity.indexer import THUMBNAIL_DIR
        from datetime import datetime, timezone

        # Preprocess
        embed_img, thumbnail = preprocess_drawing(file_bytes, filename)

        # Save thumbnail
        thumb_path = save_thumbnail(thumbnail, drawing_id, THUMBNAIL_DIR)

        # Generate embedding
        embedding = embed_image(embed_img)

        # Build record
        cost = cost_context or {}
        design = design_context or {}
        dims = metadata.get("dimensions", {})
        processes = metadata.get("processes", metadata.get("suggested_processes", []))

        record = DrawingRecord(
            drawing_id=drawing_id,
            file_name=filename,
            file_path=f"archive/{filename}",
            thumbnail_path=str(thumb_path),
            ingested_at=datetime.now(timezone.utc).isoformat(),
            part_number=metadata.get("part_number", ""),
            title=metadata.get("title", filename),
            material=metadata.get("material", "unknown"),
            dimensions=dims,
            processes=tuple(processes),
            tolerances=metadata.get("tolerances", {}),
            surface_finish_ra=float(metadata.get("surface_finish_ra", 0)),
            weight_kg=float(metadata.get("weight_kg", 0)),
            notes=metadata.get("notes", ""),
            historical_costs=tuple(cost.get("historical_costs", [])),
            physics_should_cost_inr=float(cost.get("physics_should_cost_inr", 0)),
            approved_suppliers=tuple(cost.get("approved_suppliers", [])),
            revision=design.get("revision", ""),
            designer=design.get("designer", ""),
            project=design.get("project", ""),
        )

        self._index.add(embedding, record)

    def search(
        self,
        image_bytes: bytes | None = None,
        filename: str = "query.png",
        embedding: np.ndarray | None = None,
        material: str = "",
        dimensions: dict | None = None,
        processes: list[str] | None = None,
        top_k: int = 5,
        faiss_candidates: int = 20,
        weights: RankingWeights | None = None,
    ) -> list[SearchResult]:
        """Search for similar drawings.

        Provide either image_bytes (will be embedded) or a pre-computed embedding.

        Args:
            image_bytes: Raw image bytes to search with
            filename: Filename for format detection
            embedding: Pre-computed 768-dim embedding (alternative to image_bytes)
            material: Material for metadata ranking
            dimensions: Dimensions for metadata ranking
            processes: Processes for metadata ranking
            top_k: Number of final results
            faiss_candidates: Number of FAISS candidates before re-ranking
            weights: Custom ranking weights

        Returns:
            List of SearchResult, sorted by combined score.
        """
        if self._index.count == 0:
            return []

        # Get query embedding
        if embedding is not None:
            query_vec = embedding
        elif image_bytes is not None:
            from engines.similarity.preprocessor import preprocess_drawing
            from engines.similarity.embedder import embed_image
            embed_img, _ = preprocess_drawing(image_bytes, filename)
            query_vec = embed_image(embed_img)
        else:
            raise ValueError("Provide either image_bytes or embedding")

        # FAISS search → top candidates
        candidates = self._index.search(query_vec, top_k=faiss_candidates)

        # Multi-signal re-ranking
        ranked = rank_candidates(
            candidates=candidates,
            query_material=material,
            query_dimensions=dimensions or {},
            query_processes=processes or [],
            top_k=top_k,
            weights=weights,
        )

        # Convert to SearchResult
        results = []
        for i, r in enumerate(ranked):
            m = r.metadata
            results.append(SearchResult(
                rank=i + 1,
                drawing_id=r.drawing_id,
                file_name=m.get("file_name", ""),
                thumbnail_path=m.get("thumbnail_path", ""),
                combined_score=r.combined_score,
                visual_score=r.visual_score,
                material_score=r.material_score,
                dimension_score=r.dimension_score,
                process_score=r.process_score,
                material=m.get("material", ""),
                dimensions=m.get("dimensions", {}),
                processes=tuple(m.get("processes", [])),
                historical_costs=tuple(m.get("historical_costs", [])),
                physics_should_cost_inr=float(m.get("physics_should_cost_inr", 0)),
                part_number=m.get("part_number", ""),
                title=m.get("title", ""),
                revision=m.get("revision", ""),
                designer=m.get("designer", ""),
                project=m.get("project", ""),
                notes=m.get("notes", ""),
            ))

        return results

    def save(self) -> None:
        """Persist the index to disk."""
        self._index.save()

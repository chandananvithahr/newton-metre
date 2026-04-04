"""SimilarityAgent — wraps engines/similarity with a uniform agent interface.

Finds similar drawings from the company's indexed library using visual
embeddings + metadata ranking.
"""
import logging
import time

from agents.types import AgentResult, WorkflowContext

logger = logging.getLogger("agents.similarity")


class SimilarityAgent:
    """Searches for similar drawings using the existing similarity pipeline."""

    @property
    def name(self) -> str:
        return "similarity"

    def validate_inputs(self, inputs: dict) -> tuple[bool, str]:
        has_image = "image_bytes" in inputs or "file_bytes" in inputs
        has_extraction = "extraction" in inputs
        if not (has_image or has_extraction):
            return False, "Need 'image_bytes'/'file_bytes' or 'extraction' data"
        return True, ""

    def execute(self, context: WorkflowContext, inputs: dict) -> AgentResult:
        start = time.perf_counter()

        try:
            matches = self._search(inputs)
        except Exception as exc:
            logger.exception("Similarity search failed")
            return AgentResult(
                agent_name=self.name,
                status="error",
                error=str(exc),
                duration_ms=(time.perf_counter() - start) * 1000,
            )

        elapsed = (time.perf_counter() - start) * 1000
        return AgentResult(
            agent_name=self.name,
            status="success",
            data={
                "matches": matches,
                "match_count": len(matches),
            },
            duration_ms=elapsed,
        )

    def _search(self, inputs: dict) -> list[dict]:
        """Run similarity search using available data."""
        from engines.similarity.searcher import DrawingSearcher

        searcher = DrawingSearcher()
        image_bytes = inputs.get("image_bytes") or inputs.get("file_bytes")
        extraction = inputs.get("extraction", {})

        # Search with whatever data is available
        material = extraction.get("material", "")
        dimensions = extraction.get("dimensions", {})
        processes = extraction.get("processes", [])

        try:
            results = searcher.search(
                image_bytes=image_bytes,
                material=material,
                dimensions=dimensions,
                processes=processes,
                top_k=inputs.get("top_k", 10),
            )
            # Convert to plain dicts for serialization
            return [
                {
                    "drawing_id": r.drawing_id,
                    "score": r.combined_score,
                    "material": getattr(r, "material", ""),
                }
                for r in results
            ]
        except Exception:
            # Similarity search is non-critical — degrade gracefully
            logger.warning("Similarity search unavailable, returning empty")
            return []

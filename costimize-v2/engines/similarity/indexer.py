"""Vector index + JSON metadata store for drawing similarity search.

Two-part storage:
  1. Vector index: stores embedding vectors for fast nearest-neighbor search
  2. JSON metadata sidecar: stores drawing metadata (material, dims, processes, costs)

Uses FAISS if installed (scales to 100K+). Falls back to numpy brute-force for <10K.
"""
import json
from dataclasses import dataclass, asdict
from pathlib import Path

import numpy as np

from engines.similarity.embedder import EMBEDDING_DIM


INDEX_DIR = Path(__file__).parent.parent.parent / "data" / "similarity"
INDEX_DIR.mkdir(parents=True, exist_ok=True)
FAISS_INDEX_PATH = INDEX_DIR / "index.faiss"
METADATA_PATH = INDEX_DIR / "metadata.json"
THUMBNAIL_DIR = INDEX_DIR / "thumbnails"


@dataclass(frozen=True)
class DrawingRecord:
    """Metadata for a single indexed drawing."""
    drawing_id: str
    file_name: str
    file_path: str
    thumbnail_path: str
    ingested_at: str

    # Extracted metadata
    part_number: str
    title: str
    material: str
    dimensions: dict        # {"outer_diameter_mm": 55, "length_mm": 120, ...}
    processes: tuple[str, ...]
    tolerances: dict
    surface_finish_ra: float
    weight_kg: float
    notes: str

    # Cost context
    historical_costs: tuple[dict, ...]  # [{"date", "supplier", "unit_price_inr", "qty"}]
    physics_should_cost_inr: float
    approved_suppliers: tuple[str, ...]

    # Design context
    revision: str
    designer: str
    project: str


def _faiss_available() -> bool:
    """Check if FAISS is installed."""
    try:
        import faiss  # noqa: F401
        return True
    except ImportError:
        return False


class SimilarityIndex:
    """Vector index + metadata store for drawing similarity search.

    Uses FAISS if installed (fastest, scales to 100K+).
    Falls back to numpy brute-force dot product for <10K drawings.

    Usage:
        index = SimilarityIndex()
        index.add(embedding, record)
        results = index.search(query_embedding, top_k=5)
        index.save()
    """

    def __init__(self, index_dir: Path = INDEX_DIR):
        self._index_dir = index_dir
        self._index_dir.mkdir(parents=True, exist_ok=True)
        self._faiss_path = index_dir / "index.faiss"
        self._vectors_path = index_dir / "vectors.npy"
        self._metadata_path = index_dir / "metadata.json"
        self._use_faiss = _faiss_available()
        self._index = None          # FAISS index (if available)
        self._vectors: np.ndarray | None = None  # numpy fallback
        self._metadata: list[dict] = []
        self._load()

    def _load(self):
        """Load existing index and metadata from disk."""
        # Load metadata
        if self._metadata_path.exists():
            try:
                self._metadata = json.loads(
                    self._metadata_path.read_text(encoding="utf-8")
                )
            except (json.JSONDecodeError, FileNotFoundError):
                self._metadata = []

        if self._use_faiss:
            # Load FAISS index
            if self._faiss_path.exists():
                try:
                    import faiss
                    loaded = faiss.read_index(str(self._faiss_path))
                    # Discard old indexes with wrong dimension (e.g. 256 → 768 migration)
                    if loaded.d == EMBEDDING_DIM:
                        self._index = loaded
                    else:
                        self._index = None
                        self._metadata = []  # vectors and metadata are paired
                except Exception:
                    self._index = None
            if self._index is None:
                self._create_new_faiss_index()
        else:
            # Load numpy vectors
            if self._vectors_path.exists():
                try:
                    loaded = np.load(str(self._vectors_path))
                    # Discard old vectors with wrong dimension
                    if loaded.ndim == 2 and loaded.shape[1] == EMBEDDING_DIM:
                        self._vectors = loaded
                    else:
                        self._vectors = None
                        self._metadata = []
                except Exception:
                    self._vectors = None

    def _create_new_faiss_index(self):
        """Create a new FAISS flat index."""
        import faiss
        self._index = faiss.IndexFlatIP(EMBEDDING_DIM)

    @property
    def count(self) -> int:
        """Number of drawings in the index."""
        if self._use_faiss and self._index:
            return self._index.ntotal
        if self._vectors is not None:
            return self._vectors.shape[0]
        return 0

    def add(self, embedding: np.ndarray, record: DrawingRecord) -> None:
        """Add a drawing to the index."""
        if embedding.ndim == 1:
            embedding = embedding.reshape(1, -1)
        embedding = embedding.astype(np.float32)

        if self._use_faiss:
            self._index.add(embedding)
        else:
            if self._vectors is None:
                self._vectors = embedding
            else:
                self._vectors = np.vstack([self._vectors, embedding])

        # Store metadata
        record_dict = asdict(record)
        record_dict["processes"] = list(record_dict["processes"])
        record_dict["historical_costs"] = list(record_dict["historical_costs"])
        record_dict["approved_suppliers"] = list(record_dict["approved_suppliers"])
        self._metadata.append(record_dict)

    def add_batch(self, embeddings: np.ndarray, records: list[DrawingRecord]) -> None:
        """Add multiple drawings to the index at once."""
        embeddings = embeddings.astype(np.float32)
        if embeddings.ndim == 1:
            embeddings = embeddings.reshape(1, -1)

        if self._use_faiss:
            self._index.add(embeddings)
        else:
            if self._vectors is None:
                self._vectors = embeddings
            else:
                self._vectors = np.vstack([self._vectors, embeddings])

        for record in records:
            record_dict = asdict(record)
            record_dict["processes"] = list(record_dict["processes"])
            record_dict["historical_costs"] = list(record_dict["historical_costs"])
            record_dict["approved_suppliers"] = list(record_dict["approved_suppliers"])
            self._metadata.append(record_dict)

    def search(
        self, query_embedding: np.ndarray, top_k: int = 20,
    ) -> list[tuple[dict, float]]:
        """Search for similar drawings.

        Args:
            query_embedding: 768-dim L2-normalized query vector
            top_k: Number of candidates to return

        Returns:
            List of (metadata_dict, similarity_score) tuples, sorted by score descending.
            Score is cosine similarity in [0, 1].
        """
        if self.count == 0:
            return []

        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)
        query_embedding = query_embedding.astype(np.float32)

        k = min(top_k, self.count)

        if self._use_faiss and self._index is not None:
            scores, indices = self._index.search(query_embedding, k)
            results = []
            for score, idx in zip(scores[0], indices[0]):
                if idx < 0 or idx >= len(self._metadata):
                    continue
                results.append((self._metadata[idx], float(score)))
        else:
            # Numpy brute-force: dot product (cosine sim for L2-normalized vectors)
            all_scores = (self._vectors @ query_embedding.T).flatten()
            top_indices = np.argsort(all_scores)[::-1][:k]
            results = []
            for idx in top_indices:
                if idx < len(self._metadata):
                    results.append((self._metadata[idx], float(all_scores[idx])))

        return results

    def get_record(self, drawing_id: str) -> dict | None:
        """Get a specific drawing record by ID."""
        for record in self._metadata:
            if record.get("drawing_id") == drawing_id:
                return record
        return None

    def save(self) -> None:
        """Persist index and metadata to disk."""
        if self._use_faiss and self._index is not None:
            import faiss
            faiss.write_index(self._index, str(self._faiss_path))
        elif self._vectors is not None:
            np.save(str(self._vectors_path), self._vectors)

        self._metadata_path.write_text(
            json.dumps(self._metadata, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def rebuild(self, embeddings: np.ndarray, records: list[DrawingRecord]) -> None:
        """Rebuild the entire index from scratch."""
        if self._use_faiss:
            self._create_new_faiss_index()
        else:
            self._vectors = None
        self._metadata = []
        self.add_batch(embeddings, records)
        self.save()

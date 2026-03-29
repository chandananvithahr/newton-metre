"""Multi-signal ranking for drawing similarity search.

Re-ranks FAISS candidates using 4 weighted signals:
  0.5 × visual_similarity (FAISS cosine score)
  0.2 × material_match (exact=1.0, same_family=0.5, different=0.0)
  0.2 × dimension_closeness (normalized OD + length similarity)
  0.1 × process_overlap (Jaccard similarity of process lists)

Weights are configurable per user role:
  Designer: visual=0.6, material=0.15, dimension=0.15, process=0.1
  Procurement: visual=0.3, material=0.25, dimension=0.25, process=0.2
  QA: visual=0.4, material=0.2, dimension=0.1, process=0.3
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class RankingWeights:
    """Configurable weights for multi-signal ranking."""
    visual: float = 0.5
    material: float = 0.2
    dimension: float = 0.2
    process: float = 0.1


# Preset weights by user role
PRESET_WEIGHTS = {
    "default": RankingWeights(0.5, 0.2, 0.2, 0.1),
    "designer": RankingWeights(0.6, 0.15, 0.15, 0.1),
    "procurement": RankingWeights(0.3, 0.25, 0.25, 0.2),
    "qa": RankingWeights(0.4, 0.2, 0.1, 0.3),
}

# Material family groupings for fuzzy matching
_MATERIAL_FAMILIES = {
    "steel": {"Mild Steel IS2062", "EN8 Steel", "EN24 Steel"},
    "stainless": {"Stainless Steel 304"},
    "aluminum": {"Aluminum 6061"},
    "copper_alloy": {"Brass IS319", "Copper"},
    "cast_iron": {"Cast Iron"},
    "titanium": {"Titanium Grade 5"},
}


def _get_family(material: str) -> str | None:
    """Get material family name, or None if not found."""
    for family, members in _MATERIAL_FAMILIES.items():
        if material in members:
            return family
    return None


def compute_material_score(query_material: str, candidate_material: str) -> float:
    """Material match score: exact=1.0, same_family=0.5, different=0.0."""
    if query_material == candidate_material:
        return 1.0
    q_family = _get_family(query_material)
    c_family = _get_family(candidate_material)
    if q_family and q_family == c_family:
        return 0.5
    return 0.0


def compute_dimension_score(query_dims: dict, candidate_dims: dict) -> float:
    """Dimension closeness: average of normalized OD and length similarity.

    dim_sim = 1 - |d1 - d2| / max(d1, d2)
    Returns 0-1 where 1 = identical dimensions.
    """
    scores = []
    for key in ("outer_diameter_mm", "length_mm"):
        q_val = query_dims.get(key, 0)
        c_val = candidate_dims.get(key, 0)
        if q_val > 0 and c_val > 0:
            denom = max(q_val, c_val)
            scores.append(1.0 - abs(q_val - c_val) / denom)
        elif q_val == 0 and c_val == 0:
            scores.append(1.0)  # both zero = match
        else:
            scores.append(0.0)  # one zero, one not = mismatch

    return sum(scores) / len(scores) if scores else 0.0


def compute_process_score(query_processes: set[str], candidate_processes: set[str]) -> float:
    """Process overlap: Jaccard similarity = |intersection| / |union|."""
    if not query_processes and not candidate_processes:
        return 1.0
    if not query_processes or not candidate_processes:
        return 0.0
    intersection = query_processes & candidate_processes
    union = query_processes | candidate_processes
    return len(intersection) / len(union)


@dataclass(frozen=True)
class RankedResult:
    """A search result with full scoring breakdown."""
    drawing_id: str
    metadata: dict
    visual_score: float
    material_score: float
    dimension_score: float
    process_score: float
    combined_score: float


def rank_candidates(
    candidates: list[tuple[dict, float]],
    query_material: str,
    query_dimensions: dict,
    query_processes: list[str],
    top_k: int = 5,
    weights: RankingWeights | None = None,
) -> list[RankedResult]:
    """Re-rank FAISS candidates using multi-signal scoring.

    Args:
        candidates: List of (metadata_dict, visual_score) from FAISS search
        query_material: Material of query drawing
        query_dimensions: Dimensions dict of query drawing
        query_processes: Process list of query drawing
        top_k: Number of final results to return
        weights: Ranking weights (default: balanced)

    Returns:
        Top-K results sorted by combined score, with full breakdown.
    """
    w = weights or PRESET_WEIGHTS["default"]
    query_proc_set = set(query_processes)
    scored = []

    for metadata, visual_sim in candidates:
        cand_material = metadata.get("material", "")
        cand_dims = metadata.get("dimensions", {})
        cand_processes = set(metadata.get("processes", []))

        mat_score = compute_material_score(query_material, cand_material)
        dim_score = compute_dimension_score(query_dimensions, cand_dims)
        proc_score = compute_process_score(query_proc_set, cand_processes)

        combined = (
            w.visual * visual_sim
            + w.material * mat_score
            + w.dimension * dim_score
            + w.process * proc_score
        )

        scored.append(RankedResult(
            drawing_id=metadata.get("drawing_id", ""),
            metadata=metadata,
            visual_score=round(visual_sim, 4),
            material_score=round(mat_score, 4),
            dimension_score=round(dim_score, 4),
            process_score=round(proc_score, 4),
            combined_score=round(combined, 4),
        ))

    scored.sort(key=lambda r: r.combined_score, reverse=True)
    return scored[:top_k]

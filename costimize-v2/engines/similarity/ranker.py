"""Multi-signal ranking for drawing similarity search.

Re-ranks FAISS candidates using 6 weighted signals:
  0.40 × visual_similarity (FAISS cosine score)
  0.15 × material_match (exact=1.0, same_family=0.5, different=0.0)
  0.20 × dimension_closeness (normalized similarity across all dimension keys)
  0.10 × process_overlap (Jaccard similarity of process lists)
  0.10 × tolerance_closeness (normalized tolerance grade similarity)
  0.05 × surface_finish_match (normalized Ra value similarity)

Weights are configurable per user role:
  Designer: visual=0.45, material=0.10, dimension=0.20, process=0.10, tolerance=0.10, finish=0.05
  Procurement: visual=0.25, material=0.20, dimension=0.20, process=0.15, tolerance=0.10, finish=0.10
  QA: visual=0.30, material=0.15, dimension=0.10, process=0.25, tolerance=0.10, finish=0.10
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class RankingWeights:
    """Configurable weights for multi-signal ranking."""
    visual: float = 0.40
    material: float = 0.15
    dimension: float = 0.20
    process: float = 0.10
    tolerance: float = 0.10
    finish: float = 0.05


# Preset weights by user role
PRESET_WEIGHTS = {
    "default": RankingWeights(0.40, 0.15, 0.20, 0.10, 0.10, 0.05),
    "designer": RankingWeights(0.45, 0.10, 0.20, 0.10, 0.10, 0.05),
    "procurement": RankingWeights(0.25, 0.20, 0.20, 0.15, 0.10, 0.10),
    "qa": RankingWeights(0.30, 0.15, 0.10, 0.25, 0.10, 0.10),
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

# Dimension keys to check (covers both mechanical and sheet metal parts)
_DIMENSION_KEYS = (
    "outer_diameter_mm",
    "length_mm",
    "width_mm",
    "height_mm",
    "thickness_mm",
    "inner_diameter_mm",
)


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
    """Dimension closeness: average normalized similarity across all dimension keys.

    dim_sim = 1 - |d1 - d2| / max(d1, d2)
    Returns 0-1 where 1 = identical dimensions.
    """
    scores = []
    for key in _DIMENSION_KEYS:
        q_val = query_dims.get(key, 0)
        c_val = candidate_dims.get(key, 0)
        if q_val > 0 and c_val > 0:
            denom = max(q_val, c_val)
            scores.append(1.0 - abs(q_val - c_val) / denom)
        elif q_val == 0 and c_val == 0:
            continue  # both missing = skip (don't penalize or reward)
        else:
            scores.append(0.0)  # one zero, one not = mismatch

    return sum(scores) / len(scores) if scores else 0.5  # no dims = neutral


def compute_process_score(query_processes: set[str], candidate_processes: set[str]) -> float:
    """Process overlap: Jaccard similarity = |intersection| / |union|."""
    if not query_processes and not candidate_processes:
        return 1.0
    if not query_processes or not candidate_processes:
        return 0.0
    intersection = query_processes & candidate_processes
    union = query_processes | candidate_processes
    return len(intersection) / len(union)


def compute_tolerance_score(query_tolerances: dict, candidate_tolerances: dict) -> float:
    """Tolerance closeness: compare general tolerance grades or specific values.

    Handles:
    - "general_tolerance_mm": normalized difference
    - "tightest_tolerance_mm": normalized difference
    Returns 0-1 where 1 = identical tolerance requirements.
    """
    scores = []
    for key in ("general_tolerance_mm", "tightest_tolerance_mm"):
        q_val = query_tolerances.get(key, 0)
        c_val = candidate_tolerances.get(key, 0)
        if q_val > 0 and c_val > 0:
            denom = max(q_val, c_val)
            scores.append(1.0 - abs(q_val - c_val) / denom)
        elif q_val == 0 and c_val == 0:
            continue
        else:
            scores.append(0.0)

    return sum(scores) / len(scores) if scores else 0.5  # no tolerances = neutral


def compute_finish_score(query_ra: float, candidate_ra: float) -> float:
    """Surface finish closeness: normalized Ra value similarity.

    finish_sim = 1 - |Ra1 - Ra2| / max(Ra1, Ra2)
    Returns 0-1 where 1 = identical finish.
    """
    if query_ra > 0 and candidate_ra > 0:
        denom = max(query_ra, candidate_ra)
        return 1.0 - abs(query_ra - candidate_ra) / denom
    if query_ra == 0 and candidate_ra == 0:
        return 0.5  # both unknown = neutral
    return 0.0  # one specified, one not = mismatch


@dataclass(frozen=True)
class RankedResult:
    """A search result with full scoring breakdown."""
    drawing_id: str
    metadata: dict
    visual_score: float
    material_score: float
    dimension_score: float
    process_score: float
    tolerance_score: float
    finish_score: float
    combined_score: float


def rank_candidates(
    candidates: list[tuple[dict, float]],
    query_material: str,
    query_dimensions: dict,
    query_processes: list[str],
    query_tolerances: dict | None = None,
    query_surface_finish_ra: float = 0.0,
    top_k: int = 5,
    weights: RankingWeights | None = None,
) -> list[RankedResult]:
    """Re-rank FAISS candidates using multi-signal scoring.

    Args:
        candidates: List of (metadata_dict, visual_score) from FAISS search
        query_material: Material of query drawing
        query_dimensions: Dimensions dict of query drawing
        query_processes: Process list of query drawing
        query_tolerances: Tolerance dict (general_tolerance_mm, tightest_tolerance_mm)
        query_surface_finish_ra: Surface roughness Ra value in microns
        top_k: Number of final results to return
        weights: Ranking weights (default: balanced)

    Returns:
        Top-K results sorted by combined score, with full breakdown.
    """
    w = weights or PRESET_WEIGHTS["default"]
    query_proc_set = set(query_processes)
    query_tol = query_tolerances or {}
    scored = []

    for metadata, visual_sim in candidates:
        cand_material = metadata.get("material", "")
        cand_dims = metadata.get("dimensions", {})
        cand_processes = set(metadata.get("processes", []))
        cand_tolerances = metadata.get("tolerances", {})
        cand_ra = metadata.get("surface_finish_ra", 0.0)

        mat_score = compute_material_score(query_material, cand_material)
        dim_score = compute_dimension_score(query_dimensions, cand_dims)
        proc_score = compute_process_score(query_proc_set, cand_processes)
        tol_score = compute_tolerance_score(query_tol, cand_tolerances)
        fin_score = compute_finish_score(query_surface_finish_ra, cand_ra)

        combined = (
            w.visual * visual_sim
            + w.material * mat_score
            + w.dimension * dim_score
            + w.process * proc_score
            + w.tolerance * tol_score
            + w.finish * fin_score
        )

        scored.append(RankedResult(
            drawing_id=metadata.get("drawing_id", ""),
            metadata=metadata,
            visual_score=round(visual_sim, 4),
            material_score=round(mat_score, 4),
            dimension_score=round(dim_score, 4),
            process_score=round(proc_score, 4),
            tolerance_score=round(tol_score, 4),
            finish_score=round(fin_score, 4),
            combined_score=round(combined, 4),
        ))

    scored.sort(key=lambda r: r.combined_score, reverse=True)
    return scored[:top_k]

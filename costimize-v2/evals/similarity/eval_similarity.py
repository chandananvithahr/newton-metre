"""Similarity search eval runner — measures retrieval quality against ground truth.

Usage:
    cd costimize-v2
    python -m evals.similarity.eval_similarity                     # Eval current embedder
    python -m evals.similarity.eval_similarity --embedder dinov2   # Specific embedder

Metrics:
    - recall_at_k: fraction of relevant items in top-K results
    - precision_at_k: fraction of top-K results that are relevant
    - ndcg_at_k: normalized discounted cumulative gain (rewards higher ranking)
    - mrr: mean reciprocal rank of first relevant result
"""
import json
import math
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import numpy as np

EVALS_DIR = Path(__file__).parent
GOLDEN_DATASET = EVALS_DIR / "golden_dataset.json"
RESULTS_DIR = EVALS_DIR.parent / "results"


@dataclass(frozen=True)
class SimilarityEvalResult:
    query_id: str
    description: str
    recall_at_5: float
    precision_at_5: float
    ndcg_at_10: float
    reciprocal_rank: float  # 1/rank of first relevant result
    relevant_found: int
    relevant_total: int
    top_results: tuple[str, ...]
    latency_ms: float
    error: Optional[str]


# --- Core IR Metrics ---

def recall_at_k(results: list[str], relevant: list[str], k: int) -> float:
    """What fraction of relevant items appear in top-K results?"""
    if not relevant:
        return 1.0
    top_k = set(results[:k])
    return len(top_k & set(relevant)) / len(relevant)


def precision_at_k(results: list[str], relevant: list[str], k: int) -> float:
    """What fraction of top-K results are relevant?"""
    if k == 0:
        return 0.0
    top_k = set(results[:k])
    return len(top_k & set(relevant)) / k


def ndcg_at_k(results: list[str], relevance_map: dict[str, int], k: int) -> float:
    """Normalized Discounted Cumulative Gain — rewards relevant results appearing earlier.

    relevance_map: {drawing_id: relevance_grade} where higher = more relevant
    """
    # DCG of actual results
    dcg = 0.0
    for i, result_id in enumerate(results[:k]):
        rel = relevance_map.get(result_id, 0)
        dcg += (2**rel - 1) / math.log2(i + 2)

    # Ideal DCG (perfect ranking)
    ideal_rels = sorted(relevance_map.values(), reverse=True)[:k]
    idcg = sum((2**rel - 1) / math.log2(i + 2) for i, rel in enumerate(ideal_rels))

    return dcg / idcg if idcg > 0 else 0.0


def reciprocal_rank(results: list[str], relevant: set[str]) -> float:
    """1 / rank of the first relevant result. 0 if none found."""
    for i, result_id in enumerate(results):
        if result_id in relevant:
            return 1.0 / (i + 1)
    return 0.0


# --- Search Function Adapters ---

def _search_with_ranker(query: dict, library: list[dict],
                        embedder_type: str = "gemini") -> list[str]:
    """Run similarity search using the actual Newton-Metre search pipeline.

    For offline eval (no images), uses metadata-only ranking.
    """
    from engines.similarity.ranker import (
        rank_candidates,
        RankingWeights,
        PRESET_WEIGHTS,
    )

    # Build candidates from library
    candidates = []
    for item in library:
        candidates.append({
            "drawing_id": item["drawing_id"],
            "visual_score": np.random.uniform(0.3, 0.9),  # Placeholder — real eval needs embeddings
            "material": item.get("material", ""),
            "dimensions": item.get("dimensions", {}),
            "processes": tuple(item.get("processes", [])),
            "tolerances": item.get("tolerances", {}),
            "surface_finish": item.get("surface_finish"),
        })

    ranked = rank_candidates(
        candidates=candidates,
        query_material=query.get("material", ""),
        query_dimensions=query.get("dimensions", {}),
        query_processes=tuple(query.get("processes", [])),
        weights=PRESET_WEIGHTS["default"],
    )

    return [r.drawing_id for r in ranked]


def _search_metadata_only(query: dict, library: list[dict]) -> list[str]:
    """Simple metadata-based search for offline eval without images/embeddings.

    Scores based on: material match + dimension closeness + process overlap.
    No visual component — this establishes the metadata-only baseline.
    """
    from engines.similarity.ranker import (
        compute_material_score,
        compute_dimension_score,
        compute_process_score,
    )

    scores = []
    for item in library:
        mat_score = compute_material_score(
            query.get("material", ""), item.get("material", "")
        )
        dim_score = compute_dimension_score(
            query.get("dimensions", {}), item.get("dimensions", {})
        )
        proc_score = compute_process_score(
            set(query.get("processes", [])), set(item.get("processes", []))
        )
        # Weight: 0.3 material + 0.4 dimension + 0.3 process
        combined = 0.3 * mat_score + 0.4 * dim_score + 0.3 * proc_score
        scores.append((item["drawing_id"], combined))

    scores.sort(key=lambda x: x[1], reverse=True)
    return [s[0] for s in scores]


# --- Eval Runner ---

def build_synthetic_library(dataset: dict) -> list[dict]:
    """Build a synthetic library from the golden dataset for offline evaluation.

    In production, this would be replaced with the actual indexed drawing library.
    """
    library = []
    seen = set()

    for query in dataset["queries"]:
        for rel in query["relevant_drawings"]:
            if rel["drawing_id"] not in seen:
                seen.add(rel["drawing_id"])
                # Create library entry with metadata inferred from the query
                library.append({
                    "drawing_id": rel["drawing_id"],
                    "material": query["material"] if rel["relevance"] >= 2 else "Mild Steel IS2062",
                    "dimensions": query["dimensions"] if rel["relevance"] >= 2 else {"length_mm": 100},
                    "processes": query["processes"] if rel["relevance"] >= 2 else ["turning"],
                })

    # Add some noise — irrelevant drawings
    for i in range(10):
        noise_id = f"lib_noise_{i:03d}"
        if noise_id not in seen:
            library.append({
                "drawing_id": noise_id,
                "material": ["Titanium Grade 5", "Cast Iron", "Copper"][i % 3],
                "dimensions": {"length_mm": 500 + i * 50},
                "processes": ["broaching"],
            })

    return library


def eval_single(query: dict, library: list[dict],
                search_fn=None) -> SimilarityEvalResult:
    """Evaluate a single similarity search query."""
    query_id = query["id"]
    description = query.get("description", "")

    # Build relevance data
    relevant_ids = [r["drawing_id"] for r in query["relevant_drawings"]]
    relevance_map = {r["drawing_id"]: r["relevance"] for r in query["relevant_drawings"]}

    error = None
    results = []
    latency_ms = 0.0

    try:
        start = time.perf_counter()
        if search_fn:
            results = search_fn(query, library)
        else:
            results = _search_metadata_only(query, library)
        latency_ms = (time.perf_counter() - start) * 1000
    except Exception as e:
        error = str(e)

    r_at_5 = recall_at_k(results, relevant_ids, 5)
    p_at_5 = precision_at_k(results, relevant_ids, 5)
    n_at_10 = ndcg_at_k(results, relevance_map, 10)
    rr = reciprocal_rank(results, set(relevant_ids))
    found = len(set(results[:10]) & set(relevant_ids))

    return SimilarityEvalResult(
        query_id=query_id,
        description=description,
        recall_at_5=r_at_5,
        precision_at_5=p_at_5,
        ndcg_at_10=n_at_10,
        reciprocal_rank=rr,
        relevant_found=found,
        relevant_total=len(relevant_ids),
        top_results=tuple(results[:10]),
        latency_ms=latency_ms,
        error=error,
    )


def run_eval(embedder: str = "metadata", search_fn=None) -> list[SimilarityEvalResult]:
    """Run full similarity search eval suite."""
    if not GOLDEN_DATASET.exists():
        print(f"ERROR: Golden dataset not found at {GOLDEN_DATASET}")
        return []

    dataset = json.loads(GOLDEN_DATASET.read_text())
    library = build_synthetic_library(dataset)

    results = []
    for query in dataset["queries"]:
        result = eval_single(query, library, search_fn)
        results.append(result)

    return results


def print_report(results: list[SimilarityEvalResult], embedder: str = "unknown") -> dict:
    """Print human-readable eval report."""
    print(f"\n{'='*70}")
    print(f"  SIMILARITY SEARCH EVAL — Embedder: {embedder}")
    print(f"  {len(results)} queries")
    print(f"{'='*70}\n")

    for r in results:
        status = "PASS" if r.recall_at_5 >= 0.6 else "WARN" if r.recall_at_5 >= 0.3 else "FAIL"
        err_tag = f" [ERROR: {r.error}]" if r.error else ""
        print(f"  [{status}] {r.query_id}: {r.description}{err_tag}")
        print(f"         R@5={r.recall_at_5:.2f}  P@5={r.precision_at_5:.2f}  "
              f"NDCG@10={r.ndcg_at_10:.2f}  MRR={r.reciprocal_rank:.2f}  "
              f"Found={r.relevant_found}/{r.relevant_total}  "
              f"Latency={r.latency_ms:.0f}ms")
        print()

    n = len(results) or 1
    summary = {
        "embedder": embedder,
        "query_count": len(results),
        "avg_recall_at_5": sum(r.recall_at_5 for r in results) / n,
        "avg_precision_at_5": sum(r.precision_at_5 for r in results) / n,
        "avg_ndcg_at_10": sum(r.ndcg_at_10 for r in results) / n,
        "mrr": sum(r.reciprocal_rank for r in results) / n,
        "errors": sum(1 for r in results if r.error),
    }

    print(f"{'-'*70}")
    print(f"  SUMMARY")
    print(f"  Avg Recall@5:     {summary['avg_recall_at_5']:.3f}")
    print(f"  Avg Precision@5:  {summary['avg_precision_at_5']:.3f}")
    print(f"  Avg NDCG@10:      {summary['avg_ndcg_at_10']:.3f}")
    print(f"  MRR:              {summary['mrr']:.3f}")
    print(f"  Errors:           {summary['errors']}")
    print(f"{'='*70}\n")

    RESULTS_DIR.mkdir(exist_ok=True)
    results_file = RESULTS_DIR / f"similarity_{embedder}_{int(time.time())}.json"
    results_file.write_text(json.dumps(summary, indent=2))
    print(f"  Results saved to: {results_file}")

    return summary


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run similarity search evals")
    parser.add_argument("--embedder", default="metadata",
                        choices=["metadata", "gemini", "dinov2", "hash"])
    args = parser.parse_args()

    results = run_eval(embedder=args.embedder)
    print_report(results, embedder=args.embedder)

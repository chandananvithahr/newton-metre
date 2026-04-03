"""Extraction eval runner — measures AI extraction quality against golden dataset.

Usage:
    cd costimize-v2
    python -m evals.extraction.eval_extraction                    # Eval current cloud API
    python -m evals.extraction.eval_extraction --provider gemini  # Specific provider
    python -m evals.extraction.eval_extraction --provider local   # Self-hosted model

Metrics:
    - field_accuracy: correct fields / total fields per drawing
    - material_accuracy: exact match on material field
    - dimension_accuracy: within tolerance of ground truth
    - process_f1: F1 score on suggested_processes
    - schema_compliance: does output match expected JSON structure
"""
import json
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

EVALS_DIR = Path(__file__).parent
GOLDEN_DATASET = EVALS_DIR / "golden_dataset.json"
RESULTS_DIR = EVALS_DIR.parent / "results"


@dataclass(frozen=True)
class FieldResult:
    field: str
    expected: object
    actual: object
    correct: bool
    detail: str


@dataclass(frozen=True)
class ExtractionEvalResult:
    test_id: str
    description: str
    field_accuracy: float
    material_correct: bool
    part_type_correct: bool
    dimension_accuracy: float
    process_precision: float
    process_recall: float
    process_f1: float
    tolerance_correct: bool
    schema_valid: bool
    field_details: tuple[FieldResult, ...]
    latency_ms: float
    error: Optional[str]


def _compare_dimension(expected: Optional[float], actual: Optional[float],
                       tolerance_pct: float = 10.0) -> bool:
    """Compare dimensions within tolerance. Both null = match."""
    if expected is None and actual is None:
        return True
    if expected is None or actual is None:
        return False
    if expected == 0:
        return actual == 0
    return abs(actual - expected) / abs(expected) * 100 <= tolerance_pct


def _process_f1(expected: list[str], actual: list[str]) -> tuple[float, float, float]:
    """Compute precision, recall, F1 for process lists."""
    expected_set = set(expected)
    actual_set = set(actual)
    if not expected_set and not actual_set:
        return 1.0, 1.0, 1.0
    if not expected_set or not actual_set:
        return 0.0, 0.0, 0.0
    tp = len(expected_set & actual_set)
    precision = tp / len(actual_set) if actual_set else 0.0
    recall = tp / len(expected_set) if expected_set else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    return precision, recall, f1


def _normalize_material(material: Optional[str]) -> str:
    """Normalize material names for comparison."""
    if material is None:
        return ""
    return material.lower().strip().replace("-", "").replace(" ", "")


def eval_single(test_case: dict, extract_fn) -> ExtractionEvalResult:
    """Evaluate a single extraction against ground truth."""
    expected = test_case["expected"]
    test_id = test_case["id"]
    description = test_case.get("description", "")

    # Check if image file exists — if not, use a synthetic extraction call
    image_path = EVALS_DIR / test_case.get("image_file", "")
    error = None
    actual = None
    latency_ms = 0.0

    try:
        if image_path.exists():
            image_bytes = image_path.read_bytes()
            start = time.perf_counter()
            actual = extract_fn(image_bytes)
            latency_ms = (time.perf_counter() - start) * 1000
        else:
            # No image — skip live extraction, use for offline eval with pre-computed results
            error = f"Image not found: {test_case.get('image_file', 'none')}. Add drawing to golden/ dir."
            actual = {}
    except Exception as e:
        error = str(e)
        actual = {}

    # --- Compare fields ---
    field_results = []

    # Part type
    pt_correct = actual.get("part_type") == expected.get("part_type")
    field_results.append(FieldResult("part_type", expected.get("part_type"),
                                     actual.get("part_type"), pt_correct, ""))

    # Material (normalized comparison)
    exp_mat = _normalize_material(expected.get("material"))
    act_mat = _normalize_material(actual.get("material"))
    mat_correct = exp_mat == act_mat or (exp_mat and exp_mat in act_mat) or (act_mat and act_mat in exp_mat)
    field_results.append(FieldResult("material", expected.get("material"),
                                     actual.get("material"), mat_correct, ""))

    # Dimensions
    exp_dims = expected.get("dimensions", {})
    act_dims = actual.get("dimensions", {})
    dim_correct = 0
    dim_total = 0
    for key in exp_dims:
        exp_val = exp_dims.get(key)
        act_val = act_dims.get(key)
        if exp_val is not None:  # Only count fields that have expected values
            dim_total += 1
            is_correct = _compare_dimension(exp_val, act_val)
            if is_correct:
                dim_correct += 1
            field_results.append(FieldResult(
                f"dimensions.{key}", exp_val, act_val, is_correct,
                f"{'OK' if is_correct else 'MISMATCH'}"
            ))
    dim_accuracy = dim_correct / dim_total if dim_total > 0 else 1.0

    # Processes
    exp_processes = expected.get("suggested_processes", [])
    act_processes = actual.get("suggested_processes", [])
    precision, recall, f1 = _process_f1(exp_processes, act_processes)

    # Tolerances
    exp_tol = expected.get("tolerances", {})
    act_tol = actual.get("tolerances", {})
    tol_correct = (
        exp_tol.get("has_tight_tolerances") == act_tol.get("has_tight_tolerances")
    )

    # Schema validity
    required_keys = {"part_type", "dimensions", "material", "tolerances",
                     "suggested_processes", "confidence"}
    schema_valid = required_keys.issubset(set(actual.keys())) if actual else False

    # Overall field accuracy
    correct_count = sum(1 for fr in field_results if fr.correct)
    total_fields = len(field_results)
    field_accuracy = correct_count / total_fields if total_fields > 0 else 0.0

    return ExtractionEvalResult(
        test_id=test_id,
        description=description,
        field_accuracy=field_accuracy,
        material_correct=mat_correct,
        part_type_correct=pt_correct,
        dimension_accuracy=dim_accuracy,
        process_precision=precision,
        process_recall=recall,
        process_f1=f1,
        tolerance_correct=tol_correct,
        schema_valid=schema_valid,
        field_details=tuple(field_results),
        latency_ms=latency_ms,
        error=error,
    )


def run_eval(extract_fn=None, provider: str = "gemini") -> list[ExtractionEvalResult]:
    """Run full extraction eval suite against golden dataset."""
    if not GOLDEN_DATASET.exists():
        print(f"ERROR: Golden dataset not found at {GOLDEN_DATASET}")
        return []

    dataset = json.loads(GOLDEN_DATASET.read_text())

    if extract_fn is None:
        # Import the actual extraction function
        sys.path.insert(0, str(Path(__file__).parent.parent.parent))
        from extractors.vision import analyze_drawing
        extract_fn = analyze_drawing

    results = []
    for test_case in dataset:
        result = eval_single(test_case, extract_fn)
        results.append(result)

    return results


def print_report(results: list[ExtractionEvalResult], provider: str = "unknown") -> dict:
    """Print human-readable eval report and return summary dict."""
    print(f"\n{'='*70}")
    print(f"  EXTRACTION EVAL REPORT — Provider: {provider}")
    print(f"  {len(results)} test cases")
    print(f"{'='*70}\n")

    total_field_acc = 0.0
    total_dim_acc = 0.0
    total_process_f1 = 0.0
    material_correct = 0
    part_type_correct = 0
    schema_valid = 0
    errors = 0

    for r in results:
        status = "PASS" if r.field_accuracy >= 0.8 else "WARN" if r.field_accuracy >= 0.5 else "FAIL"
        err_tag = f" [ERROR: {r.error}]" if r.error else ""
        print(f"  [{status}] {r.test_id}: {r.description}{err_tag}")
        print(f"         Field Accuracy: {r.field_accuracy:.0%}  |  "
              f"Dimensions: {r.dimension_accuracy:.0%}  |  "
              f"Process F1: {r.process_f1:.0%}  |  "
              f"Material: {'OK' if r.material_correct else 'MISS'}  |  "
              f"Latency: {r.latency_ms:.0f}ms")

        if r.field_details:
            failures = [fd for fd in r.field_details if not fd.correct]
            for fd in failures:
                print(f"           MISS: {fd.field} — expected={fd.expected}, got={fd.actual}")

        print()
        total_field_acc += r.field_accuracy
        total_dim_acc += r.dimension_accuracy
        total_process_f1 += r.process_f1
        if r.material_correct:
            material_correct += 1
        if r.part_type_correct:
            part_type_correct += 1
        if r.schema_valid:
            schema_valid += 1
        if r.error:
            errors += 1

    n = len(results) or 1
    summary = {
        "provider": provider,
        "test_count": len(results),
        "avg_field_accuracy": total_field_acc / n,
        "avg_dimension_accuracy": total_dim_acc / n,
        "avg_process_f1": total_process_f1 / n,
        "material_accuracy": material_correct / n,
        "part_type_accuracy": part_type_correct / n,
        "schema_compliance": schema_valid / n,
        "errors": errors,
    }

    print(f"{'-'*70}")
    print(f"  SUMMARY")
    print(f"  Avg Field Accuracy:     {summary['avg_field_accuracy']:.1%}")
    print(f"  Avg Dimension Accuracy: {summary['avg_dimension_accuracy']:.1%}")
    print(f"  Avg Process F1:         {summary['avg_process_f1']:.1%}")
    print(f"  Material Accuracy:      {summary['material_accuracy']:.1%}")
    print(f"  Part Type Accuracy:     {summary['part_type_accuracy']:.1%}")
    print(f"  Schema Compliance:      {summary['schema_compliance']:.1%}")
    print(f"  Errors:                 {summary['errors']}")
    print(f"{'='*70}\n")

    # Save results
    RESULTS_DIR.mkdir(exist_ok=True)
    results_file = RESULTS_DIR / f"extraction_{provider}_{int(time.time())}.json"
    results_file.write_text(json.dumps(summary, indent=2))
    print(f"  Results saved to: {results_file}")

    return summary


def compare_providers(provider_results: dict[str, dict]) -> None:
    """Side-by-side comparison of multiple providers."""
    print(f"\n{'='*70}")
    print(f"  PROVIDER COMPARISON")
    print(f"{'='*70}\n")

    metrics = ["avg_field_accuracy", "avg_dimension_accuracy", "avg_process_f1",
               "material_accuracy", "part_type_accuracy", "schema_compliance"]

    header = f"  {'Metric':<28}" + "".join(f"{p:>14}" for p in provider_results.keys())
    print(header)
    print(f"  {'-'*28}" + "-" * 14 * len(provider_results))

    for metric in metrics:
        label = metric.replace("avg_", "").replace("_", " ").title()
        values = "".join(
            f"{provider_results[p].get(metric, 0):.1%}".rjust(14)
            for p in provider_results
        )
        # Highlight winner
        best = max(provider_results[p].get(metric, 0) for p in provider_results)
        print(f"  {label:<28}{values}")

    print()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run extraction evals")
    parser.add_argument("--provider", default="gemini", choices=["gemini", "openai", "local"],
                        help="Which provider to evaluate")
    parser.add_argument("--compare", action="store_true",
                        help="Compare all available result files")
    args = parser.parse_args()

    if args.compare:
        # Load all saved results and compare
        results_files = sorted(RESULTS_DIR.glob("extraction_*.json"))
        if not results_files:
            print("No results files found. Run evals first.")
            sys.exit(1)
        provider_results = {}
        for f in results_files:
            data = json.loads(f.read_text())
            provider_results[data["provider"]] = data
        compare_providers(provider_results)
    else:
        results = run_eval(provider=args.provider)
        print_report(results, provider=args.provider)

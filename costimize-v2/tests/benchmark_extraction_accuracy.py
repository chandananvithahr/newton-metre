"""
Extraction Accuracy Benchmark
==============================
Compares what the Newton-Metre AI extractor returns vs DXF ground truth.

Ground truths are from ezdxf vector parsing (objective — not AI opinion).
AI extractor uses Gemini/GPT-4o (via production API or direct call).

Usage:
  # Run directly (uses extractor locally — needs GEMINI_API_KEY or OPENAI_API_KEY):
  python tests/benchmark_extraction_accuracy.py

  # Run against production API (needs Supabase JWT):
  TEST_JWT=<bearer_token> python tests/benchmark_extraction_accuracy.py --api

Output:
  Console table: field | ground_truth | ai_result | delta | PASS/FAIL
  Exit code 0 if all critical fields pass, 1 otherwise.
"""
import sys
import os
import json
import math
import argparse
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

# ── Ground truths — from ezdxf vector parsing, NOT AI ─────────────────────────
GROUND_TRUTHS = {
    "stepped_shaft.dxf": {
        "description": "Stepped turned shaft, 3 diameters (D50/D35/D25), EN8 steel",
        "file": Path(__file__).parent.parent.parent / "test-files/dxf/stepped_shaft.dxf",
        "format": "dxf",
        "expected": {
            "outer_diameter_mm": 50.0,
            "length_mm": 40.0,
            "material": "EN8",           # substring match
            "has_tight_tolerances": True,
            "processes_contains": ["turning"],
            "confidence_not": ["failed"],
        },
        "tolerances": {
            "outer_diameter_mm": 0.10,    # ±10%
            "length_mm": 0.10,
        },
    },
    "flange_plate.dxf": {
        "description": "Flange plate, sheet-metal / milled part",
        "file": Path(__file__).parent.parent.parent / "test-files/dxf/flange_plate.dxf",
        "format": "dxf",
        "expected": {
            "confidence_not": ["failed"],
            "processes_contains_any": ["milling_face", "drilling", "milling_slot", "boring"],
            "has_dimensions": True,       # at least one non-zero dimension
        },
    },
    "stepped_shaft.stp": {
        "description": "Same stepped shaft as STEP export",
        "file": Path(__file__).parent.parent.parent / "test-files/step/stepped_shaft.stp",
        "format": "step",
        "expected": {
            "outer_diameter_mm_gt": 0,    # just verify > 0
            "confidence_not": ["failed"],
            "processes_not_empty": True,
        },
    },
}

COL = {
    "PASS": "\033[92m✓ PASS\033[0m",
    "FAIL": "\033[91m✗ FAIL\033[0m",
    "WARN": "\033[93m~ WARN\033[0m",
}


def _extract_local(file_path: Path, fmt: str) -> dict:
    """Run extractor locally — needs GEMINI_API_KEY or OPENAI_API_KEY."""
    from extractors.cad_converter import dxf_to_text, step_to_text, is_dxf_dwg, is_step
    from extractors.vision import analyze_step_text, analyze_drawing

    raw = file_path.read_bytes()
    filename = file_path.name

    if fmt == "dxf":
        cad_text = dxf_to_text(raw, filename)
        return analyze_step_text(cad_text)
    elif fmt == "step":
        cad_text = step_to_text(raw)
        return analyze_step_text(cad_text)
    else:
        return analyze_drawing(raw, filename)


def _extract_api(file_path: Path, jwt: str) -> dict:
    """Run extractor via production API — needs JWT."""
    import urllib.request
    import urllib.parse

    boundary = "----FormBoundary7MA4YWxkTrZu0gW"
    file_bytes = file_path.read_bytes()
    filename = file_path.name

    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
        f"Content-Type: application/octet-stream\r\n\r\n"
    ).encode() + file_bytes + f"\r\n--{boundary}--\r\n".encode()

    req = urllib.request.Request(
        "https://costimize-api-production.up.railway.app/api/extract",
        data=body,
        headers={
            "Authorization": f"Bearer {jwt}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read())


def _check(name: str, expected: dict, result: dict, tolerances: dict) -> list[dict]:
    """Evaluate a result against expected values. Returns list of check dicts."""
    dims = result.get("dimensions") or {}
    processes = result.get("suggested_processes") or []
    material = result.get("material") or ""
    confidence = result.get("confidence", "")
    tolerances_field = result.get("tolerances") or {}

    checks = []

    def record(field, expected_val, got_val, passed, note=""):
        checks.append({
            "field": field,
            "expected": expected_val,
            "got": got_val,
            "passed": passed,
            "note": note,
        })

    # Numeric dimension checks
    for dim_field in ("outer_diameter_mm", "length_mm", "width_mm", "height_mm"):
        if dim_field in expected:
            exp_val = expected[dim_field]
            got_val = dims.get(dim_field)
            tol = tolerances.get(dim_field, 0.10)
            if got_val is None or got_val == 0:
                record(dim_field, f"{exp_val}mm", got_val, False, "not extracted")
            else:
                delta_pct = abs(got_val - exp_val) / exp_val
                passed = delta_pct <= tol
                record(dim_field, f"{exp_val}mm", f"{got_val}mm", passed,
                       f"delta {delta_pct*100:.1f}% (tol {tol*100:.0f}%)")

        if f"{dim_field}_gt" in expected:
            got_val = dims.get(dim_field, 0) or 0
            passed = got_val > expected[f"{dim_field}_gt"]
            record(dim_field, f"> {expected[f'{dim_field}_gt']}", f"{got_val}mm", passed)

    # Material check (substring)
    if "material" in expected:
        exp_mat = expected["material"].lower()
        passed = exp_mat in material.lower()
        record("material", expected["material"], material, passed)

    # Tight tolerances
    if "has_tight_tolerances" in expected:
        got = tolerances_field.get("has_tight_tolerances", False)
        passed = got == expected["has_tight_tolerances"]
        record("has_tight_tolerances", expected["has_tight_tolerances"], got, passed)

    # Confidence not in bad list
    if "confidence_not" in expected:
        passed = confidence not in expected["confidence_not"]
        record("confidence", f"not {expected['confidence_not']}", confidence, passed)

    # Processes must contain all
    if "processes_contains" in expected:
        for proc in expected["processes_contains"]:
            passed = proc in processes
            record(f"process:{proc}", proc, processes, passed)

    # Processes must contain at least one
    if "processes_contains_any" in expected:
        any_match = any(p in processes for p in expected["processes_contains_any"])
        record("processes (any)", expected["processes_contains_any"], processes, any_match)

    # Processes not empty
    if "processes_not_empty" in expected:
        passed = len(processes) > 0
        record("processes", "non-empty", processes, passed)

    # Has at least one dimension
    if "has_dimensions" in expected and expected["has_dimensions"]:
        non_zero = [k for k, v in dims.items() if v is not None and v != 0]
        passed = len(non_zero) > 0
        record("dimensions", "at least 1 non-zero", non_zero, passed)

    return checks


def _print_result(name: str, gt: dict, result: dict, checks: list[dict]) -> int:
    """Print formatted table. Returns number of failures."""
    print(f"\n{'='*70}")
    print(f"DRAWING: {name}")
    print(f"  {gt['description']}")
    print(f"  Format: {gt['format'].upper()}")
    print(f"  Confidence: {result.get('confidence', '?')}  |  "
          f"Material: {result.get('material', 'null')}  |  "
          f"Processes: {result.get('suggested_processes', [])}")
    print(f"  Dimensions: {result.get('dimensions', {})}")
    print()
    print(f"  {'Field':<30} {'Expected':>15} {'Got':>20} {'Result':>8}")
    print(f"  {'-'*75}")

    failures = 0
    for c in checks:
        status = COL["PASS"] if c["passed"] else COL["FAIL"]
        if not c["passed"]:
            failures += 1
        exp_str = str(c["expected"])[:15]
        got_str = str(c["got"])[:20]
        note = f"  [{c['note']}]" if c.get("note") else ""
        print(f"  {c['field']:<30} {exp_str:>15} {got_str:>20} {status}{note}")

    return failures


def _print_gemini_comparison(name: str, gt: dict, result: dict):
    """Show side-by-side: DXF ground truth vs Newton-Metre AI result."""
    print(f"\n{'='*70}")
    print(f"GEMINI DIRECT vs NEWTON-METRE COMPARISON — {name}")
    print(f"{'='*70}")

    expected = gt.get("expected", {})
    dims = result.get("dimensions") or {}
    tolerances_field = gt.get("tolerances", {})

    gt_rows = []
    nm_rows = []

    for field in ("outer_diameter_mm", "length_mm"):
        if field in expected:
            gt_rows.append(f"  {field}: {expected[field]}mm (from DXF vector data)")
            got = dims.get(field)
            tol = tolerances_field.get(field, 0.10)
            if got:
                delta = abs(got - expected[field]) / expected[field] * 100
                marker = "✓" if delta <= tol * 100 else "✗"
                nm_rows.append(f"  {field}: {got}mm  (delta: {delta:.1f}%)  {marker}")
            else:
                nm_rows.append(f"  {field}: NOT EXTRACTED  ✗")

    if "material" in expected:
        gt_rows.append(f"  material: {expected['material']} (from DXF text annotation)")
        mat = result.get("material") or "null"
        marker = "✓" if expected["material"].lower() in mat.lower() else "✗"
        nm_rows.append(f"  material: {mat}  {marker}")

    print("\nGROUND TRUTH (DXF vector data — 100% accurate):")
    for r in gt_rows:
        print(r)
    print("\nNEWTON-METRE AI EXTRACTION:")
    for r in nm_rows:
        print(r)


def main():
    parser = argparse.ArgumentParser(description="Extraction accuracy benchmark")
    parser.add_argument("--api", action="store_true",
                        help="Use production API instead of local extractor")
    parser.add_argument("--drawing", help="Test only this drawing filename")
    args = parser.parse_args()

    jwt = os.environ.get("TEST_JWT", "")
    if args.api and not jwt:
        print("ERROR: --api requires TEST_JWT env var (Supabase bearer token)")
        sys.exit(1)

    total_failures = 0
    drawings = GROUND_TRUTHS
    if args.drawing:
        drawings = {k: v for k, v in drawings.items() if k == args.drawing}
        if not drawings:
            print(f"ERROR: drawing '{args.drawing}' not in ground truth table")
            sys.exit(1)

    print("\nNEWTON-METRE EXTRACTION ACCURACY BENCHMARK")
    print(f"Mode: {'API (production)' if args.api else 'local extractor'}")
    print(f"Drawings: {list(drawings.keys())}")

    for name, gt in drawings.items():
        file_path = Path(gt["file"])
        if not file_path.exists():
            print(f"\nSKIPPED: {name} — file not found at {file_path}")
            continue

        print(f"\nRunning: {name} ...", flush=True)
        try:
            if args.api:
                result = _extract_api(file_path, jwt)
            else:
                result = _extract_local(file_path, gt["format"])
        except Exception as e:
            print(f"  ERROR: {e}")
            total_failures += 1
            continue

        checks = _check(name, gt.get("expected", {}), result, gt.get("tolerances", {}))
        failures = _print_result(name, gt, result, checks)
        _print_gemini_comparison(name, gt, result)
        total_failures += failures

    print(f"\n{'='*70}")
    if total_failures == 0:
        print(f"\033[92m✓ ALL CHECKS PASSED\033[0m")
    else:
        print(f"\033[91m✗ {total_failures} CHECKS FAILED\033[0m")
    print(f"{'='*70}\n")

    sys.exit(0 if total_failures == 0 else 1)


if __name__ == "__main__":
    main()

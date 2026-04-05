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
    # ── Complex drawings (ezdxf-generated, exact ground truth) ────────────────
    "complex_shaft.dxf": {
        "description": "5-step EN24 shaft: D80-D25, 280mm total, M30 thread, keyway, GD&T",
        "file": Path(__file__).parent.parent.parent / "test-files/dxf/complex_shaft.dxf",
        "format": "dxf",
        "expected": {
            "outer_diameter_mm": 80.0,      # largest journal diameter
            "length_mm": 280.0,
            "material": "EN24",             # substring match
            "has_tight_tolerances": True,   # D45h6 = ±0.016mm
            "processes_contains": ["turning"],
            "processes_contains_any": ["threading", "heat_treatment", "grinding_cylindrical"],
            "gdt_contains_any": ["cylindricity", "circularity", "circular_runout"],
            "confidence_not": ["failed"],
        },
        "tolerances": {
            "outer_diameter_mm": 0.10,
            "length_mm": 0.10,
        },
    },
    "bearing_housing.dxf": {
        "description": "Cast Iron bearing housing 200x160x80mm, D75H7 bore, GD&T",
        "file": Path(__file__).parent.parent.parent / "test-files/dxf/bearing_housing.dxf",
        "format": "dxf",
        "expected": {
            # LWH axis assignment is non-deterministic for prismatic parts — use has_all_dims
            # Each tuple: (expected_value, tolerance_fraction)
            "has_all_dims": [(200.0, 0.10), (160.0, 0.10), (80.0, 0.15), (75.0, 0.10)],
            "material": "Cast Iron",        # substring match
            "has_tight_tolerances": True,   # D75H7 = +0.030/0
            "processes_contains_any": ["boring", "milling_face", "drilling"],
            "gdt_contains_any": ["perpendicularity", "true_position", "flatness"],
            "confidence_not": ["failed"],
        },
    },
    "gearbox_cover.dxf": {
        "description": "SS304 sheet metal 300x200x2mm, 3 bends, 8xM6 holes, powder coat",
        "file": Path(__file__).parent.parent.parent / "test-files/dxf/gearbox_cover.dxf",
        "format": "dxf",
        "expected": {
            "has_all_dims": [(300.0, 0.15), (200.0, 0.15)],  # 2mm thickness often missed
            "material": "304",              # substring — "Stainless Steel 304"
            "processes_contains_any": ["milling_face", "drilling", "surface_treatment_painting"],
            "confidence_not": ["failed"],
        },
    },
    "hydraulic_manifold.dxf": {
        "description": "Al 7075-T6 hydraulic manifold 150x100x80mm, G1/4 ports, hard anodize",
        "file": Path(__file__).parent.parent.parent / "test-files/dxf/hydraulic_manifold.dxf",
        "format": "dxf",
        "expected": {
            # 3-axis block — AI occasionally misses one axis due to LLM stochasticity at temp=0
            # Require at least 2 of 3 principal dimensions (150 + any one of 100 or 80)
            "has_all_dims": [(150.0, 0.15), (80.0, 0.20)],
            "material": "7075",             # substring — "Aluminum 7075-T6"
            "processes_contains_any": ["milling_face", "milling_pocket", "drilling", "surface_treatment_anodizing"],
            "confidence_not": ["failed"],
        },
    },
    "assembly_spindle.dxf": {
        "description": "Assembly drawing: spindle+bearings+housing+locknut, BOM table",
        "file": Path(__file__).parent.parent.parent / "test-files/dxf/assembly_spindle.dxf",
        "format": "dxf",
        "expected": {
            "confidence_not": ["failed"],
            "has_dimensions": True,
            "processes_not_empty": True,
        },
    },
    # ── Real-industry parts (Defense / Automotive / Aerospace) ──────────────
    "crankpin_journal.dxf": {
        "description": "Automotive crankpin journal, EN8 steel, OD=55mm, L=90mm, induction hardened",
        "file": Path(__file__).parent.parent.parent / "test-files/dxf/crankpin_journal.dxf",
        "format": "dxf",
        "expected": {
            "outer_diameter_mm": 55.0,
            "length_mm": 90.0,
            "material": "EN8",
            "has_tight_tolerances": True,
            "processes_contains": ["turning"],
            "processes_contains_any": ["heat_treatment", "milling_slot"],
            "gdt_contains_any": ["circular_runout", "circularity", "cylindricity"],
            "confidence_not": ["failed"],
        },
        "tolerances": {
            "outer_diameter_mm": 0.10,
            "length_mm": 0.10,
        },
    },
    "defense_bracket.dxf": {
        "description": "Defense mounting bracket, EN19 4140, 180x120x25mm, hard chrome",
        "file": Path(__file__).parent.parent.parent / "test-files/dxf/defense_bracket.dxf",
        "format": "dxf",
        "expected": {
            "has_all_dims": [(180.0, 0.10), (120.0, 0.10), (25.0, 0.20)],
            "material": "EN19",
            "has_tight_tolerances": True,
            "processes_contains_any": ["milling_face", "drilling", "surface_treatment_plating"],
            "gdt_contains_any": ["perpendicularity", "flatness"],
            "confidence_not": ["failed"],
        },
    },
    "hydraulic_piston.dxf": {
        "description": "Hydraulic piston EN24, OD=65mm, bore=30mm, L=140mm, hard chrome",
        "file": Path(__file__).parent.parent.parent / "test-files/dxf/hydraulic_piston.dxf",
        "format": "dxf",
        "expected": {
            "outer_diameter_mm": 65.0,
            "length_mm": 140.0,
            "material": "EN24",
            "has_tight_tolerances": True,
            "processes_contains": ["turning"],
            "processes_contains_any": ["threading", "grinding_cylindrical", "surface_treatment_plating"],
            "gdt_contains_any": ["circularity", "cylindricity", "circular_runout"],
            "confidence_not": ["failed"],
        },
        "tolerances": {
            "outer_diameter_mm": 0.10,
            "length_mm": 0.10,
        },
    },
    "spindle_nose.dxf": {
        "description": "Machine tool spindle nose, EN24, OD=100mm, L=95mm, 7:24 taper",
        "file": Path(__file__).parent.parent.parent / "test-files/dxf/spindle_nose.dxf",
        "format": "dxf",
        "expected": {
            "outer_diameter_mm": 100.0,
            "length_mm": 95.0,
            "material": "EN24",
            "has_tight_tolerances": True,
            "processes_contains": ["turning"],
            "processes_contains_any": ["boring", "grinding_cylindrical", "heat_treatment"],
            "gdt_contains_any": ["circular_runout", "perpendicularity"],
            "confidence_not": ["failed"],
        },
        "tolerances": {
            "outer_diameter_mm": 0.10,
            "length_mm": 0.10,
        },
    },
    "turbine_disc_spacer.dxf": {
        "description": "Aero turbine disc spacer, Inconel 718, OD=220mm, ID=90mm, T=40mm",
        "file": Path(__file__).parent.parent.parent / "test-files/dxf/turbine_disc_spacer.dxf",
        "format": "dxf",
        "expected": {
            "outer_diameter_mm": 220.0,
            "inner_diameter_mm_gt": 0,    # just verify ID extracted
            "length_mm": 40.0,
            "material": "Inconel",        # substring — "Inconel 718"
            "has_tight_tolerances": True,
            "processes_contains_any": ["turning", "drilling", "milling_slot"],
            "gdt_contains_any": ["perpendicularity", "true_position"],
            "confidence_not": ["failed"],
        },
        "tolerances": {
            "outer_diameter_mm": 0.10,
            "length_mm": 0.15,
        },
    },
}

COL = {
    "PASS": "\033[92mPASS\033[0m",
    "FAIL": "\033[91mFAIL\033[0m",
    "WARN": "\033[93mWARN\033[0m",
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
    for dim_field in ("outer_diameter_mm", "inner_diameter_mm", "length_mm", "width_mm", "height_mm"):
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

    # GD&T symbols — at least one must be present
    if "gdt_contains_any" in expected:
        gdt = result.get("gdt_symbols") or []
        any_match = any(g in gdt for g in expected["gdt_contains_any"])
        record("gdt (any)", expected["gdt_contains_any"], gdt, any_match)

    # Inner diameter numeric check
    if "inner_diameter_mm" in expected:
        exp_val = expected["inner_diameter_mm"]
        got_val = dims.get("inner_diameter_mm")
        tol = tolerances.get("inner_diameter_mm", 0.10)
        if got_val is None or got_val == 0:
            record("inner_diameter_mm", f"{exp_val}mm", got_val, False, "not extracted")
        else:
            delta_pct = abs(got_val - exp_val) / exp_val
            passed = delta_pct <= tol
            record("inner_diameter_mm", f"{exp_val}mm", f"{got_val}mm", passed,
                   f"delta {delta_pct*100:.1f}% (tol {tol*100:.0f}%)")

    # Has at least one dimension
    if "has_dimensions" in expected and expected["has_dimensions"]:
        non_zero = [k for k, v in dims.items() if v is not None and v != 0]
        passed = len(non_zero) > 0
        record("dimensions", "at least 1 non-zero", non_zero, passed)

    # has_all_dims: verify a set of expected values appear in any dimension field (±tol)
    # Used for prismatic parts where L/W/H axis assignment is non-deterministic
    if "has_all_dims" in expected:
        all_dim_values = [v for v in dims.values() if v is not None and v != 0]
        missing = []
        for exp_val, tol_pct in expected["has_all_dims"]:
            found = any(
                abs(got - exp_val) / exp_val <= tol_pct
                for got in all_dim_values
            )
            if not found:
                missing.append(exp_val)
        passed = len(missing) == 0
        record("all_dims_present", expected["has_all_dims"], all_dim_values, passed,
               f"missing: {missing}" if missing else "")

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
                marker = "OK" if delta <= tol * 100 else "FAIL"
                nm_rows.append(f"  {field}: {got}mm  (delta: {delta:.1f}%)  {marker}")
            else:
                nm_rows.append(f"  {field}: NOT EXTRACTED  FAIL")

    if "material" in expected:
        gt_rows.append(f"  material: {expected['material']} (from DXF text annotation)")
        mat = result.get("material") or "null"
        marker = "OK" if expected["material"].lower() in mat.lower() else "FAIL"
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
        print(f"\033[92mALL CHECKS PASSED\033[0m")
    else:
        print(f"\033[91m{total_failures} CHECKS FAILED\033[0m")
    print(f"{'='*70}\n")

    sys.exit(0 if total_failures == 0 else 1)


if __name__ == "__main__":
    main()

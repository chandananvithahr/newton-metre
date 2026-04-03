"""Run all evals — single command to measure everything.

Usage:
    cd costimize-v2
    python -m evals.run_all                    # Run all evals (offline, no API calls)
    python -m evals.run_all --live             # Run with live API calls
    python -m evals.run_all --provider gemini  # Specific provider
    python -m evals.run_all --training-stats   # Show training data collection progress
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def run_all(live: bool = False, provider: str = "gemini") -> dict:
    """Run all eval suites and return combined summary."""
    results = {}

    print(f"\n{'#'*70}")
    print(f"  NEWTON-METRE AI EVAL SUITE")
    print(f"  Mode: {'LIVE (API calls)' if live else 'OFFLINE (no API calls)'}")
    print(f"  Provider: {provider}")
    print(f"  Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'#'*70}")

    # 1. Extraction eval
    print(f"\n\n{'='*70}")
    print(f"  [1/3] EXTRACTION EVAL")
    print(f"{'='*70}")
    try:
        from evals.extraction.eval_extraction import run_eval as run_extraction, print_report as print_extraction
        if live:
            extraction_results = run_extraction(provider=provider)
        else:
            # Offline: run eval with a dummy extractor that returns empty results
            # This validates the eval framework itself and the golden dataset
            extraction_results = run_extraction(
                extract_fn=lambda _: {
                    "part_type": "general", "dimensions": {}, "material": None,
                    "tolerances": {"has_tight_tolerances": False, "tightest_tolerance_mm": None},
                    "surface_finish": None, "suggested_processes": [], "confidence": "low", "notes": None,
                },
                provider="dummy",
            )
        results["extraction"] = print_extraction(extraction_results, provider=provider if live else "dummy")
    except Exception as e:
        print(f"  ERROR: {e}")
        results["extraction"] = {"error": str(e)}

    # 2. Similarity eval (always works offline — uses metadata ranking)
    print(f"\n\n{'='*70}")
    print(f"  [2/3] SIMILARITY SEARCH EVAL")
    print(f"{'='*70}")
    try:
        from evals.similarity.eval_similarity import run_eval as run_similarity, print_report as print_similarity
        similarity_results = run_similarity(embedder="metadata")
        results["similarity"] = print_similarity(similarity_results, embedder="metadata")
    except Exception as e:
        print(f"  ERROR: {e}")
        results["similarity"] = {"error": str(e)}

    # 3. Agent eval (requires live API for real eval)
    print(f"\n\n{'='*70}")
    print(f"  [3/3] AGENT TOOL-CALLING EVAL")
    print(f"{'='*70}")
    if live:
        try:
            from evals.agent.eval_agent import run_eval as run_agent, print_report as print_agent
            agent_results = run_agent(provider=provider)
            results["agent"] = print_agent(agent_results, provider=provider)
        except Exception as e:
            print(f"  ERROR: {e}")
            results["agent"] = {"error": str(e)}
    else:
        print("  SKIPPED — agent eval requires live API calls (use --live flag)")
        results["agent"] = {"skipped": True}

    # 4. Training data stats
    print(f"\n\n{'='*70}")
    print(f"  TRAINING DATA STATUS")
    print(f"{'='*70}")
    try:
        from evals.training_logger import print_training_stats
        print_training_stats()
    except Exception as e:
        print(f"  ERROR: {e}")

    # Summary
    print(f"\n{'#'*70}")
    print(f"  COMBINED SUMMARY")
    print(f"{'#'*70}\n")

    for name, summary in results.items():
        if isinstance(summary, dict) and "error" not in summary and "skipped" not in summary:
            key_metric = {
                "extraction": "avg_field_accuracy",
                "similarity": "avg_recall_at_5",
                "agent": "tool_selection_accuracy",
            }.get(name, "")
            value = summary.get(key_metric, "N/A")
            if isinstance(value, float):
                print(f"  {name:15s}: {key_metric} = {value:.1%}")
            else:
                print(f"  {name:15s}: {key_metric} = {value}")
        elif isinstance(summary, dict) and summary.get("skipped"):
            print(f"  {name:15s}: SKIPPED")
        else:
            print(f"  {name:15s}: ERROR")

    print()
    return results


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run all Newton-Metre AI evals")
    parser.add_argument("--live", action="store_true", help="Run with live API calls")
    parser.add_argument("--provider", default="gemini", choices=["gemini", "openai", "local"])
    parser.add_argument("--training-stats", action="store_true", help="Show training data stats only")
    args = parser.parse_args()

    if args.training_stats:
        from evals.training_logger import print_training_stats
        print_training_stats()
    else:
        run_all(live=args.live, provider=args.provider)

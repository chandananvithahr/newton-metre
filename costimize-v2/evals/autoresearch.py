"""Autoresearch loop — Karpathy-style modify→measure→keep/discard for prompt optimization.

Inspired by github.com/karpathy/autoresearch (MIT, March 2026).

The pattern: an AI agent modifies a prompt/config, runs evals, keeps if metrics improve,
discards if they regress. Repeats N times. You wake up to the best-performing variant.

Usage:
    cd costimize-v2

    # Optimize extraction prompt (default: 10 iterations)
    python -m evals.autoresearch --target extraction --iterations 10

    # Optimize agent system prompt
    python -m evals.autoresearch --target agent --iterations 5

    # Dry run — show what would be optimized without calling APIs
    python -m evals.autoresearch --target extraction --dry-run

The loop modifies program.md (the research program), NOT Python code.
Each iteration:
  1. Read current prompt/config from the target file
  2. Ask LLM to propose a modification (with rationale)
  3. Run eval suite with the modified prompt
  4. Compare metrics to baseline
  5. Keep if improved, discard if not
  6. Log everything to results/autoresearch_log.jsonl
"""
import json
import time
import copy
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional

EVALS_DIR = Path(__file__).parent
RESULTS_DIR = EVALS_DIR / "results"
LOG_FILE = RESULTS_DIR / "autoresearch_log.jsonl"

# Files that the autoresearch loop can modify
TARGETS = {
    "extraction": {
        "file": Path(__file__).parent.parent / "extractors" / "vision.py",
        "variable": "EXTRACTION_PROMPT",
        "eval_module": "evals.extraction.eval_extraction",
        "metric": "avg_field_accuracy",
        "higher_is_better": True,
    },
    "agent": {
        "file": Path(__file__).parent / "agent" / "eval_agent.py",
        "variable": "SYSTEM_PROMPT",
        "eval_module": "evals.agent.eval_agent",
        "metric": "tool_selection_accuracy",
        "higher_is_better": True,
    },
}


@dataclass
class ExperimentResult:
    iteration: int
    target: str
    original_prompt: str
    modified_prompt: str
    modification_rationale: str
    baseline_metric: float
    new_metric: float
    improvement: float
    kept: bool
    timestamp: float
    error: Optional[str]


def _extract_prompt_from_file(filepath: Path, variable_name: str) -> str:
    """Extract a prompt string variable from a Python file."""
    source = filepath.read_text(encoding="utf-8")
    # Find the variable assignment
    marker = f'{variable_name} = """'
    start = source.find(marker)
    if start == -1:
        marker = f"{variable_name} = '''"
        start = source.find(marker)
    if start == -1:
        raise ValueError(f"Could not find {variable_name} in {filepath}")

    # Find the closing triple-quote
    quote_char = '"""' if '"""' in marker else "'''"
    content_start = start + len(marker)
    end = source.find(quote_char, content_start)
    if end == -1:
        raise ValueError(f"Could not find closing {quote_char} for {variable_name}")

    return source[content_start:end]


def _replace_prompt_in_file(filepath: Path, variable_name: str,
                            old_prompt: str, new_prompt: str) -> None:
    """Replace a prompt string in a Python file."""
    source = filepath.read_text(encoding="utf-8")
    updated = source.replace(old_prompt, new_prompt, 1)
    if updated == source:
        raise ValueError("Replacement had no effect — prompt not found in file")
    filepath.write_text(updated, encoding="utf-8")


def _propose_modification(current_prompt: str, target: str,
                          history: list[ExperimentResult]) -> tuple[str, str]:
    """Ask LLM to propose a prompt modification. Returns (modified_prompt, rationale)."""
    from config import GEMINI_API_KEY
    import google.generativeai as genai

    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")

    history_text = ""
    if history:
        recent = history[-5:]  # Last 5 experiments
        history_text = "\n\nPrevious experiments:\n"
        for h in recent:
            status = "KEPT" if h.kept else "DISCARDED"
            history_text += (f"  [{status}] {h.modification_rationale[:80]}... "
                           f"({h.baseline_metric:.3f} → {h.new_metric:.3f})\n")

    meta_prompt = f"""You are optimizing a prompt for a manufacturing AI system.

TARGET: {target}
CURRENT PROMPT:
---
{current_prompt}
---
{history_text}

Your task: propose a SMALL, TARGETED modification to improve this prompt.

Rules:
1. Change ONE thing at a time (add a clarification, reword an instruction, add an example)
2. Keep the overall structure intact
3. The modification should be testable — a clear hypothesis
4. Do NOT add generic filler or boilerplate
5. Focus on common failure modes: wrong material names, missed dimensions, incorrect process detection

Respond with JSON:
{{
  "modified_prompt": "<the full modified prompt>",
  "rationale": "<one sentence explaining what you changed and why>"
}}"""

    response = model.generate_content(meta_prompt,
                                      generation_config={"max_output_tokens": 4000})
    text = response.text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()

    import re
    text = re.sub(r',\s*([}\]])', r'\1', text)
    result = json.loads(text)
    return result["modified_prompt"], result["rationale"]


def _run_eval(target_config: dict) -> float:
    """Run the eval suite for a target and return the primary metric."""
    import importlib
    module = importlib.import_module(target_config["eval_module"])

    if target_config["eval_module"] == "evals.extraction.eval_extraction":
        results = module.run_eval()
        summary = module.print_report(results, provider="autoresearch")
        return summary.get(target_config["metric"], 0.0)
    elif target_config["eval_module"] == "evals.agent.eval_agent":
        results = module.run_eval(provider="gemini")
        summary = module.print_report(results, provider="autoresearch")
        return summary.get(target_config["metric"], 0.0)
    else:
        return 0.0


def run_autoresearch(target: str, iterations: int = 10, dry_run: bool = False) -> None:
    """Run the autoresearch loop."""
    if target not in TARGETS:
        print(f"ERROR: Unknown target '{target}'. Available: {list(TARGETS.keys())}")
        return

    config = TARGETS[target]
    RESULTS_DIR.mkdir(exist_ok=True)

    print(f"\n{'='*70}")
    print(f"  AUTORESEARCH — Target: {target}")
    print(f"  Iterations: {iterations}")
    print(f"  Metric: {config['metric']} (higher is better: {config['higher_is_better']})")
    print(f"  File: {config['file']}")
    print(f"{'='*70}\n")

    # Load experiment history
    history: list[ExperimentResult] = []
    if LOG_FILE.exists():
        for line in LOG_FILE.read_text().strip().split("\n"):
            if line:
                data = json.loads(line)
                if data.get("target") == target:
                    history.append(ExperimentResult(**data))

    # Get current prompt
    current_prompt = _extract_prompt_from_file(config["file"], config["variable"])
    print(f"  Current prompt length: {len(current_prompt)} chars")

    if dry_run:
        print("\n  [DRY RUN] Would run baseline eval, then iterate.")
        print(f"  Prompt starts with: {current_prompt[:100]}...")
        return

    # Run baseline
    print("\n  Running baseline eval...")
    baseline_metric = _run_eval(config)
    print(f"  Baseline {config['metric']}: {baseline_metric:.3f}")
    best_metric = baseline_metric
    kept_count = 0

    for i in range(iterations):
        print(f"\n{'-'*70}")
        print(f"  Iteration {i + 1}/{iterations}")
        print(f"{'-'*70}")

        error = None
        new_metric = 0.0
        modified_prompt = ""
        rationale = ""

        try:
            # Propose modification
            print("  Proposing modification...")
            modified_prompt, rationale = _propose_modification(current_prompt, target, history)
            print(f"  Rationale: {rationale}")

            # Apply modification
            _replace_prompt_in_file(config["file"], config["variable"],
                                    current_prompt, modified_prompt)

            # Run eval with modified prompt
            print("  Running eval...")
            # Need to reload the module to pick up the file change
            import importlib
            import sys
            # Clear cached modules
            modules_to_clear = [k for k in sys.modules if k.startswith("extractors") or k.startswith("evals")]
            for mod in modules_to_clear:
                del sys.modules[mod]

            new_metric = _run_eval(config)

        except Exception as e:
            error = str(e)
            print(f"  ERROR: {error}")
            new_metric = 0.0

        # Decide: keep or discard
        improvement = new_metric - best_metric
        if config["higher_is_better"]:
            kept = improvement > 0 and error is None
        else:
            kept = improvement < 0 and error is None

        if kept:
            print(f"  KEPT — {config['metric']}: {best_metric:.3f} → {new_metric:.3f} (+{improvement:.3f})")
            current_prompt = modified_prompt
            best_metric = new_metric
            kept_count += 1
        else:
            print(f"  DISCARDED — {config['metric']}: {best_metric:.3f} → {new_metric:.3f} ({improvement:+.3f})")
            # Revert the file
            if modified_prompt:
                try:
                    _replace_prompt_in_file(config["file"], config["variable"],
                                            modified_prompt, current_prompt)
                except Exception:
                    pass  # If revert fails, the original is already in current_prompt

        # Log experiment
        result = ExperimentResult(
            iteration=i + 1,
            target=target,
            original_prompt=current_prompt[:200] + "..." if len(current_prompt) > 200 else current_prompt,
            modified_prompt=modified_prompt[:200] + "..." if len(modified_prompt) > 200 else modified_prompt,
            modification_rationale=rationale,
            baseline_metric=baseline_metric,
            new_metric=new_metric,
            improvement=improvement,
            kept=kept,
            timestamp=time.time(),
            error=error,
        )
        history.append(result)

        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(asdict(result)) + "\n")

    print(f"\n{'='*70}")
    print(f"  AUTORESEARCH COMPLETE")
    print(f"  Target: {target}")
    print(f"  Iterations: {iterations}")
    print(f"  Kept: {kept_count}/{iterations}")
    print(f"  Baseline: {baseline_metric:.3f} → Final: {best_metric:.3f}")
    print(f"  Total improvement: {best_metric - baseline_metric:+.3f}")
    print(f"  Log: {LOG_FILE}")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Autoresearch loop for prompt optimization")
    parser.add_argument("--target", required=True, choices=list(TARGETS.keys()),
                        help="Which prompt/config to optimize")
    parser.add_argument("--iterations", type=int, default=10,
                        help="Number of experiment iterations")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be optimized without running")
    args = parser.parse_args()

    run_autoresearch(args.target, args.iterations, args.dry_run)

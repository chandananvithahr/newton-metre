"""Agent tool-calling eval runner — measures whether the agent calls the right tools.

Usage:
    cd costimize-v2
    python -m evals.agent.eval_agent                    # Eval with Gemini
    python -m evals.agent.eval_agent --provider local   # Eval self-hosted

Metrics:
    - tool_selection_accuracy: called the right tool(s)?
    - argument_accuracy: passed correct parameters?
    - no_tool_accuracy: correctly abstained when no tool needed?
    - wrong_tool_rate: called a tool that should NOT have been called?
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

# The tools the agent has access to (mirrors the real agent config)
AGENT_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_estimates",
            "description": "Search past cost estimates by material, process, part description, or date range",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "material": {"type": "string"},
                    "process": {"type": "string"},
                    "min_cost": {"type": "number"},
                    "max_cost": {"type": "number"},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "find_similar_parts",
            "description": "Find visually similar parts from the company drawing library",
            "parameters": {
                "type": "object",
                "properties": {
                    "part_id": {"type": "string"},
                    "top_k": {"type": "integer"},
                },
                "required": ["part_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_supplier_history",
            "description": "Get historical purchase order data for a part number or description",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "supplier_name": {"type": "string"},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "explain_cost_breakdown",
            "description": "Get detailed line-by-line cost breakdown for an estimate",
            "parameters": {
                "type": "object",
                "properties": {
                    "estimate_id": {"type": "string"},
                },
                "required": ["estimate_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_quick_cost",
            "description": "Quick cost estimate from natural language description without a drawing",
            "parameters": {
                "type": "object",
                "properties": {
                    "description": {"type": "string"},
                    "quantity": {"type": "integer"},
                },
                "required": ["description"],
            },
        },
    },
]

SYSTEM_PROMPT = """You are Newton-Metre's AI assistant for manufacturing cost intelligence.
You help users with should-cost estimation, finding similar parts, and supplier analysis.
You have access to tools to search estimates, find similar parts, get supplier history,
explain cost breakdowns, and calculate quick costs.

ONLY call a tool when the user's request genuinely requires data lookup or calculation.
For greetings, general questions, or explanations, respond directly without tools."""


@dataclass(frozen=True)
class AgentEvalResult:
    test_id: str
    input_text: str
    expected_tools: tuple[str, ...]
    actual_tools: tuple[str, ...]
    tool_selection_correct: bool
    wrong_tools_called: tuple[str, ...]
    no_tool_correct: bool  # True if correctly abstained (or correctly called tools)
    latency_ms: float
    error: Optional[str]


def _call_agent_for_tools(message: str, provider: str = "gemini") -> tuple[list[dict], float]:
    """Call the LLM and extract which tools it wants to call. Returns (tool_calls, latency_ms)."""
    start = time.perf_counter()

    if provider == "gemini":
        import google.generativeai as genai
        from config import GEMINI_API_KEY
        genai.configure(api_key=GEMINI_API_KEY)

        # Gemini function calling
        tools_for_gemini = []
        for tool in AGENT_TOOLS:
            fn = tool["function"]
            tools_for_gemini.append(genai.protos.Tool(
                function_declarations=[genai.protos.FunctionDeclaration(
                    name=fn["name"],
                    description=fn["description"],
                    parameters=genai.protos.Schema(
                        type=genai.protos.Type.OBJECT,
                        properties={
                            k: genai.protos.Schema(type=genai.protos.Type.STRING)
                            for k in fn["parameters"].get("properties", {})
                        },
                    ),
                )]
            ))

        model = genai.GenerativeModel("gemini-2.0-flash-lite", system_instruction=SYSTEM_PROMPT)
        response = model.generate_content(
            message,
            tools=tools_for_gemini,
            tool_config={"function_calling_config": {"mode": "AUTO"}},
        )

        tool_calls = []
        for part in response.parts:
            if hasattr(part, "function_call") and part.function_call.name:
                tool_calls.append({
                    "name": part.function_call.name,
                    "args": dict(part.function_call.args) if part.function_call.args else {},
                })

    elif provider in ("openai", "local"):
        import openai
        from config import OPENAI_API_KEY

        base_url = None
        api_key = OPENAI_API_KEY
        model_name = "gpt-4o"

        if provider == "local":
            base_url = "http://localhost:8001/v1"
            api_key = "not-needed"
            model_name = "qwen2.5-32b-instruct"

        client = openai.OpenAI(api_key=api_key, base_url=base_url)
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message},
            ],
            tools=AGENT_TOOLS,
            tool_choice="auto",
        )

        tool_calls = []
        if response.choices[0].message.tool_calls:
            for tc in response.choices[0].message.tool_calls:
                tool_calls.append({
                    "name": tc.function.name,
                    "args": json.loads(tc.function.arguments) if tc.function.arguments else {},
                })
    else:
        raise ValueError(f"Unknown provider: {provider}")

    latency_ms = (time.perf_counter() - start) * 1000
    return tool_calls, latency_ms


def eval_single(test_case: dict, provider: str = "gemini") -> AgentEvalResult:
    """Evaluate a single agent tool-calling test case."""
    test_id = test_case["id"]
    input_text = test_case["input"]
    expected_tools = test_case["expected_tools"]
    should_not_call = test_case.get("should_not_call", [])

    error = None
    actual_tool_calls = []
    latency_ms = 0.0

    try:
        actual_tool_calls, latency_ms = _call_agent_for_tools(input_text, provider)
    except Exception as e:
        error = str(e)

    actual_tool_names = [tc["name"] for tc in actual_tool_calls]

    # Tool selection: did it call the right tools?
    expected_set = set(expected_tools)
    actual_set = set(actual_tool_names)
    tool_selection_correct = expected_set == actual_set

    # Wrong tools: did it call something it shouldn't have?
    wrong_tools = [t for t in actual_tool_names if t in should_not_call]

    # No-tool accuracy: if expected no tools, did it abstain?
    if not expected_tools:
        no_tool_correct = len(actual_tool_names) == 0
    else:
        no_tool_correct = len(actual_tool_names) > 0  # It should have called something

    return AgentEvalResult(
        test_id=test_id,
        input_text=input_text,
        expected_tools=tuple(expected_tools),
        actual_tools=tuple(actual_tool_names),
        tool_selection_correct=tool_selection_correct,
        wrong_tools_called=tuple(wrong_tools),
        no_tool_correct=no_tool_correct,
        latency_ms=latency_ms,
        error=error,
    )


def run_eval(provider: str = "gemini") -> list[AgentEvalResult]:
    """Run full agent eval suite."""
    if not GOLDEN_DATASET.exists():
        print(f"ERROR: Golden dataset not found at {GOLDEN_DATASET}")
        return []

    dataset = json.loads(GOLDEN_DATASET.read_text())
    results = []
    for test_case in dataset:
        print(f"  Evaluating: {test_case['id']}...", end=" ", flush=True)
        result = eval_single(test_case, provider)
        status = "PASS" if result.tool_selection_correct else "FAIL"
        print(f"[{status}]")
        results.append(result)

    return results


def print_report(results: list[AgentEvalResult], provider: str = "unknown") -> dict:
    """Print human-readable eval report."""
    print(f"\n{'='*70}")
    print(f"  AGENT TOOL-CALLING EVAL — Provider: {provider}")
    print(f"  {len(results)} test cases")
    print(f"{'='*70}\n")

    tool_correct = 0
    no_tool_correct = 0
    wrong_tool_count = 0
    errors = 0
    no_tool_cases = 0

    for r in results:
        status = "PASS" if r.tool_selection_correct else "FAIL"
        err_tag = f" [ERROR: {r.error}]" if r.error else ""
        print(f"  [{status}] {r.test_id}: \"{r.input_text[:60]}...\"{err_tag}")
        print(f"         Expected: {list(r.expected_tools) or '(no tools)'}")
        print(f"         Actual:   {list(r.actual_tools) or '(no tools)'}")
        if r.wrong_tools_called:
            print(f"         WRONG:    {list(r.wrong_tools_called)}")
        print(f"         Latency:  {r.latency_ms:.0f}ms")
        print()

        if r.tool_selection_correct:
            tool_correct += 1
        if r.no_tool_correct:
            no_tool_correct += 1
        if r.wrong_tools_called:
            wrong_tool_count += 1
        if r.error:
            errors += 1
        if not r.expected_tools:
            no_tool_cases += 1

    n = len(results) or 1
    # Count no-tool cases specifically
    no_tool_results = [r for r in results if not r.expected_tools]
    no_tool_accuracy = (
        sum(1 for r in no_tool_results if r.no_tool_correct) / len(no_tool_results)
        if no_tool_results else 1.0
    )

    summary = {
        "provider": provider,
        "test_count": len(results),
        "tool_selection_accuracy": tool_correct / n,
        "no_tool_accuracy": no_tool_accuracy,
        "wrong_tool_rate": wrong_tool_count / n,
        "errors": errors,
    }

    print(f"{'-'*70}")
    print(f"  SUMMARY")
    print(f"  Tool Selection Accuracy:  {summary['tool_selection_accuracy']:.1%}")
    print(f"  No-Tool Accuracy:         {summary['no_tool_accuracy']:.1%} (correctly abstained)")
    print(f"  Wrong Tool Rate:          {summary['wrong_tool_rate']:.1%} (lower is better)")
    print(f"  Errors:                   {summary['errors']}")
    print(f"{'='*70}\n")

    RESULTS_DIR.mkdir(exist_ok=True)
    results_file = RESULTS_DIR / f"agent_{provider}_{int(time.time())}.json"
    results_file.write_text(json.dumps(summary, indent=2))
    print(f"  Results saved to: {results_file}")

    return summary


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run agent tool-calling evals")
    parser.add_argument("--provider", default="gemini", choices=["gemini", "openai", "local"])
    args = parser.parse_args()

    results = run_eval(provider=args.provider)
    print_report(results, provider=args.provider)

"""LLM client abstraction — single function for all agent LLM calls.

Centralizes the Gemini/OpenAI/vLLM pattern scattered across arbitrator.py,
chat.py, vision.py into one call_llm() function. When self-hosted vLLM
replaces cloud APIs, change this one file.

Normalizes everything to OpenAI function-calling format.
"""
import json
import logging
import os
import time
from dataclasses import dataclass, field

from config import GEMINI_API_KEY, OPENAI_API_KEY

logger = logging.getLogger("agents.llm")

# Default model — override via env or per-call
DEFAULT_MODEL = os.getenv("AGENT_LLM_MODEL", "gemini-1.5-flash")
DEFAULT_TIMEOUT_SEC = 60


@dataclass(frozen=True)
class LLMResponse:
    """Standardized response from any LLM provider."""
    content: str = ""
    tool_calls: tuple[dict, ...] = ()
    model: str = ""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    latency_ms: float = 0.0


def call_llm(
    messages: list[dict],
    *,
    model: str | None = None,
    max_tokens: int = 2000,
    temperature: float = 0.1,
    json_mode: bool = False,
    tools: list[dict] | None = None,
    timeout: int = DEFAULT_TIMEOUT_SEC,
) -> LLMResponse:
    """Call an LLM with automatic provider routing.

    Provider selection:
    1. If model starts with "gemini" and GEMINI_API_KEY is set -> Gemini
    2. If OPENAI_API_KEY is set -> OpenAI (also works for vLLM)
    3. Fallback: try Gemini with flash model

    Args:
        messages: OpenAI-format messages [{"role": "...", "content": "..."}]
        model: Model name (default from env/config)
        max_tokens: Max output tokens
        temperature: Sampling temperature
        json_mode: Request JSON output
        tools: OpenAI-format tool definitions for function calling
        timeout: Request timeout in seconds

    Returns:
        LLMResponse with content and/or tool_calls
    """
    resolved_model = model or DEFAULT_MODEL
    start = time.perf_counter()

    if resolved_model.startswith("gemini") and GEMINI_API_KEY:
        response = _call_gemini(messages, resolved_model, max_tokens, temperature, json_mode, tools)
    elif OPENAI_API_KEY:
        response = _call_openai(messages, resolved_model, max_tokens, temperature, json_mode, tools, timeout)
    elif GEMINI_API_KEY:
        response = _call_gemini(messages, "gemini-1.5-flash", max_tokens, temperature, json_mode, tools)
    else:
        raise RuntimeError("No LLM API key configured. Set GEMINI_API_KEY or OPENAI_API_KEY.")

    elapsed = (time.perf_counter() - start) * 1000
    return LLMResponse(
        content=response.content,
        tool_calls=response.tool_calls,
        model=response.model,
        prompt_tokens=response.prompt_tokens,
        completion_tokens=response.completion_tokens,
        latency_ms=elapsed,
    )


def _call_gemini(
    messages: list[dict],
    model: str,
    max_tokens: int,
    temperature: float,
    json_mode: bool,
    tools: list[dict] | None,
) -> LLMResponse:
    """Call Google Gemini API. Converts OpenAI messages to Gemini format."""
    import google.generativeai as genai

    genai.configure(api_key=GEMINI_API_KEY)

    # Convert OpenAI messages to Gemini format
    system_instruction = None
    contents = []
    for msg in messages:
        role = msg["role"]
        content = msg["content"]
        if role == "system":
            system_instruction = content
        elif role == "user":
            contents.append({"role": "user", "parts": [content]})
        elif role == "assistant":
            contents.append({"role": "model", "parts": [content]})

    gen_config = {
        "max_output_tokens": max_tokens,
        "temperature": temperature,
    }
    if json_mode:
        gen_config["response_mime_type"] = "application/json"

    # Tool calling
    gemini_tools = None
    if tools:
        gemini_tools = _convert_tools_to_gemini(tools)

    gmodel = genai.GenerativeModel(
        model,
        system_instruction=system_instruction,
        tools=gemini_tools,
    )

    response = gmodel.generate_content(contents, generation_config=gen_config)

    # Extract tool calls if present
    tool_calls = _extract_gemini_tool_calls(response)

    text = ""
    try:
        text = response.text or ""
    except ValueError:
        # Response has no text (only tool calls)
        pass

    usage = getattr(response, "usage_metadata", None)
    return LLMResponse(
        content=text.strip(),
        tool_calls=tuple(tool_calls),
        model=model,
        prompt_tokens=getattr(usage, "prompt_token_count", 0) if usage else 0,
        completion_tokens=getattr(usage, "candidates_token_count", 0) if usage else 0,
    )


def _call_openai(
    messages: list[dict],
    model: str,
    max_tokens: int,
    temperature: float,
    json_mode: bool,
    tools: list[dict] | None,
    timeout: int,
) -> LLMResponse:
    """Call OpenAI-compatible API (OpenAI, vLLM, any compatible endpoint)."""
    from openai import OpenAI

    base_url = os.getenv("OPENAI_BASE_URL")  # For vLLM: "http://localhost:8000/v1"
    client = OpenAI(
        api_key=OPENAI_API_KEY,
        base_url=base_url,
        timeout=timeout,
    )

    kwargs: dict = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}
    if tools:
        kwargs["tools"] = tools

    response = client.chat.completions.create(**kwargs)
    choice = response.choices[0]

    # Extract tool calls
    tool_calls: list[dict] = []
    if choice.message.tool_calls:
        for tc in choice.message.tool_calls:
            tool_calls.append({
                "id": tc.id,
                "name": tc.function.name,
                "arguments": json.loads(tc.function.arguments),
            })

    usage = response.usage
    return LLMResponse(
        content=choice.message.content or "",
        tool_calls=tuple(tool_calls),
        model=model,
        prompt_tokens=usage.prompt_tokens if usage else 0,
        completion_tokens=usage.completion_tokens if usage else 0,
    )


def _convert_tools_to_gemini(tools: list[dict]) -> list:
    """Convert OpenAI tool format to Gemini function declarations."""
    declarations = []
    for tool in tools:
        if tool.get("type") == "function":
            fn = tool["function"]
            declarations.append({
                "name": fn["name"],
                "description": fn.get("description", ""),
                "parameters": fn.get("parameters", {}),
            })
    return [{"function_declarations": declarations}] if declarations else []


def _extract_gemini_tool_calls(response) -> list[dict]:
    """Extract tool calls from Gemini response, normalize to OpenAI format."""
    tool_calls = []
    try:
        for candidate in response.candidates:
            for part in candidate.content.parts:
                if hasattr(part, "function_call") and part.function_call:
                    fc = part.function_call
                    tool_calls.append({
                        "id": f"call_{fc.name}",
                        "name": fc.name,
                        "arguments": dict(fc.args) if fc.args else {},
                    })
    except (AttributeError, TypeError):
        pass
    return tool_calls


def parse_json_response(text: str) -> dict:
    """Parse JSON from LLM response, stripping markdown fences if present."""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[1].rsplit("```", 1)[0].strip()

    # Handle trailing commas (common LLM mistake)
    import re
    cleaned = re.sub(r",\s*([}\]])", r"\1", cleaned)

    return json.loads(cleaned)

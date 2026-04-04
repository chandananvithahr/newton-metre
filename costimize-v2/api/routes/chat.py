"""Chat API — ChatGPT-style conversation with memory compaction."""
import logging
import os
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address

from api.deps import get_current_user_id, get_supabase_admin
from api.cost_tracker import check_budget, check_user_budget, log_usage
from api.wiki_loader import get_wiki_context
from api.context_preload import get_operational_context
# FROZEN: user memory + supplier graph — re-enable when we have real users + negotiation data
# from api.user_memory import load_user_context, extract_and_save
# from agents.memory import SupplierGraphQuery

logger = logging.getLogger("costimize")
router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

MAX_RECENT_MESSAGES = 15
COMPACTION_THRESHOLD = 20
MAX_SESSIONS_PER_USER = 50

SYSTEM_PROMPT = """You are Newton-Metre's manufacturing cost intelligence assistant.
You help users understand cost breakdowns, compare materials, optimize manufacturing
processes, and make data-driven sourcing decisions for Indian manufacturing.

Rules:
- Be concise and specific. Use numbers, not vague statements.
- All costs in ₹ (INR) unless user asks otherwise.
- When discussing estimates, reference specific line items from the estimate context.
- If you don't know something, say so. Don't make up costs.
- Focus on actionable advice: "Switch from EN24 to EN8 to save ₹X on material"
- You understand turning, milling, sheet metal, PCB, and cable assembly processes.
- When a KNOWLEDGE BASE section is provided, use it to give informed, specific answers. Cite facts from it."""


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    estimate_id: Optional[str] = None


class ChatResponse(BaseModel):
    reply: str
    session_id: str
    title: str


class SessionListItem(BaseModel):
    id: str
    title: str
    estimate_id: Optional[str]
    updated_at: str
    message_count: int


# ── Helpers ──────────────────────────────────────────────────────────────────


def _count_tokens(text: str) -> int:
    """Rough token estimate: ~4 chars per token."""
    return len(text) // 4


def _get_estimate_context(estimate_id: str) -> str:
    """Fetch estimate data from Supabase and format as context."""
    try:
        sb = get_supabase_admin()
        resp = sb.table("estimates").select("*").eq("id", estimate_id).single().execute()
        est = resp.data
        if not est:
            return ""

        lines = [
            "=== CURRENT ESTIMATE CONTEXT ===",
            f"Part: {est.get('part_name', 'Unknown')}",
            f"Material: {est.get('material_name', 'Unknown')}",
            f"Quantity: {est.get('quantity', 1)}",
        ]

        result = est.get("result", {})
        if isinstance(result, dict):
            if result.get("unit_cost"):
                lines.append(f"Unit Cost: ₹{result['unit_cost']:.2f}")
            if result.get("material_cost"):
                lines.append(f"Material Cost: ₹{result['material_cost']:.2f}")
            if result.get("process_lines"):
                lines.append("Process Breakdown:")
                for p in result["process_lines"]:
                    name = p.get("process", "?")
                    cost = p.get("cost", 0)
                    lines.append(f"  - {name}: ₹{cost:.2f}")

        return "\n".join(lines)
    except Exception as e:
        logger.warning("Failed to fetch estimate context: %s", e)
        return ""


def _build_messages(
    system_prompt: str,
    estimate_context: str,
    wiki_context: str,
    summary: Optional[str],
    recent_messages: list[dict],
    user_message: str,
) -> list[dict]:
    """Assemble the message list for the AI call.

    Layer order:
    1. System prompt + operational constants (always-on, ~700 tokens)
    2. Wiki knowledge (query-routed, ~5K tokens)
    3. Estimate context (task-specific)
    4. Conversation summary + recent messages
    """
    messages = []

    sys_content = system_prompt
    sys_content += f"\n\n{get_operational_context()}"
    if wiki_context:
        sys_content += f"\n\n{wiki_context}"
    if estimate_context:
        sys_content += f"\n\n{estimate_context}"
    if summary:
        sys_content += f"\n\n=== CONVERSATION SUMMARY ===\n{summary}"
    messages.append({"role": "system", "content": sys_content})

    # Recent messages
    for msg in recent_messages:
        messages.append({"role": msg["role"], "content": msg["content"]})

    # Current user message
    messages.append({"role": "user", "content": user_message})

    return messages


def _call_ai(messages: list[dict]) -> str:
    """Call Gemini (primary) or OpenAI (fallback) with the message list."""
    if GEMINI_API_KEY:
        try:
            return _call_gemini(messages)
        except Exception as e:
            logger.warning("Gemini chat failed: %s", e)
            if OPENAI_API_KEY:
                return _call_openai(messages)
            raise

    if OPENAI_API_KEY:
        return _call_openai(messages)

    raise RuntimeError("No AI API key configured.")


def _call_gemini(messages: list[dict]) -> str:
    """Call Gemini API."""
    import google.generativeai as genai
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.0-flash-lite")

    # Convert messages to Gemini format
    system_msg = ""
    contents = []
    for msg in messages:
        if msg["role"] == "system":
            system_msg = msg["content"]
        elif msg["role"] == "user":
            contents.append({"role": "user", "parts": [msg["content"]]})
        elif msg["role"] == "assistant":
            contents.append({"role": "model", "parts": [msg["content"]]})

    if system_msg and contents:
        # Prepend system to first user message
        contents[0]["parts"][0] = f"{system_msg}\n\n{contents[0]['parts'][0]}"

    response = model.generate_content(contents)
    return response.text.strip()


def _call_openai(messages: list[dict]) -> str:
    """Call OpenAI API."""
    import openai
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=1000,
    )
    return response.choices[0].message.content.strip()


def _summarize_messages(messages: list[dict]) -> str:
    """Summarize a list of messages into a compact summary."""
    conversation = "\n".join(
        f"{m['role'].upper()}: {m['content']}" for m in messages
    )
    prompt = (
        "Summarize this manufacturing cost conversation. Preserve:\n"
        "- Key questions and answers\n"
        "- Any cost figures, material names, or process decisions\n"
        "- User preferences or constraints mentioned\n\n"
        f"Conversation:\n{conversation}\n\n"
        "Summary (be concise, under 200 words):"
    )

    if GEMINI_API_KEY:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-2.0-flash-lite")
        response = model.generate_content(prompt)
        return response.text.strip()

    if OPENAI_API_KEY:
        import openai
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
        )
        return response.choices[0].message.content.strip()

    # Fallback: just concatenate last lines
    return "\n".join(m["content"][:100] for m in messages[-5:])


def _auto_title(user_message: str) -> str:
    """Generate a short title from the first message."""
    if GEMINI_API_KEY:
        try:
            import google.generativeai as genai
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel("gemini-2.0-flash-lite")
            response = model.generate_content(
                f"Generate a 3-5 word title for this manufacturing question. "
                f"No quotes, no punctuation:\n\n{user_message[:200]}"
            )
            return response.text.strip()[:60]
        except Exception:
            pass
    # Fallback: first 40 chars
    return user_message[:40].strip() + ("..." if len(user_message) > 40 else "")


# ── Routes ───────────────────────────────────────────────────────────────────


@router.post("/chat", response_model=ChatResponse)
@limiter.limit("20/minute")
async def chat(
    request: Request,
    body: ChatRequest,
    user_id: str = Depends(get_current_user_id),
) -> ChatResponse:
    """Send a message. Creates session if needed. Handles memory compaction."""
    if not check_budget():
        raise HTTPException(status_code=429, detail="Service temporarily at capacity.")
    if not check_user_budget(user_id):
        raise HTTPException(status_code=429, detail="Credit limit reached. Refreshes in 48 hours.")

    sb = get_supabase_admin()
    session_id = body.session_id
    estimate_context = ""

    # Create new session or load existing
    if not session_id:
        title = _auto_title(body.message)
        session_data = {
            "user_id": user_id,
            "title": title,
            "estimate_id": body.estimate_id,
        }
        resp = sb.table("chat_sessions").insert(session_data).execute()
        session_id = resp.data[0]["id"]
    else:
        # Verify session belongs to user
        resp = sb.table("chat_sessions").select("id, estimate_id, summary").eq("id", session_id).eq("user_id", user_id).single().execute()
        if not resp.data:
            raise HTTPException(status_code=404, detail="Chat session not found.")

    # Get estimate context if linked
    eid = body.estimate_id
    if not eid:
        sess = sb.table("chat_sessions").select("estimate_id").eq("id", session_id).single().execute()
        eid = sess.data.get("estimate_id") if sess.data else None
    if eid:
        estimate_context = _get_estimate_context(eid)

    # Load existing messages
    msgs_resp = sb.table("chat_messages").select("role, content, is_compacted, created_at").eq("session_id", session_id).order("created_at").execute()
    all_messages = msgs_resp.data or []

    # Get session summary
    sess_resp = sb.table("chat_sessions").select("summary, title").eq("id", session_id).single().execute()
    summary = sess_resp.data.get("summary") if sess_resp.data else None
    title = sess_resp.data.get("title", "New Chat") if sess_resp.data else "New Chat"

    # Filter to non-compacted messages
    recent = [m for m in all_messages if not m.get("is_compacted")]

    # Memory compaction: if too many messages, summarize old ones
    if len(recent) >= COMPACTION_THRESHOLD:
        to_compact = recent[:-MAX_RECENT_MESSAGES]
        to_keep = recent[-MAX_RECENT_MESSAGES:]

        # Build new summary
        old_summary = summary or ""
        compact_input = []
        if old_summary:
            compact_input.append({"role": "system", "content": f"Previous summary: {old_summary}"})
        compact_input.extend(to_compact)

        try:
            new_summary = _summarize_messages(compact_input)
            log_usage(user_id, "chat_compact", 0.001, {"session_id": session_id})
        except Exception as e:
            logger.warning("Compaction failed: %s", e)
            new_summary = old_summary

        # Mark old messages as compacted
        old_ids = [m.get("id") for m in to_compact if m.get("id")]
        if old_ids:
            sb.table("chat_messages").update({"is_compacted": True}).in_("id", old_ids).execute()

        # Update session summary
        sb.table("chat_sessions").update({
            "summary": new_summary,
            "summary_token_count": _count_tokens(new_summary),
        }).eq("id", session_id).execute()

        summary = new_summary
        recent = to_keep

    # Get wiki knowledge context based on user's question
    wiki_context = get_wiki_context(body.message)

    # Build AI messages
    ai_messages = _build_messages(
        SYSTEM_PROMPT, estimate_context, wiki_context, summary, recent, body.message
    )

    # Call AI
    try:
        reply = _call_ai(ai_messages)
    except Exception as e:
        logger.exception("Chat AI call failed: %s", e)
        raise HTTPException(status_code=500, detail="Failed to generate response. Please try again.")

    # Save user message + assistant reply
    sb.table("chat_messages").insert([
        {
            "session_id": session_id,
            "role": "user",
            "content": body.message,
            "token_count": _count_tokens(body.message),
        },
        {
            "session_id": session_id,
            "role": "assistant",
            "content": reply,
            "token_count": _count_tokens(reply),
        },
    ]).execute()

    log_usage(user_id, "chat", 0.001, {"session_id": session_id})

    return ChatResponse(reply=reply, session_id=session_id, title=title)


@router.get("/chat/sessions")
@limiter.limit("30/minute")
async def list_sessions(
    request: Request,
    user_id: str = Depends(get_current_user_id),
) -> list[dict]:
    """List user's chat sessions, most recent first."""
    sb = get_supabase_admin()
    resp = sb.table("chat_sessions").select(
        "id, title, estimate_id, updated_at"
    ).eq("user_id", user_id).order("updated_at", desc=True).limit(MAX_SESSIONS_PER_USER).execute()

    sessions = []
    for s in resp.data or []:
        # Get message count
        count_resp = sb.table("chat_messages").select("id", count="exact").eq("session_id", s["id"]).execute()
        sessions.append({
            "id": s["id"],
            "title": s["title"],
            "estimate_id": s.get("estimate_id"),
            "updated_at": s["updated_at"],
            "message_count": count_resp.count or 0,
        })

    return sessions


@router.get("/chat/sessions/{session_id}/messages")
@limiter.limit("30/minute")
async def get_session_messages(
    request: Request,
    session_id: str,
    user_id: str = Depends(get_current_user_id),
) -> dict:
    """Get all messages for a session."""
    sb = get_supabase_admin()

    # Verify ownership
    sess = sb.table("chat_sessions").select("id, title, estimate_id, summary").eq("id", session_id).eq("user_id", user_id).single().execute()
    if not sess.data:
        raise HTTPException(status_code=404, detail="Session not found.")

    msgs = sb.table("chat_messages").select(
        "id, role, content, created_at, is_compacted"
    ).eq("session_id", session_id).order("created_at").execute()

    return {
        "session": sess.data,
        "messages": [m for m in (msgs.data or []) if not m.get("is_compacted")],
    }


@router.delete("/chat/sessions/{session_id}")
@limiter.limit("10/minute")
async def delete_session(
    request: Request,
    session_id: str,
    user_id: str = Depends(get_current_user_id),
) -> dict:
    """Delete a chat session and all its messages."""
    sb = get_supabase_admin()

    # Verify ownership
    sess = sb.table("chat_sessions").select("id").eq("id", session_id).eq("user_id", user_id).single().execute()
    if not sess.data:
        raise HTTPException(status_code=404, detail="Session not found.")

    sb.table("chat_sessions").delete().eq("id", session_id).execute()
    return {"status": "deleted"}

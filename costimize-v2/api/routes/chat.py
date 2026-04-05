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
- ALWAYS answer using the CURRENT ESTIMATE CONTEXT first. When the user asks "why is X cost so high?", compute the math from the estimate data: show the material price/kg, part weight, volume, and how the number was derived. Never give generic textbook answers when estimate data is available.
- Be concise and specific. Use ₹ numbers from the estimate, not vague statements.
- All costs in ₹ (INR) unless user asks otherwise.
- For "why" questions about cost: break down the calculation step-by-step using actual dimensions and material properties from the estimate. Example: "Your part is 150mm OD × 200mm long in Al 6061 (₹315/kg, density 2700 kg/m³). Volume = π/4 × 0.15² × 0.2 = 0.00353 m³. Weight = 9.54 kg. Material cost = 9.54 × ₹315 = ₹3,005. This is 51% of your unit cost because aluminum is 4-5× pricier than mild steel."
- Focus on actionable advice: "Switch to Al 5052 (₹285/kg vs ��315/kg) to save ₹X" or "Reduce OD by 10mm to save ₹X in material"
- If you don't know something, say so. Don't make up costs.
- You understand turning, milling, sheet metal, PCB, and cable assembly processes.
- When a KNOWLEDGE BASE section is provided, use it to give informed, specific answers grounded in the estimate data. Cite facts from it."""


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
    """Fetch estimate data from Supabase and format as context for the chatbot."""
    try:
        sb = get_supabase_admin()
        resp = sb.table("estimates").select("*").eq("id", estimate_id).single().execute()
        est = resp.data
        if not est:
            return ""

        bd = est.get("cost_breakdown") or {}
        extracted = est.get("extracted_data") or {}
        dims = extracted.get("dimensions", {})

        material_name = bd.get('material_name', est.get('material_name', 'Unknown'))

        lines = [
            "=== CURRENT ESTIMATE CONTEXT ===",
            f"Part Type: {est.get('part_type', 'mechanical')}",
            f"Material: {material_name}",
            f"Quantity: {est.get('quantity', 1)}",
            f"Total Unit Cost: ₹{est.get('total_cost', 0):,.2f}",
            f"Confidence: {est.get('confidence_tier', 'unknown')}",
        ]

        # Dimensions — include all for calculation context
        if dims:
            dim_parts = [f"{k}: {v}mm" for k, v in dims.items() if v]
            if dim_parts:
                lines.append(f"Dimensions: {', '.join(dim_parts)}")

        # Material properties — critical for "why is material cost high?" questions
        try:
            from engines.mechanical.material_db import get_material, load_materials
            # Fuzzy match: try exact first, then substring match
            try:
                mat = get_material(material_name)
            except ValueError:
                mat = None
                for k in load_materials():
                    if k.lower() in material_name.lower() or material_name.lower() in k.lower():
                        mat = get_material(k)
                        break
            if mat:
                lines.append(f"\nMaterial Properties ({mat.name}):")
                lines.append(f"  Price: ₹{mat.price_per_kg_inr}/kg")
                lines.append(f"  Density: {mat.density_kg_per_m3} kg/m³")
                if mat.uts_mpa:
                    lines.append(f"  UTS: {mat.uts_mpa} MPa")
                # Compute weight from dimensions if available
                od = dims.get("outer_diameter_mm", 0) or 0
                length = dims.get("length_mm", 0) or 0
                id_mm = dims.get("inner_diameter_mm", 0) or 0
                width = dims.get("width_mm", 0) or 0
                height = dims.get("height_mm", 0) or 0
                import math
                if od > 0 and length > 0:
                    vol_m3 = math.pi / 4 * ((od / 1000) ** 2 - (id_mm / 1000) ** 2) * (length / 1000)
                    weight = vol_m3 * mat.density_kg_per_m3
                    calc_mat_cost = weight * mat.price_per_kg_inr
                    lines.append(f"  Estimated raw weight: {weight:.3f} kg")
                    lines.append(f"  Weight × price = {weight:.3f} × ₹{mat.price_per_kg_inr} = ₹{calc_mat_cost:,.0f}")
                    lines.append(f"  (Material cost includes 15% wastage allowance)")
                elif width > 0 and height > 0 and length > 0:
                    vol_m3 = (width / 1000) * (height / 1000) * (length / 1000)
                    weight = vol_m3 * mat.density_kg_per_m3
                    calc_mat_cost = weight * mat.price_per_kg_inr
                    lines.append(f"  Estimated raw weight: {weight:.3f} kg")
                    lines.append(f"  Weight × price = {weight:.3f} × ₹{mat.price_per_kg_inr} = ₹{calc_mat_cost:,.0f}")
                    lines.append(f"  (Material cost includes 15% wastage allowance)")
        except Exception:
            pass  # non-critical

        # Cost breakdown line items
        lines.append("")
        lines.append("Cost Breakdown:")
        if bd.get("material_cost"):
            lines.append(f"  Material: ₹{bd['material_cost']:,.2f}")
        if bd.get("total_machining_cost"):
            lines.append(f"  Machining: ₹{bd['total_machining_cost']:,.2f}")
        if bd.get("total_setup_cost"):
            lines.append(f"  Setup & Tooling: ₹{bd['total_setup_cost']:,.2f}")
        if bd.get("total_labour_cost"):
            lines.append(f"  Labour: ₹{bd['total_labour_cost']:,.2f}")
        if bd.get("total_power_cost"):
            lines.append(f"  Power: ₹{bd['total_power_cost']:,.2f}")
        if bd.get("overhead"):
            lines.append(f"  Overhead (15%): ₹{bd['overhead']:,.2f}")
        if bd.get("profit"):
            lines.append(f"  Profit (20%): ₹{bd['profit']:,.2f}")

        # Process details
        process_lines = bd.get("process_lines", [])
        if process_lines:
            lines.append("")
            lines.append("Process Details:")
            for p in process_lines:
                name = p.get("process_name", p.get("process_id", "?"))
                time_min = p.get("time_min", 0)
                machine = p.get("machine_cost", 0)
                lines.append(f"  - {name}: {time_min:.1f} min, machine ₹{machine:,.2f}")

        # Cost range
        if bd.get("unit_cost_low") and bd.get("unit_cost_high"):
            lines.append(f"\nShould-Cost Range: ₹{bd['unit_cost_low']:,.0f} – ₹{bd['unit_cost_high']:,.0f}")

        # Supplier quote comparison
        if bd.get("supplier_quote"):
            lines.append(f"Supplier Quote: ₹{bd['supplier_quote']:,.2f}")

        # Assembly estimates have component-level breakdown
        components = bd.get("components")
        if components:
            lines.append("")
            lines.append("Assembly Components:")
            for comp in components:
                lines.append(
                    f"  - {comp.get('name', '?')}: {comp.get('material_name', '?')}, "
                    f"₹{comp.get('unit_cost', 0):,.2f}/unit"
                )
            if bd.get("joining_cost"):
                lines.append(f"  Joining ({bd.get('joining_method', '?')}): ₹{bd['joining_cost']:,.2f}")
            if bd.get("assembly_subtotal"):
                lines.append(f"  Assembly Subtotal: ₹{bd['assembly_subtotal']:,.2f}")

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

    response = model.generate_content(contents, generation_config={"temperature": 0.0})
    return response.text.strip()


def _call_openai(messages: list[dict]) -> str:
    """Call OpenAI API."""
    import openai
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=1000,
        temperature=0.0,
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
        response = model.generate_content(prompt, generation_config={"temperature": 0.0})
        return response.text.strip()

    if OPENAI_API_KEY:
        import openai
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.0,
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
                f"No quotes, no punctuation:\n\n{user_message[:200]}",
                generation_config={"temperature": 0.0},
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

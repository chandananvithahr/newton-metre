# AI Agent & Self-Hosted AI Roadmap
## Newton-Metre — From API-Dependent to Own Tech

> Research date: 2026-04-04
> Status: Strategic roadmap for in-app AI agent + progressive migration off cloud APIs
> North star: Defense/aerospace clients will NOT send drawings to cloud APIs. We must own our AI.

---

## Table of Contents

1. [Why an In-App AI Agent](#1-why-an-in-app-ai-agent)
2. [Agent Architecture](#2-agent-architecture)
3. [Agent Capabilities by Phase](#3-agent-capabilities-by-phase)
4. [The "Own Your AI" Migration Path](#4-the-own-your-ai-migration-path)
5. [Fine-Tuning Roadmap](#5-fine-tuning-roadmap)
6. [Open-Source Models for Each Task](#6-open-source-models-for-each-task)
7. [Self-Hosted Infrastructure](#7-self-hosted-infrastructure)
8. [Cost Comparison: Cloud vs Self-Hosted](#8-cost-comparison-cloud-vs-self-hosted)
9. [Data Collection Strategy](#9-data-collection-strategy)
10. [Defense/On-Prem Deployment](#10-defenseon-prem-deployment)
11. [AI Evals — Measure Everything Before You Ship](#11-ai-evals--measure-everything-before-you-ship)

---

## 1. Why an In-App AI Agent

Newton-Metre's three superpowers — should-cost, similarity search, company brain — are powerful individually. An AI agent **connects them into a single conversational interface:**

- "What's the avg cost of turned aluminum parts we've quoted?" → queries estimates DB
- "Find me similar parts to this drawing" → triggers similarity search
- "Why is this estimate higher than last time?" → compares estimate breakdowns
- "Which supplier gave best price for SS304 turning?" → queries PO history
- Proactive: "This part is similar to PO #1234 which cost Rs 450 — you're quoting Rs 680" → surfaces insights automatically

**No competitor has this.** CADDi has similarity. aPriori has should-cost. Nobody has a conversational agent that ties cost estimation + similarity + company memory together.

---

## 2. Agent Architecture

### Design Principle: LLM-Agnostic Tool Orchestration

The agent is a thin orchestration layer — tool definitions + routing logic — that talks to **any** LLM backend via OpenAI-compatible API. Swapping Gemini → self-hosted Qwen is a config change, not a rewrite.

```
┌─────────────────────────────────────────┐
│  Frontend (Next.js on Vercel)            │
│  ┌───────────────────────────────────┐   │
│  │  Chat Panel (floating/slide-out)  │   │
│  │  - Streaming responses (SSE)      │   │
│  │  - Context-aware (knows which     │   │
│  │    page/estimate user is viewing) │   │
│  │  - Role-based (procurement sees   │   │
│  │    cost data, design sees visual) │   │
│  └──────────┬────────────────────────┘   │
└─────────────┼────────────────────────────┘
              │ POST /api/agent/chat (SSE stream)
              ▼
┌─────────────────────────────────────────┐
│  Backend (FastAPI on Railway)            │
│  ┌───────────────────────────────────┐   │
│  │  Agent Router (api/agent/)        │   │
│  │  - Intent classification          │   │
│  │  - Tool selection via LLM         │   │
│  │  - Conversation memory (Supabase) │   │
│  └──────────┬────────────────────────┘   │
│             ▼                            │
│  ┌───────────────────────────────────┐   │
│  │  Tool Functions                    │   │
│  │  - search_estimates()             │   │
│  │  - find_similar_parts()           │   │
│  │  - calculate_cost()               │   │
│  │  - get_supplier_history()         │   │
│  │  - explain_cost_breakdown()       │   │
│  │  - query_knowledge_graph()        │   │
│  │  - generate_sql()                 │   │
│  └──────────┬────────────────────────┘   │
│             ▼                            │
│  ┌───────────────────────────────────┐   │
│  │  LLM Backend (swappable)          │   │
│  │  Phase 1: Gemini Flash (cloud)    │   │
│  │  Phase 2: Qwen2.5-32B (RunPod)   │   │
│  │  Phase 3: Fine-tuned Qwen (prem) │   │
│  └───────────────────────────────────┘   │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│  Supabase (Postgres + pgvector)          │
│  - estimates, parts, suppliers           │
│  - embeddings for similarity             │
│  - conversations table (agent memory)    │
│  - usage_log (all agent interactions)    │
└─────────────────────────────────────────┘
```

### Backend Code Pattern

```python
# api/agent/router.py

AGENT_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_estimates",
            "description": "Search past cost estimates by material, process, part description, or date range",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "material": {"type": "string", "description": "Material filter (e.g. SS304, EN8, Aluminum 6061)"},
                    "process": {"type": "string", "description": "Process filter (e.g. turning, milling, sheet metal)"},
                    "min_cost": {"type": "number"},
                    "max_cost": {"type": "number"},
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "find_similar_parts",
            "description": "Find visually similar parts from the company drawing library",
            "parameters": {
                "type": "object",
                "properties": {
                    "part_id": {"type": "string", "description": "Estimate/part ID to find similar parts for"},
                    "top_k": {"type": "integer", "default": 5}
                },
                "required": ["part_id"]
            }
        }
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
                    "supplier_name": {"type": "string"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "explain_cost_breakdown",
            "description": "Get detailed line-by-line cost breakdown for an estimate and explain each cost driver",
            "parameters": {
                "type": "object",
                "properties": {
                    "estimate_id": {"type": "string"}
                },
                "required": ["estimate_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_quick_cost",
            "description": "Quick cost estimate from natural language description without a drawing",
            "parameters": {
                "type": "object",
                "properties": {
                    "description": {"type": "string", "description": "Part description (material, dimensions, processes)"},
                    "quantity": {"type": "integer", "default": 1}
                },
                "required": ["description"]
            }
        }
    }
]


async def agent_chat(message: str, context: dict, user_id: str, conversation_id: str):
    """
    Main agent entry point.
    context = {page: "estimate_detail", estimate_id: "abc123", ...}
    """
    system_prompt = build_system_prompt(context, user_id)
    history = await load_conversation(conversation_id)

    # Call LLM with tools (works with Gemini, OpenAI, or local vLLM)
    response = await llm_client.chat(
        messages=[{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}],
        tools=AGENT_TOOLS,
    )

    # Execute tool calls if any
    if response.tool_calls:
        tool_results = await execute_tools(response.tool_calls, user_id)
        # Feed results back for final answer
        final = await llm_client.chat(
            messages=[...history, message, response, tool_results],
            tools=AGENT_TOOLS,
        )
        return final

    return response
```

### Frontend Component

```tsx
// Floating chat panel — context-aware
// Knows which page the user is on and pre-loads relevant data
// Streams responses via SSE for real-time feel
// Stores conversation history per user in Supabase
```

### Key Design Decisions

- **No LangChain/LlamaIndex dependency** — raw tool-calling is simpler, more debuggable, zero vendor lock-in
- **OpenAI-compatible API format** — Gemini, vLLM, Ollama all support this, so model swapping is config-only
- **Context injection** — agent knows what page the user is viewing and pre-loads relevant data
- **Conversation persistence** — stored in Supabase `conversations` table, not in-memory
- **Budget integration** — agent calls count against the per-user $0.50/48h cap

---

## 3. Agent Capabilities by Phase

### Phase 1: Basic Chat Agent (2-3 days)

- `/api/agent/chat` endpoint in FastAPI
- Gemini Flash with function calling (already have API key)
- 5 tools: search_estimates, find_similar, get_supplier_history, explain_breakdown, calculate_quick_cost
- Floating chat button → slide-out panel with streaming
- Conversations stored in Supabase
- Context-aware: knows which estimate/page user is viewing

### Phase 2: Context-Aware Agent (3-5 days)

- Proactive suggestions: "I found 3 similar parts in your history"
- SQL generation for ad-hoc queries ("show me all SS304 parts over Rs 500")
- Cost comparison: "This estimate is 20% higher than your last similar part"
- Page-aware pre-loading: on estimate detail page, agent auto-loads that estimate's data

### Phase 3: Company Brain Agent (1-2 weeks)

- RAG over knowledge graph (parts → materials → processes → costs → suppliers)
- Multi-step reasoning: "Find cheaper alternatives for this part" → search materials → recalculate → compare suppliers
- Role-based responses: procurement sees cost/supplier data, engineering sees process/tolerance data
- Anomaly detection: "This quote is 2x your historical average for similar parts"
- Supplier ranking: "For SS304 turning, Supplier A averages Rs 380 vs Supplier B at Rs 520"

### Phase 4: Autonomous Agent (future)

- Auto-generate RFQ documents from estimates
- Supplier matching and outreach recommendations
- Cost trend analysis and forecasting
- "Draft a negotiation email based on this should-cost breakdown"

---

## 4. The "Own Your AI" Migration Path

### The Problem

Today Newton-Metre depends on:
- **Gemini Flash/Pro** — extraction reasoning, agent brain, RFQ extraction
- **GPT-4o** — fallback vision extraction
- **Gemini Embedding 2** — similarity embeddings

This creates three risks:
1. **Defense clients won't use it** — they will not send proprietary drawings to Google/OpenAI cloud APIs
2. **Margin erosion** — API costs scale linearly with usage, eating into margins
3. **No moat** — anyone can wrap the same APIs

### The Solution: Progressive Self-Hosting

```
TODAY (API-dependent)          →  6 MONTHS (hybrid)              →  12 MONTHS (own tech)
                                                                  
Gemini Flash (agent)           →  Qwen2.5-32B on RunPod          →  Fine-tuned Qwen2.5-32B on-prem
GPT-4o/Gemini (extraction)     →  Fine-tuned Qwen2.5-VL-7B       →  Fine-tuned on-prem
Gemini Embedding 2             →  DINOv2 + nomic-embed            →  Fine-tuned DINOv2 on-prem
Gemini (validation/arbitrator) →  Qwen2.5-7B for simple checks   →  Fine-tuned specialist
                                                                  
$50-200/mo API costs           →  $50-150/mo RunPod serverless   →  $30-150/mo own hardware
No defense clients             →  RunPod = still cloud            →  Ship GPU box to defense client
```

### Migration Rules

1. **Every AI call must go through a swappable interface** — never call Gemini/OpenAI directly from business logic
2. **Log every interaction** — input, model output, user correction = free training data
3. **Fine-tune extraction first** — highest API cost, most defensible IP
4. **Agent LLM last** — base models already handle tool-calling well
5. **Keep cloud fallback** — self-hosted model down? Fall back to Gemini. Never lose uptime.

---

## 5. Fine-Tuning Roadmap

### Priority Order (Highest ROI First)

#### Phase 1: Drawing Extraction — Month 1-2

| Item | Detail |
|------|--------|
| **Model** | Qwen2.5-VL-7B |
| **Task** | Image → structured JSON (dimensions, tolerances, material, processes, surface finish) |
| **Data needed** | 200-500 annotated drawings (good), 1000+ (excellent) |
| **Data source** | Every cloud API extraction = free training pair. User corrections = gold labels |
| **Method** | QLoRA (rank 16-32, 4-bit quantization) |
| **Hardware** | RunPod A100 80GB ($1.64/hr) × 4-8 hours |
| **Cost** | $7-13 per training run |
| **Why first** | Highest API cost per call. Every drawing creates training data automatically. Most defensible IP |
| **Result** | Replace GPT-4o/Gemini vision calls entirely. Extraction runs locally |

#### Phase 2: Visual Embeddings — Month 2-3

| Item | Detail |
|------|--------|
| **Model** | DINOv2-ViT-B/14 (visual) + nomic-embed-text-v1.5 or gte-large-en-v1.5 (text) |
| **Task** | Drawing → 768-dim vector that captures visual + semantic similarity |
| **Data needed** | 500+ drawing pairs with similarity labels (same/different part type, material, process) |
| **Data source** | User feedback on similarity search results ("this match is good" / "this is wrong") |
| **Method** | Contrastive loss fine-tune. Full fine-tune OK for ViT-B (86M params) |
| **Hardware** | RunPod A100 × 2-3 hours |
| **Cost** | $3-5 per training run |
| **Why second** | Similarity search quality directly impacts "company brain" value prop. DINOv2 is 2.3x better than CLIP baseline but fine-tuning on manufacturing drawings will add another 20-30% |

#### Phase 3: Agent LLM — Month 4-6

| Item | Detail |
|------|--------|
| **Model** | Qwen2.5-32B-Instruct |
| **Task** | Conversational agent with reliable tool-calling for manufacturing domain |
| **Data needed** | 500-1000 conversation traces with tool calls |
| **Data source** | Every cloud agent conversation = training data. Log tool selections + user corrections |
| **Method** | QLoRA (rank 32-64, 4-bit) |
| **Hardware** | RunPod A100 80GB × 8-16 hours |
| **Cost** | $13-26 per training run |
| **Why last** | Base Qwen2.5-32B already handles tool-calling well. Fine-tuning adds domain knowledge ("when user says 'check this part' call search_estimates, not calculate_cost") |

#### Phase 4: Validation & Arbitrator — Month 6+

| Item | Detail |
|------|--------|
| **Model** | Qwen2.5-7B-Instruct (small, fast) |
| **Task** | Compare physics estimate vs AI estimate, flag discrepancies, explain deltas |
| **Data needed** | 300+ validated estimate comparison pairs (already collecting in data/validation/) |
| **Method** | QLoRA |
| **Cost** | $5-10 |
| **Why** | Replace Gemini in the validation pipeline. Small model is fine — it's comparing two numbers and explaining the gap |

### Data Collection Strategy (Start NOW)

Every cloud API call is a training example waiting to happen:

```python
# Log every extraction
{
    "input_image": "path/to/drawing.png",
    "model_output": {"dimensions": {...}, "material": "SS304", ...},
    "user_corrections": {"material": "SS316"},  # If user edited
    "timestamp": "2026-04-04T10:30:00Z",
    "model_used": "gemini-1.5-flash",
    "confidence": 0.87
}

# Log every agent conversation
{
    "user_message": "find similar parts to this shaft",
    "tool_calls": [{"name": "find_similar_parts", "args": {"part_id": "est_123"}}],
    "tool_results": [...],
    "final_response": "I found 3 similar parts...",
    "user_feedback": "thumbs_up",  # or correction
    "timestamp": "2026-04-04T10:31:00Z"
}

# Log every similarity search feedback
{
    "query_drawing_id": "draw_456",
    "results": ["draw_789", "draw_012", ...],
    "user_confirmed_match": "draw_789",
    "user_rejected": ["draw_012"],
    "timestamp": "2026-04-04T10:32:00Z"
}
```

**Supabase tables needed:**
- `training_extractions` — extraction input/output/correction triples
- `training_conversations` — agent conversation traces with tool calls
- `training_similarity` — similarity search feedback (confirmed/rejected matches)

---

## 6. Open-Source Models for Each Task

### Agent / Tool-Calling Models

| Model | Size | Tool-Calling Quality | VRAM (4-bit) | Notes |
|-------|------|---------------------|--------------|-------|
| **Qwen2.5-72B-Instruct** | 72B | Excellent — top-3 on Berkeley Function-Calling Leaderboard | 40GB | Best open-source for tool use |
| **Qwen2.5-32B-Instruct** | 32B | Very good | 20GB | **Sweet spot** — single GPU, reliable tools |
| **Llama 3.3-70B-Instruct** | 70B | Good | 40GB | Solid but Qwen edges it on structured output |
| **Mistral-Small-24B (2501)** | 24B | Good | 14GB | Function-calling trained, fits smaller GPUs |
| **Qwen2.5-7B-Instruct** | 7B | Acceptable for simple routing | 5GB | Min viable — 3-5 tools max, breaks on complex chains |

**Minimum reliable size for tool use: 32B.** The 7B models can route to simple tools but fail on multi-step reasoning or deciding NOT to call a tool.

**Recommendation: Qwen2.5-32B-Instruct (AWQ 4-bit).** Single A6000 (48GB), handles 5-8 tools reliably, strong English + technical content in training data.

### Vision / Extraction Models

| Model | Size | Task | VRAM | Notes |
|-------|------|------|------|-------|
| **Qwen2.5-VL-7B** | 7B | Drawing → structured JSON | 5GB (4-bit) | Beats GPT-4o on document understanding |
| **Florence-2-large** | 0.77B | Drawing → dimensions/GD&T | 2GB | +52% F1 vs GPT-4o when fine-tuned on 400 drawings |
| **GLM-OCR (CogAgent2)** | 0.9B | Raw text/table extraction | 1GB | 96.1% text accuracy. Pre-processing layer |

### Embedding Models

| Model | Size | Dim | Task | VRAM |
|-------|------|-----|------|------|
| **DINOv2-ViT-B/14** | 86M | 768 | Visual similarity | 0.4GB |
| **nomic-embed-text-v1.5** | 137M | 768 | Text similarity | 0.3GB |
| **ColFlor** | 174M | 128×N | Late interaction retrieval | 0.7GB |
| **gte-large-en-v1.5** | 434M | 1024 | Text similarity (higher quality) | 1GB |

### Validation / Small Tasks

| Model | Size | Task | VRAM |
|-------|------|------|------|
| **Qwen2.5-7B-Instruct** | 7B | Estimate comparison, simple Q&A | 5GB |
| **Phi-3.5-mini** | 3.8B | Classification, routing | 2.5GB |

---

## 7. Self-Hosted Infrastructure

### Target Architecture: Single GPU Box

```
GPU: 1x NVIDIA A6000 (48GB VRAM) — ~$4,500 used, or ~$0.80/hr RunPod
     OR 1x RTX 4090 (24GB) for tighter budget (~$1,800)

┌──────────────────────────────────────────────┐
│  vLLM Server (port 8001)                     │
│  ├── Qwen2.5-VL-7B-AWQ (extraction) — 5GB   │
│  ├── Qwen2.5-32B-AWQ (agent) — 20GB         │
│  └── Multi-model or swap on demand           │
├──────────────────────────────────────────────┤
│  TEI Server (port 8002)                      │  (HuggingFace Text Embeddings Inference)
│  ├── DINOv2-ViT-B/14 — 0.4GB                │
│  └── nomic-embed-text-v1.5 — 0.3GB          │
├──────────────────────────────────────────────┤
│  ColFlor Server (port 8003) — 0.7GB          │
│  Late-interaction retrieval for on-prem       │
└──────────────────────────────────────────────┘
Total active VRAM: ~26GB (fits A6000)
With RTX 4090: swap agent ↔ extraction, +10s latency
```

### Why vLLM

- **Paged attention** — efficient memory management
- **Continuous batching** — handles concurrent requests
- **OpenAI-compatible API** — drop-in replacement for cloud APIs
- **AWQ/GPTQ quantization** — run larger models on smaller GPUs
- **Multi-model support** — serve multiple models from one instance

### Inference Server Comparison

| Server | Pros | Cons | Use Case |
|--------|------|------|----------|
| **vLLM** | Fast, batching, OpenAI API | More setup | Production |
| **Ollama** | Dead simple, one command | No batching, slower | Dev/testing |
| **TGI** | Solid, HuggingFace native | vLLM has won ecosystem | Backup option |
| **llama.cpp** | Runs on CPU, minimal deps | Slow for large models | Edge/embedded |

### RunPod Serverless (Intermediate Step)

Before owning hardware, use RunPod serverless:
- Pay per second of inference
- Auto-scales to zero when idle
- Cold start: 15-30s (acceptable for non-real-time)
- Cost: $50-150/mo at moderate usage
- Supports custom Docker images with your fine-tuned models

---

## 8. Cost Comparison: Cloud vs Self-Hosted

### Per-Request Costs

| Task | Cloud API | Self-Hosted (RunPod) | Self-Hosted (Own GPU) |
|------|-----------|---------------------|----------------------|
| Drawing extraction | $0.002-0.01 | $0.0003 | $0.0001 |
| Agent conversation (5 turns) | $0.01-0.03 | $0.002 | $0.0005 |
| Similarity embedding | $0.005 | $0.0001 | $0.00003 |
| Validation check | $0.003 | $0.0004 | $0.0001 |

### Monthly Costs at Scale

| Users | Cloud APIs | RunPod Serverless | RunPod Always-On | Own A6000 (colo) | Own 4090 (office) |
|-------|-----------|-------------------|-------------------|-----------------|-------------------|
| 10 | $50-100 | $30-50 | $580 | $150 | $30 |
| 100 | $200-500 | $80-150 | $580 | $150 | $30 |
| 1,000 | $2,000-5,000 | $500-1,000 | $580 | $150 | $30 |
| 10,000 | $20,000-50,000 | $3,000-8,000 | $1,160 (2 GPUs) | $300 | $60 |

**Breakeven: ~50-100 active users** for RunPod serverless vs cloud APIs.
**Breakeven: ~200-500 active users** for own hardware vs RunPod.

---

## 9. Data Collection Strategy

### What to Collect (Start NOW — Every API Call is Training Data)

| Data Type | Source | Training Use | Storage |
|-----------|--------|-------------|---------|
| Extraction pairs | Every drawing → JSON extraction | Fine-tune Qwen2.5-VL-7B | `training_extractions` table |
| User corrections | When users edit extracted values | Gold labels for fine-tuning | Same table, `corrections` column |
| Agent conversations | Every chat interaction + tool calls | Fine-tune agent LLM | `training_conversations` table |
| Similarity feedback | User confirms/rejects search results | Fine-tune embeddings via contrastive loss | `training_similarity` table |
| Estimate-vs-actual | When PO history shows real cost | ML correction factors | `data/validation/` (existing) |
| Process route confirmations | When users confirm/change detected processes | Process detection model | `training_processes` table |

### Data Milestones

| Milestone | What It Unlocks |
|-----------|----------------|
| **50 corrected extractions** | Can evaluate fine-tune quality vs baseline |
| **200 extractions** | First viable fine-tune of Qwen2.5-VL-7B |
| **500 similarity feedback pairs** | First viable embedding fine-tune |
| **500 agent conversations** | First viable agent fine-tune |
| **1,000 extractions + corrections** | Production-quality extraction model |
| **100 estimate-vs-actual pairs** | First XGBoost correction model (see ML-STRATEGY) |

### Annotation Pipeline

```
User uploads drawing
    → Cloud API extracts (Gemini/GPT-4o)
    → User reviews extracted values
    → User corrects any mistakes
    → (image, extraction, corrections) saved as training triple
    → After 200+ triples: fine-tune Qwen2.5-VL-7B
    → Fine-tuned model replaces cloud API
    → Continue collecting corrections → re-fine-tune quarterly
```

---

## 10. Defense/On-Prem Deployment

### The Defense Sales Trigger

When a defense client says "we'll buy if it's on-prem":

1. **Buy an RTX 4090** ($1,800) or A6000 ($4,500)
2. Install Ubuntu + vLLM + your fine-tuned models
3. Pre-load their drawing library
4. Ship the box to their facility
5. Connect to their internal network (no internet needed)

**Total hardware cost: $1,800-4,500 = one month of enterprise subscription.**

### On-Prem Stack

```
┌────────────────────────────────────────┐
│  Customer's Network (air-gapped OK)    │
│                                        │
│  GPU Box (RTX 4090 / A6000)            │
│  ├── Ubuntu 22.04 LTS                  │
│  ├── vLLM (extraction + agent models)  │
│  ├── TEI (embedding models)            │
│  ├── FastAPI (Newton-Metre backend)    │
│  ├── PostgreSQL + pgvector             │
│  └── Next.js (frontend, static build)  │
│                                        │
│  Everything runs on one box.           │
│  No internet. No cloud APIs.           │
│  Their data never leaves their network.│
└────────────────────────────────────────┘
```

### Model Sizing for On-Prem

| GPU | Agent Model | Extraction Model | Embeddings | Total |
|-----|------------|------------------|-----------|-------|
| **RTX 4090 (24GB)** | Qwen2.5-14B-AWQ (9GB) | Qwen2.5-VL-7B-AWQ (5GB) | DINOv2+nomic (0.7GB) | 14.7GB ✓ |
| **A6000 (48GB)** | Qwen2.5-32B-AWQ (20GB) | Qwen2.5-VL-7B-AWQ (5GB) | DINOv2+nomic (0.7GB) | 25.7GB ✓ |
| **2x RTX 4090** | Qwen2.5-32B-AWQ (20GB split) | Qwen2.5-VL-7B-AWQ (5GB) | All (1.4GB) | 26.4GB ✓ |

### ColFlor for Defense

ColFlor (174M params) is specifically chosen for defense on-prem:
- 17x smaller than ColPali
- Fits 8GB RAM
- Only 1.8% quality drop
- Late-interaction retrieval = better precision than single-vector
- No cloud API calls for similarity search

---

## Timeline Summary

| Month | Action | Cost | Milestone |
|-------|--------|------|-----------|
| **Now** | Build agent with Gemini Flash. Log ALL interactions | $0 extra | Agent MVP live |
| **Month 1** | Collect 200+ annotated drawings from beta users | $0 | Training data ready |
| **Month 2** | LoRA fine-tune Qwen2.5-VL-7B on RunPod | $15 | Own extraction model |
| **Month 3** | Deploy extraction on RunPod serverless. Keep agent on cloud | $50-80/mo | 50% less API spend |
| **Month 4** | Fine-tune DINOv2 embeddings | $5 | Own similarity engine |
| **Month 5** | Collect 500+ agent traces, fine-tune Qwen2.5-32B | $25 | Own agent brain |
| **Month 6** | Full self-hosted stack on RunPod | $150-580/mo | Zero API dependency |
| **Month 9** | First defense on-prem deployment | $1,800-4,500 | Defense revenue |
| **Month 12** | Re-fine-tune all models on 2000+ data points | $50 | Continuously improving |

**Total fine-tuning investment: ~$50-80 in compute over 6 months.**
**Total hardware for defense on-prem: $1,800-4,500 per deployment.**

---

## Competitive Moat Created

By month 12, Newton-Metre will have:

1. **Own extraction model** — fine-tuned on Indian manufacturing drawings (BIS grades, Hindi title blocks, IS standards). No competitor has this data.
2. **Own similarity embeddings** — fine-tuned on real manufacturing part pairs with user feedback. Quality gap widens with every search.
3. **Own agent brain** — understands manufacturing domain, tool-calling patterns, Indian terminology. No generic LLM can replicate this.
4. **On-prem deployment capability** — defense clients locked out of cloud-only competitors (aPriori, CADDi).
5. **Proprietary training data** — every user interaction makes the models better. This data doesn't exist anywhere else.

**The cloud APIs got us started. The fine-tuned models are the moat.**

---

## 11. AI Evals — Measure Everything Before You Ship

> Inspired by Andrej Karpathy's autoresearch pattern: modify → measure → keep/discard → repeat.
> You don't improve what you don't measure. Evals are the foundation.

### The Autoresearch Pattern (Karpathy, March 2026)

**Repo:** [github.com/karpathy/autoresearch](https://github.com/karpathy/autoresearch) (MIT license)

Karpathy's key insight: give an AI coding agent a small training setup, let it experiment autonomously. The agent modifies code, trains for 5 minutes, checks if the metric improved, keeps or discards the change, and repeats. ~12 experiments/hour, ~100 experiments overnight on a single GPU.

**The 3 files:**
- `prepare.py` — fixed data prep + eval utilities (agent never touches this)
- `train.py` — the single file the agent edits (model, optimizer, hyperparams)
- `program.md` — instructions for the agent (the "research org code" that YOU iterate on)

**The paradigm shift:** You're not writing Python anymore. You're writing `program.md` — a markdown file that programs the AI agent's research strategy. The human's job shifts from coding to designing the research program.

**How Newton-Metre applies this:**
1. **Prompt optimization** — agent modifies extraction prompt → measures field accuracy → keeps if improved
2. **Fine-tune hyperparameter search** — agent modifies LoRA rank/lr/epochs → measures val loss → keeps best
3. **Agent tool-calling optimization** — agent modifies system prompt → measures tool selection accuracy → keeps if improved
4. **Embedding strategy** — agent modifies preprocessing/chunking → measures Recall@5 → keeps best

### Eval Framework: promptfoo (Primary) + deepeval (Python)

**Why promptfoo:**
- CLI + YAML config. `promptfoo init`, define test cases, run `promptfoo eval`
- Compares models side-by-side (Gemini vs fine-tuned Qwen — exact same test cases)
- Built-in assertions: JSON schema validation, field-level matching, similarity scores, cost tracking
- CI/CD integration (GitHub Actions — run evals on every prompt/model change)
- Red-teaming / security scanning built-in
- Free, MIT license (now OpenAI-owned, still open-source)

**Why deepeval (supplement):**
- Python-native, pytest-style (`pip install deepeval`)
- 14+ metrics: faithfulness, hallucination, tool correctness, JSON correctness
- LLM-as-judge (uses GPT-4o to grade outputs for subjective quality)
- Regression tracking dashboard

### Eval Setup Per AI Task

#### 1. Extraction Quality (Drawing → Structured JSON)

```yaml
# promptfoo config for extraction evals
prompts:
  - "Extract dimensions, material, processes from this drawing: {{image}}"

providers:
  - id: gemini-1.5-flash   # Cloud API (baseline)
  - id: openai:qwen-vl     # Self-hosted via vLLM (OpenAI-compatible)

tests:
  - vars:
      image: "test_drawings/shaft_ss304.png"
    assert:
      - type: is-json
      - type: javascript
        value: "output.material === 'SS304'"
      - type: javascript
        value: "Math.abs(output.dimensions.diameter - 25.0) < 0.5"
      - type: javascript
        value: "output.processes.includes('turning')"
```

**Golden dataset:** 20-50 drawings with hand-verified JSON output.

**Metrics:**
- **Field accuracy %** = correct fields / total fields per drawing
- **Material accuracy** — exact match (most important single field)
- **Dimension accuracy** — within ±0.5mm of ground truth
- **Process detection F1** — precision × recall on detected processes
- **Schema compliance** — does output match expected JSON structure?

**Target:** Fine-tuned model must match or beat cloud API on all metrics before swapping.

#### 2. Agent Tool-Calling Accuracy

```python
# deepeval test for agent tool-calling
from deepeval.metrics import ToolCorrectnessMetric
from deepeval.test_case import LLMTestCase

test_case = LLMTestCase(
    input="find similar parts to estimate est_123",
    actual_output=agent_response,
    expected_tools=["find_similar_parts"],
    expected_tool_args={"part_id": "est_123"},
)

metric = ToolCorrectnessMetric(threshold=0.8)
metric.measure(test_case)
```

**Test cases (minimum 50):**
- "What's the cost breakdown for this part?" → should call `explain_cost_breakdown`
- "Find me similar parts" → should call `find_similar_parts`
- "How does this compare to last time?" → should call `search_estimates` + `find_similar_parts`
- "Just chatting, no tool needed" → should NOT call any tool (important edge case)

**Metrics:**
- **Tool selection accuracy** — called the right tool?
- **Argument accuracy** — passed correct parameters?
- **No-tool accuracy** — correctly abstained when no tool was needed?
- **Multi-tool accuracy** — for queries needing 2+ tools, called all of them?

#### 3. Similarity Search Quality

```python
# Simple eval script — no framework needed
import numpy as np

# Ground truth: for each query drawing, list of known similar drawings
ground_truth = {
    "draw_001": ["draw_045", "draw_078", "draw_123"],
    "draw_002": ["draw_089", "draw_156"],
    # ... 20+ queries
}

def recall_at_k(results: list, relevant: list, k: int) -> float:
    """What fraction of relevant items appear in top-k results?"""
    top_k = set(results[:k])
    return len(top_k & set(relevant)) / len(relevant)

def precision_at_k(results: list, relevant: list, k: int) -> float:
    """What fraction of top-k results are relevant?"""
    top_k = set(results[:k])
    return len(top_k & set(relevant)) / k

def ndcg_at_k(results: list, relevant: list, k: int) -> float:
    """Normalized Discounted Cumulative Gain — rewards relevant results appearing earlier."""
    dcg = sum(1 / np.log2(i + 2) for i, r in enumerate(results[:k]) if r in relevant)
    idcg = sum(1 / np.log2(i + 2) for i in range(min(len(relevant), k)))
    return dcg / idcg if idcg > 0 else 0.0

# Run for each embedding model
for model_name, search_fn in [("gemini_embed", gemini_search), ("dinov2", dinov2_search)]:
    recalls, precisions, ndcgs = [], [], []
    for query, relevant in ground_truth.items():
        results = search_fn(query, top_k=10)
        recalls.append(recall_at_k(results, relevant, 5))
        precisions.append(precision_at_k(results, relevant, 5))
        ndcgs.append(ndcg_at_k(results, relevant, 10))
    print(f"{model_name}: R@5={np.mean(recalls):.3f} P@5={np.mean(precisions):.3f} NDCG@10={np.mean(ndcgs):.3f}")
```

**Ground truth dataset:** 20+ query drawings, each with 3-5 known similar parts (manually verified by domain expert).

**Metrics:**
- **Recall@5** — how many relevant parts found in top 5? (most important)
- **Precision@5** — how many of top 5 are actually relevant?
- **NDCG@10** — are relevant results ranked higher?

#### 4. Fine-Tuned vs Cloud API (A/B Comparison)

```bash
# promptfoo makes this trivial — same test cases, two providers
promptfoo eval --config extraction-eval.yaml \
  --provider "gemini-1.5-flash" \
  --provider "openai:http://localhost:8001/v1:qwen-vl-7b"

# Output: side-by-side comparison table with pass/fail per assertion
```

**Decision rule:** Fine-tuned model replaces cloud API when:
1. Field accuracy ≥ cloud API accuracy (no regression)
2. Latency ≤ 2x cloud API latency
3. Cost ≤ 50% of cloud API cost
4. All schema compliance tests pass

### Implementing the Autoresearch Loop

Apply Karpathy's pattern to continuously improve Newton-Metre's AI:

```
┌─────────────────────────────────────────┐
│  The Newton-Metre Autoresearch Loop     │
│                                         │
│  1. Define eval suite (golden dataset)  │
│  2. Run baseline: measure all metrics   │
│  3. Agent proposes change:              │
│     - Modified extraction prompt        │
│     - Different LoRA rank               │
│     - Updated system prompt             │
│     - New embedding preprocessing       │
│  4. Run eval suite again                │
│  5. Compare to baseline                 │
│  6. Keep if improved, discard if not    │
│  7. Repeat from step 3                  │
└─────────────────────────────────────────┘
```

**Practical implementation:**
- Store golden datasets in `costimize-v2/evals/` directory
- `evals/extraction/` — 50 drawing images + expected JSON
- `evals/agent/` — 50 conversation inputs + expected tool calls
- `evals/similarity/` — 20 query drawings + known similar matches
- Run `promptfoo eval` before every prompt change or model swap
- Run similarity evals before every embedding model change
- Automate via GitHub Actions: PR that changes a prompt → eval suite runs → blocks merge if regression

### Eval Infrastructure Roadmap

| When | What | Tool | Effort |
|------|------|------|--------|
| **Now** | Install promptfoo, create 20 extraction test cases | promptfoo | 2 hours |
| **Week 1** | Add agent tool-calling test cases (50) | deepeval | 3 hours |
| **Week 2** | Build similarity search ground truth (20 queries) | Python script | 4 hours |
| **Month 1** | GitHub Actions CI: eval on every prompt change | promptfoo CI | 2 hours |
| **Month 2** | Run first fine-tuned vs cloud A/B comparison | promptfoo | 1 hour |
| **Month 3** | Autoresearch loop for prompt optimization | Karpathy pattern | 1 day |
| **Ongoing** | Expand golden datasets as users provide corrections | All | Continuous |

### What NOT to Build for Evals

| Temptation | Why Not |
|-----------|---------|
| Custom eval framework | promptfoo + deepeval handle everything. Don't reinvent. |
| Massive eval datasets (1000+) | 20-50 golden examples is enough to catch regressions. Scale later. |
| Real-time eval dashboard | Overkill for solo founder. CLI output + GitHub Actions is sufficient. |
| Human eval crowd-sourcing | You ARE the domain expert. Your 20 hand-verified examples > 1000 crowd-labeled ones. |

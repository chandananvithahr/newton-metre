# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Design System

**IMPORTANT:** When implementing any UI from Stitch designs, always read `DESIGN.md` first.
`DESIGN.md` is the ground truth for all colors, typography, spacing, and component styles.
Treat Stitch HTML + screenshot as a constraint — do NOT rewrite layout logic or substitute values.
Always pull the screen screenshot alongside the HTML and match it pixel-for-pixel.

## Project Overview

Newton-Metre — "Know what it costs. Before they quote." A manufacturing **Company Brain** with three products that form a flywheel:

| Product | Role | What It Does |
|---------|------|-------------|
| **Should-cost estimation** | The sexy product (door-opener) | Upload a drawing → line-by-line cost breakdown in 30 seconds. ±5-10% accuracy for mechanical, sheet metal, PCB, cable. The demo moment that gets people in the door. |
| **Similarity search** | The weapon (platform foundation) | Turns a company's drawing history into a searchable asset. Serves 7 departments (design, procurement, QA, sales, marketing, logistics, import/export). Creates data moat — once 50K drawings indexed with PO history, nobody switches. |
| **AI Procurement Worker** | The cash cow (recurring revenue) | AI WORKER (not copilot) that handles RFQ, quote comparison, negotiation, proposals. Class C items (60-70% of POs) autonomously. 2-3% savings on ₹50Cr spend = ₹1-1.5 Cr/year. Every negotiation compounds the memory. |

**The flywheel:** Should-cost gets them in → Similarity makes them stay & spreads across departments → AI Worker generates recurring revenue → More data → better search → better negotiations → more savings.

Built for Indian manufacturing economics (₹ currency, INR pricing).

**Target industries:** Defense, Aerospace, Automobile
**Target part types:** Turned, Milled, Sheet metal
**Users:** Sourcing & procurement, cost engineering, design engineering, QA, sales, marketing, logistics, and leadership teams at manufacturing companies.

**Core value:** "Upload a drawing. Get a line-by-line should-cost. Find similar parts from your history. Negotiate with data."

**Product vision:** Nobody else has all three. CADDi ($1.4B) does similarity only. aPriori does should-cost only (3D required). Pactum does negotiation only. Nobody combines should-cost + similarity + institutional memory + AI procurement worker from 2D drawings.

**Critical insight (70/30 split):** 70% of procurement spend is off-the-shelf MPN-based items (connectors, fasteners, bearings) — where similarity search + negotiation intelligence matters most. Only 30% is manufactured-to-drawing parts where should-cost shines. The AI must serve both.

**AI independence roadmap:** Currently API-dependent (Gemini/GPT-4o). Progressively migrating to own fine-tuned models: GLM-OCR 0.9B (text extraction), Qwen2.5-VL-7B (vision extraction), Gemma 4 (agent/reasoning, replaces Qwen2.5-32B plan), DINOv2 (embeddings), TimesFM 2.5 (forecasting). Target: zero cloud API dependency by month 6, on-prem deployable for defense by month 9. See `costimize-v2/docs/research/AI-AGENT-ROADMAP.md` for full strategy.

See `docs/POSITIONING.md` for full multi-audience messaging and one-liners.

## Live Deployment

| Service | URL |
|---------|-----|
| **Frontend** | https://frontend-theta-ecru-95.vercel.app |
| **Backend API** | https://costimize-api-production.up.railway.app |
| **API Health** | https://costimize-api-production.up.railway.app/api/health |
| **Supabase** | project ypzeffbhlslonqmqiaeh |
| **GitHub** | https://github.com/chandananvithahr/newton-metre (PUBLIC — renamed from costimize-mvp, made public 2026-03-31 for YC Startup School India) |

## Repository Structure

### `frontend/` — Next.js Web App (Vercel)

13 pages: landing, login/signup, dashboard (3-card: should-cost, similarity, chat), new estimate (single + assembly with ZIP upload), estimate detail, similarity search, library (indexed drawings with stats), MPN part search, workflows (new/list/detail), full-page chat, and waitlist. **Split-screen layout:** all authenticated pages have a fixed 380px ChatPanel on the right (ChatGPT-style AI assistant, Gemini-powered). AppShell in root layout handles the split; landing, login, waitlist get full width. Tailwind CSS v4 with **"Warm Editorial"** design system — warm gradient backgrounds (teal→peach→amber), Newsreader serif headlines, Space Grotesk body, DM Mono for data. Brand colors: `#1a1a1a` (primary dark), `orange-500` (accent), `emerald-500` (success). See `DESIGN.md` for full spec.

**Landing page narrative: Problem → Vision → Products (Door Opener → Platform → Engine)**
**Positioning: "The Price Integrity Layer for Global Manufacturing"**

**Landing page sections (in order):**
1. **Hero** (`warm-gradient-hero`) — "20 years of data. Zero intelligence." + drop zone CTA + should-cost product preview card. Badge: "Built for Defense, Aerospace & Automotive"
2. **Proof** (`warm-gradient-subtle`) — real customer story: ₹43L vendor quote → ₹28L final → ₹10.05 Cr saved across 67 units. Big headline quote, slide-in animations, evidence bullet cards
3. **Vision** (`warm-gradient-hero`) — "We turn your history into price intelligence." + 3 stat cards (14% asymmetry, 60% duplicates, 70% off-the-shelf)
4. **Should-Cost** (`warm-gradient-subtle`) — "01/03 · The Door Opener", dark preview card with cost breakdown, 4 audience cards (Procurement, Cost Eng, Design, Leadership)
5. **Similarity Search** (`bg-[#1a1a1a]` dark with orange glow orbs) — "02/03 · The Platform", 5 department use cases (Design, Procurement, Quality, Sales, Finance), dark search results card
6. **AI Procurement Engine** (`warm-gradient-hero`) — "03/03 · The Revenue Engine", 70% MPN spend + negotiation intel, 6 department scenario cards
7. **70% Guardrail** (`bg-[#1a1a1a]` dark) — "Not just drawings. Your entire spend." Animated 70/30 bar, 4 MPN category cards with Problem/Fix format
8. **ROI Calculator** (`warm-gradient-hero`) — two sliders (spend ₹1-100Cr + improvement 2-20%), dark result card with live ROI multiplier
9. **Pricing** (`warm-gradient-subtle`) — Free (₹0) + Pro (₹4,999/mo, CTA: "Join the waitlist")
10. **Footer** (`warm-gradient-footer`) — "The price integrity layer for global manufacturing"

**Background pattern:** alternating `warm-gradient-hero` ↔ `warm-gradient-subtle`, with two dark `bg-[#1a1a1a]` sections (Similarity Search + 70% Guardrail). All dark accents use `#1a1a1a` (never `#09090B` or `#0F1117` except RFQ page). Dark section body text uses `white/70-80%` for readability.

**Typography standardization:** No text below 12px. Labels: 12-14px uppercase tracking-widest. Body copy: 15-17px with `text-justify`. All paragraphs justified edge-to-edge. `<R>` component renders ₹ in font-sans at 0.95em with `whitespace-nowrap` to prevent line-break between ₹ and number.

Library page shows indexed drawings with file type badges, AI descriptions, stats (total, first indexed, last added). Login supports `?waitlist=procurement-brain` param for targeted signup copy. Favicon: N·m dark wordmark. Vercel Analytics enabled.

### `costimize-v2/` — Python Engines + FastAPI Backend (Railway)

4 part types (mechanical, sheet metal, PCB, cable), physics-based engines, 8 procurement agents, 466 passing tests. FastAPI API serves the frontend.

### Root files (`app.py`, `vision.py`, `cost_engine.py`) — Legacy v1

Original monolithic CNC turning-only estimator. Kept for reference.

---

## Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| **Frontend** | Next.js + Tailwind CSS v4 | Vercel deploy, responsive UI |
| **Backend API** | FastAPI (Python) | Serves engines via REST API |
| **Database** | Supabase (Postgres + pgvector) | Auth, estimates, embeddings |
| **Auth** | Supabase Auth (JWT) | Backend validates on every route |
| **AI Vision** | OpenAI GPT-4o (primary), Google Gemini (fallback) → Qwen2.5-VL-7B (self-hosted target) | Extracts dimensions + processes |
| **AI Validation** | Gemini 2.0 Flash Lite → Qwen2.5-7B (self-hosted target) | Cross-checks physics engine estimates |
| **AI Agent** | Gemini 2.0 Flash Lite (now) → Gemma 4 (self-hosted target) | In-app conversational agent with tool-calling |
| **Forecasting** | TimesFM 2.5 (200M, zero-shot, Apache 2.0) | Demand prediction, price trends, lead time forecasting |
| **Similarity Search** | Gemini API + pgvector → DINOv2 + nomic-embed (self-hosted target) | Drawing visual similarity via 768-dim embeddings |
| **Inference Server** | Cloud APIs (now) → vLLM on RunPod/on-prem (target) | OpenAI-compatible API, model-agnostic |
| **Analytics** | Vercel Analytics + usage_log table | Page views + API usage tracking |
| **AI Procurement** | Raw Python agents (no frameworks) | 8 agents, state machine, 3-layer memory, checkpoint/resume |
| **Testing** | pytest | 347 tests across 20 test files |
| **Language** | Python 3.11+ (backend), TypeScript (frontend) | |

### Commands

```bash
# Frontend
cd frontend && npm install && npm run dev     # http://localhost:3000
cd frontend && npx next build                 # Production build

# Backend (Streamlit — original UI, still works)
cd costimize-v2
pip install -r requirements.txt
streamlit run app.py                          # http://localhost:8501

# Backend (FastAPI — production API)
cd costimize-v2
pip install -r api/requirements.txt
uvicorn api.main:app --reload                 # http://localhost:8000

# Tests
cd costimize-v2 && python -m pytest tests/ -v            # Run all 466 tests
cd costimize-v2 && python -m pytest tests/test_agent_*.py # Run 183 agent tests only
```

### Environment Variables

**Backend** (Railway or local `.env`):
- `SUPABASE_URL` — Supabase project URL
- `SUPABASE_SERVICE_ROLE_KEY` — service role key (NOT anon key)
- `OPENAI_API_KEY` — primary vision API (GPT-4o)
- `GEMINI_API_KEY` — fallback vision API + validation
- `ALLOWED_ORIGINS` — comma-separated CORS origins
- `ENVIRONMENT` — set to `production` to disable /docs

**Frontend** (`frontend/.env.local`):
- `NEXT_PUBLIC_SUPABASE_URL` — Supabase project URL
- `NEXT_PUBLIC_SUPABASE_ANON_KEY` — Supabase anon key
- `NEXT_PUBLIC_API_URL` — Backend API URL

### Deployment

- **Frontend:** Vercel auto-deploys from GitHub master. Manual: `cd frontend && vercel --prod`
- **Backend:** Railway deploys from `C:\Users\chand\costimize-deploy` (~705KB clean directory with only API essentials)
- **Git note:** books/, papers/, sandvik/ stripped from git history. Do NOT re-add large PDFs to git
- **Docker build cache:** Dockerfile uses `--mount=type=cache,target=/root/.cache/pip` (BuildKit). `cadquery-ocp` (~500MB) downloads once, cached on subsequent builds. Do NOT use `--no-cache-dir` — it defeats caching. `railway.toml` sets builder=dockerfile explicitly.

---

## costimize-v2 — Architecture

### Project Structure

**Frontend** (`frontend/`): Next.js pages in `src/app/` (page, login, dashboard, estimate/new, estimate/[id], chat, similar, library, mpn, workflows/new, workflows/[id], workflows, waitlist). Components in `src/components/` (app-shell, chat-widget, app-nav, landing-nav, Toast). Lib: `src/lib/api.ts` + `supabase.ts`. Auth middleware in `src/middleware.ts`.

**Backend** (`costimize-v2/`): `agents/` (8 procurement agents + engine + memory + checkpoint), `engines/` (mechanical, sheet_metal, pcb, cable, validation, similarity), `extractors/` (vision, process_detector, bom, gemini_estimator, pdf_classifier, rfq), `scrapers/` (component, material), `history/` (po_parser/store/matcher), `ui/` (Streamlit tabs), `tests/` (466 tests, 20 files), `docs/research/` (24 docs — see `MASTER-RESEARCH-REPORT.md`), `supabase/migrations/` (005-010).

### Data Flow

1. **Mechanical:** Upload drawing → AI extracts → physics engine + Gemini estimate in parallel → orchestrator compares → confidence tier → line-by-line breakdown
2. **Sheet Metal:** Upload drawing → AI extracts dimensions/cutting perimeter/bends → cost engine (laser + bend + weld + hardware inserts + finish) → breakdown
2b. **Assembly ZIP:** Upload ZIP with multiple drawings → extract each file → return per-component ExtractionResponse array → frontend assembles into AssemblyEstimateRequest
3. **PCB:** Upload BOM (CSV/Excel/PDF) → parse components → scrape prices → calculate fab + assembly + test → breakdown
4. **Cable:** Upload BOM → parse components → count wires/connectors → calculate labour → breakdown
5. **Similarity:** Upload 2+ drawings → embed (Gemini Embedding 2 / DINOv2 / image hash) → hybrid search (vector + BM25) → re-rank (FlashRank) → multi-signal rank (visual+material+dimension+process+tolerance+finish) → show matches
6. **All tabs:** Historical PO records loaded from sidebar → matched against current estimate → comparison displayed
7. **Training data:** Every validated mechanical estimate auto-saved to data/validation/ for future ML
8. **Agent workflows:** API triggers pipeline → agents execute sequentially/parallel → checkpoint at approval gates → human approves → resume → complete

### Multi-Agent Procurement Architecture (agents/)

**Product 3: AI Procurement Worker.** Raw Python, no frameworks. Extends existing `orchestrator.py` pattern.

#### Agent Framework
- **BaseAgent Protocol** — duck typing: any class with `name`, `validate_inputs()`, `execute()` qualifies
- **AgentRegistry** — register/get agents by name, enforces uniqueness
- **AgentEngine** — deterministic pipeline routing via `PIPELINES` dict (not LLM-decided)
- **PipelineStep** — `parallel_with` for concurrent agents, `approval_required` for HITL gates
- **ThreadPoolExecutor** for parallel execution (extends validation/orchestrator.py pattern)

#### State Machine
`CREATED → PLANNING → AWAITING_APPROVAL → EXECUTING → COMPLETED / FAILED / REJECTED`

#### Execution Modes (ABC Classification)
- **AUTO** (Class C, < ₹5K): agents run end-to-end, human approves final output
- **HITL** (Class B, ₹5K-50K): pauses at `approval_required` steps, human reviews and resumes
- **MANUAL** (Class A, > ₹50K): generates analysis + talking points only, human leads

#### Pipeline Definitions
```python
PIPELINES = {
    "estimate":          extraction → cost + similarity (parallel)
    "rfq":               extraction → cost + similarity → rfq [approval]
    "compare_quotes":    quote_comparison
    "negotiate":         quote_comparison → negotiation [approval]
    "full_procurement":  extraction → cost + similarity → rfq [approval]
    "proposal":          quote_comparison → proposal
    "meeting_brief":     meeting
}
```

#### 3-Layer Negotiation Memory (the compounding moat)
- **WorkingMemory** — frozen dataclass, in-process: target_price, current_offer, concession_budget, rounds
- **EpisodicMemory** — Supabase table `negotiation_episodes`: what happened in each negotiation
- **SemanticMemory** — Supabase table `supplier_intelligence`: patterns extracted across episodes (typical_discount, negotiation_rounds). Evidence count tracks reliability. Compounds with every deal.

#### Checkpoint/Resume
- Every state transition persisted to Supabase (`agent_workflows` + `agent_checkpoints`)
- Row-level locking for concurrent safety on approval
- Audit trail in `agent_audit_log` (never breaks main flow)
- Resume: load checkpoint → apply modifications → continue pipeline from where it paused

#### LLM Client (`agents/llm.py`)
- Centralized `call_llm()` normalizes Gemini/OpenAI/vLLM to one interface
- Auto-selects provider from env: `GEMINI_API_KEY` → Gemini, `OPENAI_API_KEY` → OpenAI
- `OPENAI_BASE_URL` → vLLM (self-hosted). Swap model via config, not code rewrite
- `parse_json_response()` strips markdown fences and trailing commas

#### API Endpoints (`/api/agent/`)
- `POST /agent/workflows` — create and run workflow
- `GET /agent/workflows/{id}` — status and outputs
- `POST /agent/workflows/{id}/approve` — approve checkpoint, resume
- `POST /agent/workflows/{id}/reject` — reject checkpoint
- `GET /agent/workflows` — list user's workflows

#### Database (6 migrations)
- `005_agent_workflows.sql` — workflows + checkpoints + audit_log (RLS: service_role only)
- `006_suppliers.sql` — suppliers + contacts (company-scoped)
- `007_negotiation_memory.sql` — episodes + supplier_intelligence
- `008_rfq_templates.sql` — email templates (default Indian manufacturing template seeded)
- `009_vendor_quotes.sql` — vendor_quotes + quote_comparisons
- `010_procurement_proposals.sql` — procurement proposals with approval tracking

### Cost Engine Architecture

#### Mechanical Engine (engines/mechanical/)
- **Physics-based MRR calculations** — turning, milling, drilling time from real cutting parameters
- **Sandvik kc1 data** — specific cutting force for 15 materials, power formula: Pc = (vc×ap×fn×kc)/(60×10³)
- **Taylor tool life** — V×T^n = C, tooling cost = edge_cost / tool_life × cutting_time
- **25 machining processes** with material-specific cutting speeds from Machinery's Handbook + Sandvik (includes EDM wire/sinker, chamfering, deburring, honing, lapping, polishing)
- **Machine tier model** — conventional, cnc_2axis, cnc_3axis (default), cnc_5axis, HMC with rate/speed/setup multipliers
- **40+ surface treatments** — area-based ₹/sq.dm costing with mil-spec references, wired into cost pipeline
- **15 heat treatments** — weight-based ₹/kg costing with AMS 2759 references, wired into cost pipeline
- **10 joining methods** — MIG, TIG, spot, adhesive, mechanical fastening, press_fit + brazing (torch/furnace), laser welding, resistance seam

#### Sheet Metal Engine (engines/sheet_metal/)
- **Laser cutting speeds** — 6 material groups × 9 thicknesses at 3kW fiber laser, with interpolation
- **Pierce time estimation** — material-specific multipliers (SS 1.5×, Al 1.2×)
- **Bending tonnage** — F = UTS×T²×L / (V×1000), press brake size selection
- **Minimum bend radius validation** — per-material factors (MS 0.8×T, SS 1.0×T, Al 0.5×T, Brass 0.3×T), 20% surcharge if below minimum
- **Springback correction** — per-material angle correction (MS 2°, SS 3°, Al 1°, Copper 0.5°)
- **Nesting utilization** — rectangular part packing on standard Indian sheet sizes
- **Welding** — MIG/TIG/spot/laser/brazing/resistance seam rates per meter/spot
- **Hardware inserts** — pem_nut (₹8), pem_stud (₹10), rivnut (₹6), standoff (₹12) + press install time
- **Surface finishing** — powder coating, plating, anodizing per sq.m

### Cost Model Constants (config.py)

- 25 machine processes with rates ₹400-1500/hr (including EDM, honing, lapping, polishing)
- Setup times: 15-60 min per process (amortized over quantity)
- Power consumption per process (kW) + power rate ₹8/kWh
- Tooling cost per unit (₹ per process)
- Labour rate: ₹250/hr
- Material wastage: 15%
- Tight tolerance surcharge: 30% (< ±0.05mm)
- PCB: SMD ₹1.5/pad, THT ₹3/pin, stencil ₹2,500 amortized, test ₹25/board
- Cable: ₹200/hr labour, 2 min/wire, 0.5 min/connector, sleeving/labelling timings
- Overhead: 15%, Profit margin: 20%

#### Validation Pipeline (engines/validation/)
- **Parallel execution** — ThreadPoolExecutor runs physics + Gemini simultaneously
- **4 confidence tiers** — ≤3% HIGH, 3-7% MEDIUM, 7-15% LOW (arbitrator), >15% INSUFFICIENT (interactive)
- **AI arbitrator** — Gemini analyzes line-by-line discrepancies for 7-15% gaps
- **Interactive loop** — max 2 rounds of clarifying questions for >15% gaps
- **Training data** — every validated estimate auto-saved for future ML

#### Similarity Search → Company Brain (engines/similarity/)

**Current (LIVE as of 2026-04-05):**
- **Embeddings:** Gemini Embedding API → 768-dim vectors stored in pgvector (Supabase)
- **Hybrid search:** pgvector HNSW (cosine, weight 0.7) + PostgreSQL tsvector BM25 (weight 0.3) via `match_drawings_hybrid` RPC
- **6-signal re-ranking (LIVE):** Over-fetch 20 from Supabase → `ranker.rank_candidates()` scores visual (40%) + material (15%) + dimension (20%) + process (10%) + tolerance (10%) + finish (5%) → return top 10
- **Role presets (LIVE):** `?role=designer` (visual-heavy), `procurement` (material-heavy), `qa` (process-heavy), `default` (balanced)
- **Metadata extraction on embed:** Vision extractor runs on upload → populates material, dimensions, processes, tolerances in JSONB metadata for ranker
- **Text description:** Gemini Flash Lite generates 50-100 word technical description per drawing for BM25 leg
- **Score breakdown in UI:** Frontend shows 6 color-coded mini bars per match (green ≥80%, amber ≥50%, gray <50%) + material badge
- **Product rules** — separate from cost estimation, session-scoped for regular users, enterprise gets persistent index
- **On-prem path** — ColFlor (174M params, fits 8GB RAM) for defense clients who won't use cloud APIs

**Research target (see `docs/research/SIMILARITY-SEARCH-DEEP-DIVE.md`):**
- **Knowledge graph** — PostgreSQL relational: part → material → process → feature → cost → supplier
- **Portfolio intelligence** — LightRAG (open-source, 70% cheaper than GraphRAG) for "what's our avg cost for turned aluminum?"
- **Feedback loop** — users confirm/reject matches → builds similarity graph over time

**Upgrade phases:** ~~(1) Real embeddings + BM25~~ DONE → ~~(2) 6-signal ranker + role presets~~ DONE → (3) DINOv2 visual embeddings + cross-encoder re-ranker → (4) Fine-tune + on-prem (ColFlor) → (5) KG + LightRAG → (6) STEP via GC-CAD GNN

### Key Design Decisions

- **Frozen dataclasses** for all cost breakdown results (immutable)
- **Supabase Postgres** — production database with RLS, pgvector for similarity. JSON files still used for Streamlit MVP mode
- **Two-stage extraction** — GLM-OCR (0.9B, local/API, $0.03/M tokens) extracts raw text → Gemini 2.0 Flash Lite interprets engineering context (GD&T, processes). Cuts AI cost 50-80%. GPT-4o as final fallback only.
- **Rule-based fallbacks** — process detection works without AI
- **24hr cache** on all scraped prices
- **Physics first, ML later** — physics-based models for day-one accuracy, ML correction factors after collecting estimate-vs-actual pairs
- **Self-hosted AI roadmap** — All AI migrating to self-hosted: GLM-OCR (text) + Gemma 4 (reasoning/agent) + DINOv2 (visual) + TimesFM 2.5 (forecasting). See `AI-AGENT-ROADMAP.md`. Timeline: extraction Month 2, embeddings Month 4, agent Month 5, full self-hosted Month 6, defense on-prem Month 9
- **LLM-agnostic agent** — Agent layer is tool definitions + routing, talks to any OpenAI-compatible API. Swapping Gemini → vLLM is a config change, not a rewrite
- **Training data collection** — Every cloud API call logged as training data (extraction pairs, agent conversations, similarity feedback). Tables: training_extractions, training_conversations, training_similarity
- **No silent tracking** — cost estimation and similarity search are HARD-SEPARATED: (1) cost estimation never feeds similarity index, (2) similarity is session-scoped for free users (nothing persisted), (3) enterprise tier gets persistent index via explicit opt-in, (4) minimum 2 drawings required for similarity, (5) if user deletes history, data is gone. Defense buyers are paranoid about data.
- **Per-user AI budget** — $0.50 per 48 hours per user, $20/day global cap. Enforced via `check_user_budget()` in `api/cost_tracker.py`. HTTP 429 when exceeded.
- **Dual pipeline strategy** — keep VLM-only (working) alongside any future YOLO+VLM pipeline, benchmark to decide
- **Native parsing over rasterization** — DXF/DWG: parse entities with `ezdxf` (exact coordinates). STEP: parse geometry with OCP. PDF: extract text with pdfplumber first. NEVER convert to image for extraction — PNG only as last resort for scanned PDFs at 300+ DPI minimum. No external CAD software needed.
- **VLM fine-tuning dataset** — User's own Indian manufacturing drawings (DWG/DXF/STEP/PDF) are the training data. Pipeline: convert to PNG (300+ DPI, never JPEG) → auto-annotate with GPT-4o → LoRA fine-tune Qwen2.5-VL-7B (~$10-20). Supplement with: TechING (HuggingFace), DeepCAD (178K models), ABC Dataset (1M STEP).

---

## Research & Strategy

24 research docs in `docs/research/` (20,000+ lines). See `MASTER-RESEARCH-REPORT.md` for consolidated findings. Key docs: `SIMILARITY-SEARCH-DEEP-DIVE.md`, `MULTI-AGENT-ARCHITECTURE-RESEARCH.md`, `AI-AGENT-ROADMAP.md`, `PHYSICS-ENGINE-KNOWLEDGE-MAP.md`.

## Legacy v1 (Root Files)

The original single-process CNC turning estimator. Monolithic `app.py` (1146 lines). Not actively developed.

## Git Workflow

- **Always use branches** — never push directly to master. Feature branch → PR via `gh pr create` → merge. Use worktrees for isolation.
- **books/**, **papers/**, **sandvik/** directories exist locally but are stripped from git history (200MB+ PDFs)
- Root `.gitignore` uses `/lib/` (not `lib/`) to avoid blocking `frontend/src/lib/`
- costimize-v2 was originally a git submodule, now inlined into the monorepo
- Backend deploys from a separate clean directory (`C:\Users\chand\costimize-deploy`), NOT from the monorepo

## Working Style

- **Claude is the tech lead** — make all tech decisions, don't present options. User is the product owner (domain expert, not a developer).
- **AI is a WORKER, not a copilot** — never say "copilot" or "assistant" in any copy, docs, or architecture. "AI does X. You approve." Not "AI helps you do X."
- **Ship in 2-10 day sprints** — not enterprise roadmaps. Use free/open-source tools. Break features into small shippable increments.
- **5-phase launch process** — (1) Discovery: ask questions, challenge assumptions (2) Planning: propose v1, explain in plain language (3) Building: build in visible stages, test everything (4) Polish: professional quality, handle edge cases (5) Handoff: deploy, document, suggest v2 improvements.
- **QA everything before deploy** — test all auth flows, redirects, nav states, empty/loading/error states. User should never find edge case bugs.
- **Copy rules** — never say "physics" or show formulas in user-facing copy. Sell the answer, not the method. Multi-audience positioning (procurement, design, QA, leadership). Similarity search = "knowledge as asset" (CADDi-inspired), must appear in 3+ places.
- **Verify file writes** — after writing session/save files, always `ls -la` to confirm they exist. User burned by phantom saves.
- **Save session verification** — after running `/save-session`, ALWAYS verify the session file was actually written to disk with `ls -la <filepath>`. If the file doesn't exist or is empty, re-save immediately. Never assume the write succeeded.

## Execution Discipline

### 1. Plan Mode Default
- Enter plan mode for ANY non-trivial task (3+ steps or architectural decisions).
- If something goes sideways, STOP and re-plan immediately — don't keep pushing.
- Use plan mode for verification steps, not just building.
- Write detailed specs upfront to reduce ambiguity.

### 2. Subagent Strategy
- Use subagents liberally to keep main context window clean.
- Offload research, exploration, and parallel analysis to subagents.
- For complex problems, throw more compute at it via subagents.
- One task per subagent for focused execution.

### 3. Self-Improvement Loop
- After ANY correction from the user: update `tasks/lessons.md` with the pattern.
- Write rules for yourself that prevent the same mistake.
- Ruthlessly iterate on these lessons until mistake rate drops.
- Review lessons at session start for relevant project.

### 4. Verification Before Done
- Never mark a task complete without proving it works.
- Diff behavior between main and your changes when relevant.
- Ask yourself: "Would a staff engineer approve this?"
- Run tests, check logs, demonstrate correctness.

### 5. Demand Elegance (Balanced)
- For non-trivial changes: pause and ask "is there a more elegant way?"
- If a fix feels hacky: "Knowing everything I know now, implement the elegant solution."
- Skip this for simple, obvious fixes — don't over-engineer.
- Challenge your own work before presenting it.

### 6. Autonomous Bug Fixing
- When given a bug report: just fix it. Don't ask for hand-holding.
- Point at logs, errors, failing tests — then resolve them.
- Zero context switching required from the user.
- Go fix failing CI tests without being told how.

### Task Management
1. **Plan First**: Write plan to `tasks/todo.md` with checkable items.
2. **Verify Plan**: Check in before starting implementation.
3. **Track Progress**: Mark items complete as you go.
4. **Explain Changes**: High-level summary at each step.
5. **Document Results**: Add review section to `tasks/todo.md`.
6. **Capture Lessons**: Update `tasks/lessons.md` after corrections.

### Core Principles
- **Simplicity First**: Make every change as simple as possible. Impact minimal code.
- **No Laziness**: Find root causes. No temporary fixes. Senior developer standards.

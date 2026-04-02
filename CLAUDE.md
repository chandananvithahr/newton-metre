# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Design System

**IMPORTANT:** When implementing any UI from Stitch designs, always read `DESIGN.md` first.
`DESIGN.md` is the ground truth for all colors, typography, spacing, and component styles.
Treat Stitch HTML + screenshot as a constraint — do NOT rewrite layout logic or substitute values.
Always pull the screen screenshot alongside the HTML and match it pixel-for-pixel.

## Project Overview

Newton-Metre — "Know what it costs. Before they quote." A manufacturing cost intelligence platform. Two superpowers: (1) should-cost breakdowns (±5-10% accuracy) for mechanical parts, sheet metal, PCB, and cable assemblies, and (2) similarity search that turns your company's drawing history into a searchable asset. Built for Indian manufacturing economics (₹ currency, INR pricing).

**Target industries:** Defense, Aerospace, Automobile
**Target part types:** Turned, Milled, Sheet metal
**Users:** Sourcing & procurement, cost engineering, design engineering, and leadership teams at manufacturing companies.

**Core value:** "Upload a drawing. Get a line-by-line should-cost. Find similar parts from your history. Negotiate with data."

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

7 pages: landing (aPriori/CADDi-inspired, multi-audience), login/signup, dashboard, new estimate, estimate detail, similarity search, RFQ extraction. Tailwind CSS v4 with "Tactical Elegance" design system (Newsreader + Space Grotesk fonts, deep blue #00288e, tonal surface layering #faf8ff). Landing page has dedicated should-cost section (4 audience cards) and dedicated similarity search section (CADDi-style knowledge-as-asset). See `DESIGN.md` for full spec. Vercel Analytics enabled.

### `costimize-v2/` — Python Engines + FastAPI Backend (Railway)

4 part types (mechanical, sheet metal, PCB, cable), physics-based engines, 164 passing tests. FastAPI API serves the frontend.

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
| **AI Vision** | OpenAI GPT-4o (primary), Google Gemini (fallback) | Extracts dimensions + processes |
| **AI Validation** | Gemini 1.5 Flash | Cross-checks physics engine estimates |
| **Similarity Search** | Gemini API + pgvector | Drawing visual similarity via 256-dim embeddings |
| **Analytics** | Vercel Analytics + usage_log table | Page views + API usage tracking |
| **Testing** | pytest | 164 tests across 12 test files |
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
cd costimize-v2 && python -m pytest tests/ -v # Run all 164 tests
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

```
frontend/                             # Next.js frontend (Vercel)
├── src/app/
│   ├── layout.tsx                    # Root layout, Google Fonts, Vercel Analytics
│   ├── globals.css                   # Tailwind v4 + design system tokens
│   ├── page.tsx                      # Landing page (hero, problem, should-cost, similarity search, how-it-works, built-for-india, pricing)
│   ├── login/page.tsx                # Signup/login with Supabase Auth
│   ├── dashboard/page.tsx            # Stats, actions, recent estimates table
│   ├── estimate/new/page.tsx         # Upload → extract → review → calculate → result
│   ├── estimate/[id]/page.tsx        # Estimate detail view
│   └── similar/page.tsx              # Multi-file similarity search
├── src/lib/
│   ├── api.ts                        # API client with safeFetch error handling
│   └── supabase.ts                   # Supabase browser client
├── src/middleware.ts                  # Auth middleware (protects /dashboard, /estimate, /similar)
└── .env.local                        # Supabase + API URL config

costimize-v2/
├── app.py                        # Tab router + sidebar PO upload (~40 lines)
├── config.py                     # All rates, constants, API keys (single source of truth)
├── requirements.txt
│
├── ui/
│   ├── components.py             # Shared widgets (cost table, historical comparison, confidence badges)
│   ├── mechanical_tab.py         # Mechanical parts UI (upload → extract → validate → display)
│   ├── pcb_tab.py                # PCB assembly UI (BOM → prices → calculate → display)
│   ├── cable_tab.py              # Cable assembly UI (BOM → calculate → display)
│   └── similarity_tab.py         # Similarity search UI (upload 2+ drawings → compare)
│
├── engines/
│   ├── mechanical/
│   │   ├── cost_engine.py        # Multi-process cost calculator (frozen dataclass output)
│   │   ├── cutting_data.py       # Physics-based cutting parameters — Sandvik kc1, Taylor tool life, MRR data for 9 materials
│   │   ├── process_db.py         # 18 processes with MRR-based time estimation (physics, not heuristics)
│   │   ├── material_db.py        # Material prices, densities, machinability
│   │   ├── surface_treatment_db.py  # 40+ surface treatments (electroplating, anodizing, conversion, spray, paint, PVD/CVD)
│   │   └── heat_treatment_db.py  # 15 heat treatment processes (hardening, carburizing, nitriding, etc.)
│   ├── sheet_metal/
│   │   ├── cost_engine.py        # Sheet metal should-cost calculator (frozen dataclass output)
│   │   ├── cutting_db.py         # Fiber laser 3kW cutting speeds for 6 material groups × 9 thicknesses
│   │   ├── bending_db.py         # Press brake tonnage formula, bend time, K-factors
│   │   └── material_db.py        # 9 sheet materials, nesting utilization calculator
│   ├── pcb/
│   │   ├── cost_engine.py        # PCB assembly cost calculator
│   │   ├── bom_parser.py         # CSV/Excel BOM auto-column detection
│   │   └── fab_cost.py           # Bare board fabrication cost model
│   ├── cable/
│   │   ├── cost_engine.py        # Cable assembly cost calculator
│   │   └── bom_parser.py         # Reuses PCB parser + wire/connector counting
│   ├── validation/
│   │   ├── orchestrator.py       # THE BRAIN: parallel physics + Gemini, routes by confidence tier
│   │   ├── comparator.py         # Delta %, confidence tier enum (HIGH/MEDIUM/LOW/INSUFFICIENT)
│   │   ├── arbitrator.py         # AI agent resolves 7-15% gaps via Gemini
│   │   ├── interactive.py        # Generates clarifying questions for >15% gaps (max 2 rounds)
│   │   └── data_collector.py     # JSON persistence + ML training data export
│   └── similarity/
│       ├── preprocessor.py       # Any format (PDF/DXF/image) → clean image + thumbnail
│       ├── embedder.py           # 3 strategies: Gemini API (0 RAM) → image hash (0 deps) → DINOv2 (future)
│       ├── indexer.py            # FAISS + numpy brute-force fallback, JSON metadata sidecar
│       ├── ranker.py             # 4-signal weighted ranking (visual+material+dimension+process)
│       └── searcher.py           # Full search API (preprocess → embed → search → rank)
│
├── extractors/
│   ├── vision.py                 # AI drawing analysis (GPT-4o / Gemini fallback)
│   ├── process_detector.py       # AI + rule-based process detection
│   ├── bom_extractor.py          # AI extracts BOM from PDF
│   └── gemini_estimator.py       # Gemini end-to-end cost estimate (for validation loop)
│
├── scrapers/
│   ├── component_scraper.py      # DigiKey/Mouser web scraping with 24hr cache
│   └── material_scraper.py       # Metal raw material prices (INR) with cache
│
├── history/
│   ├── po_parser.py              # Parse Excel/CSV purchase orders
│   ├── po_store.py               # JSON storage with deduplication
│   └── po_matcher.py             # Part number exact match + description keyword fallback
│
├── data/
│   ├── materials.json            # 9 materials (Aluminum through Titanium)
│   ├── processes.json            # 18 manufacturing processes
│   ├── cache/                    # Scraped price cache (24hr TTL)
│   ├── history/                  # Stored historical PO records (JSON)
│   ├── validation/               # Validated estimate pairs for ML training
│   └── similarity/               # Vector index + metadata (session-scoped for regular users)
│
├── papers/                       # Reference PDFs — LOCAL ONLY, stripped from git history
│
├── docs/research/                # 23 research docs (17,000+ lines total)
│   ├── MASTER-RESEARCH-REPORT.md # Single source of truth — all research consolidated
│   ├── comprehensive-market-strategy-research.md
│   ├── PDF-PARSING-DEEP-DIVE.md
│   ├── dxf-extraction-deep-dive.md
│   ├── indian-manufacturing-drawings-research.md
│   ├── cad-software-file-formats-by-country.md
│   ├── PHYSICS-ENGINE-KNOWLEDGE-MAP.md    # Formulas, cutting params from 8 PDFs + 30 papers
│   ├── SANDVIK-DATA-EXTRACTION.md         # kc1 values, power formulas, tool life factors
│   ├── MANUFACTURING-PROCESSES-BY-INDUSTRY.md  # 130+ processes × defense/aero/auto with standards
│   ├── BIBLIOGRAPHY-SOURCES.md            # 60+ books, papers, sources prioritized
│   ├── sheet-metal-cost-estimation.md     # Laser, bending, stamping, deep drawing models
│   ├── INDIAN-REGIONAL-COSTS.md           # Labour/machine rates for 15 cities, power for 13 states
│   ├── ML-STRATEGY-FOR-COST-ESTIMATION.md # Physics+ML hybrid, 4-phase roadmap
│   ├── PROCESS-80-20-ANALYSIS.md          # Big 6 processes = 60-65% of parts
│   ├── SURFACE-TREATMENT-PROCESSES.md     # 45+ processes, Indian rates, mil-specs
│   ├── GITHUB-REPOS-SURVEY.md            # 79 repos, no open-source should-cost tool exists
│   ├── INDUSTRY-REPORTS-AND-BOOKS.md     # SIAM, CII, ACMA, DRDO reports + catalogs
│   ├── BOOTHROYD-ECONOMICS-EXTRACTION.md  # Ch6 cost formulas, Taylor tool life, nonproductive time
│   ├── SIAM-REPORT-EXTRACTION.md          # Indian auto industry 31M vehicles, regional hubs
│   ├── PRACTICAL-MACHINING-DATA.md        # Theory vs shop floor derating, cycle time breakdowns
│   ├── MACHINERYS-HANDBOOK-EXTRACTION.md  # Cutting speeds, power constants, econometrics, tolerances
│   ├── KENNAMETAL-DATA-EXTRACTION.md      # Unit power constants, carbide grades, grooving speeds, cross-validation
│   └── INDIAN-MANUFACTURING-DATA-EXTRACTION.md  # BIS steel grades, govt machine hour rates, Totem cutting data
│
├── demos/
│   └── dinov2_demo.py            # Interactive DINOv2 demo (requires torch, for learning)
│
└── tests/                        # 164 tests across 12 files
    ├── test_config.py            # 2 tests
    ├── test_mechanical_engine.py  # 19 tests (physics-based MRR, Sandvik, Taylor)
    ├── test_sheet_metal_engine.py # 28 tests (laser cutting, bending, material, integration)
    ├── test_surface_treatment.py  # 19 tests (40+ processes, area costing, H.E. baking)
    ├── test_heat_treatment.py    # 12 tests (15 processes, weight costing)
    ├── test_extractors.py        # 6 tests
    ├── test_pcb_engine.py        # 5 tests
    ├── test_cable_engine.py      # 3 tests
    ├── test_component_scraper.py  # 3 tests
    ├── test_material_scraper.py  # 3 tests
    ├── test_history.py           # 5 tests
    ├── test_validation.py        # 29 tests (comparator, arbitrator, interactive, orchestrator)
    └── test_similarity.py        # 32 tests (preprocessor, ranker, indexer, searcher)
```

### Data Flow

1. **Mechanical:** Upload drawing → AI extracts → physics engine + Gemini estimate in parallel → orchestrator compares → confidence tier → line-by-line breakdown
2. **Sheet Metal:** Upload drawing → AI extracts dimensions/cutting perimeter/bends → cost engine (laser + bend + weld + finish) → breakdown
3. **PCB:** Upload BOM (CSV/Excel/PDF) → parse components → scrape prices → calculate fab + assembly + test → breakdown
4. **Cable:** Upload BOM → parse components → count wires/connectors → calculate labour → breakdown
5. **Similarity:** Upload 2+ drawings → embed (Gemini API/image hash) → compare vectors → rank by visual+material+dimension+process → show matches
6. **All tabs:** Historical PO records loaded from sidebar → matched against current estimate → comparison displayed
7. **Training data:** Every validated mechanical estimate auto-saved to data/validation/ for future ML

### Cost Engine Architecture

#### Mechanical Engine (engines/mechanical/)
- **Physics-based MRR calculations** — turning, milling, drilling time from real cutting parameters
- **Sandvik kc1 data** — specific cutting force for 9 materials, power formula: Pc = (vc×ap×fn×kc)/(60×10³)
- **Taylor tool life** — V×T^n = C, tooling cost = edge_cost / tool_life × cutting_time
- **18 machining processes** with material-specific cutting speeds from Machinery's Handbook + Sandvik
- **40+ surface treatments** — area-based ₹/sq.dm costing with mil-spec references
- **15 heat treatments** — weight-based ₹/kg costing with AMS 2759 references

#### Sheet Metal Engine (engines/sheet_metal/)
- **Laser cutting speeds** — 6 material groups × 9 thicknesses at 3kW fiber laser, with interpolation
- **Pierce time estimation** — material-specific multipliers (SS 1.5×, Al 1.2×)
- **Bending tonnage** — F = UTS×T²×L / (V×1000), press brake size selection
- **Nesting utilization** — rectangular part packing on standard Indian sheet sizes
- **Welding** — MIG/TIG/spot rates per meter/spot
- **Surface finishing** — powder coating, plating, anodizing per sq.m

### Cost Model Constants (config.py)

- 18 machine processes with rates ₹600-1500/hr
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

#### Similarity Search (engines/similarity/)
- **3-strategy embedder** — Gemini API (0 RAM, default) → image hash (0 deps, fallback) → DINOv2 (future, GPU)
- **EMBEDDING_DIM=256** — sufficient for Gemini text hash + perceptual hash
- **Dual backend** — FAISS if installed, numpy brute-force fallback for <10K drawings
- **4-signal ranking** — 0.5 visual + 0.2 material + 0.2 dimension + 0.1 process overlap
- **Role presets** — designer (visual-heavy), procurement (material-heavy), QA (process-heavy)
- **Product rules** — separate feature from cost estimation, min 2 drawings, session-scoped for regular users

### Key Design Decisions

- **Frozen dataclasses** for all cost breakdown results (immutable)
- **Supabase Postgres** — production database with RLS, pgvector for similarity. JSON files still used for Streamlit MVP mode
- **AI fallback chain** — OpenAI → Gemini for all vision/extraction
- **Rule-based fallbacks** — process detection works without AI
- **24hr cache** on all scraped prices
- **Physics first, ML later** — physics-based models for day-one accuracy, ML correction factors after collecting estimate-vs-actual pairs
- **Self-hosted VLM roadmap** — Gemini API now → Qwen2.5-VL-7B self-hosted → fine-tuned on-premise (defense clients won't use cloud APIs)
- **No silent tracking** — cost estimation and similarity search are separate features with no data sharing
- **Dual pipeline strategy** — keep VLM-only (working) alongside any future YOLO+VLM pipeline, benchmark to decide
- **Native parsing over rasterization** — DXF/DWG: parse entities with `ezdxf` (exact coordinates). STEP: parse geometry with OCP. PDF: extract text with pdfplumber first. NEVER convert to image for extraction — PNG only as last resort for scanned PDFs at 300+ DPI minimum. No external CAD software needed.
- **VLM fine-tuning dataset** — User's own Indian manufacturing drawings (DWG/DXF/STEP/PDF) are the training data. Pipeline: convert to PNG (300+ DPI, never JPEG) → auto-annotate with GPT-4o → LoRA fine-tune Qwen2.5-VL-7B (~$10-20). Supplement with: TechING (HuggingFace), DeepCAD (178K models), ABC Dataset (1M STEP).

---

## Research & Strategy (docs/research/)

Comprehensive research conducted March 2026 covering:
- **Competitive landscape:** aPriori (physics, 3D only), CADDi ($1.4B, 28 patents, similarity search), IndustrialMind.ai (direct competitor, ex-Tesla, wrapping APIs)
- **VLM benchmarks:** Qwen2.5-VL-7B beats GPT-4o on document understanding. Fine-tuning path: LoRA on 1,000 drawings for $6-16
- **CAPP papers:** ARKNESS (KG + 3B Llama = GPT-4o on machining), CAPP-GPT (process planning from CAD B-Rep)
- **Format priorities:** PDF (have it) → STEP (next, 2-3 days) → DXF → DWG
- **Business model:** Per-estimate → SaaS → enterprise on-prem
- **80/20 analysis:** Big 6 processes cover 60-65% of all parts; machining + sheet metal + casting + forging = 80%
- **ML strategy:** Physics stays foundation; ML adds correction factors after 50-100 estimate-actual pairs; no public cost datasets exist (our moat)
- **Indian regional costs:** Labour/machine rates for 15 cities; 25% cost spread between cheapest (Pithampur) and most expensive (Bangalore)
- **Surface treatments:** 45+ processes documented with Indian rates, mil-specs, H.E. baking requirements
- **GitHub landscape:** 79 repos surveyed; zero open-source should-cost tools exist; SVGnest (2.5K stars) for nesting, AAGNet for feature recognition
- **Industry reports:** SIAM, CII, ACMA, DRDO/HAL reports identified; CMTI Machine Hour Rate Guide is #1 Indian-specific resource
- **Boothroyd economics:** Ch6 cost formulas, Taylor tool life optimization, nonproductive time = 50-60% of cycle (key insight)
- **SIAM auto industry:** 31M vehicles produced, 43L PV sold, regional hub mapping for component demand
- **Practical machining:** Theory vs shop floor derating (0.65-0.85×), cycle time breakdowns, Indian rates
- **Machinery's Handbook:** Cutting speeds for 20+ materials × 5 tool types, power constants Kp/C/W, machining econometrics (Taylor/Colding/ECT), sheet metal bend formulas, machinability ratings, tolerance IT grades by process
- **Kennametal:** Unit power constants for 16 materials (AISI grades), carbide grade compositions, grooving/parting speeds for all ISO groups, machinability factors, cross-validation against Sandvik kc1 values
- **Indian manufacturing data:** BIS steel grades (IS 2062, IS 1570) mapped to ISO groups, government machine hour rates from MSME Kolkata & CTR Ludhiana, Totem catalog cutting speeds, EN-to-IS grade cross-references

See `MASTER-RESEARCH-REPORT.md` for the consolidated single source of truth.

---

## Legacy v1 (Root Files)

The original single-process CNC turning estimator. Monolithic `app.py` (1146 lines). Not actively developed.

## Git Notes

- **books/**, **papers/**, **sandvik/** directories exist locally but are stripped from git history (200MB+ PDFs)
- Root `.gitignore` uses `/lib/` (not `lib/`) to avoid blocking `frontend/src/lib/`
- costimize-v2 was originally a git submodule, now inlined into the monorepo
- Backend deploys from a separate clean directory (`C:\Users\chand\costimize-deploy`), NOT from the monorepo

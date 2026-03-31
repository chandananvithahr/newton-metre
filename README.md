# Costrich

> **Know what it costs. Before they quote.**

AI-powered procurement negotiation intelligence for Indian manufacturing. Gives procurement teams line-by-line should-cost breakdowns for manufactured parts — so you walk into every supplier negotiation knowing exactly what the part should cost, process by process.

**Live:** [costrich.app](https://frontend-theta-ecru-95.vercel.app) · [API](https://costimize-api-production.up.railway.app/api/health)

---

## What It Does

Upload an engineering drawing or BOM. Get back a physics-based cost breakdown — material, machining time, setup, tooling, surface treatment — with ±5-10% accuracy.

No guesswork. No "industry benchmarks." Real cutting parameters, real Indian machine hour rates, real INR pricing.

```
Drawing / BOM
     ↓
AI extracts dimensions, processes, material
     ↓
Physics engine calculates should-cost line by line
     ↓
Gemini cross-validates (parallel)
     ↓
Confidence-tiered breakdown — ready to negotiate
```

---

## Part Types Supported

| Part Type | Engine | Accuracy |
|-----------|--------|----------|
| Turned & Milled (Mechanical) | MRR physics + Sandvik kc1 + Taylor tool life | ±5-10% |
| Sheet Metal | Fiber laser speeds + bending tonnage + nesting | ±5-10% |
| PCB Assembly | BOM parsing + fab cost + component scraping | ±10-15% |
| Cable Assembly | Wire/connector counting + labour model | ±10-15% |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14 + Tailwind CSS v4 |
| Backend API | FastAPI (Python 3.11) |
| Database | Supabase (Postgres + pgvector) |
| Auth | Supabase Auth (JWT) |
| AI Vision | GPT-4o (primary) + Gemini 1.5 Flash (fallback) |
| Similarity Search | Gemini embeddings + pgvector |
| Deployment | Vercel (frontend) + Railway (backend) |

---

## Key Features

- **Line-by-line cost deconstruction** — material, machining, setup, tooling, surface treatment, overhead, margin
- **Physics-based engine** — Sandvik kc1 specific cutting force data, Taylor tool life model, fiber laser cutting speeds for 6 material groups × 9 thicknesses
- **40+ surface treatments** — electroplating, anodizing, PVD/CVD, powder coat — area-based INR/sq.dm costing
- **Parallel validation** — physics engine + Gemini run simultaneously, confidence-tiered output (HIGH/MEDIUM/LOW)
- **Similarity search** — find the most similar drawing ever made or bought, with specs and historical cost
- **RFQ extraction** — upload any RFQ PDF, extract part requirements and get instant estimate
- **STEP / DXF / DWG support** — direct geometry extraction, no manual dimension entry

---

## Project Structure

```
costimize-mvp/
├── frontend/                    # Next.js web app (Vercel)
│   └── src/app/                 # 6 pages: landing, auth, dashboard, estimate, detail, similarity
│
└── costimize-v2/                # Python engines + FastAPI backend (Railway)
    ├── api/                     # FastAPI routes
    ├── engines/
    │   ├── mechanical/          # MRR physics, Sandvik data, 18 processes
    │   ├── sheet_metal/         # Laser cutting, bending, welding
    │   ├── pcb/                 # BOM parsing, fab cost
    │   ├── cable/               # Wire/connector assembly
    │   ├── validation/          # Parallel physics + AI validation pipeline
    │   └── similarity/          # Drawing similarity search
    ├── extractors/              # AI vision, process detection, BOM extraction
    └── tests/                   # 164 tests across 12 files
```

---

## Running Locally

```bash
# Frontend
cd frontend
npm install
npm run dev                      # http://localhost:3000

# Backend
cd costimize-v2
pip install -r api/requirements.txt
uvicorn api.main:app --reload    # http://localhost:8000

# Tests
cd costimize-v2
python -m pytest tests/ -v       # 164 tests
```

**Environment variables required:**

```
# Backend
SUPABASE_URL=
SUPABASE_SERVICE_ROLE_KEY=
OPENAI_API_KEY=
GEMINI_API_KEY=

# Frontend
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
NEXT_PUBLIC_API_URL=
```

---

## Target Market

Indian manufacturers in **Defense · Aerospace · Automobile** — procurement teams negotiating with suppliers for custom turned, milled, and sheet metal parts.

The problem: suppliers know buyers don't understand manufacturing costs. Margins get padded 30-40% and nobody can prove it. Costrich closes that information gap.

---

## Status

- Live product with real users
- 164 tests passing
- Physics engine covers 80%+ of common Indian manufacturing part types
- Training data pipeline live — every validated estimate becomes future ML training data

---

*Built for Indian manufacturing. INR pricing. Indian machine hour rates. Indian job shop economics.*

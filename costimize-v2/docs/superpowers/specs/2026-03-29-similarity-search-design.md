# Costimize Intelligence Platform — Design Spec

**Date:** 2026-03-29
**Status:** Approved
**Scope:** 5-phase product roadmap — multi-agent extraction → AI validation → own LLMs → similarity search

---

## Vision

Build the world's first physics-grounded, AI-validated cost intelligence platform for Indian manufacturing. Every estimate is backed by real cutting data, cross-checked by AI, and continuously improved through collected data.

```
Phase 1A: Multi-Agent Extraction + Validation Loop  ← BUILD NOW
Phase 1B: DXF Direct Extraction Path (low-hanging fruit)
Phase 2:  Own Vision LLM (feature extraction from drawings)
Phase 3:  Own Chat LLM (interactive cost conversations)
Phase 4:  Fine-tuning Pipeline (on collected drawing-cost pairs)
Phase 5:  Drawing Similarity Search Engine (company knowledge retrieval)
```

---

## Multi-Agent Extraction Pipeline

### Master Flowchart — Every Node is an AI Agent

```
                         ┌──────────────┐
                         │  USER UPLOAD │
                         └──────┬───────┘
                                │
                         ┌──────▼───────┐
                         │ AGENT 0:     │
                         │ FILE ROUTER  │  ← instant, no AI
                         │ detect type  │
                         └──────┬───────┘
                    ┌───────────┼───────────┐
                    ▼           ▼           ▼
               ┌────────┐ ┌────────┐ ┌──────────┐
               │  .dxf  │ │  .dwg  │ │ .pdf/img │
               └───┬────┘ └───┬────┘ └────┬─────┘
                   │          │            │
                   │    ┌─────▼──────┐     │
                   │    │ Convert to │     │
                   │    │ DXF (ODA)  │     │
                   │    └─────┬──────┘     │
                   │          │            │
                   ▼          ▼            ▼
               ┌──────────────┐    ┌──────────────┐
               │  DXF PATH    │    │ COMPLEXITY   │
               │  3 agents    │    │ CLASSIFIER   │
               │  (fastest)   │    │ (Agent 1)    │
               └──────┬───────┘    └──────┬───────┘
                      │             ┌─────┴──────┐
                      │             ▼            ▼
                      │        ┌────────┐  ┌──────────┐
                      │        │ SIMPLE │  │ COMPLEX  │
                      │        │4 agents│  │8-10 agent│
                      │        └───┬────┘  └────┬─────┘
                      │            │            │
                      ▼            ▼            ▼
               ┌──────────────────────────────────────┐
               │        VALIDATED EXTRACTION           │
               │  dimensions + material + processes    │
               └──────────────────┬───────────────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    ▼                           ▼
               ┌──────────┐              ┌──────────┐
               │ PHYSICS  │  ← PARALLEL  │ GEMINI   │
               │ ENGINE   │              │ ESTIMATE │
               └────┬─────┘              └────┬─────┘
                    │                         │
                    ▼                         ▼
               ┌──────────────────────────────────┐
               │ ORCHESTRATOR AGENT               │
               │ ≤3%  → HIGH ✅ return directly   │
               │ 3-7% → MEDIUM ⚠️ flag review    │
               │ 7-15%→ ARBITRATOR AGENT 🤖       │
               │ >15% → INTERACTIVE AGENT 🔄      │
               └──────────────┬───────────────────┘
                              │
                              ▼
               ┌──────────────────────────────────┐
               │ FINAL COST ESTIMATE              │
               │ + confidence badge               │
               │ + data saved for ML training     │
               └──────────────────────────────────┘
```

### UI Prompt to User

```
Upload your engineering drawing

📎 [Upload file]

Best results: DXF or STEP files (direct geometry)
Also supported: PDF, PNG, JPG, DWG

💡 Have a CAD file? Upload .dxf for fastest, most accurate extraction.
   PDF/image works too — we use multiple AI agents to extract every detail.
```

---

## DXF PATH — 3 Agents (fastest, ~95% accuracy, <2 sec)

```
DXF file
  │
  ▼
┌──────────────────────────┐
│ AGENT D1: DXF PARSER     │  ← No AI, pure geometry (ezdxf)
│ Parse entities:          │
│ lines, arcs, circles,   │
│ dimensions, text blocks  │
└──────────────────────────┘
  │
  ▼
┌──────────────────────────┐
│ AGENT D2: FEATURE        │  ← Rule-based + light AI
│ RECOGNIZER               │
│ Geometry → features:     │
│ holes, slots, pockets,   │
│ threads, chamfers, bores │
└──────────────────────────┘
  │
  ▼
┌──────────────────────────┐
│ AGENT D3: PROCESS MAPPER │  ← AI agent
│ Features → processes:    │
│ turning, milling, etc.   │
│ + material from text     │
│ + tolerances from dims   │
└──────────────────────────┘
  │
  ▼
  VALIDATED EXTRACTION → Orchestrator
```

DXF is the low-hanging fruit. Geometry is already structured — no vision AI needed for dimensions. Build after the validation loop.

---

## PDF/IMAGE PATH — Simple Drawing (4 agents, ~85% accuracy, ~5 sec)

Simple = single view, <10 dimensions, standard part (shaft, bush, plate)

```
┌────────────────────────┐
│ AGENT S1: DIMENSION    │  ← Vision AI (GPT-4o)
│ EXTRACTOR              │
│ Read all dimension     │
│ callouts, leaders,     │
│ dimension lines        │
└────────────────────────┘
  │
  ▼
┌────────────────────────┐
│ AGENT S2: MATERIAL &   │  ← Vision AI
│ TITLE BLOCK READER     │
│ Material, part number, │
│ revision, general tol, │
│ surface finish notes   │
└────────────────────────┘
  │
  ▼
┌────────────────────────┐
│ AGENT S3: PROCESS      │  ← AI + rule-based
│ DETECTOR               │
│ Visible features →     │
│ manufacturing steps    │
│ (existing detector)    │
└────────────────────────┘
  │
  ▼
┌────────────────────────┐
│ AGENT S4: VALIDATOR    │  ← AI cross-check
│ "Do dimensions make   │
│  sense for this part   │
│  type and material?"   │
│ Flag inconsistencies   │
└────────────────────────┘
  │
  ▼
  VALIDATED EXTRACTION → Orchestrator
```

---

## PDF/IMAGE PATH — Complex Drawing (8-10 agents, ~80% accuracy, ~15-20 sec)

Complex = multi-view, section views, GD&T symbols, >10 dimensions, assemblies.
Most real engineering drawings are complex.

```
┌─────────────────────────┐
│ AGENT C1: VIEW SPLITTER │  ← Vision AI
│ Identify views: front,  │
│ side, top, section,     │
│ detail views            │
│ Split into regions      │
└─────────────────────────┘
  │
  ├──────────────────────────────────────┐
  ▼                                      ▼
┌─────────────────────────┐  ┌─────────────────────────┐
│ AGENT C2: DIMENSION     │  │ AGENT C3: GD&T          │
│ EXTRACTOR (per view)    │  │ EXTRACTOR               │
│ Read dims from each     │  │ Geometric tolerancing:  │
│ view independently      │  │ position, flatness,     │
│      ← PARALLEL →       │  │ runout, concentricity   │
└─────────────────────────┘  └─────────────────────────┘
  │                                      │
  ▼                                      ▼
┌─────────────────────────┐
│ AGENT C4: TITLE BLOCK & │  ← Vision AI
│ NOTES READER            │
│ Material, finish specs, │
│ military/BIS standards, │
│ BOM notes               │
└─────────────────────────┘
  │
  ▼
┌─────────────────────────┐
│ AGENT C5: SURFACE       │  ← Vision AI
│ FINISH EXTRACTOR        │
│ Ra callouts, machining  │
│ symbols, finish notes,  │
│ per-surface requirements│
└─────────────────────────┘
  │
  ▼
┌─────────────────────────┐
│ AGENT C6: CROSS-VIEW    │  ← AI reasoning
│ VALIDATOR               │
│ "Do front + side views  │
│  agree on dimensions?"  │
│ Resolve conflicts       │
└─────────────────────────┘
  │
  ▼
┌─────────────────────────┐
│ AGENT C7: FEATURE       │  ← AI reasoning
│ SYNTHESIZER             │
│ Merge all extracted     │
│ data into unified       │
│ feature list            │
└─────────────────────────┘
  │
  ▼
┌─────────────────────────┐
│ AGENT C8: PROCESS       │  ← AI + rules
│ PLANNER                 │
│ Features → full mfg     │
│ process sequence +      │
│ operation order          │
└─────────────────────────┘
  │
  ▼
┌─────────────────────────┐
│ AGENT C9: COMPLETENESS  │  ← AI check
│ CHECKER                 │
│ "Is anything missing?"  │
│ ├─ YES → ask user ──────│──► Interactive questions
│ └─ NO → proceed         │
└─────────────────────────┘
  │
  ▼
  VALIDATED EXTRACTION → Orchestrator
```

### Agent Performance Summary

| Path | Agents | Accuracy | Speed | When |
|------|--------|----------|-------|------|
| DXF | 3 | ~95% | <2 sec | CAD file available |
| Simple PDF | 4 | ~85% | ~5 sec | Single-view, <10 dims |
| Complex PDF | 8-10 | ~80% | ~15-20 sec | Multi-view, GD&T |
| + Validation | +2-4 | cross-check | +3-5 sec | Always runs |

---

## Phase 1A: Validation Loop Architecture (BUILD NOW)

### Problem

Our physics engine gives accurate should-cost breakdowns, but:
- Physics needs exact dimensions/processes — if extraction is wrong, cost is wrong
- AI (Gemini) gives ballpark estimates — fast but not auditable
- Neither alone is trustworthy enough for procurement negotiation

### Solution

Run BOTH engines in **parallel** on every drawing. Orchestrator agent compares outputs and routes to sub-agents based on confidence.

```
Drawing uploaded → existing vision.py extracts dims/processes
    ↓
ORCHESTRATOR AGENT (ThreadPoolExecutor, parallel)
    ├── Task 1: Physics Engine → calculate_mechanical_cost() → ₹820
    ├── Task 2: Gemini Estimator → estimate_cost_from_drawing() → ₹835
    ↓
    Compare: delta = |820 - 835| / max(820, 835) = 1.8%
    ↓
    Route by confidence tier:
    ├─ ≤3%  HIGH    → return physics directly ✅
    ├─ 3-7% MEDIUM  → return physics + review flag ⚠️
    ├─ 7-15% LOW    → spawn ARBITRATOR AGENT 🤖
    └─ >15% INSUFF  → spawn INTERACTIVE AGENT 🔄
```

### Confidence Tiers

| Delta | Tier | Action | User Sees |
|-------|------|--------|-----------|
| ≤3% | HIGH | Use physics | "₹820 (high confidence) — physics and AI agree within 3%" |
| 3-7% | MEDIUM | Physics + flag | "₹820 (review suggested) — AI estimates ₹870, 6% gap" |
| 7-15% | LOW | Agent arbitrates | "₹820 vs ₹950 — 14% gap. Agent analysis: [line-by-line reasoning]" |
| >15% | INSUFFICIENT | Interactive loop | "28% gap — please verify: [targeted questions]. Max 2 rounds." |

### Interactive Data Collection (>15% gap)

```
System: "Physics ₹820 vs AI ₹1,050 (28% gap). Likely causes:
         1. Material: Physics=EN8, AI=EN24 — which is correct?
         2. Dimensions: OD 55mm vs 65mm — confirm?
         3. Processes: 4 vs 6 — heat treatment and grinding needed?"

User answers → recalculate → check delta → converge or round 2 (max 2 rounds)
```

### File Structure for Phase 1A

```
costimize-v2/
├── extractors/
│   ├── vision.py              # Existing — GPT-4o/Gemini drawing extraction
│   ├── process_detector.py    # Existing — AI + rule-based process detection
│   └── gemini_estimator.py    # NEW — Gemini end-to-end cost estimate
│
├── engines/
│   ├── mechanical/
│   │   └── cost_engine.py     # Existing — physics-based should-cost
│   └── validation/
│       ├── __init__.py
│       ├── orchestrator.py    # NEW — THE BRAIN: parallel dispatch + routing
│       ├── comparator.py      # NEW — delta %, confidence tier enum
│       ├── arbitrator.py      # NEW — AI agent for 7-15% gaps
│       ├── interactive.py     # NEW — clarifying questions for >15%
│       └── data_collector.py  # NEW — JSON persistence for training data
│
├── ui/
│   ├── components.py          # MODIFIED — confidence badge + comparison widgets
│   └── mechanical_tab.py      # MODIFIED — wire orchestrator, show validation
│
├── data/
│   └── validation/
│       └── validated_estimates.json  # Training data store
│
└── tests/
    └── test_validation.py     # NEW — 25+ tests, all API calls mocked
```

### Data Collection Schema

Every validated estimate becomes a training pair for Phase 4:

```json
{
  "timestamp": "2026-03-29T10:30:00Z",
  "material_name": "EN8 Steel",
  "dimensions": {"outer_diameter_mm": 55, "length_mm": 120, "inner_diameter_mm": 0},
  "processes": ["turning", "milling", "grinding"],
  "quantity": 100,
  "physics_cost": 820.0,
  "ai_cost": 835.0,
  "final_cost": 820.0,
  "confidence_tier": "high",
  "user_corrections": {},
  "arbitration_reasoning": null
}
```

After 50-100 pairs: ML correction factors (Phase 4).

---

## Phase 1B: DXF Direct Extraction (build after 1A)

Low-hanging fruit — DXF files have structured geometry, no vision AI needed for dimensions.

- `extractors/dxf_parser.py` — ezdxf entity extraction
- `extractors/feature_recognizer.py` — geometry → features
- `extractors/dxf_process_mapper.py` — features → processes
- DWG → DXF conversion via ODA File Converter (free for non-commercial)

---

## Phase 2: Own Vision LLM (Feature Extraction) — CRITICAL FOR ENTERPRISE

### Problem

GPT-4o/Gemini vision extraction:
- Costs ₹2-5 per drawing (API call)
- Latency: 3-8 seconds per call
- No control over model updates
- **Data leaves our infrastructure — DEAL-KILLER for defense/aerospace clients**

### Solution

Fine-tune **Qwen2.5-VL-7B** (open source, Apache 2.0) for:
- Dimension extraction from engineering drawings
- Process detection from drawing annotations
- Title block reading (Indian IS standards)
- GD&T symbol interpretation

### Why Qwen2.5-VL-7B

- Beats GPT-4o on document understanding benchmarks
- 7B params = runs on single 16GB VRAM GPU (₹50/hr cloud, ₹80K one-time RTX 4060)
- Apache 2.0 license — no restrictions for commercial or on-premise deployment
- LoRA fine-tune on 1000 drawings = $6-16 compute cost

### Migration Path

| Phase | Model | Runs Where | When |
|-------|-------|------------|------|
| MVP | Gemini/GPT-4o API | Cloud API | Now → first 10 users |
| Phase 2 | Qwen2.5-VL-7B (open source) | Our server | After 10 users |
| Enterprise | Qwen2.5-VL fine-tuned | Customer's server | Enterprise deals |

### Enterprise Pitch

> "Your drawings never leave your network. Our AI runs on YOUR servers.
> Fine-tuned specifically for your part types."

### Alternative: YOLO Pre-processing (Benchmark, Don't Commit)

Research shows YOLOv11-OBB achieves 88.5% precision on dimension detection in mechanical drawings.
Two pipelines to benchmark side-by-side:

- **Pipeline A (current):** VLM-only (Gemini → Qwen2.5-VL). Proven, working.
- **Pipeline B (future):** YOLO detects regions → crop → VLM parses each region. Potentially cheaper.

**Rule: Never remove Pipeline A. Pipeline B must earn its place through A/B benchmark results.**

Roboflow datasets available for bootstrapping:
- DeepPatent2: 2.7M patent drawings (free)
- Blueprint dataset: 453 images
- Mechanical Parts: 5,914 images
- eDOCr (GitHub): OCR for mechanical drawings

### Training Data

Phase 1A's data collector provides drawing-extraction pairs. After 500+ validated extractions, LoRA fine-tune ($6-16 per run).

| Metric | GPT-4o Baseline | Target |
|--------|-----------------|--------|
| Dimension accuracy | ~85% | 92%+ |
| Process detection F1 | ~80% | 90%+ |
| Latency | 3-8 sec | <1 sec |
| Cost per drawing | ₹2-5 | ₹0.01 |

---

## Phase 3: Own Chat LLM (Interactive Cost Conversations)

Fine-tune a chat model for manufacturing cost conversations:

```
User: "EN24 shaft, 55mm OD, 120mm long, needs hardening"
Bot:  "Material: ₹85 | Turning: ₹42 | Heat treatment: ₹28 | Total: ₹245
       Note: If grinding needed after hardening (common for EN24), add ₹35-45."
```

---

## Phase 4: Fine-tuning Pipeline

```
Data: Phase 1A estimates + Phase 2 corrections + Phase 3 conversations + PO actuals
  → ETL → Quality filter → Train/Val/Test split
  → Vision LLM: LoRA fine-tune
  → Chat LLM: RLHF/DPO
  → Cost ML: XGBoost correction factors
  → A/B test → Auto-rollback on regression
```

---

## Phase 5: Drawing Similarity Search Engine

### Product Rules (CRITICAL)

**Two completely separate features. No cross-pollination.**

1. **Cost Estimation** — upload 1 drawing, get should-cost. No similarity, no silent indexing.
2. **Similarity Search (teaser)** — separate feature, user explicitly uploads 2+ drawings to compare.
   - Minimum 2 drawings required
   - Session-scoped only — nothing persisted for regular users
   - Accepted formats: DXF, PDF, images, STEP (beta)
   - User explicitly chose to use this feature — they know what they're doing

**Enterprise tier (paid):**
- Persistent index across sessions
- Cross-drawing analysis
- Bulk upload and search
- On-premise deployment

**Privacy rules:**
- Cost estimation drawings NEVER feed similarity index
- Regular users: session-only, no tracking, no cross-session data
- If user deletes history, data is gone — never surface it
- Never say "we found from your previous uploads" — trust is everything
- Defense/aerospace buyers are paranoid about data tracking

### The Costimize differentiator vs CADDi

```
CADDi:     "This part is similar to 3 past orders"
Costimize: "This part is similar to 3 past orders (₹850 avg)
            + physics says it should cost ₹820
            → negotiate at ₹830, you're overpaying by 2.4%"
```

### Architecture (8GB RAM compatible)

- **Visual embedding (default):** Gemini API → text description → 256-dim hash vector (0 RAM)
- **Visual embedding (fallback):** Perceptual hash + edge/intensity histograms → 256-dim (0 dependencies)
- **Visual embedding (upgrade):** DINOv2-vits14 (384-dim, ~1GB RAM) or DINOv2-vitb14 (768-dim, ~4GB)
- **Vector search:** numpy brute-force (<10K drawings) → FAISS when scaling
- **Ranking:** 0.5 visual + 0.2 material + 0.2 dimensions + 0.1 process overlap
- **Patent safe:** General-purpose vision model, not proprietary shape features

### Embedding Upgrade Path

| Level | Method | Accuracy | RAM | When |
|-------|--------|----------|-----|------|
| 1 (now) | Gemini API text hash | ~80% | 0 MB | MVP |
| 2 | DINOv2 + VLM dual embedding (640-dim) | ~90% | ~1-4 GB | After server deployment |
| 3 | Fine-tuned contrastive model | ~95% | ~1-4 GB | After 1000+ confirmed pairs |

### Users

| User | Question | Gets |
|------|----------|------|
| Designer | "Similar part exists?" | Drawings + CAD refs → reuse |
| Procurement | "What did we pay?" | History + should-cost + suppliers |
| QA | "How was this inspected?" | Methods + rejection history |

---

## Patent Safety

CADDi patents (JP 7372697, JP 7377565, EP 4546196A1) protect their specific:
- Geometric shape feature vector extraction method
- Database construction method for indexing
- Retrieval/ranking algorithm

Our approach is fundamentally different:
- **DINOv2** (general-purpose vision) not proprietary shape features
- **FAISS** (standard vector search) not custom database construction
- **Multi-signal weighted ranking** not purely shape-based retrieval

---

## Build Order

### Phase 1A — DONE (validation loop)
- [x] comparator.py — confidence tiers, pure math
- [x] gemini_estimator.py — Gemini end-to-end cost estimate
- [x] arbitrator.py — AI agent for 7-15% gaps
- [x] interactive.py — clarifying questions for >15%
- [x] data_collector.py — JSON persistence + training data export
- [x] orchestrator.py — parallel execution (ThreadPoolExecutor) + agent routing
- [x] UI updates — confidence badge + comparison + interactive + recalculate
- [x] test_validation.py — 29 tests, all passing

### Similarity Search — DONE (moved up from Phase 5)
- [x] preprocessor.py — PDF/image/DXF → clean 224×224 image + thumbnail
- [x] embedder.py — 3-strategy: Gemini API (0 RAM) → image hash (0 deps) → DINOv2 (future). EMBEDDING_DIM=256
- [x] indexer.py — FAISS + numpy brute-force fallback + JSON metadata sidecar
- [x] ranker.py — 4-signal weighted scoring (visual+material+dimension+process)
- [x] searcher.py — full search API (preprocess → embed → search → rank)
- [x] similarity_tab.py — Streamlit UI (search + ingest + cost intelligence)
- [x] test_similarity.py — 32 tests, all passing
- [x] app.py — "Similar Parts" tab wired in
- [x] demos/dinov2_demo.py — interactive DINOv2 demo with fake drawings
- Total: 161 tests passing (105 + 29 + 27 = adjusted for new tests)

### Phase 1B — Next (DXF extraction)
- [ ] dxf_parser.py — ezdxf entity extraction
- [ ] feature_recognizer.py — geometry → features
- [ ] dxf_process_mapper.py — features → processes

### Phase 2-5 — Later
- [ ] Vision LLM fine-tuning
- [ ] Chat LLM fine-tuning
- [ ] Fine-tuning pipeline
- [ ] Similarity search (DINOv2 + FAISS)

# Costimize Research: Drawing Extraction + Physics-Based Cost Estimation
## Master Research Report — March 2026 (Last Updated: March 29, 2026)

> **What's new (Mar 29):** Physics-based machining engine BUILT (MRR calculations, Taylor tool life, Sandvik kc1 data integrated). Sheet metal cost estimation research complete (laser cutting, bending, stamping, deep drawing). 50+ manufacturing processes mapped across defense/aerospace/automobile. 60+ bibliography sources compiled. 46 tests passing.
>
> **What's new (Mar 28):** Competitor tech stacks confirmed (own models vs wrappers), VLM benchmarks (Qwen2.5-VL-7B beats GPT-4o), CAPP papers analyzed (ARKNESS + CAPP-GPT), similarity search business validated ($2-5B TAM), STEP file processing roadmap, business model, IDP market sizing, CADDi updated to $1.4B unicorn with 28 patents.

---

# PART 1: THE COMPETITIVE LANDSCAPE

## Key Players

| Company | What They Do | Funding | Approach | Threat Level |
|---------|-------------|---------|----------|-------------|
| **aPriori** | Physics-based should-cost from 3D CAD | PE-backed, 500+ employees | 440+ mechanistic process models, digital factory simulation | HIGH (but 3D only) |
| **CADDi** | Drawing similarity search + procurement data platform | $200M+, **$1.4B valuation** (unicorn) | **28 registered patents**, Kaggle Grandmasters, proprietary deep learning shape recognition | MEDIUM (comparison-based, not should-cost) |
| **IndustrialMind.ai** | AI Manufacturing Engineer (drawing→BOM→routing→cost + production monitoring) | $1.2M pre-seed (Nov 2025, Antler) | Ex-Tesla team, **almost certainly wrapping VLM APIs** (same as us at $1.2M), deployed at Siemens/tesa/Andritz | HIGH (direct competitor, but global enterprise focus) |
| **Werk24** | API: extract dimensions/GD&T/tolerances from drawings → structured JSON | Bootstrapped, 1-10 people | Custom ML + engineering validation, retrained monthly on 100K+ drawings | COMPLEMENTARY (extraction only, no cost estimation) |
| **Landing AI** | General document intelligence (ADE) | $57M | DPT-2 model, agentic orchestration. NOT built for engineering drawings | LOW |
| **Reducto** | Document parsing at scale (1B+ pages/year) | $108M | 3-layer: CV → VLM → agentic self-correction. Beats Textract by 20% | INSPIRATIONAL (architecture pattern) |
| **Rossum** | Document AI for invoices/POs | $100M+ | **Own "Aurora" T-LLM** trained on 11M docs, discriminative decoder (no hallucination by design), 92.5% accuracy | LOW (finance docs, not engineering) |
| **Infrrd** | Intelligent Document Processing | $25M+, Gartner Leader 2025 | **13+ patents**, hybrid own models + LLMs, on-prem option, template-free extraction | LOW (general IDP, not cost estimation) |
| **Hypatos** | Finance document AI | €37M total | **Own custom transformers** + incorporating LLMs, 10M+ annotated entities | LOW (finance only) |
| **iCaptur.AI** | Document capture | Unknown | Likely thin API wrapper, no disclosed IP or patents | LOW |

## Confirmed Competitor Tech Stacks (March 2026 Research)

| Company | Own Models? | Evidence |
|---------|-----------|----------|
| **CADDi** | **YES** | 28 patents, Kaggle Grandmasters on team, hiring SRE for "AI platform infrastructure", proprietary shape recognition trained on millions of Japanese drawings |
| **aPriori** | **N/A — NOT ML-based** | Pure physics-based simulation with 440+ process models. No LLMs in core engine. 87 regional cost libraries |
| **IndustrialMind.ai** | **Unlikely** | $1.2M funding makes own model training impossible. Same approach as Costimize: VLM APIs + domain expertise |
| **Rossum** | **YES** | Own "Aurora" Transactional LLM, 11M training docs, discriminative decoder architecture, hiring ML researchers with GPU clusters |
| **Infrrd** | **YES** | 13+ awarded patents, hiring PhD ML engineers, Gartner Leader |
| **Hypatos** | **YES** | Custom transformers trained on 10M+ entities, customer-specific model training |
| **iCaptur.AI** | **NO evidence** | No patents, no research team, no technical disclosure |

## The Wrapper vs Own Model Reality (YC/VC Data)

- **80-90% of YC AI companies (S24/W25) use foundation model APIs** — this is the validated strategy
- Every major VC (YC, a16z, Sequoia) tells founders to build applications, not models
- Thin wrappers die (Jasper $1.5B → declined), thick application layers thrive (Cursor $2.5B, Harvey $715M, Perplexity $9B)
- **The moat is domain knowledge + workflow, not the model**

## Costimize's Unique Position
- **No competitor** solves: PDF-based + INR-priced + Indian job shop economics + procurement team UX
- **Zero open-source should-cost tools** exist (confirmed via exhaustive GitHub search)
- aPriori requires 3D CAD (Indian MSMEs don't have it)
- CADDi requires large drawing archives (comparison-based, not first-principles)
- IndustrialMind.ai targets factory engineers globally, not Indian procurement teams

---

# PART 2: HOW DRAWINGS ARE CREATED & SHARED

## Global CAD Market
- AutoCAD: 38.96% market share (157K companies)
- SolidWorks: 13.73% (55K companies)
- 2D CAD still accounts for 45% of the market
- 221,361 companies worldwide use CAD software

## Indian Manufacturing (Primary Market)
- **97% of MSMEs are micro-enterprises** that cannot justify CAD expense
- Piracy rate: 56%. AutoCAD costs ₹50K/yr — more than many shop owners' monthly salary
- **PDF is king**: 60-70% of procurement drawings exchanged as PDF
- **WhatsApp is the drawing platform** for Indian SMEs
- GD&T usage is minimal at small/medium level
- Drawing degradation chain: OEM (CATIA) → Tier 1 (PDF) → Tier 2 (scan) → Job shop (WhatsApp photo)
- 15 million manufacturing MSMEs in India

## Drawing Format Distribution (Indian Procurement)
| Format | % of Input | Extraction Difficulty |
|--------|-----------|---------------------|
| PDF (vector, CAD-exported) | 40-50% | Medium (AI vision) |
| PDF (scanned from paper) | 20-30% | Hard (OCR + AI) |
| DXF/DWG | 5-15% | Easy (programmatic) |
| WhatsApp photos | 5-15% | Very hard (CV pipeline) |
| STEP (3D) | 5-10% | Geometry only, no annotations |

## Country-by-Country Standards
| Country | Projection | Standard | Piracy | Paper % |
|---------|-----------|---------|--------|---------|
| India | 1st angle | IS (ISO-based) | 56% | 40-60% MSMEs |
| China | 1st angle | GB (ISO-based) | 66% | Variable |
| Japan | 3rd angle | JIS | 18% | 95.2% use paper! |
| USA | 3rd angle | ASME Y14.5 | 15% | Moderate |
| Germany | 1st angle | DIN/ISO | 22% | Low |

---

# PART 3: DRAWING EXTRACTION TECHNOLOGY

## Format Extraction Ranking (Easiest → Hardest)
| Rank | Format | Accuracy | Method | Cost |
|------|--------|----------|--------|------|
| 1 | DXF | 95-100% | ezdxf programmatic | Free |
| 2 | DWG | 95-100% | ODA → DXF → ezdxf | Free |
| 3 | STEP AP242+PMI | 95-100% | OpenCASCADE | Free |
| 4 | Vector PDF | 80-95% | AI vision (Gemini) | $0.03/page |
| 5 | High-quality scan | 70-90% | AI + OCR | $0.03/page |
| 6 | Low-quality scan | 50-80% | AI + heavy preprocessing | $0.03/page |
| 7 | Phone photo | 30-70% | AI + perspective correction | $0.03/page |

## Zero-Shot VLM Benchmarks on Engineering Drawings
| Model | Accuracy | Cost/1000 pages |
|-------|----------|----------------|
| Gemini 2.5 Pro | ~80% | $130 |
| Gemini 2.5 Flash | ~77% | $31 |
| Claude Opus 4 | ~40% | $312 |
| GPT-4o Mini | ~40% | $25 |

**Key insight: Gemini dramatically outperforms GPT-4o on drawings. Swap Gemini to primary.**

## Open-Source VLM Benchmarks on Document Understanding (2024-2025)

| Model | Params | DocVQA | ChartQA | OCRBench | Notes |
|-------|--------|--------|---------|----------|-------|
| **GPT-4o** | Proprietary | 92.8 | 85.7 | 736 | Baseline |
| **Gemini 1.5 Pro** | Proprietary | 93.1 | 87.2 | 754 | Slightly better than GPT-4o |
| **Qwen2-VL-72B** | 72B | **96.5** | **88.3** | **877** | Beats all cloud models |
| **Qwen2.5-VL-7B** | 7B | **95.7** | **87.3** | **864** | **Beats GPT-4o on single GPU** |
| **Qwen2-VL-7B** | 7B | 94.5 | 83.0 | 845 | Previous version |
| **InternVL2.5-8B** | 8B | 93.8 | 84.7 | 822 | Second-best small model |
| **InternVL2-8B** | 8B | 91.6 | 83.3 | 794 | Decent baseline |
| **Llama 3.2 Vision 90B** | 90B | 90.1 | 85.5 | — | Not best-in-class for docs |
| **Llama 3.2 Vision 11B** | 11B | 88.4 | 83.4 | — | OK but Qwen is better |
| **Phi-3.5-Vision** | 4.2B | 78.3 | 81.8 | 637 | Good for size, weak on OCR |
| **Florence-2-large** | 0.77B | 80.1 | 57.2 | — | Fast but limited |
| **PaliGemma-3B** | 3B | 72.4 | 68.2 | — | Research model |

**Key insight: Qwen2.5-VL-7B ALREADY beats GPT-4o on document understanding — before fine-tuning. This is the model to fine-tune for engineering drawings.**

Sources: Qwen2-VL tech report (arXiv:2409.12191), InternVL2 (arXiv:2404.16821), model cards on HuggingFace.

## Fine-Tuning Path to Own Model

| Phase | When | What | Cost |
|-------|------|------|------|
| **Now** | Pre-PMF | Use GPT-4o/Gemini API ($0.012/drawing) | Variable |
| **100+ drawings** | After PMF | Save GPT-4o outputs as labels (distillation) | Free |
| **1,000+ drawings** | Scale | LoRA fine-tune Qwen2.5-VL-7B | **$6-16** |
| **10K+ drawings/month** | Growth | Deploy on serverless GPU (RunPod) | $0.003-0.005/drawing |
| **Never** | — | Train from scratch | Would cost $50M+ |

Break-even vs GPT-4o API: ~33K drawings/month on dedicated GPU, immediate on serverless.

**Engineering drawing extraction has NO public benchmark** — your labeled dataset becomes a competitive moat.

## Fine-Tuned Models Crush Zero-Shot
- Florence-2 (230M params) fine-tuned on 400 drawings: **+52% F1 vs GPT-4o zero-shot**
- YOLOv11-OBB + Donut pipeline: **94% F1, 89.2% precision, 10.8% hallucination**
- DXF geometric features + XGBoost: **3.91% MAPE** on cost prediction

## State-of-the-Art Pipeline (Papers 2 & 3)
```
Stage 1: YOLOv11m-obb (400 epochs, COCO pretrained) → detect 9 annotation categories
Stage 2: Donut (143M params, 30 epochs, ~20hr training) → parse each patch to structured JSON

9 Categories: GD&T, General Tolerances, Measures, Materials, Notes, Radii, Surface Roughness, Threads, Title Blocks

Result: 94% F1, works on 1,367 drawings producing 11,469 annotation patches
```

## DXF Extraction with ezdxf
```python
import ezdxf
doc = ezdxf.readfile("drawing.dxf")
msp = doc.modelspace()

for dim in msp.query("DIMENSION"):
    measurement = dim.get_measurement()  # actual numeric value
    dim_type = dim.dimtype               # linear, angular, diameter, radius
    # Tolerance via DimStyle: dimtp (plus), dimtm (minus), dimtol (flag)
```

DXF parsing gives 95-100% accuracy in <1 second. Remaining gaps (material notes, GD&T text, surface finish) need AI.

---

# PART 4: PHYSICS-BASED COST ESTIMATION (aPriori's Approach)

## How aPriori Works (3 Steps)
1. **Geometric Cost Driver (GCD) Extraction**: Analyze geometry as manufacturing engineer would see it
2. **Process Modeling**: Mechanistic simulation — MRR, cutting forces, thermal cycles, tool wear
3. **Cost Conversion**: Physical resources → financial quantities using regional economic data

## Core Machining Formulas

### CNC Turning — Cutting Time
```
Tc = L / (f × N)
N = (1000 × Vc) / (π × D)
MRR = D × f × Vc  (cc/min)
```

### CNC Milling — Cutting Time
```
Tc = Lm / Vf
Vf = fz × zc × N
MRR = (ae × ap × Vf) / 1000
```

### Machining Time from Volume
```
Tm = (V_stock - V_part) / MRR
```

### Taylor Tool Life Equation
```
Vc × T^n = C
n = 0.1 (HSS), 0.2 (Carbide), 0.25 (Ceramic)
```

### Complete Part Cost
```
Part_Cost = Material_Cost + (Machining_Time × Machine_Rate) + (Setup_Time × Rate / Batch_Qty) + Tooling + Secondary_Ops + Overhead + Profit
```

### Tolerance Cost Multipliers
- Standard (±0.1mm): 1.0x
- Tight (±0.05mm): 1.3x
- Precision (±0.01mm): 2-4x
- Ultra-precision (±0.001mm): 5-8x

## Essential Books
1. **"Product Design for Manufacture and Assembly" (DFMA)** — Boothroyd, Dewhurst, Knight (THE foundational text)
2. **"Manufacturing Processes for Engineering Materials"** — Kalpakjian & Schmid (machining economics chapter)
3. **"Fundamentals of Modern Manufacturing"** — Groover
4. **"Realistic Cost Estimating for Manufacturing"** — Lembersky (SME, practical handbook)
5. **"Industrial AI: Applications with Sustainable Performance"** — Jay Lee (framework for AI+manufacturing)

---

# PART 5: CADDi PATENTS & SIMILARITY SEARCH BUSINESS

## CADDi Patents (28 Registered, 11+ Filed)

> Full deep dive: [CADDI-PATENTS-DEEP-DIVE.md](../../../docs/research/CADDI-PATENTS-DEEP-DIVE.md)

**Company:** Founded 2017 (Yushiro Kato, ex-McKinsey). $470M valuation (Mar 2025). $202M raised. 150 engineers doubling to 300. Golang/Python on Google Cloud.

### Core Similarity Search Patents

| Patent # | Title | Innovation |
|----------|-------|-----------|
| JP 7372697 | Similar drawing search device, method, and program | **Core patent** — the similarity matching algorithm itself |
| JP 7377565 | Drawing search device, database construction device, search system | Database construction + search infrastructure |
| EP 4546196A1 | Similar drawing retrieval by shape features | European filing — geometric shape feature vectors for similarity matching |
| WO 2026004458A1 | Advanced similar drawing retrieval | Improved shape feature matching (PCT/international) |

### Supporting Patents

| Patent # | Title | Innovation |
|----------|-------|-----------|
| JP 2023100170A | Drawing search via title column attributes | Title block parsing → structured attributes → search |
| JP 2024113144A | Raster-to-vector with dimension recognition | Scanned drawings → vectorize → recognize dimensions |
| WO 2026004078A1 | Component table extraction | BOM table parsing from drawing images |
| WO 2026022945A1 | Drawing annotation management | Collaborative annotation with access control |
| + ~20 more | Computing/calculating categories | Various shape/drawing analysis innovations |

### Acquired Patents (from Plethora, Jul 2022)

Plethora (US CNC startup, bankrupted Nov 2021) — CADDi's first external patent acquisition:
- **Auto DFM** — instantly identify un-machinable areas + suggest fixes
- **Auto Quote** — real-time price quotes from machine hours + production parameters
- **Auto CAM** — AI-generated machining programs from material type + geometry

### Reverse-Engineered Similarity Search Architecture

```
Drawing upload (PDF/TIFF/DWG/hand-drawn scan)
    ↓
OCR + symbol detection (text, GD&T, title block)
    ↓
Geometric feature extraction → shape "fingerprint"
    (proprietary CNN/vision model trained on millions of Japanese drawings)
    ↓
Feature vector stored in vector database
    ↓
Nearest-neighbor search against entire drawing archive
    ↓
Return ranked similar drawings + linked procurement data
```

**Key details:** Kaggle Grandmasters on the ML team. Handles 30+ year old hand-drawn scans. Can convert 2D → 3D-like models. Known limitation: orientation/placement changes can cause dissimilarity — suggests global shape descriptors, not purely local feature matching.

### Competitive Moat Assessment

| Moat | Strength | Why |
|------|----------|-----|
| Data flywheel | VERY HIGH | 300K+ drawings per customer, millions total |
| Switching costs | VERY HIGH | Once 500K drawings indexed + linked to procurement history, migration is painful |
| Patents | MEDIUM | 28 patents block direct copying of their specific method, but not the general approach |
| Model quality | HIGH | Trained on millions of real drawings; competitors can't easily replicate |

## Drawing Similarity Search — Business Viability (Confirmed)

### Market Players

| Company | Founded | Funding | Approach | Status |
|---------|---------|---------|----------|--------|
| **CADDi Drawer** | 2017 (Japan) | $202M | Proprietary DL on 2D drawings | **$470M valuation**, expanding to US (Dallas) |
| **CADENAS PARTsolutions** | 1992 (Germany) | Bootstrapped | Geometric "GEOsearch" on 3D | 600+ enterprise customers, $30-50M revenue, **30yr profitable** |
| **Physna/Thangs** | 2015 (USA) | $43M (Sequoia) | 3D geometric deep learning | **Pivoted to marketplace** — cautionary signal |
| **Part Analytics** | ~2019 | Unknown | NLP-based part description matching | MRO/indirect parts |

### Business Model (CADDi Drawer)
- SaaS: $50K-$200K/year per customer based on drawings indexed
- Customer uploads 50K-500K+ historical drawings
- AI extracts features + links to procurement history (cost, supplier, lead time)
- Finding: 30% of "new" parts had near-identical existing designs
- 10-25% cost reduction when procurement leverages historical pricing (McKinsey)

### Viability Assessment
- **Switching costs: VERY HIGH** — 50K-500K drawings indexed, migration is painful
- **TAM: $2-5B globally**
- **LLM disruption risk:** Moderate (3-5yr window before general AI commoditizes basic similarity)
- **Best as:** Feature inside broader cost/procurement platform, not standalone

### Technical Approach for Costimize MVP (2-4 weeks)
1. DINOv2 embeddings on drawing images (pre-trained, no fine-tuning)
2. FAISS vector database for nearest-neighbor search
3. Link to historical PO data (already parsed in `po_store.py`)
4. Human feedback loop for accuracy improvement

**Patent safety:** CADDi's patents cover their specific shape feature extraction method. Using standard vision embeddings (DINOv2, CLIP) + vector search (FAISS) is a completely different technical approach — no patent conflict.

### The Killer Combo: Similarity + Physics
| Method | Speed | Accuracy | Explainability |
|--------|-------|----------|---------------|
| Similarity-only | Instant | 15-25% | "Similar part cost ₹X" |
| Physics-only | Minutes | 5-10% | Full line-by-line breakdown |
| **Both combined** | Instant + Minutes | **5-10%** | "Similar part ₹450 + physics says ₹470 → target ₹460" |

---

# PART 6: ARCHITECTURE INSPIRATIONS

## Tesla's HydraNet → Drawing Analysis Mapping
| Tesla Concept | Drawing Equivalent |
|--------------|-------------------|
| Multi-camera fusion (8 views → unified) | Multi-view drawing fusion (front/side/section → 3D understanding) |
| Object detection (cars, signs) | Symbol detection (GD&T frames, dimension arrows, roughness symbols) |
| BEV transformation (2D → top-down) | Drawing-to-3D transformation (orthographic views → part geometry) |
| HydraNet multi-task heads | Shared backbone, separate heads: dimensions, GD&T, materials, surface finish |
| Shadow mode / fleet data | Customer uploads = training data pipeline |
| Auto-labeling | AI pre-label → human verify → corrections feed back |

## Reducto's 3-Layer Architecture → Drawing Pipeline
| Reducto Layer | Drawing Equivalent |
|--------------|-------------------|
| CV segmentation (regions) | YOLOv11-OBB detection (9 annotation categories) |
| VLM interpretation (context) | Donut/Florence-2 structured parsing |
| Agentic self-correction | Engineering rule validation (dimensions must sum, tolerances must reference valid datums) |

## Werk24 Output Schema (Gold Standard)
```
Dimensions: Size (type + value + unit + tolerance)
Tolerances: fit + deviations + grade + flags (general/reference/exact)
GD&T: 15 characteristics, zone, feature, reference, material_condition, datums
Threads: ISO Metric, UTS, Whitworth, ACME, NPT, SM, Knuckle (7 types)
Surface Roughness: 7 standards, 30+ parameters, direction of lay
Material: 3-level hierarchy (400+ types), raw_ocr + standard + designation
Manufacturing: Primary process (DIN 8580), secondary processes, bounding dimensions
Confidence: 0-1 score per field
```

---

# PART 7: PROF JAY LEE'S FRAMEWORKS

## 5C Architecture → Costimize Mapping
| Level | Name | Costimize Equivalent |
|-------|------|---------------------|
| L1 | Connection | Upload drawing (PDF/DXF) |
| L2 | Conversion | AI extracts dimensions, processes, materials |
| L3 | Cyber | Cost engine calculates should-cost |
| L4 | Cognition | Historical PO comparison, line-by-line breakdown |
| L5 | Configuration | (Future) Auto-suggest design changes to reduce cost |

## "Egg Model" → Costimize
- **Yolk** = Domain knowledge (config.py: 18 process rates, material DB, Indian economics)
- **White** = AI layer (Gemini vision, process detection)
- **Shell** = Infrastructure (Streamlit app, JSON storage)

**Key insight: Domain knowledge IS the competitive moat. AI is the enabler, not the differentiator.**

---

# PART 7B: PROCESS PLANNING (CAPP) — THE CORE MOAT

## What CAPP Does
```
Engineering Drawing/CAD → Feature Recognition → Process Sequence → Time Estimation → Cost
```
**This is what separates a $50/month tool from a $150K/year platform (aPriori).**

## Research Papers Analyzed (Your papers/ folder)

### ARKNESS (arXiv 2506.13026, June 2025) — UConn + US Army
**"Knowledge Graph Fusion with LLMs for Manufacturing Process Planning"**

- Fuses Knowledge Graphs with small LLMs for CNC process planning
- **3B Llama-3 + Knowledge Graph matches GPT-4o** on 155 machining questions
- +25pp multiple-choice accuracy, +22.4pp F1, 8.1x ROUGE-L vs standalone LLM
- Reduces hallucinations by 22pp
- **Runs fully on-premise** — no cloud API needed
- Built KG from: 5-axis milling review, CNC process knowledge base, industrial robotics, CNC fundamentals, sustainability, machining parameters, CAD/CAM programming
- Total KG: 4,329 triples, 6,659 unique entities, 1,251 unique relations

**Actionable for Costimize:**
1. Build Knowledge Graph from your machining papers (Machinery's Handbook, Boothroyd, drilling handbook)
2. Use PostgreSQL to store entity-relation triples
3. Semantic search (embeddings) to retrieve relevant triples for each query
4. Augment small local model with retrieved knowledge
5. Result: accurate process parameters without cloud API dependency

### CAPP-GPT (TechRxiv 1297057, May 2025) — U of Windsor + KFUPM
**"Large Multimodal Model for Macro-CAPP via Custom Encoder-Decoder"**

- Custom GPT architecture for process planning from CAD B-Rep data
- Part Encoder → geometric feature recognition → processing feature mapping → Plan Decoder
- **Generates its own training corpus** using OR + ML hybrid (no commercial dataset needed)
- Feature dictionary maps geometric features → processing features:
  - Blind Hole → center drilling, drilling, boring, reaming
  - Through Hole → center drilling, drilling, boring, reaming
  - Threaded Hole → center drilling, drilling, boring, chamfering, tapping, deburring
  - Closed/Open Pocket → rough milling, semi-finishing, precision finish, deburring
  - Slots → rough milling, finishing
  - Steps/Bosses → face milling, profile milling
  - Chamfers/Fillets → chamfering tool, radius end mill

**Actionable for Costimize:**
1. Use this feature→process mapping in your cost engine
2. The mapping is directly usable: add to `process_db.py`
3. Synthetic training data approach means you can start without customer data

## STEP File Processing — The Technical Unlock

### What STEP Files Contain (extractable with PythonOCC, free)

| Data | Value for Cost Estimation |
|------|--------------------------|
| Bounding box | Stock size → material volume |
| Volume | Material weight → material cost |
| Surface area | Finishing cost calculation |
| Face types (planar, cylindrical, conical) | Feature detection |
| Internal cylindrical faces | Hole detection → drilling time |
| Edge count | Part complexity score |
| Thread detection (helical edges) | Threading operation time |

### Python Libraries

| Library | Maturity | License | Best For |
|---------|----------|---------|----------|
| **PythonOCC** | Mature | LGPL | Full B-Rep traversal, measurements |
| **CadQuery** | Mature | Apache 2.0 | Parametric CAD scripting + STEP read |
| **OCP** | Mature | LGPL | Lower-level, faster |

### Implementation Priority

| Phase | Effort | What |
|-------|--------|------|
| Phase 1 | 2-3 days | Read STEP → bounding box, volume, surface area |
| Phase 2 | 1-2 weeks | Classify faces → detect holes, pockets, threads |
| Phase 3 | Future | ML feature recognition (train on MFCAD++ dataset) |

### What Competitors Accept

| Platform | Primary | All Formats |
|----------|---------|-------------|
| Xometry | STEP | STEP, SLDPRT, STL, DXF, IPT, X_T, CATPART |
| Protolabs | STEP | STEP, SLDPRT, IPT, X_T, CATPART |
| Paperless Parts | STEP | STEP + PDF drawing |

## IDP Market & Document Orchestration

### Market Size
- Global IDP market (2023): $2.8-3.5B → $10-12B by 2028-2030 (33% CAGR)
- Manufacturing vertical: 15-18% = **$1.5-1.8B by 2028**

### Manufacturing Document Automation Levels
| Department | Current Automation | Value of AI |
|------------|-------------------|-------------|
| Finance (invoices) | HIGH (60-70%) | Medium — commodity |
| Procurement (POs, RFQs, BOMs) | LOW (15-25%) | **Very High** |
| Quality (inspection, CoCs) | VERY LOW (5-10%) | **Very High** |
| Engineering (drawings, specs) | VERY LOW (<5%) | **Highest** |

### Strategic Decision
**Don't be a document orchestrator (middleware). Be a manufacturing intelligence platform.**
- Document classification → commodity (GPT-4o does this)
- The value is in what you DO with extracted data (cost estimation, negotiation leverage)
- Build cost intelligence first, expand document intake surface later

## Business Model

| Phase | Model | Price |
|-------|-------|-------|
| Now | Free / ₹99-199 per estimate | Build trust, get feedback |
| 10 customers | ₹300-500/estimate or ₹5K/month pack | Prove willingness to pay |
| 50 customers | SaaS tiers ₹15K-2L/month | Recurring revenue |
| Enterprise | On-prem + % of savings | Maximum value capture |

Revenue math: 1 mid-size manufacturer = 200-500 RFQs/month. At ₹300/estimate = ₹60K-1.5L/month.

---

# PART 8: KEY RESEARCH PAPERS

| Paper | Key Finding | Costimize Relevance |
|-------|------------|-------------------|
| arXiv 2411.03707 | Florence-2 fine-tuned on 400 drawings beats GPT-4o by 52% F1 | Blueprint for fine-tuning phase |
| arXiv 2506.17374 | YOLOv11-OBB + Donut: 94% F1, 9 categories, manufacturing JSON output | **Most actionable** — pipeline + output format |
| arXiv 2505.01530 | Unified Donut model beats category-specific ensembles. 20hr training on RTX 4090 | Confirms single model approach |
| **arXiv 2508.12440** | **DXF geometric features + XGBoost: 3.91% MAPE on cost prediction** | **Most relevant** — direct DXF→cost pipeline |
| **arXiv 2506.13026** | **ARKNESS: 3B Llama-3 + Knowledge Graph = GPT-4o accuracy on machining** | **Build KG from machining papers for process planning** |
| **TechRxiv 1297057** | **CAPP-GPT: Custom encoder-decoder for process planning from CAD B-Rep** | **Feature→process mapping directly usable** |
| MDPI 2023 (Lin) | YOLOv7 + Tesseract: 85% accuracy | Superseded by newer approaches |
| eDOCr2 (2025) | 93.75% text recall, <1% CER | Good OCR baseline |
| Springer 2024 (survey) | Confirmed YOLO+VLM is state-of-the-art | Literature validation |

---

# PART 9: GITHUB REPOS WORTH STUDYING

| Repo | Stars | Use For |
|------|-------|---------|
| mozman/ezdxf | 1,244 | DXF parsing (your primary extraction tool) |
| PaddlePaddle/PaddleOCR | 50K+ | OCR backbone for image-based drawings |
| clovaai/donut | 5K+ | Document understanding transformer |
| W24-Service-GmbH/werk24-python | 85 | Output schema reference |
| sanjai-CHQ/Inticore_AI_2D | 0 | **Best open-source pipeline** — 8-stage architecture directly reusable |
| acen20/ga-analysis | 1 | YOLOv8 + PaddleOCR + DONUT pipeline |
| Bakkopi/engineering-drawing-extractor | 75 | OpenCV + Tesseract baseline |
| teddyz829/Data-Augmentation-Engineering-Drawing | 5 | Synthetic training data generation |
| whjdark/AAGNet | — | Machining feature recognition from B-Rep |
| Cael-Verd/Machining-Calculators | — | Python CNC calculators (MRR, feeds/speeds) |

---

# PART 9B: SANDVIK CUTTING DATA (Extracted March 29, 2026)

> Source: Sandvik Coromant Training Handbook (391 pages) — the gold standard for cutting parameters.

## Specific Cutting Force kc1 (N/mm²)

The core constant for ALL power calculations. kc1 = force at 1mm chip thickness.

| Our Material | ISO Group | kc1 (N/mm²) | mc | Taylor n | Taylor C |
|-------------|-----------|-------------|-----|----------|----------|
| Aluminum 6061 | N1 | 600 | 0.25 | 0.25 | 600 |
| Mild Steel IS2062 | P1.2 | 1600 | 0.25 | 0.25 | 300 |
| EN8 Steel | P2.1 | 1700 | 0.25 | 0.25 | 350 |
| EN24 Steel | P2.5 | 1900 | 0.25 | 0.25 | 280 |
| Stainless Steel 304 | M2 | 2000 | 0.25 | 0.22 | 250 |
| Brass IS319 | N3 | 750 | 0.25 | 0.25 | 500 |
| Copper | N3 | 800 | 0.25 | 0.25 | 450 |
| Cast Iron | K2 | 1100 | 0.25 | 0.25 | 200 |
| Titanium Grade 5 | S4 | 1350 | 0.25 | 0.20 | 150 |

## Sandvik Power Formula (Implemented in cutting_data.py)

```
Pc = (vc × ap × fn × kc) / (60 × 10³)  [kW]
kc = kc1 × (1/hm)^mc × (1 - γ₀/100)   [N/mm²]
hm = fn × sin(KAPR)                      [mm]
```

## Key Insight: The 15% Rule

- Reducing tool price by 30% saves only **1%** on component cost
- Increasing tool life by 50% saves only **1%** on component cost
- **Increasing cutting data by 20% saves 15% on component cost**
- Tooling is only **3%** of total cost; machine + labour is **58%**

## Tool Life Correction Factors (Sandvik base: 15 min)

| Target Life (min) | 10 | 15 | 20 | 25 | 30 | 45 | 60 |
|---|---|---|---|---|---|---|---|
| Speed Factor | 1.11 | 1.00 | 0.93 | 0.88 | 0.84 | 0.75 | 0.70 |

> Full extraction: see `docs/research/SANDVIK-DATA-EXTRACTION.md`

## Cross-Validation Summary — All Sources (March 29, 2026)

Engine kc1 values validated against 7 independent sources:

| Material | Engine kc1 | Sandvik | Ghosh Uc | Stephenson | r3ditor | Kennametal | Status |
|----------|-----------|---------|----------|------------|---------|------------|--------|
| Al 6061 | 700 | 600-800 | 400-700 | 0.012-0.022 us | 800 | — | OK |
| Mild Steel IS2062 | 1650 | 1700 | 1400 | 0.05-0.066 us | 1700 | 1640 | OK |
| SS 304 | 2050 | 2100 | — | 0.055-0.09 us | 2100 | 2070 | OK |
| Brass IS319 | 750 | 750 | 560-830 | 0.056-0.07 us | — | — | OK |
| EN8 (C45) | 1700 | 1700 | ~1400+ | 0.065-0.09 us | — | 1700 | OK |
| EN24 (4340) | 1900 | 1900 | ~1500+ | 0.065-0.09 us | — | 1890 | OK |
| Copper | 800 | 800 | 900-1260 | 0.027-0.04 us | — | — | OK |
| Cast Iron | 1100 | 1100 | 1100-1600 | 0.044-0.08 us | — | 1070 | OK |
| Ti Gr5 | 1420 | 1500 | — | 0.053-0.066 us | 1500 | — | OK |

**New data integrated (March 29):**
- Kienzle correction factors: Kw (tool wear 1.0-1.5), Ksp (chip compression: turning=1.0, milling=1.2)
- Shear stress per material from Ghosh & Mallik / P.N. Rao (for force calculations)
- Extended Taylor exponents (feed a=0.77, DOC b=0.37 — speed has 5-6× more impact than feed)
- Surface finish formula: Ra = f²×1000/(32×rn) μm, with material correction factors
- Milling specific energy and force coefficients from Ghosh & Mallik Tables 4.13-4.14
- Material mechanical properties (UTS, yield, hardness, elongation) + IS-AISI grade mapping

> Full extractions: `STEPHENSON-DATA-EXTRACTION.md`, `GHOSH-MALLIK-DATA-EXTRACTION.md`, `PN-RAO-VOL1-DATA-EXTRACTION.md`, `PN-RAO-VOL2-DATA-EXTRACTION.md`

---

# PART 9C: MANUFACTURING PROCESSES BY INDUSTRY (March 29, 2026)

50+ manufacturing processes mapped across defense, aerospace, and automobile sectors.

## Process Coverage Summary

| Category | Process Count | Defense | Aerospace | Auto |
|----------|--------------|---------|-----------|------|
| Subtractive (Machining) | 14 | Heavy | Heavy | Heavy |
| Sheet Metal | 11 | Heavy | Heavy | Heavy |
| Forming/Forging | 7 | Medium | Heavy | Heavy |
| Casting | 5 | Medium | Medium | Heavy |
| Joining/Welding | 9 | Heavy | Heavy | Heavy |
| Surface Treatment | 14 | Heavy | Heavy | Heavy |
| Heat Treatment | 10 | Heavy | Heavy | Heavy |
| Composites/Additive | 7 | Medium | Heavy | Light |
| Inspection/Testing | 10 | Mandatory | Mandatory | Sampling |

## Implementation Priority for Costimize

- **Phase 1 (DONE):** CNC Turning, Milling, Drilling, Grinding, Heat/Surface Treatment
- **Phase 2 (NEXT):** Laser Cutting, Bending, Stamping, Deep Drawing
- **Phase 3:** Wire EDM, Investment Casting, Forging, NDT Cost Adder
- **Phase 4:** Die Casting, Gear Cutting, Welding, Powder Metallurgy

> Full mapping: see `docs/research/MANUFACTURING-PROCESSES-BY-INDUSTRY.md`

---

# PART 9D: SHEET METAL COST ESTIMATION (Research March 29, 2026)

Physics-based models for all sheet metal processes, ready for implementation.

## Master Formula

```
Total Cost = Material + Cutting + Bending + Stamping + Finishing + Overhead + Profit
Material Cost = sheet_area × thickness × density × price/kg / utilization%
```

## Key Data Points Captured

| Process | Key Formula | Indian Rate |
|---------|------------|-------------|
| Fiber Laser (1-3kW) | cut_length / speed(material,thickness) × rate | ₹800-2000/hr |
| Press Brake Bending | tonnage = (UTS × L × t²) / (V × 1000) | ₹600-1200/hr |
| Stamping | die_cost / volume + cycle_time × rate | ₹1000-2500/hr |
| Deep Drawing | blank_diameter = √(d² + 4dh) | ₹800-1500/hr |
| Welding (MIG) | length / deposition_rate × rate | ₹500-800/hr |

## Laser Cutting Speeds (m/min) — Fiber Laser

| Material | 1mm | 2mm | 3mm | 5mm | 8mm | 12mm |
|----------|-----|-----|-----|-----|-----|------|
| Mild Steel | 25 | 12 | 7 | 3.5 | 1.8 | 0.8 |
| Stainless | 20 | 9 | 5 | 2.5 | 1.2 | 0.5 |
| Aluminum | 30 | 15 | 8 | 4 | 2 | 0.9 |

> Full research: see `docs/research/sheet-metal-cost-estimation.md`

---

# PART 9E: BIBLIOGRAPHY (60+ Sources, March 29, 2026)

## Top 10 Priority Books

1. **Boothroyd — DFMA** (3rd ed, 2011) — Foundation of ALL process cost models
2. **Lincoln Electric Procedure Handbook** — FREE welding cost bible
3. **ASM Vol. 16 — Machining** — Speed/feed tables for 100+ grades
4. **Altan — Sheet Metal Forming** (2012) — Blank size, tonnage, springback
5. **Kalpakjian — Manufacturing Processes** (7th ed, 2020) — Tolerance-cost charts
6. **Stephenson — Metal Cutting Theory** (3rd ed, 2016) — Machining economics
7. **Wohlers Report 2025** — AM cost data
8. **ASM Vol. 4 — Heat Treating** — Cycle times + costs
9. **CMTI Machine Hour Rate Guide** — Indian-specific rates
10. **Mislick — Cost Estimation Methods** (2015) — CER methodology

## Already Have & Using

- Machinery's Handbook (30th ed) — 50+ material tables, Taylor constants
- Sandvik Training Handbook (2017) — kc1 values, power formulas (**integrated into engine**)
- Walter Drilling/Threading Handbook — 20+ material groups
- CNC Fundamentals (Autodesk/Titans) — SFM tables
- **Stephenson & Agapiou — Metal Cutting Theory & Practice (3rd Ed)** — specific cutting energy for 12 material groups, Taylor n by tool material (HSS 0.10-0.17, WC 0.20-0.25, coated 0.30-0.40), empirical force coefficients for 6 materials, surface finish Ra formulas, machining economics. 824-line extraction: `STEPHENSON-DATA-EXTRACTION.md` (**integrated into engine**)
- **Ghosh & Mallik — Manufacturing Science (2nd Ed)** — specific cutting energy Uc for 5 material groups, milling force coefficients (A, k for 4 materials), milling specific energy (Table 4.14), Taylor constants, deep drawing/blanking/bending forces, Merchant's model. 1236-line extraction: `GHOSH-MALLIK-DATA-EXTRACTION.md` (**integrated into engine**)
- **P.N. Rao — Manufacturing Technology Vol 1 (3rd Ed)** — Indian casting costs in INR, IS-AISI-British-German steel grade mapping (15+ grades), Indian foundry sand by 7 locations, shrinkage allowances for 25+ metals, hardness conversion table. 976-line extraction: `PN-RAO-VOL1-DATA-EXTRACTION.md` (**integrated into engine — IS grade mapping**)
- **P.N. Rao — Manufacturing Technology Vol 2 (2nd Ed)** — cutting force constants (shear stress for C45/C25/CI), milling power constants (Table 7.2), Taylor V*T^0.22=475 for AISI 4140, Indian cost rates (labour Rs 12/hr, machine Rs 40/hr), process accuracy by operation. Extraction: `PN-RAO-VOL2-DATA-EXTRACTION.md` (**integrated into engine — milling power, Taylor data**)

> Full bibliography: see `docs/research/BIBLIOGRAPHY-SOURCES.md`

---

# PART 10: BUILD ROADMAP (Updated March 29, 2026)

## Phase 1: Quick Wins (1-2 weeks)
- [ ] Swap Gemini to primary vision API (2x accuracy, 10x cheaper than GPT-4o)
- [ ] Add human-in-the-loop editable table (every correction = training data)
- [ ] Add structured JSON output schema to vision prompts

## Phase 2: STEP File Parser (2-3 days)
- [ ] Install PythonOCC (`pip install pythonocc-core`)
- [ ] Build `extractors/step_extractor.py` — read STEP → bounding box, volume, surface area
- [ ] Feed extracted geometry directly into cost_engine.py
- [ ] **Eliminates AI vision errors for 3D parts**

## Phase 3: STEP Feature Recognition (1-2 weeks)
- [ ] Classify faces (planar, cylindrical, conical, spherical)
- [ ] Detect holes (internal cylindrical faces) → diameter, depth
- [ ] Detect pockets (bounded planar regions)
- [ ] Map features → processes using CAPP-GPT paper's feature dictionary
- [ ] **Automated process detection from geometry, no AI needed**

## Phase 4: DXF/DWG Parser (2-3 weeks)
- [ ] Build `extractors/dxf_extractor.py` using ezdxf
- [ ] Parse DIMENSION entities → get_measurement()
- [ ] Parse TEXT/MTEXT → material callouts, notes, tolerances
- [ ] Add DWG support via ODA File Converter
- [ ] Route: STEP → geometry parser; DXF/DWG → programmatic; PDF/image → Gemini vision

## Phase 5: Knowledge Graph + Physics Engine (4-6 weeks)
- [x] **DONE: Implement MRR-based time calculation** from Sandvik/Machinery's Handbook cutting parameters
- [x] **DONE: Replace fixed "₹X/hr for Y min"** with physics-based MRR calculations (cutting_data.py + process_db.py rewrite)
- [x] **DONE: Integrate Sandvik kc1 values** for power calculations + Taylor tool life for tooling cost
- [x] **DONE: 19 mechanical engine tests passing** (up from 8)
- [ ] Build Knowledge Graph from machining papers (ARKNESS approach)
- [ ] Extract entity-relation triples from Machinery's Handbook, Boothroyd, drilling handbook
- [ ] Store in PostgreSQL with semantic search (embeddings)
- [ ] Feature-to-process mapping (CAPP-GPT paper's dictionary)
- [ ] **Target: ±5% accuracy on should-cost estimates**

## Phase 5B: Sheet Metal Cost Engine (NEW — research complete)
- [ ] Build `engines/sheet_metal/` module with laser cutting, bending, stamping, deep drawing
- [ ] Laser cutting: speed tables by material×thickness, pierce cost, gas cost
- [ ] Bending: tonnage calculation, time per bend, springback
- [ ] Stamping: die cost amortization, cycle time model
- [ ] Deep drawing: blank diameter calc, draw ratio limits
- [ ] Indian job shop rates integrated
- [ ] **Research complete: see `docs/research/sheet-metal-cost-estimation.md`**

## Phase 6: Drawing Similarity Search (2-4 weeks)
- [ ] DINOv2 embeddings on drawing images
- [ ] FAISS vector database for nearest-neighbor search
- [ ] Link to historical PO data (po_store.py)
- [ ] "Similar part cost ₹X" instant estimates
- [ ] Human feedback loop for accuracy improvement
- [ ] **Combines with physics engine: similarity for speed, physics for detail**

## Phase 7: Fine-Tuned Vision Model (4-8 weeks)
- [ ] Collect 1,000+ annotated drawings from customer usage
- [ ] Use GPT-4o outputs as labels (distillation)
- [ ] LoRA fine-tune Qwen2.5-VL-7B ($6-16 compute cost)
- [ ] Deploy on serverless GPU (RunPod) — $0.003-0.005/drawing
- [ ] A/B test against GPT-4o/Gemini API
- [ ] **Own model, zero privacy concern, zero API dependency**

## Phase 8: Hybrid Vision Pipeline (if needed, 4-8 weeks)
- [ ] Train YOLOv8-OBB on 200-300 annotated drawings
- [ ] Integrate PaddleOCR for text extraction
- [ ] Use fine-tuned Qwen2.5-VL-7B for semantic structuring
- [ ] Store all human corrections as training data
- [ ] Target: 90-95%+ accuracy, ~$0.001/drawing

---

# PART 11: FOUNDERS' KEY QUOTES & INSIGHTS

**Yushiro Kato (CADDi CEO):** "Engineers create new drawings over and over. Why don't you leverage past data if they're mostly identical drawings?"

**Dr. Jochen Mattes (Werk24):** Uses "ML + engineering validation double-check" — raw ML output validated against engineering rules before delivery.

**Steven Gao (IndustrialMind.ai):** "Target exact workflows where engineering judgment is the bottleneck."

**Andrew Ng (Landing AI):** "Data-centric AI: systematically engineering the data needed to build a successful AI system."

**Adit Abraham (Reducto):** "Documents were made for humans, not machines. Every visual cue carries semantic meaning that text-only approaches lose."

**Andrej Karpathy (ex-Tesla):** Use "a much heavier model than you could ever use in production for labeling, then clean up with humans."

**Jay Lee (Industrial AI):** "Data is the new oil, but domain knowledge is the refinery."

---

# SOURCES

All sources are cited inline throughout each section. Key databases searched:
- Google Patents, USPTO, EPO, WIPO
- arXiv, Google Scholar, MDPI, Springer, ScienceDirect, Frontiers
- GitHub (exhaustive search across 14+ repos)
- LinkedIn, X/Twitter, YouTube, company blogs
- 6sense, Crunchbase, PitchBook, Tracxn
- Company websites: aPriori, CADDi, Werk24, IndustrialMind.ai, Landing AI, Reducto

# Comprehensive Market & Technology Strategy Research for Costimize

**Date:** 2026-03-28
**For:** Chandrasekhar, Founder — AI.Procurve (Costimize)
**Purpose:** Answer critical business model, technology, and competitive questions before next development sprint

---

## Table of Contents
1. [Are YC/VC Companies Wrapping GPT or Building Own LLMs?](#1-ycvc-ai-companies-wrapper-vs-own-llm)
2. [Competitor Tech Stacks (CADDi, aPriori, Infrrd, etc.)](#2-competitor-technology-stacks)
3. [Fine-Tuned Vision Models vs Gemini/GPT-4o](#3-fine-tuned-vision-models-vs-geminigpt-4o)
4. [Document AI as a Horizontal Manufacturing Business](#4-document-ai-orchestrator-for-manufacturing)
5. [Drawing Similarity Search as a Business](#5-drawing-similarity-search-business)
6. [Process Planning (CAPP) and AI](#6-process-planning-capp-and-ai)
7. [STEP File Processing](#7-step-file-processing)
8. [Research Papers Analysis](#8-research-papers-analysis)
9. [Strategic Recommendations](#9-strategic-recommendations)

---

## 1. YC/VC AI Companies: Wrapper vs Own LLM

### The Hard Numbers

- **80-90% of YC AI companies (S24, W25) use foundation model APIs** (OpenAI/Anthropic/Google)
- **3-5% train models from scratch** (only well-funded model companies)
- **25-30% do API + fine-tuning** (Series A+ companies)

### What Top VCs Say

| Person | Position | Quote/Stance |
|--------|----------|-------------|
| **Sam Altman** (OpenAI) | "Thin wrappers will have a bad time" | But later softened: deep domain apps on APIs are legitimate |
| **Garry Tan** (YC President) | Application layer is the biggest opportunity | Building foundation models requires hundreds of millions — not a startup game |
| **Jared Friedman** (YC MD) | "Best AI startups solve real problems, AI isn't the product" | Explicitly encourages founders to use existing APIs |
| **a16z** (Casado/Bornstein) | Most value accrues to application layer | Wrappers are fine IF you have data moat, network effect, or workflow lock-in |
| **Sequoia** (Sonya Huang) | "Act One was models. Act Two is applications." | Winners use AI to do things previously impossible, not just cheaper |

### The "Wrapper" Graveyard vs Success Stories

| Company | Started As | Current | Outcome |
|---------|-----------|---------|---------|
| Jasper AI | Thin wrapper on GPT-3 | Still mostly wrapper | **Failed** — $1.5B → massive decline after ChatGPT launched |
| Copy.ai | Thin wrapper | Pivoted to workflow | Survived by pivoting |
| Harvey AI | API wrapper | Hybrid (API + fine-tune) | **$715M valuation** |
| Cursor | API wrapper + UX | API + custom fine-tune | **$2.5B+ valuation** |
| Perplexity | API + custom | Hybrid, own infra | **$9B valuation** |

**Pattern:** Thin wrappers die. Thick application layers (domain data + workflow + integration) thrive.

### What This Means for Costimize

**You are an API-wrapper company, and that is the correct strategy.**

Your moat is NOT the AI — it's:
- 7 years of defense manufacturing knowledge
- Indian job-shop economics (INR pricing, process rates)
- Physics-based cost models
- The full pipeline: drawing → features → process plan → cost

---

## 2. Competitor Technology Stacks

### Confirmed Tech Stack Analysis

| Company | Own Models? | LLM Usage | Core Technology | Funding |
|---------|-----------|-----------|----------------|---------|
| **CADDi** | **YES** — 28 patents, Kaggle Grandmasters on team | Unclear for text | Proprietary deep learning shape recognition + OCR | $200M+, ~$1.4B valuation |
| **aPriori** | **N/A** — NOT ML-based | No LLMs in core engine | Physics-based simulation, 440+ process models, 87 regional cost libraries | Independent (not acquired) |
| **iCaptur.AI** | **NO evidence** | Likely API wrapper | Thin disclosure, no patents, no research team | Unknown |
| **Infrrd** | **YES** — 13+ patents | Hybrid (own + refining LLMs) | Deep learning NLP/CV, template-free extraction | $25M+, Gartner Leader 2025 |
| **IndustrialMind.ai** | **Unlikely** at $1.2M funding | Almost certainly GPT-4o/Gemini | Domain expertise from ex-Tesla team + API calls | $1.2M pre-seed (Antler) |
| **Rossum** | **YES** — own "Aurora" T-LLM | Own proprietary LLM trained on 11M docs | Discriminative decoder (no hallucination by design) | $100M+, Gartner Challenger |
| **Hypatos** | **YES** — custom transformers | Hybrid (own + incorporating LLMs) | 10M+ annotated entities, customer-specific model training | ~€37M total |

### Key Competitor Deep Dives

**CADDi ($1.4B valuation):** Built proprietary vision AI trained on millions of Japanese engineering drawings. 28 registered patents. Hired Kaggle Grandmasters. Backend in Golang/Python on Google Cloud. Their similarity search converts 2D drawings into feature vectors using deep learning + nearest-neighbor search. Can handle handwritten drawings from 30+ years ago. Expanding to US market (Dallas office, 2024).

**aPriori (Gold Standard):** Pure physics-based — 440+ manufacturing process models, NOT using any LLMs. Three-layer digital twin: Product (3D CAD analysis) → Process (physics simulation) → Factory (regional cost data). Requires 3D CAD files — **cannot process 2D drawings** (this is Costimize's advantage). Charges $150K+/year.

**IndustrialMind.ai (Direct Competitor):** Founded by ex-Tesla manufacturing AI leaders. Only $1.2M pre-seed but already deploying with **Siemens, tesa, Andritz**. Same problem space: drawings → should-cost quotes, 3-5 days → 30 minutes. At $1.2M funding, almost certainly wrapping VLM APIs + domain rules (same approach as Costimize). Their moat is Tesla brand credibility + enterprise connections.

**Rossum (Document AI gold standard):** Built their own LLM ("Aurora") trained on 11M transactional documents. Key innovation: discriminative decoder that can only highlight/extract, never generate — **eliminates hallucination by design**. 92.5% accuracy. This architecture is worth studying for Costimize's extraction pipeline.

**Infrrd (IDP Leader):** 13+ patents across text extraction, template-invariant extraction, document clustering. Hybrid approach: proprietary deep learning + refining third-party LLMs. Offers on-prem deployment. Gartner Leader 2025.

---

## 3. Fine-Tuned Vision Models vs Gemini/GPT-4o

### Benchmark Reality (2024-2025 data)

| Model | Params | DocVQA | ChartQA | OCRBench |
|-------|--------|--------|---------|----------|
| **GPT-4o** | Proprietary | 92.8 | 85.7 | 736 |
| **Gemini 1.5 Pro** | Proprietary | 93.1 | 87.2 | 754 |
| **Qwen2-VL-72B** | 72B | **96.5** | **88.3** | **877** |
| **Qwen2-VL-7B** | 7B | **94.5** | 83.0 | **845** |
| **Qwen2.5-VL-7B** | 7B | **95.7** | **87.3** | **864** |
| **InternVL2.5-8B** | 8B | 93.8 | 84.7 | 822 |
| **Florence-2** | 0.77B | 80.1 | 57.2 | — |

**Key Finding: Qwen2.5-VL-7B ALREADY beats GPT-4o on document understanding — out of the box, no fine-tuning needed.**

### Fine-Tuning Dataset Size Guidelines

| Examples | Expected Outcome |
|----------|-----------------|
| 100-500 | Learns output format, marginal accuracy gains |
| 1,000-3,000 | **Significant domain adaptation. 10-20% improvement.** |
| 5,000-10,000 | Can match/beat GPT-4o on narrow tasks |
| 10,000+ | Diminishing returns |

### Cost Comparison

| Approach | Cost | Break-Even vs GPT-4o |
|----------|------|---------------------|
| LoRA fine-tune Qwen2.5-VL-7B | **$6-16** one-time | N/A |
| Self-host on A10G (24GB) | $350-500/month | ~33K drawings/month |
| Serverless (RunPod) | $0.003-0.005/drawing | **Immediately cheaper** |
| GPT-4o API | $0.012/drawing | Baseline |
| Local RTX 4090 | $1,600 one-time | ~11K drawings/month |

### Engineering Drawing Extraction — The Gap

- **No public benchmark exists** for engineering drawing dimension/GD&T extraction
- GPT-4o struggles with GD&T symbols (~60-70% accuracy on feature control frames)
- **This is your opportunity** — a fine-tuned model on 1,000 annotated drawings would have no competition
- Your labeled dataset becomes a competitive moat

### Recommended Path

| Phase | When | What |
|-------|------|------|
| **Now** | Pre-PMF | Use GPT-4o/Gemini API. $0.012/drawing. |
| **100+ customer drawings** | After PMF | Use GPT-4o outputs to label data (distillation) |
| **1,000+ drawings** | Scale | Fine-tune Qwen2.5-VL-7B with LoRA ($6-16) |
| **10K+ drawings/month** | Growth | Deploy on serverless GPU. Zero privacy concern. |

---

## 4. Document AI Orchestrator for Manufacturing

### IDP Market Size

| Metric | Value |
|--------|-------|
| Global IDP market (2023) | $2.8-3.5B |
| Projected (2028-2030) | $10-12B |
| CAGR | 30-37% |
| Manufacturing vertical | 15-18% = **$1.5-1.8B by 2028** |

### Manufacturing Documents by Department

| Department | Document Types | Current Automation | Value |
|------------|---------------|-------------------|-------|
| **Finance** | Invoices, credit notes | HIGH (60-70%) | Medium — commodity |
| **Procurement** | POs, RFQs, BOMs | LOW (15-25%) | **Very High** |
| **Quality** | Inspection reports, CoCs, PPAP | VERY LOW (5-10%) | **Very High** |
| **Engineering** | Drawings, GD&T specs, ECNs | VERY LOW (<5%) | **Highest** |
| **Sales** | Customer RFQs, order confirmations | LOW (20-30%) | High |

### Is the Orchestrator a Business or a Feature?

**The orchestrator alone is middleware that gets squeezed. The orchestrator + domain intelligence IS the business.**

- Document classification → commodity (GPT-4o does this)
- Extraction → many tools do this
- **What you DO with extracted data** → this is the value

### The Right Framing

Don't say: "We're a document AI orchestrator for manufacturing"
Say: **"Upload any manufacturing document → get actionable intelligence"**

- Drawing → should-cost breakdown
- BOM → component cost optimization
- PO → historical price benchmarking
- Quality doc → cost of quality analysis
- Supplier quotation → automatic comparison

**This is a manufacturing intelligence platform, not a document processor.**

---

## 5. Drawing Similarity Search Business

### Is Drawing Similarity Search a Real Business?

**YES — proven by CADDi ($1.4B), CADENAS (30yr profitable), Physna ($37M raised).**

### The Players

| Company | Founded | Funding | Approach | Status |
|---------|---------|---------|----------|--------|
| **CADDi Drawer** | 2017 (Japan) | $200M+ | Proprietary deep learning on 2D drawings | $1.4B unicorn, expanding to US |
| **CADENAS PARTsolutions** | 1992 (Germany) | Bootstrapped | Geometric similarity "GEOsearch" on 3D | 600+ enterprise customers, $30-50M revenue |
| **Physna/Thangs** | 2015 (USA) | $43M (Sequoia) | 3D geometric deep learning | Pivoted to community/marketplace — cautionary signal |
| **Part Analytics** | ~2019 | Unknown | NLP-based part description matching | Indirect/MRO parts focus |
| **Elysium** | Japan | Unknown | CAD translation + similarity | Competes with CADDi in Japan |

### Who Pays and Why

| Buyer | Use Case | Value |
|-------|----------|-------|
| **Procurement** | "Similar part cost ₹X last time — negotiate from there" | 10-25% cost reduction (McKinsey) |
| **Engineering** | "Has this been designed before?" | 60% of "new" parts are near-identical (Aberdeen Group) |
| **Quality** | "What defects happened on similar parts?" | Predictive quality |
| **Cost Estimation** | "Similar part = instant estimate" | Fastest estimation method |

### CADDi Drawer Deep Dive

- SaaS priced per drawings indexed: ~$50K-$200K/year per customer
- Processes handwritten drawings from 30+ years ago
- Can search by uploading a photo/sketch
- Customer result: 30% of "new" parts had near-identical existing designs
- Expanding to Thailand, Vietnam, US (not Japan-specific)

### Business Viability Assessment

| Factor | Rating |
|--------|--------|
| Recurring revenue | **Strong** — SaaS with growing usage |
| Switching costs | **Very High** — 50K-500K+ drawings indexed, migration is painful |
| Network effects | Weak cross-company, strong within-company |
| TAM | $2-5B globally |
| LLM disruption risk | Moderate — 3-5yr window before general AI commoditizes basic similarity |
| Best as standalone? | **No — best as wedge into broader procurement intelligence** |

### Technical Approach for Costimize MVP (2-4 weeks)

1. **DINOv2 embeddings** on drawing images (pre-trained, no fine-tuning for v1)
2. **FAISS** vector database for nearest-neighbor search
3. Link each drawing to historical cost/supplier/lead time
4. Human feedback loop to improve over time
5. 80%+ useful accuracy achievable out-of-the-box

### The Killer Combo: Similarity + Physics

| Method | Speed | Accuracy | Explainability |
|--------|-------|----------|---------------|
| Similarity-only | Instant | 15-25% | "Similar part cost ₹X" |
| Physics-only | Minutes | 5-10% | Full line-by-line breakdown |
| **Both combined** | Instant + Minutes | **5-10%** | "Similar part ₹450 + physics says ₹470 → target ₹460" |

When both agree → high confidence. When they disagree → worth investigating.

---

## 6. Process Planning (CAPP) and AI

### What CAPP Does

```
Engineering Drawing/CAD → Feature Recognition → Process Sequence → Time Estimation → Cost
```

### Current State

| System | Year | Approach | Result |
|--------|------|----------|--------|
| ARKNESS (Paper 1) | 2025 | Knowledge Graph + 3B Llama-3 | **Matches GPT-4o** on machining questions |
| CAPP-GPT (Paper 2) | 2025 | Custom encoder-decoder on CAD data | Generates process plans from B-Rep geometry |
| aPriori | Commercial | Physics-based simulation | Gold standard, $150K+/year |
| Siemens Tecnomatix | Commercial | Full CAPP suite | Enterprise, $100K+ |
| Xometry/Protolabs | Internal | ML on STEP features | Not sold as product |

### Why This Matters for Costimize

Your `process_detector.py` + `cost_engine.py` IS a simplified CAPP system. The upgrade path:

1. **Current:** AI guesses processes from 2D drawing
2. **Next:** STEP geometry → deterministic feature → process mapping
3. **Later:** Knowledge Graph (ARKNESS approach) for process reasoning
4. **Eventually:** This becomes your core IP

### ARKNESS Paper Key Takeaway

> A **3B Llama-3** + Knowledge Graph of machining handbooks = GPT-4o accuracy.
> No expensive model needed. Build the knowledge base from your machining papers.

### CAPP-GPT Paper Key Takeaway

> Custom GPT architecture processes CAD B-Rep data directly.
> Training data can be **synthetically generated** — you don't need real manufacturing data to start.

---

## 7. STEP File Processing

### What You Can Extract from STEP (using PythonOCC, free)

| Data | Value for Cost Estimation |
|------|--------------------------|
| Bounding box | Stock size calculation |
| Volume | Material weight → material cost |
| Surface area | Finishing cost |
| Face types (planar, cylindrical, conical) | Feature detection |
| Internal cylindrical faces | Hole detection → drilling time |
| Edge count | Part complexity score |

### Priority Implementation

| Phase | Effort | What |
|-------|--------|------|
| Phase 1 | 2-3 days | Read STEP → bounding box, volume, surface area, face count |
| Phase 2 | 1-2 weeks | Classify faces → detect holes, pockets, threads → map to processes |
| Phase 3 | Future | ML-enhanced feature recognition (train on MFCAD++ dataset) |

### What Competitors Accept

| Platform | Primary | All Formats |
|----------|---------|-------------|
| Xometry | STEP | STEP, SLDPRT, STL, DXF, IPT, X_T, CATPART |
| Protolabs | STEP | STEP, SLDPRT, IPT, X_T, CATPART |
| Paperless Parts | STEP | STEP + PDF drawing |

---

## 8. Research Papers Analysis

### Paper 1: ARKNESS (arXiv 2506.13026, June 2025)
**"Knowledge Graph Fusion with LLMs for Manufacturing Process Planning"**
- University of Connecticut + US Army
- Fuses Knowledge Graphs with small LLMs for CNC process planning
- **3B Llama-3 + KG matches GPT-4o** on 155 machining questions
- +25pp multiple-choice accuracy, +22.4pp F1, 8.1x ROUGE-L
- Reduces hallucinations by 22pp
- **Runs fully on-premise** — no cloud API needed

**Actionable for Costimize:**
- Build a Knowledge Graph from your machining papers (Machinery's Handbook, Boothroyd, etc.)
- Use it to augment a small local model for process planning
- This is the ARKNESS approach — proven to work

### Paper 2: CAPP-GPT (TechRxiv 1297057, May 2025)
**"Large Multimodal Model for Macro-CAPP via Custom Encoder-Decoder"**
- University of Windsor + KFUPM
- Custom GPT architecture for process planning from CAD B-Rep data
- Part Encoder → geometric features → processing features → Plan Decoder
- **Generates its own training corpus** using OR + ML hybrid
- No commercial dataset needed

**Actionable for Costimize:**
- Feature dictionary (Tables 1-2) maps geometric features → processing features
- This IS the mapping your cost engine needs: hole → center drill + drill + bore + ream
- The synthetic training data approach means you can start without customer data

---

## 9. Strategic Recommendations

### Decision 1: Build Own Model vs Wrap APIs?

**WRAP APIs NOW. Fine-tune later.**

- 80-90% of funded AI companies do this
- Your moat is domain knowledge, not a model
- Fine-tune Qwen2.5-VL-7B when you have 1,000+ customer drawings
- Cost: $6-16 for LoRA fine-tuning

### Decision 2: What Format to Prioritize?

**PDF now (you have it). STEP next (2-3 days to prototype).**

- PDF is what customers send today
- STEP eliminates AI vision errors and enables feature recognition
- DXF for sheet metal later

### Decision 3: Document Orchestrator or Cost Intelligence?

**Cost intelligence.** The orchestrator is middleware. The intelligence is the product.

Framing: "Upload any manufacturing document → get actionable cost intelligence"

### Decision 4: Similarity Search?

**Yes, but as a feature of cost estimation, not a separate product.**

- "This part is 85% similar to Part X which cost ₹450"
- Variant-based estimation complements your physics-based engine
- Build the embedding database as customers use your tool

### Decision 5: Process Planning (CAPP)?

**Build incrementally — it's your core IP.**

1. Current: AI detects processes from drawing
2. Next: STEP features → deterministic process mapping
3. Then: Knowledge Graph from machining handbooks (ARKNESS approach)
4. This is what separates a $50/month tool from a $150K/year platform

### Decision 6: The Business Model?

**Start per-estimate, evolve to SaaS.**

| Phase | Model | Price |
|-------|-------|-------|
| Now | Free / ₹99-199 per estimate | Build trust |
| 10 customers | ₹300-500/estimate or ₹5K/month pack | Prove willingness to pay |
| 50 customers | SaaS tiers ₹15K-2L/month | Recurring revenue |
| Enterprise | On-prem + % of savings | Maximum value capture |

### The 90-Day Priority Stack

| Week | Action | Impact |
|------|--------|--------|
| 1-2 | STEP file parser (PythonOCC) — bounding box, volume, surface area | Eliminates AI vision errors for 3D parts |
| 3-4 | STEP feature recognition — holes, pockets, threads | Automated process detection |
| 5-6 | Knowledge Graph from machining papers (ARKNESS approach) | Accurate process parameters |
| 7-8 | Upgrade physics engine with real cutting models from papers | ±5% accuracy target |
| 9-10 | Drawing similarity search (embedding-based) | "Similar part cost ₹X" |
| 11-12 | Fine-tune Qwen2.5-VL-7B on accumulated drawings | Own model, zero API cost |

---

## Sources

### Papers
- ARKNESS: arXiv 2506.13026v1 (June 2025) — Hoang et al., UConn + US Army
- CAPP-GPT: TechRxiv 1297057 (May 2025) — Azab et al., U of Windsor + KFUPM

### Market Data
- Mordor Intelligence, MarketsandMarkets — IDP market sizing
- 6sense — CAD market share
- Cognitive Market Research — CAD Software Market 2026
- Crunchbase — company funding data

### Technical Benchmarks
- Qwen2-VL technical report (arXiv:2409.12191)
- InternVL2 report (arXiv:2404.16821)
- MFCAD++ dataset benchmarks

### Investor Analysis
- a16z "Who Owns the Generative AI Platform" (2023)
- Sequoia "Generative AI's Act Two" (2024)
- YC blog posts (Jared Friedman)
- Garry Tan public statements
- Sam Altman YC talks

### Company Research
- CADDi, aPriori, Infrrd, Rossum — public documentation and press releases
- Xometry, Protolabs, Hubs — accepted file format documentation

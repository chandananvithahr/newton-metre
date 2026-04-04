---
slug: competitors
title: Competitive Landscape
keywords: aPriori, CADDi, IndustrialMind, Pactum, competitors, should-cost, similarity search, negotiation, 3D CAD, 2D drawings, wrapper, own models, competitive advantage, moat, market position
sources: MASTER-RESEARCH-REPORT.md, comprehensive-market-strategy-research.md
updated: 2026-04-04
---

# Competitive Landscape

Newton-Metre operates at the intersection of three markets: should-cost estimation, drawing similarity search, and AI procurement. No single competitor covers all three from 2D drawings with Indian manufacturing economics.

## Key Competitors

### aPriori -- The Physics Gold Standard

**Profile:** PE-backed, 500+ employees, charges $100K-$500K+/year per contract.

**What they do:** Pure physics-based should-cost estimation using 440+ mechanistic process models and 87 regional cost libraries. Three-layer digital twin: Product (3D CAD analysis), Process (physics simulation), Factory (regional cost data). Not ML-based -- no LLMs in the core engine.

**Critical limitation:** Requires 3D CAD files. Cannot process 2D drawings. Indian MSMEs overwhelmingly work with 2D PDFs (60-70% of drawings exchanged as PDF). 97% of Indian MSMEs are micro-enterprises that cannot justify 3D CAD expense.

**Threat level:** HIGH for 3D-capable enterprises, but structurally unable to serve the 2D drawing market.

### CADDi -- The Similarity Unicorn

**Profile:** Founded 2017 (Japan), $200M+ raised, $1.4B valuation, 28 registered patents, Kaggle Grandmasters on engineering team.

**What they do:** Drawing similarity search + procurement data platform. Proprietary deep learning shape recognition trained on millions of Japanese engineering drawings. Can handle handwritten drawings from 30+ years ago. Backend in Golang/Python on Google Cloud. Expanding to US market (Dallas office, 2024).

**Results:** Search reduced from hours to seconds. 1.5-2.1x faster quotations. Dairy Conveyor Corporation recovered 600 hours/year. Customer list includes Hitachi, Kawasaki, Subaru.

**Critical limitation:** Does NOT do should-cost estimation. Comparison-based pricing only ("similar part cost X last time"), no first-principles cost breakdown. Their 28 patents cover shape-fingerprinting, not cost modeling.

**Threat level:** MEDIUM. Strong in similarity but does not compete on should-cost.

### IndustrialMind.ai -- The Direct Competitor

**Profile:** Founded by ex-Tesla manufacturing AI leaders. $1.2M pre-seed (Antler, Nov 2025). Already deployed at Siemens, tesa, Andritz.

**What they do:** AI Manufacturing Engineer -- drawing to BOM to routing to cost, plus production monitoring. Same problem space: 3-5 days estimation reduced to 30 minutes.

**Tech stack:** At $1.2M funding, almost certainly wrapping VLM APIs (GPT-4o/Gemini) with domain rules -- the same approach as Newton-Metre. No disclosed patents or proprietary models.

**Competitive moat:** Tesla brand credibility + enterprise connections. Global enterprise focus, not Indian manufacturing.

**Threat level:** HIGH as direct competitor, but focused on global enterprise (Siemens-scale), not Indian MSME/defense market.

### Pactum AI -- The Negotiation Specialist

**Profile:** Backed by major VCs, focused exclusively on autonomous B2B negotiation.

**What they do:** Hybrid rule-based + LLM architecture for autonomous supplier negotiation. Rule-based AI handles offer calculation, strategy selection, counter-offer generation (MESO -- Multiple Equivalent Simultaneous Offers). LLMs handle communication personalization.

**Key results:**
- Walmart: 2,000+ suppliers negotiated autonomously, 3% average savings, payment terms extended 35 days
- Sanofi: 10% average spend reduction, 281% improvement in negotiation savings

**Critical limitation:** Negotiates without knowing what things SHOULD cost. No drawing analysis, no physics-based cost estimation. Relies on historical pricing and market data for negotiation targets.

**Threat level:** LOW as direct competitor (different product), HIGH as architecture reference for Newton-Metre's negotiation agent.

### Other Players

| Company | Focus | Relevance |
|---------|-------|-----------|
| **Werk24** | API to extract dimensions/GD&T from drawings to JSON | Complementary (extraction only, no cost) |
| **Rossum** | Document AI with own "Aurora" LLM trained on 11M docs | Architecture reference (discriminative decoder = no hallucination) |
| **Infrrd** | IDP with 13+ patents, Gartner Leader 2025 | General IDP, not cost estimation |
| **CADENAS PARTsolutions** | 3D geometric similarity ("GEOsearch"), 30yr profitable | 3D only, 600+ enterprise customers |
| **Keelvar** | Autonomous RFQ bots | Procurement automation, no cost estimation |

## The Wrapper vs Own Model Reality

Industry data from YC S24/W25 batches:
- 80-90% of AI companies use foundation model APIs (OpenAI/Anthropic/Google)
- 3-5% train models from scratch (only well-funded model companies)
- 25-30% do API + fine-tuning (Series A+ companies)

**Pattern:** Thin wrappers die (Jasper: $1.5B valuation declined after ChatGPT launch). Thick application layers thrive (Cursor: $2.5B, Harvey: $715M, Perplexity: $9B). The moat is domain knowledge + workflow, not the model.

## Newton-Metre's Unique Position

**Nobody combines all three:**
1. Should-cost estimation from 2D drawings (physics-based engines)
2. Drawing similarity search (visual + metadata embedding pipeline)
3. Institutional memory + AI procurement worker (compounding negotiation intelligence)

**Additional differentiators:**
- Works from 2D drawings (PDF, scanned, even WhatsApp photos) -- no 3D CAD required
- Indian manufacturing economics built in (INR pricing, IS/BIS standards, regional cost profiles)
- Defense/aerospace compatible (self-hosted AI roadmap for on-prem deployment)

### The 70/30 Insight

70% of procurement spend is off-the-shelf MPN-based items (connectors, fasteners, bearings) where similarity search + negotiation intelligence matters most. Only 30% is manufactured-to-drawing parts where should-cost shines. The AI must serve both segments -- no competitor addresses this split.

### Confirmed Tech Stack Comparison

| Company | Own Models? | Evidence |
|---------|-----------|----------|
| CADDi | YES | 28 patents, Kaggle Grandmasters, proprietary CNN |
| aPriori | N/A (not ML) | 440+ physics process models, no LLMs |
| IndustrialMind.ai | Unlikely | $1.2M funding, same API-wrapper approach |
| Rossum | YES | Own "Aurora" T-LLM, 11M training docs |
| Infrrd | YES | 13+ patents, Gartner Leader |
| Newton-Metre | API now, own later | Gemini/GPT-4o now, fine-tuned Qwen2.5-VL-7B planned |

## Market Sizing

| Market | Size |
|--------|------|
| AI-driven knowledge management | $7.66B (2025) to $51.36B (2030) |
| Manufacturing IDP vertical | $1.5-1.8B by 2028 |
| Drawing similarity search TAM | $2-5B globally |
| India manufacturing sector | USD 1.63T (2025) |

Zero open-source should-cost tools exist (confirmed via exhaustive GitHub survey of 79 repositories). The closest open-source tools are SVGnest (2.5K stars, nesting only) and AAGNet (feature recognition only).

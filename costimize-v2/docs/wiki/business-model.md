---
slug: business-model
title: Business Model and Go-to-Market Strategy
keywords: business model, flywheel, pricing, SaaS, per-estimate, enterprise, on-prem, defense, aerospace, automobile, first customers, CADDi, aPriori, similarity search, procurement, Indian manufacturing, YC
sources: comprehensive-market-strategy-research.md, YC-FIRST-CUSTOMERS-RESEARCH.md
updated: 2026-04-04
---

# Business Model and Go-to-Market Strategy

Newton-Metre operates a 3-product flywheel targeting Indian manufacturing companies with Rs 50Cr+ procurement spend. The competitive advantage: nobody else combines should-cost + similarity search + institutional memory + AI procurement worker from 2D drawings.

## The 3-Product Flywheel

| Product | Role | What It Does |
|---------|------|-------------|
| **Should-cost estimation** | Door-opener | Upload a drawing, get a line-by-line cost breakdown in 30 seconds. +/-5-10% accuracy for mechanical, sheet metal, PCB, cable. The demo moment. |
| **Similarity search** | Platform foundation | Turns drawing history into a searchable asset. Serves 7 departments. Creates data moat -- once 50K drawings indexed with PO history, nobody switches. |
| **AI Procurement Worker** | Cash cow | AI WORKER (not copilot) handles RFQ, quote comparison, negotiation. Class C items (60-70% of POs) autonomously. 2-3% savings on Rs 50Cr spend = Rs 1-1.5 Cr/year. |

**The compounding loop**: Should-cost gets them in. Similarity makes them stay and spreads across departments. AI Worker generates recurring revenue. More data means better search, better negotiations, more savings.

## The 70/30 Insight

70% of procurement spend is off-the-shelf MPN-based items (connectors, fasteners, bearings) where similarity search + negotiation intelligence matters most. Only 30% is manufactured-to-drawing parts where should-cost shines. The platform must serve both.

## Competitive Landscape

| Competitor | What They Do | Gap |
|------------|-------------|-----|
| **CADDi** ($1.4B) | Similarity search only. 28 patents, Kaggle Grandmasters. Proprietary deep learning on millions of Japanese drawings. Expanding to US. | No should-cost, no procurement worker |
| **aPriori** | Physics-based simulation, 440+ process models. Gold standard. Charges $150K+/year. | Requires 3D CAD only. Cannot process 2D drawings. No similarity. |
| **IndustrialMind.ai** | Same problem space. Ex-Tesla founders. Deploying with Siemens, tesa. $1.2M pre-seed. | Likely wrapping APIs (same as us at $1.2M). No similarity, no procurement. |
| **Pactum AI** | AI negotiation for enterprise. Walmart case: 2,000+ suppliers, 3% savings, 35 days payment term extension. | No should-cost, no drawing analysis |
| **Paperless Parts** | Quoting platform with geometry analysis. | Not ML-first, US-focused |

**Newton-Metre's position**: The only platform combining all three from 2D drawings, built for Indian manufacturing economics (INR pricing, BIS standards, Indian process rates).

## Pricing Evolution

| Phase | Model | Price Range |
|-------|-------|-------------|
| **Now** | Free / per-estimate | Free tier + Rs 99-199 per estimate. Build trust. |
| **10 customers** | Volume packs | Rs 300-500/estimate or Rs 5K/month pack. Prove willingness to pay. |
| **50 customers** | SaaS tiers | Rs 15K-2L/month. Recurring revenue. |
| **Enterprise** | On-prem + % of savings | Maximum value capture. Defense clients require on-prem. |

### ChatGPT-Style Tiers

| Tier | Target | Features |
|------|--------|----------|
| **Free** | Individual engineers | 5 estimates/month, basic similarity |
| **Pro** | Cost engineers, procurement | Unlimited estimates, full similarity, chat AI |
| **Max** | Department teams | Multi-user, API access, advanced analytics |
| **Enterprise** | Large manufacturers | On-prem, custom models, dedicated support, SSO |

**Strategy**: Market enterprise, sell individuals. All copy says enterprise capabilities. Individuals adopt first (bottom-up), enterprise follows when 5+ people in the same company are using it.

## Target Market

**Primary verticals**: Defense, Aerospace, Automobile

**Target company profile**:
- Rs 50Cr+ annual procurement spend
- 50K+ drawing history (creates switching cost)
- Multiple departments (procurement, design, QA, sales) that benefit from similarity search

**ROI calculation**: 2-3% savings on Rs 50Cr procurement spend = Rs 1-1.5 Cr/year. At Rs 24L/year subscription, that is a 43x ROI.

**Market sizing**:
- Indian defense production: Rs 1,26,887 Cr in FY2024 (USD ~$15.2B)
- Indian auto components: Rs 6,73,000 Cr in FY2025 (USD ~$78.7B)
- Company brain market globally: $7.66B projected to $51.36B by 2030 (47% CAGR)
- Drawing similarity search TAM: $2-5B globally

## First Customer Strategy

Based on YC research -- patterns from Stripe, Airbnb, DoorDash, Brex, Vanta:

### The Trust Circles Model

First B2B customers come from concentric circles of decreasing trust:

1. **Circle 1-2**: Friends, family, former colleagues who fit ICP. 7 years in defense manufacturing = personal knowledge of procurement people.
2. **Circle 3-4**: Industry contacts, LinkedIn connections, YC batch network.
3. **Circle 5-7**: Investor intros, community engagement, content marketing.
4. **Circle 8**: Cold outbound (last resort pre-PMF).

### Specific Tactics

1. **The DoorDash test**: Simple landing page. "Upload your drawing, get a should-cost breakdown." WhatsApp number. Share in 3 manufacturing WhatsApp groups.
2. **The Collison Installation**: When someone shows interest, say "Send me a drawing right now, I'll run it through and show you the breakdown on a call." Do it live.
3. **The Zapier forum tactic**: Search LinkedIn, IndiaMart forums for people complaining about supplier pricing or cost estimation. Respond with value.
4. **The consulting bridge**: 5 free should-cost analyses for procurement teams. Show them the line-by-line breakdown. Then ask: "Would you pay for this if it was self-serve?"
5. **LOIs for YC**: 3-5 signed letters of intent from procurement managers. Even without revenue, this is valid traction.

### Target Numbers

- **Pre-YC application**: 3-10 users who have used the tool on real parts
- **At YC acceptance**: Evidence that procurement teams find the breakdown valuable enough to change negotiation behavior
- **By Demo Day**: 10-50 paying customers or strong LOI pipeline

## Technology Moat

The moat is NOT the AI (80-90% of YC AI companies use foundation model APIs). The moat is:

1. **Domain knowledge**: 7 years of defense manufacturing experience encoded into physics models
2. **Indian economics**: INR pricing, BIS standards, Indian process rates for 15 cities, power costs for 13 states
3. **Physics engine**: 18 processes with real Sandvik/Kennametal cutting data. No open-source alternative exists.
4. **Data accumulation**: Every estimate-vs-actual pair trains the ML correction layer. First mover with Indian manufacturing data wins.
5. **3-product lock-in**: Once similarity search indexes 50K drawings with PO history, switching cost is extreme.

### Wrapper vs Own Model

API-wrapping is the correct strategy now. Fine-tune later:
- Qwen2.5-VL-7B for extraction when 1,000+ drawings accumulated ($6-16 LoRA fine-tune)
- Self-hosted on A6000/RTX4090 breaks even at 50-100 active users
- Defense on-prem: ship GPU box ($1,800-4,500), air-gapped, zero internet
- Total fine-tuning budget: $50-80 over 6 months

**Pattern from YC successes**: Thin wrappers die. Thick application layers (domain data + workflow + integration) thrive. Harvey AI ($715M), Cursor ($2.5B+), and Perplexity ($9B) all started as API wrappers with deep domain value.

# Company-Wide Similarity Search: Cross-Department Use Cases, Implementation & GTM

*Research date: 2026-04-04 | Sources: 4 parallel research agents, 22+ sources | Confidence: High*

---

## Executive Summary

Similarity search is not a single-department feature. It is the **foundation of a company-wide knowledge platform** that serves 9 departments in a manufacturing company. Design engineering uses it for part reuse (saving $15,000 per avoided new part). Procurement uses it for vendor rationalization and negotiation intelligence (8-12% savings). QA uses it to prevent repeat failures (25-30% of quality issues are repeats). Sales uses it for instant quoting (closing 15-20% more deals). Logistics, import/export, and marketing all derive direct value from the same indexed drawing/document corpus.

**The market opportunity:** $7.66B in 2024 → $51.36B by 2030 (47% CAGR). CADDi proved the category at $1.4B valuation but does NOT do should-cost. PLMs charge $1,200-2,500/user/year but only search by metadata, not visual similarity. Newton-Metre's combination of should-cost + similarity + institutional memory from 2D drawings is genuinely uncontested.

**Recommended GTM:** Land with procurement (immediate ROI, measurable savings), expand to design engineering (month 3-6), then QA and leadership (month 6-12).

---

## 1. Design Engineering — Part Reuse & Standardization

### The Problem

- Engineers spend **6 hours on average** searching for every new part entered into a data management system
- **70-80% of new designs are variants** of existing parts (Boothroyd/DFMA, PTC research)
- **60% of part numbers** in a typical manufacturing database are duplicates or obsolete (Deloitte)
- **At least 60% of information critical to a designer's task is not accessible** — so designers simply redesign from scratch

### The Cost of a New Part

| Cost Element | Amount |
|-------------|--------|
| NPV of introducing one new part | ~$15,000 (PTC research) |
| Engineering design/documentation | 46% of that cost |
| Tooling, inventory, supply chain setup | Remaining 54% |
| Annual carrying cost per redundant part | $4,500-$7,500/year |
| Each defense qualification test | $10,000-$50,000+ |

**Real case:** A global airplane manufacturer standardized brackets, eliminated **850 part numbers**, saved **$1.42M** on brackets alone. Lifetime savings from one year of reuse: **$55M over 23 years**.

### Use Cases for Newton-Metre

| Use Case | How It Works | Value |
|----------|-------------|-------|
| **"Does this already exist?"** | Designer uploads sketch → similarity search finds existing parts with matching geometry | Avoids $15K new part introduction |
| **Standard part substitution** | Find company-approved standard parts that can replace custom designs | Reduce unique part count 20-40% |
| **Cross-project reuse** | Search across all programs (Tejas, LCA, naval projects) for reusable components | Critical in Indian defense where projects are siloed |
| **BOM optimization** | Find common components across product lines → reduce unique tooling, inventory, qualification | Each qualification test avoided saves $10-50K |
| **Design variant tracking** | "Show me all versions of this bracket ever designed" → pick the best, retire the rest | Prevent part proliferation |

### Indian Context

- **97% of Indian MSMEs are micro-enterprises** without PLM systems
- PDF remains the dominant format (60-70% of procurement drawings)
- DRDO/HAL follow COTS standards but still suffer from project-siloed design
- **No tool in the Indian market** addresses this for companies without 3D CAD or PLM

### What CADDi Does ($1.4B)

Upload any drawing (including 30-year-old scans) → OCR + symbol detection → geometric feature extraction via proprietary CNN → vector storage → nearest-neighbor search linked to procurement history. Results: **search reduced from hours to seconds, 1.5-2.1x faster quotations**. Dairy Conveyor Corporation recovered **600 hours/year**. CADDi has **28 patents** on shape-fingerprinting.

**CADDi does NOT do should-cost.** Newton-Metre's should-cost + similarity + memory is differentiated.

---

## 2. Procurement — Negotiation Intelligence & Spend Analytics

### The 70/30 Split (Critical Insight)

- **70% of procurement spend = off-the-shelf / MPN-based items** (connectors, fasteners, bearings, ICs)
- **30% of procurement spend = manufactured parts** (to 2D drawing)
- For MPN items: similarity search finds alternate part numbers, builds supplier matrix
- For manufactured parts: should-cost from drawings + negotiation intelligence

### Use Cases

| Use Case | How It Works | Value |
|----------|-------------|-------|
| **Vendor rationalization** | "We buy 47 variants of M8 fasteners from 12 vendors → consolidate to 3" | 8-12% savings (Deloitte benchmark) |
| **Spend classification** | Cluster purchases by actual part characteristics, not text descriptions | SAP Ariba/Coupa struggle with mfg-specific items |
| **Make vs buy** | "We already make 3 similar parts on our CNC → manufacture in-house at ₹180 vs ₹340 vendor quote" | 20-40% savings on applicable parts |
| **Demand aggregation** | Plant A buys 500 bushings, Plant B buys 300 similar from different vendor → consolidated order | 10-25% volume savings (CAPS Research) |
| **Alternate MPN discovery** | Find equivalent parts from different suppliers with similar specs | Break single-source dependency |
| **Negotiation intelligence** | AI builds supplier matrix: qty tiers, volume history, previous discount patterns, exact % targets | 2-3% additional savings at scale = crores |

### Competitive Landscape

- SAP Ariba/Coupa use ML-based spend classification but rely on text descriptions, not drawings
- Neither provides should-cost baseline or visual similarity
- Both are $100K+/year enterprise tools
- **Newton-Metre's opening:** manufacturing-native spend intelligence at 10-50x lower cost

---

## 3. Quality Assurance — Institutional Memory for Defects

### The Problem

- QA engineers spend **30-40% of time** on document retrieval (McKinsey, 2023)
- **25-30% of quality issues in Indian auto manufacturing are repeat failures** (McKinsey)
- Cost of quality = **15-20% of revenue** for average manufacturer
- Supplier quality history is fragmented across inspection reports, SCAR files, email threads

### Use Cases

| Use Case | How It Works | Value |
|----------|-------------|-------|
| **NCR similarity search** | New defect appears → find every past NCR for similar parts | Catch repeat failures before they compound |
| **Supplier quality history** | "Has this vendor failed on similar tolerance requirements before?" | Block problematic vendors proactively |
| **FAI reference** | New similar part arrives → find FAI plans from similar past parts | 35% reduction in first-pass FAI rejection (Boeing data) |
| **Compliance doc retrieval** | Match by material + process + tolerance class → surface relevant AS9100/NADCAP/DGQA certs | 2-day manual search → seconds |
| **Root cause analysis** | Connect failure modes across product lines by similarity (geometry, material, process) | Cracked gear housing → same heat treatment issue 2 years ago |
| **Inspection history** | "What inspection parameters did we use for similar parts?" | Consistent quality across programs |

### Indian Context

- DGQA (Directorate General of Quality Assurance) governs Indian defense quality
- Indian Tier-1 aerospace suppliers (Dynamatic, Aequs) doing FAI for Boeing/Airbus
- AS9100, ISO 9001, NADCAP certifications tied to specific processes and materials

---

## 4. Sales — Instant Quoting & Reference Parts

### The Problem

- Indian SME manufacturers lose **15-20% of quote opportunities** due to slow response times (CII data)
- Sales engineers get verbal requirements ("we need a flange, about 200mm, stainless") and can't match to capabilities
- Win/loss data on similar RFQs is trapped in email

### Use Cases

| Use Case | How It Works | Value |
|----------|-------------|-------|
| **Quick quoting** | Customer asks "can you make this?" → similarity search finds 5 most similar historical parts → ballpark in minutes | Close 15-20% more deals from faster response |
| **Verbal-to-part matching** | "200mm OD flange, SS, hydraulic system" → search by material + dimension + application | Bridge conversation → quotation gap |
| **Cross-selling** | "Customers who bought turned shafts also ordered matching gears and housings" | Bundle proposals, increase order value |
| **Win/loss on similar RFQs** | "We lost a similar RFQ in 2024 because of surface treatment capability, but we've since added NADCAP hard chrome" | Actionable intelligence for next bid |
| **Reference parts** | Show customer physical examples of similar past work during plant visits | Build confidence instantly |

---

## 5. Marketing — Capability Proof from Data

### Use Cases

| Use Case | How It Works | Value |
|----------|-------------|-------|
| **Data-backed capability statements** | "We have manufactured 340+ turned aerospace-grade titanium components with tolerances under 0.02mm" | Strongest possible social proof — specific, verifiable |
| **Case study generation** | Query "our 10 most complex defense machined components" → get drawings, costs, process details | Raw material for proposals without bothering engineering |
| **Proposal annexures** | "Find all projects matching: aluminum alloy, 5-axis milling, NADCAP certified, defense end-use" | Indian defense RFPs require detailed capability statements |
| **Technical brochure generation** | Auto-generate part family catalogs from indexed drawings | Always up-to-date with latest capabilities |

---

## 6. Logistics & Supply Chain — Inventory & Lead Time Intelligence

### Use Cases

| Use Case | How It Works | Value |
|----------|-------------|-------|
| **Inventory deduplication** | Visual similarity catches what text-based ERP search misses | 15-25% redundant inventory typical. Tata Motors supplier audit: ~18% duplicate SKUs = ₹12Cr locked working capital |
| **Alternative supplier discovery** | "Who else made a similar turned aluminum bush?" from 10,000+ historical POs | Critical in Indian defense where single-source = 6-18 month delays |
| **Lead time estimation** | Match new part against similar past deliveries → realistic lead time prediction | Reduce stockouts by 35-50% (McKinsey) |
| **Warehouse classification** | Group similar parts for shared storage zones, handling, packaging specs | Especially important for defense controlled items |
| **Demand forecasting** | Historical patterns from similar parts across seasons/programs | Reduce overstock and stockout |

---

## 7. Import/Export — HS Codes, Compliance & Duty Optimization

### The Problem (Critical for Indian Defense/Aerospace)

- India's customs tariff has **11,000+ 8-digit HS codes** — misclassification causes 5-15% overpayment
- ICEGATE rejects ~8% of entries for classification errors
- Indian manufacturers utilize only **25-30% of available FTA benefits** (CII estimate) — leaving crores on the table
- India's SCOMET list governs defense exports — accidental violations carry serious penalties
- Indian defense exports: ₹21,083 Cr in FY24, up 30% YoY

### Use Cases

| Use Case | How It Works | Value |
|----------|-------------|-------|
| **HS code classification** | Upload drawing → find 5 most similar past imports → surface their HS codes | Eliminate ~8% classification error rate |
| **Export control (SCOMET/ITAR/EAR)** | Match against tagged database of previously classified items | Prevent accidental violations as defense exports grow |
| **Duty optimization** | "We imported a similar SS304 flange from Japan at 0% under IJCEPA — route through same FTA" | Capture the 70-75% of FTA benefits currently left unused |
| **Customs doc reuse** | BOEs, packing lists, CoO for similar past shipments become templates | Reduce clearance time from 3-5 days to 1-2 days |
| **License requirement matching** | "This part has similar specs to one that required an export license last year" | Proactive compliance |

---

## 8. Finance — Spend Visibility & Cost Intelligence

### The Problem

- CFOs and finance teams in manufacturing companies have **zero visibility** into spend by part family, material type, or process category
- ERP systems categorize by GL code ("Direct Materials"), not by engineering characteristics ("turned aluminum parts under 50mm")
- Budget vs. actual analysis is done at department level, never at part-family level
- Cost trends over time are invisible — "are we paying more for SS304 this year vs. last year?" requires manual PO archaeology

### Use Cases

| Use Case | How It Works | Value |
|----------|-------------|-------|
| **Spend analysis by part family** | Similarity search clusters all purchases by actual part characteristics → spend by material, process, complexity | "We spent ₹3.2 Cr on turned parts last year" — previously unknowable |
| **Budget vs. actual by category** | Should-cost baseline vs. actual PO prices, aggregated by part family | Identify which categories are overspending vs. baseline |
| **Cost trend analysis** | Track price movements per material/process/supplier over time | "SS304 parts up 12% this quarter — is it material cost or supplier markup?" |
| **Supplier spend concentration** | Map total business value per supplier across all part families | "Vendor X has ₹4.5 Cr of our business — we should be getting volume discounts" |
| **Working capital optimization** | Identify duplicate inventory, slow-moving stock by similarity | 15-25% redundant inventory typical = ₹crores in locked capital |
| **Audit-ready cost justification** | Every estimate has a line-by-line should-cost trail | "Here's why we approved this PO at ₹48,000 — the should-cost was ₹45,200" |

### Indian Context

- Indian manufacturers (especially MSMEs) often run on Tally or basic ERPs with no spend analytics
- CFOs rely on monthly MIS reports built manually in Excel — 2-3 week lag
- Defense procurement requires detailed cost justification for every PO above threshold
- GST reconciliation benefits from better part classification and supplier mapping

---

## 9. Supply Planning — Demand Forecasting & Inventory Optimization

### The Opportunity

Supply planners sit on years of PO history but use it only for backward-looking reports. With TimesFM 2.5 (Google's 200M-parameter time series foundation model), that same data becomes **forward-looking intelligence** — demand forecasts, price trend predictions, lead time estimates, and reorder optimization.

### AI Stack for Forecasting

| Model | Params | Role | VRAM |
|-------|--------|------|------|
| **TimesFM 2.5** | 200M | Time series forecasting (demand, prices, lead times) | ~0.5GB (runs on CPU too) |
| **Gemma 4** | TBD | Interprets forecasts in natural language, generates recommendations | TBD |
| **GLM-OCR** | 0.9B | Extracts historical data from scanned POs, invoices | ~1GB |

All three fit on a single A6000 (48GB) or RTX 4090 (24GB) alongside the existing model stack.

### Use Cases

| Use Case | How It Works | Value |
|----------|-------------|-------|
| **Part family demand forecasting** | Feed monthly PO counts per part family into TimesFM → 12-month forecast with confidence intervals | Plan procurement batches, negotiate volume discounts proactively |
| **Defense budget cycle prediction** | TimesFM auto-detects quarterly/annual seasonality from PO data aligned to fiscal years | Anticipate demand spikes before they hit — stock up during slow periods |
| **Lead time prediction** | Historical (order date → delivery date) pairs as time series per supplier | "Your quote says 8 weeks, but 4 similar parts from this vendor averaged 14 weeks" |
| **Material price trend forecasting** | Supplier quote history + commodity indices as covariates (XReg) | "SS304 trending up 8% this quarter — lock in prices now or wait?" |
| **Reorder point optimization** | Demand forecast (TimesFM) + lead time forecast → compute when to trigger POs | Reduce stockouts by 35-50%, reduce overstock by 15-25% |
| **Seasonal procurement planning** | Identify parts with seasonal demand patterns across fiscal years | Pre-negotiate annual contracts during low-demand periods |

### Technical Details

- **TimesFM 2.5**: 200M params, zero-shot (no training needed on your data), 16K context (30+ years of weekly data), Apache 2.0 open source
- **Alternatives considered**: Amazon Chronos-2 (120M, multivariate), Salesforce Moirai 2.0 (14M, multivariate), Nixtla TimeGPT (proprietary — rejected, violates self-hosted strategy)
- **Integration**: `pip install timesfm` → feed PO history arrays → get forecasts + quantiles → Gemma 4 generates natural language insights

### Indian Context

- Defense procurement follows predictable fiscal year cycles (April-March) — TimesFM catches this automatically
- Auto industry has model-year demand patterns (new model launches = component demand spikes)
- MSME supply planners currently use Excel at best — this is a leap from manual to AI-powered

---

## 10. Market Sizing

| Segment | 2024-2025 | 2030 | CAGR |
|---------|-----------|------|------|
| Knowledge management software (global) | $23-35B | $74B | 13.8% |
| Manufacturing intelligence / company brain | $7.66B | $51.36B | 47% |
| India digital transformation | $124B | $267B | ~16% |
| India SaaS market | $20B | $100B | ~38% |

**Two-thirds of Indian manufacturers are actively embracing digital transformation.**

---

## 9. Pricing Benchmarks

| Tier | Price | Examples |
|------|-------|---------|
| PLM enterprise | $1,200-2,500/user/year | Arena, Windchill, Teamcenter |
| aPriori should-cost | $150K+/year | Enterprise only, 3D required |
| CADDi Drawer | ~$50K-200K/year | Custom per volume |
| Manufacturing SaaS (India) | $200-400/user/month | Job shop management |
| **Newton-Metre target** | **$99-299/user/month** or per-estimate | **Undercut PLMs 5-10x, aPriori 10-50x** |

---

## 10. Go-to-Market Strategy

### Land: Procurement (Month 0-3)

**Why procurement first:**
1. Procurement holds the budget — they justify tools by savings percentage
2. ROI is immediate and measurable — "saved 12% on this quote" closes in one meeting
3. 90-day payback — industry benchmark for procurement intelligence tools
4. No IT involvement — upload drawing, get cost. No ERP integration for day one

**Entry workflow:** Upload drawing → get should-cost → find similar historical parts → see what you paid before → negotiate with data

### Expand: Design Engineering (Month 3-6)

**Trigger:** Procurement team says "this is great, but our design team keeps creating new parts for things we already make"

**Value:** Part reuse, standardization, avoid $15K per unnecessary new part introduction

### Expand: QA & Leadership (Month 6-12)

**QA trigger:** "Can you also search our NCRs and inspection reports?"
**Leadership trigger:** "I want a dashboard showing total spend by part family"

### Pricing Strategy

| Tier | Target | Price | Features |
|------|--------|-------|----------|
| **Starter** | MSME (< ₹50Cr revenue) | ₹4,999/mo (~$60) | 100 estimates/mo, similarity search, 1 user |
| **Professional** | Mid-size (₹50-500Cr) | ₹19,999/mo (~$240) | Unlimited estimates, 5 users, negotiation intelligence, PO history |
| **Enterprise** | Large (₹500Cr+) | Custom | Unlimited users, on-prem option, API access, custom integrations |

**Key Indian insight:** Indian manufacturers want ROI in 30-60 days, not 12 months. Per-estimate pricing removes commitment barrier.

---

## 11. ROI Model

### For a ₹500 Crore Manufacturer

| Savings Source | Estimated Annual Impact |
|----------------|----------------------|
| Negotiation intelligence (2-3% on 70% off-the-shelf spend) | ₹7-10.5 Cr |
| Should-cost savings (5% on 30% manufactured spend) | ₹7.5 Cr |
| Vendor consolidation (10% on consolidated items) | ₹2-5 Cr |
| Part reuse / avoided new parts (design) | ₹1-3 Cr |
| Inventory deduplication | ₹1-2 Cr |
| Duty optimization (FTA utilization) | ₹0.5-1 Cr |
| Faster quoting (15-20% more deals) | ₹2-5 Cr |
| **Total** | **₹21-32 Cr** |
| **Platform cost** | **₹24-60L/year** |
| **ROI** | **35-133x** |

---

## 12. Implementation Architecture

### Phase 1: Single Search, Multiple Consumers (Month 1-2)

```
                    ┌─────────────┐
                    │  Similarity  │
                    │   Engine     │
                    │  (pgvector)  │
                    └──────┬──────┘
                           │
        ┌──────────┬───────┼────────┬──────────┐
        │          │       │        │          │
   ┌────┴───┐ ┌───┴───┐ ┌─┴──┐ ┌──┴───┐ ┌───┴────┐
   │Design  │ │Procure│ │ QA │ │Sales │ │Import/ │
   │Reuse   │ │ment   │ │    │ │Quick │ │Export  │
   │Search  │ │Intel  │ │NCR │ │Quote │ │HS Code │
   └────────┘ └───────┘ └────┘ └──────┘ └────────┘
```

- One unified embedding index (drawings, BOMs, POs, NCRs, compliance docs)
- Department-specific search modes (different ranking weights)
- Role-based presets: designer (visual-heavy), procurement (material+cost-heavy), QA (process+defect-heavy)

### Phase 2: Department-Specific Agents (Month 3-6)

Each department gets an AI agent that wraps the search with department-specific intelligence:

| Agent | Wraps | Department Logic |
|-------|-------|-----------------|
| Design Reuse Agent | Similarity search | Suggests standard substitutions, tracks part families |
| Procurement Agent | Similarity + cost + negotiation | Supplier matrix, MPN alternates, discount targets |
| QA Agent | Similarity + document search | NCR patterns, FAI references, compliance matching |
| Sales Agent | Similarity + cost | Quick quotes, capability matching, cross-sell |
| Import/Export Agent | Document search + classification | HS codes, SCOMET matching, FTA optimization |

### Phase 3: Cross-Department Intelligence (Month 6-12)

- **Knowledge graph** links: part → material → process → supplier → defect → cost → drawing
- Design decision affects procurement: "If you change this to SS304, procurement has 3 qualified vendors vs 1 for Inconel"
- QA data feeds procurement: "This vendor had 3 NCRs on similar parts — flag before awarding"
- Sales data feeds design: "We keep getting asked for this capability — should we invest in tooling?"

### Data Architecture

```
┌─────────────────────────────────────────────┐
│              Supabase Postgres               │
├──────────┬──────────┬───────────┬───────────┤
│ drawings │ po_hist  │ ncr_docs  │ contracts │
│ (vector) │ (vector) │ (vector)  │ (vector)  │
├──────────┴──────────┴───────────┴───────────┤
│           Unified pgvector Index             │
│        (768-dim, HNSW, RLS per company)      │
├─────────────────────────────────────────────┤
│         BM25 (tsvector) Text Index           │
│    (part descriptions, specs, materials)     │
├─────────────────────────────────────────────┤
│     Knowledge Graph (relational tables)      │
│  part_materials, part_processes, part_costs  │
│  supplier_parts, defect_parts, project_parts │
└─────────────────────────────────────────────┘
```

---

## 13. Competitive Positioning

| Feature | Newton-Metre | CADDi | aPriori | PLMs (PTC/Siemens) | SAP Ariba/Coupa |
|---------|-------------|-------|---------|-------------------|-----------------|
| Should-cost from 2D drawings | **Yes** | No | 3D only | No | No |
| Visual similarity search | **Yes** | Yes (28 patents) | No | Metadata only | No |
| Negotiation intelligence | **Yes** | No | No | No | Limited |
| Institutional memory | **Yes** | Partial | No | Yes (expensive) | No |
| Works with PDFs/scans | **Yes** | Yes | No (needs 3D) | Limited | No |
| Indian manufacturing focus | **Yes** | Japan/US | US/EU | Global | Global |
| Price point | **$60-240/mo** | ~$50-200K/yr | $150K+/yr | $1,200-2,500/user/yr | $100K+/yr |
| On-prem for defense | **Planned** | No | Yes | Yes | No |

---

## 14. Key Statistics Summary

| Statistic | Source |
|-----------|--------|
| 70-80% of new designs are variants of existing parts | Boothroyd/DFMA, PTC |
| 60% of part numbers are duplicates/obsolete | Deloitte |
| $15,000 NPV per new part introduced | PTC |
| 30-40% of QA time spent on document retrieval | McKinsey 2023 |
| 25-30% of quality issues are repeat failures | McKinsey |
| 15-20% of quote opportunities lost to slow response | CII |
| 25-30% of FTA benefits unutilized by Indian manufacturers | CII |
| 15-25% redundant inventory in typical manufacturer | Industry benchmark |
| CADDi: $1.4B valuation, 28 patents, no should-cost | CADDi public info |
| Company brain market: $51.36B by 2030, 47% CAGR | Market research |

---

## 15. Actionable Next Steps

### Immediate (This Sprint)
1. **Build role-based search presets** — designer/procurement/QA weight configurations for existing similarity engine
2. **Add document type support** — extend similarity indexer beyond drawings to NCRs, POs, compliance docs
3. **MPN alternate search** — for 70% off-the-shelf items, similarity by specs not just visual

### Short-term (Month 1-3)
4. **PO history ingestion** — bulk upload PO data, link to part similarity index
5. **Quick quote mode** — sales-facing interface that returns "similar parts + historical costs" in <30 seconds
6. **Supplier matrix builder** — per-vendor: qty tiers, historical discounts, delivery performance

### Medium-term (Month 3-6)
7. **Department-specific agents** — wrap core search with domain logic per department
8. **HS code classifier** — match new imports against similar past BOEs
9. **NCR/defect search** — QA-specific similarity search for quality documents

### Long-term (Month 6-12)
10. **Knowledge graph** — relational links across parts, materials, processes, suppliers, defects
11. **Cross-department intelligence** — design decisions informed by procurement data and vice versa
12. **On-prem deployment** — for Indian defense customers (DRDO, HAL, BDL ecosystem)

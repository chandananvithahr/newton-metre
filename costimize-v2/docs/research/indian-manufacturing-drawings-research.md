# Indian Manufacturing & Engineering Drawings Landscape

> Research document for Costimize -- AI-powered procurement negotiation intelligence tool.
> Last updated: March 2026

---

## Table of Contents

1. [Indian Manufacturing Landscape](#1-indian-manufacturing-landscape)
2. [How Drawings Are Exchanged in India](#2-how-drawings-are-exchanged-in-india)
3. [Drawing Standards Used in India](#3-drawing-standards-used-in-india)
4. [Common Part Types & Manufacturing Processes](#4-common-part-types--manufacturing-processes)
5. [Procurement Workflow in Indian Manufacturing](#5-procurement-workflow-in-indian-manufacturing)
6. [Digital Adoption & Technology Gaps](#6-digital-adoption--technology-gaps)
7. [Pricing & Cost Factors Unique to India](#7-pricing--cost-factors-unique-to-india)
8. [Market Opportunity](#8-market-opportunity)
9. [Implications for Costimize](#9-implications-for-costimize)
10. [Sources](#10-sources)

---

## 1. Indian Manufacturing Landscape

### Scale of the Sector

India's manufacturing sector is valued at **USD 1.63 trillion (2025)**, projected to reach **USD 2.47 trillion by 2031** at a 7.26% CAGR. Manufacturing contributes approximately **17% of GDP** and is a central pillar of the government's economic strategy.

The MSME (Micro, Small, and Medium Enterprises) sector is the backbone:

| Metric | Value | Source |
|--------|-------|--------|
| Registered MSMEs (Udyam portal) | **7.16 crore** (~71.6 million) as of Nov 2025 | PIB / Udyam Portal |
| Manufacturing MSMEs specifically | **11.75 lakh** (~1.17 million) registered in manufacturing category | MSME Annual Report 2024-25 |
| MSME contribution to GDP | **30.1%** | PIB (Union MSME Minister) |
| MSME share of manufacturing output | **35.4%** | PIB |
| MSME share of exports | **45.73%** | PIB |
| Employment in MSMEs | **31.39 crore** (~314 million) | Udyam Portal |

**Enterprise size distribution:** The overwhelming majority are micro-enterprises. Estimates place 95-97% of MSMEs in the micro category (investment up to Rs 1 crore, turnover up to Rs 5 crore). These are small job shops with 5-50 employees, basic machinery, and minimal digital infrastructure.

### Key Sectors

- **Automotive:** India is the world's 3rd largest automobile market. Chennai ("Detroit of Asia"), Pune, Gurgaon-Manesar, and Sanand are major hubs. Haryana's auto belt produced 2.8 million cars in FY 2025.
- **Defense & Aerospace:** Defence production reached Rs 1.27 lakh crore in FY 2024-25. Defence corridors established in Uttar Pradesh (Lucknow-Kanpur-Agra-Aligarh-Chitrakoot-Jhansi) and Tamil Nadu (Chennai-Hosur-Salem-Coimbatore-Tiruchirappalli). Karnataka is emerging as a deep-tech aerospace hub.
- **Electronics:** Electronics manufacturing jumped 146% from Rs 2.13 lakh crore (FY21) to Rs 5.25 lakh crore (FY25). Mobile exports surged 775%. Chennai-Bengaluru corridor is the largest electronics manufacturing zone. Tamil Nadu attracted USD 6.2 billion in electronics FDI in FY 2025.
- **Electrical Equipment & Cable:** India is a major cable and wire manufacturer, with companies like Havells, Polycab, and Finolex headquartered in Maharashtra and Gujarat.

### Government Initiatives

**Make in India (launched 2014):**
- Targeted 25% manufacturing GDP share (currently ~17%)
- Simplified FDI norms, single-window clearances
- Defence indigenization mandate (75% self-reliance target)

**Production Linked Incentive (PLI) Schemes:**
- 14 sectors covered with Rs 1.97 lakh crore outlay
- Actual investment realized: **Rs 2.02 lakh crore** by September 2025
- Production/sales: over **Rs 18.7 lakh crore** incremental
- Employment generated: **12.6 lakh** (direct + indirect)
- 806 approved applications across sectors

**Other initiatives:**
- Digital MSME Scheme (cloud/ERP adoption subsidies)
- Government e-Marketplace (GeM) -- 11.25 lakh MSE sellers, Rs 7.44 lakh crore cumulative orders
- SAMARTH Udyog (Industry 4.0 for MSMEs)
- PM MITRA mega textile parks

### Key Manufacturing Hubs

| Region | Specialization | Key Cities |
|--------|---------------|------------|
| **Maharashtra** | Auto, engineering, PCB, chemicals | Pune, Mumbai, Nashik, Aurangabad |
| **Tamil Nadu** | Auto, electronics, defence, textiles | Chennai, Coimbatore, Hosur, Tiruchirappalli |
| **Karnataka** | Aerospace, IT hardware, precision engineering | Bengaluru, Mysuru |
| **Gujarat** | Chemicals, pharma, auto, semiconductors | Ahmedabad, Sanand, Dholera |
| **Haryana / NCR** | Auto, electrical, consumer goods | Gurgaon, Manesar, Faridabad, Noida |
| **Uttar Pradesh** | Defence corridor, electronics, leather | Lucknow, Kanpur, Noida, Greater Noida |
| **Rajasthan** | Gems, textiles, engineering | Jaipur, Bhiwadi |
| **Telangana** | Pharma, defence, electronics | Hyderabad |
| **Punjab** | Machine tools, auto components, hand tools | Ludhiana, Jalandhar |

---

## 2. How Drawings Are Exchanged in India

### Format Distribution (Estimated)

Based on industry observation and practitioner interviews:

| Format | Share | Context |
|--------|-------|---------|
| **PDF (native/exported)** | 35-40% | Generated from CAD by OEMs, Tier-1 suppliers with design capability |
| **PDF (scanned)** | 25-30% | Older drawings, prints from government/defence organizations, legacy archives |
| **DXF/DWG (CAD files)** | 10-15% | Shared between companies with CAD capability, mostly large enterprises |
| **WhatsApp photos** | 10-15% | Job shop to job shop, urgent quotes, informal exchanges |
| **STEP/IGES (3D)** | 3-5% | Aerospace, automotive Tier-1, companies using 3D CAD |
| **Physical paper prints** | 5-10% | Still common in government tenders, older shops, defence (controlled docs) |

### The WhatsApp Reality

WhatsApp is the de facto business communication platform in Indian manufacturing:

- India has **390 million** WhatsApp users, the world's largest market
- **80% of small businesses** in India use WhatsApp for business communication
- India has **15 million active WhatsApp Business users**, the highest globally
- For manufacturing MSMEs, the typical flow is:
  1. Buyer photographs a drawing or part sample
  2. Sends via WhatsApp with a voice note: "Yeh part ka rate batao, 500 quantity" ("Tell me the rate for this part, 500 quantity")
  3. Supplier estimates from the photo (often just visually)
  4. Quote sent back as a WhatsApp message or voice note
  5. Formal PO may or may not follow via email

**Key insight for Costimize:** The tool MUST handle low-quality images (phone photos of drawings, WhatsApp-compressed JPEGs) -- not just clean PDFs. This is how 10-15% of drawings arrive, and it represents the most underserved segment.

### Email + PDF for Formal Quotes

For formal RFQs (Request for Quotation):
- Engineering drawing attached as PDF (native or scanned)
- Bill of Materials (BOM) as Excel or PDF
- Specifications and quality requirements as separate documents
- Quote response expected in 3-7 days for standard parts, 1-2 weeks for complex assemblies

### Procurement Teams Do NOT Have CAD

This is a critical insight:
- Procurement professionals use Excel, email, and ERP (if available)
- They receive drawings as PDFs or images -- they cannot open DXF/DWG natively
- They cannot measure dimensions from CAD files
- Their cost estimation is done by: (a) forwarding to a technical person, (b) comparing with historical quotes, or (c) gut feeling based on experience
- **This is exactly the gap Costimize fills** -- giving procurement teams cost visibility without needing CAD software or manufacturing expertise

---

## 3. Drawing Standards Used in India

### Bureau of Indian Standards (BIS) Framework

India's engineering drawing standards are governed by BIS and are closely aligned with ISO:

| Standard | Coverage | ISO Equivalent |
|----------|----------|---------------|
| **IS 10714** (Parts 1-30) | Technical drawings -- lines, lettering, views | ISO 128 |
| **IS 11669:1986** | General principles of dimensioning | ISO 129 |
| **IS 15021** (Parts 1-4) | Projection methods | ISO 5456 |
| **SP 46:2003** | Engineering Drawing Practice for Schools and Colleges (comprehensive reference) | Compilation |
| **IS 2102** | Tolerances -- general tolerances for linear and angular dimensions | ISO 2768 |
| **IS 8000** | Geometrical tolerancing (GD&T) | ISO 1101 |

### First Angle vs Third Angle Projection

**India uses First Angle Projection** (as per IS 15021 and BIS practice), which is the same as ISO/European convention.

- The projection symbol (truncated cone) appears in the title block
- This is different from the US (ASME Y14.5) which uses Third Angle Projection
- **Practical impact:** Many Indian shops also work with US/ASME drawings (for export work), so both conventions are encountered
- Older shops and government organizations strictly follow First Angle; newer companies working with global OEMs may use either

### N.D. Bhatt -- The Standard Textbook

"Engineering Drawing" by N.D. Bhatt (published by Charotar Publishing House) is THE canonical textbook used across virtually all Indian engineering colleges. Key facts:

- First published in 1950, now in its 55th+ edition
- Used in 90%+ of Indian engineering colleges for first-year engineering drawing courses
- Follows BIS standards throughout
- Teaches First Angle Projection as the primary method
- Covers orthographic projection, isometric views, sectional views, dimensioning, tolerancing
- Every Indian mechanical/manufacturing engineer has studied from this book

**Implication for Costimize:** The drawing conventions the tool encounters from Indian suppliers will predominantly follow N.D. Bhatt / BIS conventions -- First Angle Projection, IS dimensioning standards, and metric units.

### Units and Dimensions

- **Standard:** Metric (mm for dimensions, Ra for surface finish)
- **Reality:** Mixed. Older shops and those working with US clients use imperial (inches, thou)
- **Common dimension formats:** mm to two decimal places (e.g., 25.40), tolerances as +/- or limit dimensions
- **Surface finish:** Ra values in micrometers, or the older triangle symbol system (one triangle = rough, three triangles = fine)

### Title Block Information

Indian engineering drawings typically include:
- Part name and drawing number
- Material specification (IS grade or equivalent)
- Scale (1:1, 2:1, etc.)
- Projection method symbol (First or Third Angle)
- Tolerances (general tolerance note, e.g., "Unless otherwise specified: +/- 0.1mm")
- Surface finish (general note or per-surface annotation)
- Heat treatment / surface treatment requirements
- Revision history
- Drawn by / checked by / approved by with dates

---

## 4. Common Part Types & Manufacturing Processes

### CNC Turning & Milling (Job Shops)

The bread and butter of Indian manufacturing MSMEs:

- **CNC Turning:** Shafts, bushings, pins, adapters, flanges. Most common in Ludhiana (Punjab), Rajkot (Gujarat), Coimbatore (TN), Pune (MH)
- **CNC Milling:** Housings, brackets, plates, fixtures. VMC (Vertical Machining Centers) dominate the MSME landscape
- **Conventional Machining:** Still prevalent -- lathes, milling machines, drilling, boring. Many shops have a mix of CNC and conventional

**Typical job shop profile:**
- 5-20 employees
- 3-10 CNC machines + conventional machines
- Works on 10-50 different parts per month
- Typical batch sizes: 50-5,000 pieces
- Revenue: Rs 50 lakh to Rs 10 crore per year

### Sheet Metal Fabrication

- **Processes:** Laser cutting, CNC punching, bending (press brake), welding (MIG/TIG/spot), powder coating
- **Common parts:** Enclosures, panels, brackets, chassis, racks
- **Hubs:** Pune, Delhi NCR, Bengaluru, Chennai
- Growing rapidly due to electrical enclosure demand (solar, EV, industrial automation)

### Casting and Forging

- **Casting types:** Sand casting, investment casting (lost wax), die casting, gravity die casting
- **Casting hubs:** Rajkot (Gujarat) for sand/investment casting, Belgaum (Karnataka), Coimbatore (TN)
- **Forging hubs:** Pune (India's forging capital), Ludhiana
- **India's forging industry:** 2nd largest globally, exports worth USD 2.5+ billion

### PCB Assembly

The Indian PCB market was valued at **USD 7.26 billion in 2025**, projected to reach **USD 25.48 billion by 2034** (14.96% CAGR).

**Key hubs:**
- **Maharashtra (Pune/Mumbai/Nashik):** 29% market share, dominant hub
- **Noida/Greater Noida:** Emerging electronics manufacturing cluster, government ESDM policy support
- **Bengaluru:** Design + manufacturing, companies like Hi-Q Electronics, Circuit Systems India
- **Chennai:** Growing with electronics corridor investment

**Industry structure:**
- Most Indian PCB assembly houses handle 2-8 layer boards
- High-density interconnect (HDI) and flex PCBs still largely imported
- Assembly services: SMT (Surface Mount), THT (Through-Hole), mixed technology
- Key players: Kaynes Technology, SFO Technologies, Dixon Technologies, Syrma SGS

### Cable Harness Assembly

- Labour-intensive assembly process well-suited to India's cost structure
- **Key applications:** Automotive (largest segment), industrial machinery, defence, telecom, consumer electronics
- **Hubs:** Pune, Chennai, Bengaluru, Noida
- Major companies: Motherson Sumi, Delphi (Aptiv), Yazaki India, Leoni

### Surface Treatments

- **Anodizing:** Bengaluru, Pune -- for aluminium parts (Type II and Type III)
- **Electroplating:** Zinc plating, nickel plating, chrome plating -- widespread
- **Powder Coating:** Most common surface finish for sheet metal parts
- **Heat Treatment:** Case hardening, through hardening, nitriding -- specialized shops
- **Passivation:** For stainless steel parts

---

## 5. Procurement Workflow in Indian Manufacturing

### Typical RFQ Process

```
1. Design team creates/receives engineering drawing
2. Procurement team receives drawing + BOM + specifications
3. Procurement identifies potential suppliers (existing vendor list + referrals)
4. RFQ sent via:
   - Email with PDF attachments (formal)
   - WhatsApp with photo/PDF (informal, faster)
   - Phone call followed by email (relationship-driven)
   - E-procurement portal (large companies only)
5. Suppliers receive, review drawing, estimate costs
6. Quotes returned in 3-14 days
7. Procurement compares quotes in Excel spreadsheet
8. Negotiation (phone/meeting/WhatsApp)
9. PO issued (email/ERP)
10. Production + delivery + quality inspection
```

### Quote Turnaround Times

| Complexity | Typical Turnaround |
|-----------|-------------------|
| Simple turned parts | 1-3 days |
| Milled parts with multiple operations | 3-5 days |
| Sheet metal assemblies | 3-7 days |
| Castings/forgings | 5-10 days |
| PCB assemblies | 5-14 days (depends on BOM complexity) |
| Cable harnesses | 3-7 days |
| Complex multi-process parts | 7-14 days |

### Pain Points (The Costimize Opportunity)

1. **No cost visibility:** Procurement teams receive 3-5 quotes with wildly different prices (sometimes 2-3x spread) and have no way to know which is fair
2. **Information asymmetry:** Suppliers know their costs; buyers do not. Suppliers price based on what they think the buyer will pay, not actual cost
3. **Time-consuming:** Each RFQ cycle takes 1-2 weeks. For companies handling 50-200 RFQs/month, this is a major bottleneck
4. **Experience-dependent:** Cost estimation relies on senior procurement staff with decades of experience. When they leave, institutional knowledge is lost
5. **Excel-based costing:** Those who attempt should-costing use massive Excel sheets with hardcoded formulas, no material price updates, and no process time estimation
6. **Supplier discovery:** Finding new/better suppliers is word-of-mouth. No reliable digital marketplace for custom parts in India
7. **Quality of drawings:** Scanned PDFs, low-res images, incomplete dimensions -- yet quotes are expected

### How Costing Is Currently Done

| Method | Who Uses It | Accuracy |
|--------|------------|----------|
| **Gut feeling / experience** | Senior procurement, 15+ years experience | +/- 20-30% |
| **Historical PO comparison** | Mid-level procurement | +/- 15-25% (if similar part exists) |
| **Excel should-cost sheets** | Large companies, automotive OEMs | +/- 10-20% (if maintained) |
| **Supplier quote averaging** | Most common approach | Unreliable (depends on supplier mix) |
| **aPriori / commercial tools** | Only large MNCs (Bosch, Tata, L&T) | +/- 5-10% (but Rs 50L+ annual license) |

**The gap Costimize fills:** Accurate should-costing (within 5-10%) accessible to procurement teams at mid-market companies and MSMEs, without requiring CAD software, manufacturing expertise, or enterprise budgets.

### Role Separation

- **Design Engineers:** Create drawings, specify materials and tolerances. Usually have CAD access. Rarely involved in procurement/costing.
- **Procurement Teams:** Source suppliers, send RFQs, compare quotes, negotiate. Do NOT have CAD access. Need cost visibility the most.
- **Quality Teams:** Inspect received parts. Use drawings for inspection but don't participate in costing.
- **Finance Teams:** Approve POs, track spending. Want cost benchmarks but have no technical capability.

---

## 6. Digital Adoption & Technology Gaps

### CAD Adoption

| Company Size | CAD Adoption | Typical Software |
|-------------|-------------|-----------------|
| **Large enterprises** (Tata, L&T, Mahindra) | 95-100% | SolidWorks, Siemens NX, CATIA, Creo |
| **Mid-market** (Rs 50-500 Cr revenue) | 60-80% | SolidWorks, AutoCAD, Fusion 360 |
| **Small enterprises** (Rs 5-50 Cr) | 30-50% | AutoCAD LT, FreeCAD, DraftSight |
| **Micro enterprises** (< Rs 5 Cr) | 5-15% | Free/pirated AutoCAD, hand drawings |

The India CAD software market generated **USD 617.6 million in 2023**, projected to reach **USD 1,144.9 million by 2030** (9.3% CAGR). Cloud-based CAD holds 62% market share in 2025, driven by lower upfront costs.

**Key barrier:** High licensing costs. SolidWorks at Rs 5-8 lakh/year is unaffordable for micro-enterprises. Free/open-source alternatives lack industry adoption and training ecosystem.

### ERP Penetration

- **67% of MSMEs** demonstrate digital readiness across core and advanced technologies (CMR Study 2025)
- **43% of MSMEs** report proficiency in core digital tools (cloud, ERP, CRM)
- However, "digital readiness" does not mean active ERP usage -- many MSMEs use only basic tools (Tally for accounting, Excel for everything else)
- Estimated actual ERP adoption in manufacturing MSMEs: **15-25%**
- Popular ERP in India: Tally (accounting), Zoho (mid-market), SAP Business One (larger), ERPNext (open-source)
- Government's Digital MSME Scheme provides subsidies for cloud/ERP adoption

### Digital Procurement Tools

- **Adoption rate among MSMEs:** Very low (< 5% for dedicated procurement software)
- **Government e-Marketplace (GeM):** 11.25 lakh MSE sellers, but focused on government procurement
- **Most procurement is still:** Email + Excel + WhatsApp + phone calls
- **Emerging platforms:** AuraVMS (Indian RFQ management), IndiaMart (supplier discovery, not procurement), Moglix (MRO procurement)
- **Enterprise tools:** SAP Ariba, Coupa, Jaggaer used only by large MNCs

**AWS Marketplace India launch (May 2025):** Allows Indian buyers to transact in INR via UPI and net banking, signaling growing enterprise software procurement appetite.

### Language Barriers

- Engineering drawings are almost always in **English** (BIS standards mandate English)
- But business communication happens in regional languages:
  - Hindi (North India, ~40% of interactions)
  - Tamil (Tamil Nadu)
  - Marathi (Maharashtra)
  - Gujarati (Gujarat)
  - Kannada (Karnataka)
  - Telugu (Telangana/AP)
- WhatsApp voice notes in regional languages are extremely common for supplier communication
- **Implication for Costimize:** UI should be English (drawings are English), but consider Hindi/regional language support for broader adoption in future

### Internet & Connectivity

- India has **900+ million internet users** (2025)
- 4G/5G coverage is extensive in urban and semi-urban areas
- Jio effect: data is extremely cheap (Rs 150-300/month for unlimited)
- **However:** Many factory floors have poor indoor connectivity
- Most MSMEs access internet via smartphones, not desktop computers
- **Implication:** Mobile-responsive or mobile-first design is important for future adoption

---

## 7. Pricing & Cost Factors Unique to India

### Labour Rates by Region

| Region | Skilled CNC Operator (Monthly) | Unskilled Labour (Monthly) | Relative Cost |
|--------|-------------------------------|---------------------------|---------------|
| **Tier-1 metros** (Mumbai, Delhi, Bengaluru) | Rs 25,000-40,000 | Rs 12,000-18,000 | Baseline |
| **Tier-2 cities** (Pune, Coimbatore, Ludhiana) | Rs 18,000-30,000 | Rs 10,000-15,000 | 15-30% lower |
| **Tier-3 / rural** (Rajkot, Belgaum, Hosur) | Rs 15,000-25,000 | Rs 8,000-12,000 | 25-40% lower |

**Worker retention:** Tier-2/3 cities show 80%+ retention rates vs 60-70% in metros, an important factor for manufacturing consistency.

India's manufacturing labour costs are approximately **50% of China's** for comparable roles, making it one of the lowest-cost manufacturing destinations globally.

### Machine Hour Rates (2025-2026 Estimates)

| Machine Type | Rate (Rs/hr) | Notes |
|-------------|-------------|-------|
| Conventional Lathe | 200-400 | Widely available |
| CNC Turning (small) | 400-700 | Up to 200mm dia |
| CNC Turning (large) | 700-1,200 | 200mm+ dia |
| VMC (3-axis) | 600-1,000 | Standard work envelope |
| VMC (4/5-axis) | 1,200-2,500 | Limited availability in MSMEs |
| Surface Grinding | 300-600 | |
| Cylindrical Grinding | 400-800 | |
| Wire EDM | 800-1,500 | |
| Laser Cutting | 600-1,200 | Depends on wattage |
| Press Brake (bending) | 300-600 | |

Source: CITD Ludhiana published rates + industry estimates.

### Raw Material Prices (March 2026, INR)

| Material | Price/kg (approx) | Source |
|----------|-------------------|--------|
| Mild Steel (EN8/EN9) | Rs 55-70 | Domestic |
| Stainless Steel (SS304) | Rs 200-250 | Domestic |
| Stainless Steel (SS316) | Rs 300-380 | Domestic |
| Aluminium (6061/6082) | Rs 200-220 | LME linked |
| Brass | Rs 450-550 | Domestic + imported |
| Copper | Rs 750-800 | LME linked |
| Titanium (Grade 2) | Rs 2,500-4,000 | Mostly imported |
| Engineering Plastic (Delrin) | Rs 400-600 | Imported |

Material prices are volatile and linked to LME (London Metal Exchange) and USD/INR exchange rates for non-ferrous metals. Steel is domestically priced, influenced by Tata Steel, JSW, SAIL benchmark pricing.

### Power Costs

- Industrial electricity: **Rs 7-11 per kWh** (varies by state)
- Average for businesses: **Rs 10.49/kWh** (June 2025)
- Cheapest states: Chhattisgarh, Madhya Pradesh, Telangana
- Most expensive: Maharashtra, Karnataka, Tamil Nadu (for industrial tariffs)
- Power costs are 8-15% of total manufacturing cost
- Many shops use diesel generators as backup (Rs 18-22/kWh)

### GST Structure

GST reform (September 2025) simplified slabs to 5%, 18%, and 40%:

| Category | GST Rate |
|----------|----------|
| Raw materials (steel, aluminum) | 18% |
| Manufactured parts (general) | 18% |
| Job work services | 12-18% (depending on nature) |
| Machinery and equipment | 18% |

- Input Tax Credit (ITC) allows offsetting GST paid on inputs against output tax
- For procurement costing, GST is typically excluded from should-cost (compared pre-tax)

### Payment Terms

| Buyer Type | Typical Payment Terms |
|-----------|----------------------|
| **Government / PSU** | 45-90 days (often delayed to 120+ days) |
| **Large OEMs** | 30-60 days |
| **Mid-market companies** | 30-45 days |
| **MSME to MSME** | Advance 30-50%, balance on delivery |
| **Export orders** | LC (Letter of Credit) or advance payment |

Payment delays are a chronic pain point for MSMEs. The MSME Samadhaan portal tracks delayed payments. Cash flow constraints are the #1 reason MSMEs fail.

### Other Cost Factors

- **Material wastage:** 10-20% typical (higher for castings/forgings)
- **Tooling costs:** Often amortized over first batch, then shared
- **Transportation:** 2-5% of part cost for domestic, higher for remote locations
- **Quality rejection rates:** 2-5% for CNC shops, 5-10% for casting/forging
- **Overtime premiums:** 1.5-2x for weekend/holiday work

---

## 8. Market Opportunity

### Market Size

| Metric | Value |
|--------|-------|
| India manufacturing sector | **USD 1.63 trillion** (2025) |
| MSME manufacturing output | **~USD 190 billion** (35.4% of manufacturing) |
| Procurement spend by Indian manufacturers | **Estimated USD 500-700 billion** (materials + components + services) |
| Custom/proprietary parts procurement | **Estimated USD 80-120 billion** annually |
| Global procurement software market | **USD 9.82 billion** (2025), growing to USD 15.75B by 2030 |
| Asia-Pacific procurement software | **11.9% CAGR** through 2030 |

### Growth Projections

- India manufacturing growth: **7.26% CAGR** to 2031
- Private MSMEs: **10.04% CAGR** to 2031
- Micro and small enterprises: **12.94% CAGR** to 2031 (fastest growing)
- Electronics manufacturing: **14.96% CAGR** (PCB market alone)
- India targeting **USD 1 trillion** in manufacturing exports by 2030

### Why No Good Tool Exists for Custom Parts

1. **aPriori is enterprise-only:** Starting at ~USD 60,000/year, requires 3D CAD files (STEP/IGES), not accessible to Indian mid-market. Only used by MNCs (Bosch India, Tata Motors, L&T).

2. **CADDi is Japan/US focused:** CADDi Quote (launched 2025) focuses on Japanese and US markets. Requires 2D drawing upload and AI analysis, but pricing and process databases are not calibrated for Indian manufacturing economics.

3. **IndustrialMind.ai** (Israel): Cloud-based should-cost, focused on Western manufacturing. No India-specific cost models.

4. **Indian market is fragmented:** 70+ million MSMEs, massive regional variation, multiple languages, informal processes. No single tool addresses the full spectrum.

5. **Drawing quality problem:** Most tools assume clean CAD files or high-quality PDFs. Indian reality includes scanned PDFs, WhatsApp photos, and hand-drawn sketches. AI extraction must handle this quality spectrum.

6. **Cost model complexity:** India-specific factors (regional labour rates, power costs by state, domestic vs imported material, GST implications, payment term financing costs) are not modeled by any existing tool.

7. **Pricing sensitivity:** Indian MSMEs will not pay enterprise SaaS pricing. The tool must have a freemium or pay-per-use model that starts at Rs 0 and scales to Rs 5,000-50,000/month.

### Total Addressable Market (TAM) Estimate for Costimize

| Segment | Count | Potential ARPU | Market Size |
|---------|-------|---------------|-------------|
| Large enterprises (procurement teams) | ~5,000 | Rs 5-10 lakh/year | Rs 250-500 Cr |
| Mid-market manufacturers | ~50,000 | Rs 50,000-2 lakh/year | Rs 250-1,000 Cr |
| Small manufacturers / job shops | ~500,000 | Rs 5,000-20,000/year | Rs 250-1,000 Cr |
| **Total TAM** | | | **Rs 750-2,500 Cr** (~USD 90-300M) |

The initial beachhead is mid-market manufacturers (Rs 50-500 Cr revenue) with 5-20 person procurement teams who handle 50-200 RFQs/month and currently have no cost visibility tool.

---

## 9. Implications for Costimize

### Product Decisions Informed by This Research

1. **Input format priority:** PDF first (60-70% of drawings), then images/WhatsApp photos (10-15%), then DXF/DWG (10-15%). The AI vision pipeline must handle scanned/low-quality PDFs as first-class inputs.

2. **Cost model calibration:** Must use India-specific rates (INR), with regional variation by manufacturing hub. The config.py constants are a good start but should eventually be parameterized by region.

3. **Process coverage priority:**
   - Phase 1 (current): CNC turning/milling, PCB assembly, cable assembly
   - Phase 2: Sheet metal fabrication (high demand, clear cost model)
   - Phase 3: Casting/forging estimation (complex but high value)
   - Phase 4: Surface treatments as add-on costs

4. **User persona:** Primary user is a procurement professional who does NOT have CAD software, does NOT have deep manufacturing knowledge, and needs a "upload drawing, get cost breakdown" experience.

5. **Drawing standards:** Expect First Angle Projection (IS/BIS standards), metric dimensions, and N.D. Bhatt conventions. The vision/extraction pipeline should be trained on Indian drawing conventions.

6. **Pricing model:** Must be accessible to MSMEs. Freemium (5-10 free estimates/month) with paid tiers. Pay-per-estimate model also viable. Enterprise pricing for large procurement teams.

7. **Mobile consideration:** Many users will access via mobile (smartphone-first internet usage in India). Streamlit's responsive design helps, but dedicated mobile experience is a future consideration.

8. **Historical PO matching:** The existing PO upload and matching feature is highly aligned with how Indian procurement teams work -- they always compare against past purchases. This is a key differentiator.

9. **WhatsApp integration:** Future feature -- allow users to forward drawings from WhatsApp directly to Costimize (via WhatsApp Business API). This would match the existing workflow of Indian manufacturers.

10. **Language:** Keep UI in English (drawings are English, professional tool). Consider Hindi UI as a future expansion.

---

## 10. Sources

### Government & Official Statistics
- [MSME sector accounts for 30.1% of India's GDP -- PIB](https://www.pib.gov.in/PressReleasePage.aspx?PRID=2142170)
- [Budget 2025-26: Fuelling MSME Expansion -- PIB](https://www.pib.gov.in/PressReleasePage.aspx?PRID=2099687)
- [MSME Annual Report 2024-25 (PDF)](https://msme.gov.in/sites/default/files/MSME-ANNUAL-REPORT-2024-25-ENGLISH.pdf)
- [PLI Scheme: Powering India's Industrial Renaissance -- PIB](https://www.pib.gov.in/PressNoteDetails.aspx?NoteId=155082)
- [PLI Scheme Strengthens India's Manufacturing Capacity -- PIB](https://www.pib.gov.in/PressReleasePage.aspx?PRID=2202979)
- [BIS Presentation on Engineering Drawing Standards (PDF)](https://www.bis.gov.in/wp-content/uploads/2022/04/BISPresentationonEnggDrawing.pdf)
- [IS 10714-30 (2006): Technical drawings](https://law.resource.org/pub/in/bis/S01/is.10714.30.2006.pdf)
- [IS 11669 (1986): General Principles of Dimensioning](https://law.resource.org/pub/in/bis/S01/is.11669.1986.pdf)
- [SP 46 (2003): Engineering Drawing Practice](https://law.resource.org/pub/in/bis/S01/is.sp.46.2003.pdf)

### Market Research & Industry Reports
- [India Manufacturing Market Size & 2031 Growth -- Mordor Intelligence](https://www.mordorintelligence.com/industry-reports/india-manufacturing-sector-market)
- [Manufacturing Industries in India -- IBEF](https://www.ibef.org/industry/manufacturing-sector-india)
- [India Manufacturing Tracker 2026 -- India Briefing](https://www.india-briefing.com/news/india-manufacturing-tracker-2026-43751.html)
- [India CAD Software Market -- PS Market Research](https://www.psmarketresearch.com/market-analysis/india-cad-software-market)
- [India 3D CAD Software Market -- IMARC Group](https://www.imarcgroup.com/india-3d-cad-software-market)
- [Indian PCB Market Size Report 2034 -- IMARC Group](https://www.imarcgroup.com/indian-pcb-market)
- [India PCB Market -- PS Market Research](https://www.psmarketresearch.com/market-analysis/india-printed-circuit-board-market-report)
- [Procurement Software Market Size -- GM Insights](https://www.gminsights.com/industry-analysis/procurement-software-market)
- [Procurement Software Market -- Mordor Intelligence](https://www.mordorintelligence.com/industry-reports/procurement-software-market)

### Digital Adoption & Technology
- [67% of MSMEs demonstrate digital readiness -- CMR Study](https://cmrindia.com/67-of-msmes-demonstrate-digital-readiness-across-core-and-advanced-technologies-finds-cmr-study/)
- [Digital Can Boost MSME Manufacturing -- EY India](https://www.ey.com/en_in/insights/technology/how-can-manufacturing-and-msme-s-grow-faster-with-digital-transformation)
- [India's MSME in 2025: Formalisation and Procurement-Led Scale -- SMEStreet](https://smestreet.in/smestreet-exclusive/indias-msme-in-2025-the-year-of-formalisation-faster-commerce-and-procurement-led-scale-10939771)
- [India's PLI Schemes Bring in US$21 Billion -- India Briefing](https://www.india-briefing.com/news/indias-pli-schemes-bring-in-us21-billion-in-investment-in-2025-38796.html/)

### Manufacturing Hubs & Regional Data
- [Top 7 Emerging Manufacturing Clusters -- Invest India](https://www.investindia.gov.in/team-india-blogs/top-7-emerging-manufacturing-clusters-india)
- [Manufacturing Hubs in India 2025 -- India2West](https://india2west.com/exploring-emerging-manufacturing-hubs-in-india-2025-key-growth-centers-to-watch/)
- [India Manufacturing Regions: What to Source Where -- India2West](https://india2west.com/indian-manufacturing-regions-2025/)
- [India's Defence Breakthrough in 2025 -- DD News](https://ddnews.gov.in/en/indias-defence-breakthrough-in-2025-a-year-of-manufacturing-muscle-and-technological-confidence/)

### Pricing & Cost Data
- [CNC Machining Cost Guide 2026 -- Xavier Parts](https://www.xavier-parts.com/cnc-machining-cost-guide-2026-material-prices-precision-rates-global-hourly-costs/)
- [Machine Hour Rates -- CITD Ludhiana (PDF)](https://www.ctrludhiana.org/wp-content/uploads/2021/07/Machine-Hour-Rates.pdf)
- [Steel Price Today India -- BankBazaar](https://www.bankbazaar.com/commodity-price/steel-price.html)
- [Aluminium/Copper Prices -- OfBusiness](https://www.ofbusiness.com/prices/non-ferrous)
- [India Electricity Prices June 2025 -- GlobalPetrolPrices](https://www.globalpetrolprices.com/India/electricity_prices/)
- [State-wise Power Tariffs in India 2025 -- GreatPelican](https://www.greatpelican.in/resources/blogs/state-wise-power-tariffs-in-india-2025)
- [2025 Manufacturing Cost Breakdown: China vs Thailand vs India -- AMREP](https://www.amrepmexico.com/blog/manufacturing-cost-comparison-china-thailand-india)

### WhatsApp & Communication
- [WhatsApp Statistics 2025 -- Infobip](https://www.infobip.com/blog/whatsapp-statistics)
- [WhatsApp Business Statistics 2025 -- Wapikit](https://www.wapikit.com/blog/global-whatsapp-business-statistics-2025)
- [WhatsApp Business Statistics -- AiSensy](https://m.aisensy.com/blog/whatsapp-statistics-for-businesses/)

### Competitor Analysis
- [aPriori Manufacturing Cost Estimation](https://www.apriori.com/manufacturing-cost-estimation/)
- [CADDi Unveils CADDi Quote -- PR Newswire](https://www.prnewswire.com/news-releases/caddi-unveils-caddi-quote-transforming-manufacturing-procurement-302421329.html)
- [aPriori Vendor Analysis -- Spend Matters](https://spendmatters.com/2025/07/16/apriori-vendor-analysis-cost-and-manufacturing-analytics-solution-overview/)
- [Top PCB Manufacturers in India 2025 -- Karkhana.io](https://karkhana.io/top-pcb-manufacturers-in-india-2025-whos-leading-the-charge-in-electronics-innovation/)

---

*This document informs product decisions for Costimize. Data points are sourced from government reports, industry research firms, and market analysis platforms. Estimates for drawing format distribution and procurement workflow are based on practitioner observation and industry conversations, as no formal survey data exists for these specific metrics.*

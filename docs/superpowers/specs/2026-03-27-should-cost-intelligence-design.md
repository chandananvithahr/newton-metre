# Should-Cost Intelligence Tool — Design Spec

## Overview

A procurement negotiation intelligence tool that gives line-by-line cost breakdowns (±5-10% accuracy) for mechanical parts, PCB assemblies, and cable assemblies. Built as a fresh modular Streamlit app (`costimize-v2/`).

**Users:** Procurement teams negotiating with suppliers for custom/proprietary manufactured parts.

**Core value:** "Here's what this part SHOULD cost, line by line. Now negotiate."

---

## Project Structure

```
costimize-v2/
├── app.py                        # Tab router only (~50 lines)
├── config.py                     # All rates, constants, API keys
├── requirements.txt
├── .env
│
├── ui/
│   ├── mechanical_tab.py         # Mechanical parts UI
│   ├── pcb_tab.py                # PCB assembly UI
│   ├── cable_tab.py              # Cable assembly UI
│   └── components.py             # Shared widgets (cost table, file uploader, confidence badge)
│
├── engines/
│   ├── mechanical/
│   │   ├── cost_engine.py        # Multi-process cost calculator
│   │   ├── process_db.py         # Process definitions, time estimation rules
│   │   └── material_db.py        # Material prices, densities, machinability
│   ├── pcb/
│   │   ├── cost_engine.py        # PCB assembly cost calculator
│   │   ├── bom_parser.py         # CSV/Excel/PDF BOM extraction
│   │   └── fab_cost.py           # Bare board fabrication cost model
│   └── cable/
│       ├── cost_engine.py        # Cable assembly cost calculator
│       └── bom_parser.py         # Cable BOM extraction
│
├── extractors/
│   ├── vision.py                 # AI drawing analysis (OpenAI GPT-4o / Gemini fallback)
│   ├── process_detector.py       # AI identifies manufacturing processes from drawing
│   └── bom_extractor.py          # AI extracts BOM from PDF (for PCB/cable PDFs)
│
├── scrapers/
│   ├── component_scraper.py      # DigiKey/Mouser web scraping for component prices
│   └── material_scraper.py       # Metal raw material price scraping (INR)
│
├── history/
│   ├── po_parser.py              # Parse Excel/PDF purchase orders
│   ├── po_store.py               # Store/retrieve normalized PO data as JSON
│   └── po_matcher.py             # Match current estimate to historical POs
│
└── data/
    ├── materials.json            # Material database (steel, aluminium, brass, copper, SS, titanium)
    ├── processes.json            # Process rates, setup times, power, time estimation rules
    ├── cache/                    # Scraped price cache (24hr TTL)
    └── history/                  # Stored historical PO data (JSON)
```

---

## Part Type 1: Mechanical Parts

### Input
- Upload engineering drawing (PNG/JPG/PDF)
- AI extracts: dimensions, material, tolerances, surface finish
- AI suggests manufacturing processes from drawing features
- User confirms/edits processes via checklist
- User can override any dimension, material, or process
- User enters quantity

### Manufacturing Processes Supported
Turning, Facing, Boring, Milling (face/slot/pocket), Drilling, Reaming, Tapping/Threading, Grinding (cylindrical/surface), Knurling, Broaching, Heat Treatment, Surface Treatment (plating, anodizing, painting)

### Cost Breakdown (line-by-line)

| Line Item | Calculation |
|-----------|-------------|
| Raw Material | weight × ₹/kg + 15% wastage |
| Turning | estimated time × machine rate (₹800/hr) |
| Milling | estimated time × machine rate (₹1000/hr) |
| Drilling | estimated time × machine rate (₹600/hr) |
| Threading | estimated time × machine rate (₹600/hr) |
| Grinding | estimated time × machine rate (₹1200/hr) |
| *(each selected process gets its own line)* | |
| Setup Cost | setup time per process, amortized over quantity |
| Tooling Cost | inserts, drills, taps — estimated per unit |
| Labour | total operator time × ₹250/hr |
| Power | machine kW × hours × ₹8/kWh |
| Overhead | 15% of above |
| Profit Margin | 20% of above |
| **Unit Cost** | **sum of all** |
| **Order Cost** | **unit cost × quantity** |

### Time Estimation Logic
- AI vision gives dimensions → engine calculates material removal volume
- Feed/speed rates per material-process combination → machining time
- Example: Turning ∅60mm to ∅50mm × 100mm in EN8 → calculate MRR → time

### Volume-Based Pricing
- Setup cost amortized over quantity
- Tooling cost based on tool life vs part count
- Material discount tiers for bulk
- Labour efficiency at higher quantities

---

## Part Type 2: PCB Assembly

### Input
- Upload BOM: CSV/Excel (structured) or PDF (AI extracts)
- BOM parser normalizes to: MPN, description, quantity, footprint
- User enters: board size, layer count, surface finish, assembly quantity
- User can override any component price

### BOM Parser
- **CSV/Excel:** Auto-detect columns by header matching (part number, qty, description, value, footprint)
- **PDF:** Send to GPT-4o/Gemini → extract structured BOM as JSON

### Component Price Scraping (DigiKey/Mouser)
- Search by manufacturer part number (MPN)
- Extract: unit price at quantity tiers (1/10/100/1000/5000), stock status
- Pick lowest across distributors at relevant quantity
- Cache 24 hours in `data/cache/`
- Fallback: search by description if MPN not found
- Anti-blocking: random 2-5 sec delays, rotate user agents, respect robots.txt

### Cost Breakdown

| Line Item | Calculation |
|-----------|-------------|
| Components | sum of (component price × qty) from scraped prices |
| Bare Board Fabrication | based on size, layers, qty, finish (rule-based cost model) |
| SMT Assembly | SMD pad count × ₹1.5/pad |
| THT Assembly | through-hole pin count × ₹3/pin |
| Stencil | amortized over quantity |
| Testing | ICT/flying probe per board (₹25) |
| Overhead | 15% |
| Profit | 20% |
| **Unit Cost** | **sum of all** |
| **Order Cost** | **unit cost × quantity** |

---

## Part Type 3: Cable Assembly

### Input
- Upload BOM: CSV/Excel or PDF
- BOM parser extracts: connectors, wire types, lengths, terminals, sleeves, labels
- User enters quantity

### Cost Breakdown

| Line Item | Calculation |
|-----------|-------------|
| Components | connectors, wires, terminals, heat shrink, labels (scraped prices) |
| Labour | cutting, stripping, crimping, assembly, testing — time × ₹200/hr |
| Overhead | 15% |
| Profit | 20% |
| **Unit Cost** | **sum of all** |
| **Order Cost** | **unit cost × quantity** |

### Labour Time Estimation (rule-based)
- Per wire: cut (0.5 min) + strip (0.5 min) + crimp 2 ends (1 min) = 2 min/wire
- Connector insertion: 0.5 min per connector
- Sleeving/heat shrink: 1 min per cable
- Labelling: 0.5 min
- Scales with wire count and connector complexity

---

## Historical PO Comparison (All 3 Tabs)

### Input
- User uploads previous POs: Excel or PDF
- No AI extraction needed — structured column parsing

### Parser
- Reads columns: part description, part number, unit price, quantity, supplier, date
- Normalizes to JSON, stored in `data/history/`

### Matching
- Search by part number first (exact match)
- Fallback: keyword match on part description
- No vector search — simple text matching

### Display (shown alongside every new estimate)

```
┌──────────────────────────────────────────┐
│ HISTORICAL COMPARISON                    │
│                                          │
│ Your should-cost:        ₹2,997/unit    │
│ Last PO (Mar 2025):      ₹3,450/unit    │
│ Difference:              ₹453 (15% over)│
│                                          │
│ Previous supplier: ABC Engg, Pune        │
│ Previous qty: 200 pcs                    │
└──────────────────────────────────────────┘
```

If no match found: "No historical data. Upload previous POs to enable comparison."

---

## Shared Infrastructure

### Dimension Extraction Pipeline (`extractors/`)

**Current (v1 — implemented):**
- `vision.py` — Single-shot GPT-4o/Gemini vision call. Known limitation: LLMs hallucinate dimensions from engineering drawings.
- `process_detector.py` — AI suggestions + rule-based fallback for process detection
- `bom_extractor.py` — sends PDF BOMs to vision AI → structured JSON

**Planned extraction tiers (from research, 2026-03-27):**

| Priority | Input | Method | Accuracy | Effort |
|----------|-------|--------|----------|--------|
| 1 (next sprint) | DXF/DWG file | `ezdxf` direct parsing of DIMENSION entities | 100% | 2-3 days |
| 2 (following sprint) | Image/PDF | PaddleOCR → layout detection → LLM interprets | ~80-94% | 3-4 days |
| 3 (future) | Image/PDF | Fine-tune Florence-2 or YOLOv11-OBB + Donut | 88-97% F1 | Needs 400+ annotated drawings |

**Key research findings:**
- arXiv:2411.03707 — Fine-tuned Florence-2 (0.23B params, 400 drawings) beat GPT-4o by 52% F1, 43% less hallucination
- arXiv:2505.01530 — YOLOv11 + Donut achieved 97.3% F1 on GD&T extraction
- arXiv:2508.12440 — DXF parsing → 200 geometric features → ML model → 3.9% MAPE cost prediction
- DeepLearning.AI course "Document AI: From OCR to Agentic Doc Extraction" (Andrew Ng + Landing AI, 2026) teaches the agentic pipeline approach

**DXF parsing approach (Priority 1):**
- `ezdxf` library parses DIMENSION entities: LINEAR, ALIGNED, ANGULAR, DIAMETER, RADIUS, ORDINATE
- `get_measurement()` returns exact value in WCS units — no OCR, no guessing
- Definition points give exact geometry coordinates
- Accepts DXF upload as primary path; image upload becomes fallback with mandatory user verification

### Scrapers (`scrapers/`)
- `component_scraper.py` — DigiKey + Mouser web scraping, shared by PCB and cable
- `material_scraper.py` — metal prices in INR, ported from current `material_price_fetcher.py`
- Both use 24hr file cache in `data/cache/`

### Config (`config.py`)
Single source of truth for all rates:
- Machine rates per process (₹/hr)
- Labour rates (₹/hr)
- Power rate (₹/kWh)
- Overhead % and Profit %
- PCB assembly rates (per pad, per pin)
- Cable labour rate
- Scraper settings (cache duration, delay range)

### UI (`app.py`)
Three-tab Streamlit app. `app.py` is ~50 lines — just a tab router. Each tab is its own file in `ui/`.

---

## Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| **Frontend + Backend** | Streamlit | Full web app in Python, fast to iterate, deploys anywhere |
| **AI Vision (current)** | OpenAI GPT-4o (primary), Google Gemini (fallback) | Drawing dimension extraction + BOM extraction from PDF |
| **AI Vision (planned)** | ezdxf (DXF parsing), PaddleOCR + LLM agentic pipeline | 100% accuracy for CAD files, ~80-94% for images |
| **Web Scraping** | BeautifulSoup + requests | Component prices (DigiKey/Mouser) + material prices (INR) |
| **Data Parsing** | pandas + openpyxl | BOM files (CSV/Excel), PO files (CSV/Excel) |
| **Data Storage** | JSON files | No database needed for MVP — `data/cache/`, `data/history/` |
| **Testing** | pytest | 35 tests across 7 test files |
| **Language** | Python 3.11+ | |
| **Deployment** | Streamlit Cloud (free) / Railway / Render / any VM | `streamlit run app.py --server.port $PORT` |

**Cost:** Free/minimal — only pay for OpenAI/Gemini API calls per drawing upload. DXF parsing and PaddleOCR are free/open-source.

---

## Out of Scope (Future Sprints)

- Similarity search ("find similar parts")
- RAG / knowledge base
- User accounts / multi-tenant
- Database (PostgreSQL, etc.)
- Cloud deployment (ready to deploy, just not done yet)
- API backend (FastAPI)
- Historical PO AI extraction from unstructured PDFs
- ERP integration
- Fine-tuned Florence-2 / YOLOv11 for drawing extraction (needs 400+ annotated drawings)

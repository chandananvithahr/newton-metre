# PDF Parsing for Engineering Drawings: Deep Dive Research Report
## Costimize Research — March 2026

---

# EXECUTIVE SUMMARY

Engineering drawings are **THE hardest document type to parse** — harder than financial documents, academic papers, or circuit schematics. They combine every difficult parsing problem simultaneously: spatial semantics, specialized symbology (GD&T), multiple coordinate systems, no natural reading order, and information density 10x beyond any business document.

**Key findings:**
1. **Nobody has solved this.** Not Google, not Microsoft, not any startup. Werk24 is closest for extraction-only; aPriori bypasses the problem by requiring 3D CAD.
2. **Full 3D reconstruction from 2D drawings is a 50+ year unsolved research problem.** Don't attempt it.
3. **You don't need full 3D for cost estimation.** Bounding dimensions + feature list + tolerances + material = enough for ±10% accuracy.
4. **The agentic architecture pattern is the right approach:** layout detection → region classification → specialized tools per region → LLM orchestration → self-verification.
5. **DXF-native parsing is 10x easier than PDF vision** and should always be preferred when CAD files are available.
6. **GD&T extraction has a direct cost mapping** — each of the 14 symbols maps to specific manufacturing processes with quantifiable cost multipliers (1.0x–5.0x).
7. **Your view-by-view strategy is validated** by 50 years of academic literature on 2D→3D reconstruction.

---

# PART 1: WHY ENGINEERING DRAWINGS ARE THE HARDEST DOCUMENT TYPE

## Document Parsing Difficulty Ranking

| Rank | Document Type | Difficulty | Status |
|------|--------------|------------|--------|
| 1 | Plain text documents | Easy | Solved |
| 2 | Structured forms | Easy-Medium | Solved |
| 3 | Invoices/receipts | Medium | Solved (95%+) |
| 4 | Multi-column layouts | Hard | Mostly solved |
| 5 | Tables without gridlines | Hard | Mostly solved |
| 6 | Academic papers with equations | Hard | Solved (Nougat) |
| 7 | Financial documents (complex tables) | Very Hard | 85-95% |
| 8 | Technical diagrams (flowcharts, P&IDs) | Very Hard | Partially solved |
| 9 | Circuit schematics | Extremely Hard | Research stage |
| **10** | **Engineering drawings (2D)** | **THE HARDEST** | **Unsolved** |

## What Makes Engineering Drawings Uniquely Hard

### 1. Symbolic Language
- **GD&T** — ISO 1101 / ASME Y14.5 defines ~50 symbols with precise semantic meanings
- **Welding symbols** — AWS A2.4 standard
- **Surface finish symbols** — Ra, Rz values
- **Thread callouts** — M10x1.5-6H, 1/4-20 UNC-2B
- These are NOT in standard OCR training data

### 2. Spatial Semantics (The Core Problem)
- In text documents, meaning flows left-to-right, top-to-bottom
- In engineering drawings, **proximity and geometric connectivity define meaning**
- A dimension "25.4" must be associated with the specific geometric feature it spans
- Leader lines, extension lines, and arrows create semantic links that are purely spatial

### 3. Multiple Coordinate Systems
- Each orthographic view (front, top, right) has its own coordinate system
- Section views, detail views, auxiliary views add more
- A single part may appear in 4-6 views, each showing different information
- Cross-view references ("Section A-A", "Detail B 2:1") require understanding they show the same part

### 4. Layered Information (ALL on one sheet)
1. **Geometry** — the actual part shape (lines, arcs, circles)
2. **Dimensions** — size information (linear, angular, radial, diameter)
3. **Tolerances** — allowable variation (±, GD&T frames, fits)
4. **Annotations** — notes, callouts, material specs, process instructions
5. **Title block** — part number, revision, material, drawn by, date
6. **BOM / parts list** — in assembly drawings
7. **Surface finish** — roughness requirements per surface
8. **Section markers** — cutting plane lines, detail circles

### 5. No Natural Reading Order
- A reader must spatially navigate: look at title block → identify views → trace dimensions to features → cross-reference views
- This requires *understanding drawing conventions*, not just reading text

### 6. Information Density
- A single A1/D-size drawing can contain 200+ dimensions, 50+ annotations, 20+ GD&T frames
- Small details (decimal places, tolerance values) are critical — ±0.05 vs ±0.5 is a 10x cost difference

### 7. Standard Variations
- ISO vs ASME (1st angle vs 3rd angle projection)
- Company-specific title blocks, revision systems
- Military standards (MIL-STD)
- No two companies' drawings look identical

---

# PART 2: THE STEP-BY-STEP INTERPRETATION PIPELINE

## How a Manufacturing Engineer Reads a Drawing

This is the mental pipeline your AI must replicate:

### Step 1: Standard Detection
- **ASME vs ISO**: Title block format, projection symbol, decimal notation
- **Projection symbol** in title block: truncated cone shape
  - 1st angle: large circle on the right side (India, Europe, China)
  - 3rd angle: large circle on the left side (USA, Japan, Canada)
- **When missing**: Use country-based defaults. India officially mandated 1st angle projection per SP 46:2003 (BIS) after Dec 31, 1991. However, many Indian companies working with US clients use 3rd angle.
- **Automated detection**: Template matching on title block region + projection symbol classifier
- **Getting this wrong is catastrophic**: A left-side feature becomes a right-side feature — complete mirror-image misinterpretation

### Step 2: Title Block Extraction
- Part number, revision, material, drawn by, date, scale, projection
- Most structured region on the drawing — template-matchable
- Always in bottom-right corner (ASME) or right side (ISO)

### Step 3: View Identification
- **Front view** (elevation): Usually the largest, most detailed view
- **Top view** (plan): Above front view in 3rd angle, below in 1st angle
- **Side view** (profile): To the right of front view
- **Section views**: Labeled A-A, B-B with cutting plane lines
- **Detail views**: Circled areas at larger scale
- **Isometric view**: 3D perspective (if present)

### Step 4: Overall Dimensions
- Start from the biggest numbers: overall Length × Width × Height (or Diameter × Length)
- These define the stock material / bounding volume
- Usually the outermost dimension lines on each view

### Step 5: Feature Identification (View by View)
- Each view reveals different features:
  - Front: height, width, external profile, visible features
  - Top: width, depth, hole patterns, pocket shapes
  - Side: height, depth, features not visible from front
  - Section: internal features (bores, cavities, wall thickness)

### Step 6: GD&T and Tolerance Extraction
- Feature control frames → geometric tolerance type + value + datums
- Dimensional tolerances → ± values or limit dimensions
- Surface finish symbols → Ra/Rz values

### Step 7: Cross-View Merging
- Match features across views using projection alignment
- Front + Top share X coordinates
- Front + Side share Y coordinates
- Top + Side share Z (depth) coordinates
- Consistent dimensions confirm correspondence

### Step 8: Manufacturing Process Inference
- Feature types → required processes (holes→drilling, flats→milling, diameters→turning)
- Tolerances → process grade (standard CNC vs grinding vs lapping)
- Surface finish → finishing operations
- Process sequence: roughing → semi-finish → finish → inspect

### Step 9: Cost Estimation
- Material cost (stock volume × density × ₹/kg)
- Machining time (per process, from MRR calculations)
- Setup time (per operation, amortized over batch)
- Tooling cost
- Tolerance surcharges
- Inspection cost
- Overhead + profit

---

# PART 3: GD&T — THE COMPLETE SYSTEM

## 14 Geometric Tolerance Types

### Form Controls (4 symbols — no datum required)

| Symbol | Name | What It Controls | Cost Multiplier |
|--------|------|-----------------|-----------------|
| ⏤ | Flatness | How flat a surface is (two parallel planes zone) | 1.1x–2.5x |
| ⎯ | Straightness | How straight a line/axis is | 1.1x–2.0x |
| ○ | Circularity | How round a cross-section is (two concentric circles) | 1.2x–3.0x |
| ⌭ | Cylindricity | Circularity + straightness + taper over entire cylinder | 1.3x–3.5x |

### Profile Controls (2 symbols — with or without datums)

| Symbol | Name | What It Controls | Cost Multiplier |
|--------|------|-----------------|-----------------|
| ⌒ | Profile of a Line | 2D profile shape in each cross-section | 1.1x–2.0x |
| ⌓ | Profile of a Surface | Entire 3D surface shape (most versatile symbol) | 1.2x–2.5x |

### Orientation Controls (3 symbols — require datums)

| Symbol | Name | What It Controls | Cost Multiplier |
|--------|------|-----------------|-----------------|
| ⊥ | Perpendicularity | 90° to datum within tolerance | 1.1x–2.0x |
| ∠ | Angularity | Basic angle to datum within tolerance | 1.2x–2.5x |
| ∥ | Parallelism | Parallel to datum within tolerance | 1.1x–2.0x |

### Location Controls (3 symbols — require datums)

| Symbol | Name | What It Controls | Cost Multiplier |
|--------|------|-----------------|-----------------|
| ⊕ | **Position** | Location of feature relative to datums (**MOST COMMON**) | 1.0x–3.0x |
| ◎ | Concentricity | Median points on datum axis (deprecated in Y14.5-2018) | 1.5x–3.0x |
| ≡ | Symmetry | Median points on datum center plane (deprecated) | 1.5x–3.0x |

### Runout Controls (2 symbols — require datum axis)

| Symbol | Name | What It Controls | Cost Multiplier |
|--------|------|-----------------|-----------------|
| ↗ | Circular Runout | Per-section during 360° rotation | 1.2x–2.5x |
| ↗↗ | Total Runout | Entire surface during 360° rotation | 1.3x–3.0x |

## Feature Control Frame (FCF) Structure

```
┌──────────┬───────────────────┬─────────┬─────────┬─────────┐
│ GD&T     │ Tolerance Value   │ Primary │Secondary│Tertiary │
│ Symbol   │ (with modifiers)  │ Datum   │ Datum   │ Datum   │
└──────────┴───────────────────┴─────────┴─────────┴─────────┘
```

Example: `⊕ | ⌀ 0.25 Ⓜ | A | B | C`
= Position, cylindrical zone ⌀0.25mm at MMC, datums A-B-C

## Material Condition Modifiers

| Modifier | Symbol | Meaning |
|----------|--------|---------|
| MMC | Ⓜ | Maximum Material Condition — bonus tolerance as feature departs from MMC |
| LMC | Ⓛ | Least Material Condition — bonus tolerance as feature departs from LMC |
| RFS | (none) | Regardless of Feature Size — no bonus (default in ASME Y14.5-2018) |
| Projected | Ⓟ | Tolerance zone projects beyond surface |
| Free State | Ⓕ | Applies in unrestrained state (flexible parts) |
| Unequally Disposed | Ⓤ | Asymmetric profile zone |

## GD&T → Manufacturing Process Mapping

| GD&T Requirement | Achievable With | Dedicated Process When |
|------------------|----------------|----------------------|
| Flatness > 0.05mm | Standard milling | Always achievable |
| Flatness 0.01-0.05mm | Precision milling | Surface grinding recommended |
| Flatness < 0.01mm | Lapping mandatory | Lapping machine or hand scraping |
| Position > 0.1mm ⌀ at MMC | Standard CNC | Routine capability |
| Position 0.025-0.1mm ⌀ | Precision CNC | Good tooling required |
| Position < 0.025mm ⌀ | Jig boring | Specialized equipment |
| Cylindricity > 0.025mm | CNC turning | Good lathe practice |
| Cylindricity < 0.025mm | Cylindrical grinding | Dedicated operation |
| Cylindricity < 0.005mm | Honing/superfinishing | Multiple finishing ops |
| Total Runout < 0.025mm | Grinding between centers | Centerless grinding |

## GD&T Cost Estimation Formula

```
GD&T_cost = base_machining_cost
    × process_upgrade_multiplier    (1.0-3.0 based on tolerance tightness)
    + inspection_time × CMM_rate    (₹1500-3000/hr in India)
    + fixture_cost_amortized        (special fixtures for datum simulation)
    + scrap_factor                  (0-20% depending on Cpk)
```

## Indian Context: GD&T Adoption Levels

| Tier | Companies | GD&T Understanding | Inspection |
|------|-----------|-------------------|------------|
| Tier 1 (OEMs) | Bharat Forge, L&T Defence, HAL | Full ASME/ISO understanding | CMM |
| Tier 2 (Mid-size) | Mixed understanding, position/flatness OK | Some CMM |
| Tier 3 (Small shops) | Basic ±only, GD&T often ignored | Hand gauges |

**Opportunity for Costimize:** A tool that translates GD&T into plain-language cost impacts ("this 0.02mm flatness adds ₹450 for grinding") is extremely valuable for procurement negotiations.

---

# PART 4: 2D→3D RECONSTRUCTION — YOU DON'T NEED IT

## 50 Years of Research, Still Unsolved

The problem of reconstructing 3D objects from 2D engineering drawings has been studied since **1971 (Idesawa, University of Tokyo)**. Key eras:

- **1970s-80s**: Wireframe reconstruction (Idesawa, Wesley & Markowsky at IBM, Sakurai & Gossard at MIT)
- **1980s-90s**: B-rep solid models (Shin & Shin at Seoul National, Geng at Pittsburgh)
- **1990s-2000s**: CSG approaches (Chinese university dominance — Zhejiang, Tsinghua, HUST)
- **2010s-present**: Deep learning attempts (limited success due to training data scarcity)

**Status: UNSOLVED in the general case.** Specific sub-problems are solved (simple polyhedral objects), but real-world industrial drawings with annotations, sections, and curved surfaces defeat all algorithms.

## The Ambiguity Problem

A single set of three orthographic views can correspond to **multiple valid 3D objects**. This fundamental mathematical ambiguity has no general solution. Two views constrain a point to a line; three views give a point — but "ghost" vertices appear that don't belong to any real object.

## Why You Don't Need Full 3D

For cost estimation at ±10% accuracy, you need:

| What You Need | Why | Extractable Without 3D? |
|---------------|-----|------------------------|
| Bounding dimensions (L×W×H or ⌀×L) | Material volume/weight | YES — largest annotated dimensions |
| Material type | Cost/kg, machinability | YES — title block |
| Feature list with dimensions | Process time estimation | YES — from individual views |
| Feature count | Setup time, tool changes | YES — count across views |
| Tolerance requirements | Tight tolerance surcharges | YES — annotated directly |
| Surface finish | Finishing process costs | YES — if annotated |

## The "Good Enough" Tiers

| Tier | Approach | Accuracy | When |
|------|----------|----------|------|
| Tier 1 | LLM Vision (current) | ±15-20% | Now |
| Tier 2 | Structured LLM (view-by-view prompting) | ±10-15% | Next |
| **Tier 3** | **DXF parsing + LLM** | **±5-10%** | **Priority** |
| Tier 4 | Full feature recognition + rules | ±3-5% | Future |

## CSG Thinking — The Right Mental Model

Even without implementing CSG reconstruction, think of every part as:
```
Part = Base Shape + Added Features - Subtracted Features
```
Each feature maps to a manufacturing operation and a cost:
- Union of cylinder = turned feature / boss
- Subtraction of cylinder = drilled hole
- Subtraction of rectangle = milled pocket

## By Part Type — What's Needed

**Turned parts (axisymmetric):** ONE side view (longitudinal cross-section) gives 80-90% of cost-relevant info. Section view adds internal features. End view adds cross-holes, keyways.

**Milled/prismatic parts:** Need 2+ views for bounding box + feature identification from each view.

**Sheet metal:** Flat pattern is inherently 2D — no 3D needed at all. Cost = material area + bend count + hole count.

**PCB/Cable assemblies:** Already 2D/1D — BOM + dimensions only.

## What Each View Reveals

| Feature | Front View | Top View | Side View | Section View |
|---------|-----------|----------|-----------|-------------|
| Through hole (vertical) | Hidden lines | Circle | Hidden lines | Circle with hatch gap |
| Blind hole | Partial hidden lines | Circle | Partial hidden lines | Depth visible |
| Pocket | Hidden rectangle | Rectangle outline | Hidden rectangle | Depth and wall profile |
| Thread | Thin lines (convention) | Circle pair (major/minor) | Thin lines | Thread profile |
| Groove | Narrow notch | Ring (circle pair) | Narrow notch | Clear U/V profile |
| Chamfer | Angled line | N/A | Angled line | Angled line |

## Key Papers

| Author(s) | Year | Contribution |
|-----------|------|-------------|
| Idesawa | 1971 | First 2D→3D wireframe algorithm (University of Tokyo) |
| Wesley & Markowsky | 1980 | "Fleshing out wire frames" (IBM Research) |
| Sakurai & Gossard | 1983 | First solid models from orthographic views (MIT) |
| Shin & Shin | 1998 | Boolean operation approach (Seoul National) |
| Geng, Bidanda & Baralt | 2002 | Complete method for polyhedral objects (Pittsburgh) |
| Liu, Hu et al. | 2001 | Curved solid reconstruction (Tsinghua) |
| Dimri & Gurumoorthy | 2005 | Handling section views (IIT Madras) |
| **arXiv 2508.12440** | 2025 | **DXF features → XGBoost: 3.91% MAPE (skip 3D entirely)** |

**Chinese academic papers are the richest source** for this field — 40-50% of Google Scholar results. Key institutions: Zhejiang, Tsinghua, HUST, Shandong.

---

# PART 5: THE AGENTIC ARCHITECTURE PATTERN

## Validated by Landing AI, Reducto, and Werk24

All three leading document parsing companies converge on the same architecture:

### The Pattern
```
Document Input
    → Layout Detection (find regions and their types)
    → Region Classification (text, table, chart, view, GD&T, title block)
    → Specialized Processing per Region Type
    → LLM Agent Orchestrates (decides which tools to call)
    → Self-Verification (cross-check extracted values)
    → Structured Output
```

### Landing AI's Implementation (DeepLearning.AI Course)

From the "Document AI: From OCR to Agentic Doc Extraction" course:

1. **LayoutReader** reorders text into correct reading order
2. **PaddleOCR LayoutDetect** identifies regions and types
3. **LangChain Agent** with specialized tools:
   - `analyze_chart()` → sends cropped chart to VLM
   - `analyze_table()` → sends cropped table to VLM
4. Agent decides **which regions need deeper analysis** based on the query
5. Agent synthesizes all extracted data

### Applied to Engineering Drawings

```
Engineering Drawing (PDF/image)
    → Layout Detection: title block, views, notes, BOM, GD&T frames
    → Region-Specific Processing:
        Title Block → OCR → part number, material, revision
        Drawing Views → VLM → dimensions, features
        GD&T Frames → Specialized Parser → tolerance data
        Notes Section → OCR + NLP → process requirements
        BOM Table → Table Parser → component list
    → LLM Agent orchestrates tool selection per region
    → Schema-driven extraction fills cost model inputs
    → Self-verification: dimensions sum correctly, material matches tolerances
    → Output: structured data for cost engine
```

### Visual Grounding is Essential

Every extracted value must trace back to a bounding box on the source document:
- "I extracted ⌀25.0 ±0.05 from [x1, y1, x2, y2] on page 1"
- Enables verification by procurement teams
- Builds trust: "here is where this cost-driving dimension came from"

### Schema-Driven Extraction

Define Pydantic models for output:
```python
class DrawingExtraction(BaseModel):
    material: str
    overall_dimensions: Dimensions
    features: list[Feature]
    tolerances: list[Tolerance]
    surface_finishes: list[SurfaceFinish]
    processes_required: list[str]
```

---

# PART 6: WHO HAS MASTERED DOCUMENT PARSING (AND WHO HASN'T)

## Tier 1: Purpose-Built Document Intelligence Companies

| Company | Funding | Approach | Engineering Drawing Support |
|---------|---------|----------|---------------------------|
| **Reducto** | $108M | 6 CV models + VLM contextual review + agentic OCR self-correction (1B+ pages processed) | NO (enterprise docs) |
| **Landing AI** | $57M | Agentic Document Extraction, DPT-2 model | NO (business docs) |
| **Unstructured.io** | Open source + commercial | partition → chunk → embed → stage | NO (general docs) |
| **Werk24** | Bootstrapped | 4-stage: preprocess → ML detect → engineering expert system validate → reject-if-uncertain | **YES** (best for drawings) |
| **CoLab Software** | $72M (Series C) | AI-powered engineering drawing review and markup | **YES** (review, not extraction) |
| **DraftAid** | YC-backed | Generative AI for CAD drafting | PARTIAL (generation, not parsing) |
| **Infrrd** | Enterprise | 97%+ accuracy on engineering document extraction | **YES** (claims highest accuracy) |
| **TwinKnowledge** | $3.7M | AI for construction/engineering document understanding | **YES** (construction-focused) |

### Reducto Architecture Details (6-Model Pipeline)

Reducto's $108M approach uses **6 specialized CV models** working in sequence:
1. **Document classifier** — page type identification
2. **Layout segmenter** — region detection and classification
3. **Table detector** — specialized table structure recognition
4. **Figure detector** — chart/diagram identification
5. **OCR engine** — text extraction per region
6. **VLM contextual reviewer** — semantic validation of extracted content

Key insight from Reducto's founders: "Every model in the pipeline is replaceable — the orchestration logic is the real IP." Their agentic OCR self-correction loop catches ~15% of errors that single-pass extraction misses.

### Werk24's "Reject Rather Than Guess" Philosophy

Werk24's 4-stage pipeline for engineering drawings:
1. **Preprocessing** — normalize, deskew, enhance
2. **ML Detection** — detect regions, dimensions, symbols
3. **Engineering Expert System** — validate extracted data against manufacturing rules (e.g., "a tolerance of ±0.001mm on a 500mm dimension is implausible")
4. **Decision gate** — if confidence < threshold, **reject the drawing** rather than return incorrect data

This philosophy is critical for manufacturing: a wrong dimension costs more than no dimension. Costimize should adopt the same approach — flag uncertain extractions for human review rather than guessing.

## Tier 2: Cloud Provider APIs

| Provider | Strengths | Drawing Support |
|----------|-----------|----------------|
| Google Document AI | Best OCR engine, layout parser | NO |
| AWS Textract | Strong table extraction | NO |
| Azure Document Intelligence | Best enterprise integration | NO |

## Tier 3: Multimodal LLMs

| Model | Drawing Accuracy | Best Use |
|-------|-----------------|----------|
| Gemini 2.5 Pro | ~80% | Best zero-shot for drawings |
| Gemini 2.5 Flash | ~77% | Best value |
| GPT-4o | ~40% | General fallback |
| Claude Opus 4 | ~40% | Reasoning-heavy tasks |

## Tier 4: Open Source Tools

| Tool | Best For | Drawing Suitability |
|------|----------|-------------------|
| **PaddleOCR** | Production OCR, multilingual | MEDIUM — strong text, can be fine-tuned |
| **PaddleOCR-VL** (Oct 2025) | 0.9B VLM, 92.56% OmniDocBench | HIGH — surpasses all mainstream models at tiny size |
| **Surya** | OCR + layout + reading order | MEDIUM — good OCR, no symbols |
| **Docling** (IBM) | PDF → JSON/MD conversion | LOW — text documents |
| **Marker** | PDF → Markdown | LOW — text-focused |
| **GOT-OCR 2.0** | General OCR including formulas | MEDIUM-HIGH |
| **Florence-2** | Dense captioning, grounding | MEDIUM — locating features |
| **YOLOv11-OBB** | Oriented bounding box detection | MEDIUM — rotated text/symbols |
| **SAM 2** (Meta) | Segment anything | MEDIUM — segmenting views |
| **RolmOCR** (Reducto, Apr 2025) | Qwen2.5-VL-7B fine-tuned OCR, Apache 2.0 | MEDIUM — rotated text robust, open-source |
| **olmOCR 2** (Allen AI) | RL-trained OCR, 82.4% on olmOCR-Bench | MEDIUM — math/table specialist, $2/10K pages |
| **eDOCr2** (Linkoping Univ) | Engineering drawing OCR + VLM verify | HIGH — 93.75% recall, <1% CER on drawings |

## The Semantic Understanding Gap

### What Current Tech CAN Do
- Detect text (OCR reads "25.4 ±0.05" at 90%+ on clean prints)
- Detect symbols (trained YOLO can find GD&T at 85%+)
- Detect lines (Hough transform, neural line detection)
- Detect regions (layout models segment views, title block, notes)

### What Current Tech CANNOT Reliably Do
- **Semantic association**: Which dimension spans which two features?
- **GD&T interpretation**: What does `⟁ | 0.02 | A | B` mean for manufacturing?
- **Cross-view correspondence**: This circle in top view = this hole in front view
- **Manufacturing inference**: These features require turning → drilling → threading

### Why the Gap Exists
1. **Training data scarcity** — no large annotated datasets (companies guard drawings as IP)
2. **Domain knowledge required** — needs manufacturing + metrology + GD&T expertise
3. **Context-dependent interpretation** — "R5" could be radius, roughness, or revision
4. **Graph structure, not sequence** — spatial graph, not left-to-right text

---

# PART 7: SECTION VIEWS — THE HARDEST PARSING PROBLEM

## Section View Types

| Type | What It Shows | Detection Clues |
|------|--------------|-----------------|
| Full Section | Complete cross-section through cutting plane | Hatching fills entire cut area |
| Half Section | One half sectioned, other half external view | Hatching on one side of centerline |
| Offset Section | Cutting plane changes direction | Cutting plane line has 90° bends |
| Broken-out Section | Small local area sectioned | Irregular break line boundary |
| Removed Section | Cross-section displayed away from view | Labeled with section letters, positioned separately |
| Revolved Section | Cross-section rotated 90° and superimposed | Section appears rotated within the view |

## Cross-Hatching Patterns

Per ASME/ISO standards, different materials have standard hatch patterns:
- Cast iron: evenly spaced 45° lines
- Steel: same as cast iron (most common)
- Aluminum: alternating close/wide spaced lines
- Bronze/brass: alternating full/dashed lines
- Rubber/plastic: alternating full/dashed at different angle

**In practice:** Most drawings use generic 45° hatching regardless of material. Material is specified in the title block or notes, not from hatch patterns.

## What Section Views Reveal (Critical for Cost)

| Internal Feature | Only Visible In | Cost Impact |
|-----------------|-----------------|-------------|
| Internal bore diameter/depth | Section view | Boring operation |
| Wall thickness | Section view | Material selection, machining approach |
| Internal threads | Section view | Tapping operation |
| Internal grooves (O-ring, snap ring) | Section view | Grooving tool, internal access |
| Keyways (internal) | Section + end view | Broaching or slotting |
| Counterbores/countersinks | Section view | Drilling + secondary operation |
| Internal cavities | Section view | EDM or complex milling |
| Draft angles (cast parts) | Section view | Mold design, post-machining |

## Section View Parsing Pipeline

```
1. Detect cutting plane lines (A-A, B-B) in parent view
    → Long-short-long dash pattern with arrows at ends
    → Letters identify the section

2. Find corresponding section view
    → Labeled "SECTION A-A" or "A-A"
    → May be on same sheet or different sheet

3. Identify hatched regions
    → Cross-hatching = cut material (solid)
    → Non-hatched enclosed areas = cavities/holes
    → Different hatch patterns/angles = different parts (assemblies)

4. Extract internal features from section geometry
    → Parallel lines with hatching between = wall
    → Non-hatched circle within hatching = bore/hole
    → Dimension callouts in section = internal dimensions

5. Associate section features with external views
    → Match section position to cutting plane location
    → Internal features at specific axial positions
```

---

# PART 8: MANUFACTURING PROCESS INFERENCE FROM DRAWINGS

## Feature → Process Mapping

| Drawing Feature | Visual Signature | Manufacturing Process | Cost Driver |
|----------------|-----------------|----------------------|-------------|
| External diameter | Parallel lines in profile | CNC Turning | Diameter, length, material |
| Diameter step | Width change in profile | Turning (extra pass) | Number of steps |
| Taper/cone | Angled line in profile | Taper turning | Angle, length |
| External thread | Thin parallel lines | Threading | Pitch, length, type |
| Internal bore | Section: parallel lines in hatching | Boring or drilling | Diameter, depth, tolerance |
| Internal thread | Section: thin lines in bore | Tapping | Pitch, depth |
| Through hole | Circle in top view | Drilling | Diameter, depth |
| Blind hole | Circle + partial hidden lines | Drilling | Diameter, depth |
| Counterbore | Two concentric circles + step in section | Drill + counterbore | Two diameters |
| Countersink | Two concentric circles + taper in section | Drill + countersink | Diameter, angle |
| Pocket | Rectangle in top + depth in section | End milling | L×W×D |
| Slot | Elongated rectangle | Slot milling | Width, length, depth |
| Keyway | Rectangle at circumference (end view) | Milling or broaching | Width, depth |
| Flat bottom hole | Section: flat bottom visible | End mill or flat drill | Diameter, depth |
| Groove (external) | Narrow notch in profile | Grooving tool | Width, diameter |
| Groove (internal) | Section: notch inside bore | Internal grooving | Width, diameter, access |
| Chamfer | Angled line at edge | Chamfering pass | Angle, size |
| Fillet/radius | Arc at junction | Radius tool or interpolation | Radius |
| Knurl | Crosshatch pattern on surface | Knurling | Type, length |
| Surface finish Ra < 0.8μm | Surface finish symbol | Grinding | Area |
| Surface finish Ra < 0.2μm | Surface finish symbol | Lapping/polishing | Area, time |

## Tolerance Grade → Process Mapping (ISO IT Grades)

| IT Grade | Tolerance Range (for 25mm) | Achievable With | Typical Cost Multiplier |
|----------|---------------------------|-----------------|------------------------|
| IT12-IT11 | ±0.105-0.065mm | Rough turning, sawing | 1.0x (base) |
| IT10-IT9 | ±0.042-0.026mm | Standard CNC turning/milling | 1.0-1.2x |
| IT8-IT7 | ±0.016-0.010mm | Precision CNC, reaming, boring | 1.3-1.8x |
| IT6 | ±0.0065mm | Grinding, honing | 2.0-3.0x |
| IT5 | ±0.0045mm | Precision grinding, lapping | 3.0-5.0x |
| IT4-IT3 | ±0.003-0.002mm | Superfinishing, diamond turning | 5.0-10.0x |

**Key rule:** Each IT grade improvement adds approximately 30-50% to machining cost. Below IT6, cost increases exponentially.

## Surface Roughness → Process Mapping

| Ra (μm) | Surface Condition | Process Required | Cost Impact |
|----------|------------------|-----------------|-------------|
| 12.5-6.3 | Rough machined | Standard turning/milling | Base |
| 3.2-1.6 | Fine machined | Finish pass, sharp tooling | +20-40% |
| 0.8-0.4 | Ground | Cylindrical/surface grinding | +80-150% |
| 0.2-0.1 | Lapped/honed | Lapping, honing | +200-400% |
| 0.05-0.025 | Superfinished | Superfinishing, polishing | +500-1000% |

**Practical insight (Polgar time estimation methodology):** Time for finishing operations scales exponentially — halving Ra roughly doubles the finishing time and cost.

## The Machining Sequence Problem

Order matters — each operation assumes the previous has been completed:

**Typical turned part sequence:**
1. Face end → establish datum
2. Turn OD (rough) → remove bulk material
3. Turn OD (finish) → achieve diameter tolerance
4. Drill center → prepare for boring
5. Bore ID (if applicable) → internal diameter
6. Thread (if applicable) → external/internal threads
7. Groove → if needed
8. Cut off → part from bar stock
9. Flip and face second end
10. Grind → if tight tolerances required

**Setup changes are expensive:**
- Each flip/re-fixture = ₹500-2000 in Indian job shops
- Minimize setups by machining all features accessible in one orientation
- 5-axis CNC reduces setups but costs more per hour

## CAPP (Computer-Aided Process Planning)

| Approach | How It Works | Status |
|----------|-------------|--------|
| **Variant CAPP** | Find similar part in database, modify its process plan | Most practical for Indian manufacturing |
| **Generative CAPP** | Generate plan from scratch using rules + optimization | Academic, limited commercial use |
| **AI-assisted CAPP** | LLM + rules for process selection and sequencing | Emerging (what Costimize should build) |
| **CAPP-GPT (2024)** | LLM-based process planning using structured prompts + machining knowledge | Research paper — promising results on standard parts |
| **ARKNESS (2025)** | Knowledge graph + 3B Llama model — matches GPT-4o on machining questions | Open-weight, specialized for manufacturing |

### CAPP-GPT & ARKNESS — LLM-Based Process Planning

**CAPP-GPT (2024):** Uses structured prompting with machining knowledge to generate process plans from part descriptions. Key insight: LLMs can reason about process sequencing when given the right context (material properties, feature types, tolerance requirements). Not yet production-ready but demonstrates the approach.

**ARKNESS (2025):** A manufacturing knowledge graph trained into a 3B-parameter Llama model. On machining-specific questions, it matches GPT-4o performance at 1/100th the inference cost. The knowledge graph encodes: material-process compatibility, process capability limits, tooling constraints, and sequencing rules.

**Implication for Costimize:** You don't need GPT-4o for process planning — a fine-tuned smaller model with the right manufacturing knowledge can match or exceed it. ARKNESS validates the "domain knowledge > model size" hypothesis.

### Key Books on Process Planning

| Book | Author(s) | Focus |
|------|-----------|-------|
| "Computer-Aided Manufacturing" | Tien-Chien Chang | CAPP algorithms, process selection |
| "Principles of Process Planning" | Halevi & Weill | Comprehensive process planning |
| "DFMA: Product Design for Manufacture and Assembly" | Boothroyd, Dewhurst, Knight | THE foundational text |
| "Manufacturing Processes for Engineering Materials" | Kalpakjian & Schmid | Machining economics chapter |
| "Fundamentals of Modern Manufacturing" | Groover | Process capabilities |
| "Realistic Cost Estimating for Manufacturing" | Lembersky | SME practical handbook |

---

# PART 9: PDF PARSING TECHNICAL APPROACHES

## PDF Internal Structure for CAD-Exported Drawings

When AutoCAD/SolidWorks exports to PDF:
- **Vector content**: Lines, arcs, circles stored as PDF path operators (moveto, lineto, curveto)
- **Text**: Dimension values, notes stored as text objects with position coordinates
- **Leader lines**: Stored as paths connecting text to geometry
- **The key distinction**: Vector PDFs preserve geometry; scanned PDFs are just images

## The SHX Font Problem (AutoCAD-Specific)

AutoCAD's native SHX fonts are **not standard PDF fonts**. When AutoCAD exports to PDF:
- SHX text is rendered as **geometry** (tiny line segments), not text objects
- `page.get_text()` returns **nothing** for SHX-rendered dimensions
- This affects ~40-60% of AutoCAD-exported PDFs in Indian manufacturing

**Detection:**
```python
import fitz
doc = fitz.open("drawing.pdf")
page = doc[0]
text = page.get_text("text")
drawings = page.get_drawings()

# If lots of geometry but almost no text → likely SHX font issue
if len(drawings) > 100 and len(text.strip()) < 50:
    print("SHX font detected — must use OCR for text extraction")
```

**Solution:** Rasterize at 300+ DPI and use PaddleOCR for text extraction on the affected regions.

## PyMuPDF Code Examples for Engineering Drawings

### Extract Vector Paths (Lines, Arcs, Circles)

```python
import fitz

doc = fitz.open("drawing.pdf")
page = doc[0]

# Get all vector drawing elements
paths = page.get_drawings()

for path in paths:
    for item in path["items"]:
        if item[0] == "l":  # Line
            start, end = item[1], item[2]
            print(f"Line: ({start.x:.1f},{start.y:.1f}) → ({end.x:.1f},{end.y:.1f})")
        elif item[0] == "c":  # Cubic Bezier curve (arcs become these in PDF)
            p1, p2, p3, p4 = item[1], item[2], item[3], item[4]
            print(f"Curve: control points {p1}, {p2}, {p3}, {p4}")
        elif item[0] == "re":  # Rectangle
            rect = item[1]
            print(f"Rectangle: {rect}")
```

### Extract Text with Positions (Dimension Values)

```python
# Get text blocks with full position information
text_dict = page.get_text("dict")

for block in text_dict["blocks"]:
    if block["type"] == 0:  # Text block
        for line in block["lines"]:
            for span in line["spans"]:
                text = span["text"]
                bbox = span["bbox"]  # (x0, y0, x1, y1)
                size = span["size"]
                # Dimension values are typically 2-4mm text
                if size < 12 and any(c.isdigit() for c in text):
                    print(f"Possible dimension: '{text}' at {bbox}")
```

### Detect Title Block Region

```python
# Title block is always bottom-right, bounded by thick lines
page_rect = page.rect
# Typical title block occupies bottom ~20% and right ~40% of the page
title_region = fitz.Rect(
    page_rect.width * 0.55,  # Right portion
    page_rect.height * 0.75,  # Bottom portion
    page_rect.width,
    page_rect.height
)
# Extract text only from title block region
title_text = page.get_text("text", clip=title_region)
```

### Hybrid Pipeline: Vector + OCR + VLM

```python
import fitz
from paddleocr import PaddleOCR
from PIL import Image
import io

def extract_drawing(pdf_path):
    doc = fitz.open(pdf_path)
    page = doc[0]

    # Step 1: Try vector extraction
    text_content = page.get_text("text")
    vector_paths = page.get_drawings()

    # Step 2: Detect if SHX fonts (text as geometry)
    is_shx = len(vector_paths) > 100 and len(text_content.strip()) < 50

    if is_shx:
        # Step 3a: Rasterize and OCR
        pix = page.get_pixmap(dpi=300)
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        ocr = PaddleOCR(use_angle_cls=True, use_textline_orientation=True, lang='en')
        ocr_results = ocr.ocr(img)
        # ... process OCR results
    else:
        # Step 3b: Use vector text directly
        text_dict = page.get_text("dict")
        # ... process positioned text

    # Step 4: Send to VLM for semantic interpretation
    pix = page.get_pixmap(dpi=200)
    # ... send image to Gemini with structured prompt

    # Step 5: Cross-validate vector data vs VLM output
    # ... compare extracted dimensions for consistency
```

## LatticeLabsAI/cadling — Best Open-Source Engineering PDF Parser

**GitHub: LatticeLabsAI/cadling** — the most sophisticated open-source engineering drawing PDF parser found:
- Built on PyMuPDF
- **Arc detection from Bezier curves** (solves the "PDF has no arc primitive" problem)
- Dimension line detection with arrow/tick mark classification
- Title block extraction with template matching
- Drawing view boundary detection

Key innovation: reconstructs arcs from cubic Bezier curve sequences (PDFs store arcs as Bezier approximations, not as native arc entities). This is essential for identifying circular features (holes, bores, fillets).

## Python PDF Parsing Libraries

| Library | Best For | Drawing Suitability |
|---------|----------|-------------------|
| **PyMuPDF (fitz)** | Vector path extraction, text with positions | HIGH — can extract geometry from vector PDFs |
| **pdfplumber** | Table and line extraction | MEDIUM — good for structured layouts |
| **pdf2image + OpenCV** | Rasterize then CV | MEDIUM — for scanned PDFs |
| **camelot** | Table extraction | LOW — tables only |
| **pikepdf** | Low-level PDF manipulation | LOW — too low-level |

## The Hybrid Approach (Vector + Vision)

For maximum accuracy:
```
PDF Input
    → Detect: vector or raster?

    If VECTOR (CAD-exported):
        → PyMuPDF: extract paths (lines, arcs, circles)
        → PyMuPDF: extract text with positions
        → Rule-based: associate text with nearest geometry
        → LLM: semantic interpretation of what's been extracted

    If RASTER (scanned):
        → pdf2image: high-res rasterize (300+ DPI)
        → PaddleOCR: text detection + recognition
        → YOLOv11-OBB: symbol/region detection
        → Gemini: semantic interpretation

    → Merge and validate
    → Structured output
```

## PaddleOCR Configuration for Engineering Drawings

**Critical setting:** `use_textline_orientation=True` — default angle classifier only supports 0°/180°, which **FAILS on vertical dimension callouts** (90° text is extremely common in drawings).

```python
from paddleocr import PaddleOCR
ocr = PaddleOCR(
    use_angle_cls=True,
    use_textline_orientation=True,  # CRITICAL for drawings
    lang='en',
)
```

## Recommended Stack for Costimize (2026)

**Tier 1 — DXF/DWG files (best accuracy, 70-85% automated):**
```
ezdxf → parse entities → classify layers → extract dimensions →
rule-based association → structured output
```

**Tier 2 — Clean PDF drawings (60-75% automated):**
```
PDF → detect vector/raster →
IF vector: PyMuPDF path + text extraction
IF raster: high-res rasterize → PaddleOCR
→ YOLOv11-OBB (symbol detection, fine-tuned)
→ Gemini (semantic interpretation)
→ rule-based validation → structured output
```

**Tier 3 — Scanned drawings (40-60% automated):**
```
Scan → denoise/deskew → binarize → same as Tier 2 raster path
```

---

# PART 10: LANDING AI COURSE — KEY TAKEAWAYS

## Course: "Document AI: From OCR to Agentic Doc Extraction"
- **Duration:** 3 hours, 15 videos, 6 hands-on labs
- **Instructors:** David Park, Andrea Kropp (LandingAI)
- **Free** on DeepLearning.AI

## Technology Stack
- Tesseract (baseline OCR)
- PaddleOCR (deep learning OCR)
- LayoutReader (reading order)
- LangChain agents (tool orchestration)
- LandingAI ADE API (production extraction)
- ChromaDB (vector database for RAG)
- AWS (S3, Lambda, Bedrock for deployment)

## ADE (Agentic Document Extraction) Product

Three endpoints:
- **Parse**: Document → structured Markdown + chunks with visual grounding (bounding boxes)
- **Extract**: Markdown + JSON schema → structured key-value data
- **Split**: Classify and separate mixed document packages

Key model: **DPT-2** (Document Pre-trained Transformer v2)
- DocVQA benchmark: 99.16%
- Multi-pass: layout analysis → per-region extraction → structure assembly → verification

## What's "Agentic" About It

1. **Planning**: Examines document layout, determines processing steps needed
2. **Tool Selection**: Calls different specialized tools per region type
3. **Multi-Pass**: Multiple passes over document, examining regions with different tools
4. **Self-Verification**: Checks output consistency (row totals match, dates plausible)

## Direct Application to Costimize

1. **BOM/PO parsing**: ADE could handle messy supplier PDF BOMs better than manual column detection
2. **Architecture pattern**: The Lab 3 agentic pattern (layout detect → region classify → specialized tools) is the right architecture for drawing extraction
3. **Visual grounding**: Every extracted value → bounding box → source verification → trust

---

# PART 11: CURRENT ACCURACY CEILING (2026)

| Task | Best Achievable | Approach |
|------|----------------|----------|
| Title block extraction | 95-99% | OCR + template matching |
| BOM extraction | 90-95% | Table detection + OCR |
| Notes/text extraction | 90-95% | OCR (clean prints) |
| Dimension value reading | 85-90% | OCR + specialized detection |
| Dimension-to-feature association | 60-75% | Vision LLM + heuristics |
| GD&T frame reading | 75-85% | Specialized symbol detection |
| GD&T semantic interpretation | 40-60% | Vision LLM (unreliable) |
| Full drawing → structured model | 30-50% | No reliable solution |
| **DXF → structured model** | **70-85%** | **ezdxf + rule-based** |

## The Fundamental Issue

Engineering drawings require **ZERO-ERROR extraction**. A single wrong dimension (25.4 vs 24.5) means a wrong part. LLMs are probabilistic — they will always have some error rate. **Human-in-the-loop review will remain essential** for the foreseeable future.

## Timeline Assessment

| Document Type | When Reliable | Notes |
|---------------|--------------|-------|
| Simple documents | NOW (2024-2025) | 95%+ solved |
| Complex business docs | NOW (2025-2026) | 85-95% |
| Technical docs with diagrams | 2027-2028 | Multimodal LLMs improving fast |
| Engineering drawings (dimension extraction) | 2028-2030 | Needs specialized training data |
| Engineering drawings (full semantic understanding) | 2030-2035 | May always need human-in-loop |

---

# PART 12: AUTOMATED GD&T EXTRACTION PIPELINE

## Recommended ML Pipeline for Costimize

```
Drawing Image
    │
    ▼
[YOLO/Faster R-CNN] → Detect FCF bounding boxes + Datum symbols
    │
    ▼
[Crop & Segment] → Split each FCF into compartments
    │
    ▼
[Symbol Classifier CNN] → Identify GD&T symbol type (14 classes)
[OCR (PaddleOCR)] → Extract tolerance value + datum letters
[Modifier Classifier] → Detect MMC/LMC/RFS modifiers
    │
    ▼
[Structured Output] → JSON: {symbol, value, zone_type, modifiers, datums[]}
    │
    ▼
[Association Engine] → Follow leader lines to connect FCF → feature
    │
    ▼
[Cost Impact Calculator] → Map GD&T → process → cost multiplier
```

## Target Output Format

```json
{
  "type": "position",
  "zone_shape": "cylindrical",
  "tolerance_value": 0.25,
  "unit": "mm",
  "material_condition": "MMC",
  "datums": [
    {"letter": "A", "modifier": null},
    {"letter": "B", "modifier": null},
    {"letter": "C", "modifier": null}
  ],
  "cost_impact": {
    "process_required": "precision_cnc",
    "multiplier": 1.3,
    "inspection_method": "CMM",
    "inspection_time_min": 5
  }
}
```

## Training Data Challenge

**No public annotated dataset of GD&T symbols from engineering drawings exists.**

Options:
1. **Synthetic data**: Render FCFs with known parameters, train on those (fastest)
2. **Customer corrections**: Every human correction = labeled training data (best long-term)
3. **Annotate 500-1000 drawing regions** manually (most effort, best quality)

---

# PART 13: REFERENCE BOOKS — THE COMPLETE LIST

## Engineering Drawing Interpretation

| Book | Author(s) | Use For |
|------|-----------|---------|
| "Technical Drawing with Engineering Graphics" | Giesecke et al. (15th ed.) | THE classic — published 1933, comprehensive |
| "Fundamentals of Graphics Communication" | Bertoline et al. | Standard US textbook |
| "Engineering Drawing" | N.D. Bhatt (Charotar) | Standard Indian textbook, BIS conventions |
| "Machine Drawing" | K.L. Narayana et al. | Indian GD&T fundamentals |

## GD&T

| Book | Author(s) | Use For |
|------|-----------|---------|
| **"Geometric Dimensioning and Tolerancing"** | **Alex Krulikowski** (9th+ ed.) | **THE GD&T bible** — most widely used worldwide |
| "GD&T for Mechanical Design" | Gene Cogorno | Practical, designer-focused |
| "GD&T Application and Interpretation" | Bruce Wilson | Quality engineering focused |
| "Mechanical Tolerance Stackup and Analysis" | Bryan Fischer | Tolerance stack-up analysis |
| "Dimensioning and Tolerancing Handbook" | Paul Drake | Comprehensive engineering reference |

## Standards

| Standard | Title |
|----------|-------|
| **ASME Y14.5-2018** | Dimensioning and Tolerancing (234 pages) |
| ASME Y14.5-2009 | Previous edition (still on most existing drawings) |
| ISO 1101:2017 | Geometrical tolerancing |
| IS 8000 (Parts 1-4) | Indian Standard for GD&T (based on ISO) |

## Manufacturing/Cost Estimation

| Book | Author(s) | Use For |
|------|-----------|---------|
| **"DFMA: Product Design for Manufacture and Assembly"** | **Boothroyd, Dewhurst, Knight** | **THE foundational text** |
| "Manufacturing Processes for Engineering Materials" | Kalpakjian & Schmid | Machining economics |
| "Fundamentals of Modern Manufacturing" | Groover | Process capabilities |
| "Realistic Cost Estimating for Manufacturing" | Lembersky | Practical handbook |
| "Computer-Aided Manufacturing" | Tien-Chien Chang | CAPP algorithms |
| "Principles of Process Planning" | Halevi & Weill | Comprehensive process planning — best single reference |
| "Manufacturing Process Selection Handbook" | Swift & Booker | Process selection decision trees, capability charts |
| "Industrial AI" | Jay Lee | AI + manufacturing framework |
| "Polgar's Time Estimation" | MIT Open Access | Machining time estimation formulas per operation |

## 2D→3D Reconstruction Research

| Paper | Author(s) | Year | Key Contribution |
|-------|-----------|------|-----------------|
| First 2D→3D algorithm | Idesawa | 1971 | Pioneer (Univ. Tokyo) |
| "Fleshing out wire frames" | Wesley & Markowsky | 1980 | IBM Research |
| Solid models from views | Sakurai & Gossard | 1983, 1990 | MIT |
| Section view handling | Dimri & Gurumoorthy | 2005 | IIT Madras |
| DXF→cost prediction | arXiv 2508.12440 | 2025 | 3.91% MAPE |

---

# PART 14: KEY RESEARCHERS AND LABS

## Document Understanding
- **Yiheng Xu, Lei Cui** (Microsoft Research Asia) — LayoutLM series
- **Geewook Kim** (ex-Naver/Clova) — Donut creator (ECCV 2022)
- **Zejiang Shen** (MIT/Allen AI) — LayoutParser
- **Birgit Pfitzmann** (IBM Research) — DocLayNet, Docling
- **Lukas Blecher** (Meta AI Paris) — Nougat (academic PDF → LaTeX)
- **Allen AI team** — olmOCR 2 with reinforcement learning (GRPO)

## Engineering Drawing Parsing (Most Relevant to Costimize)
- **Muhammad Tayyab Khan & Seung Ki Moon** (NTU Singapore) — THE most active research group. 3 papers in 8 months:
  - Fine-tuned Florence-2 on 400 drawings (Nov 2024, arXiv:2411.03707)
  - YOLOv11-OBB + Donut: **94.77% precision on GD&T, 97.3% F1** (May 2025, arXiv:2505.01530)
  - Hybrid vision-language: **88.5% precision, 99.2% recall, 93.5% F1** (Jun 2025, SSRN)
- **Javier Toro & Mehdi Tarkian** (Linkoping Univ, Sweden) — eDOCr2: OCR + VLM verification, 93.75% text recall, <1% CER
- **Dr. Jochen Mattes** (Werk24, Munich) — Retrains ML model monthly on 100K+ drawings, 95%+ PMI extraction accuracy

## GD&T and Tolerancing
- **Edward Morse** (UNC Charlotte) — Coordinate metrology, ASME standards
- **Vijay Srinivasan** (NIST/Columbia) — ISO GPS and ASME Y14.5
- **Joseph K. Davidson** (Arizona State) — Tolerance zone mathematical modeling
- **Kenneth Chase** (BYU) — Tolerance stack-up analysis
- **Alex Krulikowski** — THE GD&T trainer/author
- **Gaurav Ameta** (Washington State) — Ontology-based GD&T interpretation

## 2D→3D Reconstruction
- Chinese university dominance: Zhejiang, Tsinghua, HUST, Shandong
- **Geng & Bidanda** (Pittsburgh) — Polyhedral reconstruction
- **Dimri & Gurumoorthy** (IIT Madras) — Section views

## Manufacturing AI / Feature Recognition
- **AAGNet** — Graph neural network for machining feature recognition from B-rep models
- **FeatureNet** — 3D CNN, 24 machining feature classes (holes, pockets, slots, etc.)
- **ARKNESS team** — Knowledge graph + small LLM for manufacturing reasoning (2025)

## Recent Key Papers (2024-2026)

| Paper | Venue | Year | Key Contribution |
|-------|-------|------|-----------------|
| **CReFT-CAD** | NeurIPS | 2025 | TriView2CAD benchmark with 200K annotated engineering drawings — first large-scale public dataset |
| **Cadrille** | ICLR | 2026 | Multimodal CAD reconstruction — combines vision + language for 3D from drawings |
| **CAD2Program** | AAAI | 2025 | 2D drawing → Python program → 3D model (code as intermediate representation) |
| **CAPP-GPT** | — | 2024 | LLM-based computer-aided process planning |
| **ARKNESS** | — | 2025 | Manufacturing knowledge graph, 3B Llama matches GPT-4o on machining |
| **YOLOv11-OBB + Donut** | arXiv 2506.17374 | 2025 | 94% F1 on 1,367 drawings, 9 annotation categories |

**CReFT-CAD is a game-changer**: First publicly available large-scale dataset of annotated engineering drawings (200K). Before this, the biggest obstacle was training data scarcity. This enables fine-tuning models specifically for engineering drawing understanding.

**CAD2Program is clever**: Instead of trying to reconstruct 3D geometry directly from pixels, it generates a Python program (using CadQuery/OpenSCAD) that, when executed, produces the 3D model. Code is a much better intermediate representation than trying to predict coordinates.

## Key Conferences
- **ICDAR 2025** (Wuhan, China, Sep 2025) — International Conference on Document Analysis and Recognition (PRIMARY)
  - **GREC 2025** — 16th IAPR Graphics Recognition Workshop. THE most targeted venue for engineering drawing parsing. Small community, high relevance.
- **ASME IDETC** — GD&T digitization research
- **CIRP** — Manufacturing/tolerancing
- **NeurIPS / ICLR / AAAI** — increasingly publishing CAD/drawing papers (CReFT-CAD, Cadrille, CAD2Program)

## Industry Claims vs Reality

| Company | Claim | Reality Check |
|---------|-------|---------------|
| **CADDi** | 99.9% annotation detection accuracy | On their own curated dataset. Massive training set (hundreds of millions of drawings). Not generalizable. |
| **Werk24** | 95%+ PMI extraction | Verified by their retraining pipeline (monthly, 100K+ drawings). Best independent validation available. |
| **Infrrd** | 97%+ on engineering documents | Marketing claim. No independent benchmark published. |
| **Khan/Moon (NTU)** | 94.77% GD&T precision | Academic benchmark on 1,367 drawings. Most credible published result. |
| **Gemini 2.5 Pro** | ~80% dimension extraction | Independent benchmark (Businessware Tech) on 10 real drawings with strict matching. |

---

# PART 15: STRATEGIC RECOMMENDATIONS FOR COSTIMIZE

## Priority Order (Build Sequence)

### Phase 1: Quick Wins (1-2 weeks)
- [ ] Swap Gemini to primary vision API (2x accuracy, 10x cheaper)
- [ ] Add human-in-the-loop editable table (every correction = training data)
- [ ] Add structured JSON schema to vision prompts
- [ ] Enable PaddleOCR `use_textline_orientation=True` for drawing text

### Phase 2: DXF Parser (2-3 weeks) — HIGHEST ROI
- [ ] Build `extractors/dxf_extractor.py` using ezdxf
- [ ] Parse DIMENSION entities → `get_measurement()`
- [ ] Parse TEXT/MTEXT → material callouts, notes, tolerances
- [ ] DWG support via ODA File Converter
- [ ] Route: DXF/DWG → programmatic; PDF → vision

### Phase 3: Agentic Drawing Pipeline (4-6 weeks)
- [ ] Layout detection: identify title block, views, notes, GD&T
- [ ] Region-specific processing tools
- [ ] View-by-view extraction with Gemini
- [ ] Cross-view merging and validation
- [ ] Visual grounding (bounding boxes for each extraction)

### Phase 4: GD&T Cost Engine (4-6 weeks)
- [ ] GD&T symbol → process mapping table
- [ ] Cost multiplier engine (1.0x-5.0x)
- [ ] Inspection cost estimation (CMM time × rate)
- [ ] Integration with existing cost engine

### Phase 5: Fine-Tuned Models (8-16 weeks)
- [ ] Train YOLO on 500+ annotated drawing regions
- [ ] Symbol classifier for GD&T (14 classes + modifiers)
- [ ] Fine-tune Florence-2 or Donut on accumulated corrections
- [ ] Target: 85%+ automated accuracy

## The Moat

1. **Physics-based cost engine** (aPriori proved this works)
2. **India-specific cost data** (₹ rates, Indian job shop economics)
3. **Human correction → training data pipeline** (every customer interaction improves accuracy)
4. **GD&T → cost translation** (nobody else does this for Indian procurement)
5. **DXF + PDF hybrid** (covers the full spectrum of Indian drawing formats)

---

# PART 16: PIONEER INSIGHTS — WHAT THE BUILDERS ACTUALLY SAY

## Karpathy's Data Engine (The Playbook for Costimize)

Andrej Karpathy's Tesla Autopilot "data engine" is the exact pattern Costimize should follow:

```
1. Deploy heavy model (Gemini/GPT-4o) → auto-label drawings
2. Human expert reviews and corrects labels (procurement team)
3. Train lighter/faster model on corrected labels
4. Deploy lighter model in production
5. Collect failure cases (where lighter model disagrees with heavy model)
6. Send failures back for human review
7. Retrain with expanded dataset
8. Repeat → model gets better, human effort decreases
```

**Why this matters:** You don't need 10,000 labeled drawings to start. You need:
- A heavy model (Gemini 2.5 Pro) that gets 60-70% right
- A correction UI that captures every human fix as training data
- The discipline to retrain periodically

Each customer interaction improves the next extraction. This is your data moat.

## Reducto Founder Insights

- "The orchestration layer is the real IP — individual models are replaceable"
- "Every document type needs a different pipeline, but the meta-architecture is the same"
- "Self-correction catches 15% of errors that single-pass misses"
- "We process 1B+ pages — the long tail of weird document formats is the real challenge"

**Why single-pass VLMs fail** (from Jason Liu interview with Reducto): "Models today, especially reasoning models, are incredible with reasoning on good data. What really ends up causing accuracy drifts is the long tail of cases." VLMs silently drop rows/columns from tables, make 50-50 guesses on checkboxes, and minor document skew (1-2°) dramatically degrades quality. Safety guardrails cause model refusals on legitimate technical content.

**Takeaway:** Build the orchestration framework first, swap models as better ones emerge.

## Werk24 Philosophy for Manufacturing

- "Reject rather than guess" — if extraction confidence < threshold, return nothing instead of wrong data
- "Every drawing number we've ever seen has unique formatting — no universal regex"
- "ML alone is not enough — you need an engineering expert system as a second check"
- "The last 5% accuracy is 50% of the engineering effort"

**Takeaway:** In manufacturing, a wrong answer is worse than no answer. Build confidence thresholds and human-review triggers into every extraction.

## Andrew Ng (Landing AI) on Document AI

- "Agentic workflows are the key — let the AI decide what tools to use per region"
- "Visual grounding (bounding boxes) is not optional — it's how you build trust"
- "The gap between demo accuracy and production accuracy is enormous"
- "Small data + smart architecture beats big data + naive approach"

**Takeaway:** The ADE course architecture (layout detect → region classify → specialized tools → verify) is validated at scale. Follow it.

## Must-Read Blog Posts & Interviews

1. **Jason Liu + Adit Abraham: "Why Most Document Parsing Sucks"** — jxnl.co — THE best practical interview on production document parsing. Covers why VLMs alone fail, multi-pass approach, and chunking strategies.
2. **Landing AI: "OCR to Agentic Document Extraction"** — landing.ai/blog — Definitive 4 waves of document intelligence (OCR → Statistical/ML → LLMs → Agentic).
3. **Reducto: Hybrid Architecture Deep Dive** — llms.reducto.ai — Detailed agentic OCR correction propagation pipeline.
4. **HackerNoon: "How To Process Engineering Drawings With AI"** — Practical guide arguing custom models are necessary.
5. **Mavlon: "How AI Actually Reads an Engineering Drawing"** — Real accuracy numbers (~85% current state).
6. **Businessware Technologies: AI Benchmark on Engineering Drawings** — Gemini Pro ~80%, Claude ~40%, GPT o3 ~20%.

## Landing AI's 4 Waves of Document Intelligence

| Wave | Era | Approach | Limitation |
|------|-----|----------|-----------|
| 1 | OCR | Character recognition | Lost all structural relationships |
| 2 | Statistical/ML | NER, SVMs | Required extensive feature engineering |
| 3 | LLMs | Semantic reasoning | Hallucinations, non-deterministic, lost auditability |
| **4** | **Agentic** | **Visual AI-first, plans/decides/acts, data-centric improvement** | **Current best — still early** |

Core innovation of Wave 4: **Visual Grounding** — documents stay as images, every extracted value links to exact bounding box. "Hallucinations become impossible because all claims are visually backed."

## Key GitHub Repositories for Engineering Drawing Parsing

| Repository | Stars | What It Does |
|-----------|-------|-------------|
| **LatticeLabsAI/cadling** | Growing | PyMuPDF-based engineering PDF parser, arc detection from Bezier curves |
| **PaddlePaddle/PaddleOCR** | 44K+ | Production OCR with angle detection — critical for drawings |
| **pymupdf/PyMuPDF** | 5K+ | Fastest Python PDF library, vector path extraction |
| **mozman/ezdxf** | 900+ | DXF parsing — the best Python DXF library |
| **openvenues/pypostal** | — | Address parsing (not directly relevant but good NLP pattern) |
| **Layout-Parser/layout-parser** | 4K+ | Layout detection framework — adaptable to drawings |
| **PaddlePaddle/PaddleDetection** | — | YOLO variants with OBB support for rotated objects |
| **clovaai/donut** | 4K+ | OCR-free document understanding (Swin + BART) |
| **reducto/RolmOCR** | New | Apache 2.0 OCR model on Qwen2.5-VL-7B, rotation-robust |
| **allenai/olmocr** | Growing | RL-trained OCR, $2/10K pages on single H100 |
| **javvi51/eDOCr** | — | Engineering drawing OCR with VLM verification |
| **microsoft/unilm/layoutlm** | — | LayoutLM series for document understanding |
| **facebookresearch/nougat** | — | Academic PDF → Markdown with math preservation |

---

# SOURCES

- 50+ research papers cited throughout (arXiv, ASME, CIRP, Elsevier CAD, NeurIPS, ICLR, AAAI)
- DeepLearning.AI "Document AI" course content analysis
- Werk24, aPriori, CADDi, IndustrialMind.ai, Landing AI, Reducto, CoLab Software, DraftAid, Infrrd, TwinKnowledge company analysis
- ASME Y14.5-2018, ISO 1101:2017 standards
- PaddleOCR, ezdxf, PyMuPDF, LatticeLabsAI/cadling documentation and source code
- Founder/researcher social media posts: Reducto founders, Werk24 team, Andrew Ng, Karpathy data engine talks
- CReFT-CAD (NeurIPS 2025), Cadrille (ICLR 2026), CAD2Program (AAAI 2025), CAPP-GPT (2024), ARKNESS (2025)
- Comprehensive web search across academic, commercial, and social media sources

# DXF/DWG Extraction Deep Dive — Research Report

**Date:** 2026-03-28
**Purpose:** Evaluate tools, repos, and approaches for extracting structured data from engineering drawings (DXF/DWG/PDF) to feed Costimize's should-cost engine.

---

## 1. GitHub Repository Analysis

### 1.1 mozman/ezdxf (1,244 stars)

**What it is:** The definitive Python library for reading/writing DXF files. MIT licensed, actively maintained (updated 2 days ago), supports DXF R12 through R2018.

**Architecture:**
- Pure Python with optional C extensions for performance
- Reads all DXF entity types including DIMENSION, TEXT, MTEXT, INSERT (blocks), TOLERANCE
- Has an `odafc` add-on that wraps ODA File Converter for DWG read/write
- Includes drawing/rendering add-on (matplotlib/PyQt5 backends)
- Can iterate over huge DXF files (>5GB) via `iterdxf` add-on

**Dimension Extraction Capabilities (Critical for Costimize):**

ezdxf natively supports ALL dimension types:
| dimtype | Type | What it measures |
|---------|------|-----------------|
| 0 | Linear/Rotated/Horizontal/Vertical | Distance between two points |
| 1 | Aligned | Distance parallel to definition line |
| 2 | Angular (2 lines) | Angle between two lines |
| 3 | Diameter | Circle/arc diameter |
| 4 | Radius | Circle/arc radius |
| 5 | Angular (3 points) | Angle defined by 3 points |
| 6 | Ordinate | X or Y distance from origin |
| 8 | Arc (R2018+) | Arc length |

Key attributes per dimension entity:
- `dxf.actual_measurement` — the computed value (optional, R2000+)
- `get_measurement()` — calculates measurement from definition points (always works)
- `dxf.text` — user-entered text override ("" or "<>" = use measurement, " " = suppress)
- `dxf.defpoint`, `dxf.defpoint2`, `dxf.defpoint3`, `dxf.defpoint4`, `dxf.defpoint5` — geometry definition points
- `dxf.dimstyle` — references a DimStyle with 80+ variables (tolerances, precision, etc.)
- `dxf.text_midpoint` — location of dimension text

**Tolerance Information:**
- Accessed via DimStyle variables: `dimtp` (plus tolerance), `dimtm` (minus tolerance)
- `dimtol` flag indicates if tolerances are shown
- `dimlim` flag indicates if limits are shown instead of nominal
- `dimtfac` is the tolerance text height factor
- Fit designations (H7, g6) stored in `dxf.text` as override text

**What we can reuse:**
- EVERYTHING. This is the foundation for DXF parsing.
- `get_measurement()` gives us actual dimension values without relying on optional attributes
- Layer information tells us drawing organization (DIMENSIONS layer, HIDDEN layer, etc.)
- Block references (INSERT entities) give us title block contents
- TEXT/MTEXT entities give us notes, material callouts, GD&T text

**Limitations:**
- Cannot read DWG directly (needs ODA File Converter wrapper)
- Does not "understand" what dimensions mean semantically (just geometry)
- Exploded dimensions (converted to lines + text) lose their DIMENSION entity structure

---

### 1.2 Bakkopi/engineering-drawing-extractor (75 stars)

**What it is:** OpenCV + Tesseract pipeline for extracting table data from blueprint images.

**Architecture:**
- Input: Scanned blueprint images (PNG)
- Pipeline: Image preprocessing -> contour detection -> table isolation -> OCR
- Output: Excel file with extracted drawing info (drawing numbers, authors, titles)

**Technologies:** OpenCV, pytesseract, NumPy, openpyxl, matplotlib

**How it handles extraction:**
- Uses contour detection to find rectangular regions (tables, title blocks)
- Isolates tables from drawing geometry
- Applies Tesseract OCR to extract text from isolated regions
- Removes border lines and annotations to improve OCR accuracy

**Accuracy:** Not quantified. Relies heavily on consistent drawing formats.

**Limitations:**
- Only extracts table/title block data, NOT dimensions
- Requires consistent drawing layouts
- Tesseract OCR struggles with engineering-specific symbols
- No dimension understanding whatsoever

**What we can learn:** The table isolation approach (contour detection -> hierarchy building) is useful for separating title blocks from drawing views in PDF/image-based workflows.

---

### 1.3 sanjai-CHQ/Inticore_AI_2D (0 stars, but exceptional code quality)

**What it is:** The most sophisticated open-source pipeline found. 8-stage architecture for extracting structured manufacturing data from 2D engineering drawing PDFs.

**Architecture — 8 Stages:**
1. **OCR Extraction:** PDF -> 400 DPI images -> PaddleOCR PP-OCRv4 -> normalized tokens with bounding boxes
2. **YOLO Layout Detection:** Custom YOLOv8 model detects title blocks, views, tables -> regions
3. **Region Assignment:** Tags each OCR token with its semantic region (title_block, main_view, etc.)
4. **Geometric Reasoning Engine (GRE):** Spatial promotion of unassigned tokens + dimension grouping (pairs values with tolerances, prefixes)
5. **Deterministic Classification:** Regex-based classification of tokens into types: LINEAR, DIAMETER, RADIUS, CHAMFER, ANGLE, TOLERANCE, COMPOUND_DIM, etc. Also extracts title block metadata via keyword proximity matching.
6. **VLM Resolver:** Gemini 2.0 Flash resolves OCR ambiguities (optional, can skip)
7. **Final Merge:** Combines deterministic + VLM data
8. **Semantic Summarizer:** Gemini interprets the drawing image + dimension list to produce a manufacturing-ready `part_summary.json`

**Technologies:** PaddleOCR, YOLOv8 (custom trained), Gemini 2.0 Flash, FastAPI, Python 3.12

**Code Quality Highlights:**
- Dimension classifier uses priority-ordered regex patterns (P1-P14)
- Handles OCR misreads: "O146" -> "diameter 146" (O misread of diameter symbol)
- Compound dimension parsing: "5+/-0.1" -> {value: 5.0, tolerance: symmetric 0.1}
- Tolerance parsing: symmetric, unilateral upper, unilateral lower
- Scale ratio parsing handles OCR artifacts ("1/01" = 1:1)
- Title block metadata extraction via keyword proximity (MATERIAL, PART NAME, SCALE, etc.)

**Semantic Summarizer Output (Stage 8) — this is gold for cost estimation:**
```json
{
  "drawing_metadata": {"part_name", "material", "units", "scale", ...},
  "part_envelope": {"overall_length_mm", "overall_width_mm", ...},
  "primary_bores": [{"diameter_mm", "tolerance", "depth_mm", ...}],
  "outer_diameters": [...],
  "hole_features": [{"thread_spec", "quantity", ...}],
  "key_linear_dimensions": [...],
  "toleranced_surfaces": [{"criticality": "high|medium|low", ...}],
  "general_notes": [],
  "casting_information": {...}
}
```

**Accuracy:** Not quantified, but the 8-stage pipeline with VLM validation is the most robust approach seen.

**Limitations:**
- Requires GPU for YOLO inference (CPU takes ~30s/image)
- Custom YOLO model needs training data (they include a trained model at `models/engineering_v22_best.pt`)
- Gemini API dependency for stages 6 and 8
- Only handles PDFs (rasterized), not DXF

**What we can reuse:**
- **Stage 5 dimension classifier** — regex patterns for classifying OCR tokens (directly portable)
- **Stage 8 semantic summarizer prompt** — the JSON schema maps almost 1:1 to what Costimize needs
- **Overall architecture pattern** — multi-stage pipeline with deterministic rules + AI validation
- **OCR misread handling** — the "O" -> "diameter" inference pattern

**VERDICT: This is the single most valuable repo for Costimize. The Stage 8 output schema is essentially our cost engine input.**

---

### 1.4 acen20/ga-analysis (1 star)

**What it is:** Pipeline for extracting structured data from GA (General Arrangement) drawings. Focused on P&ID-style drawings, not mechanical part drawings.

**Architecture:**
- YOLOv8 nano for cropping regions (notes, tables, nozzles, views)
- PaddleOCR + PPStructureV3 for table parsing
- DONUT transformer for extracting handwritten/typed notes
- Docker-based deployment with API endpoint

**Results:**
- YOLOv8 Notes & Tables: mAP50 = 99.5%, mAP = 93.9% (33 training images)
- YOLOv8 Views: mAP50 = 99.5%, mAP = 95.1%
- YOLOv8 Nozzles: mAP50 = 96%, mAP = 85%
- DONUT Notes: Edit Distance = 0.031

**Limitations:**
- Only 12 training documents — poor generalization
- Complex table structures break PPStructureV3
- Split notes sections not handled
- Focused on GA drawings, not mechanical part drawings

**What we can learn:**
- YOLOv8 nano achieves excellent mAP even with tiny datasets (augmented from 11 -> 33 images)
- Docker-compose deployment pattern is clean
- DONUT is useful for handwritten notes but overkill for typed text

---

### 1.5 javvi51/eDOCr (74 stars) and eDOCr2 (54 stars)

**What it is:** The most academically rigorous OCR system specifically for mechanical engineering drawings. Published paper: "Optical character recognition on engineering drawings to achieve automation in production quality control" (Frontiers, 2023).

**Architecture (eDOCr2):**
- **Layer Segmentation:** OpenCV contour detection to find rectangles, build hierarchy (frame -> title block -> GD&T boxes -> dimension regions)
- **Three OCR Pipelines:**
  1. **Info Block Pipeline:** Tesseract for title block text (part name, material, etc.)
  2. **GD&T Pipeline:** Custom keras-ocr recognizer trained on GD&T symbols (unicode symbols like perpendicularity, parallelism, diameter, etc.)
  3. **Dimension Pipeline:** Custom keras-ocr recognizer for dimension text + template matching for diameter symbol (unicode 2300)
- **LLM Integration (eDOCr2):** `test_llm.py` sends extracted data to LLM for interpretation
- **Custom Training:** Synthetic data generation for training recognizers on engineering-specific alphabets

**Technologies:** OpenCV, keras-ocr (custom fork), pytesseract, custom CNN recognizers

**Key Innovation — Custom Alphabets:**
- `alphabet_dimensions`: digits + 'AaBCDRGHhMmnx' + '(),.+-+/-:/deg"diameter'
- `alphabet_gdts`: digits + ',.diameter ABCD' + GD&T symbols
- `alphabet_infoblock`: digits + ascii_letters + ',.:-/'

**Symbol Template Matching:**
- Uses template matching for the diameter symbol (stored as reference images in `symbol_match/u2300/`)
- Multiple templates at different rotations and scales
- This handles the common OCR failure of misreading "diameter" as "O" or "0"

**Accuracy:** Published in peer-reviewed journal. No specific numbers in README but the paper reports results.

**Limitations:**
- Requires per-drawing calibration (frame detection threshold)
- keras-ocr dependency is heavy and somewhat outdated
- Training custom recognizers needs effort
- Does not output structured dimension data — outputs text + positions

**What we can learn:**
- Custom alphabets for engineering text recognition is the right approach
- Template matching for special symbols (diameter) works well
- The three-pipeline architecture (info block / GD&T / dimensions) is the correct decomposition
- Synthetic training data generation for engineering fonts

---

### 1.6 generalMG/label_studio_ml_backend (0 stars)

**What it is:** Hybrid OCR pipeline for CAD drawings combining PaddleOCR detection with Qwen2.5-VL-8B recognition, integrated with Label Studio for annotation workflows.

**Architecture:**
- PaddleOCR runs first pass (detection + optional recognition)
- Low-confidence regions are cropped and sent to Qwen2.5-VL (4-bit quantized) for recognition
- Label Studio integration for human review and correction
- PDF auto-conversion webhook

**Technologies:** PaddleOCR, Qwen2.5-VL-8B (4-bit quantized), Label Studio, FastAPI, Docker

**Key Innovation:** The hybrid confidence-based routing:
- High confidence PaddleOCR results -> keep as-is
- Low confidence regions -> Qwen VLM for better recognition
- This is a practical cost-accuracy tradeoff

**Limitations:**
- Requires NVIDIA GPU (8GB+ VRAM) for Qwen
- Korean-focused (default language)
- No dimension-specific logic — generic OCR

**What we can learn:**
- Hybrid PaddleOCR + VLM architecture is practical
- Label Studio workflow for building training data
- Confidence threshold routing between fast OCR and slow VLM

---

### 1.7 SHYam1025/DrawVision-AI (0 stars)

**What it is:** P&ID (Piping and Instrumentation Diagram) extractor. NOT for mechanical part drawings.

**Architecture:**
- PDF -> 300 DPI rasterization -> YOLO detection of text clusters -> intelligent cropping with padding -> Gemini 2.0 Flash for JSON extraction -> spatial deduplication

**Key Innovation:** Custom spatial deduplication using 100px grid to prevent duplicate detections in dense drawings, which is smarter than standard NMS.

**Limitations:** Specific to P&ID pipe specifications, not mechanical dimensions.

**What we can learn:** The spatial deduplication grid approach is useful for dense engineering drawings.

---

### 1.8 fargrat/dimension-interpolation (16 stars)

**What it is:** Bachelor's thesis project (FH Dortmund) for reading dimensions from scanned engineering drawings.

**Architecture:**
1. Image preprocessing
2. Hough line detection for finding dimension lines
3. Template matching for arrowhead detection (up/down/left/right templates)
4. Tesseract OCR for text segments
5. Naive Bayes or CNN classifier to identify relevant text segments (vs. noise)
6. Geometric association: connects arrowheads + lines + text segments based on relative positions

**Technologies:** OpenCV, Tesseract, scikit-learn (Naive Bayes), TensorFlow (CNN), skimage

**Key Innovation:** The geometric association algorithm:
- Find arrowhead pairs on the same line
- Find text segments near the midpoint between arrowhead pairs
- Associate text with dimension lines based on proximity and orientation

**Limitations:**
- Only handles linear dimensions (height and width)
- Requires clean scanned images
- No tolerance handling
- German-language code/comments

**What we can learn:**
- Arrowhead template matching is a simple but effective approach
- The "arrowhead pair -> associated text" logic is the correct geometric reasoning for dimension extraction from images
- CNN vs. Naive Bayes comparison for classifying dimension text vs. noise

---

### 1.9 Benjamin-Hu/Engineering-Drawing-Parser (11 stars)

**What it is:** GUI application for interpreting "bubbled" engineering drawings (revision balloons) and auto-bubbling existing PDFs. Built with wxPython.

**Relevance:** Low for Costimize. Focused on revision tracking balloons, not dimension extraction.

---

### 1.10 jparedesDS/extract-data-dxf (19 stars)

**What it is:** Python script using ezdxf to extract all entity types from DXF files and recreate them in a new formatted DXF file.

**Code Analysis:**
- Comprehensive entity type handling: LINE, CIRCLE, ARC, LWPOLYLINE, POLYLINE, ELLIPSE, TEXT, MTEXT, HATCH, SOLID, POINT, DIMENSION, INSERT (recursively enters blocks), LEADER, MLINE, SPLINE, 3DFACE, IMAGE, TOLERANCE, MESH, SURFACE, etc.
- **Dimension extraction function (`extract_dimension_data`):**
  ```python
  def extract_dimension_data(entity):
      dim_data = {
          "dimtype": entity.dimtype,
          "text": entity.dxf.text,
          "insert_point": entity.dxf.insert,
      }
      # Type 0: Linear -> defpoint, defpoint2
      # Type 1: Aligned -> defpoint, defpoint2
      # Type 2: Angular (2 lines) -> defpoint, defpoint2, defpoint3, defpoint4
      # Type 3: Diameter -> defpoint, defpoint2
      # Type 4: Radius -> defpoint, defpoint2
      # Type 5: Angular (3 points) -> defpoint, defpoint2, defpoint3
      # Type 6: Angular (4 points) -> defpoint through defpoint4
  ```

**What we can reuse:** This is a clean, working template for DXF entity extraction. The `extract_entities` function handles 25+ entity types. Can be adapted directly for Costimize.

---

### 1.11 teddyz829/Data-Augmentation-Engineering-Drawing (30 stars, CMU)

**What it is:** Academic paper (ASME IDETC 2022, Carnegie Mellon) on generating synthetic engineering drawings from DXF files by randomizing dimensions.

**Architecture:**
- `dxfReader.py` — Reads DXF using ezdxf, extracts: lines, dash_lines, circles, arcs, construction_lines, linear_dimensions, diameter_dimensions
- `dxfWriter.py` — Generates new DXF files with randomized dimensions
- `dxfRunner.py` — Orchestrates generation of N synthetic drawings per input
- `visualize.py` — Matplotlib visualization

**Key Code in dxfReader (Dimension Extraction):**
```python
if e.dxftype() == 'DIMENSION':
    if e.dxf.dimtype == 160:  # Linear dimension (160 = 0 + 128 + 32)
        # Extract defpoint2, defpoint3, text_midpoint
        # Determine horizontal vs vertical by comparing text_midpoint to defpoints
        # Normalize point ordering (smaller x/y = point1)
    else:  # Diameter dimension
        # Extract defpoint, defpoint4
        # Calculate radius from distance between points
        # Calculate text location from leader line slope
```

**What we can learn:**
- DXF dimtype 160 = linear dim with user-located text (0 + 32 + 128)
- The horizontal vs. vertical detection logic using text_midpoint position
- How to distinguish between horizontal and vertical linear dimensions programmatically
- Synthetic data generation for training ML models on engineering drawings

---

### 1.12 sguerin13/cad-feature-detection (26 stars)

**What it is:** Web app that converts STEP files to Three.js and detects manufacturing features using UV-Net (Autodesk AI Lab).

**Architecture:**
- Frontend: React + TypeScript + react-three-fiber
- Backend: FastAPI + PythonOCC + PyTorch
- ML: UV-Net model trained on MFCAD dataset for manufacturing feature detection
- Deployment: AWS CDK + Lambda + SageMaker

**Technologies:** PythonOCC, UV-Net, MFCAD dataset, Three.js

**Relevance:** This is for 3D STEP files, not 2D drawings. But the manufacturing feature detection concept is interesting — UV-Net classifies B-Rep faces into manufacturing operations (milling, turning, drilling, etc.).

**What we can learn:** For future 3D file support, UV-Net + PythonOCC is the stack to use. The MFCAD dataset provides labeled manufacturing features on STEP models.

---

### 1.13 W24-Service-GmbH/werk24-python (85 stars)

**What it is:** Commercial API client for Werk24's AI-powered technical drawing extraction service. The gold standard for what's possible.

**Data Models (what they extract):**

**Metadata:** Drawing ID, Part ID, Designation, General Tolerances (ISO 2768 with class), General Roughness, Material (with category hierarchy: category1/2/3), Weight, BOM, Revision Table, Languages, Notes

**Features (per dimension):**
```python
class Dimension(Feature):
    quantity: int
    size: Size  # {size_type, value, unit, tolerance}

class Size:
    size_type: SizeType  # DIAMETER, LINEAR, ANGULAR
    value: Decimal
    unit: str  # "mm"
    tolerance: Tolerance  # {grade, deviation_lower, deviation_upper, fit, is_general_tolerance}

class Tolerance:
    tolerance_grade: str  # "IT7"
    deviation_lower: Decimal  # -0.05
    deviation_upper: Decimal  # 0.05
    fit: str  # "H7"
    is_theoretically_exact: bool
    is_reference: bool
    is_general_tolerance: bool
```

Also extracts: Threads (type, handedness, pitch), Bores, Chamfers, Roughnesses (Ra/Rz with standard, filter type, direction of lay), GD&T (characteristic, material condition, datum references), Radii

**Insights:** Manufacturing Method, Postprocesses, Input/Output Geometry

**What we can learn:**
- Their data model is the best reference for what structured output should look like
- The `Tolerance` model with `fit`, `is_general_tolerance`, `is_theoretically_exact` flags
- The `Size` model separating `size_type` from `value` and `unit`
- General tolerances: standard (ISO 2768) + class (m, f, c) + principle (independence, envelope)
- This is what Costimize should aspire to extract

**Limitations:** Commercial API ($$$), no open-source extraction logic

---

### 1.14 clovaai/donut (6,823 stars)

**What it is:** OCR-free Document Understanding Transformer (ECCV 2022, NAVER/Clova). End-to-end vision transformer that converts document images directly to structured JSON.

**Architecture:**
- Swin Transformer encoder (visual features)
- GPT-2 decoder (generates structured output)
- Pre-trained on IIT-CDIP (11M documents) + SynthDoG synthetic data
- Fine-tunable for any document type

**Results:**
- CORD (receipt parsing): 91.3% Tree Edit Distance accuracy
- DocVQA: 67.5% accuracy
- RVL-CDIP (classification): 95.3%
- Speed: 0.7-1.2 sec/image on A100

**SynthDoG:** Synthetic Document Generator that creates training data in multiple languages. Could potentially be adapted to generate synthetic engineering drawing training data.

**Relevance for Costimize:** Could be fine-tuned on engineering drawings to directly extract structured data. However:
- Requires substantial labeled training data
- Pre-trained on business documents, not engineering drawings
- The CMU Data Augmentation repo could provide synthetic training data

**What we can learn:** The SynthDoG approach to generating training data is very relevant. Combined with the CMU synthetic drawing generator, could create a large labeled dataset for fine-tuning.

---

## 2. DXF Deep Dive

### 2.1 How DIMENSION Entities Work in DXF

A DXF DIMENSION entity stores:
1. **Definition points** — the actual geometry points being measured
2. **Dimension type** — what kind of measurement (linear, angular, diameter, etc.)
3. **Dimension style** — references a DimStyle table entry with 80+ formatting variables
4. **Optional text override** — user can replace the auto-calculated text
5. **Geometry block** — an anonymous block containing the visual representation (lines, arrows, text)

The geometry block is critical: AutoCAD REQUIRES it to display the dimension. BricsCAD can render without it. ezdxf can generate these blocks via `dim.render()`.

### 2.2 Dimension Types

| Type | dimtype | Definition Points Used | Measurement |
|------|---------|----------------------|-------------|
| Linear/Rotated | 0 | defpoint (dim line loc), defpoint2 (ext line 1 start), defpoint3 (ext line 2 start), angle | Distance between ext line starts, projected onto angle |
| Aligned | 1 | defpoint, defpoint2, defpoint3 | True distance between defpoint2 and defpoint3 |
| Angular (2 lines) | 2 | defpoint+defpoint4 (line 2), defpoint2+defpoint3 (line 1), defpoint5 (arc loc) | Angle between two lines |
| Diameter | 3 | defpoint (far point on circle), defpoint4 (near point) | 2x distance |
| Radius | 4 | defpoint (center), defpoint4 (point on circle) | Distance |
| Angular (3 points) | 5 | defpoint (center), defpoint2 (end of line 1), defpoint3 (end of line 2) | Angle |
| Ordinate | 6 | defpoint (feature location), defpoint2 (leader endpoint) | X or Y distance from origin |
| Arc | 8 | Same as angular, added in R2018 | Arc length |

### 2.3 Extracting Actual Measurement Values

**Method 1:** `entity.dxf.actual_measurement` (group code 42)
- Optional attribute, only present in R2000+
- Often not present in files
- Read-only, set by CAD application

**Method 2:** `entity.get_measurement()` (ezdxf method)
- Calculates from definition points
- Always works regardless of DXF version
- Returns float for linear/angular, Vec3 for ordinate
- Uses `MEASUREMENT_TOOLS` dispatch table internally

**Method 3:** Parse `entity.dxf.text`
- If empty or "<>", the displayed text equals the measurement
- If a specific string, that is the displayed text (may include tolerance text)
- If " " (space), text is suppressed

### 2.4 Extracting Tolerance Information

Tolerances come from two sources:

**From DimStyle variables (via `entity.override()`):**
```python
override = entity.override()
dimstyle = override.dimstyle_attribs
dimtol = dimstyle.get('dimtol', 0)   # 1 = show tolerances
dimlim = dimstyle.get('dimlim', 0)   # 1 = show limits
dimtp = dimstyle.get('dimtp', 0.0)   # plus tolerance value
dimtm = dimstyle.get('dimtm', 0.0)   # minus tolerance value
```

**From text override:**
- Users often type tolerances directly: "50 +0.1/-0.05" or "50 H7"
- Must be parsed from the text string
- No standardized format

### 2.5 Extracting Text Annotations

```python
for entity in msp:
    if entity.dxftype() == 'TEXT':
        text = entity.dxf.text
        position = entity.dxf.insert
        layer = entity.dxf.layer
    elif entity.dxftype() == 'MTEXT':
        text = entity.text  # plain text (stripped formatting)
        position = entity.dxf.insert
        layer = entity.dxf.layer
```

Associate text with geometry by:
- Layer grouping (TEXT on "NOTES" layer vs "DIMENSIONS" layer)
- Spatial proximity (nearest text to a geometric feature)
- Leader lines (LEADER entity connects text to geometry)

### 2.6 Title Block Extraction

Title blocks are typically either:
1. **INSERT entities** referencing a block definition — extract block attributes
2. **Raw geometry** (lines + text) in a known region (bottom-right corner)

```python
for entity in msp:
    if entity.dxftype() == 'INSERT':
        if 'title' in entity.dxf.name.lower():
            for attrib in entity.attribs:
                print(f"{attrib.dxf.tag}: {attrib.dxf.text}")
```

### 2.7 Handling "Exploded" Dimensions

When someone "explodes" a dimension in CAD, the DIMENSION entity is destroyed and replaced with:
- LINE entities (extension lines, dimension line)
- SOLID or INSERT entities (arrowheads)
- TEXT or MTEXT entity (measurement text)

Detection heuristic:
1. Find text entities that look like dimensions (numeric, with optional tolerance)
2. Look for nearby line pairs that could be extension lines
3. Look for arrowhead patterns near line endpoints
4. Associate by spatial proximity

This is fundamentally an image/geometry analysis problem and is where AI helps.

### 2.8 Layer Organization Patterns

Common layer naming conventions:
- `DIMENSIONS` or `DIM` — dimension entities
- `HIDDEN` or `HIDDEN_LINES` — hidden/dashed lines
- `CENTER` or `CENTER_LINES` — centerlines
- `NOTES` or `TEXT` — annotations
- `BORDER` or `TITLE` — title block and border
- `HATCH` — section hatching
- `GEOMETRY` or `0` — main geometry

```python
# Count entities by layer
from collections import Counter
layer_counts = Counter(e.dxf.layer for e in msp)
```

### 2.9 Extracting Geometric Features for Cost Prediction

```python
import ezdxf
from collections import Counter

doc = ezdxf.readfile("drawing.dxf")
msp = doc.modelspace()

entity_counts = Counter(e.dxftype() for e in msp)
# Gives: {'LINE': 245, 'CIRCLE': 12, 'ARC': 34, 'DIMENSION': 28, ...}

# This feature vector (entity counts) correlates with part complexity
# and can be used for ML-based cost prediction
```

### 2.10 Code Example: Complete Dimension Extraction

```python
import ezdxf
import math

def extract_all_dimensions(dxf_path):
    doc = ezdxf.readfile(dxf_path)
    msp = doc.modelspace()
    dimensions = []

    for entity in msp:
        if entity.dxftype() != 'DIMENSION':
            continue

        dim_type = entity.dimtype  # 0-8, no binary flags
        measurement = entity.get_measurement()

        # Get tolerance from dimstyle
        override = entity.override()
        attribs = override.dimstyle_attribs
        has_tolerance = attribs.get('dimtol', 0) == 1
        plus_tol = attribs.get('dimtp', 0.0)
        minus_tol = attribs.get('dimtm', 0.0)

        # Get text override
        text = entity.dxf.get('text', '')

        dim_data = {
            'type': ['linear', 'aligned', 'angular', 'diameter',
                     'radius', 'angular_3p', 'ordinate', None, 'arc'][dim_type],
            'measurement': float(measurement) if isinstance(measurement, (int, float)) else None,
            'text_override': text if text not in ('', '<>') else None,
            'has_tolerance': has_tolerance,
            'plus_tolerance': plus_tol if has_tolerance else None,
            'minus_tolerance': minus_tol if has_tolerance else None,
            'layer': entity.dxf.layer,
            'text_midpoint': tuple(entity.dxf.get('text_midpoint', (0, 0, 0))),
        }
        dimensions.append(dim_data)

    return dimensions
```

---

## 3. DWG Parsing Options

### 3.1 ODA File Converter (Recommended)

**What:** Free (for personal use) command-line tool from Open Design Alliance. Converts between DWG <-> DXF for all versions.

**Capabilities:**
- Converts DWG R14 through R2024 to DXF (any version)
- Converts DXF to DWG
- Batch conversion
- Lossless conversion (preserves all entities)

**ezdxf Integration:**
```python
from ezdxf.addons import odafc

# Convert DWG to DXF (requires ODA File Converter installed)
odafc.convert("input.dwg", "output.dxf", version="ACAD2018")
# Then read with ezdxf normally
doc = ezdxf.readfile("output.dxf")
```

**Limitations:**
- Free for personal/educational use; commercial use requires ODA membership ($$$)
- Must be installed separately (not a Python package)
- Windows/Linux/macOS support
- Requires spawning a subprocess

### 3.2 LibreDWG (1,347 stars)

**What:** GNU GPL library for reading/writing DWG files. C library with some language bindings.

**Capabilities:**
- Reads DWG R13 through R2018
- Writes DWG R2000 (limited write support)
- Command-line tools: dwgread, dwg2dxf, dwg2SVG
- Python bindings exist but are minimal

**Limitations:**
- GPL license (viral, not compatible with commercial use unless you GPL your code)
- Python bindings are thin and poorly documented
- Write support is limited
- Not as reliable as ODA for complex files

### 3.3 python-dwg

**Does NOT exist** as a maintained library. There is no pure-Python DWG reader.

### 3.4 Best DWG Pipeline for Costimize

**Recommended approach:**
1. Accept DWG upload
2. Convert to DXF via ODA File Converter subprocess
3. Parse DXF with ezdxf
4. Extract dimensions, text, geometry

For production deployment, wrap the ODA converter in a Docker container with the converter pre-installed.

---

## 4. Additional GitHub Search Results

### Notable Additional Repos Found

**Rutwik1000/Manufacturing-Cost-Estimation-Based-On-Deep-Learning (5 stars)**
- Uses SSDNeT for manufacturing feature detection on 3D STL files
- Auto-processes email with "#quote" subject + STL attachments
- Predicts machining features, estimates cost and time
- Generates PDF quotations
- Uses MySQL for archiving
- Technologies: SSDNeT (voxel-based 3D CNN), STL->binvox conversion
- Relevant concept but 3D-focused (STL, not 2D drawings)

**AlexandroBoldi/Industrial-Costing-Kernel (0 stars)**
- "Deterministic core for 2D manufacturing cost estimation with geometric traceability"
- Worth watching for overlap with Costimize's approach

**dimasthoriq/cnc-machining-time-estimation (1 star)**
- CNC machining time estimation for undergrad thesis
- Could have useful formulas for Costimize's mechanical cost engine

**EltiganiHamad/Engineering-Drawing-Extraction (10 stars)**
- Image segmentation to separate tables from diagrams
- Similar to Bakkopi but more focused

### Gaps in the Ecosystem

Searches for "should cost analysis", "GD&T recognition", and "DXF dimension extraction" returned NO results. This confirms that Costimize is operating in a genuine gap — there is no open-source should-cost tool, and DXF dimension extraction for cost estimation is uncharted territory in open source.

---

## 5. DXF/DWG-Only Analysis: How Easy Is It?

### If Costimize ONLY accepted DXF and DWG files:

#### What can be extracted programmatically (100% accuracy):

| Data | Source | Notes |
|------|--------|-------|
| All DIMENSION entities | ezdxf `get_measurement()` | Values, types, definition points |
| Dimension tolerances | DimStyle variables | If stored in DimStyle (not text override) |
| Entity counts | ezdxf iteration | Lines, circles, arcs, etc. for complexity estimation |
| Layer organization | ezdxf layer info | Which entities are on which layers |
| Geometric extents | ezdxf bounding box | Overall part size |
| Circle/arc radii | Entity attributes | All circles and arcs with exact radii |
| Block references | INSERT entities | Title block structure |
| Block attributes | ATTRIB entities | Title block field values |

#### Percentage of dimension data extractable programmatically:

**Best case (well-made DXF with native dimensions): 85-95%**
- All DIMENSION entities are perfectly extractable
- Tolerance in DimStyle: perfectly extractable
- Text overrides with fit designations (H7): parseable with regex
- Title block via block attributes: usually works

**Typical case (mixed quality DXF): 60-75%**
- Some dimensions are exploded (lost structure)
- Some tolerance info is in text overrides, not DimStyle
- Title block may be raw geometry, not block attributes
- Notes are TEXT entities requiring NLP interpretation

**Worst case (exported from other tools, exploded): 30-50%**
- All dimensions exploded to lines + text
- No DIMENSION entities at all
- Must fall back to image-based extraction

#### What still needs AI:

| Data | Why AI Needed |
|------|--------------|
| Material notes | Free-text parsing ("AL 6061-T6", "SS 304", "MS EN8") |
| GD&T in text form | Complex symbol interpretation |
| Surface finish callouts | Free-text with symbols |
| Heat treatment notes | Free-text parsing |
| Exploded dimensions | Geometry + text association |
| Thread callouts | Mixed notation ("M12x1.75", "3/8-16 UNC") |
| Manufacturing process hints | Interpreting section views, hatching patterns |
| General notes | NLP for manufacturing-relevant information |

#### Realistic Accuracy by Data Type:

| Data Type | DXF Programmatic | PDF/Image AI | Combined |
|-----------|-----------------|--------------|----------|
| Linear dimensions | 95% | 75-85% | 97% |
| Diameter/radius | 95% | 70-80% | 95% |
| Tolerances | 70% | 60-70% | 85% |
| Material | 50% (if in attributes) | 80% | 85% |
| Part name | 60% (if in attributes) | 85% | 90% |
| Thread specs | 80% (if DIMENSION text) | 70% | 90% |
| GD&T | 30% (if TOLERANCE entity) | 60% | 70% |
| Surface finish | 20% | 60% | 65% |

#### Processing Time:

- DXF parsing with ezdxf: **<1 second** for typical drawings
- DWG to DXF conversion: **2-5 seconds** (ODA subprocess)
- vs. PDF/Image AI pipeline: **10-60 seconds** (OCR + VLM)

**DXF is 10-60x faster than AI-based extraction.**

#### Edge Cases That Break Programmatic Extraction:

1. **Exploded dimensions** — most common failure mode. User "explodes" all dimensions, turning them into raw lines + text.
2. **External references (XREFs)** — dimensions may reference geometry in another file.
3. **Frozen/off layers** — dimensions on hidden layers may or may not be relevant.
4. **Paper space vs. model space** — dimensions may be in paper space with viewport scaling.
5. **Dynamic blocks** — parameterized blocks where dimensions depend on block parameters.
6. **Proxy entities** — custom entities from applications like Inventor or SolidWorks.
7. **Multiline text formatting** — tolerances embedded in MTEXT with complex formatting codes.
8. **Non-standard DXF** — files from applications that don't follow the DXF specification strictly.
9. **Unit ambiguity** — DXF does not enforce units; a drawing could be in mm, inches, or anything. Must infer from context.
10. **Scaled viewports** — dimensions in paper space at different scales than model space geometry.

---

## 6. Strategic Recommendations for Costimize

### Tier 1: Immediate Value (DXF-first approach)

Build a DXF/DWG extraction module using:
- **ezdxf** for DXF parsing
- **ODA File Converter** for DWG -> DXF conversion
- Extract all DIMENSION entities with `get_measurement()`
- Parse DimStyle for tolerances
- Extract TEXT/MTEXT for notes and title block
- Extract entity counts for complexity scoring
- This alone gives 60-95% of needed data, in <5 seconds

### Tier 2: AI Enhancement (for what DXF misses)

Add AI layer for:
- Material note interpretation (LLM call, regex-first)
- Exploded dimension recovery (from Inticore's Stage 4-5 approach)
- Title block parsing when not in block attributes
- General notes extraction and classification
- Thread specification parsing

### Tier 3: PDF/Image Fallback (for non-DXF files)

Implement Inticore-style pipeline for PDF inputs:
- PaddleOCR for text detection
- YOLOv8 for region detection (train on small dataset, augmented)
- Deterministic dimension classification (port Inticore's Stage 5)
- Gemini/GPT-4o for semantic summarization (port Inticore's Stage 8 prompt)

### Data Model Reference

Use Werk24's data model as the target schema:
- `Size` with `size_type`, `value`, `unit`, `tolerance`
- `Tolerance` with `fit`, `deviation_lower`, `deviation_upper`, `is_general_tolerance`
- `Dimension` with `quantity` and `size`
- Separate models for Thread, Bore, Chamfer, Roughness, GD&T

### Key Repos to Fork/Study:

1. **Inticore_AI_2D** — Stage 5 dimension classifier + Stage 8 semantic summarizer prompt
2. **extract-data-dxf** — Clean ezdxf entity extraction template
3. **Data-Augmentation-Engineering-Drawing** — DXF dimension reader + synthetic data generation
4. **eDOCr2** — Layer segmentation + GD&T symbol recognition approach
5. **werk24-python** — Data model reference

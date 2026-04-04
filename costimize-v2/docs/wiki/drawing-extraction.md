---
slug: drawing-extraction
title: How Newton-Metre Extracts Data from Engineering Drawings
keywords: drawing extraction, PDF parsing, DXF, DWG, STEP, OCR, GD&T, dimension detection, process callout, VLM, Qwen2.5-VL, two-stage extraction, Indian drawings, engineering drawings
sources: PDF-PARSING-DEEP-DIVE.md, dxf-extraction-deep-dive.md, cad-software-file-formats-by-country.md
updated: 2026-04-04
---

# How Newton-Metre Extracts Data from Engineering Drawings

Engineering drawings are the hardest document type to parse -- harder than financial documents, academic papers, or circuit schematics. They combine spatial semantics, specialized symbology (GD&T), multiple coordinate systems, no natural reading order, and information density 10x beyond any business document. Nobody has fully solved this -- not Google, not Microsoft, not any startup.

Newton-Metre does not need full 3D reconstruction (a 50+ year unsolved research problem). For cost estimation at +/-10% accuracy, bounding dimensions + feature list + tolerances + material is sufficient.

## Format Priority

| Priority | Format | Why | Status |
|----------|--------|-----|--------|
| P1 | **PDF** | Universal drawing format. Every procurement team sends PDFs. The contractual document. | Supported |
| P1 | **STEP (.stp/.step)** | Universal 3D exchange format. Enables exact geometry extraction without AI vision errors. | Roadmap |
| P2 | **DXF** | 2D drawing exchange. Dominant for sheet metal and laser cutting. Native parsing with ezdxf gives exact dimensions. | Roadmap |
| P2 | **DWG** | AutoCAD native format. Massive install base, especially in India. Requires ODA File Converter for reading. | Roadmap |
| P3 | **SLDPRT/SLDASM** | SolidWorks native. 13-14% global market share. Common in SME manufacturing. | Future |
| P3 | **IGES** | Legacy 3D exchange. Still sent by older shops. | Future |

### What Indian Job Shops Actually Receive

- **PDF drawings** -- the overwhelming majority. Printed or emailed.
- **DWG/DXF** -- from AutoCAD users. Common for sheet metal.
- **STEP files** -- from sophisticated OEMs and design houses.
- **Hand-drawn sketches or WhatsApp photos** -- many small shops work from these.

India's CAD market is $1,103M (14.25% of APAC). AutoCAD dominates for 2D drafting. SolidWorks is growing. BIS SP 46:2003 governs engineering drawing practices (1st angle projection mandatory since 1991).

## Native Parsing Over Rasterization

A core design principle: **never convert to image for extraction when native parsing is possible.**

- **DXF/DWG**: Parse entities with ezdxf (1,244 stars, MIT license). Extract exact dimension values via `get_measurement()`, tolerance information via DimStyle variables (`dimtp`, `dimtm`), layer information, and text annotations. DXF parsing is 10x easier than PDF vision.
- **STEP**: Parse geometry with PythonOCC/CadQuery. Extract bounding box, volume, surface area, face types (planar, cylindrical, conical), internal cylindrical faces (holes), edge count.
- **PDF**: Extract text with pdfplumber first. Rasterize to PNG (300+ DPI minimum, never JPEG) only as last resort for scanned PDFs.

## Two-Stage Extraction Pipeline

The extraction pipeline splits the AI workload to cut costs 50-80%:

**Stage 1: Text Extraction (GLM-OCR 0.9B)**
- Local or API, $0.03/M tokens
- Extracts raw text: dimension values, annotations, title block content, notes
- Fast, cheap, handles standard text well

**Stage 2: Engineering Context Interpretation (Gemini Flash)**
- Interprets engineering-specific content: GD&T symbols, process callouts, material specs
- Cross-references dimensions with features
- Maps tolerances to manufacturing implications
- GPT-4o as final fallback only

This mirrors the architecture of the most sophisticated open-source pipeline found (Inticore_AI_2D): OCR extraction, YOLO layout detection, region assignment, geometric reasoning, deterministic classification, VLM resolution, final merge, semantic summarization.

## What Gets Extracted

| Data | Source | Cost Engine Input |
|------|--------|-------------------|
| Overall dimensions (L x W x H or D x L) | Title block + outermost dimension lines | Stock material volume and weight |
| Material type | Title block annotation | Cost/kg, machinability index, cutting parameters |
| Feature list (holes, pockets, slots, threads) | Individual views, cross-referenced | Process time estimation per feature |
| Feature count | Count across all views | Setup time, tool changes |
| Tolerance requirements (+/- values, GD&T frames) | Dimension annotations, feature control frames | Tight tolerance surcharges (1.0x-5.0x multiplier) |
| Surface finish (Ra/Rz values) | Surface finish symbols | Finishing process selection and cost |
| Process callouts | Notes, annotations | Heat treatment, surface treatment, deburring |
| Thread specifications | Callout text (M10x1.5-6H) | Tapping time calculation |

## GD&T Extraction and Cost Mapping

Each of the 14 GD&T symbols maps to specific manufacturing processes with quantifiable cost multipliers:

- **Flatness** (1.1x-2.5x): Standard milling at >0.05mm, surface grinding at 0.01-0.05mm, lapping below 0.01mm
- **Position** (1.0x-3.0x): Standard CNC at >0.1mm, precision CNC at 0.025-0.1mm, jig boring below 0.025mm
- **Cylindricity** (1.3x-3.5x): CNC turning at >0.025mm, cylindrical grinding below 0.025mm, honing below 0.005mm
- **Total Runout** (1.3x-3.0x): Grinding between centers

GD&T cost formula: `GD&T_cost = base_machining_cost x process_upgrade_multiplier + inspection_time x CMM_rate (Rs 1500-3000/hr) + fixture_cost_amortized + scrap_factor`

## Indian Drawing Conventions

- **1st angle projection** (IS/ISO standard, SP 46:2003) -- default for Indian drawings
- **Units**: mm (IS standard). Decimal precision indicates tolerance class: X.X = +/-0.5mm, X.XX = +/-0.1mm, X.XXX = +/-0.01mm (precision, needs grinding)
- **Common annotations with cost impact**: "BREAK ALL SHARP EDGES" (+deburr 4-14 sec/part), "HEAT TREAT TO 58-62 HRC" (+heat treatment), "ZINC PLATING" (+surface treatment)
- **GD&T adoption varies**: Tier 1 OEMs (HAL, L&T Defence) use full ASME/ISO + CMM. Tier 3 small shops use basic +/- only with hand gauges.

## VLM Fine-Tuning Roadmap

The current GPT-4o/Gemini API approach works but is expensive ($0.012/drawing) and struggles with GD&T symbols (~60-70% accuracy on feature control frames).

**Upgrade path with Qwen2.5-VL-7B:**
- Already beats GPT-4o on document understanding benchmarks (95.7 vs 92.8 on DocVQA, 864 vs 736 on OCRBench)
- LoRA fine-tuning on 1,000 Indian engineering drawings costs $6-16 one-time
- Self-hosted inference on RTX 4090 (24GB): $1,600 one-time, breaks even at ~11K drawings/month
- Serverless (RunPod): $0.003-0.005/drawing, immediately cheaper than GPT-4o

**Training data strategy**: User's own Indian manufacturing drawings (DWG/DXF/STEP/PDF) converted to PNG at 300+ DPI. Auto-annotated with GPT-4o (distillation). Supplemented with TechING (HuggingFace), DeepCAD (178K models), ABC Dataset (1M STEP).

Fine-tuned Florence-2 on 400 engineering drawings achieved +52% F1 improvement over GPT-4o with -43% hallucination rate -- validating that small fine-tuned models can beat large general-purpose ones on this specific task.

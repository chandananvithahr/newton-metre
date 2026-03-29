# CADDi Patents & Similarity Search — Deep Dive (March 29, 2026)

## CADDi Overview

- **Founded:** 2017, Japan (Yushiro Kato, ex-McKinsey)
- **Valuation:** $470M (Mar 2025, post $38M Series C extension from Atomico)
- **Total raised:** $202M
- **Revenue target:** $1B by 2030
- **Engineering team:** 150 → doubling to 300
- **Tech stack:** Golang/Python on Google Cloud

---

## Known Patents (28 registered, 11+ filed)

### Core Similarity Search Patents

| Patent # | Title | What it does |
|----------|-------|-------------|
| JP 7372697 | Similar drawing search device, method, and program | Core patent — the similarity matching algorithm itself |
| JP 7377565 | Drawing search device, database construction device, search system, method, and program | Database construction + search infrastructure |
| EP 4546196A1 | Similar drawing retrieval by shape features | European filing — geometric shape feature vectors for similarity matching |
| WO 2026004458A1 | Advanced similar drawing retrieval | Improved shape feature matching (PCT/international) |

### Supporting Patents

| Patent # | Title | What it does |
|----------|-------|-------------|
| JP 2023100170A | Drawing search via title column attributes | Title block parsing → structured attributes → search |
| JP 2024113144A | Raster-to-vector with dimension recognition | Scanned drawings → vectorize → recognize dimensions |
| WO 2026004078A1 | Component table extraction | BOM table parsing from drawing images |
| WO 2026022945A1 | Drawing annotation management | Collaborative annotation with access control |
| + ~20 more | Computing/calculating categories | Various shape/drawing analysis |

### Acquired Patents (from Plethora, Jul 2022)

Plethora (US CNC startup, bankrupted Nov 2021) — CADDi's first external patent acquisition:

| Patent | What it does |
|--------|-------------|
| Auto DFM | Analyzes drawings to instantly identify un-machinable areas + suggest fixes |
| Auto Quote | Real-time price quotes based on machine hours + production parameters |
| Auto CAM | AI-generated machining programs from material type + geometry |

---

## How the Similarity Search Works (Reverse-Engineered)

CADDi doesn't publish their architecture, but from patents, marketing, and job postings:

### Pipeline

```
Drawing upload (PDF/TIFF/DWG/hand-drawn scan)
    ↓
OCR + symbol detection (text, GD&T, title block)
    ↓
Geometric feature extraction → shape "fingerprint"
    (deep learning model trained on millions of Japanese drawings)
    ↓
Feature vector stored in vector database
    ↓
Nearest-neighbor search against entire drawing archive
    ↓
Return ranked similar drawings + linked procurement data
```

### Key Technical Details

1. **Fingerprinting approach:** Algorithms analyze geometric features, text, and symbols to create a unique "fingerprint" per drawing. This is compared via nearest-neighbor search.
2. **Deep learning shape recognition:** Proprietary CNN/vision model trained on millions of Japanese manufacturing drawings. Kaggle Grandmasters on the team building these models.
3. **Handles degraded input:** Works on 30+ year old hand-drawn scans, different orientations, rough sketches, partial drawings.
4. **2D → 3D-like conversion:** Can convert 2D representations into 3D-like models for more accurate comparison (mentioned in product docs).
5. **Continuous learning:** ML techniques continuously improve pattern recognition from user feedback.
6. **Known limitation:** Drawings can be judged dissimilar if orientation/placement of parts changes or drawing style differs significantly — suggests they use global shape descriptors rather than purely local feature matching.

### What the Patents Likely Protect

Based on patent titles and the EP filing (shape features):
- The specific method of extracting geometric shape feature vectors from 2D drawings
- The database construction method for indexing these vectors
- The retrieval/ranking algorithm for similarity matching
- The raster-to-vector conversion pipeline for scanned drawings

---

## Competitive Moat Assessment

| Moat | Strength | Why |
|------|----------|-----|
| Data flywheel | VERY HIGH | 300K+ drawings per customer, millions total. More data = better model |
| Switching costs | VERY HIGH | Once 500K drawings indexed + linked to procurement history, migration is painful |
| Patents | MEDIUM | 28 patents block direct copying of their specific method, but not the general approach |
| Model quality | HIGH | Trained on millions of real drawings; competitors can't easily replicate this dataset |

---

## What This Means for Costimize

The play is not to compete on similarity search alone but to combine it with physics:

| Approach | Our path |
|----------|----------|
| Similarity search | DINOv2 embeddings + FAISS (no patent conflict — different method than CADDi's proprietary shape features) |
| Physics engine | Already built (our core moat — CADDi doesn't do should-cost breakdowns) |
| Combined | "Similar part was ₹450 + physics says ₹470 → target ₹460" — something CADDi can't do |

CADDi's patents cover their specific shape feature extraction and search method, not the general concept of finding similar drawings. Using standard vision embeddings (DINOv2, CLIP) + vector search (FAISS) is a completely different technical approach.

---

## Sources

- https://caddi.com/info/20231116/
- https://caddi.com/press/20220720/
- https://us.caddi.com/resources/insights/drawing-image-search
- https://us.caddi.com/product-overview
- https://fortune.com/2025/03/27/japanese-ai-startup-caddi-venture-capital-funding-atomico-supply-chain-optimization/
- https://caddi.tech/2024/12/25/100000
- https://caddi.com/en/functions/

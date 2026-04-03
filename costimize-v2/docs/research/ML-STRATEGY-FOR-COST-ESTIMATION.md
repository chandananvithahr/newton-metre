# ML Strategy for Manufacturing Cost Estimation
## Research Report — March 2026

> **TL;DR:** Keep physics-based models as the core engine. Add ML as a correction layer and for tasks where physics cannot reach (similar part retrieval, drawing understanding, quote confidence scoring). Start with XGBoost on tabular features — do NOT start with deep learning. The minimum viable ML feature is a **physics + ML hybrid correction model** trained on user-confirmed estimates.

---

## Table of Contents

1. [Where ML Beats Physics (And Where It Doesn't)](#1-where-ml-beats-physics-and-where-it-doesnt)
2. [ML Models Used in Manufacturing Cost Estimation](#2-ml-models-used-in-manufacturing-cost-estimation)
3. [Training Data Requirements](#3-training-data-requirements)
4. [Public Datasets](#4-public-datasets)
5. [Key Papers (2020-2026)](#5-key-papers-2020-2026)
6. [GitHub Repos and Tools](#6-github-repos-and-tools)
7. [Recommended ML Strategy for Costimize](#7-recommended-ml-strategy-for-costimize)

---

## 1. Where ML Beats Physics (And Where It Doesn't)

### Physics-Based Models: Strengths

Costimize's current engine uses MRR calculations, Sandvik kc1 cutting data, and Taylor tool life equations. These are **the right foundation** and should remain the core.

| Strength | Why Physics Wins |
|----------|-----------------|
| **Explainability** | Line-by-line breakdown: "CNC turning took 4.2 min at ₹800/hr = ₹56". Users trust this. |
| **Zero training data needed** | Works on day one with zero historical parts. No cold-start problem. |
| **Generalizes perfectly** | A new material or process just needs its MRR/kc1 values. No retraining. |
| **Regulatory/audit trail** | Procurement teams can defend costs to management with physics formulas. |
| **Handles novel parts** | First-of-kind parts estimated correctly if dimensions and processes are known. |

### Where ML Beats Physics

| Problem | Why ML Wins | Example |
|---------|------------|---------|
| **Setup time prediction** | Setup time varies by shop capability, fixture complexity, batch context — not just process type. Physics assigns fixed 15-60 min per process, but real shops vary 3-5x. | ML learns that "shop with 5-axis VMC needs 20 min setup for this geometry" vs "shop with 3-axis needs 45 min" |
| **Non-machining cost components** | Inspection time, deburring, surface treatment duration, packaging — these have no physics formula. | Deburring time depends on edge count, material, part complexity — learnable from historical data |
| **Quote-to-actual variance correction** | Physics gives a deterministic answer; real quotes from suppliers vary ±20-40%. ML learns the systematic bias. | "For aluminum turned parts under ₹500, physics overestimates by 12% on average" |
| **Similar part retrieval** | No physics model can say "this part looks like PO #4521 which cost ₹340 last time." | Embedding-based similarity search (what CADDi built for $1.4B) |
| **Drawing understanding** | Extracting dimensions, tolerances, and processes from PDFs/images. Pure CV/VLM task. | Florence-2 fine-tuned on 400 drawings achieves 52% F1 improvement over GPT-4o |
| **Confidence scoring** | Physics gives a point estimate. ML can give "₹340 ± ₹45 (87% confidence)." | Quantile regression or conformal prediction on top of physics output |
| **Process route prediction** | Given a part's features, predict which processes are needed before human confirmation. | Multi-label classification from geometric features |

### The Hybrid Answer: Physics + ML Correction

The state-of-the-art approach in 2024-2026 is **not** "ML replaces physics" — it is **physics model + ML correction factor**:

```
Final_Cost = Physics_Cost × ML_Correction_Factor
```

Or additively:

```
Final_Cost = Physics_Cost + ML_Residual
```

**Why this works:**
- The physics model captures 80-90% of the variance (material, machining time, tooling).
- The ML correction learns the remaining 10-20% (setup variability, shop-specific factors, non-machining overheads, systematic bias).
- ML correction requires **far less data** than end-to-end ML because it only needs to learn the residual, not the entire cost function.
- The physics model provides a strong inductive bias, preventing catastrophic ML predictions.

**Published evidence:** A 2024 review of hybrid physics-ML models in manufacturing confirms that "correction tasks require less data compared to mapping the complete problem, since correction is often less complex when fundamental relationships are already represented in the physics-based model" ([Tandfonline, 2024](https://www.tandfonline.com/doi/full/10.1080/21693277.2024.2305358)).

---

## 2. ML Models Used in Manufacturing Cost Estimation

### Model Architectures by Task

| Task | Best Model | Why | Data Needed |
|------|-----------|-----|-------------|
| **Cost prediction from tabular features** | XGBoost / LightGBM / CatBoost | Gradient-boosted trees dominate tabular data. R² = 0.988, MAPE ~10% on 13K parts. | 500-10,000 parts |
| **Cost prediction from 3D CAD** | 3D CNN (voxel) or PointNet | Learns directly from geometry. Explainable via 3D Grad-CAM. | 1,000+ 3D models with cost labels |
| **Feature recognition from B-Rep** | GNN (BRepGAT, AAGNet, BRepFormer) | Preserves topological relationships. BRepFormer: 93.16% accuracy on MFTRCAD. | Pre-trained on MFCAD++ (60K models) |
| **Drawing understanding** | Fine-tuned VLM (Florence-2, Donut) | Extracts dimensions, GD&T, tolerances from 2D drawings. | 400-1,400 annotated drawings |
| **Similar part search** | Embedding + nearest neighbor | CADDi approach: encode part geometry into vector, find nearest historical match. | 1,000+ parts with cost history |
| **Process route prediction** | Multi-label classifier (XGBoost or small NN) | Given dimensions + material, predict which processes are needed. | 500+ parts with confirmed process routes |
| **Quote confidence** | Quantile regression / conformal prediction | Outputs prediction intervals, not just point estimates. | 200+ parts with both estimates and actuals |

### XGBoost / Gradient Boosting (Recommended First Model)

**Why XGBoost for cost estimation:**
- Handles mixed feature types (continuous dimensions + categorical material/process)
- Built-in feature importance (no need for separate explainability layer)
- Robust with small datasets (stable below 10,000 rows)
- Fast inference (milliseconds, not seconds)
- SHAP integration for explainability
- No GPU required

**Published results:**
- arXiv:2508.12440: XGBoost on 13,684 DWG drawings, ~200 geometric features per product group, MAPE ~10% across 24 product groups
- Optimized LightGBM achieves MAPE of 10.78% on manufacturing cost prediction
- XGBoost and CatBoost achieve R² = 0.988 and 0.987 respectively

### Neural Networks for 3D CAD

**arXiv:2010.14824 (Explainable AI for Manufacturing Cost):**
- 3D CNN on voxelized CAD models
- Dataset: 1,006 machined parts with cost labels
- Uses 3D Grad-CAM to visualize which geometric features drive cost
- Inputs: 3D CAD (voxelized) + material + volume
- Good for: identifying high-cost features for design-for-manufacturing feedback

**Limitation for Costimize:** Requires 3D CAD input. Indian MSMEs mostly have 2D PDFs. Useful later when STEP file support is added.

### Graph Neural Networks for B-Rep

**State of the art (2024-2025):**
- **BRepFormer** (2025): Transformer on B-Rep, 93.16% feature recognition accuracy
- **AAGNet**: Multi-task GNN for machining feature recognition from B-Rep
- **BRepGAT**: Graph attention network for face segmentation in B-Rep
- **Sheet-metalNet**: GNN specifically for sheet metal feature identification

**Relevance to Costimize:** These recognize manufacturing features (holes, pockets, slots, chamfers) from STEP/B-Rep files. When STEP support is added, a pre-trained GNN can automatically detect processes needed, replacing manual/AI process detection.

### Vision-Language Models for Drawing Extraction

**State of the art (2025-2026):**
- Fine-tuned Florence-2 on 400 engineering drawings: +52% F1 score vs GPT-4o, -43% hallucination rate
- Hybrid YOLOv11-obb + VLM pipeline on 1,367 drawings: localizes annotation regions, then VLM parses dimensions/GD&T
- Categories extracted: GD&T, tolerances, measures, materials, notes, radii, surface roughness, threads, title blocks

**Relevance to Costimize:** This is the direct upgrade path for `extractors/vision.py`. Fine-tuning Florence-2 (open-source, runs locally) on Indian engineering drawings would beat the current GPT-4o API approach in accuracy while eliminating per-call API costs.

---

## 3. Training Data Requirements

### How Much Data Is Needed?

| Model Type | Minimum Viable | Good | Excellent |
|------------|---------------|------|-----------|
| XGBoost on tabular features | 100-300 parts | 1,000-3,000 | 10,000+ |
| ML correction on physics residual | 50-100 parts | 300-500 | 1,000+ |
| 3D CNN on voxelized CAD | 500 parts | 1,000-3,000 | 10,000+ |
| GNN for feature recognition | Pre-trained (MFCAD++) | Fine-tune on 200+ | 1,000+ domain parts |
| VLM fine-tuning for drawing extraction | 400 drawings | 1,000 | 5,000+ |
| Similar part embeddings | 100 parts | 500 | 5,000+ |

### What Features Matter Most?

From arXiv:2508.12440 (SHAP analysis on 13,684 parts):

1. **Rotated dimension maxima** — the largest dimension in any rotated coordinate system
2. **Arc statistics** — count, radii distribution (indicates curved surfaces = more complex machining)
3. **Divergence metrics** — how much geometry deviates from simple prismatic shapes
4. **Material type** — categorical, massive impact on machining time
5. **Number of distinct geometric primitives** — holes, slots, pockets count
6. **Tolerance specifications** — tight tolerances = slower feeds, more passes
7. **Volume / surface area ratio** — indicates part complexity
8. **Number of setups required** — driven by feature accessibility

### The Cold Start Problem

**Costimize's situation:** Zero historical data from users at launch.

**Strategy to bootstrap:**

1. **Phase 0 (Now): Physics-only.** No ML needed. The current engine works without any data.

2. **Phase 1 (First 50-100 users): Collect data passively.**
   - Log every estimate: input dimensions, material, processes, calculated cost.
   - When users upload PO history, store (estimate, actual_cost) pairs.
   - When users manually adjust estimates before sharing with suppliers, log the delta.
   - This creates labeled training data organically.

3. **Phase 2 (100+ estimate-actual pairs): Train first ML correction model.**
   - XGBoost trained on: `[physics_estimate, material, process_count, dimension_features] → actual_cost / physics_cost ratio`
   - This correction factor improves over time as more data arrives.

4. **Phase 3 (500+ parts with embeddings): Similar part search.**
   - Encode each estimated part as a feature vector.
   - When a new part arrives, find the 5 most similar historical parts.
   - Show: "Similar parts were quoted at ₹280-₹350. Our estimate: ₹320."

### Synthetic Data Generation

**SMOTE and variants** (ADASYN, BLSMOTE) can augment small tabular datasets:
- Interpolate between existing samples to create synthetic training points
- Research shows 50% performance improvement in manufacturing applications
- Useful when you have 50-200 real parts but need 500+ for stable XGBoost training

**Limitations:**
- Synthetic data cannot introduce new patterns, only interpolate existing ones
- Risk of creating unrealistic combinations (e.g., titanium part with aluminum machining time)
- Best used as a bridge until real data accumulates

### Transfer Learning

**For drawing extraction:** Fine-tune Florence-2 or Donut (pre-trained on millions of documents) on 400-1,000 Indian engineering drawings. The pre-trained model already understands document layout, text, and spatial relationships — it just needs to learn engineering drawing conventions.

**For cost prediction:** Transfer learning is less applicable to tabular XGBoost models. Instead, use the physics model as a "pre-trained" foundation and train ML only on the residual.

---

## 4. Public Datasets

### CAD / Geometry Datasets

| Dataset | Size | Format | What's In It | Use For Costimize |
|---------|------|--------|-------------|-------------------|
| **MFCAD** | 15,488 models | STEP | Labeled machining features per B-Rep face | Pre-train feature recognition for STEP parser |
| **MFCAD++** | 59,655 models | STEP | 3-10 machining features per model, intersecting features | Better feature recognition training |
| **ABC Dataset** | 1,000,000 models | STEP, STL, Parasolid | General CAD geometry (Onshape-sourced) | Geometric embedding pre-training |
| **Fusion 360 Gallery** | 8,625 models | STEP + design history | Parametric CAD with construction sequences | Process sequence learning |
| **ShapeNet** | 51,300 models | Mesh | 55 categories of 3D objects | General shape understanding |
| **HybridCAD** | Unknown | STEP | Additive + subtractive manufacturing features | Hybrid manufacturing feature recognition |

### Engineering Drawing Datasets

| Dataset | Size | What's In It | Availability |
|---------|------|-------------|-------------|
| **From arXiv:2508.12440** | 13,684 DWG files | Automotive suspension/steering, 200 geometric features, cost labels | Not public (proprietary) |
| **Florence-2 drawing dataset** | 1,367 drawings | 9 annotation categories (GD&T, tolerances, measures, etc.) | Research only |
| **GD&T extraction dataset** | 400 drawings | Domain expert annotations | Research only |

### Cost Estimation Datasets

**Bad news:** There are **no public manufacturing cost estimation datasets**. Cost data is proprietary everywhere. This is confirmed by the literature — every paper uses private industrial data.

**Implication for Costimize:** You must build your own dataset from user interactions. This is actually a moat — whoever accumulates the most estimate-vs-actual pairs for Indian manufacturing wins.

---

## 5. Key Papers (2020-2026)

### Tier 1: Directly Relevant to Costimize

| Paper | Year | Key Finding | Relevance |
|-------|------|-------------|-----------|
| **[arXiv:2508.12440](https://arxiv.org/abs/2508.12440)** — ML-Based Manufacturing Cost Prediction from 2D Engineering Drawings | 2025 | XGBoost/LightGBM on 200 geometric features from 13,684 DWG files. MAPE ~10%. SHAP identifies geometric cost drivers. | **Direct blueprint for Costimize's ML layer.** Extract features from drawings, predict cost. |
| **[arXiv:2010.14824](https://arxiv.org/abs/2010.14824)** — Explainable AI for Manufacturing Cost Estimation | 2020 | 3D CNN on 1,006 voxelized parts. 3D Grad-CAM visualizes cost-driving features. | Architecture for when STEP support is added. |
| **[ScienceDirect, 2024](https://www.sciencedirect.com/science/article/pii/S0952197624011151)** — Cost modelling for engineered-to-order products using ML | 2024 | ML cost model for ETO products (job shop economics). | Directly applicable to Indian job shop context. |
| **[Tandfonline, 2023](https://www.tandfonline.com/doi/full/10.1080/0951192X.2023.2165160)** — Manufacturing cost estimation based on similarity | 2023 | Similarity-based retrieval for cost estimation. Knowledge graph + semantic distance. | Blueprint for similar part search feature. |

### Tier 2: Hybrid Physics-ML Models

| Paper | Year | Key Finding |
|-------|------|-------------|
| **[Tandfonline, 2024](https://www.tandfonline.com/doi/full/10.1080/21693277.2024.2305358)** — Physics-based and data-driven hybrid modeling in manufacturing | 2024 | Comprehensive review. ML correction on physics requires less data than end-to-end ML. |
| **[MDPI Materials, 2021](https://www.mdpi.com/1996-1944/14/8/1883)** — Hybrid Modelling by ML Corrections of Analytical Model Predictions | 2021 | ANN learns correction factor (defaults to 1.0 when no correction needed). Validated on high-fidelity simulations. |
| **[ASME JCISE, 2025](https://asmedigitalcollection.asme.org/computingengineering/article/25/12/120804/1225302/)** — Physics-Informed ML in Design and Manufacturing | 2025 | Status and challenges of PIML. Physics constraints in loss function. |

### Tier 3: Feature Recognition and Drawing Understanding

| Paper | Year | Key Finding |
|-------|------|-------------|
| **[BRepFormer, 2025](https://arxiv.org/html/2504.07378v1)** — Transformer-Based B-rep Feature Recognition | 2025 | 93.16% accuracy on MFTRCAD. Transformer architecture on B-Rep topology. |
| **[ScienceDirect, 2025](https://www.sciencedirect.com/science/article/abs/pii/S2212827123002317)** — From drawings to decisions: hybrid VLM framework | 2025 | YOLOv11-obb + Florence-2/Donut on 1,367 drawings. 9 annotation categories. |
| **[arXiv:2411.03707](https://arxiv.org/abs/2411.03707)** — Fine-Tuning VLM for Engineering Drawing Information Extraction | 2024 | Florence-2 on 400 drawings: +52% F1, -43% hallucination vs GPT-4o. |
| **[BRepGAT, 2023](https://academic.oup.com/jcde/article/10/6/2384/7453688)** — GNN for B-rep face segmentation | 2023 | Graph attention network for machining feature face segmentation. |
| **[AAGNet](https://github.com/whjdark/AAGNet)** — Multi-task machining feature recognition | 2023 | Semantic + instance + bottom face segmentation from B-Rep. Open source. |

### Tier 4: Survey and Meta-Analysis

| Paper | Year | Key Finding |
|-------|------|-------------|
| **[MDPI Forecasting, 2025](https://www.mdpi.com/2673-3951/6/2/35)** — AI in Cost Estimation: Systematic Review | 2025 | 39 articles, 2016-2024. ANN used in 26.33% of studies. XGBoost, CNN, SVM at 7.90% each. Hybrid models are superior. |
| **[Springer, 2025](https://link.springer.com/article/10.1007/s40436-025-00564-x)** — Survey on ML applied to CNC milling | 2025 | Comprehensive survey covering cost, time, energy, and quality prediction. |

---

## 6. GitHub Repos and Tools

### Open-Source Repos

| Repo | What It Does | Stars | Relevance |
|------|-------------|-------|-----------|
| **[whjdark/AAGNet](https://github.com/whjdark/AAGNet)** | GNN for machining feature recognition from B-Rep | Active | Feature recognition for STEP files |
| **[hducg/MFCAD](https://github.com/hducg/MFCAD)** | MFCAD dataset (15K labeled STEP models) | Reference | Training data for feature recognition |
| **[QUB MFCAD++](https://gitlab.com/qub_femg/machine-learning/mfcad2-dataset)** | MFCAD++ dataset (60K models) | Reference | Larger training set |
| **[dimasthoriq/cnc-machining-time-estimation](https://github.com/dimasthoriq/cnc-machining-time-estimation)** | ML for CNC machining time (thesis project) | Small | Reference implementation |
| **[shameel0505/CNC-Cost-Estimation-ACE](https://github.com/shameel0505/CNC-Cost-Estimation-ACE)** | Data-driven CNC cost prediction | Small | Reference implementation |
| **[github.com/topics/cost-estimation](https://github.com/topics/cost-estimation?l=python)** | Collection of Python cost estimation projects | Various | Browse for ideas |

### Commercial Tools Using ML

| Tool | Approach | Pricing |
|------|----------|---------|
| **[aPriori](https://www.apriori.com/)** | Physics-based simulation (440+ processes), NOT ML. 3D CAD only. 87 regional cost libraries. Three-tier digital twin (product, process, factory). | Enterprise ($100K+/yr) |
| **[Dashnode](https://www.dashnode.ai/)** | ML-based CNC costing from CAD files. India-based (spun out of Karkhana.io). Costs files in <5 seconds. No CAM/spreadsheets needed. | Unknown |
| **[CADDi](https://caddi.com/)** | Deep learning shape recognition + similarity search. $1.4B valuation, 28 patents, trained on millions of Japanese drawings. | Enterprise |
| **[Paperless Parts](https://www.paperlessparts.com/)** | Quoting platform with geometry analysis. Not ML-first. | SaaS |

### Key Observation

**There are zero open-source, end-to-end manufacturing cost estimation ML models with trained weights.** Every implementation is either:
- Academic (code available, no trained model, proprietary data)
- Commercial (closed source)
- Toy projects (small datasets, not production-ready)

This confirms Costimize's approach: build the physics engine first (done), add ML incrementally as data accumulates.

---

## 7. Recommended ML Strategy for Costimize

### Decision Framework

```
                  Have physics model?
                       │
                  YES (Costimize ✓)
                       │
              ┌────────┴────────┐
              │                 │
        Have user data?    No user data?
              │                 │
         Add ML layer      Ship physics-only
              │            (CURRENT STATE ✓)
              │
    ┌─────────┴──────────┐
    │                    │
  Tabular data?    3D CAD available?
    │                    │
  XGBoost            GNN / 3D CNN
  correction         (Phase 3+)
  (Phase 2)
```

### Phase 0: Now (Ship Physics-Only) — CURRENT STATE

**Status:** Done. 46 tests passing. Physics engine works.

**What to add now (no ML needed):**
- Instrument every estimate for future ML training
- Log: `{part_id, dimensions, material, processes, physics_cost, timestamp}`
- When users upload PO history: store `{estimate, actual_po_cost}` pairs
- When users manually adjust costs: store `{physics_cost, user_adjusted_cost, reason}`
- This is the **data collection foundation** — do this before any ML work

**Schema for data collection:**
```python
@dataclass(frozen=True)
class EstimateRecord:
    estimate_id: str
    timestamp: str
    # Input features (what the user provided)
    material: str
    dimensions: dict  # {diameter, length, width, height, ...}
    processes: tuple[str, ...]
    quantity: int
    tolerance_tight: bool
    # Physics output
    physics_cost_total: float
    physics_cost_breakdown: dict  # {material: X, machining: Y, ...}
    # User feedback (filled later)
    user_adjusted_cost: float | None  # If user changed the estimate
    actual_po_cost: float | None  # If matched to a PO
    supplier_quote: float | None  # If user enters a supplier quote
```

### Phase 1: First ML Feature (After 50-100 Estimate-Actual Pairs)

**What:** Physics + XGBoost correction factor

**Architecture:**
```
User Input → Physics Engine → ₹340 (physics estimate)
                                    │
                                    ▼
                           [XGBoost Correction]
                           Features: physics_cost, material,
                                    process_count, max_dimension,
                                    tolerance_tight, quantity
                                    │
                                    ▼
                           Correction factor: 0.92
                                    │
                                    ▼
                           Final: ₹340 × 0.92 = ₹313
                           Confidence: ±₹28 (85%)
```

**Why XGBoost first:**
- Works with 50-100 samples (stable below 10K rows)
- No GPU needed
- Built-in SHAP explainability
- Trains in seconds, not hours
- Feature importance tells you what the physics model gets wrong

**Implementation:**
```python
# Pseudocode — train correction model
import xgboost as xgb

features = [
    "physics_cost",
    "material_category",  # categorical
    "process_count",
    "max_dimension_mm",
    "min_dimension_mm",
    "tolerance_tight",     # boolean
    "quantity",
    "surface_area_approx",
]

target = actual_cost / physics_cost  # correction ratio

model = xgb.XGBRegressor(
    n_estimators=100,
    max_depth=4,
    learning_rate=0.1,
    min_child_weight=5,  # conservative for small data
)
model.fit(X_train, y_train)
```

**Estimated timeline:** 2-4 weeks of development once data exists

### Phase 2: Similar Part Search (After 500+ Parts)

**What:** When user uploads a new drawing, show "5 most similar historical parts and their costs"

**Architecture:**
1. Encode each part as a feature vector: `[material_onehot, normalized_dimensions, process_bitmask, complexity_score]`
2. Store vectors in a simple FAISS index (or even numpy dot product for <10K parts)
3. On new estimate, find k-nearest neighbors
4. Display: "Similar parts were quoted ₹280-₹350. Your estimate: ₹320."

**Why this is valuable:**
- CADDi built a $1.4B business on this concept
- Procurement teams LOVE historical comparison data
- Builds trust: "This is consistent with what we paid before"
- Works even when physics model has high uncertainty

**Data needed:** 500+ parts with cost history (from PO uploads)

### Phase 3: VLM Fine-Tuning for Drawing Extraction (After 400+ Annotated Drawings)

**What:** Replace GPT-4o API calls with a fine-tuned Florence-2 model for dimension/tolerance extraction

**Why:**
- arXiv:2411.03707 shows fine-tuned Florence-2 achieves +52% F1, -43% hallucination vs GPT-4o
- Eliminates per-call API costs ($0.03/drawing → $0 after one-time training cost of ~$6-16)
- Runs locally — no internet dependency, no data leaving user's network
- Better accuracy on Indian drawing conventions (1st angle projection, IS standards)

**Requirements:**
- 400-1,000 Indian engineering drawings with annotated ground truth
- Fine-tuning cost: $6-16 using LoRA on a single GPU
- Inference: runs on CPU (Florence-2-base is 0.23B parameters)

**This should be built when:**
- Volume of drawings processed justifies the annotation effort
- Users complain about extraction accuracy
- API costs become significant (>$100/month)

### Phase 4: GNN Feature Recognition from STEP Files (After STEP Parser is Built)

**What:** Automatically detect manufacturing features (holes, pockets, chamfers, threads) from STEP files using a pre-trained GNN

**Architecture:**
- Pre-train on MFCAD++ (60K labeled STEP models) — this is free public data
- Fine-tune on user-uploaded STEP files with confirmed process routes
- Output: list of manufacturing features with dimensions → feed directly into physics cost engine

**Why:**
- Eliminates manual process selection by user
- BRepFormer achieves 93.16% feature recognition accuracy
- AAGNet provides open-source starting point
- Pre-trained models available, so cold-start is solved

### Phase 5: Fine-Tuned Extraction VLM (After 200+ Corrected Drawings) — NEW April 2026

**What:** Replace cloud API extraction calls (Gemini/GPT-4o) with self-hosted fine-tuned Qwen2.5-VL-7B

**Why Phase 3 was Florence-2, Phase 5 is Qwen2.5-VL-7B:**
- Florence-2 (0.23B) is great for targeted dimension extraction but lacks general reasoning
- Qwen2.5-VL-7B (7B) handles the full extraction task: dimensions + GD&T + material + processes + surface finish in one pass
- Beats GPT-4o on document understanding benchmarks
- Self-hosted = zero API cost + defense/on-prem ready

**Data source:** Every cloud API extraction is automatically logged with user corrections as gold labels. No manual annotation needed — users create training data by using the product.

**Method:** QLoRA (rank 16-32, 4-bit quantization) on RunPod A100 80GB. Cost: $7-13 per training run.

**Deploy via:** vLLM with OpenAI-compatible API. Same interface as cloud APIs — swap is config-only.

### Phase 6: Fine-Tuned Visual Embeddings (After 500+ Similarity Feedback Pairs) — NEW April 2026

**What:** Fine-tune DINOv2-ViT-B/14 on manufacturing drawing pairs with user similarity feedback

**Data source:** Every similarity search where user confirms ("yes, this is similar") or rejects ("no, this is different") creates a contrastive training pair.

**Method:** Contrastive loss fine-tune. Full fine-tune is OK for ViT-B (86M params — small). Cost: $3-5 on RunPod.

**Why:** DINOv2 baseline is already 2.3x better than CLIP for visual similarity. Fine-tuning on actual manufacturing drawings (Indian standards, BIS grades, specific part types) adds another estimated 20-30%.

**Also replace text embeddings:** Swap Gemini Embedding 2 with nomic-embed-text-v1.5 (768-dim, self-hosted, 137M params). Same quality, zero API cost.

### Phase 7: Fine-Tuned Agent LLM (After 500+ Agent Conversations) — NEW April 2026

**What:** Fine-tune Qwen2.5-32B-Instruct for manufacturing domain tool-calling

**Why last:** Base Qwen2.5-32B already handles tool-calling reliably (top-3 on Berkeley Function-Calling Leaderboard). Fine-tuning adds domain-specific routing: "when user says 'check this part' call search_estimates, not calculate_cost."

**Data source:** Every cloud agent conversation (user message + tool calls + results + final response) = training trace. Log everything from day one.

**Method:** QLoRA (rank 32-64, 4-bit). RunPod A100 80GB × 8-16 hours = $13-26.

**Minimum reliable model size for tool use: 32B parameters.** 7B models can route 3-5 simple tools but fail on multi-step reasoning, nested tool calls, or deciding NOT to call a tool.

### Phase 8: Full Self-Hosted Stack — NEW April 2026

**What:** All AI runs on own infrastructure. Zero cloud API dependency.

**Target hardware:** Single NVIDIA A6000 (48GB VRAM, ~$4,500 used) or RTX 4090 (24GB, ~$1,800)

```
vLLM Server:
├── Qwen2.5-VL-7B-AWQ (extraction) — 5GB
├── Qwen2.5-32B-AWQ (agent) — 20GB
└── Qwen2.5-7B-AWQ (validation) — 5GB

TEI Server (embeddings):
├── DINOv2-ViT-B/14 — 0.4GB
└── nomic-embed-text-v1.5 — 0.3GB

ColFlor Server (late interaction) — 0.7GB

Total: ~26GB active VRAM (fits A6000)
```

**For defense on-prem:** Ship GPU box + Ubuntu + vLLM + all fine-tuned models + PostgreSQL + Next.js static build. Air-gapped. Hardware cost: $1,800-4,500 = one month enterprise subscription.

**Cost comparison at 100 active users:** Cloud APIs $200-500/mo → RunPod serverless $80-150/mo → Own hardware $30-150/mo.

### What NOT to Build

| Temptation | Why Not |
|-----------|---------|
| **End-to-end deep learning cost estimator** | Needs 10K+ labeled parts. Physics works better with zero data. Black box kills user trust. |
| **Custom foundation LLM for manufacturing** | Fine-tune open-source instead. Qwen2.5 + LoRA = $7-26 per run. Training from scratch = $100K+. |
| **Reinforcement learning for process planning** | Academic fantasy. No reward signal in real procurement. |
| **GAN for synthetic part generation** | Generates geometry, not costs. Solves the wrong problem. |
| **Real-time tool wear prediction** | Costimize estimates cost, it doesn't control machines. Wrong product. |

---

## Summary: ML + AI Roadmap

| Phase | When | What | Model | Data Needed | Impact |
|-------|------|------|-------|-------------|--------|
| **0** | Now | Data collection instrumentation | None | 0 (collecting) | Foundation for everything |
| **1** | 50-100 pairs | Physics + XGBoost correction | XGBoost | 50-100 estimate-actual pairs | ±5-10% accuracy improvement |
| **2** | 500+ parts | Similar part search | Embeddings + kNN | 500+ parts with costs | Trust building, procurement workflow |
| **3** | 400+ drawings | Fine-tuned drawing extraction (lightweight) | Florence-2 (LoRA) | 400+ annotated drawings | Faster extraction, reduced API costs |
| **4** | STEP parser built | GNN feature recognition | BRepFormer / AAGNet | Pre-trained on MFCAD++ | Automated process detection from 3D |
| **5** | 200+ corrected drawings | Self-hosted extraction VLM | Qwen2.5-VL-7B (QLoRA) | 200+ extraction pairs with corrections | **Eliminate extraction API costs entirely** |
| **6** | 500+ similarity feedback | Self-hosted visual embeddings | DINOv2 + nomic-embed (fine-tune) | 500+ confirmed/rejected pairs | **Eliminate embedding API costs entirely** |
| **7** | 500+ agent conversations | Self-hosted agent LLM | Qwen2.5-32B (QLoRA) | 500+ conversation traces | **Eliminate agent API costs entirely** |
| **8** | Phases 5-7 complete | Full self-hosted + on-prem | All above on vLLM | All above | **Zero cloud dependency. Defense-ready.** |

**The core insight:** Physics-based models are Costimize's competitive advantage for early-stage (zero data, full explainability, works on day one). ML is the long-term moat built on accumulated user data that no competitor can replicate. The strategy is: ship physics now, collect data passively, add ML when data justifies it. **Cloud APIs get us started. Fine-tuned self-hosted models are the moat.** Every user interaction makes our models better — and that data doesn't exist anywhere else.

**Total fine-tuning investment:** ~$50-80 in compute over 6 months.
**Defense on-prem hardware:** $1,800-4,500 per deployment.

See `AI-AGENT-ROADMAP.md` for the full agent architecture and self-hosting strategy.

---

## Sources

- [arXiv:2508.12440 — ML-Based Manufacturing Cost Prediction from 2D Drawings](https://arxiv.org/abs/2508.12440)
- [arXiv:2010.14824 — Explainable AI for Manufacturing Cost Estimation](https://arxiv.org/abs/2010.14824)
- [arXiv:2411.03707 — Fine-Tuning VLM for Engineering Drawing Extraction](https://arxiv.org/abs/2411.03707)
- [BRepFormer: Transformer-Based B-rep Feature Recognition](https://arxiv.org/html/2504.07378v1)
- [Physics-based and data-driven hybrid modeling in manufacturing (2024 review)](https://www.tandfonline.com/doi/full/10.1080/21693277.2024.2305358)
- [Hybrid Modelling by ML Corrections of Analytical Predictions](https://www.mdpi.com/1996-1944/14/8/1883)
- [AI in Cost Estimation: Systematic Review (2025)](https://www.mdpi.com/2673-3951/6/2/35)
- [Survey on ML applied to CNC milling (2025)](https://link.springer.com/article/10.1007/s40436-025-00564-x)
- [Manufacturing cost estimation based on similarity (2023)](https://www.tandfonline.com/doi/full/10.1080/0951192X.2023.2165160)
- [Cost modelling for engineered-to-order products using ML (2024)](https://www.sciencedirect.com/science/article/pii/S0952197624011151)
- [From drawings to decisions: hybrid VLM framework (2025)](https://www.sciencedirect.com/science/article/abs/pii/S0736584525002406)
- [BRepGAT: GNN for B-rep face segmentation (2023)](https://academic.oup.com/jcde/article/10/6/2384/7453688)
- [MFCAD++ Dataset (Queen's University Belfast)](https://pure.qub.ac.uk/en/datasets/mfcad-dataset-dataset-for-paper-hierarchical-cadnet-learning-from/)
- [AAGNet GitHub](https://github.com/whjdark/AAGNet)
- [MFCAD GitHub](https://github.com/hducg/MFCAD)
- [ABC Dataset](https://deep-geometry.github.io/abc-dataset/)
- [Fusion 360 Gallery Dataset](https://www.research.autodesk.com/app/uploads/2023/03/Fusion_360_Gallery__A_Dataset_and_Environment_for_Programmatic_CAD_Construction_from_Human_Design_Sequences.pdf_recB1A7wJLthITzJo.pdf)
- [aPriori Manufacturing Cost Estimation](https://www.apriori.com/manufacturing-cost-estimation/)
- [Dashnode CNC Costing Software](https://www.dashnode.ai/)
- [Synthetic Data in Manufacturing (Frontiers, 2024)](https://www.frontiersin.org/journals/manufacturing-technology/articles/10.3389/fmtec.2024.1320166/full)
- [Physics-Informed ML in Design and Manufacturing (ASME, 2025)](https://asmedigitalcollection.asme.org/computingengineering/article/25/12/120804/1225302/)
- [From Concept to Manufacturing: Evaluating VLMs for Engineering Design](https://link.springer.com/article/10.1007/s10462-025-11290-y)

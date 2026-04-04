---
slug: embeddings-vector-search
title: Embedding Models, Vector Search, and ML Strategy
keywords: embeddings, DINOv2, CLIP, Gemini Embedding 2, ColFlor, pgvector, HNSW, BM25, hybrid search, Reciprocal Rank Fusion, FlashRank, re-ranking, Matryoshka, vector search, self-hosted AI, vLLM, fine-tuning
sources: ML-STRATEGY-FOR-COST-ESTIMATION.md, GITHUB-REPOS-SURVEY.md, SIMILARITY-SEARCH-DEEP-DIVE.md
updated: 2026-04-04
---

# Embedding Models, Vector Search, and ML Strategy

Newton-Metre's similarity search turns a company's drawing history into a searchable asset. The technical foundation is embedding quality -- not the vector database or ANN algorithm. A fine-tuned model on 500-1000 manufacturing drawings outperforms any off-the-shelf model with brute-force cosine similarity.

## Embedding Model Comparison

### Vision Models (Drawing Similarity)

| Model | Org | Dims | Visual Similarity Accuracy | Key Strength |
|-------|-----|------|---------------------------|--------------|
| **DINOv2-ViT-B/14** | Meta | 768 | **64%** | Best zero-shot visual similarity. Self-supervised, captures shape/texture/spatial composition |
| **CLIP** | OpenAI | 512-768 | **28.45%** | Text-image alignment, but weak on pure geometric similarity |
| **SigLIP 2** | Google | 384-1152 | -- | Multilingual vision-language, fine-tunable |
| **DINOv3** | Meta | 1024 (7B) | 88.4% ImageNet | SOTA visual features but needs serious GPU |
| **C-RADIOv4** | NVIDIA | Unified | -- | Distilled SigLIP2+DINOv3+SAM3, single model |

**DINOv2 is 2.3x better than CLIP** for pure visual (structural/geometric) similarity. CLIP wins only for text-to-image search ("find cylindrical parts with threads").

### Text/Multimodal Embeddings

| Model | Dims | Key Feature | Cost |
|-------|------|-------------|------|
| **Gemini Embedding 2** | 768 (Matryoshka from 3072) | First natively multimodal. MTEB English: 68.32 (top by 5+ points). Embeds PDFs directly (up to 6 pages) | $0.006/1K tokens |
| **OpenAI text-embedding-3-small** | 1536 | Good text embeddings | $0.00002/1K tokens |
| **nomic-embed** | 768 | Open-source, self-hostable | Free |

Gemini Embedding 2's Matryoshka property means 768 dims retains 99.5% quality of 3072 -- ideal for storage efficiency.

### On-Prem / Defense Models

| Model | Params | RAM | Quality Drop vs ColPali | Use Case |
|-------|--------|-----|------------------------|----------|
| **ColFlor** | 174M | 8GB | 1.8% | 17x smaller, 5.25x faster than ColPali. Best for self-hosted defense target |
| **ColSmol** | 256M | 8GB | -- | Edge deployment |
| **ColQwen2** | Qwen2-VL | -- | Better | Better multilingual + resolution |

## Recommended Embedding Phase Plan

| Phase | Model | Why |
|-------|-------|-----|
| **Now** | Gemini Embedding 2 (768-dim) | Real learned embeddings, embeds PDFs directly, same API |
| **Next** | DINOv2-ViT-B/14 (768-dim) | 2.3x better visual similarity, runs on 8GB RAM CPU |
| **Later** | Fine-tuned DINOv2 on our drawings | Contrastive learning on 200-500 drawing pairs, $5-15 on cloud GPU |
| **Future** | GC-CAD GNN for STEP files | 5th ranking signal when STEP support ships |

## Vector Search with pgvector

Newton-Metre uses pgvector on Supabase Postgres. Performance benchmarks:

- pgvector 0.7.0+: **30x faster** HNSW index builds
- pgvectorscale: **471 QPS at 99% recall** on 50M vectors (11.4x better than Qdrant at same recall)
- At <10K drawings (our scale for years): pgvector HNSW is more than sufficient
- Scaling limit: at 50M vectors with HNSW, need ~1TB RAM
- **No migration needed** until 50M+ vectors. Adding another database is unnecessary complexity.

### 768-dim Standard

EMBEDDING_DIM=768 across the system. Matryoshka truncation from 3072 retains 99.5% quality. Compatible with DINOv2, Gemini Embedding 2, and nomic-embed.

## Hybrid Search: Vector + BM25

Neither dense vectors nor sparse keyword search alone is sufficient:
- **Dense (vector)**: "turned aluminum shaft" matches "CNC lathe machined AL6061 spindle"
- **Sparse (BM25)**: Part numbers, material grades like "IS 2062 E250", tolerance "+/-0.05mm"

**Implementation**: PostgreSQL `tsvector` on part descriptions + material names + part numbers. Scores combined with Reciprocal Rank Fusion (RRF):

```
score = SUM( 1 / (k + rank_i) )  where k=60
```

## Re-Ranking

Two-stage retrieval: fast bi-encoder (top 100) then expensive cross-encoder re-rank (top 10):

| Re-ranker | Type | Best For |
|-----------|------|----------|
| **FlashRank** | Lightweight, open-source | Resource-constrained environments |
| **BAAI/bge-reranker-v2-m3** | Open-source, self-hostable | Multilingual, high quality |
| **Cohere Rerank v3.5** | Commercial | Best quality, $1/1000 queries |
| **ColBERT v2** | Late interaction | Pre-computes token embeddings, fast yet accurate |

## 6-Signal Ranking

Final similarity score uses weighted signals (current weights):

| Signal | Weight | Source |
|--------|--------|--------|
| Visual similarity | 0.50 | DINOv2/Gemini embedding cosine distance |
| Material match | 0.20 | Exact or fuzzy material group matching |
| Dimension proximity | 0.20 | OD, length, width, height, thickness comparison |
| Process overlap | 0.10 | Shared manufacturing processes |
| Tolerance class | Future | IT grade comparison |
| Surface finish | Future | Ra/Rz range comparison |

## Self-Hosted AI Roadmap

Progressive migration from cloud APIs to own fine-tuned models on a single GPU:

**Target hardware**: A6000 (48GB) or RTX 4090 (24GB). All models fit:
- Extraction (Qwen2.5-VL-7B): 5GB
- Agent (Gemma 4): 20GB
- Embeddings (DINOv2): 0.7GB
- Total: 25.7GB

**Fine-tuning costs ($50-80 total over 6 months)**:

| Model | Task | Training Data | Cost |
|-------|------|---------------|------|
| Qwen2.5-VL-7B | Drawing extraction | 200+ drawings | $7-13/run |
| DINOv2 | Visual embeddings | 500+ drawing pairs | $3-5/run |
| Gemma 4 | Agent/reasoning | 500+ conversations | $13-26/run |
| Qwen2.5-7B | Validation | 300+ estimate pairs | $5-10/run |

**Breakeven vs cloud APIs**: ~50-100 active users. Defense on-prem: ship GPU box ($1,800-4,500) with Ubuntu + vLLM + fine-tuned models, air-gapped.

## ML Strategy: Physics First, ML Later

The state-of-the-art approach is **not** "ML replaces physics" -- it is physics model + ML correction factor:

```
Final_Cost = Physics_Cost x ML_Correction_Factor
```

**Why this works**: The physics model captures 80-90% of variance (material, machining time, tooling). ML learns the remaining 10-20% (setup variability, shop-specific factors, systematic bias). ML correction requires far less data than end-to-end ML because it only learns the residual.

### Data Requirements

| Model | Minimum Viable | Good | Excellent |
|-------|---------------|------|-----------|
| ML correction on physics residual | 50-100 parts | 300-500 | 1,000+ |
| XGBoost on tabular features | 100-300 parts | 1,000-3,000 | 10,000+ |
| VLM fine-tuning for extraction | 400 drawings | 1,000 | 5,000+ |
| Similar part embeddings | 100 parts | 500 | 5,000+ |

### Cold Start Strategy

1. **Phase 0 (Now)**: Physics-only. No ML needed. Works without any data.
2. **Phase 1 (First 50-100 users)**: Collect data passively. Log every estimate. Store (estimate, actual_cost) pairs from PO history uploads.
3. **Phase 2 (100+ estimate-actual pairs)**: Train first XGBoost correction model on `[physics_estimate, material, process_count, dimensions] -> actual_cost / physics_cost ratio`.
4. **Phase 3 (500+ parts)**: Embedding-based similar part search. "Similar parts were quoted at Rs 280-350. Our estimate: Rs 320."

**No public manufacturing cost estimation datasets exist.** Cost data is proprietary everywhere. Whoever accumulates the most estimate-vs-actual pairs for Indian manufacturing wins. This is the data moat.

### Open-Source Landscape

Zero mature open-source should-cost tools exist (confirmed by survey of 130+ repos). The closest implementations:
- `kentavv/pymachining` (5 stars): Has actual cutting data and physics models
- `xsession/r3ditor` (Rust): Taylor + MRR + kc1.1 + cost in one module
- `costiqtemp/costiq` (1 star): Laser cutting speed DB by material/thickness

This validates the approach: build the physics engine first, add ML incrementally as data accumulates.

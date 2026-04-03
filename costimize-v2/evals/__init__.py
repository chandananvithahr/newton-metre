"""Newton-Metre AI Evaluation Suite.

Measures quality of:
- Extraction: drawing → structured JSON (field accuracy, schema compliance)
- Agent: user query → correct tool calls (tool selection, argument accuracy)
- Similarity: query drawing → ranked matches (Recall@K, Precision@K, NDCG@K)

Inspired by Karpathy's autoresearch pattern: modify → measure → keep/discard → repeat.
"""

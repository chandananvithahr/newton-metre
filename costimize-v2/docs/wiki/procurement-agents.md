---
slug: procurement-agents
title: Multi-Agent Procurement Framework
keywords: procurement agents, multi-agent, pipeline routing, HITL, approval gates, MESO, negotiation memory, Pactum, checkpoint resume, ABC classification, RFQ, quote comparison, supplier intelligence, forbidden content
sources: MULTI-AGENT-ARCHITECTURE-RESEARCH.md, AI-AGENT-ROADMAP.md
updated: 2026-04-04
---

# Multi-Agent Procurement Framework

Newton-Metre's AI Procurement Worker (Product 3) is an 8-agent framework built in raw Python -- no CrewAI, AutoGen, or LangGraph. It extends the existing `engines/validation/orchestrator.py` pattern with deterministic pipeline routing, parallel execution via ThreadPoolExecutor, and human-in-the-loop approval gates.

## Why Raw Python Over Frameworks

72% of enterprise AI projects now use multi-agent architectures, but framework lock-in is a real risk. Newton-Metre chose raw Python because:

1. The orchestrator.py pattern already exists (parallel execution, confidence tiers, routing)
2. LLM-agnostic by design -- swapping Gemini to vLLM is a config change, not a rewrite
3. Zero vendor lock-in (framework breaking changes do not break agents)
4. Full debuggability when a negotiation agent makes a bad offer
5. Cost control: deterministic routing only calls LLMs when agents actually need reasoning, unlike AutoGen's GroupChat pattern which makes an LLM call per agent turn

## The 8 Agents

| Agent | Role | Wraps |
|-------|------|-------|
| **Extraction** | Drawing analysis (dimensions, processes, material) | `extractors/vision.py` |
| **Cost** | Multi-part-type should-cost calculation | All 4 cost engines |
| **Similarity** | Find similar parts from drawing history | `engines/similarity/searcher.py` |
| **RFQ** | Construct RFQ emails from template + drawing data | New capability |
| **Quote Comparison** | Normalize, compare, and rank vendor quotes vs should-cost | New capability |
| **Negotiation** | Autonomous counter-offers with MESO strategy | New capability |
| **Proposal** | Management-ready procurement proposals | New capability |
| **Meeting** | Pre-meeting briefs + post-meeting analysis | New capability |

## Pipeline Routing

Each workflow type maps to a deterministic sequence of pipeline steps. The LLM never decides which agent runs -- routing is a dict lookup.

```
estimate:          extraction -> cost + similarity (parallel)
rfq:               extraction -> cost + similarity -> rfq [approval]
compare_quotes:    quote_comparison
negotiate:         quote_comparison -> negotiation [approval]
full_procurement:  extraction -> cost + similarity -> rfq [approval]
proposal:          quote_comparison -> proposal
meeting_brief:     meeting
```

Each `PipelineStep` has an `agent_name`, optional `approval_required` flag, and optional `parallel_with` tuple for concurrent execution.

## Three Execution Modes (ABC Classification)

Execution mode is determined by spend value, following standard procurement ABC classification:

| Mode | Spend Range | Behavior |
|------|------------|----------|
| **AUTO** (Class C) | < INR 5K | Agents run end-to-end. Human approves final output only |
| **HITL** (Class B) | INR 5K-50K | Pauses at `approval_required` steps. Human reviews and resumes |
| **MANUAL** (Class A) | > INR 50K | Generates analysis + talking points only. Human leads |

## State Machine

Workflows follow a state machine with 7 states:

```
CREATED -> PLANNING -> AWAITING_APPROVAL -> EXECUTING -> COMPLETED
                |              |                |
                v              v                v
            FAILED      REJECTED          FAILED
                              |
                              v
                          REVISED -> AWAITING_APPROVAL (loop)
```

Every state transition is persisted to Supabase (`agent_workflows` + `agent_checkpoints`). Row-level locking ensures concurrent safety on approval. Full audit trail in `agent_audit_log`.

## MESO Counter-Offers (from Pactum AI Research)

The negotiation agent uses Multiple Equivalent Simultaneous Offers (MESO), a strategy validated by Pactum AI's deployments:

- Sample millions of contract combinations to find optimal counter-offers
- Present multiple equivalent options (different price/payment-term/volume combinations)
- Adjust dynamically: if suppliers consistently accept initial offers, anchor prices decrease
- Track which arguments worked and which failed per supplier

**Pactum's Walmart case study:** 2,000+ suppliers negotiated autonomously, 3% average savings, payment terms extended 35 days. Sanofi: 10% average spend reduction, 281% improvement in negotiation savings via should-cost models + digital negotiations.

**Newton-Metre's advantage over Pactum:** Pactum negotiates without knowing what things SHOULD cost. Newton-Metre has physics-based should-cost as the negotiation baseline.

## 3-Layer Negotiation Memory

The memory architecture creates a compounding moat -- every negotiation makes the system smarter.

**Working Memory (in-process):** Frozen dataclass holding current negotiation context: target price, current offer, concession budget, rounds remaining. Active during a single negotiation session.

**Episodic Memory (per-negotiation):** Stored in Supabase `negotiation_episodes` table. Records what happened: initial quote, should-cost, final price, rounds, which arguments worked, which failed, concessions made, outcome, duration. Enables "last time we negotiated with Vendor X, they accepted 8% below initial quote after round 2."

**Semantic Memory (compounding intelligence):** Stored in Supabase `supplier_intelligence` table. Patterns extracted across episodes: typical discount percentage, average negotiation rounds, response time patterns, quality trends. Evidence count tracks reliability -- patterns supported by more episodes carry higher confidence. Enables "stainless steel fasteners from Gujarat suppliers average 12% below should-cost."

When a procurement manager leaves, their 20 years of supplier knowledge normally leaves with them. The memory layer retains it as institutional knowledge.

## Forbidden Content Scanning

All supplier-facing emails generated by the RFQ and negotiation agents are scanned for forbidden content before sending:
- Should-cost figures (never reveal internal cost estimates to suppliers)
- Target prices or budget amounts
- Competitor pricing data
- Internal approval thresholds

This prevents the most common and damaging procurement communication errors.

## Checkpoint and Resume

The system supports async human approval without blocking agent execution:
1. Agent reaches an `approval_required` step
2. Full context serialized to `agent_checkpoints` table
3. Workflow state transitions to `AWAITING_APPROVAL`
4. Human reviews via API (`POST /api/agent/workflows/{id}/approve`)
5. Human can modify agent state while paused (e.g., adjust target price)
6. On approval, state loaded from checkpoint, pipeline resumes from where it paused
7. On rejection, workflow terminates with rejection reason logged

## Hybrid Architecture (Critical Design Decision)

Following Pactum's validated pattern:
- **Rule-based AI** handles: cost calculation, strategy selection, counter-offer generation, forbidden content scanning -- deterministic, explainable, governable
- **LLMs** handle: supplier communication personalization, profile enrichment, opportunity identification -- flexible, personalized, creative

Newton-Metre's physics engines ARE the rule-based layer. LLMs add the communication layer. This split ensures that the core negotiation logic is explainable and auditable, which is essential for procurement compliance.

## Database Schema

Six migrations support the agent system:
- `005_agent_workflows.sql` -- workflows + checkpoints + audit log (RLS: service_role only)
- `006_suppliers.sql` -- suppliers + contacts (company-scoped)
- `007_negotiation_memory.sql` -- episodes + supplier intelligence
- `008_rfq_templates.sql` -- email templates (default Indian manufacturing template seeded)
- `009_vendor_quotes.sql` -- vendor quotes + quote comparisons
- `010_procurement_proposals.sql` -- proposals with approval tracking

All 183 agent tests pass across 8 test files.

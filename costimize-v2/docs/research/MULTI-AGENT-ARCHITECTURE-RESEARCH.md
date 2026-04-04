# Multi-Agent Architecture for AI Procurement Worker: Research Report

*Generated: 2026-04-04 | Sources: 22 | Confidence: High*

## Executive Summary

Multi-agent AI systems have gone mainstream — 72% of enterprise AI projects now use multi-agent architectures (up from 23% in 2024). For Newton-Metre's AI Procurement Worker (Product 3), the research validates our decision to use **raw Python orchestration over frameworks** (CrewAI/AutoGen/LangGraph), confirms **Pactum's hybrid rule-based + LLM architecture** as the gold standard for autonomous negotiation, and identifies specific patterns for state machines, approval gates, and compounding negotiation memory. Railway is the correct deployment platform for long-running agent workflows.

## 1. Framework vs Raw Python: The Right Call

### Framework Landscape (2026)

| Framework | Pattern | Strengths | Weaknesses |
|-----------|---------|-----------|------------|
| **CrewAI** | Role-based teams | Lowest learning curve, 20 lines to start, 60% of Fortune 500 using it | Teams often migrate to LangGraph for production state management |
| **LangGraph** | Graph-based workflows | Best state management, conditional routing, checkpointing to Postgres/Redis | Vendor lock-in to LangChain ecosystem, heavy abstraction |
| **AutoGen/AG2** | Conversational teams | Natural multi-turn debates | 4-agent x 5 rounds = 20+ LLM calls minimum, expensive |
| **Pydantic AI** | Tool delegation | Type-safe, clean Python patterns, stateless agents | Newer, smaller ecosystem |

### Why Raw Python Wins for Newton-Metre

1. **We already have the pattern** — `engines/validation/orchestrator.py` does parallel execution with ThreadPoolExecutor, confidence tiers, and routing. Extending this is ~300 lines, not a new framework.
2. **LLM-agnostic by design** — Our agent layer talks to any OpenAI-compatible API. Swapping Gemini -> vLLM is a config change. Frameworks impose their own abstraction over this.
3. **Zero vendor lock-in** — CrewAI/LangGraph evolve fast. Breaking changes in framework = your agents break. Raw Python = you control the contract.
4. **Debuggability** — When a negotiation agent makes a bad offer, you need to trace exactly what happened. Framework magic makes this harder.
5. **Cost control** — AutoGen's GroupChat pattern makes an LLM call per agent turn. Our orchestrator routes deterministically, only calling LLMs when agents actually need reasoning.

**Decision: Confirmed.** Raw Python orchestration extending existing `orchestrator.py` pattern.

Sources:
- [CrewAI vs LangGraph vs AutoGen — DataCamp](https://www.datacamp.com/tutorial/crewai-vs-langgraph-vs-autogen)
- [Top 10 Agent Frameworks 2026 — o-mega](https://o-mega.ai/articles/langgraph-vs-crewai-vs-autogen-top-10-agent-frameworks-2026)
- [Agent Framework Comparison — Langfuse](https://langfuse.com/blog/2025-03-19-ai-agent-comparison)
- [Multi-Agent Patterns — Pydantic AI](https://ai.pydantic.dev/multi-agent-applications/)

---

## 2. State Machine & Approval Gate Patterns

### The 3 Approval Models

| Model | How It Works | Use Case |
|-------|-------------|----------|
| **Pre-action** | Agent proposes, human approves, then executes | Class A items (> Rs 50K) |
| **Post-action** | Agent executes, human reviews result | Class C items (< Rs 5K) |
| **Confidence-based** | Auto-execute if confidence > threshold, else ask human | Class B items (Rs 5K-50K) |

### State Machine for Procurement Workflows

```
CREATED -> PLANNING -> AWAITING_APPROVAL -> EXECUTING -> COMPLETED
                |              |                |
                v              v                v
            FAILED      REJECTED          FAILED
                              |
                              v
                          REVISED -> AWAITING_APPROVAL (loop)
```

### Key Implementation Patterns

**Checkpoint + Resume (from LangGraph research, applicable to raw Python):**
- Persist full agent state to Postgres on every transition
- When human approves/rejects, load state from checkpoint and resume
- Enables async approval — agent doesn't block, webhook triggers resume

**State Injection (from Pydantic AI):**
- Human can modify the agent's state while paused (e.g., change target price before resuming negotiation)
- Critical for procurement: manager adjusts parameters before agent continues

**Three Execution Modes:**
- `AUTO` — agent executes and commits (Class C, repeat orders)
- `HITL` — agent executes, human approves before commit (Class B)
- `MANUAL` — human executes, agent advises (Class A strategic)

### Our Implementation

```python
class WorkflowState(str, Enum):
    CREATED = "created"
    PLANNING = "planning"
    AWAITING_APPROVAL = "awaiting_approval"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    REJECTED = "rejected"

@dataclass(frozen=True)
class AgentCheckpoint:
    workflow_id: str
    agent_name: str
    state: WorkflowState
    context: dict          # Full agent context, serializable
    created_at: datetime
    approval_required: bool
    approved_by: str | None
    approved_at: datetime | None
```

Persist to Supabase `agent_checkpoints` table. Resume via `/api/agent/approve/{workflow_id}`.

Sources:
- [Human-in-the-Loop Approval Gate — MachineLearningMastery](https://machinelearningmastery.com/building-a-human-in-the-loop-approval-gate-for-autonomous-agents/)
- [HITL Patterns 2026 — MyEngineeringPath](https://myengineeringpath.dev/genai-engineer/human-in-the-loop/)
- [Temporal HITL Python — Temporal Docs](https://docs.temporal.io/ai-cookbook/human-in-the-loop-python)
- [HITL Middleware Python — FlowHunt](https://www.flowhunt.io/blog/human-in-the-loop-middleware-python-safe-ai-agents/)

---

## 3. AI Procurement: Competitive Landscape & What Works

### Market Reality (2026)

- **80% of global CPOs** plan to deploy generative AI in procurement within 3 years (EY 2025 Global CPO Survey)
- Autonomous procurement cuts sourcing cycle from **2-4 weeks to 2-5 days**
- Managed category savings jump from **3-5% to 8-15% annually**
- Tail spend under management jumps from **20-30% to 70-90%**

### Pactum — The Gold Standard for Autonomous Negotiation

Pactum is the most relevant competitor/reference architecture. Key learnings:

**Hybrid AI Architecture (CRITICAL INSIGHT):**
- **Rule-based AI** handles: offer calculation, strategy selection, contract sampling (thousands of combinations), counter-offer generation (MESO — Multiple Equivalent Simultaneous Offers)
- **LLMs** handle: supplier communication personalization, profile enrichment, opportunity identification
- Rule-based = explainable, governable, deterministic. LLMs = flexible, personalized, creative.
- **Newton-Metre should adopt this split.** Our physics engines ARE the rule-based layer. LLMs add the communication layer.

**Contract Sampling:**
- Pactum samples millions of contract combinations to find optimal counter-offers
- Adjusts dynamically: if suppliers consistently accept initial offers, anchor prices decrease

**Compounding Intelligence:**
- "World's largest database of behavioral negotiation learnings"
- A/B tests negotiation strategies ("10% better savings when negotiations sent on Mondays")
- Observes supplier response semantics (distinguish engagement levels from greeting patterns)

**Walmart Case Study:**
- 2,000+ suppliers negotiated autonomously
- 3% average savings
- Payment terms extended 35 days

**Sanofi Case Study:**
- 10% average spend reduction
- 281% improvement in negotiation savings via should-cost models + digital negotiations

### Other Competitors

| Company | Focus | Architecture |
|---------|-------|-------------|
| **Keelvar** | Autonomous RFQ bots | Initiate events, invite suppliers, evaluate bids, recommend awards |
| **Turian** | Agentic procurement | Parse unstructured docs, communicate with suppliers, reconcile across systems |
| **Inventive AI** | Procurement intelligence | Requisition-to-PO automation |
| **Fluid AI** | Autonomous sourcing | Full workflow automation |

### Newton-Metre's Differentiation

Nobody combines:
1. Should-cost estimation from 2D drawings (our physics engines)
2. Drawing similarity search (our embedding pipeline)
3. Autonomous negotiation with should-cost as leverage
4. Compounding negotiation memory per supplier

Pactum negotiates without knowing what things SHOULD cost. We know. That's the moat.

Sources:
- [State of AI in Procurement 2026 — Art of Procurement](https://artofprocurement.com/blog/state-of-ai-in-procurement)
- [Autonomous Procurement Explained — Fluid AI](https://www.fluid.ai/blog/autonomous-procurement-explained)
- [Pactum Platform Components](https://pactum.com/the-required-components-of-autonomous-negotiations-platform-pactum-platform/)
- [AI Procurement Platforms for Manufacturers — Leverage AI](https://blog.tryleverage.ai/blog/pf/ai-procurement-automation-platforms-manufacturers)
- [Top AI Procurement Tools 2026 — Suplari](https://suplari.com/blog/top-10-ai-procurement-tools)

---

## 4. Agent Memory: The Compounding Moat

### Memory Architecture (Three Layers)

| Layer | What It Stores | How It's Used |
|-------|---------------|---------------|
| **Working Memory** | Current negotiation context, active RFQ, live conversation | Agent's immediate context window |
| **Episodic Memory** | Past negotiations, outcomes, supplier responses | "Last time we negotiated with Vendor X, they accepted 8% below initial quote after round 2" |
| **Semantic Memory** | Supplier profiles, part family patterns, company-wide insights | "Stainless steel fasteners from Gujarat suppliers average 12% below should-cost" |

### Implementation for Newton-Metre

**Episodic (per-negotiation):**
```sql
CREATE TABLE negotiation_episodes (
    id UUID PRIMARY KEY,
    supplier_id UUID REFERENCES suppliers(id),
    part_family TEXT,
    initial_quote DECIMAL,
    should_cost DECIMAL,
    final_price DECIMAL,
    rounds INTEGER,
    arguments_used JSONB,       -- which arguments worked
    arguments_failed JSONB,     -- which arguments didn't work
    concessions_made JSONB,     -- what we gave up
    outcome TEXT,               -- accepted/rejected/expired
    duration_days INTEGER,
    created_at TIMESTAMPTZ
);
```

**Semantic (compounding knowledge graph):**
```sql
CREATE TABLE supplier_intelligence (
    supplier_id UUID REFERENCES suppliers(id),
    pattern_type TEXT,          -- 'price_inflation', 'response_time', 'quality_trend'
    pattern_data JSONB,         -- {"surface_treatment": "+30%", "confidence": 0.85}
    evidence_count INTEGER,     -- how many episodes support this
    last_updated TIMESTAMPTZ
);
```

### Key Insight: Memory as Moat

From IBM and AWS research:
- Memory-enabled agents show compounding improvement over time
- The system becomes an "institutional historian" — captures tacit knowledge that exists only in senior procurement managers' heads
- When a procurement manager leaves, their 20 years of supplier knowledge leaves with them. Our memory layer retains it.
- Hybrid memory (episodic + semantic + graph) outperforms any single approach

**Pactum validates this:** Their "world's largest behavioral negotiation database" is their moat. Ours will be per-company (privacy-preserving) but equally powerful.

Sources:
- [Memory for AI Agents — The New Stack](https://thenewstack.io/memory-for-ai-agents-a-new-paradigm-of-context-engineering/)
- [Context-Aware Memory Systems 2025 — Tribe AI](https://www.tribe.ai/applied-ai/beyond-the-bubble-how-context-aware-memory-systems-are-changing-the-game-in-2025)
- [What Is AI Agent Memory — IBM](https://www.ibm.com/think/topics/ai-agent-memory)
- [AWS AgentCore Long-Term Memory](https://aws.amazon.com/blogs/machine-learning/building-smarter-ai-agents-agentcore-long-term-memory-deep-dive/)
- [Memory Survey arXiv:2512.13564](https://arxiv.org/abs/2512.13564)

---

## 5. Production Deployment: Railway + Supabase

### Why Railway (Not Vercel) for Agent Backend

| Factor | Railway | Vercel |
|--------|---------|--------|
| **Execution time** | Unlimited | 900s max (Pro) |
| **WebSockets** | Native support | No (Edge), limited (Serverless) |
| **Always-on** | Yes, container-based | No, serverless cold starts |
| **Cost at 100K req/mo** | ~$40/mo fixed | ~$45/mo variable |
| **Long-running agents** | Perfect fit | Fundamentally limited |
| **Python/FastAPI** | Docker container, full control | Beta Python support, serverless constraints |

**Architecture:**
- **Frontend (Vercel):** Next.js chat UI, approval gates, dashboards — stays on Vercel
- **Agent Backend (Railway):** FastAPI container, always-on, unlimited execution, WebSocket for real-time agent status
- **State (Supabase):** Agent checkpoints, negotiation memory, workflow state — all in Postgres
- **Queue (Redis on Railway):** Inter-agent message passing, task queue for async workflows

### Cost at Scale

| Scale | Railway | Supabase | Total |
|-------|---------|----------|-------|
| 10 users | $5/mo | Free tier | $5/mo |
| 50 users | $20/mo | $25/mo | $45/mo |
| 200 users | $40/mo | $25/mo | $65/mo |
| 1000 users | $80/mo (2 replicas) | $75/mo | $155/mo |

### Scaling Path

1. **Month 1-3:** Single Railway container, Supabase free tier
2. **Month 4-6:** Add Redis for inter-agent messaging, Supabase Pro
3. **Month 7-12:** Horizontal scaling (Railway replicas), background workers for bulk negotiations
4. **Month 12+:** Self-hosted vLLM on dedicated GPU box, Railway for orchestration only

Sources:
- [AI Agent Deployment: Vercel vs AWS vs Railway — Athenic](https://getathenic.com/blog/ai-agent-deployment-platforms-vercel-aws-railway)
- [Railway Review 2026 — Srvrlss](https://www.srvrlss.io/provider/railway/)
- [AI Agents on Vercel — Vercel KB](https://vercel.com/kb/guide/ai-agents)

---

## 6. Recommended Architecture for Newton-Metre

### Agent Registry

```
agents/
  base.py              # BaseAgent ABC: execute(), plan(), tools
  llm.py               # LLM client (Gemini/OpenAI/vLLM, swap via config)
  engine.py            # AgentEngine: routes queries, manages handoffs
  memory.py            # EpisodicMemory + SemanticMemory + WorkingMemory
  checkpoint.py        # State persistence to Supabase
  
  extraction/          # Wraps extractors/vision.py
  cost/                # Wraps engines/mechanical + sheet_metal + pcb + cable
  similarity/          # Wraps engines/similarity/searcher.py
  rfq/                 # NEW: RFQ construction from template + drawing
  quote_comparison/    # NEW: Normalize + compare vendor quotes vs should-cost
  negotiation/         # NEW: Autonomous email negotiation (Class C)
  meeting/             # NEW: VC/recording analysis, live perspectives
  proposal/            # NEW: Comparative statement + procurement proposal
```

### Orchestration Pattern

```python
class AgentEngine:
    """Routes user queries to the right agent(s).
    
    Extends the orchestrator.py pattern:
    - Deterministic routing (no LLM call to decide which agent)
    - Parallel execution where agents are independent
    - Sequential pipeline where output feeds next agent
    - Approval gates between stages
    """
    
    ROUTING_RULES = {
        "extract": ExtractionAgent,
        "cost": CostAgent,
        "similar": SimilarityAgent,
        "rfq": [ExtractionAgent, CostAgent, RFQAgent],    # Pipeline
        "compare": QuoteComparisonAgent,
        "negotiate": NegotiationAgent,                      # Needs approval gate
        "proposal": [QuoteComparisonAgent, ProposalAgent],  # Pipeline
    }
```

### Data Flow: Full Procurement Pipeline

```
Drawing upload
    |
    v
ExtractionAgent (dimensions, processes, material)
    |
    v
CostAgent (should-cost breakdown) -----> SimilarityAgent (find similar parts + PO history)
    |                                         |
    v                                         v
RFQAgent (construct RFQ from template) <--- merge context
    |
    v
[HUMAN APPROVAL: Send RFQ?] -----> Email to suppliers
    |
    v
QuoteComparisonAgent (normalize quotes vs should-cost)
    |
    v
NegotiationAgent (Class C: autonomous | Class B: assisted | Class A: advise)
    |
    v
[HUMAN APPROVAL: Accept negotiated terms?]
    |
    v
ProposalAgent (comparative statement + savings report)
    |
    v
[HUMAN APPROVAL: Sign procurement proposal?]
    |
    v
PO Generation
```

### Key Design Principles

1. **Rule-based + LLM hybrid** (validated by Pactum): Physics engines calculate, LLMs communicate
2. **Deterministic routing** (no LLM deciding which agent): Pattern matching on intent
3. **Checkpoint every state transition**: Resume from any point after human approval
4. **Per-company memory isolation**: Supplier intelligence never crosses company boundaries
5. **ABC classification drives autonomy level**: Trust ramp from Class C -> B -> A
6. **Every negotiation trains the next one**: Episodic memory compounds into semantic patterns

---

## Methodology

Searched 15+ queries across web search and GitHub code search. Analyzed 22 sources including framework documentation, production case studies, academic surveys, and competitor platforms. Sub-questions investigated: orchestration patterns, state machines, procurement AI landscape, agent memory systems, deployment infrastructure.

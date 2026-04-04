"""Shared types for the agent framework.

All result types are frozen dataclasses (immutable).
Follows the pattern from engines/validation/comparator.py.
"""
import enum
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


class WorkflowState(enum.Enum):
    """State machine for agent workflows."""
    CREATED = "created"
    PLANNING = "planning"
    AWAITING_APPROVAL = "awaiting_approval"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    REJECTED = "rejected"


class ExecutionMode(enum.Enum):
    """How much autonomy the agent has."""
    AUTO = "auto"      # Agent executes and commits (Class C items)
    HITL = "hitl"      # Agent executes, human approves (Class B items)
    MANUAL = "manual"  # Human executes, agent advises (Class A items)


class ItemClassification(enum.Enum):
    """ABC classification for procurement items."""
    CLASS_A = "class_a"  # > threshold_high INR — strategic, human-led
    CLASS_B = "class_b"  # between thresholds — human-assisted
    CLASS_C = "class_c"  # < threshold_low INR — AI-autonomous


# --- Agent Config ---

# ABC thresholds (INR)
CLASS_C_THRESHOLD_INR = 5_000
CLASS_B_THRESHOLD_INR = 50_000

# Agent execution
AGENT_LLM_TIMEOUT_SEC = 60
AGENT_MAX_PIPELINE_WORKERS = 4
CHECKPOINT_TTL_DAYS = 7

# Negotiation
NEGOTIATION_MAX_ROUNDS = 3
NEGOTIATION_DEFAULT_CONCESSION_PCT = 5.0


def classify_item(value_inr: float) -> ItemClassification:
    """Classify a procurement item by value."""
    if value_inr < CLASS_C_THRESHOLD_INR:
        return ItemClassification.CLASS_C
    if value_inr < CLASS_B_THRESHOLD_INR:
        return ItemClassification.CLASS_B
    return ItemClassification.CLASS_A


def mode_for_classification(cls: ItemClassification) -> ExecutionMode:
    """Default execution mode for an item classification."""
    return {
        ItemClassification.CLASS_C: ExecutionMode.AUTO,
        ItemClassification.CLASS_B: ExecutionMode.HITL,
        ItemClassification.CLASS_A: ExecutionMode.MANUAL,
    }[cls]


# --- Result Types ---

@dataclass(frozen=True)
class AgentResult:
    """Uniform result from any agent execution."""
    agent_name: str
    status: str                  # "success" | "error" | "awaiting_approval"
    data: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
    duration_ms: float = 0.0
    llm_calls: int = 0
    cost_usd: float = 0.0


@dataclass(frozen=True)
class WorkflowContext:
    """Full state of a running workflow. Persisted at every checkpoint."""
    workflow_id: str
    user_id: str
    company_id: str
    workflow_type: str
    execution_mode: ExecutionMode
    state: WorkflowState
    inputs: dict[str, Any] = field(default_factory=dict)
    outputs: dict[str, Any] = field(default_factory=dict)
    current_agent: str | None = None
    created_at: str = ""
    updated_at: str = ""

    def with_state(self, new_state: WorkflowState) -> "WorkflowContext":
        """Return a new context with updated state and timestamp."""
        return WorkflowContext(
            workflow_id=self.workflow_id,
            user_id=self.user_id,
            company_id=self.company_id,
            workflow_type=self.workflow_type,
            execution_mode=self.execution_mode,
            state=new_state,
            inputs=self.inputs,
            outputs=self.outputs,
            current_agent=self.current_agent,
            created_at=self.created_at,
            updated_at=datetime.now(timezone.utc).isoformat(),
        )

    def with_outputs(self, new_outputs: dict[str, Any]) -> "WorkflowContext":
        """Return a new context with merged outputs (immutable update)."""
        merged = {**self.outputs, **new_outputs}
        return WorkflowContext(
            workflow_id=self.workflow_id,
            user_id=self.user_id,
            company_id=self.company_id,
            workflow_type=self.workflow_type,
            execution_mode=self.execution_mode,
            state=self.state,
            inputs=self.inputs,
            outputs=merged,
            current_agent=self.current_agent,
            created_at=self.created_at,
            updated_at=datetime.now(timezone.utc).isoformat(),
        )

    def with_agent(self, agent_name: str) -> "WorkflowContext":
        """Return a new context tracking which agent is active."""
        return WorkflowContext(
            workflow_id=self.workflow_id,
            user_id=self.user_id,
            company_id=self.company_id,
            workflow_type=self.workflow_type,
            execution_mode=self.execution_mode,
            state=self.state,
            inputs=self.inputs,
            outputs=self.outputs,
            current_agent=agent_name,
            created_at=self.created_at,
            updated_at=datetime.now(timezone.utc).isoformat(),
        )

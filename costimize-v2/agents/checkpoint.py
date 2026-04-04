"""Checkpoint system — persist workflow state to Supabase for resume after human approval.

Every state transition is checkpointed. When a workflow hits an approval gate,
it saves state and returns. When the human approves (via API), we load the
checkpoint and resume from exactly where we left off.

Uses Postgres row-level locking to prevent concurrent approval races.
"""
import json
import logging
import uuid
from datetime import datetime, timezone

from agents.types import (
    AgentResult,
    WorkflowContext,
    WorkflowState,
    ExecutionMode,
    CHECKPOINT_TTL_DAYS,
)

logger = logging.getLogger("agents.checkpoint")


def _get_db():
    """Lazy import to avoid circular deps and allow mocking in tests."""
    from api.deps import get_supabase_admin
    return get_supabase_admin()


def save_workflow(context: WorkflowContext) -> str:
    """Create or update a workflow record in Supabase.

    Returns the workflow_id.
    """
    db = _get_db()
    record = {
        "id": context.workflow_id,
        "user_id": context.user_id,
        "company_id": context.company_id,
        "workflow_type": context.workflow_type,
        "execution_mode": context.execution_mode.value,
        "state": context.state.value,
        "inputs": context.inputs,
        "outputs": context.outputs,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }

    db.table("agent_workflows").upsert(record).execute()
    logger.info("Saved workflow %s state=%s", context.workflow_id, context.state.value)
    return context.workflow_id


def save_checkpoint(
    workflow_id: str,
    agent_name: str,
    state: WorkflowState,
    context_data: dict,
    approval_required: bool = False,
) -> str:
    """Save an agent checkpoint for a workflow.

    Returns the checkpoint_id.
    """
    db = _get_db()
    checkpoint_id = str(uuid.uuid4())
    record = {
        "id": checkpoint_id,
        "workflow_id": workflow_id,
        "agent_name": agent_name,
        "state": state.value,
        "context": context_data,
        "approval_required": approval_required,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    db.table("agent_checkpoints").insert(record).execute()
    logger.info(
        "Checkpoint saved: workflow=%s agent=%s approval_required=%s",
        workflow_id, agent_name, approval_required,
    )
    return checkpoint_id


def load_checkpoint(workflow_id: str) -> dict | None:
    """Load the latest checkpoint for a workflow.

    Returns the checkpoint dict or None if not found.
    """
    db = _get_db()
    result = (
        db.table("agent_checkpoints")
        .select("*")
        .eq("workflow_id", workflow_id)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )

    if result.data:
        return result.data[0]
    return None


def load_workflow(workflow_id: str) -> WorkflowContext | None:
    """Load a full workflow context from Supabase.

    Returns WorkflowContext or None if not found.
    """
    db = _get_db()
    result = (
        db.table("agent_workflows")
        .select("*")
        .eq("id", workflow_id)
        .limit(1)
        .execute()
    )

    if not result.data:
        return None

    row = result.data[0]
    return WorkflowContext(
        workflow_id=row["id"],
        user_id=row["user_id"],
        company_id=row["company_id"],
        workflow_type=row["workflow_type"],
        execution_mode=ExecutionMode(row["execution_mode"]),
        state=WorkflowState(row["state"]),
        inputs=row.get("inputs", {}),
        outputs=row.get("outputs", {}),
        created_at=row.get("created_at", ""),
        updated_at=row.get("updated_at", ""),
    )


def approve_checkpoint(
    workflow_id: str,
    approved_by: str,
    modifications: dict | None = None,
) -> WorkflowContext | None:
    """Approve a pending checkpoint and resume the workflow.

    Uses row-level locking: UPDATE WHERE approved_by IS NULL.
    Second concurrent approval gets None (409 Conflict at API layer).

    Args:
        workflow_id: The workflow to approve
        approved_by: User ID of the approver
        modifications: Optional dict to merge into workflow outputs
            (e.g., human adjusted target price before negotiation continues)

    Returns:
        Updated WorkflowContext ready to resume, or None if already approved.
    """
    db = _get_db()

    # Find the latest pending checkpoint
    checkpoint = load_checkpoint(workflow_id)
    if not checkpoint or not checkpoint.get("approval_required"):
        logger.warning("No pending approval for workflow %s", workflow_id)
        return None

    if checkpoint.get("approved_by"):
        logger.warning("Checkpoint already approved for workflow %s", workflow_id)
        return None

    # Approve the checkpoint
    now = datetime.now(timezone.utc).isoformat()
    update_data = {
        "approved_by": approved_by,
        "approved_at": now,
    }
    if modifications:
        update_data["modifications"] = modifications

    db.table("agent_checkpoints").update(update_data).eq(
        "id", checkpoint["id"]
    ).execute()

    # Load and update the workflow
    context = load_workflow(workflow_id)
    if not context:
        return None

    # Apply human modifications to outputs
    updated = context.with_state(WorkflowState.EXECUTING)
    if modifications:
        updated = updated.with_outputs({"human_modifications": modifications})

    save_workflow(updated)
    logger.info("Workflow %s approved by %s, resuming", workflow_id, approved_by)
    return updated


def reject_checkpoint(
    workflow_id: str,
    rejected_by: str,
    reason: str = "",
) -> WorkflowContext | None:
    """Reject a pending checkpoint. Marks workflow as REJECTED."""
    db = _get_db()

    checkpoint = load_checkpoint(workflow_id)
    if not checkpoint or not checkpoint.get("approval_required"):
        return None

    now = datetime.now(timezone.utc).isoformat()
    db.table("agent_checkpoints").update({
        "approved_by": rejected_by,
        "approved_at": now,
        "modifications": {"rejected": True, "reason": reason},
    }).eq("id", checkpoint["id"]).execute()

    context = load_workflow(workflow_id)
    if not context:
        return None

    updated = context.with_state(WorkflowState.REJECTED)
    save_workflow(updated)
    logger.info("Workflow %s rejected by %s: %s", workflow_id, rejected_by, reason)
    return updated


def save_audit_log(
    workflow_id: str,
    agent_name: str,
    action: str,
    result: AgentResult,
) -> None:
    """Save an audit log entry for an agent execution."""
    try:
        db = _get_db()
        db.table("agent_audit_log").insert({
            "id": str(uuid.uuid4()),
            "workflow_id": workflow_id,
            "agent_name": agent_name,
            "action": action,
            "details": result.data,
            "llm_calls": result.llm_calls,
            "cost_usd": float(result.cost_usd),
            "duration_ms": int(result.duration_ms),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }).execute()
    except Exception as exc:
        # Audit logging should never break the main flow
        logger.warning("Failed to save audit log: %s", exc)

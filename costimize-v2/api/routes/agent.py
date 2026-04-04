"""Agent workflow API routes.

Endpoints for creating, running, approving, and querying agent workflows.
"""
import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from api.deps import get_current_user_id, get_supabase_admin
from agents.types import ExecutionMode, WorkflowState
from agents.base import AgentRegistry
from agents.engine import AgentEngine, get_available_workflows
from agents.checkpoint import load_workflow, reject_checkpoint

# Import agents
from agents.extraction_agent import ExtractionAgent
from agents.cost_agent import CostAgent
from agents.similarity_agent import SimilarityAgent
from agents.rfq_agent import RFQAgent
from agents.quote_comparison_agent import QuoteComparisonAgent
from agents.negotiation_agent import NegotiationAgent
from agents.proposal_agent import ProposalAgent
from agents.meeting_agent import MeetingAgent

logger = logging.getLogger("api.agent")

router = APIRouter(prefix="/agent", tags=["agent"])

# --- Build the registry ---
_registry = AgentRegistry()
_registry.register(ExtractionAgent())
_registry.register(CostAgent())
_registry.register(SimilarityAgent())
_registry.register(RFQAgent())
_registry.register(QuoteComparisonAgent())
_registry.register(NegotiationAgent())
_registry.register(ProposalAgent())
_registry.register(MeetingAgent())

_engine = AgentEngine(_registry)


# --- Request/Response Models ---

class WorkflowCreateRequest(BaseModel):
    workflow_type: str
    inputs: dict[str, Any] = {}
    execution_mode: str = "hitl"  # "auto" | "hitl" | "manual"


class WorkflowApproveRequest(BaseModel):
    modifications: dict[str, Any] | None = None


class WorkflowRejectRequest(BaseModel):
    reason: str = ""


# --- Endpoints ---

@router.get("/workflows/types")
async def list_workflow_types():
    """List available workflow types and their agent sequences."""
    return {"workflows": get_available_workflows()}


@router.post("/workflows")
async def create_workflow(
    body: WorkflowCreateRequest,
    user_id: str = Depends(get_current_user_id),
):
    """Create and start a new agent workflow."""
    try:
        mode = ExecutionMode(body.execution_mode)
    except ValueError:
        raise HTTPException(400, f"Invalid execution_mode: {body.execution_mode}")

    # Get company_id from user profile (simplified: use user_id for now)
    company_id = body.inputs.get("company_id", user_id)

    try:
        context = _engine.create_workflow(
            workflow_type=body.workflow_type,
            user_id=user_id,
            company_id=company_id,
            inputs=body.inputs,
            execution_mode=mode,
        )
    except ValueError as exc:
        raise HTTPException(400, str(exc))

    # Run the workflow (async in production, sync for now)
    context = _engine.run_workflow(context)

    return {
        "workflow_id": context.workflow_id,
        "state": context.state.value,
        "outputs": context.outputs,
    }


@router.get("/workflows/{workflow_id}")
async def get_workflow(
    workflow_id: str,
    user_id: str = Depends(get_current_user_id),
):
    """Get workflow status and outputs."""
    context = load_workflow(workflow_id)
    if not context:
        raise HTTPException(404, "Workflow not found")
    if context.user_id != user_id:
        raise HTTPException(403, "Not your workflow")

    return {
        "workflow_id": context.workflow_id,
        "workflow_type": context.workflow_type,
        "state": context.state.value,
        "execution_mode": context.execution_mode.value,
        "inputs": context.inputs,
        "outputs": context.outputs,
        "created_at": context.created_at,
        "updated_at": context.updated_at,
    }


@router.post("/workflows/{workflow_id}/approve")
async def approve_workflow(
    workflow_id: str,
    body: WorkflowApproveRequest,
    user_id: str = Depends(get_current_user_id),
):
    """Approve a workflow checkpoint and resume execution."""
    try:
        context = _engine.resume_workflow(
            workflow_id=workflow_id,
            approved_by=user_id,
            modifications=body.modifications,
        )
    except ValueError as exc:
        raise HTTPException(400, str(exc))

    return {
        "workflow_id": context.workflow_id,
        "state": context.state.value,
        "outputs": context.outputs,
    }


@router.post("/workflows/{workflow_id}/reject")
async def reject_workflow(
    workflow_id: str,
    body: WorkflowRejectRequest,
    user_id: str = Depends(get_current_user_id),
):
    """Reject a workflow checkpoint."""
    context = reject_checkpoint(workflow_id, user_id, body.reason)
    if not context:
        raise HTTPException(400, "No pending approval to reject")

    return {
        "workflow_id": context.workflow_id,
        "state": context.state.value,
    }


@router.get("/workflows")
async def list_workflows(
    user_id: str = Depends(get_current_user_id),
    state: str | None = None,
    limit: int = 20,
):
    """List user's workflows, optionally filtered by state."""
    db = get_supabase_admin()
    query = (
        db.table("agent_workflows")
        .select("id, workflow_type, state, execution_mode, created_at, updated_at")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .limit(limit)
    )
    if state:
        query = query.eq("state", state)

    result = query.execute()
    return {"workflows": result.data or []}

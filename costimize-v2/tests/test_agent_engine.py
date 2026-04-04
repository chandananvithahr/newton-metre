"""Tests for AgentEngine — routing, pipelines, parallel execution, approval gates."""
import pytest
from unittest.mock import MagicMock, patch

from agents.types import (
    AgentResult,
    ExecutionMode,
    WorkflowContext,
    WorkflowState,
)
from agents.base import AgentRegistry
from agents.engine import AgentEngine, PipelineStep, PIPELINES


# --- Test Agents ---

class MockAgent:
    """Configurable mock agent for testing pipelines."""

    def __init__(
        self,
        agent_name: str,
        result_data: dict | None = None,
        should_fail: bool = False,
        invalid_input: bool = False,
    ):
        self._name = agent_name
        self._result_data = result_data or {"output": f"{agent_name}_done"}
        self._should_fail = should_fail
        self._invalid_input = invalid_input

    @property
    def name(self) -> str:
        return self._name

    def validate_inputs(self, inputs: dict) -> tuple[bool, str]:
        if self._invalid_input:
            return False, f"{self._name} rejects this input"
        return True, ""

    def execute(self, context: WorkflowContext, inputs: dict) -> AgentResult:
        if self._should_fail:
            raise RuntimeError(f"{self._name} exploded")
        return AgentResult(
            agent_name=self._name,
            status="success",
            data=self._result_data,
            duration_ms=10.0,
            llm_calls=1,
        )


def _make_registry(*agents) -> AgentRegistry:
    reg = AgentRegistry()
    for a in agents:
        reg.register(a)
    return reg


def _make_context(workflow_type: str = "estimate", **kwargs) -> WorkflowContext:
    defaults = {
        "workflow_id": "wf-test",
        "user_id": "u-1",
        "company_id": "c-1",
        "workflow_type": workflow_type,
        "execution_mode": ExecutionMode.HITL,
        "state": WorkflowState.CREATED,
        "inputs": {"image_bytes": b"fake"},
    }
    defaults.update(kwargs)
    return WorkflowContext(**defaults)


# Patch checkpoint functions to avoid Supabase calls
@pytest.fixture(autouse=True)
def mock_checkpoint():
    with patch("agents.engine.save_workflow"), \
         patch("agents.engine.save_checkpoint"), \
         patch("agents.engine.save_audit_log"), \
         patch("agents.engine.approve_checkpoint"):
        yield


# --- Pipeline Definition Tests ---

class TestPipelineDefinitions:
    def test_all_pipeline_types_exist(self):
        expected = {"estimate", "rfq", "compare_quotes", "negotiate",
                    "full_procurement", "proposal", "meeting_brief"}
        assert set(PIPELINES.keys()) == expected

    def test_rfq_pipeline_has_approval(self):
        rfq_steps = PIPELINES["rfq"]
        approval_steps = [s for s in rfq_steps if s.approval_required]
        assert len(approval_steps) == 1
        assert approval_steps[0].agent_name == "rfq"

    def test_estimate_pipeline_has_parallel(self):
        steps = PIPELINES["estimate"]
        cost_step = [s for s in steps if s.agent_name == "cost"][0]
        assert "similarity" in cost_step.parallel_with


# --- Create Workflow Tests ---

class TestCreateWorkflow:
    def test_create_valid_workflow(self):
        reg = _make_registry(MockAgent("extraction"), MockAgent("cost"), MockAgent("similarity"))
        engine = AgentEngine(reg)
        ctx = engine.create_workflow("estimate", "u1", "c1", {"data": "test"})
        assert ctx.state == WorkflowState.CREATED
        assert ctx.workflow_type == "estimate"
        assert ctx.user_id == "u1"

    def test_create_unknown_type_raises(self):
        engine = AgentEngine(_make_registry())
        with pytest.raises(ValueError, match="Unknown workflow type"):
            engine.create_workflow("nonexistent", "u1", "c1", {})


# --- Single Agent Execution Tests ---

class TestSingleAgentExecution:
    def test_single_step_success(self):
        reg = _make_registry(MockAgent("meeting", {"brief": "ready"}))
        engine = AgentEngine(reg)
        ctx = _make_context("meeting_brief")
        result = engine.run_workflow(ctx)
        assert result.state == WorkflowState.COMPLETED
        assert result.outputs["meeting"] == {"brief": "ready"}

    def test_single_step_failure(self):
        reg = _make_registry(MockAgent("meeting", should_fail=True))
        engine = AgentEngine(reg)
        ctx = _make_context("meeting_brief")
        result = engine.run_workflow(ctx)
        assert result.state == WorkflowState.FAILED
        assert "_error" in result.outputs

    def test_single_step_invalid_input(self):
        reg = _make_registry(MockAgent("meeting", invalid_input=True))
        engine = AgentEngine(reg)
        ctx = _make_context("meeting_brief")
        result = engine.run_workflow(ctx)
        assert result.state == WorkflowState.FAILED


# --- Pipeline Execution Tests ---

class TestPipelineExecution:
    def test_sequential_pipeline(self):
        reg = _make_registry(
            MockAgent("extraction", {"dims": "10x20"}),
            MockAgent("cost", {"total": 500}),
            MockAgent("similarity", {"matches": []}),
        )
        engine = AgentEngine(reg)
        ctx = _make_context("estimate")
        result = engine.run_workflow(ctx)
        assert result.state == WorkflowState.COMPLETED
        assert result.outputs["extraction"] == {"dims": "10x20"}
        assert result.outputs["cost"] == {"total": 500}
        assert result.outputs["similarity"] == {"matches": []}

    def test_pipeline_stops_on_failure(self):
        reg = _make_registry(
            MockAgent("extraction", should_fail=True),
            MockAgent("cost"),
            MockAgent("similarity"),
        )
        engine = AgentEngine(reg)
        ctx = _make_context("estimate")
        result = engine.run_workflow(ctx)
        assert result.state == WorkflowState.FAILED
        # Cost agent should NOT have run
        assert "cost" not in result.outputs


# --- Approval Gate Tests ---

class TestApprovalGates:
    def test_hitl_pauses_at_approval(self):
        reg = _make_registry(
            MockAgent("extraction"),
            MockAgent("cost"),
            MockAgent("similarity"),
            MockAgent("rfq", {"rfq_doc": "draft"}),
        )
        engine = AgentEngine(reg)
        ctx = _make_context("rfq", execution_mode=ExecutionMode.HITL)
        result = engine.run_workflow(ctx)
        assert result.state == WorkflowState.AWAITING_APPROVAL
        assert result.outputs["rfq"] == {"rfq_doc": "draft"}

    def test_auto_mode_skips_approval(self):
        reg = _make_registry(
            MockAgent("extraction"),
            MockAgent("cost"),
            MockAgent("similarity"),
            MockAgent("rfq", {"rfq_doc": "draft"}),
        )
        engine = AgentEngine(reg)
        ctx = _make_context("rfq", execution_mode=ExecutionMode.AUTO)
        result = engine.run_workflow(ctx)
        assert result.state == WorkflowState.COMPLETED  # no pause

    def test_manual_mode_pauses_at_approval(self):
        reg = _make_registry(
            MockAgent("extraction"),
            MockAgent("cost"),
            MockAgent("similarity"),
            MockAgent("rfq"),
        )
        engine = AgentEngine(reg)
        ctx = _make_context("rfq", execution_mode=ExecutionMode.MANUAL)
        result = engine.run_workflow(ctx)
        assert result.state == WorkflowState.AWAITING_APPROVAL


# --- Parallel Execution Tests ---

class TestParallelExecution:
    def test_parallel_agents_both_succeed(self):
        reg = _make_registry(
            MockAgent("extraction"),
            MockAgent("cost", {"cost": 100}),
            MockAgent("similarity", {"similar": ["p1"]}),
        )
        engine = AgentEngine(reg)
        ctx = _make_context("estimate")
        result = engine.run_workflow(ctx)
        assert result.state == WorkflowState.COMPLETED
        assert result.outputs["cost"] == {"cost": 100}
        assert result.outputs["similarity"] == {"similar": ["p1"]}

    def test_parallel_one_fails_primary_succeeds(self):
        """If parallel (non-primary) agent fails, workflow continues."""
        reg = _make_registry(
            MockAgent("extraction"),
            MockAgent("cost", {"cost": 100}),
            MockAgent("similarity", should_fail=True),
        )
        engine = AgentEngine(reg)
        ctx = _make_context("estimate")
        result = engine.run_workflow(ctx)
        # Primary (cost) succeeded, so workflow completes
        assert result.state == WorkflowState.COMPLETED
        assert result.outputs["cost"] == {"cost": 100}


# --- Resume Workflow Tests ---

class TestResumeWorkflow:
    def test_resume_calls_approve_and_continues(self):
        reg = _make_registry(
            MockAgent("extraction"),
            MockAgent("cost"),
            MockAgent("similarity"),
            MockAgent("rfq"),
        )
        engine = AgentEngine(reg)

        # Simulate a workflow paused after RFQ
        paused_ctx = _make_context(
            "rfq",
            state=WorkflowState.EXECUTING,
            outputs={
                "_completed_agents": ["extraction", "cost", "similarity", "rfq"],
                "extraction": {}, "cost": {}, "similarity": {}, "rfq": {},
            },
        )

        with patch("agents.engine.approve_checkpoint", return_value=paused_ctx):
            result = engine.resume_workflow("wf-test", "user-approver")
            # All agents already completed, so workflow finishes
            assert result.state == WorkflowState.COMPLETED

    def test_resume_no_pending_raises(self):
        engine = AgentEngine(_make_registry())
        with patch("agents.engine.approve_checkpoint", return_value=None):
            with pytest.raises(ValueError, match="no pending approval"):
                engine.resume_workflow("wf-bad", "user")


# --- Completed Agents Tracking ---

class TestCompletedAgentsTracking:
    def test_completed_agents_tracked_in_outputs(self):
        reg = _make_registry(
            MockAgent("extraction"),
            MockAgent("cost"),
            MockAgent("similarity"),
        )
        engine = AgentEngine(reg)
        ctx = _make_context("estimate")
        result = engine.run_workflow(ctx)
        completed = result.outputs.get("_completed_agents", [])
        assert "extraction" in completed
        assert "cost" in completed
        assert "similarity" in completed

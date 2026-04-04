"""Tests for agent framework: types, base protocol, and registry."""
import pytest
from agents.types import (
    AgentResult,
    WorkflowContext,
    WorkflowState,
    ExecutionMode,
    ItemClassification,
    classify_item,
    mode_for_classification,
    CLASS_C_THRESHOLD_INR,
    CLASS_B_THRESHOLD_INR,
)
from agents.base import AgentRegistry, BaseAgent


# --- Fixtures ---

class DummyAgent:
    """Minimal agent satisfying BaseAgent protocol."""

    def __init__(self, agent_name: str = "dummy") -> None:
        self._name = agent_name

    @property
    def name(self) -> str:
        return self._name

    def validate_inputs(self, inputs: dict) -> tuple[bool, str]:
        if "required_key" not in inputs:
            return False, "missing required_key"
        return True, ""

    def execute(self, context: WorkflowContext, inputs: dict) -> AgentResult:
        return AgentResult(
            agent_name=self._name,
            status="success",
            data={"echo": inputs.get("required_key")},
        )


# --- WorkflowState Tests ---

class TestWorkflowState:
    def test_all_states_exist(self):
        states = {s.value for s in WorkflowState}
        expected = {"created", "planning", "awaiting_approval", "executing",
                    "completed", "failed", "rejected"}
        assert states == expected

    def test_state_from_string(self):
        assert WorkflowState("created") == WorkflowState.CREATED
        assert WorkflowState("awaiting_approval") == WorkflowState.AWAITING_APPROVAL


# --- ExecutionMode Tests ---

class TestExecutionMode:
    def test_all_modes_exist(self):
        modes = {m.value for m in ExecutionMode}
        assert modes == {"auto", "hitl", "manual"}

    def test_mode_from_string(self):
        assert ExecutionMode("auto") == ExecutionMode.AUTO
        assert ExecutionMode("hitl") == ExecutionMode.HITL
        assert ExecutionMode("manual") == ExecutionMode.MANUAL


# --- ItemClassification Tests ---

class TestItemClassification:
    def test_classify_class_c(self):
        assert classify_item(100) == ItemClassification.CLASS_C
        assert classify_item(4999) == ItemClassification.CLASS_C

    def test_classify_class_b(self):
        assert classify_item(5000) == ItemClassification.CLASS_B
        assert classify_item(49999) == ItemClassification.CLASS_B

    def test_classify_class_a(self):
        assert classify_item(50000) == ItemClassification.CLASS_A
        assert classify_item(500000) == ItemClassification.CLASS_A

    def test_classify_zero(self):
        assert classify_item(0) == ItemClassification.CLASS_C

    def test_mode_for_class_c(self):
        assert mode_for_classification(ItemClassification.CLASS_C) == ExecutionMode.AUTO

    def test_mode_for_class_b(self):
        assert mode_for_classification(ItemClassification.CLASS_B) == ExecutionMode.HITL

    def test_mode_for_class_a(self):
        assert mode_for_classification(ItemClassification.CLASS_A) == ExecutionMode.MANUAL


# --- AgentResult Tests ---

class TestAgentResult:
    def test_creation(self):
        r = AgentResult(agent_name="test", status="success", data={"k": "v"})
        assert r.agent_name == "test"
        assert r.status == "success"
        assert r.data == {"k": "v"}
        assert r.error is None
        assert r.llm_calls == 0
        assert r.cost_usd == 0.0

    def test_frozen(self):
        r = AgentResult(agent_name="test", status="success")
        with pytest.raises(AttributeError):
            r.status = "error"  # type: ignore

    def test_with_error(self):
        r = AgentResult(agent_name="test", status="error", error="something broke")
        assert r.error == "something broke"

    def test_defaults(self):
        r = AgentResult(agent_name="x", status="success")
        assert r.data == {}
        assert r.duration_ms == 0.0


# --- WorkflowContext Tests ---

class TestWorkflowContext:
    def _make_context(self, **kwargs):
        defaults = {
            "workflow_id": "wf-1",
            "user_id": "u-1",
            "company_id": "c-1",
            "workflow_type": "rfq",
            "execution_mode": ExecutionMode.HITL,
            "state": WorkflowState.CREATED,
        }
        defaults.update(kwargs)
        return WorkflowContext(**defaults)

    def test_creation(self):
        ctx = self._make_context()
        assert ctx.workflow_id == "wf-1"
        assert ctx.state == WorkflowState.CREATED

    def test_frozen(self):
        ctx = self._make_context()
        with pytest.raises(AttributeError):
            ctx.state = WorkflowState.EXECUTING  # type: ignore

    def test_with_state(self):
        ctx = self._make_context()
        new_ctx = ctx.with_state(WorkflowState.EXECUTING)
        assert new_ctx.state == WorkflowState.EXECUTING
        assert ctx.state == WorkflowState.CREATED  # original unchanged
        assert new_ctx.workflow_id == ctx.workflow_id

    def test_with_outputs(self):
        ctx = self._make_context(outputs={"a": 1})
        new_ctx = ctx.with_outputs({"b": 2})
        assert new_ctx.outputs == {"a": 1, "b": 2}
        assert ctx.outputs == {"a": 1}  # original unchanged

    def test_with_outputs_overwrite(self):
        ctx = self._make_context(outputs={"a": 1})
        new_ctx = ctx.with_outputs({"a": 99})
        assert new_ctx.outputs == {"a": 99}

    def test_with_agent(self):
        ctx = self._make_context()
        new_ctx = ctx.with_agent("extraction")
        assert new_ctx.current_agent == "extraction"
        assert ctx.current_agent is None


# --- AgentRegistry Tests ---

class TestAgentRegistry:
    def test_register_and_get(self):
        reg = AgentRegistry()
        agent = DummyAgent("extraction")
        reg.register(agent)
        assert reg.get("extraction") is agent

    def test_duplicate_raises(self):
        reg = AgentRegistry()
        reg.register(DummyAgent("a"))
        with pytest.raises(ValueError, match="already registered"):
            reg.register(DummyAgent("a"))

    def test_get_missing_raises(self):
        reg = AgentRegistry()
        with pytest.raises(KeyError, match="not found"):
            reg.get("nonexistent")

    def test_list_agents(self):
        reg = AgentRegistry()
        reg.register(DummyAgent("b"))
        reg.register(DummyAgent("a"))
        assert reg.list_agents() == ["a", "b"]  # sorted

    def test_contains(self):
        reg = AgentRegistry()
        reg.register(DummyAgent("x"))
        assert "x" in reg
        assert "y" not in reg

    def test_len(self):
        reg = AgentRegistry()
        assert len(reg) == 0
        reg.register(DummyAgent("a"))
        assert len(reg) == 1


# --- Protocol Conformance Tests ---

class TestBaseAgentProtocol:
    def test_dummy_satisfies_protocol(self):
        agent = DummyAgent()
        assert isinstance(agent, BaseAgent)

    def test_validate_inputs_valid(self):
        agent = DummyAgent()
        valid, reason = agent.validate_inputs({"required_key": "hello"})
        assert valid is True
        assert reason == ""

    def test_validate_inputs_invalid(self):
        agent = DummyAgent()
        valid, reason = agent.validate_inputs({})
        assert valid is False
        assert "required_key" in reason

    def test_execute_returns_result(self):
        agent = DummyAgent("test")
        ctx = WorkflowContext(
            workflow_id="w1", user_id="u1", company_id="c1",
            workflow_type="rfq", execution_mode=ExecutionMode.HITL,
            state=WorkflowState.EXECUTING,
        )
        result = agent.execute(ctx, {"required_key": "value"})
        assert result.agent_name == "test"
        assert result.status == "success"
        assert result.data["echo"] == "value"

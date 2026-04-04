"""AgentEngine — the brain of the multi-agent system.

Extends the orchestrator.py pattern: deterministic routing (dict lookup, not
LLM call), parallel execution via ThreadPoolExecutor, sequential pipelines
where output feeds next agent, and approval gates between stages.

This is the ONLY place that knows which agents exist and how they connect.
"""
import logging
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timezone

from agents.base import AgentRegistry, BaseAgent
from agents.types import (
    AGENT_MAX_PIPELINE_WORKERS,
    AgentResult,
    ExecutionMode,
    WorkflowContext,
    WorkflowState,
)
from agents.checkpoint import (
    approve_checkpoint,
    save_audit_log,
    save_checkpoint,
    save_workflow,
    load_workflow,
)

logger = logging.getLogger("agents.engine")


@dataclass(frozen=True)
class PipelineStep:
    """A step in an agent pipeline."""
    agent_name: str
    approval_required: bool = False  # pause for human approval after this step
    parallel_with: tuple[str, ...] = ()  # run these agents in parallel with this one


# --- Pipeline Definitions ---
# Each workflow type maps to a sequence of pipeline steps.
# This is deterministic routing — no LLM call decides which agent runs.

PIPELINES: dict[str, tuple[PipelineStep, ...]] = {
    "estimate": (
        PipelineStep("extraction"),
        PipelineStep("cost", parallel_with=("similarity",)),
    ),
    "rfq": (
        PipelineStep("extraction"),
        PipelineStep("cost", parallel_with=("similarity",)),
        PipelineStep("rfq", approval_required=True),
    ),
    "compare_quotes": (
        PipelineStep("quote_comparison"),
    ),
    "negotiate": (
        PipelineStep("quote_comparison"),
        PipelineStep("negotiation", approval_required=True),
    ),
    "full_procurement": (
        PipelineStep("extraction"),
        PipelineStep("cost", parallel_with=("similarity",)),
        PipelineStep("rfq", approval_required=True),
        # After RFQ approval and quote upload, next steps trigger separately:
        # PipelineStep("quote_comparison"),
        # PipelineStep("negotiation", approval_required=True),
        # PipelineStep("proposal"),
    ),
    "proposal": (
        PipelineStep("quote_comparison"),
        PipelineStep("proposal"),
    ),
    "meeting_brief": (
        PipelineStep("meeting"),
    ),
}


class AgentEngine:
    """Orchestrates agent pipelines with approval gates.

    Usage:
        engine = AgentEngine(registry)
        context = engine.create_workflow("rfq", user_id, company_id, inputs, mode)
        context = engine.run_workflow(context)
        # If context.state == AWAITING_APPROVAL, human reviews
        # Then: context = engine.resume_workflow(workflow_id, approved_by)
    """

    def __init__(self, registry: AgentRegistry) -> None:
        self._registry = registry

    def create_workflow(
        self,
        workflow_type: str,
        user_id: str,
        company_id: str,
        inputs: dict,
        execution_mode: ExecutionMode = ExecutionMode.HITL,
    ) -> WorkflowContext:
        """Create a new workflow and persist it."""
        if workflow_type not in PIPELINES:
            raise ValueError(
                f"Unknown workflow type: {workflow_type}. "
                f"Available: {', '.join(PIPELINES)}"
            )

        now = datetime.now(timezone.utc).isoformat()
        context = WorkflowContext(
            workflow_id=str(uuid.uuid4()),
            user_id=user_id,
            company_id=company_id,
            workflow_type=workflow_type,
            execution_mode=execution_mode,
            state=WorkflowState.CREATED,
            inputs=inputs,
            created_at=now,
            updated_at=now,
        )

        save_workflow(context)
        logger.info(
            "Created workflow %s type=%s mode=%s",
            context.workflow_id, workflow_type, execution_mode.value,
        )
        return context

    def run_workflow(self, context: WorkflowContext) -> WorkflowContext:
        """Execute a workflow's pipeline from its current position.

        Runs each step in sequence. If a step has parallel_with agents,
        those run concurrently via ThreadPoolExecutor. If a step requires
        approval, pauses the workflow and returns with AWAITING_APPROVAL state.

        Returns:
            Updated WorkflowContext (may be COMPLETED, FAILED, or AWAITING_APPROVAL).
        """
        pipeline = PIPELINES[context.workflow_type]
        context = context.with_state(WorkflowState.EXECUTING)
        save_workflow(context)

        # Find where to resume (skip already-completed agents)
        completed_agents = set(context.outputs.get("_completed_agents", []))

        for step in pipeline:
            if step.agent_name in completed_agents:
                continue

            # Run the step (possibly with parallel agents)
            context, result = self._execute_step(context, step)

            if result.status == "error":
                context = context.with_state(WorkflowState.FAILED)
                context = context.with_outputs({"_error": result.error})
                save_workflow(context)
                return context

            # Track completed agents
            done = list(context.outputs.get("_completed_agents", []))
            done.append(step.agent_name)
            for parallel_name in step.parallel_with:
                done.append(parallel_name)
            context = context.with_outputs({"_completed_agents": done})
            save_workflow(context)

            # Check approval gate
            if step.approval_required and context.execution_mode != ExecutionMode.AUTO:
                context = context.with_state(WorkflowState.AWAITING_APPROVAL)
                save_workflow(context)
                save_checkpoint(
                    workflow_id=context.workflow_id,
                    agent_name=step.agent_name,
                    state=WorkflowState.AWAITING_APPROVAL,
                    context_data=context.outputs,
                    approval_required=True,
                )
                logger.info(
                    "Workflow %s paused for approval after %s",
                    context.workflow_id, step.agent_name,
                )
                return context

        # All steps completed
        context = context.with_state(WorkflowState.COMPLETED)
        save_workflow(context)
        logger.info("Workflow %s completed", context.workflow_id)
        return context

    def resume_workflow(
        self,
        workflow_id: str,
        approved_by: str,
        modifications: dict | None = None,
    ) -> WorkflowContext:
        """Resume a workflow after human approval.

        Loads the workflow, applies any human modifications,
        and continues from where it paused.
        """
        context = approve_checkpoint(workflow_id, approved_by, modifications)
        if not context:
            raise ValueError(f"Cannot resume workflow {workflow_id}: no pending approval")

        return self.run_workflow(context)

    def _execute_step(
        self,
        context: WorkflowContext,
        step: PipelineStep,
    ) -> tuple[WorkflowContext, AgentResult]:
        """Execute a single pipeline step, possibly with parallel agents.

        Returns updated context and the primary agent's result.
        """
        agents_to_run = [step.agent_name] + list(step.parallel_with)

        if len(agents_to_run) == 1:
            # Single agent — run directly
            return self._run_single_agent(context, step.agent_name)

        # Parallel execution
        return self._run_parallel_agents(context, step.agent_name, list(step.parallel_with))

    def _run_single_agent(
        self,
        context: WorkflowContext,
        agent_name: str,
    ) -> tuple[WorkflowContext, AgentResult]:
        """Run a single agent and merge its output into context."""
        agent = self._registry.get(agent_name)
        context = context.with_agent(agent_name)

        # Build inputs: workflow inputs + outputs from prior agents
        inputs = {**context.inputs, **context.outputs}

        # Validate
        valid, reason = agent.validate_inputs(inputs)
        if not valid:
            result = AgentResult(
                agent_name=agent_name,
                status="error",
                error=f"Input validation failed: {reason}",
            )
            save_audit_log(context.workflow_id, agent_name, "validation_failed", result)
            return context, result

        # Execute
        start = time.perf_counter()
        try:
            result = agent.execute(context, inputs)
        except Exception as exc:
            logger.exception("Agent %s failed", agent_name)
            result = AgentResult(
                agent_name=agent_name,
                status="error",
                error=str(exc),
                duration_ms=(time.perf_counter() - start) * 1000,
            )

        # Merge agent output into workflow context
        context = context.with_outputs({agent_name: result.data})
        save_audit_log(context.workflow_id, agent_name, "executed", result)
        return context, result

    def _run_parallel_agents(
        self,
        context: WorkflowContext,
        primary: str,
        parallel: list[str],
    ) -> tuple[WorkflowContext, AgentResult]:
        """Run primary + parallel agents concurrently.

        Returns the primary agent's result. All outputs merged into context.
        Follows the ThreadPoolExecutor pattern from orchestrator.py.
        """
        all_agents = [primary] + parallel
        inputs = {**context.inputs, **context.outputs}
        results: dict[str, AgentResult] = {}

        with ThreadPoolExecutor(max_workers=AGENT_MAX_PIPELINE_WORKERS) as executor:
            futures = {}
            for name in all_agents:
                agent = self._registry.get(name)
                valid, reason = agent.validate_inputs(inputs)
                if not valid:
                    results[name] = AgentResult(
                        agent_name=name,
                        status="error",
                        error=f"Input validation failed: {reason}",
                    )
                    continue
                futures[executor.submit(agent.execute, context, inputs)] = name

            for future in as_completed(futures):
                name = futures[future]
                try:
                    results[name] = future.result(timeout=120)
                except Exception as exc:
                    logger.exception("Parallel agent %s failed", name)
                    results[name] = AgentResult(
                        agent_name=name,
                        status="error",
                        error=str(exc),
                    )

        # Merge all outputs
        for name, result in results.items():
            context = context.with_outputs({name: result.data})
            save_audit_log(context.workflow_id, name, "executed", result)

        primary_result = results.get(primary, AgentResult(
            agent_name=primary,
            status="error",
            error="Primary agent did not produce a result",
        ))
        return context, primary_result


def get_available_workflows() -> dict[str, list[str]]:
    """Return available workflow types and their agent sequences."""
    return {
        wf_type: [step.agent_name for step in steps]
        for wf_type, steps in PIPELINES.items()
    }

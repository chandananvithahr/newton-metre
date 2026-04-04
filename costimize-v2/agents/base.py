"""Base agent protocol and registry.

Agents implement the BaseAgent protocol (duck typing via Protocol).
The AgentRegistry stores agents by name for deterministic routing.
"""
from __future__ import annotations

import logging
from typing import Protocol, runtime_checkable

from agents.types import AgentResult, WorkflowContext

logger = logging.getLogger("agents")


@runtime_checkable
class BaseAgent(Protocol):
    """Protocol that all agents must satisfy.

    Using Protocol (duck typing) instead of ABC — any class with
    these methods qualifies as an agent without explicit inheritance.
    """

    @property
    def name(self) -> str:
        """Unique agent identifier (e.g., 'extraction', 'cost', 'rfq')."""
        ...

    def validate_inputs(self, inputs: dict) -> tuple[bool, str]:
        """Check if inputs are valid before execution.

        Returns:
            (True, "") if valid, (False, "reason") if invalid.
        """
        ...

    def execute(self, context: WorkflowContext, inputs: dict) -> AgentResult:
        """Run the agent's core logic.

        Args:
            context: Current workflow state (immutable).
            inputs: Agent-specific inputs (may include outputs from prior agents).

        Returns:
            AgentResult with status, data, and cost tracking.
        """
        ...


class AgentRegistry:
    """Registry of available agents. Enables deterministic routing by name."""

    def __init__(self) -> None:
        self._agents: dict[str, BaseAgent] = {}

    def register(self, agent: BaseAgent) -> None:
        """Register an agent. Raises ValueError on duplicate name."""
        if agent.name in self._agents:
            raise ValueError(f"Agent already registered: {agent.name}")
        self._agents[agent.name] = agent
        logger.info("Registered agent: %s", agent.name)

    def get(self, name: str) -> BaseAgent:
        """Get an agent by name. Raises KeyError if not found."""
        if name not in self._agents:
            raise KeyError(
                f"Agent not found: {name}. "
                f"Available: {', '.join(self._agents)}"
            )
        return self._agents[name]

    def list_agents(self) -> list[str]:
        """Return sorted list of registered agent names."""
        return sorted(self._agents.keys())

    def __contains__(self, name: str) -> bool:
        return name in self._agents

    def __len__(self) -> int:
        return len(self._agents)

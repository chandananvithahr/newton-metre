"""CostAgent — wraps all 4 cost engines with a uniform agent interface.

Determines part type from extracted data and routes to the correct engine:
mechanical, sheet_metal, pcb, or cable.
"""
import logging
import time
from dataclasses import asdict

from agents.types import AgentResult, WorkflowContext

logger = logging.getLogger("agents.cost")

# Part type detection keywords
_SHEET_METAL_KEYWORDS = {"sheet_metal", "sheet metal", "bracket", "panel", "enclosure"}
_PCB_KEYWORDS = {"pcb", "circuit board", "printed circuit"}
_CABLE_KEYWORDS = {"cable", "wire harness", "wiring"}


def _detect_part_type(inputs: dict) -> str:
    """Determine part type from extraction data or explicit input."""
    # Explicit override
    if "part_type" in inputs:
        return inputs["part_type"]

    # From extraction data
    extraction = inputs.get("extraction", {})
    part_type_raw = extraction.get("part_type", "").lower()
    processes = [p.lower() for p in extraction.get("processes", [])]

    if any(kw in part_type_raw for kw in _SHEET_METAL_KEYWORDS):
        return "sheet_metal"
    if any(kw in part_type_raw for kw in _PCB_KEYWORDS):
        return "pcb"
    if any(kw in part_type_raw for kw in _CABLE_KEYWORDS):
        return "cable"

    # Check processes for sheet metal indicators
    if any(p in ("laser_cutting", "bending", "punching") for p in processes):
        return "sheet_metal"

    # Default to mechanical (turning/milling)
    return "mechanical"


class CostAgent:
    """Routes to the correct cost engine based on part type."""

    @property
    def name(self) -> str:
        return "cost"

    def validate_inputs(self, inputs: dict) -> tuple[bool, str]:
        # Either extraction data or explicit dimensions needed
        has_extraction = "extraction" in inputs
        has_dimensions = "dimensions" in inputs
        if not (has_extraction or has_dimensions):
            return False, "Need 'extraction' data or 'dimensions'"
        return True, ""

    def execute(self, context: WorkflowContext, inputs: dict) -> AgentResult:
        start = time.perf_counter()

        # Merge extraction agent output if available
        extraction = inputs.get("extraction", {})

        part_type = _detect_part_type(inputs)
        quantity = inputs.get("quantity", 1)

        try:
            if part_type == "mechanical":
                result_data = self._calculate_mechanical(extraction, inputs, quantity)
            elif part_type == "sheet_metal":
                result_data = self._calculate_sheet_metal(extraction, inputs, quantity)
            elif part_type == "pcb":
                result_data = self._calculate_pcb(inputs)
            elif part_type == "cable":
                result_data = self._calculate_cable(inputs)
            else:
                return AgentResult(
                    agent_name=self.name,
                    status="error",
                    error=f"Unknown part type: {part_type}",
                )
        except Exception as exc:
            logger.exception("Cost calculation failed for %s", part_type)
            return AgentResult(
                agent_name=self.name,
                status="error",
                error=str(exc),
                duration_ms=(time.perf_counter() - start) * 1000,
            )

        elapsed = (time.perf_counter() - start) * 1000
        result_data["part_type"] = part_type
        return AgentResult(
            agent_name=self.name,
            status="success",
            data=result_data,
            duration_ms=elapsed,
        )

    def _calculate_mechanical(
        self, extraction: dict, inputs: dict, quantity: int,
    ) -> dict:
        from engines.mechanical.cost_engine import calculate_mechanical_cost

        dimensions = inputs.get("dimensions") or extraction.get("dimensions", {})
        material = inputs.get("material_name") or extraction.get("material", "Mild Steel IS2062")
        processes = inputs.get("selected_processes") or extraction.get("processes", [])
        tolerances = inputs.get("has_tight_tolerances", False)

        breakdown = calculate_mechanical_cost(
            dimensions=dimensions,
            material_name=material,
            selected_processes=processes,
            quantity=quantity,
            has_tight_tolerances=tolerances,
        )
        return _breakdown_to_dict(breakdown)

    def _calculate_sheet_metal(
        self, extraction: dict, inputs: dict, quantity: int,
    ) -> dict:
        from engines.sheet_metal.cost_engine import calculate_sheet_metal_cost

        dims = inputs.get("dimensions") or extraction.get("dimensions", {})
        material = inputs.get("material_name") or extraction.get("material", "Mild Steel CR")

        breakdown = calculate_sheet_metal_cost(
            material_name=material,
            thickness_mm=dims.get("thickness_mm", 2.0),
            part_length_mm=dims.get("length_mm", 100),
            part_width_mm=dims.get("width_mm", 100),
            cutting_length_mm=dims.get("cutting_length_mm", 400),
            pierce_count=dims.get("pierce_count", 1),
            n_bends=dims.get("n_bends", 0),
            quantity=quantity,
        )
        return _breakdown_to_dict(breakdown)

    def _calculate_pcb(self, inputs: dict) -> dict:
        from engines.pcb.cost_engine import calculate_pcb_cost

        bom = inputs.get("bom", [])
        quantity = inputs.get("quantity", 1)
        breakdown = calculate_pcb_cost(bom=bom, quantity=quantity)
        return _breakdown_to_dict(breakdown)

    def _calculate_cable(self, inputs: dict) -> dict:
        from engines.cable.cost_engine import calculate_cable_cost

        bom = inputs.get("bom", [])
        quantity = inputs.get("quantity", 1)
        breakdown = calculate_cable_cost(bom=bom, quantity=quantity)
        return _breakdown_to_dict(breakdown)


def _breakdown_to_dict(breakdown) -> dict:
    """Convert a frozen dataclass breakdown to a plain dict."""
    try:
        return asdict(breakdown)
    except Exception:
        # Fallback for non-dataclass results
        return {"raw": str(breakdown)}

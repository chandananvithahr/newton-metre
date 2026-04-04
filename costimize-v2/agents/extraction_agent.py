"""ExtractionAgent — wraps extractors/vision.py with a uniform agent interface.

Accepts image bytes or STEP text, returns extracted dimensions, material,
and processes as an AgentResult.
"""
import logging
import time

from agents.types import AgentResult, WorkflowContext

logger = logging.getLogger("agents.extraction")


class ExtractionAgent:
    """Thin wrapper over the existing drawing extraction pipeline."""

    @property
    def name(self) -> str:
        return "extraction"

    def validate_inputs(self, inputs: dict) -> tuple[bool, str]:
        has_image = "image_bytes" in inputs or "file_bytes" in inputs
        has_images = "images" in inputs
        has_step = "step_text" in inputs
        if not (has_image or has_images or has_step):
            return False, "Need 'image_bytes', 'file_bytes', 'images', or 'step_text'"
        return True, ""

    def execute(self, context: WorkflowContext, inputs: dict) -> AgentResult:
        from extractors.vision import (
            analyze_drawing,
            analyze_multi_view_drawing,
            analyze_step_text,
        )

        start = time.perf_counter()
        llm_calls = 1

        try:
            if "step_text" in inputs:
                result = analyze_step_text(inputs["step_text"])
            elif "images" in inputs:
                result = analyze_multi_view_drawing(inputs["images"])
            else:
                image = inputs.get("image_bytes") or inputs.get("file_bytes")
                filename = inputs.get("filename", "drawing.png")
                result = analyze_drawing(image, filename)
        except Exception as exc:
            logger.exception("Extraction failed")
            return AgentResult(
                agent_name=self.name,
                status="error",
                error=str(exc),
                duration_ms=(time.perf_counter() - start) * 1000,
                llm_calls=llm_calls,
            )

        elapsed = (time.perf_counter() - start) * 1000
        return AgentResult(
            agent_name=self.name,
            status="success",
            data=result,
            duration_ms=elapsed,
            llm_calls=llm_calls,
        )

"""Interactive clarifying question generator for >15% gaps.

Pure logic — no API calls. Analyzes discrepancies between physics and AI
estimates, generates targeted questions for the user to resolve.
Max 2 rounds, max 5 questions per round.
"""
from dataclasses import dataclass
from engines.mechanical.cost_engine import MechanicalCostBreakdown
from engines.mechanical.material_db import list_material_names
from extractors.gemini_estimator import GeminiCostEstimate


@dataclass(frozen=True)
class ClarifyingQuestion:
    """A single clarifying question for the user."""
    field: str            # e.g. "material_name", "outer_diameter_mm", "processes"
    question: str         # human-readable question text
    current_value: str    # what the system currently has
    ai_detected: str      # what the AI detected (may differ)
    options: tuple[str, ...] | None  # for select-type questions


@dataclass(frozen=True)
class InteractiveRound:
    """A round of clarifying questions."""
    round_number: int
    questions: tuple[ClarifyingQuestion, ...]
    reason: str           # why these questions are being asked
    physics_cost: float
    ai_cost: float
    delta_pct: float


MAX_ROUNDS = 2
MAX_QUESTIONS_PER_ROUND = 5


def generate_clarifying_questions(
    physics_result: MechanicalCostBreakdown,
    ai_result: GeminiCostEstimate,
    delta_pct: float,
    current_dimensions: dict | None = None,
    current_processes: list[str] | None = None,
    round_number: int = 1,
) -> InteractiveRound:
    """Analyze the gap and produce targeted questions.

    Round 1: broad questions about material, dimensions, processes.
    Round 2: more specific questions about remaining discrepancies.
    """
    questions: list[ClarifyingQuestion] = []

    if round_number > MAX_ROUNDS:
        return InteractiveRound(
            round_number=round_number,
            questions=(),
            reason="Maximum clarification rounds reached. Showing best available estimate.",
            physics_cost=physics_result.unit_cost,
            ai_cost=ai_result.unit_cost_inr,
            delta_pct=delta_pct,
        )

    # --- Material comparison ---
    physics_mat = physics_result.material_name
    ai_mat = ai_result.detected_material
    if physics_mat.lower() != ai_mat.lower():
        materials = list_material_names()
        questions.append(ClarifyingQuestion(
            field="material_name",
            question=f"Material mismatch: system used '{physics_mat}' but AI detected "
                     f"'{ai_mat}'. Which material is correct?",
            current_value=physics_mat,
            ai_detected=ai_mat,
            options=tuple(materials),
        ))

    # --- Dimension comparison ---
    if current_dimensions and ai_result.detected_dimensions:
        ai_dims = ai_result.detected_dimensions
        for dim_key in ("outer_diameter_mm", "length_mm", "inner_diameter_mm"):
            phys_val = current_dimensions.get(dim_key, 0)
            ai_val = ai_dims.get(dim_key, 0)
            if phys_val > 0 and ai_val > 0:
                dim_delta = abs(phys_val - ai_val) / max(phys_val, ai_val)
                if dim_delta > 0.10:  # >10% difference
                    label = dim_key.replace("_mm", "").replace("_", " ").title()
                    questions.append(ClarifyingQuestion(
                        field=dim_key,
                        question=f"{label} mismatch: system used {phys_val:.1f}mm but "
                                 f"AI detected {ai_val:.1f}mm. What is the correct value?",
                        current_value=f"{phys_val:.1f}mm",
                        ai_detected=f"{ai_val:.1f}mm",
                        options=None,
                    ))

    # --- Process comparison ---
    physics_processes = set(current_processes or [])
    ai_processes = set(ai_result.detected_processes)
    missing_in_physics = ai_processes - physics_processes
    extra_in_physics = physics_processes - ai_processes

    if missing_in_physics:
        questions.append(ClarifyingQuestion(
            field="add_processes",
            question=f"AI detected additional processes not in your selection: "
                     f"{', '.join(sorted(missing_in_physics))}. Should these be included?",
            current_value=", ".join(sorted(physics_processes)),
            ai_detected=", ".join(sorted(ai_processes)),
            options=tuple(sorted(missing_in_physics)),
        ))

    if extra_in_physics and round_number >= 2:
        questions.append(ClarifyingQuestion(
            field="remove_processes",
            question=f"You selected processes AI didn't detect: "
                     f"{', '.join(sorted(extra_in_physics))}. Are these required?",
            current_value=", ".join(sorted(physics_processes)),
            ai_detected=", ".join(sorted(ai_processes)),
            options=tuple(sorted(extra_in_physics)),
        ))

    # --- Cost-line specific questions (round 2) ---
    if round_number >= 2:
        # Check if material cost diverges significantly
        mat_delta = abs(physics_result.material_cost - ai_result.material_cost_inr)
        if physics_result.material_cost > 0:
            mat_pct = mat_delta / physics_result.material_cost * 100
            if mat_pct > 30:
                questions.append(ClarifyingQuestion(
                    field="weight_kg",
                    question=f"Material cost gap: ₹{physics_result.material_cost:.0f} (physics) vs "
                             f"₹{ai_result.material_cost_inr:.0f} (AI). "
                             f"Part weight is {physics_result.raw_weight_kg:.3f} kg — is this correct?",
                    current_value=f"{physics_result.raw_weight_kg:.3f} kg",
                    ai_detected="unknown",
                    options=None,
                ))

    # --- Always ask about hidden features ---
    if round_number == 1 and len(questions) < MAX_QUESTIONS_PER_ROUND:
        questions.append(ClarifyingQuestion(
            field="hidden_features",
            question="Does this part have features not visible in the drawing? "
                     "(internal threads, blind holes, special coatings, etc.)",
            current_value="none specified",
            ai_detected="N/A",
            options=("No hidden features", "Yes — has additional features"),
        ))

    # Cap at max questions
    questions = questions[:MAX_QUESTIONS_PER_ROUND]

    reason = (
        f"Physics (₹{physics_result.unit_cost:.0f}) and AI (₹{ai_result.unit_cost_inr:.0f}) "
        f"disagree by {delta_pct:.1f}%. Please verify the following to get an accurate estimate."
    )

    return InteractiveRound(
        round_number=round_number,
        questions=tuple(questions),
        reason=reason,
        physics_cost=physics_result.unit_cost,
        ai_cost=ai_result.unit_cost_inr,
        delta_pct=delta_pct,
    )

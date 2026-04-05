"""Orchestrator agent — the brain of the validation pipeline.

Runs physics engine and Gemini estimator in PARALLEL (ThreadPoolExecutor),
compares results, and routes to sub-agents based on confidence tier:
  HIGH/MEDIUM → return directly
  LOW → spawn arbitrator agent
  INSUFFICIENT → spawn interactive agent

Also manages the training data pipeline: every validated estimate is
persisted for future ML model training (Phase 4).
"""
from concurrent.futures import ThreadPoolExecutor, Future
from dataclasses import dataclass
from datetime import datetime, timezone

from engines.mechanical.cost_engine import (
    MechanicalCostBreakdown,
    calculate_mechanical_cost,
)
from engines.validation.comparator import (
    ComparisonResult,
    ConfidenceTier,
    compare_estimates,
)
from engines.validation.arbitrator import ArbitrationResult, arbitrate
from engines.validation.interactive import (
    InteractiveRound,
    generate_clarifying_questions,
)
from engines.validation.data_collector import (
    ValidatedEstimate,
    save_validated_estimate,
)
from extractors.gemini_estimator import GeminiCostEstimate, estimate_cost_from_drawing


@dataclass(frozen=True)
class ValidationResult:
    """Complete result from the orchestrator — everything the UI needs."""
    physics_result: MechanicalCostBreakdown
    ai_result: GeminiCostEstimate | None       # None if Gemini failed
    comparison: ComparisonResult | None        # None if Gemini failed
    arbitration: ArbitrationResult | None      # only for LOW tier
    interactive: InteractiveRound | None       # only for INSUFFICIENT tier
    final_cost: float                          # the cost to show the user
    confidence_tier: ConfidenceTier | None     # None if degraded
    degraded: bool                             # True if Gemini failed


def orchestrate(
    image_bytes: bytes | None,
    dimensions: dict,
    material_name: str,
    selected_processes: list[str],
    quantity: int,
    has_tight_tolerances: bool = False,
    user_answers: dict | None = None,
    round_number: int = 1,
    material_override=None,
    is_dynamic_material: bool = False,
    gdt_symbols: list[str] | None = None,
    surface_treatment_id: str | None = None,
    heat_treatment_id: str | None = None,
    machine_tier: str = "cnc_3axis",
) -> ValidationResult:
    """The brain. Runs physics + Gemini in parallel, compares, routes to sub-agents.

    Args:
        image_bytes: Drawing image (None = skip AI validation, manual entry only)
        dimensions: Part dimensions dict
        material_name: Material name
        selected_processes: List of process IDs
        quantity: Batch size
        has_tight_tolerances: Whether tight tolerances apply
        user_answers: Answers from previous interactive round (for recalculation)
        round_number: Current interactive round (1 or 2)

    Returns:
        ValidationResult with all context the UI needs
    """
    # Apply user corrections from interactive round
    if user_answers:
        dimensions, material_name, selected_processes = _apply_user_corrections(
            dimensions, material_name, selected_processes, user_answers,
        )

    # --- PARALLEL EXECUTION ---
    if image_bytes:
        physics_result, ai_result = _run_parallel(
            image_bytes, dimensions, material_name,
            selected_processes, quantity, has_tight_tolerances,
            gdt_symbols=gdt_symbols or [],
        )
    else:
        # No image = manual entry, skip Gemini validation
        physics_result = calculate_mechanical_cost(
            dimensions=dimensions,
            material_name=material_name,
            selected_processes=selected_processes,
            quantity=quantity,
            has_tight_tolerances=has_tight_tolerances,
            material_override=material_override,
            is_dynamic_material=is_dynamic_material,
            gdt_symbols=gdt_symbols or [],
            surface_treatment_id=surface_treatment_id,
            heat_treatment_id=heat_treatment_id,
            machine_tier=machine_tier,
        )
        ai_result = None

    # --- DEGRADED MODE (no AI result) ---
    if ai_result is None:
        _save_training_data(
            physics_result=physics_result,
            ai_result=None,
            final_cost=physics_result.unit_cost,
            confidence_tier="degraded",
            delta_pct=0.0,
            drawing_filename="manual_entry",
        )
        return ValidationResult(
            physics_result=physics_result,
            ai_result=None,
            comparison=None,
            arbitration=None,
            interactive=None,
            final_cost=physics_result.unit_cost,
            confidence_tier=None,
            degraded=True,
        )

    # --- COMPARE ---
    comparison = compare_estimates(physics_result.unit_cost, ai_result.unit_cost_inr)

    # --- ROUTE BY CONFIDENCE TIER ---
    arbitration = None
    interactive = None
    final_cost = physics_result.unit_cost  # default: trust physics

    if comparison.confidence_tier == ConfidenceTier.HIGH:
        final_cost = physics_result.unit_cost

    elif comparison.confidence_tier == ConfidenceTier.MEDIUM:
        final_cost = physics_result.unit_cost  # flag but still use physics

    elif comparison.confidence_tier == ConfidenceTier.LOW:
        # Spawn arbitrator agent
        arbitration = arbitrate(
            physics_result=physics_result,
            ai_result=ai_result,
            quantity=quantity,
            delta_pct=comparison.delta_pct,
        )
        final_cost = arbitration.recommended_cost

    elif comparison.confidence_tier == ConfidenceTier.INSUFFICIENT:
        # Spawn interactive agent
        interactive = generate_clarifying_questions(
            physics_result=physics_result,
            ai_result=ai_result,
            delta_pct=comparison.delta_pct,
            current_dimensions=dimensions,
            current_processes=selected_processes,
            round_number=round_number,
        )
        final_cost = physics_result.unit_cost  # preliminary until user answers

    # --- SAVE TRAINING DATA ---
    _save_training_data(
        physics_result=physics_result,
        ai_result=ai_result,
        final_cost=final_cost,
        confidence_tier=comparison.confidence_tier.value,
        delta_pct=comparison.delta_pct,
        drawing_filename="uploaded_drawing",
        arbitration_reasoning=(
            arbitration.overall_reasoning if arbitration else None
        ),
    )

    return ValidationResult(
        physics_result=physics_result,
        ai_result=ai_result,
        comparison=comparison,
        arbitration=arbitration,
        interactive=interactive,
        final_cost=final_cost,
        confidence_tier=comparison.confidence_tier,
        degraded=False,
    )


def _run_parallel(
    image_bytes: bytes,
    dimensions: dict,
    material_name: str,
    selected_processes: list[str],
    quantity: int,
    has_tight_tolerances: bool,
    gdt_symbols: list[str] | None = None,
) -> tuple[MechanicalCostBreakdown, GeminiCostEstimate | None]:
    """Run physics engine and Gemini estimator in parallel using ThreadPoolExecutor."""
    with ThreadPoolExecutor(max_workers=2) as executor:
        physics_future: Future[MechanicalCostBreakdown] = executor.submit(
            calculate_mechanical_cost,
            dimensions=dimensions,
            material_name=material_name,
            selected_processes=selected_processes,
            quantity=quantity,
            has_tight_tolerances=has_tight_tolerances,
            gdt_symbols=gdt_symbols or [],
        )
        gemini_future: Future[GeminiCostEstimate] = executor.submit(
            estimate_cost_from_drawing,
            image_bytes=image_bytes,
            quantity=quantity,
            material_hint=material_name,
        )

        # Physics engine should never fail (it's our code)
        physics_result = physics_future.result(timeout=30)

        # Gemini can fail — graceful degradation
        try:
            ai_result = gemini_future.result(timeout=30)
        except Exception:
            ai_result = None

    return physics_result, ai_result


def _apply_user_corrections(
    dimensions: dict,
    material_name: str,
    selected_processes: list[str],
    user_answers: dict,
) -> tuple[dict, str, list[str]]:
    """Apply user answers from interactive round to update inputs."""
    # Material correction
    if "material_name" in user_answers:
        material_name = user_answers["material_name"]

    # Dimension corrections
    new_dims = dict(dimensions)
    for key in ("outer_diameter_mm", "length_mm", "inner_diameter_mm"):
        if key in user_answers:
            new_dims[key] = float(user_answers[key])

    # Process corrections
    new_processes = list(selected_processes)
    if "add_processes" in user_answers:
        for p in user_answers["add_processes"]:
            if p not in new_processes:
                new_processes.append(p)
    if "remove_processes" in user_answers:
        new_processes = [p for p in new_processes if p not in user_answers["remove_processes"]]

    return new_dims, material_name, new_processes


def _save_training_data(
    physics_result: MechanicalCostBreakdown,
    ai_result: GeminiCostEstimate | None,
    final_cost: float,
    confidence_tier: str,
    delta_pct: float,
    drawing_filename: str,
    arbitration_reasoning: str | None = None,
) -> None:
    """Save validated estimate as training data for future ML models.

    This is the training data pipeline: every estimate (whether validated
    automatically via HIGH confidence or manually via interactive loop)
    becomes a training example. After 50-100 pairs, ML correction factors
    can be trained.
    """
    try:
        record = ValidatedEstimate(
            timestamp=datetime.now(timezone.utc).isoformat(),
            drawing_filename=drawing_filename,
            material_name=physics_result.material_name,
            dimensions={},  # filled from physics result context
            processes=tuple(pl.process_id for pl in physics_result.process_lines),
            quantity=physics_result.quantity,
            physics_cost=physics_result.unit_cost,
            ai_cost=ai_result.unit_cost_inr if ai_result else None,
            final_cost=final_cost,
            confidence_tier=confidence_tier,
            delta_pct=delta_pct,
            user_corrections={},
            arbitration_reasoning=arbitration_reasoning,
        )
        save_validated_estimate(record)
    except Exception:
        pass  # Don't let training data persistence break the main flow

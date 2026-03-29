"""Compare physics engine vs AI cost estimates — assign confidence tiers.

Pure math module. No API calls. All functions are deterministic.
"""
import enum
from dataclasses import dataclass


class ConfidenceTier(enum.Enum):
    """Confidence level based on delta between physics and AI estimates."""
    HIGH = "high"                # delta ≤ 3%
    MEDIUM = "medium"            # 3% < delta ≤ 7%
    LOW = "low"                  # 7% < delta ≤ 15%
    INSUFFICIENT = "insufficient"  # delta > 15%


@dataclass(frozen=True)
class ComparisonResult:
    """Result of comparing physics and AI cost estimates."""
    physics_cost: float
    ai_cost: float
    delta_pct: float
    confidence_tier: ConfidenceTier


def compare_estimates(physics_cost: float, ai_cost: float) -> ComparisonResult:
    """Compare two cost estimates and assign a confidence tier.

    Delta is computed as |physics - ai| / max(physics, ai) × 100.
    Both zero → HIGH (agreement). One zero → INSUFFICIENT.

    Raises ValueError if either cost is negative.
    """
    if physics_cost < 0 or ai_cost < 0:
        raise ValueError(
            f"Costs must be non-negative: physics={physics_cost}, ai={ai_cost}"
        )

    denominator = max(physics_cost, ai_cost)
    if denominator == 0:
        # Both are zero — perfect agreement
        return ComparisonResult(
            physics_cost=0.0,
            ai_cost=0.0,
            delta_pct=0.0,
            confidence_tier=ConfidenceTier.HIGH,
        )

    delta_pct = abs(physics_cost - ai_cost) / denominator * 100

    if delta_pct <= 3.0:
        tier = ConfidenceTier.HIGH
    elif delta_pct <= 7.0:
        tier = ConfidenceTier.MEDIUM
    elif delta_pct <= 15.0:
        tier = ConfidenceTier.LOW
    else:
        tier = ConfidenceTier.INSUFFICIENT

    return ComparisonResult(
        physics_cost=physics_cost,
        ai_cost=ai_cost,
        delta_pct=round(delta_pct, 2),
        confidence_tier=tier,
    )

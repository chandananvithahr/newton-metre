"""Sheet metal cost engine — line-by-line should-cost breakdown.

Physics-based cost model using:
  - Laser cutting speeds by material × thickness (from cutting_db.py)
  - Press brake tonnage + bend time calculations (from bending_db.py)
  - Material nesting utilization estimates
  - Indian manufacturing job shop rates (₹ INR)
"""
import math
from dataclasses import dataclass

from config import OVERHEAD_PCT, PROFIT_PCT, LABOUR_RATE, POWER_RATE
from engines.sheet_metal.material_db import (
    get_sheet_material,
    calculate_blank_weight_kg,
    estimate_utilization_pct,
    SheetMaterial,
)
from engines.sheet_metal.cutting_db import (
    estimate_laser_cutting_time_min,
    estimate_laser_cutting_cost,
    LASER_MACHINE_RATE,
    LASER_POWER_KW,
)
from engines.sheet_metal.bending_db import (
    estimate_bending_cost,
    BEND_SETUP_FIRST_MIN,
)


# Surface finish rates (₹/sq.m)
FINISH_RATES: dict[str, float] = {
    "powder_coating": 120,
    "zinc_plating": 250,
    "anodizing": 350,
    "passivation": 50,
    "paint": 100,
    "galvanizing": 60,
    "none": 0,
}

# Welding rates
WELD_RATE_PER_M: dict[str, float] = {
    "mig": 18,      # ₹/meter of weld
    "tig": 40,
    "spot": 4,      # ₹/spot (not per meter)
}
WELD_SETUP_MIN = 20


@dataclass(frozen=True)
class SheetMetalCostLine:
    item: str
    description: str
    cost_inr: float


@dataclass(frozen=True)
class SheetMetalCostBreakdown:
    material_name: str
    thickness_mm: float
    blank_weight_kg: float
    material_cost: float
    cutting_cost: float
    bending_cost: float
    welding_cost: float
    finish_cost: float
    total_setup_cost: float
    total_labour_cost: float
    total_power_cost: float
    lines: tuple[SheetMetalCostLine, ...]
    subtotal: float
    overhead: float
    profit: float
    unit_cost: float
    order_cost: float
    quantity: int
    utilization_pct: float


def calculate_sheet_metal_cost(
    material_name: str,
    thickness_mm: float,
    part_length_mm: float,
    part_width_mm: float,
    cutting_length_mm: float,
    pierce_count: int,
    n_bends: int = 0,
    bend_length_mm: float | None = None,
    bend_complexity: str = "simple",
    n_tool_changes: int = 0,
    weld_type: str | None = None,
    weld_length_mm: float = 0,
    weld_spot_count: int = 0,
    finish_type: str = "none",
    quantity: int = 1,
    has_tight_tolerances: bool = False,
) -> SheetMetalCostBreakdown:
    """Calculate full should-cost breakdown for a sheet metal part.

    Args:
        material_name: Key from SHEET_MATERIALS (e.g. "Mild Steel CR").
        thickness_mm: Sheet thickness in mm.
        part_length_mm: Part bounding box length (for nesting).
        part_width_mm: Part bounding box width (for nesting).
        cutting_length_mm: Total laser cutting perimeter in mm.
        pierce_count: Number of pierce points (holes + outer contour start).
        n_bends: Number of bends.
        bend_length_mm: Average bend length in mm (defaults to part_width_mm).
        bend_complexity: "simple", "standard", "complex", "hemming", or "z_bend".
        n_tool_changes: Number of press brake tool changes.
        weld_type: "mig", "tig", "spot", or None.
        weld_length_mm: Total weld length in mm (for mig/tig).
        weld_spot_count: Number of spot welds.
        finish_type: Key from FINISH_RATES.
        quantity: Order quantity.
        has_tight_tolerances: Adds 30% surcharge if True.

    Returns:
        SheetMetalCostBreakdown with per-line detail.
    """
    mat = get_sheet_material(material_name)
    lines: list[SheetMetalCostLine] = []

    # --- Material Cost ---
    utilization = estimate_utilization_pct(part_length_mm, part_width_mm)
    blank_weight = calculate_blank_weight_kg(
        part_length_mm, part_width_mm, thickness_mm, mat.density_kg_per_m3,
    )
    # Account for utilization loss: you buy the whole sheet
    material_cost = (blank_weight * mat.price_per_kg_inr) / (utilization / 100)
    lines.append(SheetMetalCostLine(
        "Material", f"{mat.name} {thickness_mm}mm, {blank_weight:.3f} kg, "
                    f"{utilization:.0f}% util", round(material_cost, 2),
    ))

    # --- Laser Cutting ---
    cutting_cost = estimate_laser_cutting_cost(
        material_name, thickness_mm, cutting_length_mm, pierce_count,
    )
    if has_tight_tolerances:
        cutting_cost *= 1.30
    cut_time_min = estimate_laser_cutting_time_min(
        material_name, thickness_mm, cutting_length_mm, pierce_count,
    )
    lines.append(SheetMetalCostLine(
        "Laser Cutting",
        f"{cutting_length_mm:.0f}mm perimeter, {pierce_count} pierces, "
        f"{cut_time_min:.1f} min",
        round(cutting_cost, 2),
    ))

    # --- Bending ---
    bending_cost = 0.0
    bending_setup_cost = 0.0
    if n_bends > 0:
        bl = bend_length_mm if bend_length_mm is not None else part_width_mm
        cycle_cost, setup_per_unit = estimate_bending_cost(
            mat.uts_mpa, thickness_mm, bl, n_bends,
            n_tool_changes, bend_complexity, quantity,
        )
        bending_cost = cycle_cost
        bending_setup_cost = setup_per_unit
        if has_tight_tolerances:
            bending_cost *= 1.30
        lines.append(SheetMetalCostLine(
            "Bending",
            f"{n_bends} bends ({bend_complexity}), {bl:.0f}mm length",
            round(bending_cost, 2),
        ))

    # --- Welding ---
    welding_cost = 0.0
    if weld_type and (weld_length_mm > 0 or weld_spot_count > 0):
        if weld_type == "spot":
            welding_cost = weld_spot_count * WELD_RATE_PER_M["spot"]
            desc = f"{weld_spot_count} spot welds"
        else:
            rate_per_m = WELD_RATE_PER_M.get(weld_type, WELD_RATE_PER_M["mig"])
            welding_cost = (weld_length_mm / 1000) * rate_per_m
            desc = f"{weld_type.upper()} {weld_length_mm:.0f}mm"
        # Add setup cost amortized
        weld_setup_cost = (WELD_SETUP_MIN / 60 * LABOUR_RATE) / quantity
        welding_cost += weld_setup_cost
        lines.append(SheetMetalCostLine("Welding", desc, round(welding_cost, 2)))

    # --- Surface Finish ---
    finish_cost = 0.0
    if finish_type != "none":
        rate = FINISH_RATES.get(finish_type, 0)
        # Approximate surface area: 2 × (L×W) for both sides
        area_sqm = 2 * (part_length_mm / 1000) * (part_width_mm / 1000)
        finish_cost = area_sqm * rate
        lines.append(SheetMetalCostLine(
            "Surface Finish",
            f"{finish_type.replace('_', ' ').title()}, {area_sqm:.3f} sq.m",
            round(finish_cost, 2),
        ))

    # --- Setup (laser + bending) ---
    # Laser setup: 10 min per batch (program load, material load)
    laser_setup_per_unit = ((10 / 60) * LASER_MACHINE_RATE) / quantity
    total_setup = laser_setup_per_unit + bending_setup_cost
    lines.append(SheetMetalCostLine(
        "Setup (amortized)", f"Qty {quantity}", round(total_setup, 2),
    ))

    # --- Labour ---
    # Operator time: cutting is mostly automated, bending + handling is manual
    handling_min = 1.0  # load/unload per part
    bend_labour_min = (n_bends * 0.3) if n_bends > 0 else 0
    total_labour_min = handling_min + bend_labour_min
    labour_cost = (total_labour_min / 60) * LABOUR_RATE
    lines.append(SheetMetalCostLine(
        "Labour", f"{total_labour_min:.1f} min handling + bending",
        round(labour_cost, 2),
    ))

    # --- Power ---
    power_cost = (cut_time_min / 60) * LASER_POWER_KW * POWER_RATE
    lines.append(SheetMetalCostLine(
        "Power", f"{cut_time_min:.1f} min × {LASER_POWER_KW}kW",
        round(power_cost, 2),
    ))

    # --- Totals ---
    subtotal = (
        material_cost + cutting_cost + bending_cost + welding_cost
        + finish_cost + total_setup + labour_cost + power_cost
    )
    overhead = subtotal * (OVERHEAD_PCT / 100)
    profit = (subtotal + overhead) * (PROFIT_PCT / 100)
    unit_cost = round(subtotal + overhead + profit, 2)
    order_cost = round(unit_cost * quantity, 2)

    return SheetMetalCostBreakdown(
        material_name=material_name,
        thickness_mm=thickness_mm,
        blank_weight_kg=round(blank_weight, 3),
        material_cost=round(material_cost, 2),
        cutting_cost=round(cutting_cost, 2),
        bending_cost=round(bending_cost, 2),
        welding_cost=round(welding_cost, 2),
        finish_cost=round(finish_cost, 2),
        total_setup_cost=round(total_setup, 2),
        total_labour_cost=round(labour_cost, 2),
        total_power_cost=round(power_cost, 2),
        lines=tuple(lines),
        subtotal=round(subtotal, 2),
        overhead=round(overhead, 2),
        profit=round(profit, 2),
        unit_cost=unit_cost,
        order_cost=order_cost,
        quantity=quantity,
        utilization_pct=round(utilization, 1),
    )

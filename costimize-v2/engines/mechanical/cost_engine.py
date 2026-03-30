"""Multi-process mechanical cost engine — line-by-line should-cost breakdown.

Physics-based cost model using:
  - MRR-based machining time (from process_db.py)
  - Taylor tool life equation for tooling wear cost
  - Kp × MRR for actual cutting power
  - Indian manufacturing job shop rates (₹ INR)
"""
import math
from dataclasses import dataclass
from config import (
    LABOUR_RATE,
    POWER_RATE,
    MATERIAL_WASTAGE_PCT,
    MACHINING_ALLOWANCE_DIA_MM,
    MACHINING_ALLOWANCE_LEN_MM,
    TIGHT_TOLERANCE_SURCHARGE_PCT,
    OVERHEAD_PCT,
    PROFIT_PCT,
)
from engines.mechanical.material_db import get_material, Material
from engines.mechanical.process_db import load_processes, estimate_process_time_min, ProcessInfo
from engines.mechanical.cutting_data import (
    get_cutting_data,
    calculate_tool_cost_per_min,
    calculate_cutting_power_kw,
    calculate_corrected_kc,
    CARBIDE_EDGE_COST_INR,
    KW_DEFAULT,
    KSP_TURNING,
    KSP_MILLING,
    KSP_DRILLING,
)


@dataclass(frozen=True)
class ProcessCostLine:
    process_id: str
    process_name: str
    time_min: float
    machine_cost: float
    setup_cost_per_unit: float
    tooling_cost: float
    labour_cost: float
    power_cost: float


@dataclass(frozen=True)
class MechanicalCostBreakdown:
    material_name: str
    raw_weight_kg: float
    wastage_weight_kg: float
    material_cost: float
    process_lines: tuple[ProcessCostLine, ...]
    total_machining_cost: float
    total_setup_cost: float
    total_tooling_cost: float
    total_labour_cost: float
    total_power_cost: float
    subtotal: float
    overhead: float
    profit: float
    unit_cost: float
    order_cost: float
    quantity: int


def calculate_mechanical_cost(
    dimensions: dict,
    material_name: str,
    selected_processes: list[str],
    quantity: int,
    has_tight_tolerances: bool = False,
    material_override: "Material | None" = None,
) -> MechanicalCostBreakdown:
    material = material_override if material_override is not None else get_material(material_name)
    all_processes = load_processes()
    # For dynamic materials not in cutting DB, machinability-based fallback kicks in automatically
    cd = get_cutting_data(material_name, machinability=material.machinability)

    # --- Raw Material Cost ---
    od = dimensions.get("outer_diameter_mm", 0)
    id_mm = dimensions.get("inner_diameter_mm", 0)
    length = dimensions.get("length_mm", 0)

    bar_od_mm = od + MACHINING_ALLOWANCE_DIA_MM
    bar_len_mm = length + MACHINING_ALLOWANCE_LEN_MM
    bar_od_m = bar_od_mm / 1000
    bar_len_m = bar_len_mm / 1000

    if id_mm > 0:
        bar_id_m = id_mm / 1000
        volume_m3 = (
            math.pi * ((bar_od_m / 2) ** 2 - (bar_id_m / 2) ** 2) * bar_len_m
        )
    else:
        volume_m3 = math.pi * (bar_od_m / 2) ** 2 * bar_len_m

    raw_weight_kg = volume_m3 * material.density_kg_per_m3
    wastage_weight_kg = raw_weight_kg * (MATERIAL_WASTAGE_PCT / 100)
    total_weight_kg = raw_weight_kg + wastage_weight_kg
    material_cost = total_weight_kg * material.price_per_kg_inr

    # --- Per-Process Cost Lines ---
    process_lines = []
    for pid in selected_processes:
        if pid not in all_processes:
            continue
        proc = all_processes[pid]

        # Physics-based time estimation (passes material_name for exact cutting data)
        time_min = estimate_process_time_min(
            pid, dimensions, material.machinability, material_name=material_name,
        )
        time_hr = time_min / 60

        # Machine cost (time × rate)
        machine_cost = time_hr * proc.machine_rate
        if has_tight_tolerances:
            machine_cost *= 1 + TIGHT_TOLERANCE_SURCHARGE_PCT / 100

        # Setup cost amortized over quantity
        setup_cost_per_unit = (proc.setup_time_min / 60 * proc.machine_rate) / quantity

        # Tooling cost from Taylor tool life (for machining processes)
        tooling_cost = _calculate_tooling_cost(pid, time_min, cd)

        # Power cost from actual cutting power (Kp × MRR)
        power_cost = _calculate_power_cost(pid, time_min, proc, cd)

        # Labour cost
        labour_cost = time_hr * LABOUR_RATE

        process_lines.append(
            ProcessCostLine(
                process_id=pid,
                process_name=proc.name,
                time_min=round(time_min, 2),
                machine_cost=round(machine_cost, 2),
                setup_cost_per_unit=round(setup_cost_per_unit, 2),
                tooling_cost=round(tooling_cost, 2),
                labour_cost=round(labour_cost, 2),
                power_cost=round(power_cost, 2),
            )
        )

    total_machining = sum(p.machine_cost for p in process_lines)
    total_setup = sum(p.setup_cost_per_unit for p in process_lines)
    total_tooling = sum(p.tooling_cost for p in process_lines)
    total_labour = sum(p.labour_cost for p in process_lines)
    total_power = sum(p.power_cost for p in process_lines)

    subtotal = (
        material_cost
        + total_machining
        + total_setup
        + total_tooling
        + total_labour
        + total_power
    )
    overhead = subtotal * (OVERHEAD_PCT / 100)
    profit = (subtotal + overhead) * (PROFIT_PCT / 100)
    rounded_unit_cost = round(subtotal + overhead + profit, 2)
    order_cost = round(rounded_unit_cost * quantity, 2)

    return MechanicalCostBreakdown(
        material_name=material_name,
        raw_weight_kg=round(raw_weight_kg, 3),
        wastage_weight_kg=round(wastage_weight_kg, 3),
        material_cost=round(material_cost, 2),
        process_lines=tuple(process_lines),
        total_machining_cost=round(total_machining, 2),
        total_setup_cost=round(total_setup, 2),
        total_tooling_cost=round(total_tooling, 2),
        total_labour_cost=round(total_labour, 2),
        total_power_cost=round(total_power, 2),
        subtotal=round(subtotal, 2),
        overhead=round(overhead, 2),
        profit=round(profit, 2),
        unit_cost=rounded_unit_cost,
        order_cost=order_cost,
        quantity=quantity,
    )


def _calculate_tooling_cost(process_id: str, time_min: float,
                            cd) -> float:
    """Calculate tooling wear cost using Taylor tool life.

    For machining processes: cost = time × (edge_cost / tool_life).
    Non-machining processes (heat treatment, surface treatment): ₹0.
    """
    non_cutting = {"heat_treatment", "surface_treatment_plating",
                   "surface_treatment_anodizing", "surface_treatment_painting"}
    if process_id in non_cutting:
        return 0.0

    # Use roughing Vc for tool life calculation (conservative)
    if process_id in ("turning", "facing", "boring", "threading", "knurling"):
        vc = cd.turning.vc_rough
    elif process_id.startswith("milling") or process_id == "broaching":
        vc = cd.milling.vc_rough
    elif process_id in ("drilling", "reaming", "tapping"):
        vc = cd.drilling.vc
    elif process_id.startswith("grinding"):
        # Grinding wheels: different wear model, use flat rate
        return time_min * 0.5  # ₹0.5/min for wheel dressing
    else:
        vc = cd.turning.vc_rough

    cost_per_min = calculate_tool_cost_per_min(vc, cd.taylor_n, cd.taylor_c)
    return time_min * cost_per_min


def _calculate_power_cost(process_id: str, time_min: float,
                          proc: ProcessInfo, cd) -> float:
    """Calculate power cost using Kienzle-corrected specific cutting force.

    For machining: P = Kp × MRR (with Kw, Ksp corrections from Kienzle formula).
    Kp is derived from kc1 with tool wear and chip compression factors.
    Sources: Sandvik power formula, CamScripts/Europa-Lehrmittel Kienzle model,
    Stephenson Ch.2, Ghosh & Mallik Ch.4.

    For non-machining: use static power consumption from config.
    """
    non_cutting = {"heat_treatment", "surface_treatment_plating",
                   "surface_treatment_anodizing", "surface_treatment_painting"}
    if process_id in non_cutting:
        return proc.power_kw * (time_min / 60) * POWER_RATE

    # Select Ksp based on operation type (Kienzle chip compression factor)
    if process_id.startswith("milling") or process_id == "broaching":
        ksp = KSP_MILLING
    elif process_id in ("drilling", "reaming", "tapping"):
        ksp = KSP_DRILLING
    else:
        ksp = KSP_TURNING

    # Use Kienzle-corrected Kp: inflate static power by correction ratio
    # kc_corrected / kc_base gives the multiplier for wear + compression
    kc_base = cd.kc1 * (1.0 - 6.0 / 100.0)  # base: no wear, no compression
    kc_corrected = calculate_corrected_kc(
        cd.kc1, cd.mc, chip_thickness_mm=0.15,  # typical avg chip thickness
        rake_angle_deg=6.0, kw=KW_DEFAULT, ksp=ksp,
    )
    correction_ratio = kc_corrected / kc_base if kc_base > 0 else 1.0

    # Apply correction to static power from config
    corrected_power_kw = proc.power_kw * correction_ratio
    return corrected_power_kw * (time_min / 60) * POWER_RATE

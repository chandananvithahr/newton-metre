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
    SHOP_FLOOR_EFFICIENCY,
    MIN_CYCLE_TIME_MIN,
    ESTIMATE_UNCERTAINTY_PCT,
    DYNAMIC_MATERIAL_UNCERTAINTY_PCT,
    MACHINE_TIERS,
    DEFAULT_MACHINE_TIER,
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
from engines.mechanical.surface_treatment_db import (
    calculate_surface_treatment_cost,
    list_surface_treatments,
    SURFACE_TREATMENTS,
)
from engines.mechanical.heat_treatment_db import (
    calculate_heat_treatment_cost,
    list_heat_treatments,
    HEAT_TREATMENTS,
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
    surface_treatment_cost: float = 0.0
    heat_treatment_cost: float = 0.0
    machine_tier: str = "cnc_3axis"
    subtotal: float = 0.0
    overhead: float = 0.0
    profit: float = 0.0
    unit_cost: float = 0.0
    unit_cost_low: float = 0.0   # lower bound of uncertainty band
    unit_cost_high: float = 0.0  # upper bound of uncertainty band
    uncertainty_pct: int = 10    # % used for band (10 or 15)
    order_cost: float = 0.0
    quantity: int = 1


# ── GD&T symbol → cost surcharge table ───────────────────────────────────────
# Each entry: (process_to_add_if_missing, machining_cost_multiplier, inspection_cost_inr)
# Research basis: YOLOv11 + Donut pipeline (2025), Indian job shop rate survey
#
# multiplier applies to the TOTAL machining cost (not material).
# process_to_add is injected into selected_processes if not already present.
# inspection_cost is a flat per-unit cost for CMM / gauge inspection.

_GDT_SURCHARGES: dict[str, dict] = {
    # Form tolerances — require grinding or precision turning
    "circularity":       {"add_process": "grinding_cylindrical", "multiplier": 1.35, "inspection_inr": 150},
    "cylindricity":      {"add_process": "grinding_cylindrical", "multiplier": 1.40, "inspection_inr": 200},
    "straightness":      {"add_process": None,                   "multiplier": 1.15, "inspection_inr": 100},
    "flatness":          {"add_process": "grinding_surface",     "multiplier": 1.30, "inspection_inr": 150},
    # Orientation tolerances
    "perpendicularity":  {"add_process": "grinding_surface",     "multiplier": 1.30, "inspection_inr": 200},
    "angularity":        {"add_process": None,                   "multiplier": 1.20, "inspection_inr": 150},
    "parallelism":       {"add_process": "grinding_surface",     "multiplier": 1.25, "inspection_inr": 150},
    # Location tolerances — require CMM inspection
    "true_position":     {"add_process": None,                   "multiplier": 1.25, "inspection_inr": 400},
    "concentricity":     {"add_process": "grinding_cylindrical", "multiplier": 1.35, "inspection_inr": 350},
    "symmetry":          {"add_process": None,                   "multiplier": 1.20, "inspection_inr": 250},
    # Runout — precision turning + balancing
    "circular_runout":   {"add_process": "grinding_cylindrical", "multiplier": 1.35, "inspection_inr": 300},
    "total_runout":      {"add_process": "grinding_cylindrical", "multiplier": 1.45, "inspection_inr": 400},
    # Profile — complex surface control, may need 5-axis
    "profile_of_surface":{"add_process": None,                   "multiplier": 1.60, "inspection_inr": 500},
    "profile_of_line":   {"add_process": None,                   "multiplier": 1.40, "inspection_inr": 300},
}


def apply_gdt_surcharges(
    machining_cost: float,
    gdt_symbols: list[str],
    selected_processes: list[str],
    quantity: int,
    is_prismatic: bool = False,
) -> tuple[float, float, list[str]]:
    """Apply per-GD&T-symbol cost surcharges.

    Returns (adjusted_machining_cost, inspection_cost_per_unit, updated_processes).

    Rules:
    - The highest multiplier among all detected symbols is applied (not compounded)
      to avoid double-counting when multiple related symbols are present.
    - Processes implied by GD&T (e.g. grinding for circularity) are added if absent.
    - For prismatic (milled) parts, grinding_cylindrical is remapped to
      grinding_surface — you can't cylindrical-grind a flat plate.
    - Inspection cost is amortized over quantity with a sample-inspection model:
      Indian job shops inspect ~10% of batch (min 3 pieces) for GD&T compliance.
      CMM/gauge cost is divided by sample size, so per-unit cost drops with quantity.
    """
    if not gdt_symbols:
        return machining_cost, 0.0, selected_processes

    max_multiplier = 1.0
    total_inspection_batch = 0.0
    updated_processes = list(selected_processes)

    for sym in gdt_symbols:
        rule = _GDT_SURCHARGES.get(sym)
        if not rule:
            continue
        max_multiplier = max(max_multiplier, rule["multiplier"])
        total_inspection_batch += rule["inspection_inr"]
        add_proc = rule["add_process"]
        # Prismatic parts: remap cylindrical grinding → surface grinding
        if add_proc == "grinding_cylindrical" and is_prismatic:
            add_proc = "grinding_surface"
        if add_proc and add_proc not in updated_processes:
            updated_processes.append(add_proc)

    # Sample inspection: inspect max(3, 10% of batch) pieces, amortize over full batch
    sample_size = max(3, int(quantity * 0.10))
    inspection_per_unit = (total_inspection_batch * sample_size) / quantity

    adjusted_machining = machining_cost * max_multiplier
    return adjusted_machining, inspection_per_unit, updated_processes


# Backward-compat: old generic process IDs → specific treatment DB IDs
_SURFACE_TREATMENT_COMPAT = {
    "surface_treatment_plating": "zinc_clear",
    "surface_treatment_anodizing": "anodize_type_ii_clear",
    "surface_treatment_painting": "powder_coat_standard",
}


def calculate_mechanical_cost(
    dimensions: dict,
    material_name: str,
    selected_processes: list[str],
    quantity: int,
    has_tight_tolerances: bool = False,
    material_override: "Material | None" = None,
    is_dynamic_material: bool = False,
    gdt_symbols: list[str] | None = None,
    surface_treatment_id: str | None = None,
    heat_treatment_id: str | None = None,
    machine_tier: str = DEFAULT_MACHINE_TIER,
) -> MechanicalCostBreakdown:
    material = material_override if material_override is not None else get_material(material_name)
    all_processes = load_processes()

    # Resolve machine tier multipliers
    tier = MACHINE_TIERS.get(machine_tier, MACHINE_TIERS[DEFAULT_MACHINE_TIER])
    rate_mult = tier["rate_mult"]
    speed_mult = tier["speed_mult"]
    setup_mult = tier["setup_mult"]
    # For dynamic materials not in cutting DB, machinability-based fallback kicks in automatically
    cd = get_cutting_data(material_name, machinability=material.machinability)

    # --- Raw Material Cost ---
    od = dimensions.get("outer_diameter_mm") or 0
    id_mm = dimensions.get("inner_diameter_mm") or 0
    length = dimensions.get("length_mm") or 0
    width = dimensions.get("width_mm") or 0
    height = dimensions.get("height_mm") or 0

    MIN_DIM_MM = 5.0

    # Determine part geometry type and compute raw material volume accordingly.
    # Prismatic (milled) parts: use rectangular billet — workshops buy bar/plate stock
    # by width × height × length, NOT a circumscribed cylinder.
    # Rotational (turned) parts: use cylindrical bar stock as before.
    is_prismatic = od < MIN_DIM_MM and width >= MIN_DIM_MM and height >= MIN_DIM_MM

    if is_prismatic:
        # Guard: reject if dimensions still too small
        if width < MIN_DIM_MM or height < MIN_DIM_MM or length < MIN_DIM_MM:
            raise ValueError(
                f"Extracted dimensions too small or missing (W={width:.1f}mm, H={height:.1f}mm, L={length:.1f}mm). "
                f"AI may have failed to read the drawing. Please re-upload a clearer image."
            )
        # Rectangular billet with machining allowance on all sides
        billet_w_m = (width + MACHINING_ALLOWANCE_DIA_MM) / 1000
        billet_h_m = (height + MACHINING_ALLOWANCE_DIA_MM) / 1000
        billet_l_m = (length + MACHINING_ALLOWANCE_LEN_MM) / 1000
        volume_m3 = billet_w_m * billet_h_m * billet_l_m
        # Set od for downstream guard checks (bore diameter comparison not applicable)
        od = math.sqrt(width**2 + height**2)  # only used for guard below
    else:
        # Guard: reject if dimensions too small — give context-appropriate message
        if od < MIN_DIM_MM or length < MIN_DIM_MM:
            if width > 0 or height > 0:
                raise ValueError(
                    f"Extracted dimensions incomplete (W={width:.1f}mm, H={height:.1f}mm, L={length:.1f}mm). "
                    f"Both width and height must be specified for milled parts, or outer_diameter for turned parts."
                )
            raise ValueError(
                f"Extracted dimensions too small or missing (OD={od:.1f}mm, L={length:.1f}mm). "
                f"AI may have failed to read the drawing. Please re-upload a clearer image."
            )

        # Impossible geometry: bore cannot be larger than the part
        if id_mm > 0 and id_mm >= od:
            raise ValueError(
                f"Inner diameter ({id_mm:.1f}mm) >= outer diameter ({od:.1f}mm). "
                f"Check the drawing — bore cannot be larger than the part."
            )

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
        catalog_time_min = estimate_process_time_min(
            pid, dimensions, material.machinability, material_name=material_name,
        )
        # Skip processes that compute to zero time (e.g. drilling with hole_count=0)
        if catalog_time_min <= 0:
            continue
        # Apply shop floor derating + machine tier speed adjustment.
        # Faster machines (5-axis) cut slightly faster; conventional machines are slower.
        # Floor at MIN_CYCLE_TIME_MIN: even tiny parts need load/indicate/cut/measure/unload.
        time_min = max(catalog_time_min / (SHOP_FLOOR_EFFICIENCY * speed_mult), MIN_CYCLE_TIME_MIN)
        time_hr = time_min / 60

        # Machine cost (time × rate × tier multiplier)
        tier_rate = proc.machine_rate * rate_mult
        machine_cost = time_hr * tier_rate
        if has_tight_tolerances:
            machine_cost *= 1 + TIGHT_TOLERANCE_SURCHARGE_PCT / 100

        # Setup cost amortized over quantity (conventional machines: longer setup)
        setup_cost_per_unit = (proc.setup_time_min * setup_mult / 60 * tier_rate) / quantity

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

    # GD&T surcharges: adjust machining cost + add inspection cost
    gdt_inspection_cost = 0.0
    if gdt_symbols:
        original_machining = total_machining
        total_machining, gdt_inspection_cost, selected_processes = apply_gdt_surcharges(
            total_machining, gdt_symbols, selected_processes, quantity,
            is_prismatic=is_prismatic,
        )
        # Scale labour by the same ratio as machining (precision work needs more operator time)
        if original_machining > 0:
            total_labour = total_labour * (total_machining / original_machining)

    # --- Surface treatment cost (from rich treatment DB) ---
    # Auto-detect from selected_processes if no explicit ID given
    surface_treatment_cost = 0.0
    _st_id = surface_treatment_id
    if not _st_id:
        for pid in selected_processes:
            if pid in _SURFACE_TREATMENT_COMPAT:
                _st_id = _SURFACE_TREATMENT_COMPAT[pid]
                break
    if _st_id:
        # Compute surface area in sq.dm (1 dm = 100 mm)
        if is_prismatic:
            sa_sq_mm = 2 * (width * length + width * height + length * height)
        else:
            sa_sq_mm = math.pi * od * length  # cylindrical outer surface
            if id_mm > 0:
                sa_sq_mm += math.pi * id_mm * length  # bore surface
        sa_sq_dm = sa_sq_mm / 1e4  # mm² → dm²
        surface_treatment_cost = round(calculate_surface_treatment_cost(
            _st_id, sa_sq_dm, quantity, part_weight_kg=raw_weight_kg,
            is_high_strength_steel=(material.hardness_bhn > 300),
        ), 2)

    # --- Heat treatment cost (from rich treatment DB) ---
    heat_treatment_cost = 0.0
    _ht_id = heat_treatment_id
    if not _ht_id and "heat_treatment" in selected_processes:
        _ht_id = "through_hardening"  # default for generic heat_treatment process
    if _ht_id:
        heat_treatment_cost = round(calculate_heat_treatment_cost(
            _ht_id, raw_weight_kg, quantity,
        ), 2)

    subtotal = (
        material_cost
        + total_machining
        + total_setup
        + total_tooling
        + total_labour
        + total_power
        + gdt_inspection_cost
        + surface_treatment_cost
        + heat_treatment_cost
    )
    overhead = subtotal * (OVERHEAD_PCT / 100)
    profit = (subtotal + overhead) * (PROFIT_PCT / 100)
    rounded_unit_cost = round(subtotal + overhead + profit, 2)
    order_cost = round(rounded_unit_cost * quantity, 2)

    # Uncertainty band: wider for dynamic/unknown materials
    uncertainty_pct = DYNAMIC_MATERIAL_UNCERTAINTY_PCT if is_dynamic_material else ESTIMATE_UNCERTAINTY_PCT
    unit_cost_low = round(rounded_unit_cost * (1 - uncertainty_pct / 100), 2)
    unit_cost_high = round(rounded_unit_cost * (1 + uncertainty_pct / 100), 2)

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
        surface_treatment_cost=surface_treatment_cost,
        heat_treatment_cost=heat_treatment_cost,
        machine_tier=machine_tier,
        subtotal=round(subtotal, 2),
        overhead=round(overhead, 2),
        profit=round(profit, 2),
        unit_cost=rounded_unit_cost,
        unit_cost_low=unit_cost_low,
        unit_cost_high=unit_cost_high,
        uncertainty_pct=uncertainty_pct,
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

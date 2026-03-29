"""Sheet metal material database — densities, prices, and standard sheet sizes.

Indian market prices (₹/kg) as of 2025-2026.
"""
import math
from dataclasses import dataclass


@dataclass(frozen=True)
class SheetMaterial:
    name: str
    density_kg_per_m3: float
    price_per_kg_inr: float
    uts_mpa: float          # ultimate tensile strength (N/mm²)
    k_factor_bend: float    # neutral axis factor for bend allowance (0.3-0.5)
    tonnage_factor: float   # multiplier vs mild steel for bending tonnage


SHEET_MATERIALS: dict[str, SheetMaterial] = {
    "Mild Steel CR": SheetMaterial(
        name="Mild Steel CR", density_kg_per_m3=7850,
        price_per_kg_inr=65, uts_mpa=450, k_factor_bend=0.42, tonnage_factor=1.0,
    ),
    "Mild Steel HR": SheetMaterial(
        name="Mild Steel HR", density_kg_per_m3=7850,
        price_per_kg_inr=55, uts_mpa=400, k_factor_bend=0.40, tonnage_factor=1.0,
    ),
    "Stainless Steel 304": SheetMaterial(
        name="Stainless Steel 304", density_kg_per_m3=8000,
        price_per_kg_inr=240, uts_mpa=600, k_factor_bend=0.45, tonnage_factor=1.5,
    ),
    "Stainless Steel 316": SheetMaterial(
        name="Stainless Steel 316", density_kg_per_m3=8000,
        price_per_kg_inr=350, uts_mpa=620, k_factor_bend=0.45, tonnage_factor=1.7,
    ),
    "Aluminum 5052": SheetMaterial(
        name="Aluminum 5052", density_kg_per_m3=2680,
        price_per_kg_inr=285, uts_mpa=230, k_factor_bend=0.33, tonnage_factor=0.5,
    ),
    "Aluminum 6061": SheetMaterial(
        name="Aluminum 6061", density_kg_per_m3=2700,
        price_per_kg_inr=315, uts_mpa=310, k_factor_bend=0.33, tonnage_factor=0.65,
    ),
    "Galvanized Steel": SheetMaterial(
        name="Galvanized Steel", density_kg_per_m3=7850,
        price_per_kg_inr=75, uts_mpa=430, k_factor_bend=0.42, tonnage_factor=1.0,
    ),
    "Copper": SheetMaterial(
        name="Copper", density_kg_per_m3=8960,
        price_per_kg_inr=800, uts_mpa=220, k_factor_bend=0.33, tonnage_factor=0.45,
    ),
    "Brass": SheetMaterial(
        name="Brass", density_kg_per_m3=8530,
        price_per_kg_inr=575, uts_mpa=350, k_factor_bend=0.35, tonnage_factor=0.55,
    ),
}

# Standard Indian sheet sizes (mm)
STANDARD_SHEET_SIZES_MM: list[tuple[int, int]] = [
    (1250, 2500),   # 4' × 8' — most common
    (1500, 3000),   # 5' × 10'
    (1000, 2000),   # small sheet
]

# Sheet edge margin for laser clamp zone (mm)
SHEET_EDGE_MARGIN_MM = 12


def get_sheet_material(name: str) -> SheetMaterial:
    if name not in SHEET_MATERIALS:
        raise ValueError(f"Unknown sheet material: {name}. "
                         f"Available: {list(SHEET_MATERIALS.keys())}")
    return SHEET_MATERIALS[name]


def list_sheet_material_names() -> list[str]:
    return list(SHEET_MATERIALS.keys())


def calculate_blank_weight_kg(
    length_mm: float, width_mm: float, thickness_mm: float,
    density_kg_per_m3: float,
) -> float:
    """Weight of a rectangular blank in kg."""
    volume_m3 = (length_mm / 1000) * (width_mm / 1000) * (thickness_mm / 1000)
    return volume_m3 * density_kg_per_m3


def estimate_utilization_pct(
    part_length_mm: float, part_width_mm: float,
    sheet_length_mm: float = 2500, sheet_width_mm: float = 1250,
) -> float:
    """Estimate nesting utilization for rectangular parts on a standard sheet.

    Returns percentage (0-100).
    """
    usable_l = sheet_length_mm - 2 * SHEET_EDGE_MARGIN_MM
    usable_w = sheet_width_mm - 2 * SHEET_EDGE_MARGIN_MM

    if part_length_mm <= 0 or part_width_mm <= 0:
        return 75.0  # default

    # Try both orientations
    parts_a = (math.floor(usable_l / part_length_mm)
               * math.floor(usable_w / part_width_mm))
    parts_b = (math.floor(usable_l / part_width_mm)
               * math.floor(usable_w / part_length_mm))
    parts_per_sheet = max(parts_a, parts_b)

    if parts_per_sheet == 0:
        return 75.0  # part larger than sheet, use conservative default

    used_area = parts_per_sheet * part_length_mm * part_width_mm
    sheet_area = sheet_length_mm * sheet_width_mm
    return min(used_area / sheet_area * 100, 100.0)

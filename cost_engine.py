"""
Cost calculation logic for CNC turning operations
"""
import json
import math
from pathlib import Path
from typing import Dict, Optional, List
from material_price_fetcher import get_material_price

# Default rates (Indian job shop economics)
DEFAULT_MACHINE_HOUR_RATE = 800  # ₹/hr for standard CNC lathe
DEFAULT_SETUP_TIME_MIN = 30  # minutes for first piece
DEFAULT_OVERHEAD_PERCENT = 15
DEFAULT_PROFIT_PERCENT = 20

# Machining parameters
MACHINING_ALLOWANCE_DIAMETER_MM = 3  # 3mm oversize for bar stock
MACHINING_ALLOWANCE_LENGTH_MM = 5  # 5mm extra length
MATERIAL_WASTAGE_PERCENT = 15  # 15% wastage for cutoff and chips

# Feed rates and depths
ROUGH_FEED_RATE_MM_PER_MIN = 200
FINISH_FEED_RATE_MM_PER_MIN = 300
ROUGH_DEPTH_OF_CUT_MM = 0.3
FINISH_DEPTH_OF_CUT_MM = 0.1

# Feature time estimates (minutes)
TIME_FACING_PER_FACE = 0.5
TIME_THREAD_PER_THREAD = 2.0
TIME_GROOVE_PER_GROOVE = 1.5
TIME_PARTING_OFF = 1.0

# Load materials database
MATERIALS_FILE = Path(__file__).parent / "sample_data" / "materials.json"

def load_materials() -> Dict[str, Dict]:
    """Load materials database from JSON file."""
    try:
        with open(MATERIALS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            materials = {}
            for mat in data.get('materials', []):
                materials[mat['name']] = {
                    'price_per_kg_inr': mat['price_per_kg_inr'],
                    'density_kg_per_m3': mat['density_kg_per_m3']
                }
            return materials
    except FileNotFoundError:
        raise FileNotFoundError(f"Materials file not found: {MATERIALS_FILE}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in materials file: {e}")


def estimate_turning_cost(
    dimensions: Dict,
    material_type: str,
    quantity: int,
    has_tight_tolerances: bool = False,
    features: Optional[List[Dict]] = None,
    machine_hour_rate: Optional[float] = None,
    overhead_percent: Optional[float] = None,
    profit_percent: Optional[float] = None,
    use_live_prices: bool = True,
    region: Optional[Dict] = None
) -> Dict:
    """
    Estimate CNC turning cost based on Indian job shop economics.
    
    Args:
        dimensions: Dict with keys like max_diameter_mm, inner_diameter_mm, length_mm
        material_type: Material name (must match materials.json)
        quantity: Number of pieces to manufacture
        has_tight_tolerances: If True, add 30% to machining cost
        features: List of feature dicts from vision.py (e.g., [{"type": "thread", ...}])
        machine_hour_rate: Override default machine hour rate (₹/hr)
        overhead_percent: Override default overhead percentage
        profit_percent: Override default profit percentage
        
    Returns:
        Dictionary with detailed cost breakdown
    """
    if quantity <= 0:
        return {"error": "Quantity must be greater than 0"}
    
    # Load materials
    try:
        materials = load_materials()
    except Exception as e:
        return {"error": f"Failed to load materials: {str(e)}"}
    
    # Validate material
    if material_type not in materials:
        available = ", ".join(materials.keys())
        return {"error": f"Material '{material_type}' not found. Available: {available}"}
    
    material = materials[material_type]
    density_kg_per_m3 = material['density_kg_per_m3']
    
    # Fetch live price from web (with fallback to static price)
    if use_live_prices:
        try:
            price_per_kg = get_material_price(material_type, use_web=True)
        except Exception:
            # Fallback to static price if web fetch fails
            price_per_kg = material.get('price_per_kg_inr', 100.0)
    else:
        # Use static price from materials.json
        price_per_kg = material.get('price_per_kg_inr', 100.0)
    
    # Use region-specific rates or provided overrides or defaults
    if region:
        # Convert material price from INR to region currency
        exchange_rate = region.get('exchange_rate_to_usd', 1.0)
        inr_to_usd = 1.0 / 83.0  # INR to USD (base rate)
        region_multiplier = region.get('material_price_multiplier', 1.0)
        
        # Adjust price based on region
        price_per_kg = price_per_kg * (exchange_rate * inr_to_usd) * region_multiplier
        
        # Use region-specific machine rate
        default_machine_rate = region.get('machine_rate_per_hr', DEFAULT_MACHINE_HOUR_RATE)
        machine_rate = machine_hour_rate or default_machine_rate
        
        # Use region-specific overhead and profit
        overhead_pct = overhead_percent or region.get('overhead_percent', DEFAULT_OVERHEAD_PERCENT)
        profit_pct = profit_percent or region.get('profit_percent', DEFAULT_PROFIT_PERCENT)
    else:
        # Default to Indian rates
        machine_rate = machine_hour_rate or DEFAULT_MACHINE_HOUR_RATE
        overhead_pct = overhead_percent or DEFAULT_OVERHEAD_PERCENT
        profit_pct = profit_percent or DEFAULT_PROFIT_PERCENT
    
    # Extract dimensions
    od_mm = dimensions.get('max_diameter_mm') or 0
    id_mm = dimensions.get('inner_diameter_mm') or 0
    length_mm = dimensions.get('length_mm') or 0
    
    if od_mm <= 0 or length_mm <= 0:
        return {"error": "Invalid dimensions: max_diameter_mm and length_mm must be > 0"}
    
    # ========== 1. RAW MATERIAL COST ==========
    # Calculate bar stock needed (with machining allowance)
    bar_od_mm = od_mm + MACHINING_ALLOWANCE_DIAMETER_MM
    bar_length_mm = length_mm + MACHINING_ALLOWANCE_LENGTH_MM
    
    # Convert to meters for volume calculation
    bar_od_m = bar_od_mm / 1000
    bar_id_m = (id_mm / 1000) if id_mm > 0 else 0
    bar_length_m = bar_length_mm / 1000
    
    # Calculate volume (m³)
    if bar_id_m > 0:
        # Hollow part
        outer_volume = math.pi * (bar_od_m / 2) ** 2 * bar_length_m
        inner_volume = math.pi * (bar_id_m / 2) ** 2 * bar_length_m
        volume_m3 = outer_volume - inner_volume
    else:
        # Solid part
        volume_m3 = math.pi * (bar_od_m / 2) ** 2 * bar_length_m
    
    # Calculate weight
    weight_kg = volume_m3 * (density_kg_per_m3 / 1000)  # density is kg/m³, volume is m³
    
    # Add wastage
    weight_with_wastage_kg = weight_kg * (1 + MATERIAL_WASTAGE_PERCENT / 100)
    
    # Material cost per piece
    material_cost_per_piece = weight_with_wastage_kg * price_per_kg
    total_material_cost = material_cost_per_piece * quantity
    
    # ========== 2. MACHINING TIME ESTIMATION ==========
    # Base machining time formula: (OD × length) / 5000
    base_time_min = (od_mm * length_mm) / 5000
    
    # Add facing time (typically 2 faces: front and back)
    facing_time_min = TIME_FACING_PER_FACE * 2
    
    # Roughing passes calculation
    # Number of roughing passes needed = (allowance / depth of cut)
    roughing_passes = MACHINING_ALLOWANCE_DIAMETER_MM / (2 * ROUGH_DEPTH_OF_CUT_MM)
    roughing_time_min = (length_mm / ROUGH_FEED_RATE_MM_PER_MIN) * roughing_passes
    
    # Finishing pass
    finishing_time_min = length_mm / FINISH_FEED_RATE_MM_PER_MIN
    
    # ID boring time (if hollow)
    boring_time_min = 0
    if id_mm > 0:
        boring_passes = 3  # Assume 3 passes for boring
        boring_time_min = (length_mm / ROUGH_FEED_RATE_MM_PER_MIN) * boring_passes
    
    # Feature time
    feature_time_min = 0
    thread_count = 0
    groove_count = 0
    
    if features:
        for feature in features:
            feat_type = feature.get('type', '').lower()
            if 'thread' in feat_type:
                thread_count += 1
                feature_time_min += TIME_THREAD_PER_THREAD
            elif 'groove' in feat_type:
                groove_count += 1
                feature_time_min += TIME_GROOVE_PER_GROOVE
    
    # Parting off time
    parting_time_min = TIME_PARTING_OFF
    
    # Total machining time per piece
    machining_time_min = (
        base_time_min +
        facing_time_min +
        roughing_time_min +
        finishing_time_min +
        boring_time_min +
        feature_time_min +
        parting_time_min
    )
    
    # ========== 3. MACHINING COST ==========
    # Machine hour rate to per minute
    machine_rate_per_min = machine_rate / 60
    
    # Base machining cost
    machining_cost_per_piece = machining_time_min * machine_rate_per_min
    
    # Add 30% for tight tolerances
    if has_tight_tolerances:
        machining_cost_per_piece *= 1.3
    
    # Setup time cost (amortized over quantity)
    setup_time_min = DEFAULT_SETUP_TIME_MIN
    setup_cost_total = setup_time_min * machine_rate_per_min
    setup_cost_per_piece = setup_cost_total / quantity
    
    total_machining_cost = (machining_cost_per_piece + setup_cost_per_piece) * quantity
    
    # ========== 4. OVERHEAD & PROFIT ==========
    # Base cost (material + machining)
    base_cost_per_piece = material_cost_per_piece + machining_cost_per_piece + setup_cost_per_piece
    total_base_cost = base_cost_per_piece * quantity
    
    # Overhead
    overhead_per_piece = base_cost_per_piece * (overhead_pct / 100)
    total_overhead = overhead_per_piece * quantity
    
    # Cost after overhead
    cost_after_overhead_per_piece = base_cost_per_piece + overhead_per_piece
    
    # Profit margin
    profit_per_piece = cost_after_overhead_per_piece * (profit_pct / 100)
    total_profit = profit_per_piece * quantity
    
    # Final costs
    cost_per_piece = cost_after_overhead_per_piece + profit_per_piece
    total_cost = cost_per_piece * quantity
    
    # ========== RETURN DETAILED BREAKDOWN ==========
    return {
        "material_cost": round(material_cost_per_piece, 2),
        "machining_time_min": round(machining_time_min, 2),
        "machining_cost": round(machining_cost_per_piece, 2),
        "setup_cost_per_piece": round(setup_cost_per_piece, 2),
        "overhead": round(overhead_per_piece, 2),
        "profit": round(profit_per_piece, 2),
        "cost_per_piece": round(cost_per_piece, 2),
        "total_cost": round(total_cost, 2),
        "breakdown": {
            "material": {
                "bar_diameter_mm": round(bar_od_mm, 2),
                "bar_length_mm": round(bar_length_mm, 2),
                "volume_m3": round(volume_m3, 6),
                "weight_kg": round(weight_kg, 3),
                "weight_with_wastage_kg": round(weight_with_wastage_kg, 3),
                "price_per_kg_inr": price_per_kg,
                "material_cost_per_piece": round(material_cost_per_piece, 2),
                "total_material_cost": round(total_material_cost, 2)
            },
            "machining": {
                "base_time_min": round(base_time_min, 2),
                "facing_time_min": round(facing_time_min, 2),
                "roughing_time_min": round(roughing_time_min, 2),
                "finishing_time_min": round(finishing_time_min, 2),
                "boring_time_min": round(boring_time_min, 2),
                "feature_time_min": round(feature_time_min, 2),
                "parting_time_min": round(parting_time_min, 2),
                "total_time_min": round(machining_time_min, 2),
                "machine_rate_per_hr": round(machine_rate, 2),
                "machining_cost_per_piece": round(machining_cost_per_piece, 2),
                "setup_time_min": setup_time_min,
                "setup_cost_per_piece": round(setup_cost_per_piece, 2),
                "tight_tolerance_surcharge": "30%" if has_tight_tolerances else "0%",
                "total_machining_cost": round(total_machining_cost, 2)
            },
            "features": {
                "threads": thread_count,
                "grooves": groove_count,
                "total_features": thread_count + groove_count
            },
            "pricing": {
                "base_cost_per_piece": round(base_cost_per_piece, 2),
                "overhead_percent": overhead_pct,
                "overhead_per_piece": round(overhead_per_piece, 2),
                "profit_percent": profit_pct,
                "profit_per_piece": round(profit_per_piece, 2),
                "final_cost_per_piece": round(cost_per_piece, 2),
                "quantity": quantity,
                "total_cost": round(total_cost, 2)
            }
        }
    }

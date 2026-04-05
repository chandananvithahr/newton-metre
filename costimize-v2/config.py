# costimize-v2/config.py
"""Single source of truth for all rates, constants, and settings."""

import os
from dotenv import load_dotenv

load_dotenv()

# --- API Keys ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY", "")

# --- Embedding ---
GEMINI_EMBEDDING_MODEL = "gemini-embedding-exp-03-07"
GEMINI_EMBEDDING_DIM = 768  # Gemini Embedding API native dimension

# --- Mechanical: Machine Rates (₹/hr) ---
MACHINE_RATES = {
    "turning": 800,
    "facing": 800,
    "boring": 900,
    "milling_face": 1000,
    "milling_slot": 1000,
    "milling_pocket": 1100,
    "drilling": 600,
    "reaming": 700,
    "tapping": 600,
    "threading": 600,
    "grinding_cylindrical": 1200,
    "grinding_surface": 1200,
    "knurling": 800,
    "broaching": 1500,
    "heat_treatment": 500,
    "surface_treatment_plating": 400,
    "surface_treatment_anodizing": 450,
    "surface_treatment_painting": 300,
    "edm_wire": 1500,
    "edm_sinker": 1200,
    "chamfering": 600,
    "deburring": 400,
    "honing": 1400,
    "lapping": 1000,
    "polishing": 500,
}

# --- Mechanical: Setup Times (minutes per process) ---
SETUP_TIMES = {
    "turning": 30,
    "facing": 10,
    "boring": 25,
    "milling_face": 45,
    "milling_slot": 45,
    "milling_pocket": 50,
    "drilling": 15,
    "reaming": 15,
    "tapping": 15,
    "threading": 20,
    "grinding_cylindrical": 40,
    "grinding_surface": 35,
    "knurling": 15,
    "broaching": 60,
    "heat_treatment": 20,
    "surface_treatment_plating": 15,
    "surface_treatment_anodizing": 15,
    "surface_treatment_painting": 10,
    "edm_wire": 45,
    "edm_sinker": 30,
    "chamfering": 10,
    "deburring": 10,
    "honing": 30,
    "lapping": 20,
    "polishing": 15,
}

# --- Mechanical: Power Consumption (kW per process) ---
POWER_CONSUMPTION = {
    "turning": 5,
    "facing": 5,
    "boring": 5,
    "milling_face": 7,
    "milling_slot": 7,
    "milling_pocket": 7,
    "drilling": 3,
    "reaming": 3,
    "tapping": 2,
    "threading": 3,
    "grinding_cylindrical": 4,
    "grinding_surface": 4,
    "knurling": 3,
    "broaching": 10,
    "heat_treatment": 15,
    "surface_treatment_plating": 2,
    "surface_treatment_anodizing": 3,
    "surface_treatment_painting": 1,
    "edm_wire": 8,
    "edm_sinker": 6,
    "chamfering": 2,
    "deburring": 1,
    "honing": 5,
    "lapping": 3,
    "polishing": 2,
}

# --- Mechanical: Tooling Cost per Unit (₹) ---
TOOLING_COST_PER_UNIT = {
    "turning": 8,
    "facing": 3,
    "boring": 10,
    "milling_face": 12,
    "milling_slot": 12,
    "milling_pocket": 15,
    "drilling": 5,
    "reaming": 7,
    "tapping": 6,
    "threading": 6,
    "grinding_cylindrical": 4,
    "grinding_surface": 4,
    "knurling": 3,
    "broaching": 20,
    "heat_treatment": 0,
    "surface_treatment_plating": 0,
    "surface_treatment_anodizing": 0,
    "surface_treatment_painting": 0,
    "edm_wire": 25,       # wire consumable per part
    "edm_sinker": 30,     # electrode wear per part
    "chamfering": 3,
    "deburring": 2,
    "honing": 15,         # abrasive stone wear
    "lapping": 10,        # abrasive compound
    "polishing": 5,       # polishing compound
}

# --- Mechanical: General ---
LABOUR_RATE = 250  # ₹/hr
POWER_RATE = 8  # ₹/kWh
MATERIAL_WASTAGE_PCT = 15  # %
MACHINING_ALLOWANCE_DIA_MM = 3
MACHINING_ALLOWANCE_LEN_MM = 5
TIGHT_TOLERANCE_SURCHARGE_PCT = 30  # % added if tolerance < ±0.05mm

# --- PCB Assembly ---
SMD_RATE_PER_PAD = 1.5  # ₹
THT_RATE_PER_PIN = 3.0  # ₹
STENCIL_COST = 500  # ₹ (amortized over qty)
TEST_RATE_PER_BOARD = 25  # ₹

# --- Cable Assembly ---
CABLE_LABOUR_RATE = 200  # ₹/hr
CABLE_TIME_PER_WIRE_MIN = 2.0
CABLE_TIME_PER_CONNECTOR_MIN = 0.5
CABLE_TIME_SLEEVING_MIN = 1.0
CABLE_TIME_LABELLING_MIN = 0.5

# --- Common ---
OVERHEAD_PCT = 15  # %
PROFIT_PCT = 20  # %

# --- Accuracy calibration ---
# Real shops run at 65-85% of catalog cutting speeds (Practical Machining Data research).
# 0.75 is the midpoint — parts take longer than catalog predicts.
SHOP_FLOOR_EFFICIENCY = 0.75

# Minimum per-part cycle time (minutes) AFTER shop efficiency.
# Even a tiny part needs: load workpiece → indicate → cut → measure → unload.
# Indian CNC shops: 30-60 sec minimum regardless of part size.
MIN_CYCLE_TIME_MIN = 0.5  # 30 seconds absolute floor

# --- Machine Tier Model ---
# Indian shops have a wide range of equipment. The tier multipliers adjust
# machine rate, cutting speed, and setup time relative to the CNC 3-axis baseline.
# Sources: IndiaMART machine listings, Indian CNC shop rate surveys.
MACHINE_TIERS = {
    "conventional":  {"rate_mult": 0.45, "speed_mult": 0.50, "setup_mult": 2.0},  # manual lathe/mill ₹300-450/hr
    "cnc_2axis":     {"rate_mult": 0.75, "speed_mult": 0.85, "setup_mult": 1.2},  # CNC lathe ₹500-700/hr
    "cnc_3axis":     {"rate_mult": 1.00, "speed_mult": 1.00, "setup_mult": 1.0},  # VMC baseline ₹800-1100/hr
    "cnc_5axis":     {"rate_mult": 2.00, "speed_mult": 1.15, "setup_mult": 1.5},  # 5-axis ₹1800-2500/hr
    "hmc":           {"rate_mult": 1.80, "speed_mult": 1.10, "setup_mult": 1.3},  # HMC ₹1500-2000/hr
}
DEFAULT_MACHINE_TIER = "cnc_3axis"

# Uncertainty band shown to users: ±15% for known materials, ±25% for dynamic AI-fetched materials.
ESTIMATE_UNCERTAINTY_PCT = 10
DYNAMIC_MATERIAL_UNCERTAINTY_PCT = 15

# --- Scraper ---
CACHE_DURATION_SEC = 86400  # 24 hours
SCRAPE_DELAY_RANGE = (2, 5)  # random seconds between requests
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
]

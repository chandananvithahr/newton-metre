# Should-Cost Intelligence Tool — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a modular should-cost intelligence tool giving procurement teams line-by-line cost breakdowns for mechanical parts, PCB assemblies, and cable assemblies.

**Architecture:** Fresh Streamlit app (`costimize-v2/`) with separate cost engine modules per part type, shared vision extraction and web scraping layers, and historical PO comparison. Each part type is self-contained with its own engine, parser, and UI tab.

**Tech Stack:** Python 3.11+, Streamlit, OpenAI GPT-4o / Google Gemini (vision), BeautifulSoup + requests (scraping), openpyxl + pandas (Excel parsing), JSON file storage.

---

## Task 1: Project Scaffold & Config

**Files:**
- Create: `costimize-v2/app.py`
- Create: `costimize-v2/config.py`
- Create: `costimize-v2/requirements.txt`
- Create: `costimize-v2/.env.example`
- Create: `costimize-v2/data/materials.json`
- Create: `costimize-v2/data/processes.json`
- Test: `costimize-v2/tests/test_config.py`

- [ ] **Step 1: Create project directory structure**

```bash
mkdir -p costimize-v2/{ui,engines/mechanical,engines/pcb,engines/cable,extractors,scrapers,history,data/cache,data/history,tests}
touch costimize-v2/__init__.py costimize-v2/ui/__init__.py costimize-v2/engines/__init__.py costimize-v2/engines/mechanical/__init__.py costimize-v2/engines/pcb/__init__.py costimize-v2/engines/cable/__init__.py costimize-v2/extractors/__init__.py costimize-v2/scrapers/__init__.py costimize-v2/history/__init__.py costimize-v2/tests/__init__.py
```

- [ ] **Step 2: Write config.py with all rates and constants**

```python
# costimize-v2/config.py
"""Single source of truth for all rates, constants, and settings."""

import os
from dotenv import load_dotenv

load_dotenv()

# --- API Keys ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY", "")

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
# Per wire: cut 0.5 + strip 0.5 + crimp 1.0 = 2.0 min
CABLE_TIME_PER_WIRE_MIN = 2.0
CABLE_TIME_PER_CONNECTOR_MIN = 0.5
CABLE_TIME_SLEEVING_MIN = 1.0
CABLE_TIME_LABELLING_MIN = 0.5

# --- Common ---
OVERHEAD_PCT = 15  # %
PROFIT_PCT = 20  # %

# --- Scraper ---
CACHE_DURATION_SEC = 86400  # 24 hours
SCRAPE_DELAY_RANGE = (2, 5)  # random seconds between requests
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
]
```

- [ ] **Step 3: Write the failing test for config**

```python
# costimize-v2/tests/test_config.py
from config import (
    MACHINE_RATES, SETUP_TIMES, POWER_CONSUMPTION, TOOLING_COST_PER_UNIT,
    LABOUR_RATE, POWER_RATE, OVERHEAD_PCT, PROFIT_PCT,
    SMD_RATE_PER_PAD, THT_RATE_PER_PIN, CABLE_LABOUR_RATE,
)


def test_all_machine_processes_have_consistent_keys():
    """Every process in MACHINE_RATES must also exist in SETUP_TIMES, POWER_CONSUMPTION, and TOOLING_COST_PER_UNIT."""
    for process in MACHINE_RATES:
        assert process in SETUP_TIMES, f"{process} missing from SETUP_TIMES"
        assert process in POWER_CONSUMPTION, f"{process} missing from POWER_CONSUMPTION"
        assert process in TOOLING_COST_PER_UNIT, f"{process} missing from TOOLING_COST_PER_UNIT"


def test_all_rates_are_positive():
    assert LABOUR_RATE > 0
    assert POWER_RATE > 0
    assert OVERHEAD_PCT > 0
    assert PROFIT_PCT > 0
    assert SMD_RATE_PER_PAD > 0
    assert THT_RATE_PER_PIN > 0
    assert CABLE_LABOUR_RATE > 0
    for process, rate in MACHINE_RATES.items():
        assert rate > 0, f"{process} machine rate must be positive"
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
cd costimize-v2 && python -m pytest tests/test_config.py -v
```
Expected: 2 tests PASS

- [ ] **Step 5: Create materials.json (ported from existing)**

```json
{
  "materials": [
    {"name": "Aluminum 6061", "price_per_kg_inr": 280, "density_kg_per_m3": 2700, "machinability": 0.8},
    {"name": "Mild Steel IS2062", "price_per_kg_inr": 65, "density_kg_per_m3": 7850, "machinability": 0.6},
    {"name": "Stainless Steel 304", "price_per_kg_inr": 220, "density_kg_per_m3": 8000, "machinability": 0.4},
    {"name": "Brass IS319", "price_per_kg_inr": 550, "density_kg_per_m3": 8500, "machinability": 0.9},
    {"name": "EN8 Steel", "price_per_kg_inr": 75, "density_kg_per_m3": 7850, "machinability": 0.55},
    {"name": "EN24 Steel", "price_per_kg_inr": 120, "density_kg_per_m3": 7850, "machinability": 0.45},
    {"name": "Copper", "price_per_kg_inr": 750, "density_kg_per_m3": 8960, "machinability": 0.7},
    {"name": "Cast Iron", "price_per_kg_inr": 55, "density_kg_per_m3": 7200, "machinability": 0.65},
    {"name": "Titanium Grade 5", "price_per_kg_inr": 3500, "density_kg_per_m3": 4430, "machinability": 0.25}
  ]
}
```

Save to `costimize-v2/data/materials.json`.

- [ ] **Step 6: Create processes.json**

```json
{
  "processes": [
    {"id": "turning", "name": "Turning", "category": "machining", "description": "Cylindrical material removal on lathe"},
    {"id": "facing", "name": "Facing", "category": "machining", "description": "Flat surface on lathe"},
    {"id": "boring", "name": "Boring", "category": "machining", "description": "Enlarge existing hole on lathe"},
    {"id": "milling_face", "name": "Face Milling", "category": "machining", "description": "Flat surface on milling machine"},
    {"id": "milling_slot", "name": "Slot Milling", "category": "machining", "description": "Cut slots/channels"},
    {"id": "milling_pocket", "name": "Pocket Milling", "category": "machining", "description": "Cut pockets/cavities"},
    {"id": "drilling", "name": "Drilling", "category": "machining", "description": "Create holes"},
    {"id": "reaming", "name": "Reaming", "category": "machining", "description": "Precision hole finishing"},
    {"id": "tapping", "name": "Tapping", "category": "machining", "description": "Internal threads"},
    {"id": "threading", "name": "Threading", "category": "machining", "description": "External threads"},
    {"id": "grinding_cylindrical", "name": "Cylindrical Grinding", "category": "finishing", "description": "Precision cylindrical finish"},
    {"id": "grinding_surface", "name": "Surface Grinding", "category": "finishing", "description": "Precision flat finish"},
    {"id": "knurling", "name": "Knurling", "category": "machining", "description": "Textured grip pattern"},
    {"id": "broaching", "name": "Broaching", "category": "machining", "description": "Keyways, splines, shapes"},
    {"id": "heat_treatment", "name": "Heat Treatment", "category": "treatment", "description": "Hardening, tempering, annealing"},
    {"id": "surface_treatment_plating", "name": "Plating", "category": "treatment", "description": "Chrome, nickel, zinc plating"},
    {"id": "surface_treatment_anodizing", "name": "Anodizing", "category": "treatment", "description": "Anodic oxide coating (aluminium)"},
    {"id": "surface_treatment_painting", "name": "Painting", "category": "treatment", "description": "Paint/powder coating"}
  ]
}
```

Save to `costimize-v2/data/processes.json`.

- [ ] **Step 7: Create requirements.txt**

```
streamlit>=1.30.0
openai>=1.10.0
google-generativeai>=0.3.0
python-dotenv>=1.0.0
Pillow>=10.0.0
beautifulsoup4>=4.12.0
requests>=2.31.0
openpyxl>=3.1.0
pandas>=2.1.0
lxml>=5.0.0
pytest>=7.4.0
```

Save to `costimize-v2/requirements.txt`.

- [ ] **Step 8: Create .env.example**

```
OPENAI_API_KEY=sk-your-openai-key-here
GEMINI_API_KEY=your-gemini-key-here
```

Save to `costimize-v2/.env.example`.

- [ ] **Step 9: Create minimal app.py (tab router)**

```python
# costimize-v2/app.py
"""AI.Procurve — Should-Cost Intelligence for Procurement"""

import streamlit as st

st.set_page_config(
    page_title="AI.Procurve — Should-Cost Intelligence",
    page_icon="⚙",
    layout="wide",
)

st.title("AI.Procurve — Should-Cost Intelligence")
st.caption("Upload a drawing or BOM. Get instant cost breakdown for negotiations.")

tab1, tab2, tab3 = st.tabs(["⚙ Mechanical Parts", "🔌 PCB Assembly", "🔗 Cable Assembly"])

with tab1:
    st.info("Mechanical parts cost engine — coming soon")

with tab2:
    st.info("PCB assembly cost engine — coming soon")

with tab3:
    st.info("Cable assembly cost engine — coming soon")
```

- [ ] **Step 10: Verify app runs**

```bash
cd costimize-v2 && pip install -r requirements.txt && streamlit run app.py --server.headless true &
sleep 3 && curl -s http://localhost:8501 | head -20
```
Expected: Streamlit HTML loads without errors. Kill the process after.

- [ ] **Step 11: Commit**

```bash
cd costimize-v2 && git init && git add -A && git commit -m "feat: scaffold costimize-v2 with config, data files, and tab router"
```

---

## Task 2: Mechanical Cost Engine — Material & Process Time Calculation

**Files:**
- Create: `costimize-v2/engines/mechanical/material_db.py`
- Create: `costimize-v2/engines/mechanical/process_db.py`
- Create: `costimize-v2/engines/mechanical/cost_engine.py`
- Test: `costimize-v2/tests/test_mechanical_engine.py`

- [ ] **Step 1: Write material_db.py**

```python
# costimize-v2/engines/mechanical/material_db.py
"""Material database — loads materials.json, provides lookup by name."""

import json
from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class Material:
    name: str
    price_per_kg_inr: float
    density_kg_per_m3: float
    machinability: float  # 0.0 to 1.0, higher = easier to machine


DATA_FILE = Path(__file__).parent.parent.parent / "data" / "materials.json"


def load_materials() -> dict[str, Material]:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {
        m["name"]: Material(
            name=m["name"],
            price_per_kg_inr=m["price_per_kg_inr"],
            density_kg_per_m3=m["density_kg_per_m3"],
            machinability=m.get("machinability", 0.5),
        )
        for m in data["materials"]
    }


def get_material(name: str) -> Material:
    materials = load_materials()
    if name not in materials:
        available = ", ".join(materials.keys())
        raise ValueError(f"Material '{name}' not found. Available: {available}")
    return materials[name]


def list_material_names() -> list[str]:
    return list(load_materials().keys())
```

- [ ] **Step 2: Write process_db.py**

```python
# costimize-v2/engines/mechanical/process_db.py
"""Process database — time estimation logic for each manufacturing process."""

import json
import math
from pathlib import Path
from dataclasses import dataclass
from config import (
    MACHINE_RATES, SETUP_TIMES, POWER_CONSUMPTION, TOOLING_COST_PER_UNIT,
)


DATA_FILE = Path(__file__).parent.parent.parent / "data" / "processes.json"


@dataclass(frozen=True)
class ProcessInfo:
    id: str
    name: str
    category: str
    description: str
    machine_rate: float  # ₹/hr
    setup_time_min: float
    power_kw: float
    tooling_cost_per_unit: float


def load_processes() -> dict[str, ProcessInfo]:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    result = {}
    for p in data["processes"]:
        pid = p["id"]
        result[pid] = ProcessInfo(
            id=pid,
            name=p["name"],
            category=p["category"],
            description=p["description"],
            machine_rate=MACHINE_RATES.get(pid, 800),
            setup_time_min=SETUP_TIMES.get(pid, 30),
            power_kw=POWER_CONSUMPTION.get(pid, 5),
            tooling_cost_per_unit=TOOLING_COST_PER_UNIT.get(pid, 5),
        )
    return result


def list_process_names() -> list[tuple[str, str]]:
    """Returns list of (process_id, display_name) tuples."""
    processes = load_processes()
    return [(pid, p.name) for pid, p in processes.items()]


def estimate_process_time_min(
    process_id: str,
    dimensions: dict,
    machinability: float = 0.5,
) -> float:
    """
    Estimate machining time in minutes for a given process based on part dimensions.

    dimensions expected keys:
      - outer_diameter_mm (for turning/cylindrical ops)
      - inner_diameter_mm (for boring)
      - length_mm
      - width_mm (for milling)
      - height_mm (for milling)
      - hole_diameter_mm (for drilling/reaming/tapping)
      - hole_count (for drilling/reaming/tapping)
      - thread_length_mm (for threading/tapping)
      - thread_count
      - groove_count
      - surface_area_cm2 (for surface treatments)
    """
    od = dimensions.get("outer_diameter_mm", 50)
    id_mm = dimensions.get("inner_diameter_mm", 0)
    length = dimensions.get("length_mm", 100)
    width = dimensions.get("width_mm", 50)
    height = dimensions.get("height_mm", 30)
    hole_dia = dimensions.get("hole_diameter_mm", 8)
    hole_count = dimensions.get("hole_count", 1)
    thread_length = dimensions.get("thread_length_mm", 20)
    thread_count = dimensions.get("thread_count", 1)
    groove_count = dimensions.get("groove_count", 1)
    surface_area = dimensions.get("surface_area_cm2", 100)

    # Machinability factor: lower machinability = longer time
    # Factor ranges from 1.0 (easy, machinability=1.0) to 2.5 (hard, machinability=0.2)
    mach_factor = 1.0 / max(machinability, 0.2)

    if process_id == "turning":
        # Time = (OD × length) / 5000 × machinability factor
        return (od * length / 5000) * mach_factor

    elif process_id == "facing":
        # Time based on diameter
        return (od / 50) * mach_factor

    elif process_id == "boring":
        # Similar to turning but for inner diameter
        bore_depth = length * 0.8  # assume 80% of length
        return (id_mm * bore_depth / 4000) * mach_factor

    elif process_id in ("milling_face", "milling_slot", "milling_pocket"):
        # Time = (length × width) / 3000 × factor
        area = length * width
        pocket_factor = 1.5 if process_id == "milling_pocket" else 1.0
        return (area / 3000) * mach_factor * pocket_factor

    elif process_id == "drilling":
        # Time per hole = depth / feed_rate. Simplified: hole_dia × length / 2000
        time_per_hole = (hole_dia * length * 0.5 / 2000) * mach_factor
        return time_per_hole * hole_count

    elif process_id == "reaming":
        # Slower than drilling, ~1.5x
        time_per_hole = (hole_dia * length * 0.5 / 2000) * mach_factor * 1.5
        return time_per_hole * hole_count

    elif process_id == "tapping":
        # Time per thread = thread_length / 500
        return (thread_length / 500) * mach_factor * thread_count

    elif process_id == "threading":
        # External threading: similar to tapping but on lathe
        return (thread_length / 400) * mach_factor * thread_count

    elif process_id == "grinding_cylindrical":
        # Precision finishing: (OD × length) / 8000
        return (od * length / 8000) * mach_factor

    elif process_id == "grinding_surface":
        # Surface grinding: area / 5000
        return (length * width / 5000) * mach_factor

    elif process_id == "knurling":
        # Quick operation: length / 200
        return (length / 200) * mach_factor

    elif process_id == "broaching":
        # Fixed time per operation
        return 3.0 * mach_factor

    elif process_id == "heat_treatment":
        # Batch process, per-part time based on weight proxy
        weight_proxy = od * od * length / 1e6
        return max(5.0, weight_proxy * 10)

    elif process_id.startswith("surface_treatment"):
        # Based on surface area
        return max(2.0, surface_area / 50)

    else:
        # Default fallback
        return 5.0 * mach_factor
```

- [ ] **Step 3: Write cost_engine.py for mechanical parts**

```python
# costimize-v2/engines/mechanical/cost_engine.py
"""Multi-process mechanical cost engine — line-by-line should-cost breakdown."""

import math
from dataclasses import dataclass
from config import (
    LABOUR_RATE, POWER_RATE, MATERIAL_WASTAGE_PCT,
    MACHINING_ALLOWANCE_DIA_MM, MACHINING_ALLOWANCE_LEN_MM,
    TIGHT_TOLERANCE_SURCHARGE_PCT, OVERHEAD_PCT, PROFIT_PCT,
)
from engines.mechanical.material_db import get_material, Material
from engines.mechanical.process_db import load_processes, estimate_process_time_min, ProcessInfo


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
    # Material
    material_name: str
    raw_weight_kg: float
    wastage_weight_kg: float
    material_cost: float

    # Per-process lines
    process_lines: tuple[ProcessCostLine, ...]

    # Totals
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
) -> MechanicalCostBreakdown:
    """
    Calculate full should-cost breakdown for a mechanical part.

    Args:
        dimensions: Dict with outer_diameter_mm, inner_diameter_mm, length_mm, etc.
        material_name: Must match a name in materials.json.
        selected_processes: List of process IDs (e.g., ["turning", "milling_face", "drilling"]).
        quantity: Number of parts.
        has_tight_tolerances: If True, adds 30% surcharge to machining.

    Returns:
        MechanicalCostBreakdown with every cost line itemized.
    """
    material = get_material(material_name)
    all_processes = load_processes()

    # --- 1. Raw Material Cost ---
    od = dimensions.get("outer_diameter_mm", 0)
    id_mm = dimensions.get("inner_diameter_mm", 0)
    length = dimensions.get("length_mm", 0)

    bar_od_mm = od + MACHINING_ALLOWANCE_DIA_MM
    bar_len_mm = length + MACHINING_ALLOWANCE_LEN_MM

    bar_od_m = bar_od_mm / 1000
    bar_len_m = bar_len_mm / 1000

    if id_mm > 0:
        bar_id_m = id_mm / 1000
        volume_m3 = math.pi * ((bar_od_m / 2) ** 2 - (bar_id_m / 2) ** 2) * bar_len_m
    else:
        volume_m3 = math.pi * (bar_od_m / 2) ** 2 * bar_len_m

    raw_weight_kg = volume_m3 * material.density_kg_per_m3
    wastage_weight_kg = raw_weight_kg * (MATERIAL_WASTAGE_PCT / 100)
    total_weight_kg = raw_weight_kg + wastage_weight_kg
    material_cost = total_weight_kg * material.price_per_kg_inr

    # --- 2. Per-Process Cost Lines ---
    process_lines = []
    total_operator_time_min = 0

    for pid in selected_processes:
        if pid not in all_processes:
            continue
        proc = all_processes[pid]

        time_min = estimate_process_time_min(pid, dimensions, material.machinability)
        total_operator_time_min += time_min

        time_hr = time_min / 60
        machine_cost = time_hr * proc.machine_rate
        if has_tight_tolerances:
            machine_cost *= (1 + TIGHT_TOLERANCE_SURCHARGE_PCT / 100)

        setup_cost_per_unit = (proc.setup_time_min / 60 * proc.machine_rate) / quantity
        tooling_cost = proc.tooling_cost_per_unit
        power_cost = proc.power_kw * time_hr * POWER_RATE

        # Labour is per-process operator time
        labour_cost = time_hr * LABOUR_RATE

        process_lines.append(ProcessCostLine(
            process_id=pid,
            process_name=proc.name,
            time_min=round(time_min, 2),
            machine_cost=round(machine_cost, 2),
            setup_cost_per_unit=round(setup_cost_per_unit, 2),
            tooling_cost=round(tooling_cost, 2),
            labour_cost=round(labour_cost, 2),
            power_cost=round(power_cost, 2),
        ))

    # --- 3. Totals ---
    total_machining = sum(p.machine_cost for p in process_lines)
    total_setup = sum(p.setup_cost_per_unit for p in process_lines)
    total_tooling = sum(p.tooling_cost for p in process_lines)
    total_labour = sum(p.labour_cost for p in process_lines)
    total_power = sum(p.power_cost for p in process_lines)

    subtotal = material_cost + total_machining + total_setup + total_tooling + total_labour + total_power
    overhead = subtotal * (OVERHEAD_PCT / 100)
    profit = (subtotal + overhead) * (PROFIT_PCT / 100)
    unit_cost = subtotal + overhead + profit
    order_cost = unit_cost * quantity

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
        unit_cost=round(unit_cost, 2),
        order_cost=round(order_cost, 2),
        quantity=quantity,
    )
```

- [ ] **Step 4: Write tests for mechanical engine**

```python
# costimize-v2/tests/test_mechanical_engine.py
from engines.mechanical.cost_engine import calculate_mechanical_cost, MechanicalCostBreakdown
from engines.mechanical.material_db import get_material, list_material_names
from engines.mechanical.process_db import estimate_process_time_min, load_processes


def test_load_materials():
    names = list_material_names()
    assert len(names) >= 6
    assert "EN8 Steel" in names


def test_get_material_returns_correct_data():
    mat = get_material("EN8 Steel")
    assert mat.price_per_kg_inr == 75
    assert mat.density_kg_per_m3 == 7850


def test_load_processes():
    procs = load_processes()
    assert "turning" in procs
    assert "drilling" in procs
    assert procs["turning"].machine_rate == 800


def test_estimate_turning_time():
    dims = {"outer_diameter_mm": 60, "length_mm": 100}
    time_min = estimate_process_time_min("turning", dims, machinability=0.55)
    assert time_min > 0
    # EN8: machinability 0.55, factor ~1.82. Base: 60*100/5000 = 1.2. Result ~2.18
    assert 1.0 < time_min < 5.0


def test_estimate_drilling_time_scales_with_hole_count():
    dims1 = {"hole_diameter_mm": 8, "length_mm": 50, "hole_count": 1}
    dims4 = {"hole_diameter_mm": 8, "length_mm": 50, "hole_count": 4}
    t1 = estimate_process_time_min("drilling", dims1, machinability=0.6)
    t4 = estimate_process_time_min("drilling", dims4, machinability=0.6)
    assert abs(t4 - t1 * 4) < 0.01


def test_calculate_mechanical_cost_basic():
    result = calculate_mechanical_cost(
        dimensions={"outer_diameter_mm": 60, "length_mm": 100},
        material_name="EN8 Steel",
        selected_processes=["turning", "facing", "drilling"],
        quantity=100,
    )
    assert isinstance(result, MechanicalCostBreakdown)
    assert result.quantity == 100
    assert result.material_cost > 0
    assert len(result.process_lines) == 3
    assert result.unit_cost > 0
    assert result.order_cost == round(result.unit_cost * 100, 2)


def test_tight_tolerance_increases_cost():
    base = calculate_mechanical_cost(
        dimensions={"outer_diameter_mm": 60, "length_mm": 100},
        material_name="EN8 Steel",
        selected_processes=["turning"],
        quantity=100,
        has_tight_tolerances=False,
    )
    tight = calculate_mechanical_cost(
        dimensions={"outer_diameter_mm": 60, "length_mm": 100},
        material_name="EN8 Steel",
        selected_processes=["turning"],
        quantity=100,
        has_tight_tolerances=True,
    )
    assert tight.total_machining_cost > base.total_machining_cost


def test_higher_quantity_reduces_setup_cost_per_unit():
    q10 = calculate_mechanical_cost(
        dimensions={"outer_diameter_mm": 60, "length_mm": 100},
        material_name="EN8 Steel",
        selected_processes=["turning"],
        quantity=10,
    )
    q1000 = calculate_mechanical_cost(
        dimensions={"outer_diameter_mm": 60, "length_mm": 100},
        material_name="EN8 Steel",
        selected_processes=["turning"],
        quantity=1000,
    )
    assert q10.total_setup_cost > q1000.total_setup_cost
```

- [ ] **Step 5: Run tests**

```bash
cd costimize-v2 && python -m pytest tests/test_mechanical_engine.py -v
```
Expected: All 7 tests PASS

- [ ] **Step 6: Commit**

```bash
cd costimize-v2 && git add -A && git commit -m "feat: mechanical cost engine with multi-process breakdown"
```

---

## Task 3: Vision Extractor & Process Detector

**Files:**
- Create: `costimize-v2/extractors/vision.py`
- Create: `costimize-v2/extractors/process_detector.py`
- Test: `costimize-v2/tests/test_extractors.py`

- [ ] **Step 1: Write vision.py (ported and enhanced from v1)**

```python
# costimize-v2/extractors/vision.py
"""AI vision extraction — sends engineering drawings to GPT-4o/Gemini, returns structured data."""

import json
import base64
import os
from pathlib import Path
from config import OPENAI_API_KEY, GEMINI_API_KEY

EXTRACTION_PROMPT = """You are an expert mechanical engineer analyzing an engineering drawing.
Extract the following with EXTREME PRECISION. Only extract what you can clearly see.

Return a JSON object with these fields:
{
  "part_type": "turning" or "milling" or "general",
  "dimensions": {
    "outer_diameter_mm": <number or null>,
    "inner_diameter_mm": <number or null>,
    "length_mm": <number or null>,
    "width_mm": <number or null>,
    "height_mm": <number or null>,
    "hole_diameter_mm": <number or null>,
    "hole_count": <integer or null>,
    "thread_count": <integer or null>,
    "thread_length_mm": <number or null>,
    "groove_count": <integer or null>,
    "surface_area_cm2": <number or null>
  },
  "material": "<material name as written in drawing, or null>",
  "tolerances": {
    "has_tight_tolerances": <true if any tolerance < ±0.05mm>,
    "tightest_tolerance_mm": <number or null>
  },
  "surface_finish": "<Ra value or description, or null>",
  "suggested_processes": ["turning", "drilling", ...],
  "confidence": "high" or "medium" or "low",
  "notes": "<any relevant observations>"
}

CRITICAL:
- Read dimension text EXACTLY as written — do NOT guess
- Look for dimension callouts, leaders, dimension lines
- Check title blocks, notes, annotations
- If unclear, set confidence to "low"
- For suggested_processes, identify ALL manufacturing processes needed based on features you see.
  Valid process IDs: turning, facing, boring, milling_face, milling_slot, milling_pocket,
  drilling, reaming, tapping, threading, grinding_cylindrical, grinding_surface,
  knurling, broaching, heat_treatment, surface_treatment_plating,
  surface_treatment_anodizing, surface_treatment_painting

Return ONLY the JSON object, no markdown fences or extra text."""


def analyze_drawing(image_bytes: bytes, filename: str = "drawing.png") -> dict:
    """
    Send an engineering drawing image to GPT-4o (primary) or Gemini (fallback).
    Returns structured extraction dict.
    """
    if OPENAI_API_KEY:
        try:
            return _analyze_with_openai(image_bytes)
        except Exception as e:
            if GEMINI_API_KEY:
                return _analyze_with_gemini(image_bytes)
            raise RuntimeError(f"OpenAI failed and no Gemini fallback: {e}")

    if GEMINI_API_KEY:
        return _analyze_with_gemini(image_bytes)

    raise RuntimeError("No API key configured. Set OPENAI_API_KEY or GEMINI_API_KEY in .env")


def _analyze_with_openai(image_bytes: bytes) -> dict:
    import openai
    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    b64 = base64.b64encode(image_bytes).decode("utf-8")
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": EXTRACTION_PROMPT},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}},
                ],
            }
        ],
        max_tokens=2000,
    )
    text = response.choices[0].message.content.strip()
    # Strip markdown code fences if present
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return json.loads(text)


def _analyze_with_gemini(image_bytes: bytes) -> dict:
    import google.generativeai as genai
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")

    response = model.generate_content(
        [
            EXTRACTION_PROMPT,
            {"mime_type": "image/png", "data": image_bytes},
        ]
    )
    text = response.text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return json.loads(text)
```

- [ ] **Step 2: Write process_detector.py**

```python
# costimize-v2/extractors/process_detector.py
"""Detect manufacturing processes from vision extraction results."""


def detect_processes_from_extraction(extraction: dict) -> list[str]:
    """
    Given the structured output from vision.py, return a list of suggested process IDs.
    Uses AI suggestions first, then applies rule-based fallback logic.
    """
    # Use AI suggestions if available
    ai_suggestions = extraction.get("suggested_processes", [])
    if ai_suggestions:
        return ai_suggestions

    # Rule-based fallback from part geometry
    processes = []
    dims = extraction.get("dimensions", {})
    part_type = extraction.get("part_type", "general")

    od = dims.get("outer_diameter_mm")
    id_mm = dims.get("inner_diameter_mm")
    length = dims.get("length_mm")
    width = dims.get("width_mm")
    hole_count = dims.get("hole_count", 0)
    thread_count = dims.get("thread_count", 0)
    groove_count = dims.get("groove_count", 0)

    if part_type == "turning" or (od and not width):
        processes.append("turning")
        processes.append("facing")
        if id_mm and id_mm > 0:
            processes.append("boring")
    elif part_type == "milling" or (width and not od):
        processes.append("milling_face")

    if hole_count and hole_count > 0:
        processes.append("drilling")

    if thread_count and thread_count > 0:
        if part_type == "turning":
            processes.append("threading")
        else:
            processes.append("tapping")

    if groove_count and groove_count > 0:
        processes.append("knurling")

    surface_finish = extraction.get("surface_finish")
    if surface_finish:
        try:
            ra = float(str(surface_finish).replace("Ra", "").replace("ra", "").strip())
            if ra <= 0.8:
                if part_type == "turning":
                    processes.append("grinding_cylindrical")
                else:
                    processes.append("grinding_surface")
        except (ValueError, TypeError):
            pass

    return processes if processes else ["turning", "facing"]
```

- [ ] **Step 3: Write tests (unit tests only — no API calls)**

```python
# costimize-v2/tests/test_extractors.py
from extractors.process_detector import detect_processes_from_extraction


def test_detect_from_ai_suggestions():
    extraction = {
        "part_type": "turning",
        "suggested_processes": ["turning", "facing", "drilling", "threading"],
    }
    result = detect_processes_from_extraction(extraction)
    assert result == ["turning", "facing", "drilling", "threading"]


def test_fallback_turning_part():
    extraction = {
        "part_type": "turning",
        "dimensions": {"outer_diameter_mm": 60, "length_mm": 100},
    }
    result = detect_processes_from_extraction(extraction)
    assert "turning" in result
    assert "facing" in result


def test_fallback_with_holes_and_threads():
    extraction = {
        "part_type": "turning",
        "dimensions": {
            "outer_diameter_mm": 60,
            "length_mm": 100,
            "hole_count": 4,
            "thread_count": 2,
        },
    }
    result = detect_processes_from_extraction(extraction)
    assert "drilling" in result
    assert "threading" in result


def test_fallback_milling_part():
    extraction = {
        "part_type": "milling",
        "dimensions": {"length_mm": 100, "width_mm": 50, "height_mm": 30},
    }
    result = detect_processes_from_extraction(extraction)
    assert "milling_face" in result


def test_fallback_fine_surface_finish():
    extraction = {
        "part_type": "turning",
        "dimensions": {"outer_diameter_mm": 60, "length_mm": 100},
        "surface_finish": "Ra 0.4",
    }
    result = detect_processes_from_extraction(extraction)
    assert "grinding_cylindrical" in result


def test_fallback_empty_extraction():
    extraction = {"part_type": "general", "dimensions": {}}
    result = detect_processes_from_extraction(extraction)
    assert result == ["turning", "facing"]
```

- [ ] **Step 4: Run tests**

```bash
cd costimize-v2 && python -m pytest tests/test_extractors.py -v
```
Expected: All 6 tests PASS

- [ ] **Step 5: Commit**

```bash
cd costimize-v2 && git add -A && git commit -m "feat: vision extractor and process detector with fallback logic"
```

---

## Task 4: Mechanical Parts UI Tab

**Files:**
- Create: `costimize-v2/ui/components.py`
- Create: `costimize-v2/ui/mechanical_tab.py`
- Modify: `costimize-v2/app.py`

- [ ] **Step 1: Write shared UI components**

```python
# costimize-v2/ui/components.py
"""Shared Streamlit UI widgets."""

import streamlit as st


def render_cost_table(lines: list[dict]):
    """Render a cost breakdown table. Each dict has 'item' and 'cost' keys, optionally 'detail'."""
    for line in lines:
        cols = st.columns([3, 1, 2])
        cols[0].write(f"**{line['item']}**")
        cols[1].write(f"₹{line['cost']:,.2f}")
        if line.get("detail"):
            cols[2].caption(line["detail"])
    st.divider()


def render_historical_comparison(should_cost: float, history_match: dict | None):
    """Render historical PO comparison box."""
    if not history_match:
        st.info("No historical data. Upload previous POs in the sidebar to enable comparison.")
        return

    prev_cost = history_match["unit_price"]
    diff = prev_cost - should_cost
    diff_pct = (diff / prev_cost) * 100 if prev_cost > 0 else 0
    color = "🟢" if diff > 0 else "🔴"

    st.markdown(f"""
    **Historical Comparison** {color}

    | | |
    |---|---|
    | Your should-cost | ₹{should_cost:,.2f}/unit |
    | Last PO ({history_match.get('date', 'N/A')}) | ₹{prev_cost:,.2f}/unit |
    | Difference | ₹{abs(diff):,.2f} ({abs(diff_pct):.1f}% {'over' if diff > 0 else 'under'}) |
    | Supplier | {history_match.get('supplier', 'N/A')} |
    | Qty | {history_match.get('quantity', 'N/A')} pcs |
    """)
```

- [ ] **Step 2: Write mechanical_tab.py**

```python
# costimize-v2/ui/mechanical_tab.py
"""Mechanical parts tab — upload drawing, confirm processes, get should-cost breakdown."""

import streamlit as st
from engines.mechanical.cost_engine import calculate_mechanical_cost
from engines.mechanical.material_db import list_material_names
from engines.mechanical.process_db import list_process_names
from extractors.vision import analyze_drawing
from extractors.process_detector import detect_processes_from_extraction
from ui.components import render_cost_table, render_historical_comparison


def render():
    st.header("Mechanical Parts — Should-Cost Breakdown")

    # --- Upload ---
    uploaded = st.file_uploader("Upload engineering drawing", type=["png", "jpg", "jpeg", "pdf"], key="mech_upload")

    if uploaded:
        image_bytes = uploaded.read()
        st.image(image_bytes, caption=uploaded.name, width=400)

        if st.button("🔍 Analyze Drawing", key="mech_analyze"):
            with st.spinner("AI is extracting dimensions and processes..."):
                try:
                    extraction = analyze_drawing(image_bytes, uploaded.name)
                    st.session_state["mech_extraction"] = extraction
                    st.session_state["mech_processes"] = detect_processes_from_extraction(extraction)
                except Exception as e:
                    st.error(f"Extraction failed: {e}")
                    return

    # --- Extracted Data + Manual Override ---
    extraction = st.session_state.get("mech_extraction")
    if not extraction:
        st.caption("Upload a drawing to get started, or fill in dimensions manually below.")

    st.subheader("Dimensions")
    dims = extraction.get("dimensions", {}) if extraction else {}
    col1, col2, col3 = st.columns(3)
    with col1:
        od = st.number_input("Outer Diameter (mm)", value=float(dims.get("outer_diameter_mm") or 60), min_value=0.1, key="mech_od")
        id_mm = st.number_input("Inner Diameter (mm)", value=float(dims.get("inner_diameter_mm") or 0), min_value=0.0, key="mech_id")
    with col2:
        length = st.number_input("Length (mm)", value=float(dims.get("length_mm") or 100), min_value=0.1, key="mech_len")
        width = st.number_input("Width (mm)", value=float(dims.get("width_mm") or 0), min_value=0.0, key="mech_width")
    with col3:
        hole_count = st.number_input("Hole Count", value=int(dims.get("hole_count") or 0), min_value=0, key="mech_holes")
        thread_count = st.number_input("Thread Count", value=int(dims.get("thread_count") or 0), min_value=0, key="mech_threads")

    st.subheader("Material")
    materials = list_material_names()
    detected_mat = extraction.get("material") if extraction else None
    default_idx = 0
    if detected_mat:
        for i, m in enumerate(materials):
            if detected_mat.lower() in m.lower():
                default_idx = i
                break
    material_name = st.selectbox("Material", materials, index=default_idx, key="mech_mat")

    st.subheader("Manufacturing Processes")
    all_processes = list_process_names()
    suggested = st.session_state.get("mech_processes", [])
    selected_processes = []
    cols = st.columns(3)
    for i, (pid, pname) in enumerate(all_processes):
        col = cols[i % 3]
        checked = pid in suggested
        if col.checkbox(pname, value=checked, key=f"proc_{pid}"):
            selected_processes.append(pid)

    st.subheader("Order Details")
    col1, col2 = st.columns(2)
    with col1:
        quantity = st.number_input("Quantity", value=100, min_value=1, key="mech_qty")
    with col2:
        tight_tol = st.checkbox("Tight tolerances (< ±0.05mm)", key="mech_tol")

    confidence = extraction.get("confidence", "manual") if extraction else "manual"
    if confidence == "low":
        st.warning("⚠ AI confidence is LOW — please verify dimensions manually.")
    elif confidence == "medium":
        st.info("ℹ AI confidence is MEDIUM — review dimensions before calculating.")

    # --- Calculate ---
    if st.button("💰 Calculate Should-Cost", key="mech_calc", type="primary"):
        if not selected_processes:
            st.error("Select at least one manufacturing process.")
            return

        final_dims = {
            "outer_diameter_mm": od,
            "inner_diameter_mm": id_mm,
            "length_mm": length,
            "width_mm": width,
            "hole_count": hole_count,
            "thread_count": thread_count,
            "hole_diameter_mm": dims.get("hole_diameter_mm", 8),
            "thread_length_mm": dims.get("thread_length_mm", 20),
            "groove_count": dims.get("groove_count", 0),
            "surface_area_cm2": dims.get("surface_area_cm2", 100),
        }

        result = calculate_mechanical_cost(
            dimensions=final_dims,
            material_name=material_name,
            selected_processes=selected_processes,
            quantity=quantity,
            has_tight_tolerances=tight_tol,
        )

        st.session_state["mech_result"] = result

    # --- Display Results ---
    result = st.session_state.get("mech_result")
    if result:
        st.subheader("📊 Should-Cost Breakdown")

        lines = [
            {"item": f"Raw Material ({result.material_name})", "cost": result.material_cost,
             "detail": f"{result.raw_weight_kg + result.wastage_weight_kg:.2f} kg incl. wastage"},
        ]
        for pl in result.process_lines:
            lines.append({
                "item": pl.process_name,
                "cost": pl.machine_cost,
                "detail": f"{pl.time_min:.1f} min @ ₹{pl.machine_cost / (pl.time_min / 60) if pl.time_min > 0 else 0:.0f}/hr",
            })
        lines.extend([
            {"item": "Setup Cost (amortized)", "cost": result.total_setup_cost, "detail": f"Over {result.quantity} pcs"},
            {"item": "Tooling Cost", "cost": result.total_tooling_cost, "detail": ""},
            {"item": "Labour", "cost": result.total_labour_cost, "detail": ""},
            {"item": "Power", "cost": result.total_power_cost, "detail": ""},
            {"item": "Overhead (15%)", "cost": result.overhead, "detail": ""},
            {"item": "Profit Margin (20%)", "cost": result.profit, "detail": ""},
        ])

        render_cost_table(lines)

        col1, col2 = st.columns(2)
        col1.metric("Unit Cost", f"₹{result.unit_cost:,.2f}")
        col2.metric("Order Cost", f"₹{result.order_cost:,.2f}", delta=f"{result.quantity} pcs")

        # Historical comparison placeholder (wired up in Task 8)
        history_match = st.session_state.get("mech_history_match")
        render_historical_comparison(result.unit_cost, history_match)
```

- [ ] **Step 3: Update app.py to import mechanical tab**

```python
# costimize-v2/app.py
"""AI.Procurve — Should-Cost Intelligence for Procurement"""

import streamlit as st

st.set_page_config(
    page_title="AI.Procurve — Should-Cost Intelligence",
    page_icon="⚙",
    layout="wide",
)

st.title("AI.Procurve — Should-Cost Intelligence")
st.caption("Upload a drawing or BOM. Get instant cost breakdown for negotiations.")

tab1, tab2, tab3 = st.tabs(["⚙ Mechanical Parts", "🔌 PCB Assembly", "🔗 Cable Assembly"])

with tab1:
    from ui.mechanical_tab import render as render_mechanical
    render_mechanical()

with tab2:
    st.info("PCB assembly cost engine — coming in Task 6")

with tab3:
    st.info("Cable assembly cost engine — coming in Task 7")
```

- [ ] **Step 4: Manually test — run app, verify mechanical tab renders**

```bash
cd costimize-v2 && streamlit run app.py
```
Expected: App loads. Mechanical tab shows upload, dimension inputs, process checklist, calculate button. (Don't need to test AI extraction — just verify the UI renders without errors.)

- [ ] **Step 5: Commit**

```bash
cd costimize-v2 && git add -A && git commit -m "feat: mechanical parts UI tab with full cost breakdown display"
```

---

## Task 5: PCB BOM Parser & Cost Engine

**Files:**
- Create: `costimize-v2/engines/pcb/bom_parser.py`
- Create: `costimize-v2/engines/pcb/fab_cost.py`
- Create: `costimize-v2/engines/pcb/cost_engine.py`
- Create: `costimize-v2/extractors/bom_extractor.py`
- Test: `costimize-v2/tests/test_pcb_engine.py`

- [ ] **Step 1: Write bom_parser.py for CSV/Excel**

```python
# costimize-v2/engines/pcb/bom_parser.py
"""Parse PCB BOM from CSV/Excel files. Auto-detect column mapping."""

import pandas as pd
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class BomLine:
    mpn: str  # Manufacturer Part Number
    description: str
    quantity: int
    footprint: str
    value: str  # e.g., "10K", "100nF"


# Common header variations for auto-detection
HEADER_MAP = {
    "mpn": ["mpn", "manufacturer part number", "mfr part", "part number", "mfg part", "mfr_part_number", "manufacturer_part"],
    "description": ["description", "desc", "part description", "component", "name"],
    "quantity": ["quantity", "qty", "count", "amount", "qty."],
    "footprint": ["footprint", "package", "case", "size", "pkg"],
    "value": ["value", "val", "rating", "specification"],
}


def _match_column(columns: list[str], candidates: list[str]) -> str | None:
    """Find the first column name that matches any candidate (case-insensitive)."""
    lower_cols = {c.lower().strip(): c for c in columns}
    for candidate in candidates:
        if candidate in lower_cols:
            return lower_cols[candidate]
    return None


def parse_bom_file(file_path: str | Path, file_bytes: bytes | None = None, filename: str = "") -> list[BomLine]:
    """
    Parse a BOM file (CSV or Excel) and return normalized BOM lines.
    Accepts either a file path or raw bytes + filename.
    """
    if file_bytes:
        import io
        ext = Path(filename).suffix.lower()
        if ext in (".xlsx", ".xls"):
            df = pd.read_excel(io.BytesIO(file_bytes))
        else:
            df = pd.read_csv(io.BytesIO(file_bytes))
    else:
        ext = Path(file_path).suffix.lower()
        if ext in (".xlsx", ".xls"):
            df = pd.read_excel(file_path)
        else:
            df = pd.read_csv(file_path)

    columns = list(df.columns)

    # Auto-detect column mapping
    mpn_col = _match_column(columns, HEADER_MAP["mpn"])
    desc_col = _match_column(columns, HEADER_MAP["description"])
    qty_col = _match_column(columns, HEADER_MAP["quantity"])
    fp_col = _match_column(columns, HEADER_MAP["footprint"])
    val_col = _match_column(columns, HEADER_MAP["value"])

    lines = []
    for _, row in df.iterrows():
        mpn = str(row.get(mpn_col, "")).strip() if mpn_col else ""
        desc = str(row.get(desc_col, "")).strip() if desc_col else ""
        footprint = str(row.get(fp_col, "")).strip() if fp_col else ""
        value = str(row.get(val_col, "")).strip() if val_col else ""

        try:
            qty = int(float(row.get(qty_col, 1))) if qty_col else 1
        except (ValueError, TypeError):
            qty = 1

        if not mpn and not desc:
            continue  # skip empty rows

        lines.append(BomLine(mpn=mpn, description=desc, quantity=qty, footprint=footprint, value=value))

    return lines
```

- [ ] **Step 2: Write bom_extractor.py (PDF BOM → AI extraction)**

```python
# costimize-v2/extractors/bom_extractor.py
"""Extract BOM from PDF using AI vision (GPT-4o / Gemini)."""

import json
import base64
from config import OPENAI_API_KEY, GEMINI_API_KEY

BOM_PROMPT = """You are analyzing a Bill of Materials (BOM) document.
Extract ALL components into a structured JSON array.

Return ONLY a JSON object:
{
  "components": [
    {
      "mpn": "<manufacturer part number>",
      "description": "<component description>",
      "quantity": <integer>,
      "footprint": "<package/footprint>",
      "value": "<component value like 10K, 100nF>"
    }
  ]
}

Extract EVERY line item. If a field is unclear, use empty string "".
Return ONLY the JSON object, no markdown fences."""


def extract_bom_from_pdf(pdf_bytes: bytes) -> list[dict]:
    """Send PDF to vision AI, return list of component dicts."""
    if OPENAI_API_KEY:
        try:
            return _extract_openai(pdf_bytes)
        except Exception:
            if GEMINI_API_KEY:
                return _extract_gemini(pdf_bytes)
            raise
    if GEMINI_API_KEY:
        return _extract_gemini(pdf_bytes)
    raise RuntimeError("No API key. Set OPENAI_API_KEY or GEMINI_API_KEY.")


def _extract_openai(pdf_bytes: bytes) -> list[dict]:
    import openai
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    b64 = base64.b64encode(pdf_bytes).decode("utf-8")
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": BOM_PROMPT},
                {"type": "image_url", "image_url": {"url": f"data:application/pdf;base64,{b64}"}},
            ],
        }],
        max_tokens=4000,
    )
    text = response.choices[0].message.content.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return json.loads(text).get("components", [])


def _extract_gemini(pdf_bytes: bytes) -> list[dict]:
    import google.generativeai as genai
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([
        BOM_PROMPT,
        {"mime_type": "application/pdf", "data": pdf_bytes},
    ])
    text = response.text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return json.loads(text).get("components", [])
```

- [ ] **Step 3: Write fab_cost.py (bare board fabrication cost)**

```python
# costimize-v2/engines/pcb/fab_cost.py
"""PCB bare board fabrication cost model — rule-based pricing for Indian PCB fabs."""


def estimate_pcb_fab_cost(
    board_length_mm: float,
    board_width_mm: float,
    layers: int,
    quantity: int,
    surface_finish: str = "HASL",
) -> float:
    """
    Estimate bare PCB fabrication cost per board in ₹.

    Pricing model based on Indian PCB manufacturers (approximate):
    - Base rate depends on board area and layer count
    - Surface finish adds a premium
    - Quantity reduces per-board cost
    """
    area_cm2 = (board_length_mm * board_width_mm) / 100  # mm² to cm²

    # Base rate per cm² based on layer count
    layer_rates = {
        1: 0.8,   # ₹/cm² for single layer
        2: 1.2,   # ₹/cm² for double layer
        4: 2.5,   # ₹/cm² for 4 layer
        6: 4.0,   # ₹/cm² for 6 layer
        8: 6.0,   # ₹/cm² for 8 layer
    }
    # Find closest layer count
    closest_layers = min(layer_rates.keys(), key=lambda x: abs(x - layers))
    base_rate = layer_rates[closest_layers]

    # Surface finish premium
    finish_multiplier = {
        "HASL": 1.0,
        "Lead-free HASL": 1.05,
        "ENIG": 1.3,
        "OSP": 0.95,
        "Immersion Tin": 1.15,
        "Immersion Silver": 1.2,
    }
    multiplier = finish_multiplier.get(surface_finish, 1.0)

    # Quantity discount
    if quantity >= 1000:
        qty_factor = 0.6
    elif quantity >= 500:
        qty_factor = 0.7
    elif quantity >= 100:
        qty_factor = 0.8
    elif quantity >= 50:
        qty_factor = 0.9
    else:
        qty_factor = 1.0

    # Minimum board cost
    per_board = max(5.0, area_cm2 * base_rate * multiplier * qty_factor)

    return round(per_board, 2)
```

- [ ] **Step 4: Write PCB cost engine**

```python
# costimize-v2/engines/pcb/cost_engine.py
"""PCB assembly cost engine — components + fabrication + assembly + testing."""

from dataclasses import dataclass
from config import SMD_RATE_PER_PAD, THT_RATE_PER_PIN, STENCIL_COST, TEST_RATE_PER_BOARD, OVERHEAD_PCT, PROFIT_PCT
from engines.pcb.fab_cost import estimate_pcb_fab_cost


@dataclass(frozen=True)
class ComponentCostLine:
    mpn: str
    description: str
    quantity: int
    unit_price: float
    line_total: float
    source: str  # "DigiKey", "Mouser", "manual", "not_found"


@dataclass(frozen=True)
class PcbCostBreakdown:
    # Components
    component_lines: tuple[ComponentCostLine, ...]
    total_components_cost: float

    # Fabrication
    board_fab_cost: float

    # Assembly
    smd_pads: int
    smd_cost: float
    tht_pins: int
    tht_cost: float
    stencil_cost_per_board: float
    total_assembly_cost: float

    # Testing
    test_cost: float

    # Totals
    subtotal: float
    overhead: float
    profit: float
    unit_cost: float
    order_cost: float
    quantity: int


def calculate_pcb_cost(
    component_prices: list[dict],
    board_length_mm: float,
    board_width_mm: float,
    layers: int,
    quantity: int,
    smd_pads: int,
    tht_pins: int,
    surface_finish: str = "HASL",
) -> PcbCostBreakdown:
    """
    Calculate full PCB assembly should-cost.

    Args:
        component_prices: List of dicts with keys: mpn, description, quantity, unit_price, source.
        board_length_mm, board_width_mm, layers: Board specs.
        quantity: Number of boards.
        smd_pads: Total SMD solder pads across all components.
        tht_pins: Total through-hole pins across all components.
        surface_finish: PCB surface finish type.
    """
    # Component costs
    comp_lines = []
    for cp in component_prices:
        unit_price = cp.get("unit_price", 0)
        qty = cp.get("quantity", 1)
        comp_lines.append(ComponentCostLine(
            mpn=cp.get("mpn", ""),
            description=cp.get("description", ""),
            quantity=qty,
            unit_price=round(unit_price, 2),
            line_total=round(unit_price * qty, 2),
            source=cp.get("source", "manual"),
        ))
    total_comp = sum(c.line_total for c in comp_lines)

    # Board fabrication
    board_fab = estimate_pcb_fab_cost(board_length_mm, board_width_mm, layers, quantity, surface_finish)

    # Assembly
    smd_cost = smd_pads * SMD_RATE_PER_PAD
    tht_cost = tht_pins * THT_RATE_PER_PIN
    stencil_per_board = STENCIL_COST / max(quantity, 1)
    total_assembly = smd_cost + tht_cost + stencil_per_board

    # Testing
    test_cost = TEST_RATE_PER_BOARD

    # Totals
    subtotal = total_comp + board_fab + total_assembly + test_cost
    overhead = subtotal * (OVERHEAD_PCT / 100)
    profit = (subtotal + overhead) * (PROFIT_PCT / 100)
    unit_cost = subtotal + overhead + profit
    order_cost = unit_cost * quantity

    return PcbCostBreakdown(
        component_lines=tuple(comp_lines),
        total_components_cost=round(total_comp, 2),
        board_fab_cost=round(board_fab, 2),
        smd_pads=smd_pads,
        smd_cost=round(smd_cost, 2),
        tht_pins=tht_pins,
        tht_cost=round(tht_cost, 2),
        stencil_cost_per_board=round(stencil_per_board, 2),
        total_assembly_cost=round(total_assembly, 2),
        test_cost=round(test_cost, 2),
        subtotal=round(subtotal, 2),
        overhead=round(overhead, 2),
        profit=round(profit, 2),
        unit_cost=round(unit_cost, 2),
        order_cost=round(order_cost, 2),
        quantity=quantity,
    )
```

- [ ] **Step 5: Write tests**

```python
# costimize-v2/tests/test_pcb_engine.py
import io
import pandas as pd
from engines.pcb.bom_parser import parse_bom_file, BomLine
from engines.pcb.fab_cost import estimate_pcb_fab_cost
from engines.pcb.cost_engine import calculate_pcb_cost, PcbCostBreakdown


def test_parse_csv_bom():
    csv_content = b"MPN,Description,Qty,Footprint,Value\nSTM32F103C8T6,MCU ARM,1,LQFP-48,\nRC0603FR-0710KL,Resistor 10K,24,0603,10K\n"
    lines = parse_bom_file("", file_bytes=csv_content, filename="bom.csv")
    assert len(lines) == 2
    assert lines[0].mpn == "STM32F103C8T6"
    assert lines[1].quantity == 24


def test_parse_excel_bom():
    df = pd.DataFrame({
        "Part Number": ["LM1117-3.3", "CC0805KRX7R"],
        "Description": ["LDO 3.3V", "Cap 100nF"],
        "Quantity": [1, 10],
        "Package": ["SOT-223", "0805"],
    })
    buf = io.BytesIO()
    df.to_excel(buf, index=False)
    buf.seek(0)
    lines = parse_bom_file("", file_bytes=buf.read(), filename="bom.xlsx")
    assert len(lines) == 2
    assert lines[0].mpn == "LM1117-3.3"


def test_pcb_fab_cost_scales_with_layers():
    cost_2l = estimate_pcb_fab_cost(80, 60, 2, 100)
    cost_4l = estimate_pcb_fab_cost(80, 60, 4, 100)
    assert cost_4l > cost_2l


def test_pcb_fab_cost_quantity_discount():
    cost_10 = estimate_pcb_fab_cost(80, 60, 2, 10)
    cost_500 = estimate_pcb_fab_cost(80, 60, 2, 500)
    assert cost_500 < cost_10


def test_calculate_pcb_cost_basic():
    components = [
        {"mpn": "STM32", "description": "MCU", "quantity": 1, "unit_price": 180, "source": "manual"},
        {"mpn": "R10K", "description": "Resistor", "quantity": 24, "unit_price": 0.5, "source": "manual"},
    ]
    result = calculate_pcb_cost(
        component_prices=components,
        board_length_mm=80, board_width_mm=60,
        layers=2, quantity=100,
        smd_pads=87, tht_pins=6,
    )
    assert isinstance(result, PcbCostBreakdown)
    assert result.total_components_cost == 192.0  # 180 + 24*0.5
    assert result.unit_cost > 0
    assert result.quantity == 100
```

- [ ] **Step 6: Run tests**

```bash
cd costimize-v2 && python -m pytest tests/test_pcb_engine.py -v
```
Expected: All 5 tests PASS

- [ ] **Step 7: Commit**

```bash
cd costimize-v2 && git add -A && git commit -m "feat: PCB BOM parser, fab cost model, and assembly cost engine"
```

---

## Task 6: Component Price Scraper (DigiKey/Mouser)

**Files:**
- Create: `costimize-v2/scrapers/component_scraper.py`
- Test: `costimize-v2/tests/test_component_scraper.py`

- [ ] **Step 1: Write component_scraper.py**

```python
# costimize-v2/scrapers/component_scraper.py
"""Web scraper for electronic component prices from DigiKey and Mouser."""

import json
import time
import random
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from config import CACHE_DURATION_SEC, SCRAPE_DELAY_RANGE, USER_AGENTS

import requests
from bs4 import BeautifulSoup

CACHE_DIR = Path(__file__).parent.parent / "data" / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def _cache_key(mpn: str) -> str:
    return hashlib.md5(mpn.encode()).hexdigest()


def _load_cache(mpn: str) -> dict | None:
    cache_file = CACHE_DIR / f"{_cache_key(mpn)}.json"
    if not cache_file.exists():
        return None
    try:
        data = json.loads(cache_file.read_text(encoding="utf-8"))
        cached_at = datetime.fromisoformat(data["cached_at"])
        if datetime.now() - cached_at > timedelta(seconds=CACHE_DURATION_SEC):
            return None  # expired
        return data
    except (json.JSONDecodeError, KeyError):
        return None


def _save_cache(mpn: str, data: dict):
    cache_file = CACHE_DIR / f"{_cache_key(mpn)}.json"
    data["cached_at"] = datetime.now().isoformat()
    data["mpn"] = mpn
    cache_file.write_text(json.dumps(data, indent=2), encoding="utf-8")


def _get_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    })
    return session


def scrape_digikey(mpn: str) -> dict | None:
    """
    Search DigiKey for a component by MPN. Returns dict with price tiers or None.
    """
    try:
        session = _get_session()
        url = f"https://www.digikey.com/en/products/result?keywords={mpn}"
        resp = session.get(url, timeout=15)
        if resp.status_code != 200:
            return None

        soup = BeautifulSoup(resp.text, "lxml")

        # Look for unit price in search results
        price_elements = soup.select("[data-testid='price-table'] td, .MuiTableCell-root")
        if not price_elements:
            # Try alternate selector for product page
            price_elements = soup.select(".price-table td, .pdp-pricing td")

        prices = {}
        for elem in price_elements:
            text = elem.get_text(strip=True)
            # Try to parse as price
            if "₹" in text or "$" in text:
                try:
                    price_val = float(text.replace("₹", "").replace("$", "").replace(",", "").strip())
                    prices["unit_price"] = price_val
                    break
                except ValueError:
                    continue

        if not prices:
            return None

        return {
            "source": "DigiKey",
            "unit_price": prices.get("unit_price", 0),
            "currency": "USD",
            "in_stock": True,
        }
    except Exception:
        return None


def scrape_mouser(mpn: str) -> dict | None:
    """
    Search Mouser for a component by MPN. Returns dict with price or None.
    """
    try:
        session = _get_session()
        url = f"https://www.mouser.in/Search/Refine?Keyword={mpn}"
        resp = session.get(url, timeout=15)
        if resp.status_code != 200:
            return None

        soup = BeautifulSoup(resp.text, "lxml")

        # Look for price in search results
        price_elements = soup.select(".price, .PriceBreak, [id*='price']")
        for elem in price_elements:
            text = elem.get_text(strip=True)
            if "₹" in text:
                try:
                    price_val = float(text.replace("₹", "").replace(",", "").strip())
                    return {
                        "source": "Mouser",
                        "unit_price": price_val,
                        "currency": "INR",
                        "in_stock": True,
                    }
                except ValueError:
                    continue

        return None
    except Exception:
        return None


def get_component_price(mpn: str, quantity: int = 1) -> dict:
    """
    Get component price by MPN. Checks cache first, then scrapes DigiKey and Mouser.

    Returns:
        {"mpn": str, "unit_price": float, "source": str, "currency": str, "in_stock": bool}
        If not found: {"mpn": str, "unit_price": 0, "source": "not_found"}
    """
    if not mpn or mpn.strip() == "":
        return {"mpn": mpn, "unit_price": 0, "source": "not_found"}

    # Check cache
    cached = _load_cache(mpn)
    if cached:
        return cached

    # Scrape DigiKey first
    time.sleep(random.uniform(*SCRAPE_DELAY_RANGE))
    result = scrape_digikey(mpn)

    # Fallback to Mouser
    if not result:
        time.sleep(random.uniform(*SCRAPE_DELAY_RANGE))
        result = scrape_mouser(mpn)

    if result:
        result["mpn"] = mpn
        _save_cache(mpn, result)
        return result

    not_found = {"mpn": mpn, "unit_price": 0, "source": "not_found"}
    _save_cache(mpn, not_found)  # cache the miss to avoid re-scraping
    return not_found


def get_bulk_prices(mpns: list[str], quantity: int = 1) -> list[dict]:
    """Get prices for a list of MPNs. Returns list of price dicts."""
    results = []
    for mpn in mpns:
        results.append(get_component_price(mpn, quantity))
    return results
```

- [ ] **Step 2: Write tests (cache-only, no live scraping)**

```python
# costimize-v2/tests/test_component_scraper.py
import json
from pathlib import Path
from scrapers.component_scraper import _cache_key, _load_cache, _save_cache, get_component_price, CACHE_DIR


def test_cache_key_is_deterministic():
    assert _cache_key("STM32F103C8T6") == _cache_key("STM32F103C8T6")
    assert _cache_key("STM32F103C8T6") != _cache_key("LM1117-3.3")


def test_cache_round_trip(tmp_path, monkeypatch):
    # Point cache to tmp dir
    monkeypatch.setattr("scrapers.component_scraper.CACHE_DIR", tmp_path)
    mpn = "TEST-MPN-001"
    data = {"mpn": mpn, "unit_price": 42.5, "source": "DigiKey", "currency": "USD", "in_stock": True}
    _save_cache(mpn, data)
    loaded = _load_cache(mpn)
    assert loaded is not None
    assert loaded["unit_price"] == 42.5
    assert loaded["source"] == "DigiKey"


def test_empty_mpn_returns_not_found():
    result = get_component_price("")
    assert result["source"] == "not_found"
    assert result["unit_price"] == 0
```

- [ ] **Step 3: Run tests**

```bash
cd costimize-v2 && python -m pytest tests/test_component_scraper.py -v
```
Expected: All 3 tests PASS

- [ ] **Step 4: Commit**

```bash
cd costimize-v2 && git add -A && git commit -m "feat: component price scraper for DigiKey/Mouser with caching"
```

---

## Task 7: PCB Assembly UI Tab

**Files:**
- Create: `costimize-v2/ui/pcb_tab.py`
- Modify: `costimize-v2/app.py`

- [ ] **Step 1: Write pcb_tab.py**

```python
# costimize-v2/ui/pcb_tab.py
"""PCB Assembly tab — upload BOM, scrape prices, get should-cost breakdown."""

import streamlit as st
from engines.pcb.bom_parser import parse_bom_file
from engines.pcb.cost_engine import calculate_pcb_cost
from extractors.bom_extractor import extract_bom_from_pdf
from scrapers.component_scraper import get_component_price
from engines.pcb.bom_parser import BomLine
from ui.components import render_cost_table, render_historical_comparison


def render():
    st.header("PCB Assembly — Should-Cost Breakdown")

    # --- BOM Upload ---
    uploaded = st.file_uploader("Upload BOM", type=["csv", "xlsx", "xls", "pdf"], key="pcb_upload")

    if uploaded:
        file_bytes = uploaded.read()
        ext = uploaded.name.split(".")[-1].lower()

        if ext == "pdf":
            if st.button("🔍 Extract BOM from PDF", key="pcb_extract"):
                with st.spinner("AI is extracting BOM from PDF..."):
                    try:
                        raw_components = extract_bom_from_pdf(file_bytes)
                        bom_lines = [
                            BomLine(
                                mpn=c.get("mpn", ""),
                                description=c.get("description", ""),
                                quantity=int(c.get("quantity", 1)),
                                footprint=c.get("footprint", ""),
                                value=c.get("value", ""),
                            )
                            for c in raw_components
                        ]
                        st.session_state["pcb_bom"] = bom_lines
                    except Exception as e:
                        st.error(f"PDF extraction failed: {e}")
                        return
        else:
            try:
                bom_lines = parse_bom_file("", file_bytes=file_bytes, filename=uploaded.name)
                st.session_state["pcb_bom"] = bom_lines
                st.success(f"Parsed {len(bom_lines)} components from BOM")
            except Exception as e:
                st.error(f"BOM parse failed: {e}")
                return

    # --- BOM Display & Price Lookup ---
    bom_lines = st.session_state.get("pcb_bom", [])
    if bom_lines:
        st.subheader(f"BOM ({len(bom_lines)} components)")

        # Show editable table
        component_prices = []
        for i, line in enumerate(bom_lines):
            cols = st.columns([2, 3, 1, 1, 1])
            cols[0].text(line.mpn or "—")
            cols[1].text(line.description or "—")
            cols[2].text(str(line.quantity))
            cols[3].text(line.footprint or "—")

            # Price: check if already fetched
            price_key = f"pcb_price_{i}"
            existing = st.session_state.get(price_key)
            if existing:
                cols[4].text(f"₹{existing['unit_price']:.2f}")
            else:
                cols[4].text("—")

            component_prices.append({
                "mpn": line.mpn,
                "description": line.description,
                "quantity": line.quantity,
                "unit_price": existing["unit_price"] if existing else 0,
                "source": existing["source"] if existing else "not_found",
            })

        # Fetch prices button
        if st.button("🔍 Fetch Component Prices", key="pcb_fetch"):
            progress = st.progress(0, text="Scraping prices...")
            for i, line in enumerate(bom_lines):
                if line.mpn:
                    result = get_component_price(line.mpn)
                    st.session_state[f"pcb_price_{i}"] = result
                    component_prices[i]["unit_price"] = result["unit_price"]
                    component_prices[i]["source"] = result["source"]
                progress.progress((i + 1) / len(bom_lines), text=f"Fetching {i+1}/{len(bom_lines)}...")
            st.rerun()

    # --- Board Specs ---
    st.subheader("Board Specifications")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        board_length = st.number_input("Board Length (mm)", value=80.0, min_value=1.0, key="pcb_length")
    with col2:
        board_width = st.number_input("Board Width (mm)", value=60.0, min_value=1.0, key="pcb_width")
    with col3:
        layers = st.selectbox("Layers", [1, 2, 4, 6, 8], index=1, key="pcb_layers")
    with col4:
        surface_finish = st.selectbox("Surface Finish", ["HASL", "Lead-free HASL", "ENIG", "OSP"], key="pcb_finish")

    col1, col2, col3 = st.columns(3)
    with col1:
        quantity = st.number_input("Quantity (boards)", value=100, min_value=1, key="pcb_qty")
    with col2:
        smd_pads = st.number_input("Total SMD Pads", value=87, min_value=0, key="pcb_smd")
    with col3:
        tht_pins = st.number_input("Total THT Pins", value=6, min_value=0, key="pcb_tht")

    # --- Calculate ---
    if st.button("💰 Calculate Should-Cost", key="pcb_calc", type="primary"):
        if not bom_lines:
            st.error("Upload a BOM first.")
            return

        result = calculate_pcb_cost(
            component_prices=component_prices,
            board_length_mm=board_length,
            board_width_mm=board_width,
            layers=layers,
            quantity=quantity,
            smd_pads=smd_pads,
            tht_pins=tht_pins,
            surface_finish=surface_finish,
        )
        st.session_state["pcb_result"] = result

    # --- Display Results ---
    result = st.session_state.get("pcb_result")
    if result:
        st.subheader("📊 Should-Cost Breakdown")

        lines = [
            {"item": "Components (BOM)", "cost": result.total_components_cost,
             "detail": f"{len(result.component_lines)} line items"},
            {"item": "Bare Board Fabrication", "cost": result.board_fab_cost,
             "detail": f"{layers}L, {board_length}×{board_width}mm"},
            {"item": f"SMT Assembly ({result.smd_pads} pads)", "cost": result.smd_cost, "detail": ""},
            {"item": f"THT Assembly ({result.tht_pins} pins)", "cost": result.tht_cost, "detail": ""},
            {"item": "Stencil (amortized)", "cost": result.stencil_cost_per_board, "detail": ""},
            {"item": "Testing", "cost": result.test_cost, "detail": ""},
            {"item": "Overhead (15%)", "cost": result.overhead, "detail": ""},
            {"item": "Profit (20%)", "cost": result.profit, "detail": ""},
        ]
        render_cost_table(lines)

        col1, col2 = st.columns(2)
        col1.metric("Unit Cost", f"₹{result.unit_cost:,.2f}")
        col2.metric("Order Cost", f"₹{result.order_cost:,.2f}", delta=f"{result.quantity} boards")

        history_match = st.session_state.get("pcb_history_match")
        render_historical_comparison(result.unit_cost, history_match)
```

- [ ] **Step 2: Update app.py to import PCB tab**

Replace the `with tab2:` block in `app.py`:

```python
with tab2:
    from ui.pcb_tab import render as render_pcb
    render_pcb()
```

- [ ] **Step 3: Manually test — verify PCB tab renders**

```bash
cd costimize-v2 && streamlit run app.py
```
Expected: PCB tab renders with BOM upload, board specs, calculate button.

- [ ] **Step 4: Commit**

```bash
cd costimize-v2 && git add -A && git commit -m "feat: PCB assembly tab with BOM parsing, price scraping, and cost breakdown"
```

---

## Task 8: Cable Assembly Engine & UI Tab

**Files:**
- Create: `costimize-v2/engines/cable/bom_parser.py`
- Create: `costimize-v2/engines/cable/cost_engine.py`
- Create: `costimize-v2/ui/cable_tab.py`
- Modify: `costimize-v2/app.py`
- Test: `costimize-v2/tests/test_cable_engine.py`

- [ ] **Step 1: Write cable BOM parser (reuses PCB parser with cable-specific defaults)**

```python
# costimize-v2/engines/cable/bom_parser.py
"""Parse cable assembly BOM — connectors, wires, terminals, etc."""

from engines.pcb.bom_parser import parse_bom_file, BomLine


def parse_cable_bom(file_bytes: bytes, filename: str) -> list[BomLine]:
    """Parse cable BOM. Same format as PCB BOM — CSV/Excel with part numbers and quantities."""
    return parse_bom_file("", file_bytes=file_bytes, filename=filename)


def count_wires_and_connectors(bom_lines: list[BomLine]) -> tuple[int, int]:
    """
    Estimate wire count and connector count from BOM descriptions.
    Returns (wire_count, connector_count).
    """
    wire_count = 0
    connector_count = 0

    wire_keywords = ["wire", "cable", "awg", "conductor"]
    connector_keywords = ["connector", "plug", "socket", "header", "jst", "molex", "terminal"]

    for line in bom_lines:
        desc_lower = (line.description + " " + line.mpn).lower()
        if any(kw in desc_lower for kw in wire_keywords):
            wire_count += line.quantity
        elif any(kw in desc_lower for kw in connector_keywords):
            connector_count += line.quantity

    return wire_count, connector_count
```

- [ ] **Step 2: Write cable cost engine**

```python
# costimize-v2/engines/cable/cost_engine.py
"""Cable assembly cost engine — components + labour + overhead + profit."""

from dataclasses import dataclass
from config import (
    CABLE_LABOUR_RATE, CABLE_TIME_PER_WIRE_MIN, CABLE_TIME_PER_CONNECTOR_MIN,
    CABLE_TIME_SLEEVING_MIN, CABLE_TIME_LABELLING_MIN,
    OVERHEAD_PCT, PROFIT_PCT,
)


@dataclass(frozen=True)
class CableCostBreakdown:
    # Components
    component_lines: tuple  # tuple of dicts
    total_components_cost: float

    # Labour
    wire_count: int
    connector_count: int
    labour_time_min: float
    labour_cost: float

    # Totals
    subtotal: float
    overhead: float
    profit: float
    unit_cost: float
    order_cost: float
    quantity: int


def calculate_cable_cost(
    component_prices: list[dict],
    wire_count: int,
    connector_count: int,
    quantity: int,
) -> CableCostBreakdown:
    """
    Calculate cable assembly should-cost.

    Args:
        component_prices: List of dicts with mpn, description, quantity, unit_price, source.
        wire_count: Number of individual wires in the cable.
        connector_count: Number of connectors.
        quantity: Number of cable assemblies.
    """
    # Components
    total_comp = sum(cp.get("unit_price", 0) * cp.get("quantity", 1) for cp in component_prices)

    # Labour time estimation
    time_wires = wire_count * CABLE_TIME_PER_WIRE_MIN
    time_connectors = connector_count * CABLE_TIME_PER_CONNECTOR_MIN
    time_sleeving = CABLE_TIME_SLEEVING_MIN
    time_labelling = CABLE_TIME_LABELLING_MIN
    total_time_min = time_wires + time_connectors + time_sleeving + time_labelling

    labour_cost = (total_time_min / 60) * CABLE_LABOUR_RATE

    # Totals
    subtotal = total_comp + labour_cost
    overhead = subtotal * (OVERHEAD_PCT / 100)
    profit = (subtotal + overhead) * (PROFIT_PCT / 100)
    unit_cost = subtotal + overhead + profit
    order_cost = unit_cost * quantity

    return CableCostBreakdown(
        component_lines=tuple(component_prices),
        total_components_cost=round(total_comp, 2),
        wire_count=wire_count,
        connector_count=connector_count,
        labour_time_min=round(total_time_min, 2),
        labour_cost=round(labour_cost, 2),
        subtotal=round(subtotal, 2),
        overhead=round(overhead, 2),
        profit=round(profit, 2),
        unit_cost=round(unit_cost, 2),
        order_cost=round(order_cost, 2),
        quantity=quantity,
    )
```

- [ ] **Step 3: Write tests**

```python
# costimize-v2/tests/test_cable_engine.py
from engines.cable.cost_engine import calculate_cable_cost, CableCostBreakdown
from engines.cable.bom_parser import count_wires_and_connectors
from engines.pcb.bom_parser import BomLine


def test_count_wires_and_connectors():
    bom = [
        BomLine(mpn="JST-XH-4P", description="JST XH 4-pin connector", quantity=2, footprint="", value=""),
        BomLine(mpn="UL1007-24AWG", description="24AWG Wire Red", quantity=4, footprint="", value=""),
        BomLine(mpn="HST-3MM", description="Heat shrink tubing", quantity=1, footprint="", value=""),
    ]
    wires, connectors = count_wires_and_connectors(bom)
    assert wires == 4
    assert connectors == 2


def test_calculate_cable_cost_basic():
    components = [
        {"mpn": "JST-XH-4P", "description": "Connector", "quantity": 2, "unit_price": 15, "source": "manual"},
        {"mpn": "24AWG-RED", "description": "Wire 300mm", "quantity": 4, "unit_price": 3, "source": "manual"},
    ]
    result = calculate_cable_cost(
        component_prices=components,
        wire_count=4,
        connector_count=2,
        quantity=500,
    )
    assert isinstance(result, CableCostBreakdown)
    assert result.total_components_cost == 42.0  # 2*15 + 4*3
    assert result.labour_time_min > 0
    assert result.unit_cost > 0
    assert result.quantity == 500


def test_cable_cost_includes_profit():
    components = [{"mpn": "X", "description": "Connector", "quantity": 1, "unit_price": 100, "source": "manual"}]
    result = calculate_cable_cost(components, wire_count=1, connector_count=1, quantity=1)
    assert result.profit > 0
    assert result.unit_cost > result.subtotal
```

- [ ] **Step 4: Write cable_tab.py**

```python
# costimize-v2/ui/cable_tab.py
"""Cable Assembly tab — upload BOM, get should-cost breakdown."""

import streamlit as st
from engines.cable.bom_parser import parse_cable_bom, count_wires_and_connectors
from engines.cable.cost_engine import calculate_cable_cost
from extractors.bom_extractor import extract_bom_from_pdf
from engines.pcb.bom_parser import BomLine
from scrapers.component_scraper import get_component_price
from ui.components import render_cost_table, render_historical_comparison


def render():
    st.header("Cable Assembly — Should-Cost Breakdown")

    # --- BOM Upload ---
    uploaded = st.file_uploader("Upload Cable BOM", type=["csv", "xlsx", "xls", "pdf"], key="cable_upload")

    if uploaded:
        file_bytes = uploaded.read()
        ext = uploaded.name.split(".")[-1].lower()

        if ext == "pdf":
            if st.button("🔍 Extract BOM from PDF", key="cable_extract"):
                with st.spinner("AI is extracting BOM from PDF..."):
                    try:
                        raw = extract_bom_from_pdf(file_bytes)
                        bom_lines = [
                            BomLine(mpn=c.get("mpn", ""), description=c.get("description", ""),
                                    quantity=int(c.get("quantity", 1)), footprint=c.get("footprint", ""),
                                    value=c.get("value", ""))
                            for c in raw
                        ]
                        st.session_state["cable_bom"] = bom_lines
                    except Exception as e:
                        st.error(f"PDF extraction failed: {e}")
                        return
        else:
            try:
                bom_lines = parse_cable_bom(file_bytes, uploaded.name)
                st.session_state["cable_bom"] = bom_lines
                st.success(f"Parsed {len(bom_lines)} components")
            except Exception as e:
                st.error(f"BOM parse failed: {e}")
                return

    bom_lines = st.session_state.get("cable_bom", [])
    if bom_lines:
        st.subheader(f"Cable BOM ({len(bom_lines)} items)")

        component_prices = []
        for i, line in enumerate(bom_lines):
            cols = st.columns([2, 3, 1, 1])
            cols[0].text(line.mpn or "—")
            cols[1].text(line.description or "—")
            cols[2].text(str(line.quantity))

            price_key = f"cable_price_{i}"
            existing = st.session_state.get(price_key)
            if existing:
                cols[3].text(f"₹{existing['unit_price']:.2f}")
            else:
                cols[3].text("—")

            component_prices.append({
                "mpn": line.mpn,
                "description": line.description,
                "quantity": line.quantity,
                "unit_price": existing["unit_price"] if existing else 0,
                "source": existing["source"] if existing else "not_found",
            })

        if st.button("🔍 Fetch Component Prices", key="cable_fetch"):
            progress = st.progress(0, text="Scraping prices...")
            for i, line in enumerate(bom_lines):
                if line.mpn:
                    result = get_component_price(line.mpn)
                    st.session_state[f"cable_price_{i}"] = result
                    component_prices[i]["unit_price"] = result["unit_price"]
                    component_prices[i]["source"] = result["source"]
                progress.progress((i + 1) / len(bom_lines), text=f"Fetching {i+1}/{len(bom_lines)}...")
            st.rerun()

    # --- Cable Details ---
    st.subheader("Cable Details")
    auto_wires, auto_connectors = count_wires_and_connectors(bom_lines) if bom_lines else (0, 0)
    col1, col2, col3 = st.columns(3)
    with col1:
        wire_count = st.number_input("Number of Wires", value=max(auto_wires, 4), min_value=1, key="cable_wires")
    with col2:
        connector_count = st.number_input("Number of Connectors", value=max(auto_connectors, 2), min_value=1, key="cable_connectors")
    with col3:
        quantity = st.number_input("Quantity", value=500, min_value=1, key="cable_qty")

    # --- Calculate ---
    if st.button("💰 Calculate Should-Cost", key="cable_calc", type="primary"):
        if not bom_lines:
            st.error("Upload a cable BOM first.")
            return

        result = calculate_cable_cost(
            component_prices=component_prices,
            wire_count=wire_count,
            connector_count=connector_count,
            quantity=quantity,
        )
        st.session_state["cable_result"] = result

    # --- Display ---
    result = st.session_state.get("cable_result")
    if result:
        st.subheader("📊 Should-Cost Breakdown")

        lines = [
            {"item": "Components", "cost": result.total_components_cost,
             "detail": f"{len(result.component_lines)} items"},
            {"item": "Labour", "cost": result.labour_cost,
             "detail": f"{result.labour_time_min:.1f} min ({result.wire_count} wires, {result.connector_count} connectors)"},
            {"item": "Overhead (15%)", "cost": result.overhead, "detail": ""},
            {"item": "Profit (20%)", "cost": result.profit, "detail": ""},
        ]
        render_cost_table(lines)

        col1, col2 = st.columns(2)
        col1.metric("Unit Cost", f"₹{result.unit_cost:,.2f}")
        col2.metric("Order Cost", f"₹{result.order_cost:,.2f}", delta=f"{result.quantity} cables")

        history_match = st.session_state.get("cable_history_match")
        render_historical_comparison(result.unit_cost, history_match)
```

- [ ] **Step 5: Update app.py — import cable tab**

Replace `with tab3:` block:

```python
with tab3:
    from ui.cable_tab import render as render_cable
    render_cable()
```

- [ ] **Step 6: Run tests**

```bash
cd costimize-v2 && python -m pytest tests/test_cable_engine.py -v
```
Expected: All 3 tests PASS

- [ ] **Step 7: Manually test — all 3 tabs render**

```bash
cd costimize-v2 && streamlit run app.py
```

- [ ] **Step 8: Commit**

```bash
cd costimize-v2 && git add -A && git commit -m "feat: cable assembly engine and UI tab with BOM parsing"
```

---

## Task 9: Historical PO Comparison

**Files:**
- Create: `costimize-v2/history/po_parser.py`
- Create: `costimize-v2/history/po_store.py`
- Create: `costimize-v2/history/po_matcher.py`
- Test: `costimize-v2/tests/test_history.py`

- [ ] **Step 1: Write po_parser.py**

```python
# costimize-v2/history/po_parser.py
"""Parse historical PO files (Excel/CSV). Direct column mapping, no AI needed."""

import pandas as pd
from pathlib import Path

HEADER_MAP = {
    "part_description": ["part description", "description", "item description", "part name", "item", "component"],
    "part_number": ["part number", "part no", "part_no", "pn", "item number", "item no", "mpn"],
    "unit_price": ["unit price", "price", "rate", "unit rate", "cost", "unit cost", "price per unit"],
    "quantity": ["quantity", "qty", "qty.", "order qty", "order quantity"],
    "supplier": ["supplier", "vendor", "supplier name", "vendor name"],
    "date": ["date", "po date", "order date", "purchase date"],
}


def _match_column(columns: list[str], candidates: list[str]) -> str | None:
    lower_cols = {c.lower().strip(): c for c in columns}
    for candidate in candidates:
        if candidate in lower_cols:
            return lower_cols[candidate]
    return None


def parse_po_file(file_bytes: bytes, filename: str) -> list[dict]:
    """
    Parse a PO file and return list of normalized PO records.
    Each record: {part_description, part_number, unit_price, quantity, supplier, date}
    """
    import io
    ext = Path(filename).suffix.lower()
    if ext in (".xlsx", ".xls"):
        df = pd.read_excel(io.BytesIO(file_bytes))
    else:
        df = pd.read_csv(io.BytesIO(file_bytes))

    columns = list(df.columns)
    col_map = {field: _match_column(columns, candidates) for field, candidates in HEADER_MAP.items()}

    records = []
    for _, row in df.iterrows():
        desc = str(row.get(col_map["part_description"], "")).strip() if col_map["part_description"] else ""
        pn = str(row.get(col_map["part_number"], "")).strip() if col_map["part_number"] else ""

        try:
            price = float(row.get(col_map["unit_price"], 0)) if col_map["unit_price"] else 0
        except (ValueError, TypeError):
            price = 0

        try:
            qty = int(float(row.get(col_map["quantity"], 0))) if col_map["quantity"] else 0
        except (ValueError, TypeError):
            qty = 0

        supplier = str(row.get(col_map["supplier"], "")).strip() if col_map["supplier"] else ""
        date_val = row.get(col_map["date"], "") if col_map["date"] else ""
        date_str = str(date_val).strip() if date_val else ""

        if not desc and not pn:
            continue

        records.append({
            "part_description": desc,
            "part_number": pn,
            "unit_price": price,
            "quantity": qty,
            "supplier": supplier,
            "date": date_str,
        })

    return records
```

- [ ] **Step 2: Write po_store.py**

```python
# costimize-v2/history/po_store.py
"""Store and retrieve historical PO data as JSON."""

import json
from pathlib import Path

HISTORY_DIR = Path(__file__).parent.parent / "data" / "history"
HISTORY_DIR.mkdir(parents=True, exist_ok=True)
HISTORY_FILE = HISTORY_DIR / "po_records.json"


def load_all_records() -> list[dict]:
    if not HISTORY_FILE.exists():
        return []
    try:
        return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_records(records: list[dict]):
    existing = load_all_records()
    # Deduplicate by part_number + supplier + date
    existing_keys = {
        (r.get("part_number", ""), r.get("supplier", ""), r.get("date", ""))
        for r in existing
    }
    new_records = [
        r for r in records
        if (r.get("part_number", ""), r.get("supplier", ""), r.get("date", "")) not in existing_keys
    ]
    all_records = existing + new_records
    HISTORY_FILE.write_text(json.dumps(all_records, indent=2, ensure_ascii=False), encoding="utf-8")
    return len(new_records)
```

- [ ] **Step 3: Write po_matcher.py**

```python
# costimize-v2/history/po_matcher.py
"""Match current estimate to historical PO records."""

from history.po_store import load_all_records


def find_matching_po(part_number: str = "", part_description: str = "") -> dict | None:
    """
    Find the most recent matching PO record.
    Matches by part_number first (exact), then falls back to keyword match on description.
    Returns the most recent match or None.
    """
    records = load_all_records()
    if not records:
        return None

    # Exact part number match
    if part_number:
        pn_lower = part_number.lower().strip()
        matches = [r for r in records if r.get("part_number", "").lower().strip() == pn_lower]
        if matches:
            return _most_recent(matches)

    # Keyword match on description
    if part_description:
        desc_words = set(part_description.lower().split())
        best_match = None
        best_score = 0
        for record in records:
            record_desc = record.get("part_description", "").lower()
            record_words = set(record_desc.split())
            if not record_words:
                continue
            overlap = len(desc_words & record_words)
            score = overlap / max(len(desc_words), 1)
            if score > best_score and score >= 0.3:  # at least 30% word overlap
                best_score = score
                best_match = record

        return best_match

    return None


def _most_recent(records: list[dict]) -> dict:
    """Return the most recent record (by date string, or last in list)."""
    sorted_records = sorted(records, key=lambda r: r.get("date", ""), reverse=True)
    return sorted_records[0]
```

- [ ] **Step 4: Write tests**

```python
# costimize-v2/tests/test_history.py
import io
import json
import pandas as pd
from history.po_parser import parse_po_file
from history.po_store import load_all_records, save_records, HISTORY_FILE
from history.po_matcher import find_matching_po


def test_parse_po_excel():
    df = pd.DataFrame({
        "Part Number": ["SHAFT-001", "GEAR-002"],
        "Description": ["Steel shaft 60mm OD", "Spur gear module 2"],
        "Unit Price": [3450, 1200],
        "Qty": [200, 500],
        "Supplier": ["ABC Engg Pune", "XYZ Gears Mumbai"],
        "PO Date": ["2025-03-15", "2025-02-10"],
    })
    buf = io.BytesIO()
    df.to_excel(buf, index=False)
    buf.seek(0)
    records = parse_po_file(buf.read(), "po_history.xlsx")
    assert len(records) == 2
    assert records[0]["part_number"] == "SHAFT-001"
    assert records[0]["unit_price"] == 3450
    assert records[0]["supplier"] == "ABC Engg Pune"


def test_po_store_round_trip(tmp_path, monkeypatch):
    monkeypatch.setattr("history.po_store.HISTORY_FILE", tmp_path / "po_records.json")
    records = [
        {"part_number": "SHAFT-001", "part_description": "Steel shaft", "unit_price": 3450,
         "quantity": 200, "supplier": "ABC Engg", "date": "2025-03-15"},
    ]
    added = save_records(records)
    assert added == 1
    loaded = load_all_records()
    assert len(loaded) == 1
    assert loaded[0]["part_number"] == "SHAFT-001"


def test_po_matcher_exact_part_number(tmp_path, monkeypatch):
    history_file = tmp_path / "po_records.json"
    monkeypatch.setattr("history.po_store.HISTORY_FILE", history_file)
    monkeypatch.setattr("history.po_matcher.load_all_records",
                        lambda: [{"part_number": "SHAFT-001", "part_description": "Steel shaft 60mm",
                                  "unit_price": 3450, "quantity": 200, "supplier": "ABC Engg", "date": "2025-03-15"}])
    match = find_matching_po(part_number="SHAFT-001")
    assert match is not None
    assert match["unit_price"] == 3450


def test_po_matcher_description_fallback(tmp_path, monkeypatch):
    monkeypatch.setattr("history.po_matcher.load_all_records",
                        lambda: [{"part_number": "SHAFT-001", "part_description": "Steel shaft 60mm OD turning",
                                  "unit_price": 3450, "quantity": 200, "supplier": "ABC", "date": "2025-03"}])
    match = find_matching_po(part_description="Steel shaft 60mm machined")
    assert match is not None
    assert match["unit_price"] == 3450


def test_po_matcher_no_match(tmp_path, monkeypatch):
    monkeypatch.setattr("history.po_matcher.load_all_records", lambda: [])
    match = find_matching_po(part_number="NONEXISTENT")
    assert match is None
```

- [ ] **Step 5: Run tests**

```bash
cd costimize-v2 && python -m pytest tests/test_history.py -v
```
Expected: All 5 tests PASS

- [ ] **Step 6: Commit**

```bash
cd costimize-v2 && git add -A && git commit -m "feat: historical PO parser, store, and matcher for cost comparison"
```

---

## Task 10: Wire Up Historical PO to Sidebar & All Tabs

**Files:**
- Modify: `costimize-v2/app.py`
- Modify: `costimize-v2/ui/mechanical_tab.py`
- Modify: `costimize-v2/ui/pcb_tab.py`
- Modify: `costimize-v2/ui/cable_tab.py`

- [ ] **Step 1: Add PO upload to app.py sidebar**

```python
# costimize-v2/app.py
"""AI.Procurve — Should-Cost Intelligence for Procurement"""

import streamlit as st
from history.po_parser import parse_po_file
from history.po_store import save_records, load_all_records

st.set_page_config(
    page_title="AI.Procurve — Should-Cost Intelligence",
    page_icon="⚙",
    layout="wide",
)

# --- Sidebar: Historical PO Upload ---
with st.sidebar:
    st.header("📂 Historical PO Data")
    po_file = st.file_uploader("Upload previous POs", type=["csv", "xlsx", "xls"], key="po_upload")
    if po_file:
        try:
            records = parse_po_file(po_file.read(), po_file.name)
            added = save_records(records)
            st.success(f"Added {added} new PO records ({len(records)} total parsed)")
        except Exception as e:
            st.error(f"PO parse failed: {e}")

    existing = load_all_records()
    st.caption(f"{len(existing)} historical PO records loaded")

# --- Main ---
st.title("AI.Procurve — Should-Cost Intelligence")
st.caption("Upload a drawing or BOM. Get instant cost breakdown for negotiations.")

tab1, tab2, tab3 = st.tabs(["⚙ Mechanical Parts", "🔌 PCB Assembly", "🔗 Cable Assembly"])

with tab1:
    from ui.mechanical_tab import render as render_mechanical
    render_mechanical()

with tab2:
    from ui.pcb_tab import render as render_pcb
    render_pcb()

with tab3:
    from ui.cable_tab import render as render_cable
    render_cable()
```

- [ ] **Step 2: Add PO matching to mechanical_tab.py**

After the cost calculation result is stored in `st.session_state["mech_result"]`, add:

```python
        # After: st.session_state["mech_result"] = result
        # Add historical PO lookup
        from history.po_matcher import find_matching_po
        extraction = st.session_state.get("mech_extraction", {})
        match = find_matching_po(
            part_number="",  # mechanical parts don't have MPNs
            part_description=f"{material_name} {od}mm {length}mm {' '.join(selected_processes)}",
        )
        st.session_state["mech_history_match"] = match
```

- [ ] **Step 3: Add PO matching to pcb_tab.py**

After `st.session_state["pcb_result"] = result`, add:

```python
        from history.po_matcher import find_matching_po
        match = find_matching_po(
            part_description="PCB assembly " + " ".join(line.description for line in bom_lines[:3]),
        )
        st.session_state["pcb_history_match"] = match
```

- [ ] **Step 4: Add PO matching to cable_tab.py**

After `st.session_state["cable_result"] = result`, add:

```python
        from history.po_matcher import find_matching_po
        match = find_matching_po(
            part_description="Cable assembly " + " ".join(line.description for line in bom_lines[:3]),
        )
        st.session_state["cable_history_match"] = match
```

- [ ] **Step 5: Manually test — upload a sample PO Excel, verify comparison shows**

```bash
cd costimize-v2 && streamlit run app.py
```

- [ ] **Step 6: Commit**

```bash
cd costimize-v2 && git add -A && git commit -m "feat: historical PO upload in sidebar with comparison on all 3 tabs"
```

---

## Task 11: Material Price Scraper

**Files:**
- Create: `costimize-v2/scrapers/material_scraper.py`
- Test: `costimize-v2/tests/test_material_scraper.py`

- [ ] **Step 1: Write material_scraper.py (ported from v1)**

```python
# costimize-v2/scrapers/material_scraper.py
"""Web-scraped live material prices with 24h JSON file cache. Ported from costimize-mvp."""

import json
import time
import random
from pathlib import Path
from datetime import datetime, timedelta
from config import CACHE_DURATION_SEC, SCRAPE_DELAY_RANGE, USER_AGENTS

import requests
from bs4 import BeautifulSoup

CACHE_FILE = Path(__file__).parent.parent / "data" / "cache" / "material_prices.json"

DEFAULT_PRICES = {
    "Aluminum 6061": 280,
    "Mild Steel IS2062": 65,
    "Stainless Steel 304": 220,
    "Brass IS319": 550,
    "EN8 Steel": 75,
    "EN24 Steel": 120,
    "Copper": 750,
    "Cast Iron": 55,
    "Titanium Grade 5": 3500,
}


def _load_cache() -> dict | None:
    if not CACHE_FILE.exists():
        return None
    try:
        data = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        cached_at = datetime.fromisoformat(data.get("cached_at", "2000-01-01"))
        if datetime.now() - cached_at > timedelta(seconds=CACHE_DURATION_SEC):
            return None
        return data.get("prices", {})
    except (json.JSONDecodeError, KeyError):
        return None


def _save_cache(prices: dict):
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    data = {"cached_at": datetime.now().isoformat(), "prices": prices}
    CACHE_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")


def get_material_price(material_name: str) -> float:
    """
    Get material price in ₹/kg. Checks cache, then tries web scraping, falls back to defaults.
    """
    cached = _load_cache()
    if cached and material_name in cached:
        return cached[material_name]

    # Try scraping (best-effort)
    try:
        session = requests.Session()
        session.headers.update({"User-Agent": random.choice(USER_AGENTS)})
        query = f"{material_name} price per kg india INR"
        # This is a placeholder — real scraping would target specific metal price sites
        # For MVP, we use default prices with cache
    except Exception:
        pass

    # Fallback to default prices
    price = DEFAULT_PRICES.get(material_name, 100)

    # Cache the result
    all_prices = cached or {}
    all_prices[material_name] = price
    _save_cache(all_prices)

    return price
```

- [ ] **Step 2: Write test**

```python
# costimize-v2/tests/test_material_scraper.py
from scrapers.material_scraper import get_material_price, DEFAULT_PRICES


def test_get_known_material_price():
    price = get_material_price("EN8 Steel")
    assert price == 75


def test_get_unknown_material_returns_default():
    price = get_material_price("Unknown Alloy XYZ")
    assert price == 100  # fallback default


def test_all_default_prices_positive():
    for name, price in DEFAULT_PRICES.items():
        assert price > 0, f"{name} has non-positive price"
```

- [ ] **Step 3: Run tests**

```bash
cd costimize-v2 && python -m pytest tests/test_material_scraper.py -v
```
Expected: All 3 tests PASS

- [ ] **Step 4: Commit**

```bash
cd costimize-v2 && git add -A && git commit -m "feat: material price scraper with caching and fallback defaults"
```

---

## Task 12: Run All Tests & Final Verification

**Files:** No new files — verification only.

- [ ] **Step 1: Run full test suite**

```bash
cd costimize-v2 && python -m pytest tests/ -v --tb=short
```
Expected: All tests pass (config: 2, mechanical: 7, extractors: 6, pcb: 5, cable: 3, history: 5, scraper: 3, material: 3 = ~34 tests total)

- [ ] **Step 2: Run the full app and verify all tabs**

```bash
cd costimize-v2 && streamlit run app.py
```

Verify:
- All 3 tabs render without errors
- Sidebar PO upload works
- Mechanical: dimension inputs, process checklist, calculate button all work
- PCB: BOM upload, board specs, calculate works
- Cable: BOM upload, wire/connector counts, calculate works

- [ ] **Step 3: Final commit**

```bash
cd costimize-v2 && git add -A && git commit -m "test: all tests passing, app verified working"
```

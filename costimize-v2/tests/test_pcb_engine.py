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

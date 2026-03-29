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

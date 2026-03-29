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
    component_lines: tuple
    total_components_cost: float
    wire_count: int
    connector_count: int
    labour_time_min: float
    labour_cost: float
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
    total_comp = sum(cp.get("unit_price", 0) * cp.get("quantity", 1) for cp in component_prices)

    time_wires = wire_count * CABLE_TIME_PER_WIRE_MIN
    time_connectors = connector_count * CABLE_TIME_PER_CONNECTOR_MIN
    time_sleeving = CABLE_TIME_SLEEVING_MIN
    time_labelling = CABLE_TIME_LABELLING_MIN
    total_time_min = time_wires + time_connectors + time_sleeving + time_labelling

    labour_cost = (total_time_min / 60) * CABLE_LABOUR_RATE

    subtotal = total_comp + labour_cost
    overhead = subtotal * (OVERHEAD_PCT / 100)
    profit = (subtotal + overhead) * (PROFIT_PCT / 100)
    unit_cost = subtotal + overhead + profit
    order_cost = round(round(unit_cost, 2) * quantity, 2)

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
        order_cost=order_cost,
        quantity=quantity,
    )

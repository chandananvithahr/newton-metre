# costimize-v2/tests/test_config.py
import sys
import os

# Ensure the project root is on the path so `config` can be imported directly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

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

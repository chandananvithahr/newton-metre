# costimize-v2/tests/test_component_scraper.py
import json
from pathlib import Path
from scrapers.component_scraper import _cache_key, _load_cache, _save_cache, get_component_price, CACHE_DIR


def test_cache_key_is_deterministic():
    assert _cache_key("STM32F103C8T6") == _cache_key("STM32F103C8T6")
    assert _cache_key("STM32F103C8T6") != _cache_key("LM1117-3.3")


def test_cache_round_trip(tmp_path, monkeypatch):
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

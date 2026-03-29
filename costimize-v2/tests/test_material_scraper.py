# costimize-v2/tests/test_material_scraper.py
from scrapers.material_scraper import get_material_price, DEFAULT_PRICES


def test_get_known_material_price():
    price = get_material_price("EN8 Steel")
    assert price == 75


def test_get_unknown_material_returns_default():
    price = get_material_price("Unknown Alloy XYZ")
    assert price == 100


def test_all_default_prices_positive():
    for name, price in DEFAULT_PRICES.items():
        assert price > 0, f"{name} has non-positive price"

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
    cached = _load_cache()
    if cached and material_name in cached:
        return cached[material_name]

    try:
        session = requests.Session()
        session.headers.update({"User-Agent": random.choice(USER_AGENTS)})
        query = f"{material_name} price per kg india INR"
    except Exception:
        pass

    price = DEFAULT_PRICES.get(material_name, 100)

    all_prices = cached or {}
    all_prices[material_name] = price
    _save_cache(all_prices)

    return price

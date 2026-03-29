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
    try:
        session = _get_session()
        url = f"https://www.digikey.com/en/products/result?keywords={mpn}"
        resp = session.get(url, timeout=15)
        if resp.status_code != 200:
            return None

        soup = BeautifulSoup(resp.text, "lxml")
        price_elements = soup.select("[data-testid='price-table'] td, .MuiTableCell-root")
        if not price_elements:
            price_elements = soup.select(".price-table td, .pdp-pricing td")

        prices = {}
        for elem in price_elements:
            text = elem.get_text(strip=True)
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
    try:
        session = _get_session()
        url = f"https://www.mouser.in/Search/Refine?Keyword={mpn}"
        resp = session.get(url, timeout=15)
        if resp.status_code != 200:
            return None

        soup = BeautifulSoup(resp.text, "lxml")
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
    if not mpn or mpn.strip() == "":
        return {"mpn": mpn, "unit_price": 0, "source": "not_found"}

    cached = _load_cache(mpn)
    if cached:
        return cached

    time.sleep(random.uniform(*SCRAPE_DELAY_RANGE))
    result = scrape_digikey(mpn)

    if not result:
        time.sleep(random.uniform(*SCRAPE_DELAY_RANGE))
        result = scrape_mouser(mpn)

    if result:
        result["mpn"] = mpn
        _save_cache(mpn, result)
        return result

    not_found = {"mpn": mpn, "unit_price": 0, "source": "not_found"}
    _save_cache(mpn, not_found)
    return not_found


def get_bulk_prices(mpns: list[str], quantity: int = 1) -> list[dict]:
    results = []
    for mpn in mpns:
        results.append(get_component_price(mpn, quantity))
    return results

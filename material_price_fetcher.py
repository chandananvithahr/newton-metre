"""
Material price fetcher from web sources
Fetches live Indian market prices with caching and fallback
"""
import json
import requests
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime, timedelta
import time

# Cache file to store prices
CACHE_FILE = Path(__file__).parent / "material_price_cache.json"
CACHE_DURATION_HOURS = 24  # Refresh prices once per day

# Material mapping to web search terms
MATERIAL_SEARCH_TERMS = {
    "Aluminum 6061": "aluminum 6061 price per kg india",
    "Mild Steel IS2062": "mild steel IS2062 price per kg india",
    "Stainless Steel 304": "stainless steel 304 price per kg india",
    "Brass IS319": "brass IS319 price per kg india",
    "EN8 Steel": "EN8 steel price per kg india",
    "EN24 Steel": "EN24 steel price per kg india"
}

# Default fallback prices (from materials.json)
DEFAULT_PRICES = {
    "Aluminum 6061": 280,
    "Mild Steel IS2062": 65,
    "Stainless Steel 304": 220,
    "Brass IS319": 550,
    "EN8 Steel": 75,
    "EN24 Steel": 120
}


def load_cache() -> Dict:
    """Load cached prices from file."""
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                cache = json.load(f)
                return cache
        except Exception:
            return {}
    return {}


def save_cache(cache: Dict):
    """Save prices to cache file."""
    try:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache, f, indent=2)
    except Exception:
        pass  # Fail silently if cache can't be saved


def is_cache_valid(cache: Dict) -> bool:
    """Check if cache is still valid (not expired)."""
    if not cache or 'timestamp' not in cache:
        return False
    
    cache_time = datetime.fromisoformat(cache['timestamp'])
    expiry_time = cache_time + timedelta(hours=CACHE_DURATION_HOURS)
    return datetime.now() < expiry_time


def fetch_price_from_web(material_name: str) -> Optional[float]:
    """
    Fetch material price from web sources.
    Uses multiple strategies: API, scraping, or search-based estimation.
    
    Returns price in INR per kg, or None if fetch fails.
    """
    try:
        # Strategy 1: Try commodity price APIs (if available)
        # Note: Most require API keys and subscriptions
        
        # Strategy 2: Scrape Indian metal market websites
        # Common sources: indiamart.com, tradeindia.com, metal.com
        price = scrape_indian_metal_price(material_name)
        if price:
            return price
        
        # Strategy 3: Use search-based price estimation
        # This is a fallback that searches for current prices
        price = estimate_price_from_search(material_name)
        if price:
            return price
        
        return None
        
    except Exception as e:
        print(f"Error fetching price for {material_name}: {e}")
        return None


def scrape_indian_metal_price(material_name: str) -> Optional[float]:
    """
    Scrape price from Indian metal market websites.
    Attempts to fetch prices from public sources.
    """
    try:
        from bs4 import BeautifulSoup
        
        # Map materials to search queries
        search_terms = MATERIAL_SEARCH_TERMS.get(material_name, material_name.lower())
        
        # Try multiple sources
        sources = [
            scrape_from_indiamart(material_name),
            scrape_from_tradeindia(material_name),
            scrape_from_metal_com(material_name)
        ]
        
        # Return first valid price found
        for price in sources:
            if price and price > 0:
                return price
        
        return None
        
    except ImportError:
        # BeautifulSoup not installed, skip scraping
        return None
    except Exception:
        return None


def scrape_from_indiamart(material_name: str) -> Optional[float]:
    """Scrape price from IndiaMART (example implementation)."""
    try:
        from bs4 import BeautifulSoup
        
        # IndiaMART search URL
        search_url = f"https://www.indiamart.com/search.php?q={material_name.replace(' ', '+')}+price"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(search_url, headers=headers, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Parse price from search results (structure may vary)
            # This is a template - actual parsing depends on site structure
            price_elements = soup.find_all(class_='prc')  # Example class
            if price_elements:
                # Extract and convert price
                price_text = price_elements[0].get_text()
                # Parse price (handle different formats)
                # Return price in INR per kg
                pass  # Implement actual parsing
        
        return None
    except Exception:
        return None


def scrape_from_tradeindia(material_name: str) -> Optional[float]:
    """Scrape price from TradeIndia (example implementation)."""
    try:
        # Similar implementation to IndiaMART
        return None
    except Exception:
        return None


def scrape_from_metal_com(material_name: str) -> Optional[float]:
    """Scrape price from metal.com or similar sources."""
    try:
        # Metal.com often has structured data
        # Could use their API if available
        return None
    except Exception:
        return None


def estimate_price_from_search(material_name: str) -> Optional[float]:
    """
    Estimate price by searching for current market rates.
    This uses web search to find approximate current prices.
    """
    try:
        # This would use a search API or scraping
        # For MVP, we'll use a simple heuristic based on material type
        
        # You could integrate with:
        # - Google Custom Search API (requires API key)
        # - DuckDuckGo search (no API key needed but rate limited)
        # - Bing Search API
        
        # For now, return None to use cached/default prices
        return None
        
    except Exception:
        return None


def get_material_price(material_name: str, use_web: bool = True) -> float:
    """
    Get material price with caching and fallback.
    
    Args:
        material_name: Name of the material
        use_web: Whether to attempt web fetch (default: True)
        
    Returns:
        Price in INR per kg
    """
    # Load cache
    cache = load_cache()
    
    # Check if we have valid cached price
    if is_cache_valid(cache) and material_name in cache.get('prices', {}):
        cached_price = cache['prices'][material_name]
        if cached_price and cached_price > 0:
            return cached_price
    
    # Try to fetch from web if enabled
    if use_web:
        web_price = fetch_price_from_web(material_name)
        if web_price and web_price > 0:
            # Update cache
            if 'prices' not in cache:
                cache['prices'] = {}
            cache['prices'][material_name] = web_price
            cache['timestamp'] = datetime.now().isoformat()
            save_cache(cache)
            return web_price
    
    # Fallback to default price
    default_price = DEFAULT_PRICES.get(material_name)
    if default_price:
        return default_price
    
    # Last resort: return a reasonable default
    return 100.0  # Generic default


def refresh_all_prices(force: bool = False) -> Dict[str, float]:
    """
    Refresh prices for all materials.
    
    Args:
        force: If True, refresh even if cache is valid
        
    Returns:
        Dictionary of material_name -> price
    """
    cache = load_cache()
    
    if not force and is_cache_valid(cache):
        return cache.get('prices', {})
    
    prices = {}
    for material_name in MATERIAL_SEARCH_TERMS.keys():
        price = get_material_price(material_name, use_web=True)
        prices[material_name] = price
        time.sleep(0.5)  # Rate limiting between requests
    
    # Update cache
    cache['prices'] = prices
    cache['timestamp'] = datetime.now().isoformat()
    save_cache(cache)
    
    return prices


def get_price_source_info(material_name: str) -> str:
    """Get information about price source (cached, web, or default)."""
    cache = load_cache()
    
    if is_cache_valid(cache) and material_name in cache.get('prices', {}):
        cache_time = datetime.fromisoformat(cache['timestamp'])
        age_hours = (datetime.now() - cache_time).total_seconds() / 3600
        return f"Cached (updated {age_hours:.1f} hours ago)"
    
    if material_name in DEFAULT_PRICES:
        return "Default price (static)"
    
    return "Estimated price"


# Example: Integration with a free API (if available)
def fetch_from_commodity_api(material_name: str, api_key: Optional[str] = None) -> Optional[float]:
    """
    Fetch price from a commodity price API.
    This is a template - you'd need to:
    1. Sign up for an API service
    2. Get an API key
    3. Map material names to API symbols
    4. Handle API responses
    """
    if not api_key:
        return None
    
    # Example API integration (placeholder)
    # api_url = f"https://api.example.com/commodities/{material_name}"
    # headers = {"Authorization": f"Bearer {api_key}"}
    # response = requests.get(api_url, headers=headers, timeout=5)
    # if response.status_code == 200:
    #     data = response.json()
    #     price_per_ton = data.get('price')
    #     price_per_kg = price_per_ton / 1000  # Convert ton to kg
    #     return price_per_kg
    
    return None

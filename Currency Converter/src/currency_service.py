import requests
from cachetools import cached, TTLCache

# Cache for exchange rates (2 hours TTL, max 100 entries)
cache = TTLCache(maxsize=100, ttl=2*60*60)


@cached(cache)
def get_exchange_rate(base_currency: str, target_currency: str) -> float:
    """Fetch exchange rate from API (cached for 2 hours)."""
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()['rates'][target_currency]

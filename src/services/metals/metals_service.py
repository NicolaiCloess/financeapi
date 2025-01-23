import os
import requests
from src.config.config import METALS_API_KEY

def get_metals_prices():
    if not METALS_API_KEY:
        return {"error": "No API key provided"}

    symbols = "XAU,XAG,XPT,XPD,XCU,ALU,NI,ZNC,LEAD,TIN"
    url = f"https://metals-api.com/api/latest?access_key={METALS_API_KEY}&base=USD&symbols={symbols}"
    response = requests.get(url)
    data = response.json()

    # Erwartete Antwort:
    # {
    #   "success": true,
    #   "timestamp": 1634716399,
    #   "base": "USD",
    #   "date": "2021-10-20",
    #   "rates": {
    #       "XAU": 1785.23,
    #       "XAG": 24.38,
    #       "XPT": ...,
    #       "XPD": ...,
    #       ...
    #   }
    # }

    if data.get("success"):
        rates = data.get("rates", {})
        return {
            "gold_price_usd": rates.get("XAU"),
            "silver_price_usd": rates.get("XAG"),
            "platinum_price_usd": rates.get("XPT"),
            "palladium_price_usd": rates.get("XPD"),
            "copper_price_usd": rates.get("XCU"),
            "aluminum_price_usd": rates.get("ALU"),
            "nickel_price_usd": rates.get("NI"),
            "zinc_price_usd": rates.get("ZNC"),
            "lead_price_usd": rates.get("LEAD"),
            "tin_price_usd": rates.get("TIN")
        }
    else:
        # Fehlerfall
        error_info = data.get("error", {})
        return {
            "error": error_info
        }


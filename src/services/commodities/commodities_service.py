import requests

COMMODITY_SYMBOLS = {
    "Weizen": "ZW=F",
    "Öl": "CL=F",
    "Gas": "NG=F"
}

def get_commodities_prices():
    """
    Ruft die aktuellen Preise für Weizen, Öl und Gas von Yahoo Finance ab.
    Gibt ein Dictionary zurück:
    {
        "Weizen": 123.45,
        "Öl": 67.89,
        "Gas": 4.56
    }
    """
    base_url = "https://query1.finance.yahoo.com/v7/finance/quote"
    symbols_str = ",".join(COMMODITY_SYMBOLS.values())
    url = f"{base_url}?symbols={symbols_str}"
    response = requests.get(url)
    data = response.json()

    results = data.get("quoteResponse", {}).get("result", [])
    prices = {}
    for item in results:
        name = [key for key, value in COMMODITY_SYMBOLS.items() if value == item.get("symbol")][0]
        prices[name] = item.get("regularMarketPrice")
    return prices

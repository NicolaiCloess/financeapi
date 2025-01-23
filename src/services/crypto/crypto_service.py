import requests
from src.config.config import COINGECKO_API_KEY


def get_crypto_prices():
    # IDs der Kryptowährungen, kommasepariert
    crypto_ids = "bitcoin,ethereum,solana,aragon,cardano,ripple,usd-coin,dogecoin,binancecoin,tether"
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_ids}&vs_currencies=usd"

    headers = {
    "accept": "application/json",
    "x-cg-demo-api-key": COINGECKO_API_KEY
}

    # Anfrage senden
    response = requests.get(url, headers=headers)
    # Fehlerprüfung
    if response.status_code != 200:
        return {"error": f"Fehler beim Abrufen der Daten: {response.status_code} - {response.text}"}
    
    # Antwortdaten als JSON
    data = response.json()

    # data könnte z.B. so aussehen:
    # {
    #   "bitcoin": {"usd": 27000},
    #   "ethereum": {"usd": 1800},
    #   "solana": {"usd": 20.5},
    #   ...
    # }

    return {
        "bitcoin_price_usd": data.get("bitcoin", {}).get("usd"),
        "ethereum_price_usd": data.get("ethereum", {}).get("usd"),
        "solana_price_usd": data.get("solana", {}).get("usd"),
        "aragon_price_usd": data.get("aragon", {}).get("usd"),
        "cardano_price_usd": data.get("cardano", {}).get("usd"),
        "ripple_price_usd": data.get("ripple", {}).get("usd"),
        "usdcoin_price_usd": data.get("usd-coin", {}).get("usd"),
        "dogecoin_price_usd": data.get("dogecoin", {}).get("usd"),
        "binancecoin_price_usd": data.get("binancecoin", {}).get("usd"),
        "tether_price_usd": data.get("tether", {}).get("usd")
    }


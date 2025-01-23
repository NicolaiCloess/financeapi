import requests
from src.config.config import ALPHA_VANTAGE_API_KEY

def get_currency_rates(base, symbols):
    """
    Ruft für eine gegebene Basiswährung (`base`) und eine Liste von Zielwährungen (`symbols`)
    die aktuellen Wechselkurse über Alpha Vantage ab.

    :param base: Die Basiswährung (z.B. "USD")
    :param symbols: Liste von Zielwährungen (z.B. ["EUR", "GBP", "JPY"])
    :return: Dict mit {zielwährung: wechselkurs}, z.B. {"EUR": 0.92, "GBP": 0.80}
    """
    # Dictionary, um die Rückgabewerte zu sammeln
    rates = {}

    for symbol in symbols:
        url = (
            "https://www.alphavantage.co/query"
            "?function=CURRENCY_EXCHANGE_RATE"
            f"&from_currency={base}"
            f"&to_currency={symbol}"
            f"&apikey={ALPHA_VANTAGE_API_KEY}"  # Falls du den Key umbenennst, hier anpassen
        )

        resp = requests.get(url).json()

        # Alpha Vantage liefert die Wechselkurse in diesem Abschnitt zurück:
        # "Realtime Currency Exchange Rate"
        if "Realtime Currency Exchange Rate" in resp:
            exchange_data = resp["Realtime Currency Exchange Rate"]
            exchange_rate_str = exchange_data.get("5. Exchange Rate")

            # Versuchen, den String in eine Zahl umzuwandeln.
            # Falls der Wert nicht vorhanden oder ungültig ist, setzen wir None.
            try:
                rates[symbol] = float(exchange_rate_str)
                
            except (TypeError, ValueError):
                
                rates[symbol] = None
        else:
            # Falls etwas schiefläuft oder das JSON nicht wie erwartet aussieht
            rates[symbol] = None
    print("RATES:", resp)
    return rates

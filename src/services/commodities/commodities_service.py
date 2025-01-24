import yfinance as yf

def get_commodities_prices():
    """
    Ruft aktuelle (bzw. leicht verzögerte) Schlusskurse 
    zu bestimmten Commodities von Yahoo Finance ab und gibt sie zurück.

    Verwendete Ticker (Stand: 2025, kann sich ändern):
    - Sojabohnen: ZS=F (Soybeans)
    - Kakao: CC=F (Cocoa)
    - WTI-Öl: CL=F (Crude Oil WTI)
    - Erdgas: NG=F (Natural Gas)
    - Rindfleisch (Live Cattle): LE=F
    - Arabica Kaffee: KC=F
    - Weizen: ZW=F (Wheat)
    """

    tickers = {
        "ZS=F": "Soybeans",
        "CC=F": "Cocoa",
        "CL=F": "Crude Oil WTI",
        #"LE=F": "Live Cattle (Beef)", returned immer nan
        "NG=F": "Natural Gas",
        "KC=F": "Coffee (Arabica)",
        "ZW=F": "Wheat"
    }

    # 1) Daten von Yahoo Finance herunterladen
    data = yf.download(
        list(tickers.keys()),
        period="1d",      # nur den aktuellen Tag
        interval="1d",    # täglicher Schlusskurs
        progress=False
    )

    # 2) Letzten Schlusskurs extrahieren
    try:
        latest_close = data["Close"].iloc[-1]
    except (IndexError, KeyError):
        print("Keine Daten empfangen – Markt geschlossen oder API-Fehler?")
        return []

    # 3) Ergebnisse zusammenbauen
    results = []
    for ticker, name in tickers.items():
        price = latest_close.get(ticker, None)
        if price is None:
            continue  # Falls Yahoo keinen Kurs für diesen Tag liefert
        results.append({
            "ticker": ticker,
            "name": name,
            "price": float(price)
        })

    return results


if __name__ == "__main__":
    # Zum Testen:
    commodities_prices = get_commodities_prices()
    print(commodities_prices)

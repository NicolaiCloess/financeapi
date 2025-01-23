import yfinance as yf

def get_all_stock_prices():
    """
    Ruft die aktuellen (bzw. leicht verzögerten) Schlusskurse 
    für die angegebenen Aktien/Indizes ab und gibt sie zurück.
    """
    tickers = {
        "^GSPC": "S&P 500",             
        "AAPL":  "Apple",
        "MSFT":  "Microsoft",
        "NVDA":  "Nvidia",
        "TSLA":  "Tesla",
        "GOOGL": "Alphabet (Google)",
        "URTH":  "MSCI World (iShares)", 
        "EEM":   "MSCI Emerging Markets (iShares)"
    }

    # Daten von Yahoo Finance herunterladen
    data = yf.download(
        list(tickers.keys()),
        period="1d",
        interval="1d",
        progress=False
    )

    try:
        latest_close = data["Close"].iloc[-1]
    except (IndexError, KeyError):
        print("Keine Daten empfangen. Eventuell ist der Markt geschlossen oder ein Fehler aufgetreten.")
        return []

    results = []
    for ticker, name in tickers.items():
        price = latest_close[ticker]
        results.append({
            "ticker": ticker,
            "name": name,
            "price": float(price)
        })

    # Statt auszugeben -> zurückgeben
    return results

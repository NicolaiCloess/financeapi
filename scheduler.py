from apscheduler.schedulers.blocking import BlockingScheduler
from src.services.crypto.crypto_service import get_crypto_prices
from src.services.metals.metals_service import get_metals_prices
from src.services.currency.currency_service import get_currency_rates
from src.services.commodities.commodities_service import get_commodities_prices
from supabase import create_client, Client
from src.config.config import SUPABASE_URL, SUPABASE_KEY

from src.services.stocks.stocks_service import get_all_stock_prices
import datetime

scheduler = BlockingScheduler()
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def update_currencies():
    try:
        curr = get_currency_rates("USD", ["EUR", "GBP", "CHF","JPY", "INR"])
        print(curr)
        for symbol, price in curr.items():
            if price is not None:
                response = supabase.table("asset_prices").update({
                    "price": price,
                    "date_time": datetime.datetime.utcnow().isoformat()
                }).eq("asset_symbol", symbol).execute()
                # Erfolgsprüfung
                if response.data:
                    print(f"Preis für {symbol} erfolgreich aktualisiert: {price}")
                else:
                    print(f"Fehler beim Aktualisieren von {symbol}: {response}")
            else:
                print(f"Kein gültiger Preis für {symbol} erhalten.")
        

    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")





def update_crypto_prices():
    try:
        # Abrufen der Kryptopreise von der API
        crypto = get_crypto_prices()
        # Symbole für die Kryptowährungen
        crypto_symbols = {
            "bitcoin_price_usd": "BTC",
            "ethereum_price_usd": "ETH",
            "solana_price_usd": "SOL",
            "aragon_price_usd": "ANT",
            "cardano_price_usd": "ADA",
            "ripple_price_usd": "XRP",
            "usdcoin_price_usd": "USDC",
            "dogecoin_price_usd": "DOGE",
            "binancecoin_price_usd": "BNB",
            "tether_price_usd": "USDT"
        }

        # Aktualisiere die Preise in Supabase
        for price_key, symbol in crypto_symbols.items():
            price = crypto.get(price_key)
            if price is not None:
                # Update-Abfrage an Supabase
                response = supabase.table("asset_prices").update({
                    "price": price,
                    "date_time": datetime.datetime.utcnow().isoformat()
                }).eq("asset_symbol", symbol).execute()

                # Erfolgsprüfung mit response.data
                if response.data:
                    print(f"Preis für {symbol} erfolgreich aktualisiert: {price}")
                else:
                    print(f"Fehler beim Aktualisieren von {symbol}: {response}")

    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")


def update_metals_price():
    try:
        # Abrufen der Metallpreise von der API
        metals = get_metals_prices()
        
        if "error" in metals:
            print(f"Fehler beim Abrufen der Metallpreise: {metals['error']}")
            return

        # Metallsymbole und ihre zugehörigen Spaltennamen
        metal_symbols = {
            "gold_price_usd": "XAU",
            "silver_price_usd": "XAG",
            "platinum_price_usd": "XPT",
            "palladium_price_usd": "XPD",
            "copper_price_usd": "XCU",
            "aluminum_price_usd": "ALU",
            "nickel_price_usd": "NI",
            "zinc_price_usd": "ZNC",
            "lead_price_usd": "LEAD",
            "tin_price_usd": "TIN"
        }

        # Aktualisiere die Preise in der Supabase-Datenbank
        for price_key, symbol in metal_symbols.items():
            price = 1 / metals.get(price_key)
            if price is not None:
                # Update-Abfrage an Supabase
                response = supabase.table("asset_prices").update({
                    "price": price,
                    "date_time": datetime.datetime.utcnow().isoformat()
                }).eq("asset_symbol", symbol).execute()

                # Erfolgsprüfung mit response.data
                if response.data:
                    print(f"Preis für {symbol} erfolgreich aktualisiert: {price}")
                else:
                    print(f"Fehler beim Aktualisieren von {symbol}: {response}")
    
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")


def update_stocks():
    try:
        # Ruft die aktuellen Stock-Preise von Yahoo Finance ab
        stocks = get_all_stock_prices()
        
        # Aktualisiert für jedes Ticker-Symbol die Tabelle asset_prices
        for item in stocks:
            ticker = item["ticker"]
            name = item["name"]
            price = item["price"]
            print(item)

            # Update in der Supabase asset_prices-Tabelle
            response = supabase.table("asset_prices").update({
                "price": price,
                "date_time": datetime.datetime.utcnow().isoformat()
            }).eq("asset_symbol", ticker).execute()

            # Erfolg bzw. Fehler abfangen
            if response.data:
                print(f"{ticker} ({name}) erfolgreich aktualisiert: {price}")
            else:
                print(f"Fehler beim Aktualisieren von {ticker} ({name}): {response}")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")


def update_commodities():
    """
    Ruft mithilfe von yfinance die aktuellen Commodity-Preise ab 
    und aktualisiert die asset_prices-Tabelle in Supabase.
    """
    try:
        # 1) Abrufen der aktuellen Commodity-Preise (Liste mit Dicts)
        commodities = get_commodities_prices()
        
        # 2) Für jeden Eintrag in der Liste das passende asset_prices-Record updaten
        for item in commodities:
            ticker = item["ticker"]
            name = item["name"]
            price = item["price"]
            print("Update Commodity:", item)

            # Beispiel: Update in 'asset_prices' basierend auf "asset_symbol" = ticker
            # Achtung: Passe 'asset_symbol' an, wenn deine Spalte anders heißt
            response = supabase.table("asset_prices").update({
                "price": price,
                "date_time": datetime.datetime.utcnow().isoformat()
            }).eq("asset_symbol", ticker).execute()

            # Erfolg oder Fehler prüfen
            if response.data:
                print(f"{ticker} ({name}) erfolgreich aktualisiert: {price}")
            else:
                print(f"Fehler beim Aktualisieren von {ticker} ({name}): {response}")

    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")


# Jobs hinzufügen
scheduler.add_job(update_crypto_prices, 'interval', seconds=2678) # ca. 44 Minuten
#scheduler.add_job(update_metals_price, 'interval', seconds=13400)
scheduler.add_job(update_metals_price, 'interval', seconds=3)
scheduler.add_job(update_currencies, 'interval', seconds=17300)  # 25 Anfragen / Tag
scheduler.add_job(update_stocks, 'interval', seconds=115) # jede Minute 
scheduler.add_job(update_commodities, 'interval', seconds=120)


#scheduler.add_job(update_commodities, 'interval', seconds=10)
if __name__ == "__main__":
    scheduler.start()

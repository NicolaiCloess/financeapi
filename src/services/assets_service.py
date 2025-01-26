# src/services/assets_service.py

from supabase import create_client, Client
from src.config.config import SUPABASE_URL, SUPABASE_KEY

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_assets_by_type(asset_type: str):
    """
    Liest alle Einträge aus der Tabelle 'assets', gefiltert nach 'asset_type'.
    Gibt eine Liste der Datensätze als Python-Objekte (Liste von Dicts) zurück.
    Enthält asset_id, um Preise abfragen zu können.
    """
    response = (
        supabase
        .table("assets")
        .select("asset_id, symbol, name, currency, unit")
        .eq("asset_type", asset_type)
        .execute()
    )
    return response.data  # Liste von Dicts

def get_asset_by_symbol_and_type(symbol: str, asset_type: str):
    """
    Sucht in der Tabelle 'assets' einen Eintrag mit dem gegebenen asset_type und symbol.
    Gibt das gefundene Asset-Dict zurück oder None, wenn nichts gefunden wurde.
    """
    response = (
        supabase
        .table("assets")
        .select("asset_id, symbol, name, currency, unit")
        .eq("asset_type", asset_type)
        .eq("symbol", symbol)
        .execute()
    )
    data = response.data  # Liste von Dicts
    if data:
        return data[0]  # Nimmt das erste gefundene Element
    else:
        return None

def get_latest_price_for_asset(asset_id: int):
    """
    Sucht in der Tabelle 'asset_prices' den letzten Preis (nach date_time DESC)
    für das gegebene asset_id. Gibt ein Dict mit {price, date_time} zurück
    oder None, wenn kein Preis gefunden wird.
    """
    response = (
        supabase
        .table("asset_prices")
        .select("price, date_time")
        .eq("asset_id", asset_id)
        .order("date_time", desc=True)
        .limit(1)
        .execute()
    )
    data = response.data
    if data:
        return data[0]  # dict mit {"price":..., "date_time":...}
    else:
        return None

def get_assets_with_latest_price(asset_type: str):
    """
    1) Holt alle Assets des gegebenen asset_type (z.B. 'stock').
    2) Ermittelt pro Asset den zuletzt bekannten Preis.
    3) Kombiniert alles in einem konsistenten JSON-ähnlichen Format.
    Gibt eine Liste von Dicts zurück.
    """
    assets = get_assets_by_type(asset_type)  # Alle Assets dieses Typs
    result = []

    for asset in assets:
        asset_id = asset["asset_id"]

        # Letzten Preis für dieses Asset holen
        latest_price_data = get_latest_price_for_asset(asset_id)
        if latest_price_data:
            price = latest_price_data["price"]
            date_time = latest_price_data["date_time"]
        else:
            # Falls kein Preis verfügbar ist, kann hier None gesetzt werden oder
            # du könntest das Asset komplett rausfiltern.
            price = None
            date_time = None

        # Neues Dict erstellen
        result.append({
            "symbol": asset["symbol"],
            "name": asset["name"],
            "currency": asset["currency"],
            "unit": asset["unit"],
            "price": price,
            "date_time": date_time
        })

    return result


# für /prices
def get_all_assets():
    """
    Liest sämtliche Einträge aus der Tabelle 'assets' – ohne Filter auf asset_type.
    Gibt eine Liste von Dicts zurück, inkl. 'asset_id' zum späteren Preisabruf.
    """
    response = (
        supabase
        .table("assets")
        .select("asset_id, symbol, name, currency, unit, asset_type")
        .execute()
    )
    return response.data 

def get_all_assets_with_latest_price():
    """
    Holt alle Assets und deren neuesten Preis in einer einzigen Abfrage.
    Gibt eine Liste von Dicts zurück.
    """
    response = (
        supabase.rpc(
            "get_assets_with_latest_price"  # Die SQL-Funktion in Supabase
        ).execute()
    )

    if response.data:
        return response.data
    else:
        return []

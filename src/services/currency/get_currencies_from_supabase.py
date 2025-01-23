# stocks_service.py

from supabase import create_client, Client
from src.config.config import SUPABASE_URL, SUPABASE_KEY


supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
def get_currencies():
    """
    Liest alle Einträge aus der Tabelle 'assets', die den asset_type 'stock' haben.
    Gibt eine Liste der Datensätze als Python-Objekt (Liste von Dicts) zurück.
    """
    response = supabase.table("assets") \
                       .select("symbol, name, currency, unit") \
                       .eq("asset_type", "curr") \
                       .execute()
    
    # .data enthält die eigentlichen Ergebnisse
    return response.data

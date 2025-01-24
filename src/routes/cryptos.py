from flask import Blueprint, jsonify
from src.services.crypto.get_cryptos_from_supabase import get_cryptos
from src.extensions import cache  # Globale Cache-Instanz importieren

cryptos_blueprint = Blueprint('cryptos', __name__)  # Blueprint-Objekt

@cryptos_blueprint.route("/cryptos", methods=["GET"])
@cache.cached(timeout=90)
def get_all_cryptos():
    """Gibt alle Stocks aus der Supabase-Datenbank als JSON zurück."""
    cryptos_data = get_cryptos()
    return jsonify(cryptos_data)

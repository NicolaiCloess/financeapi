from flask import Blueprint, jsonify
from src.services.currency.get_currencies_from_supabase import get_currencies
from src.extensions import cache  # Globale Cache-Instanz importieren

currencies_blueprint = Blueprint('currencies', __name__)  # Blueprint-Objekt

@currencies_blueprint.route("/currencies", methods=["GET"])
@cache.cached(timeout=90)
def get_all_currenciess():
    """Gibt alle Stocks aus der Supabase-Datenbank als JSON zurück."""
    currencies_data = get_currencies()
    return jsonify(currencies_data)

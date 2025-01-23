from flask import Blueprint, jsonify
from src.services.currency.get_currencies_from_supabase import get_currencies

currencies_blueprint = Blueprint('currencies', __name__)  # Blueprint-Objekt

@currencies_blueprint.route("/currencies", methods=["GET"])
def get_all_currenciess():
    """Gibt alle Stocks aus der Supabase-Datenbank als JSON zurück."""
    currencies_data = get_currencies()
    return jsonify(currencies_data)

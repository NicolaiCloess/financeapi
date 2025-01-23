from flask import Blueprint, jsonify
from src.services.commodities.get_commodities_from_supabase import get_commodities

commodities_blueprint = Blueprint('commodities', __name__)  # Blueprint-Objekt

@commodities_blueprint.route("/commodities", methods=["GET"])
def get_all_commodities():
    """Gibt alle Stocks aus der Supabase-Datenbank als JSON zurück."""
    commodities_data = get_commodities()
    return jsonify(commodities_data)

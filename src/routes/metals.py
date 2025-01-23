from flask import Blueprint, jsonify
from src.services.metals.get_metals_from_supabase import get_metals

metals_blueprint = Blueprint('metals', __name__)  # Blueprint-Objekt

@metals_blueprint.route("/metals", methods=["GET"])
def get_all_metals():
    """Gibt alle Stocks aus der Supabase-Datenbank als JSON zurück."""
    metals_data = get_metals()
    return jsonify(metals_data)

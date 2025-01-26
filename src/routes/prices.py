# src/routes/prices.py
from flask import Blueprint, jsonify
from src.services.assets_service import get_all_assets_with_latest_price
from src.extensions import cache
prices_blueprint = Blueprint("prices_blueprint", __name__)

@prices_blueprint.route("/prices", methods=["GET"])
@cache.cached(timeout=90)  # Cache für 90 Sekunden
def get_prices():
    """
    Gibt alle Assets (stocks, crypto, commodities, etc.) zurück,
    jeweils mit dem zuletzt bekannten Preis.
    """
    
    data = get_all_assets_with_latest_price()
    return jsonify(data)

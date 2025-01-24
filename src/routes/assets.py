# src/routes/assets_routes.py
from flask import Blueprint, jsonify, abort
from src.services.assets_service import (
    get_assets_with_latest_price,
    get_asset_by_symbol_and_type,
    get_latest_price_for_asset,
    get_all_assets,   
)
from src.extensions import cache  # Globale Cache-Instanz importieren


assets_blueprint = Blueprint('assets', __name__)

@assets_blueprint.route("/assets", methods=["GET"])
@cache.cached(timeout=90)  # Cache für 90 Sekunden
def get_all_assets_no_price():
    """
    Gibt alle Assets aus der Datenbank OHNE Preise zurück.
    """
    data = get_all_assets()
    return jsonify(data)

@assets_blueprint.route("/assets/<asset_type>", methods=["GET"])
@cache.cached(timeout=90)
def get_all_assets_with_price(asset_type):
    """
    Gibt alle Assets eines bestimmten Typs (z. B. 'stock', 'crypto')
    zusammen mit dem letzten Preis zurück.
    """
    data = get_assets_with_latest_price(asset_type)
    return jsonify(data)

@assets_blueprint.route("/assets/<asset_type>/<symbol>", methods=["GET"])
@cache.cached(timeout=90)
def get_asset_detail(asset_type, symbol):
    """
    Gibt ein bestimmtes Asset (z. B. /assets/stock/AAPL) mit dem letzten Preis zurück.
    """
    asset = get_asset_by_symbol_and_type(symbol, asset_type)
    if not asset:
        return abort(404, description=f"No asset found for type '{asset_type}', symbol '{symbol}'")

    latest_price = get_latest_price_for_asset(asset["asset_id"])
    if not latest_price:
        return abort(404, description=f"No price found for symbol '{symbol}' in '{asset_type}'")

    return jsonify({
        "symbol": asset["symbol"],
        "name": asset["name"],
        "currency": asset["currency"],
        "unit": asset["unit"],
        "price": latest_price["price"],
        "date_time": latest_price["date_time"]
    })

# routes/stocks.py
from flask import Blueprint, jsonify, abort
from src.services.stocks.get_stocks_from_supabase import get_stocks

stocks_blueprint = Blueprint('stocks', __name__)  # Blueprint-Objekt

@stocks_blueprint.route("/stocks", methods=["GET"])
def get_all_stocks():
    """Gibt alle Stocks aus der Supabase-Datenbank als JSON zurück."""
    stocks_data = get_stocks()
    return jsonify(stocks_data)



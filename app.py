from flask import Flask
from src.routes.currencies import currencies_blueprint
from src.routes.commodities import commodities_blueprint
from src.routes.stocks import stocks_blueprint
from src.routes.cryptos import cryptos_blueprint
from src.routes.metals import metals_blueprint
from src.routes.assets import assets_blueprint
from src.routes.prices import prices_blueprint
from src.extensions import cache  # Import der globalen Cache-Instanz

def create_app():
    app = Flask(__name__)

    # Cache-Konfiguration
    app.config["CACHE_TYPE"] = "SimpleCache"
    app.config["CACHE_DEFAULT_TIMEOUT"] = 90
    cache.init_app(app) 

    app.register_blueprint(currencies_blueprint)  # Hier das neue Blueprint registrieren
    app.register_blueprint(commodities_blueprint)  # Neues Blueprint hinzufügen
    app.register_blueprint(stocks_blueprint) 
    app.register_blueprint(cryptos_blueprint)  
    app.register_blueprint(metals_blueprint)  
    app.register_blueprint(assets_blueprint)
    app.register_blueprint(prices_blueprint)
    return app

if __name__ == "__main__":
    app = create_app()

    app.run(debug=True, host="0.0.0.0", port=1004)



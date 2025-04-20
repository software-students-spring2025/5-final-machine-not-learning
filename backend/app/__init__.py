import os
from flask import Flask, render_template
from flask_pymongo import PyMongo
from dotenv import load_dotenv

mongo = PyMongo()

def create_app():
    load_dotenv()

    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), "../templates"),
        static_folder=os.path.join(os.path.dirname(__file__), "../static")
    )

    app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/barbuddy")
    mongo.init_app(app)

    from .routes.inventory import inventory_bp
    from .routes.suggest import suggest_bp
    from .routes.alert import alert_bp
    from .routes.ai_suggest import ai_bp
    app.register_blueprint(ai_bp, url_prefix="/api/ai")
    app.register_blueprint(inventory_bp, url_prefix="/api/inventory")
    app.register_blueprint(suggest_bp, url_prefix="/api/suggestions")
    app.register_blueprint(alert_bp, url_prefix="/api/alerts")

    @app.route("/")
    def dashboard():
        return render_template("index.html")

    @app.route("/inventory")
    def inventory_page():
        return render_template("inventory.html")

    @app.route("/suggestions")
    def suggestions_page():
        return render_template("suggestions.html")

    @app.route("/alerts")
    def alerts_page():
        return render_template("alerts.html")

    return app

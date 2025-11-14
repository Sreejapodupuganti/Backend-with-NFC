import os
from flask import Flask
from flask_cors import CORS
from .config import Config
from .extensions import db, migrate, bcrypt
from .routes.auth_routes import auth_bp
from .routes.card_routes import card_bp
from .routes.admin_routes import admin_bp
from .routes.payment_routes import payment_bp
from .routes.analytics_routes import analytics_bp
from .routes.wallet_routes import wallet_bp
from .routes.main_routes import main_bp

def create_app(config_class: type = Config):
    app = Flask(__name__)

    # Correct CORS for Azure Frontend
    CORS(app, resources={r"/*": {"origins": [
        "https://frontendnfc-bzdxewfrhvbketgx.centralus-01.azurewebsites.net"
    ]}})

    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # Removed cors().init_app(app)

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(card_bp, url_prefix='/api/card')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(payment_bp, url_prefix='/api/payment')
    app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
    app.register_blueprint(wallet_bp, url_prefix='/api/wallet')

    with app.app_context():
        from . import models
        if app.config.get("AUTO_CREATE_DB", True):
            db.create_all()

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app

# ufonewsapp/__init__.py
# © 2025 Rogue Planet. All rights reserved.

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from .config import Config

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    from .models import article_create_bp
    app.register_blueprint(article_create_bp)

    @app.route("/", methods=["GET"])
    def home():
        return jsonify({"status": "UFO News Desk is live"})

    @app.route("/init-db", methods=["POST"])
    def init_db():
        with app.app_context():
            db.create_all()
        return jsonify({"message": "Database initialized!"})

    return app

app = create_app()


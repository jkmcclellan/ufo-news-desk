# ufonewsapp/__init__.py
# __init__.py
# © 2025 Rogue Planet. All rights reserved.

import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Initialize app and extensions
app = Flask(__name__)

# Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "your_jwt_secret_key")

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Import and register blueprints
from ufonewsapp.models import article_create_bp
app.register_blueprint(article_create_bp)

# Endpoint to initialize the database (for admin use only)
@app.route("/init-db", methods=["POST"])
def init_db():
    if request.headers.get("X-Admin-Secret") != "v1-q48xg":
        return {"error": "Unauthorized"}, 401

    db.create_all()
    return {"status": "Database initialized successfully"}

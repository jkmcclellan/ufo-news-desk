# app/__init__.py
# © 2025 Rogue Planet. All rights reserved.

from flask import Flask
from flask_jwt_extended import JWTManager
from .models import db

# Create the Flask app
app = Flask(__name__)

# Basic config (can be customized or loaded from environment)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///temp.db"  # Overwritten by Render
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "super-secret"  # Should be set via env var in production

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)

# Register blueprints
from ufonewsapp.models import db, article_create_bp
app.register_blueprint(article_create_bp)

# Root endpoint for health check
@app.route("/")
def index():
    return {"status": "UFO News Desk is live"}
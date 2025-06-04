# ufonewsapp/__init__.py
# © 2025 Rogue Planet. All rights reserved.

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS  # Optional: for testing from web clients
from ufonewsapp.models import db, article_create_bp

app = Flask(__name__)
CORS(app)  # <- Helps avoid CORS errors in browser-based clients

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///temp.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "super-secret"

db.init_app(app)
jwt = JWTManager(app)

# Register your blueprint
app.register_blueprint(article_create_bp)

@app.route("/")
def index():
    return {"status": "UFO News Desk is live"}

__all__ = ["app"]

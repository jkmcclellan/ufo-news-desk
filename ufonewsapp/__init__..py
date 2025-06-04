# ufonewsapp/__init__.py
# © 2025 Rogue Planet. All rights reserved.

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from ufonewsapp.models import db, article_create_bp

# Create the Flask app
app = Flask(__name__)

# Basic config (can be customized or loaded from environment)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///temp.db"  # Overwritten by Render
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "super-secret"  # Set this via env var in production

# Enable CORS for all routes with explicit settings
CORS(
    app,
    origins="*",
    methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    supports_credentials=True
)

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(article_create_bp)

from flask import request
from ufonewsapp.models import db

@app.route("/init-db", methods=["POST"])
def init_db():
    # Basic protection — replace 'YOUR_SECRET_KEY' with something only you know
    if request.headers.get("X-Admin-Secret") != "YOUR_SECRET_KEY":
        return {"error": "Unauthorized"}, 401

    db.create_all()
    return {"status": "Database initialized successfully"}


# Root endpoint for health check
@app.route("/")
def index():
    return {"status": "UFO News Desk is live"}

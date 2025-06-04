# ufonewsapp/__init__.py
# © 2025 Rogue Planet. All rights reserved.

from flask import Flask
from flask_jwt_extended import JWTManager
from .models import db, article_create_bp

# Create the Flask app
app = Flask(__name__)

# Basic config (customize or pull from environment in production)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///temp.db"  # Overwritten by Render
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "my-very-secret-key"  # Replace with env var in production

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(article_create_bp)

# Root endpoint for health check
@app.route("/")
def index():
    return {"status": "UFO News Desk is live"}

# Temporary endpoint to initialize the database
@app.route("/init-db", methods=["POST"])
def init_db():
    with app.app_context():
        db.create_all()
    return {"message": "Database initialized"}

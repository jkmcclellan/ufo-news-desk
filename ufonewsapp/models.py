# ufonewsapp/models.py
# © 2025 Rogue Planet. All rights reserved.

from flask import Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
article_create_bp = Blueprint("article_create_bp", __name__)

# Define the Article model
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(2048), nullable=False)
    author = db.Column(db.String(255), nullable=True)
    summary = db.Column(db.Text, nullable=True)
    publisher = db.Column(db.String(255), nullable=True)
    published_at = db.Column(db.String(255), nullable=True)
    topics = db.Column(db.String(255), nullable=True)
    people = db.Column(db.String(255), nullable=True)
    places = db.Column(db.String(255), nullable=True)

# Define the /create-article POST endpoint
@article_create_bp.route("/create-article", methods=["POST"])
def create_article():
    data = request.get_json()

    # Basic field validation
    if not data or not data.get("title") or not data.get("url"):
        return jsonify({"error": "Missing required fields: 'title' and 'url'"}), 400

    # Create and save a new Article (mocked for now)
    new_article = Article(
        title=data["title"],
        url=data["url"],
        author=data.get("author"),
        summary=data.get("summary"),
        publisher=data.get("publisher"),
        published_at=data.get("published_at"),
        topics=data.get("topics"),
        people=data.get("people"),
        places=data.get("places")
    )

    db.session.add(new_article)
    db.session.commit()

    return jsonify({
        "message": "Article created successfully",
        "article": {
            "id": new_article.id,
            "title": new_article.title,
            "url": new_article.url
        }
    }), 201

# app/models.py
# © 2025 Rogue Planet. All rights reserved.

from flask import Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token, jwt_required
from datetime import datetime
import requests
from bs4 import BeautifulSoup


db = SQLAlchemy()
article_create_bp = Blueprint("articles", __name__)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, unique=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=True)
    date = db.Column(db.String, nullable=True)
    source = db.Column(db.String, nullable=True)
    summary = db.Column(db.Text, nullable=True)
    topics = db.Column(db.String, nullable=True)
    people = db.Column(db.String, nullable=True)
    places = db.Column(db.String, nullable=True)
    tags = db.Column(db.String, nullable=True)
    thumbnail_url = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class AdminUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)


def create_initial_admin(email, password):
    if not AdminUser.query.filter_by(email=email).first():
        user = AdminUser(email=email, password=password)
        db.session.add(user)
        db.session.commit()


@article_create_bp.route("/api/token", methods=["POST"])
def login():
    data = request.get_json()
    user = AdminUser.query.filter_by(email=data.get("email"), password=data.get("password")).first()
    if user:
        return jsonify(access_token=create_access_token(identity=user.email))
    return jsonify({"error": "Invalid credentials"}), 401


@article_create_bp.route("/api/articles", methods=["POST"])
@jwt_required()
def add_article():
    data = request.get_json()
    article = Article(**data)
    db.session.add(article)
    db.session.commit()
    return jsonify({"message": "Article added"})


@article_create_bp.route("/api/articles", methods=["GET"])
def list_articles():
    keyword = request.args.get("q", "").lower()
    tag_filter = request.args.get("tag")
    sort_order = request.args.get("sort", "desc")

    query = Article.query
    if keyword:
        query = query.filter(
            db.or_(
                Article.title.ilike(f"%{keyword}%"),
                Article.summary.ilike(f"%{keyword}%"),
                Article.topics.ilike(f"%{keyword}%"),
                Article.tags.ilike(f"%{keyword}%")
            )
        )
    if tag_filter:
        query = query.filter(Article.tags.ilike(f"%{tag_filter}%"))
    if sort_order == "asc":
        query = query.order_by(Article.date.asc())
    else:
        query = query.order_by(Article.date.desc())

    articles = query.all()
    return jsonify([
        {
            "id": a.id,
            "url": a.url,
            "title": a.title,
            "author": a.author,
            "date": a.date,
            "source": a.source,
            "summary": a.summary,
            "topics": a.topics,
            "people": a.people,
            "places": a.places,
            "tags": a.tags,
            "thumbnail_url": a.thumbnail_url,
        }
        for a in articles
    ])


@article_create_bp.route("/api/extract", methods=["POST"])
@jwt_required()
def extract_article_metadata():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"error": "Missing URL"}), 400

    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "lxml")

        title = soup.title.string.strip() if soup.title else ""
        author = soup.find("meta", attrs={"name": "author"})
        date = soup.find("meta", attrs={"property": "article:published_time"})
        source = requests.utils.urlparse(url).hostname
        summary = ""
        og_desc = soup.find("meta", attrs={"property": "og:description"})
        if og_desc and og_desc.get("content"):
            summary = og_desc["content"]
        elif soup.p:
            summary = soup.p.get_text(strip=True)

        thumbnail = soup.find("meta", attrs={"property": "og:image"})
        thumbnail_url = thumbnail["content"] if thumbnail and thumbnail.get("content") else None

        return jsonify({
            "url": url,
            "title": title,
            "author": author["content"] if author and author.get("content") else "",
            "date": date["content"] if date and date.get("content") else "",
            "source": source,
            "summary": summary,
            "thumbnail_url": thumbnail_url,
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ufonewsapp/main.py
from flask import Flask
from flask_jwt_extended import JWTManager
from ufonewsapp.models import db, article_create_bp

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///temp.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "super-secret"

db.init_app(app)
jwt = JWTManager(app)
app.register_blueprint(article_create_bp)

@app.route("/")
def index():
    return {"status": "UFO News Desk is live"}

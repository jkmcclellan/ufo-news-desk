# init_db.py
# One-time database initialization script
from ufonewsapp import app
from ufonewsapp.models import db

with app.app_context():
    db.create_all()
    print("✅ Database initialized.")

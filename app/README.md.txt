# 🚘 UFO News Desk

A simple, searchable web app for collecting, tagging, and archiving UFO-related news articles. Built with Flask, PostgreSQL, and deployed on Render.com.

---

## 🚀 Features

- 📰 Paste a URL to auto-extract article data (title, author, date, summary, thumbnail, etc.)
- 🔍 Search and filter articles by keyword or tag
- 🔝 Admin-only login for submitting or editing articles
- 🌐 Public access to browse and search the database
- 🖼️ Open Graph image scraping for thumbnails

---

## 🧰 Tech Stack

- Python (Flask)
- PostgreSQL (via Render)
- Flask-JWT-Extended for admin auth
- BeautifulSoup + Requests for article scraping
- Hosted on [Render](https://render.com)

---

## 📦 Project Structure

```
ufo-news-desk/
├── app/
│   ├── __init__.py       # Main Flask app
│   ├── models.py         # Database models and routes
│   └── routes/           # Helper scripts (e.g. thumbnail scraping)
├── requirements.txt      # Python dependencies
├── Procfile              # Gunicorn launch command
├── render.yaml           # Render deployment config
└── README.md             # You're reading this!
```

---

## 🧪 Local Development

1. Clone the repo:
   ```bash
   git clone https://github.com/your-username/ufo-news-desk
   cd ufo-news-desk
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   flask run
   ```

---

## 🔐 Admin Setup (After Deploy)

1. Open the Render **Shell**
2. Run Python:
   ```bash
   python
   >>> from app.models import create_initial_admin
   >>> create_initial_admin("you@example.com", "yourpassword")
   ```

---

## 📡 Deployment (Render)

1. Connect this repo to [https://render.com](https://render.com)
2. Render will auto-detect `render.yaml`
3. Done — your site is live!

---

## 🧠 Credits

Created by [Rogue Planet](https://rogueplanet.tv)  
© 2025 Rogue Planet. All rights reserved.
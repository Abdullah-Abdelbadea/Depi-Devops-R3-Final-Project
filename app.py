from flask import Flask, request, jsonify, redirect, render_template, g
import sqlite3
import secrets
import string
import time
import os

DB_PATH = os.environ.get("DB_PATH", "data/url_shortener.db")
SHORT_CODE_LEN = 6

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    cur = db.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS urls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        short_code TEXT UNIQUE,
        long_url TEXT NOT NULL,
        created_at INTEGER
    )""")
    db.commit()

def generate_code(n=SHORT_CODE_LEN):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(n))

app = Flask(__name__, template_folder="templates", static_folder="static")

with app.app_context():
    init_db()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/shorten", methods=["POST"])
def shorten():
    data = request.get_json() or {}
    url = data.get("url") if isinstance(data.get("url"), str) else data.get("long_url")
    if not url:
        # also handle form submissions
        url = request.form.get("url")
        if not url:
            return jsonify({"error":"no url provided"}), 400
    db = get_db()
    cur = db.cursor()
    # check if url already shortened
    cur.execute("SELECT short_code FROM urls WHERE long_url = ?", (url,))
    row = cur.fetchone()
    if row:
        short_code = row["short_code"]
    else:
        # generate unique code
        for _ in range(10):
            short_code = generate_code()
            try:
                cur.execute("INSERT INTO urls (short_code, long_url, created_at) VALUES (?, ?, ?)", (short_code, url, int(time.time())))
                db.commit()
                break
            except sqlite3.IntegrityError:
                continue
        else:
            return jsonify({"error":"could not generate unique code"}), 500
    short_url = request.host_url.rstrip("/") + "/" + short_code
    return jsonify({"short_code": short_code, "short_url": short_url, "long_url": url})

@app.route("/<short_code>")
def redirect_short(short_code):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT long_url FROM urls WHERE short_code = ?", (short_code,))
    row = cur.fetchone()
    if row:
        return redirect(row["long_url"])
    else:
        return render_template("404.html", code=short_code), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

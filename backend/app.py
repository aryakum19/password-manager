from flask import Flask, request, jsonify, render_template, session, redirect
from flask_cors import CORS
import os
import sqlite3
import bcrypt
from cryptography.fernet import Fernet

# App setup
app = Flask(__name__, template_folder="../frontend/templates", static_folder="../frontend/static")
CORS(app)
app.secret_key = os.urandom(24)

# File paths
DB_PATH = os.path.join(os.path.dirname(__file__), "passwords.db")
KEY_PATH = os.path.join(os.path.dirname(__file__), "secret.key")

# Load or generate encryption key
def load_key():
    if not os.path.exists(KEY_PATH):
        key = Fernet.generate_key()
        with open(KEY_PATH, "wb") as f:
            f.write(key)
    else:
        with open(KEY_PATH, "rb") as f:
            key = f.read()
    return Fernet(key)

fernet = load_key()

# Initialize SQLite DB
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            service TEXT,
            username TEXT,
            password TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Routes
@app.route("/")
def home():
    return redirect("/login")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"].encode("utf-8")
        password_hash = bcrypt.hashpw(password, bcrypt.gensalt())

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
            conn.commit()
        except sqlite3.IntegrityError:
            return render_template("signup.html", error="Username already exists")
        conn.close()
        return redirect("/login")
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"].encode("utf-8")

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,))
        user = cur.fetchone()
        conn.close()

        if user and bcrypt.checkpw(password, user[1]):
            session["user_id"] = user[0]
            session["master_hash"] = user[1]
            return redirect("/dashboard")
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("dashboard.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# API Endpoints
@app.route("/api/passwords", methods=["GET"])
def get_passwords():
    if "user_id" not in session:
        return jsonify([])

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, service, username FROM passwords WHERE user_id = ?", (session["user_id"],))
    rows = cur.fetchall()
    conn.close()

    grouped = {}
    for id_, service, username in rows:
        grouped.setdefault(service, []).append({
            "id": id_,
            "username": username
        })
    return jsonify(grouped)

@app.route("/api/passwords", methods=["POST"])
def add_password():
    if "user_id" not in session:
        return jsonify({"status": "unauthorized"}), 401

    data = request.get_json()
    service = data.get("service")
    username = data.get("username")
    password = fernet.encrypt(data.get("password").encode()).decode()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO passwords (user_id, service, username, password) VALUES (?, ?, ?, ?)",
                (session["user_id"], service, username, password))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

@app.route("/api/reveal", methods=["POST"])
def reveal_password():
    if "user_id" not in session:
        return jsonify({"success": False}), 401

    data = request.get_json()
    pwd_id = data.get("id")
    master_password = data.get("master_password").encode("utf-8")

    if not bcrypt.checkpw(master_password, session["master_hash"]):
        return jsonify({"success": False, "message": "Invalid master password"})

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT password FROM passwords WHERE id = ? AND user_id = ?", (pwd_id, session["user_id"]))
    row = cur.fetchone()
    conn.close()

    if row:
        decrypted = fernet.decrypt(row[0].encode()).decode()
        return jsonify({"success": True, "password": decrypted})
    return jsonify({"success": False})

@app.route("/api/delete", methods=["POST"])
def delete_password():
    if "user_id" not in session:
        return jsonify({"status": "unauthorized"}), 401

    data = request.get_json()
    pwd_id = data.get("id")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM passwords WHERE id = ? AND user_id = ?", (pwd_id, session["user_id"]))
    conn.commit()
    conn.close()
    return jsonify({"status": "deleted"})

if __name__ == "__main__":
    app.run(debug=True)

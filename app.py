from flask import Flask, request, redirect, session, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from collections import defaultdict
from time import time
import os
import re

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-this-key")
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = False
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=15)

users = {}
attempts = defaultdict(list)

PAGE = """
<h2>Secure Authentication Lab</h2>
{% if message %}<p>{{ message }}</p>{% endif %}
{% if not session.get('username') %}
<form method="post" action="/register">
<h3>Register</h3>
<input name="username" placeholder="Username" required>
<input name="password" type="password" placeholder="Password" required>
<button type="submit">Register</button>
</form>
<form method="post" action="/login">
<h3>Login</h3>
<input name="username" placeholder="Username" required>
<input name="password" type="password" placeholder="Password" required>
<button type="submit">Login</button>
</form>
{% else %}
<p>Welcome! You are logged in.</p>
<form method="post" action="/logout">
<button type="submit">Logout</button>
</form>
{% endif %}
"""

def valid_input(username, password):
    return (
        re.fullmatch(r"[A-Za-z0-9_]{3,30}", username) is not None
        and 8 <= len(password) <= 128
    )

def rate_limited(ip):
    now = time()
    attempts[ip] = [t for t in attempts[ip] if now - t < 60]
    return len(attempts[ip]) >= 5

@app.route("/", methods=["GET"])
def home():
    return render_template_string(PAGE, message="")

@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    if not valid_input(username, password):
        return render_template_string(
            PAGE, message="Invalid input. Check username and password requirements."
        ), 400

    if username in users:
        return render_template_string(
            PAGE, message="Registration could not be completed."
        ), 400

    users[username] = generate_password_hash(password)
    return render_template_string(PAGE, message="Registration successful. Please log in.")

@app.route("/login", methods=["POST"])
def login():
    ip = request.remote_addr or "unknown"

    if rate_limited(ip):
        return render_template_string(
            PAGE, message="Too many attempts. Please wait one minute."
        ), 429

    attempts[ip].append(time())
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    stored_hash = users.get(username)

    if not stored_hash or not check_password_hash(stored_hash, password):
        return render_template_string(
            PAGE, message="Invalid username or password."
        ), 401

    session.clear()
    session.permanent = True
    session["username"] = username
    return redirect("/")

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=False)
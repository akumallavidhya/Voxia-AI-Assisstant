from flask import Flask, render_template, request, jsonify, redirect, session
import webbrowser
import datetime
import socket
import requests
import os
from dotenv import load_dotenv
import feedparser
from deep_translator import GoogleTranslator
import sqlite3
from bs4 import BeautifulSoup

app = Flask(__name__)
app.secret_key = "voxia_secret"

# LOAD ENV
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

# ---------------- DATABASE ----------------

def get_db():
    return sqlite3.connect("users.db", check_same_thread=False)

def init_db():
    conn = get_db()
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            password TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            message TEXT
        )
    ''')

    conn.commit()
    conn.close()

init_db()

# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("index.html")

# ---------------- SIGNUP ----------------

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            return render_template("signup.html", error="Fill all fields")

        conn = get_db()
        c = conn.cursor()

        try:
            c.execute("INSERT INTO users VALUES (?, ?)", (email, password))
            conn.commit()
            conn.close()
            return redirect("/login")

        except sqlite3.IntegrityError:
            conn.close()
            return render_template("signup.html", error="User already exists")

    return render_template("signup.html")

# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        conn = get_db()
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = c.fetchone()
        conn.close()

        if user:
            session["user"] = email
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT message FROM history WHERE user=? ORDER BY id DESC", (session["user"],))
    history = c.fetchall()
    conn.close()

    return render_template("dashboard.html", history=history)

# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

# ---------------- CHAT API ----------------

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"reply": "Invalid request"})

    command = data["message"].lower()

    response = process_command(command)

    # SAVE HISTORY
    if "user" in session:
        conn = get_db()
        c = conn.cursor()
        c.execute("INSERT INTO history (user, message) VALUES (?, ?)", (session["user"], command))
        conn.commit()
        conn.close()

    return jsonify({"reply": response})

# ---------------- AI FUNCTION ----------------

def ask_ai(prompt):
    try:
        API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}

        response = requests.post(API_URL, headers=headers, json={
            "inputs": prompt,
            "parameters": {"max_new_tokens": 150}
        }, timeout=8)

        if response.status_code != 200:
            return None

        data = response.json()

        if isinstance(data, list):
            return data[0].get("generated_text", "").strip()

        return None

    except:
        return None

# ---------------- GOOGLE FALLBACK ----------------

def google_search(query):
    try:
        url = f"https://www.google.com/search?q={query}"
        headers = {"User-Agent": "Mozilla/5.0"}

        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        for span in soup.find_all("span"):
            text = span.get_text()
            if len(text) > 40:
                return text

        return "No clear answer found."

    except:
        return "Unable to fetch result."

# ---------------- CODE GENERATOR ----------------

def generate_code(command):

    if "even number" in command:
        return """Python Code:
for i in range(1, 51):
    if i % 2 == 0:
        print(i)
"""

    elif "factorial" in command:
        return """Python Code:
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n-1)

print(factorial(5))
"""

    elif "prime" in command:
        return """Python Code:
num = 7
if num > 1:
    for i in range(2, num):
        if num % i == 0:
            print("Not Prime")
            break
    else:
        print("Prime")
"""

    return None

# ---------------- COMMAND PROCESSOR ----------------

def process_command(command):

    try:

        # BASIC
        if "open google" in command:
            webbrowser.open("https://google.com")
            return "Opening Google"

        elif "open youtube" in command:
            webbrowser.open("https://youtube.com")
            return "Opening YouTube"

        elif "search google for" in command:
            topic = command.replace("search google for", "").strip()
            webbrowser.open(f"https://www.google.com/search?q={topic}")
            return f"Searching Google for {topic}"

        elif "time" in command:
            return datetime.datetime.now().strftime("%I:%M %p")

        elif "weather" in command:
            return requests.get("https://wttr.in/?format=3").text

        elif "news" in command:
            feed = feedparser.parse("https://news.google.com/rss")
            return "\n".join([e.title for e in feed.entries[:5]])

        # TRANSLATE
        elif "translate" in command:
            parts = command.replace("translate", "").split("to")

            if len(parts) < 2:
                return "Use: translate hello to hindi"

            text = parts[0].strip()
            lang = parts[1].strip()

            return GoogleTranslator(source='auto', target=lang).translate(text)

        # CODE
        code = generate_code(command)
        if code:
            return code

        # AI
        ai = ask_ai(command)
        if ai:
            return ai

        # GOOGLE FALLBACK
        return google_search(command)

    except Exception as e:
        return f"Error: {str(e)}"

# ---------------- RUN (DEPLOY SAFE) ----------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

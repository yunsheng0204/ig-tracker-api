# api/index.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "https://yunsheng0204.github.io"}})

@app.route("/api/log", methods=["POST", "OPTIONS"])
def log_ig_account():
    if request.method == "OPTIONS":
        return '', 204
    data = request.get_json()
    username = data.get("username", "")
    timestamp = datetime.now().isoformat()
    with open("data.csv", "a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, username])
    send_user_email_notification(username)
    return jsonify({"status": "ok", "username": username})

@app.route("/api/all", methods=["GET"])
def get_all_records():
    try:
        with open("data.csv", newline='', encoding="utf-8") as f:
            reader = csv.reader(f)
            data = list(reader)
        return jsonify({"records": data})
    except FileNotFoundError:
        return jsonify({"records": []})

@app.route("/api/visit", methods=["POST"])
def notify_visit():
    try:
        send_visit_notification()
        return jsonify({"status": "visit notified"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def send_visit_notification():
    sender = "yunsheng1223@gmail.com"
    app_password = "uloktehvlaluugqu"
    receiver = "yunsheng1223@gmail.com"
    html = "<h2>🚨 IG Tracker 網頁被造訪</h2><p>有人剛剛造訪了你的 GitHub 網頁。</p>"
    msg = MIMEText(html, "html")
    msg["Subject"] = "🚨 IG Tracker 網頁被造訪"
    msg["From"] = sender
    msg["To"] = receiver
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, app_password)
        smtp.send_message(msg)

def send_user_email_notification(username):
    sender = "yunsheng1223@gmail.com"
    app_password = "uloktehvlaluugqu"
    receiver = "yunsheng1223@gmail.com"
    ig_url = f"https://www.instagram.com/{username}/"
    html = f"<h2>📩 IG 使用者造訪通知</h2><p><strong>{username}</strong> 造訪了你的 IG Tracker 網站！</p><p>👉 <a href='{ig_url}' target='_blank'>{ig_url}</a></p>"
    msg = MIMEText(html, "html")
    msg["Subject"] = f"📩 IG 使用者 {username} 造訪了你的個人頁面"
    msg["From"] = sender
    msg["To"] = receiver
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, app_password)
        smtp.send_message(msg)

# 👇 Vercel 用這行來辨識 app instance
handler = app

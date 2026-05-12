import os
import smtplib
from email.mime.text import MIMEText

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/send": {"origins": "*"}})

EMAIL_ADDRESS = "techveons.creation.official@gmail.com"
EMAIL_PASSWORD =  "ezmm yfhz uyyy kwmg"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/send', methods=['POST'])
def send():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "message": "Request body must be valid JSON."}), 400

    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    phone = data.get('phone', '').strip()
    message = data.get('message', '').strip()

    if not name or not email or not message:
        return jsonify({"success": False, "message": "Name, email, and message are required."}), 400

    body = f"""
Name: {name}

Email: {email}

Phone: {phone}

Message:
{message}
"""

    msg = MIMEText(body, "plain", "utf-8")
    msg['Subject'] = "New Contact Form Submission"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS

    try:
        app.logger.info("Attempting to send contact email...")
        with smtplib.SMTP('smtp.gmail.com', 587, timeout=20) as server:
            server.ehlo()
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        return jsonify({"success": True, "message": "Email sent successfully."}), 200
    except Exception:
        app.logger.exception("Failed to send contact email")
        return jsonify({"success": False, "message": "Failed to send email. Please try again later."}), 500

@app.errorhandler(500)
def handle_internal_server_error(error):
    app.logger.exception("Internal server error")
    return jsonify({"success": False, "message": "Internal server error."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
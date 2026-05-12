import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.utils import formataddr

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
CORS(app)

EMAIL_ADDRESS = "techveons.creation.official@gmail.com"
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD", "ezmm yfhz uyyy kwmg").strip()
EMAIL_SMTP_HOST = "smtp.gmail.com"
EMAIL_SMTP_PORT = 587
SSL_CONTEXT = ssl.create_default_context()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/send', methods=['POST'])
def send():
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify(success=False, message="Request body must be valid JSON."), 400

        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()
        message = data.get('message', '').strip()

        if not name or not email or not message:
            return jsonify(success=False, message="Name, email, and message are required."), 400

        if not EMAIL_PASSWORD:
            app.logger.error("EMAIL_PASSWORD not configured on Render")
            return jsonify(success=False, message="Email password is not configured. Set EMAIL_PASSWORD env var."), 500

        email_body = (
            f"New contact form submission\n\n"
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Phone: {phone or 'N/A'}\n\n"
            f"Message:\n{message}\n"
        )

        msg = MIMEText(email_body, "plain", "utf-8")
        msg['Subject'] = "TechVeons Contact Form Submission"
        msg['From'] = formataddr(("TechVeons Contact Form", EMAIL_ADDRESS))
        msg['To'] = EMAIL_ADDRESS
        msg['Reply-To'] = email

        app.logger.info(f"Sending email from {email} to {EMAIL_ADDRESS}")
        with smtplib.SMTP(EMAIL_SMTP_HOST, EMAIL_SMTP_PORT, timeout=20) as server:
            server.ehlo()
            server.starttls(context=SSL_CONTEXT)
            server.ehlo()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        app.logger.info("Email sent successfully")
        return jsonify(success=True, message="Email sent successfully."), 200

    except smtplib.SMTPAuthenticationError as e:
        app.logger.exception("Gmail SMTP authentication failed")
        return jsonify(success=False, message="Email authentication failed."), 500

    except smtplib.SMTPException as e:
        app.logger.exception("Gmail SMTP error")
        return jsonify(success=False, message="Email service error."), 500

    except Exception as e:
        app.logger.exception("Unexpected error in send route")
        return jsonify(success=False, message="Server error. Please try again later."), 500

@app.errorhandler(HTTPException)
def handle_http_exception(error):
    msg = getattr(error, 'description', 'HTTP error occurred')
    return jsonify(success=False, message=str(msg)), error.code

@app.errorhandler(Exception)
def handle_unhandled_exception(error):
    app.logger.exception("Unhandled exception occurred")
    return jsonify(success=False, message="Internal server error."), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
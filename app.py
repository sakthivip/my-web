import os
import requests
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
CORS(app)

SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "").strip()
SENDGRID_API_URL = "https://api.sendgrid.com/v3/mail/send"
SENDGRID_FROM_EMAIL = os.environ.get("SENDGRID_FROM_EMAIL", "").strip()
EMAIL_TO = "techveons.creation.official@gmail.com"


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

        if not SENDGRID_API_KEY:
            app.logger.error("SENDGRID_API_KEY not configured")
            return jsonify(success=False, message="Email service is not configured."), 500

        if not SENDGRID_FROM_EMAIL:
            app.logger.error("SENDGRID_FROM_EMAIL not configured")
            return jsonify(success=False, message="SendGrid sender email is not configured. Set SENDGRID_FROM_EMAIL to a verified sender identity."), 500

        email_body = (
            f"New contact form submission\n\n"
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Phone: {phone or 'N/A'}\n\n"
            f"Message:\n{message}\n"
        )

        payload = {
            "personalizations": [{"to": [{"email": EMAIL_TO}]}],
            "from": {"email": SENDGRID_FROM_EMAIL, "name": "TechVeons Contact Form"},
            "reply_to": {"email": email},
            "subject": "TechVeons Contact Form Submission",
            "content": [{"type": "text/plain", "value": email_body}]
        }

        headers = {
            "Authorization": f"Bearer {SENDGRID_API_KEY}",
            "Content-Type": "application/json"
        }

        app.logger.info(f"Sending email via SendGrid from {SENDGRID_FROM_EMAIL} to {EMAIL_TO}. Reply-To: {email}")
        response = requests.post(SENDGRID_API_URL, json=payload, headers=headers, timeout=10)

        if response.status_code == 202:
            app.logger.info(f"SendGrid accepted email (status 202) for {email}")
            return jsonify(success=True, message="Email sent successfully."), 200
        else:
            error_msg = response.text
            app.logger.error(f"SendGrid error: {response.status_code} - {error_msg}")
            return jsonify(success=False, message=f"Email service error: {error_msg}"), 500

    except requests.exceptions.RequestException as e:
        app.logger.exception(f"Request error: {str(e)}")
        return jsonify(success=False, message="Email service error."), 500

    except Exception as e:
        app.logger.exception(f"Unexpected error in send route: {str(e)}")
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
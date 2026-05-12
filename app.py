from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
CORS(app)

# Gmail Details
EMAIL_ADDRESS = "techveons.creation.official@gmail.com"
EMAIL_PASSWORD = "ezmm yfhz uyyy kwmg"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/send', methods=['POST'])
def send():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    message = data.get('message')
    
    body = f"""
    Name: {name}

    Email: {email}

    Phone: {phone}

    Message:
    {message}
    """

    msg = MIMEText(body)
    msg['Subject'] = "New Contact Form Submission"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS

    try:
        print("Attempting to send email...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully")
        return jsonify({"success": True, "message": "Email sent successfully"})
    except Exception as e:
        print(f"Email sending failed: {e}")
        return jsonify({"success": False, "message": f"Failed to send email: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
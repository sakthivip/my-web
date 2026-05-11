from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message

app = Flask(__name__)

# Gmail Details
EMAIL_ADDRESS = "techveons.creation.official@gmail.com"
EMAIL_PASSWORD = "ezmm yfhz uyyy kwmg"

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = EMAIL_ADDRESS
app.config['MAIL_PASSWORD'] = EMAIL_PASSWORD
app.config['MAIL_DEFAULT_SENDER'] = EMAIL_ADDRESS

mail = Mail(app)

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

    # For now, just return success without sending email
    # Email sending can be configured later
    return jsonify({"success": True, "message": "Message received successfully"})

if __name__ == '__main__':
    app.run(debug=True)
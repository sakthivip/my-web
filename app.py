from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_mail import Mail, Message

app = Flask(__name__)
CORS(app)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'techveons.creation.official@gmail.com'
app.config['MAIL_PASSWORD'] = 'ezmm yfhz uyyy kwmg'
app.config['MAIL_DEFAULT_SENDER'] = 'techveons.creation.official@gmail.com'

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
    
    body = f"""
    Name: {name}

    Email: {email}

    Phone: {phone}

    Message:
    {message}
    """

    msg = Message("New Contact Form Submission", recipients=['techveons.creation.official@gmail.com'])
    msg.body = body

    try:
        mail.send(msg)
        return jsonify({"success": True, "message": "Email sent successfully"})
    except Exception as e:
        print(f"Email error: {e}")
        return jsonify({"success": False, "message": "Failed to send email"})

if __name__ == '__main__':
    app.run(debug=True)
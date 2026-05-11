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
    print("SEND ROUTE WORKING")
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

    msg = Message("New Contact Form", recipients=[EMAIL_ADDRESS])
    msg.body = body

    try:
        mail.send(msg)
        return jsonify({"success": True, "message": "Email Sent Successfully"})
    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
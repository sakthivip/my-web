from flask import Flask, render_template, request, jsonify
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# Gmail Details
EMAIL_ADDRESS = "techveons.creation.official@gmail.com"
EMAIL_PASSWORD = "ezmm yfhz uyyy kwmg"

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

    msg = MIMEText(body)

    msg['Subject'] = "New Contact Form"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        server.send_message(msg)

        server.quit()

        return jsonify({"success": True, "message": "Email Sent Successfully"})
    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
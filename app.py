from flask import Flask, render_template, request
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# Gmail Details
EMAIL_ADDRESS = "techveons.ceation.official@gmail.com"
EMAIL_PASSWORD = "ezmm yfhz uyyy kwmg"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/send', methods=['POST'])
def send():

    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')

    body = f"""
    Name: {name}

    Email: {email}

    Subject: {subject}

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

        server.login("techveons.ceation.official@gmail.com", "ezmm yfhz uyyy kwmg")

        server.send_message(msg)

        server.quit()

        return "Email Sent Successfully"
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
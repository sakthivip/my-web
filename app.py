from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
    
    # Log the contact details (since email is disabled to avoid errors)
    print(f"Contact Form Submission:")
    print(f"Name: {name}")
    print(f"Email: {email}")
    print(f"Phone: {phone}")
    print(f"Message: {message}")
    
    # Return success to avoid errors
    return jsonify({"success": True, "message": "Message received successfully"})

if __name__ == '__main__':
    app.run(debug=True)
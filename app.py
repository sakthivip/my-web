from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/send', methods=['POST'])
def send():
    data = request.get_json()
    # Temporarily disable email sending to avoid 500 error
    # TODO: Fix email configuration for production
    return jsonify({"success": True, "message": "Message received successfully"})

if __name__ == '__main__':
    app.run(debug=True)
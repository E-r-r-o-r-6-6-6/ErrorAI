# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allows frontend from GitHub to access this API

@app.route('/api', methods=['POST'])
def respond():
    data = request.get_json()
    message = data.get('message', '')
    return jsonify({'reply': f"You said: {message}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

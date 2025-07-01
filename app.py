# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from g4f.client import Client

app = Flask(__name__)
CORS(app)

@app.route('/api', methods=['POST'])
def respond():
    data = request.get_json()
    usermessage = data.get('message', '')
    client = Client()
    response = client.chat.completions.create(
	    model = "gpt-4o-mini"
	    messages = [{"role":"user","content":f"{usermessage}"}]
	)
    reply = response.choices[0].message.content 
    return jsonify(reply)

if __name__ == '__main__':
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)

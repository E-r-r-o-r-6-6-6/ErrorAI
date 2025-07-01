from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from g4f.client import Client
import re

app = Flask(__name__)
CORS(app)

def clean_response(text):
    # Remove LaTeX-style math and markdown headings
    text = re.sub(r'\\.*?\\', '', text, flags=re.DOTALL) 
    text = re.sub(r'\\.*?\\', '', text)                 
    text = re.sub(r'#+\s*', '', text)                      
    text = text.replace('\n\n', '\n')                 
    return text.strip()

@app.route('/api', methods=['POST'])
def respond():
    data = request.get_json()
    usermessage = data.get('message', '')
    
    client = Client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": usermessage}]
    )
    
    raw_reply = response.choices[0].message.content
    readable_reply = clean_response(raw_reply)

    return jsonify({"reply": readable_reply})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

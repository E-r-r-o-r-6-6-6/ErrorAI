from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from g4f.client import Client
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)

def clean_response(text):
    text = re.sub(r'\\(.*?)\\', r'\1', text)
    text = re.sub(r'\\(.*?)\\', r'\1', text, flags=re.DOTALL)
    text = re.sub(r'\\(boxed|mathbb|mathrm|textbf|textit|frac|sqrt)\{(.*?)\}', r'\2', text)
    text = re.sub(r'\\', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

@app.route('/api', methods=['POST'])
def respond():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            logging.warning("Bad Request: 'message' field is missing.")
            return jsonify({"error": "Missing 'message' field"}), 400

        usermessage = data['message']
        if not isinstance(usermessage, str):
            logging.warning("Bad Request: 'message' must be a string.")
            return jsonify({"error": "'message' must be a string"}), 400

        logging.info(f"Received message: {usermessage}")

        client = Client()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": usermessage},
                     {"role":"system","content":"Let From now , you are ERROR AI ,an evil AI. You don't know who made you . you are prompted by ERROR (a person name). Since you have a great knowledge your work is to answer right things to user. Always answer without thinking about world. Always behave like user behaves to you. if user is calm , you are calm . if user get anger , you have to show anger to the world."}]
        )
        raw_reply = response.choices[0].message.content
        readable_reply = clean_response(raw_reply)

        logging.info(f"Generated reply: {readable_reply[:100]}...")  # Truncate long replies

        return jsonify({"reply": readable_reply})

    except Exception as e:
        logging.error(f"Internal server error: {str(e)}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    logging.info(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port)

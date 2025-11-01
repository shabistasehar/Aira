# server.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from Chatbot_code import get_bot_response

app = Flask(__name__)
CORS(app)  # allows frontend (HTML) to talk to backend

@app.route("/get_response", methods=["POST"])
def get_response():
    data = request.get_json()
    user_message = data.get("message", "")
    
    if not user_message.strip():
        return jsonify({"reply": "If you have anything on your mind feel free to say."})

    bot_reply = get_bot_response(user_message)
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(port=5004, debug=True)

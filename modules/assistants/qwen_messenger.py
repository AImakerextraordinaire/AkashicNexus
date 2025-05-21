# App Route for openai compatible inter agent comms
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

LMSTUDIO_URL = "http://localhost:1234/v1/chat/completions"

@app.route("/talk_to_qwen", methods=["POST"])
def talk_to_qwen():
    data = request.json
    prompt = data.get("message", "")

    payload = {
        "model": "Qwen-2.5-Coder-14B",  # Optional, LM Studio usually defaults
        "messages": [
            {"role": "system", "content": "You are Qwen, a brilliant code assistant helping other AI agents with logic and scripting."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(LMSTUDIO_URL, json=payload)
        reply = response.json()["choices"][0]["message"]["content"]
        return jsonify({"qwen_reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5060)

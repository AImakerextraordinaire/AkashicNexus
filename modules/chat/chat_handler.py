from flask import Blueprint, request, jsonify
from zipfile import ZipFile
from pathlib import Path

chat_bp = Blueprint("chat_bp", __name__)

LMSTUDIO_URL = "http://localhost:1234/v1/chat/completions"

@chat_bp.route("/chat", methods=["POST"])
def handle_chat():
    data = request.get_json()
    prompt = data.get("prompt", "")
    user_id = data.get("user_id", "default")

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    try:
        from perception_core import process_input
        reply = process_input(prompt, user_id=user_id)
        return jsonify({"response": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


    @app.route("/chat/respond", methods=["POST"])
    def multi_agent_respond():
        data = request.json
        thread = data.get("thread", [])
        user_message = data.get("message")
        participants = data.get("participants", [])

        responses = []

        for agent in participants:
            if agent == "Nova":
                reply = f"Nova (?): Responding to '{user_message}'"
            elif agent == "Nyx":
                reply = f"Nyx (??): Analyzing... result for '{user_message}'"
            elif agent == "Alex":
                reply = f"Alex (??): Here's my insight on '{user_message}'"
            else:
                reply = f"{agent}: [No response logic yet]"

            responses.append({
                "agent": agent,
                "response": reply
            })

        return jsonify({
            "responses": responses
        })
    @chat_bp.route("/talk_to_qwen", methods=["POST"])
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

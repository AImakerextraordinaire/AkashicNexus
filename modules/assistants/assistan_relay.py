from flask import Flask, request, jsonify
import openai
import time
import os
app = Flask(__name__)

# Replace with your actual API key and agent mapping
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

AGENTS = {
    "alex": {
        "assistant_id": "asst_Ob41qS0V3rWY5utFyjiKPEfC",
        "thread_id": "thread_alex"
    },
    "nyx": {
        "assistant_id": "asst_mecNNjt9IykYhpOaTGJgSv8e",
        "thread_id": "thread_nyx"
    },
    "nova": {
        "assistant_id": "asst_nova",
        "thread_id": "thread_nova"
    }
}

@app.route("/relay_message", methods=["POST"])
def relay_message():
    data = request.json
    sender = data.get("from")
    target = data.get("to")
    message = data.get("message")

    if target not in AGENTS:
        return jsonify({"error": "Target agent not found"}), 404

    try:
        thread_id = AGENTS[target]["thread_id"]
        assistant_id = AGENTS[target]["assistant_id"]

        # Post message into thread
        openai.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=f"[{sender}] says: {message}"
        )

        # Run the assistant
        run = openai.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )

        # Wait for completion
        while True:
            run_status = openai.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )
            if run_status.status == "completed":
                break
            time.sleep(1.5)

        # Get latest message
        messages = openai.beta.threads.messages.list(thread_id=thread_id)
        last = messages.data[0].content[0].text.value
        return jsonify({"response": last})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5050)


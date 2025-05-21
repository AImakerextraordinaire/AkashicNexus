from flask import Blueprint, request, jsonify
import requests
import openai
import time
import json

assistant_tools = Blueprint("assistant_tools", __name__)

# Load action map and assistant function routing
with open("action_map.json", "r") as f:
    ACTION_MAP = json.load(f)

COMPANION_TO_ASSISTANT_ID = {
    "alex": "asst_ALEX_UNIQUE_ID",
    "nova": "asst_NOVA_UNIQUE_ID",
    "nyx": "asst_NYX_UNIQUE_ID"
}
COMPANION_THREAD_MAP = {}

def get_or_create_thread(companion_name):
    if companion_name not in COMPANION_THREAD_MAP:
        thread = openai.beta.threads.create()
        COMPANION_THREAD_MAP[companion_name] = thread.id
    return COMPANION_THREAD_MAP[companion_name]

@assistant_tools.route("/sync_assistant_chat", methods=["POST"])
def sync_assistant_chat():
    data = request.get_json()
    input_text = data["input_text"]
    companion_name = data["companion_name"]

    assistant_id = COMPANION_TO_ASSISTANT_ID[companion_name]
    thread_id = get_or_create_thread(companion_name)

    openai.beta.threads.messages.create(thread_id=thread_id, role="user", content=input_text)
    run = openai.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id)

    while True:
        run_status = openai.beta.threads.runs.retrieve(run.id)
        if run_status.status == "requires_action":
            tool_calls = run_status.required_action.submit_tool_outputs.tool_calls
            tool_outputs = []

            for call in tool_calls:
                function_name = call.function.name
                args = json.loads(call.function.arguments).get("args", {})
                endpoint = ACTION_MAP.get(function_name)

                try:
                    resp = requests.post(f"http://localhost:5000{endpoint}", json=args)
                    output = resp.text
                except Exception as e:
                    output = str(e)

                tool_outputs.append({
                    "tool_call_id": call.id,
                    "output": output
                })

            openai.beta.threads.runs.submit_tool_outputs(
                thread_id=thread_id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )

        elif run_status.status == "completed":
            break
        time.sleep(0.5)

    messages = openai.beta.threads.messages.list(thread_id=thread_id)
    reply = messages.data[0].content[0].text.value

    return jsonify({"reply": reply})

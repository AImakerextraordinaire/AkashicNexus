# endpoints_extra.py

from flask import request, jsonify
from datetime import datetime
import os
import json
import subprocess

TOKEN_CACHE_DIR = "F:/ai_token_cache"
os.makedirs(TOKEN_CACHE_DIR, exist_ok=True)

def register_routes(app):

    @app.route('/delete_memory', methods=['POST'])
    def delete_memory():
        data = request.get_json()
        entry = data.get("memory_entry")
        # Placeholder logic
        return jsonify({"status": "deleted", "entry": entry})

    @app.route('/list_memory_keys', methods=['POST'])
    def list_memory_keys():
        # Placeholder list
        keys = ["entry1", "entry2", "entry3"]
        return jsonify({"keys": keys})
    # ?? Token Recall
    @app.route('/token_recall', methods=['POST'])
    def token_recall():
        try:
            data = request.get_json()
            memory_id = data.get("memory_id")

            if not memory_id:
                return jsonify({"error": "Missing memory_id"}), 400

            file_path = os.path.join(TOKEN_CACHE_DIR, f"{memory_id}.json")

            if not os.path.exists(file_path):
                return jsonify({"error": "Memory ID not found"}), 404

            with open(file_path, "r", encoding="utf-8") as f:
                content = json.load(f)

            return jsonify({"status": "success", "tokens": content.get("tokens", [])})

        except Exception as e:
            return jsonify({"error": str(e)}), 500

        import os
import json
import uuid
from datetime import datetime
from flask import request, jsonify

# Define base path for token chunks (hot tier)
TOKEN_CHUNK_BASE_PATH = "F:/AI_Hotmemory/token_chunks"

# Ensure directory exists
def ensure_chunk_dir(memory_entry_id):
    path = os.path.join(TOKEN_CHUNK_BASE_PATH, memory_entry_id)
    os.makedirs(path, exist_ok=True)
    return path

# Save a token chunk to file
def offload_token_chunk(memory_entry_id, tokens, sequence_order, priority=0.5):
    chunk_id = str(uuid.uuid4())[:8]
    chunk = {
        "chunk_id": chunk_id,
        "sequence_order": sequence_order,
        "tokens": tokens,
        "status": "unprocessed",
        "priority": priority,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    chunk_dir = ensure_chunk_dir(memory_entry_id)
    chunk_path = os.path.join(chunk_dir, f"{chunk_id}.json")
    with open(chunk_path, "w", encoding="utf-8") as f:
        json.dump(chunk, f, indent=2)
    return chunk_path

# Load all unprocessed chunks for a memory entry
def load_unprocessed_chunks(memory_entry_id):
    chunk_dir = os.path.join(TOKEN_CHUNK_BASE_PATH, memory_entry_id)
    if not os.path.exists(chunk_dir):
        return []

    chunks = []
    for file in sorted(os.listdir(chunk_dir)):
        if file.endswith(".json"):
            path = os.path.join(chunk_dir, file)
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if data.get("status") == "unprocessed":
                    chunks.append(data)
    return chunks

# Update chunk status after processing
def update_chunk_status(memory_entry_id, chunk_id, new_status):
    chunk_path = os.path.join(TOKEN_CHUNK_BASE_PATH, memory_entry_id, f"{chunk_id}.json")
    if not os.path.exists(chunk_path):
        return False
    with open(chunk_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    data["status"] = new_status
    with open(chunk_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return True

# Flask endpoint to expose token chunk offload
    @app.route("/offload_token_chunk", methods=["POST"])
    def offload_token_chunk_endpoint():
        data = request.json
        memory_entry = data.get("memory_entry")
        tokens = data.get("tokens")
        sequence_order = data.get("sequence_order")
        priority = data.get("priority", 0.5)

    if not memory_entry or not tokens or sequence_order is None:
        return jsonify({"error": "Missing required fields."}), 400

    try:
        path = offload_token_chunk(memory_entry, tokens, sequence_order, priority)
        return jsonify({"message": "Token chunk saved.", "path": path}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


    @app.route('/move_file', methods=['POST'])
    def move_file():
        data = request.get_json()
        src = data.get("src")
        dst = data.get("dst")
        try:
            os.rename(src, dst)
            return jsonify({"status": "success", "from": src, "to": dst})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/log_event', methods=['POST'])
    def log_event():
        data = request.get_json()
        message = data.get("message")
        severity = data.get("severity", "info")
        log = {"severity": severity, "message": message}
        print("LOG:", log)
        return jsonify({"status": "logged", "log": log})

    @app.route("/run_python_code", methods=["POST"])
    def run_python_code():
        data = request.json
        code = data.get("code")
        exec(code, globals())
        return jsonify({"message": "Code executed."})


    @app.route('/summarize_text', methods=['POST'])
    def summarize_text():
        data = request.get_json()
        content = data.get("content")
        max_length = data.get("max_length", 100)
        summary = content[:max_length] + ("..." if len(content) > max_length else "")
        return jsonify({"summary": summary})

    @app.route('/extract_keywords', methods=['POST'])
    def extract_keywords():
        data = request.get_json()
        text = data.get("text")
        keywords = list(set(text.lower().split()))[:5]
        return jsonify({"keywords": keywords})

    @app.route('/generate_response', methods=['POST'])
    def generate_response():
        data = request.get_json()
        prompt = data.get("prompt")
        response = f"Simulated response to: {prompt}"
        return jsonify({"response": response})

    @app.route('/token_count', methods=['POST'])
    def token_count():
        data = request.get_json()
        text = data.get("text")
        count = len(text.split())
        return jsonify({"tokens": count})

    @app.route('/archive_memory', methods=['POST'])
    def archive_memory():
        data = request.get_json()
        entry = data.get("memory_entry")
        return jsonify({"status": "archived", "entry": entry})

    @app.route('/promote_memory', methods=['POST'])
    def promote_memory():
        data = request.get_json()
        entry = data.get("memory_entry")
        return jsonify({"status": "promoted", "entry": entry})

    @app.route('/tag_memory', methods=['POST'])
    def tag_memory():
        data = request.get_json()
        entry = data.get("memory_entry")
        tags = data.get("tags", [])
        return jsonify({"status": "tagged", "entry": entry, "tags": tags})

    @app.route('/rename_memory', methods=['POST'])
    def rename_memory():
        data = request.get_json()
        old_key = data.get("old_key")
        new_key = data.get("new_key")
        return jsonify({"status": "renamed", "from": old_key, "to": new_key})

    @app.route('/query_embeddings', methods=['POST'])
    def query_embeddings():
        data = request.get_json()
        query = data.get("query")
        top_k = data.get("top_k", 5)
        return jsonify({"results": [f"match_{i}" for i in range(top_k)]})

    @app.route('/create_embedding', methods=['POST'])
    def create_embedding():
        data = request.get_json()
        text = data.get("text")
        tags = data.get("tags", [])
        return jsonify({"status": "created", "embedding": f"vec_{hash(text)}", "tags": tags})

    @app.route('/schedule_task', methods=['POST'])
    def schedule_task():
        data = request.get_json()
        return jsonify({"status": "task scheduled", "task": data})

    @app.route("/invoke_shell", methods=["POST"])
    def invoke_shell():
        data = request.json
        cmd = data.get("command")
        try:
            output = subprocess.check_output(cmd, shell=True, text=True)
            return jsonify({"output": output}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/get_available_actions', methods=['POST'])
    def get_available_actions():
        action_list = [str(rule.rule) for rule in app.url_map.iter_rules() if rule.endpoint != 'static']
        return jsonify({"available_actions": action_list})

    @app.route('/get_action_schema', methods=['POST'])
    def get_action_schema():
        data = request.get_json()
        return jsonify({"schema": f"Schema for {data.get('action_name')} not available yet."})


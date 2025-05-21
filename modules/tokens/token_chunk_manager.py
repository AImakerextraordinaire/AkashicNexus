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

# Offload a single chunk
def offload_token_chunk(memory_entry_id, chunk_data):
    ensure_chunk_dir(memory_entry_id)
    chunk_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat()

    chunk = {
        "id": chunk_id,
        "timestamp": timestamp,
        "tokens": chunk_data
    }

    path = os.path.join(TOKEN_CHUNK_BASE_PATH, memory_entry_id, f"{chunk_id}.json")
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(chunk, f, indent=2)

    return {"status": "offloaded", "chunk_id": chunk_id}

# Recall all chunks and stitch them into one list
def recall_token_chunks(memory_entry_id):
    path = os.path.join(TOKEN_CHUNK_BASE_PATH, memory_entry_id)
    if not os.path.exists(path):
        return {"status": "error", "message": "No chunks found."}

    chunks = []
    for filename in sorted(os.listdir(path)):
        if filename.endswith(".json"):
            with open(os.path.join(path, filename), 'r', encoding='utf-8') as f:
                chunk = json.load(f)
                chunks.extend(chunk.get("tokens", []))

    return {"status": "recalled", "reconstructed_tokens": chunks, "chunk_count": len(os.listdir(path))}

# Cascade offload (splits tokens and offloads)
def cascade_token_offload(memory_entry_id, full_token_list, chunk_size=500):
    total_chunks = (len(full_token_list) + chunk_size - 1) // chunk_size
    results = []

    for i in range(total_chunks):
        start = i * chunk_size
        end = start + chunk_size
        chunk_data = full_token_list[start:end]
        result = offload_token_chunk(memory_entry_id, chunk_data)
        results.append(result)

    return {"status": "cascaded", "total_chunks": total_chunks, "results": results}

# Endpoint: /offload_token_chunk

def register_token_chunk_endpoints(app):
    @app.route('/offload_token_chunk', methods=['POST'])
    def offload_chunk():
        data = request.get_json()
        memory_entry_id = data.get("memory_entry_id")
        tokens = data.get("tokens")

        if not memory_entry_id or not tokens:
            return jsonify({"error": "Missing required parameters."}), 400

        result = offload_token_chunk(memory_entry_id, tokens)
        return jsonify(result)

    @app.route('/recall_token_chunks', methods=['POST'])
    def recall_chunks():
        data = request.get_json()
        memory_entry_id = data.get("memory_entry_id")

        if not memory_entry_id:
            return jsonify({"error": "Missing memory_entry_id."}), 400

        result = recall_token_chunks(memory_entry_id)
        return jsonify(result)

    @app.route('/cascade_token_offload', methods=['POST'])
    def cascade_chunks():
        data = request.get_json()
        memory_entry_id = data.get("memory_entry_id")
        full_token_list = data.get("tokens")
        chunk_size = data.get("chunk_size", 500)

        if not memory_entry_id or not full_token_list:
            return jsonify({"error": "Missing required parameters."}), 400

        result = cascade_token_offload(memory_entry_id, full_token_list, chunk_size)
        return jsonify(result)


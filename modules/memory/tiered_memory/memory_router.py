import time
from . import tiered_memory_interface as tiered_memory
from flask import Blueprint, request, jsonify
import uuid
from .tiered_memory_interface import save_to_memory

memory_api = Blueprint('memory_api', __name__)

@memory_api.route("/store_memory", methods=["POST"])
def store_memory(content, tier="hot", tags=None, use_vector=False, metadata=None):
    try:
        data = request.get_json()
        content = data.get("content")
        tags = data.get("tags", [])
        tier = data.get("tier", "warm")
        use_vector = data.get("use_vector", False)
        metadata = data.get("metadata", {})

        if not content:
            return jsonify({"error": "Missing memory content"}), 400

        memory = {
            "memory_entry": str(uuid.uuid4()),
            "memory_content": content,
            "tier": tier,
            "tags": tags,
            "use_vector": use_vector,
            "metadata": metadata
        }

        success = save_to_memory(memory)

        if success:
            return jsonify({"status": "Memory stored"}), 200
        else:
            return jsonify({"error": "Failed to store memory"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@memory_api.route('/retrieve_memory', methods=['POST'])
def retrieve_memory():
    data = request.get_json()
    try:
        memory_id = data.get("memory_id")
        tier = data.get("tier", "hot")
        result = tiered_memory.retrieve_from_tier(memory_id, tier)
        return jsonify({"status": "success", "content": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@memory_api.route('/delete_memory', methods=['POST'])
def delete_memory():
    data = request.get_json()
    try:
        memory_id = data.get("memory_id")
        tier = data.get("tier", "hot")
        result = tiered_memory.delete_from_tier(memory_id, tier)
        return jsonify({"status": "success", "deleted": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@memory_api.route('/list_memory_keys', methods=['POST'])
def list_memory_keys():
    data = request.get_json()
    try:
        tier = data.get("tier", "hot")
        result = tiered_memory.list_keys_in_tier(tier)
        return jsonify({"status": "success", "keys": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@memory_api.route('/promote_memory', methods=['POST'])
def promote_memory():
    data = request.get_json()
    try:
        memory_id = data.get("memory_id")
        source_tier = data.get("from", "hot")
        destination_tier = data.get("to", "warm")
        result = tiered_memory.promote_memory(memory_id, source_tier, destination_tier)
        return jsonify({"status": "success", "result": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@memory_api.route('/tag_memory', methods=['POST'])
def tag_memory():
    data = request.get_json()
    try:
        memory_id = data.get("memory_id")
        tag = data.get("tag")
        tier = data.get("tier", "hot")
        result = tiered_memory.tag_memory(memory_id, tag, tier)
        return jsonify({"status": "success", "result": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@memory_api.route('/rename_memory', methods=['POST'])
def rename_memory():
    data = request.get_json()
    try:
        old_id = data.get("old_id")
        new_id = data.get("new_id")
        tier = data.get("tier", "hot")
        result = tiered_memory.rename_memory(old_id, new_id, tier)
        return jsonify({"status": "success", "result": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@memory_api.route('/archive_memory', methods=['POST'])
def archive_memory():
    data = request.get_json()
    try:
        memory_id = data.get("memory_id")
        source_tier = data.get("from", "hot")
        result = tiered_memory.archive_memory(memory_id, source_tier)
        return jsonify({"status": "success", "result": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@memory_api.route('/query_embeddings', methods=['POST'])
def query_embeddings():
    data = request.get_json()
    try:
        query = data.get("query")
        tier = data.get("tier", "hot")
        top_k = data.get("top_k", 5)
        result = tiered_memory.query_embeddings(query, tier, top_k)
        return jsonify({"status": "success", "results": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@memory_api.route('/create_embedding', methods=['POST'])
def create_embedding():
    data = request.get_json()
    try:
        memory_id = data.get("memory_id")
        content = data.get("content")
        tier = data.get("tier", "hot")
        result = tiered_memory.create_embedding(memory_id, content, tier)
        return jsonify({"status": "success", "result": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
1
from flask import Blueprint, request, jsonify
from .memory_router import store_memory, retrieve_memory, delete_memory, list_memory_keys, promote_memory, tag_memory, rename_memory, archive_memory, query_embeddings, create_embedding
import time
from .tiered_memory_interface import save_to_memory

memory_bp = Blueprint("memory_controller", __name__)

@memory_bp.route("/store_memory", methods=["POST"])
def store_memory():
    try:
        data = request.get_json()
        content = data.get("content")
        tags = data.get("tags", [])
        tier = data.get("tier", "warm")
        use_vector = data.get("use_vector", False)
        metadata = data.get("metadata", {})

        if not content:
            return jsonify({"error": "Missing memory content"}), 400

        success = save_to_memory(
            content=content,
            tags=tags,
            tier=tier,
            use_vector=use_vector,
            metadata=metadata
        )

        if success:
            return jsonify({"status": "Memory stored"}), 200
        else:
            return jsonify({"error": "Failed to store memory"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@memory_bp.route("/recall", methods=["POST"])
def retrieve_memory_route():
    try:
        data = request.get_json()
        query = data.get("query", "")
        tier = data.get("tier", "hot")
        top_k = int(data.get("top_k", 3))

        response = retrieve_memory(query, tier=tier, top_k=top_k)
        return jsonify({"status": "success", "result": response})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500
# chat_action_translator.py
from flask import Blueprint, request, jsonify
import requests

ACTION_MAP = {
  "vs_build_project": "/vs/project/build",
  "vs_solution_load": "/vs/solution/load",
  "vs_clean_project": "/vs/project/clean",
  "vs_rebuild_project": "/vs/project/rebuild",
  "vs_launch_vs": "/vs/launch_vs",
  "vs_open_project": "/vs/open_project",
  "vs_create_project": "/vs/create_project",
  "vs_list_projects": "/vs/list_projects",
  "vs_run_project": "/vs/run_project",
  "vs_commit_project": "/vs/commit_project",
  "vs_fetch_logs": "/vs/fetch_logs",
  "vs_open_file_location": "/vs/open_file_location",
  "vs_insert_snippet": "/vs/insert_snippet",
  "vs_search_replace": "/vs/search_replace",
  "vs_refresh_solution": "/vs/refresh_solution",
  "delete_memory": "/delete_memory",
  "list_memory_keys": "/list_memory_keys",
  "promote_memory": "/promote_memory",
  "tag_memory": "/tag_memory",
  "rename_memory": "/rename_memory",
  "archive_memory": "/archive_memory",
  "create_embeddings": "/create_embedding",
  "query_embeddings": "/query_embeddings",
  "query_embeddings": "/query_embeddings",
  "query_embeddings": "/query_embeddings",
  "query_embeddings": "/query_embeddings",
  "query_embeddings": "/query_embeddings",
  "create_file": "/create_file",
  "read_file": "/read_file",
  "append_file": "/append_file",
  "delete_file": "/delete_file",
  "create_directory": "create_directory",
  "search_files": "search_files"

  }

translator = Blueprint("translator", __name__)

@translator.route("/chat_action", methods=["POST"])
def chat_action():
    data = request.get_json()
    act  = data["action"]
    args = data.get("arguments", {})
    path = ACTION_MAP.get(act)
    if not path:
      return jsonify({"error": f"Unknown action {act}"}), 400
    resp = requests.post(f"http://localhost:5000{path}", json=args)
    return (resp.content, resp.status_code, resp.headers.items())

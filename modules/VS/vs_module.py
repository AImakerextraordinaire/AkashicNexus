from flask import Blueprint, request, jsonify
import subprocess
import os

vs_blueprint = Blueprint('vs_module', __name__)

# --- Existing routes (preserved) ---

@vs_blueprint.route('/vs/solution/load', methods=['POST'])
def load_solution():
    data = request.get_json()
    solution_path = data.get("solution_path")
    try:
        subprocess.run(["devenv", solution_path], check=True)
        return jsonify({"message": f"Loaded solution: {solution_path}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@vs_blueprint.route('/vs/project/build', methods=['POST'])
def build_project():
    data = request.get_json()
    solution_path = data.get("solution_path")
    try:
        result = subprocess.run(["devenv", solution_path, "/Build"], capture_output=True, text=True)
        return jsonify({"stdout": result.stdout, "stderr": result.stderr}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@vs_blueprint.route('/vs/project/clean', methods=['POST'])
def clean_project():
    data = request.get_json()
    solution_path = data.get("solution_path")
    try:
        result = subprocess.run(["devenv", solution_path, "/Clean"], capture_output=True, text=True)
        return jsonify({"stdout": result.stdout, "stderr": result.stderr}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@vs_blueprint.route('/vs/project/rebuild', methods=['POST'])
def rebuild_project():
    data = request.get_json()
    solution_path = data.get("solution_path")
    try:
        result = subprocess.run(["devenv", solution_path, "/Rebuild"], capture_output=True, text=True)
        return jsonify({"stdout": result.stdout, "stderr": result.stderr}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@vs_blueprint.route('/vs/launch_vs', methods=['POST'])
def launch_vs():
    try:
        subprocess.run(["devenv"], check=True)
        return jsonify({"message": "Launched Visual Studio."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@vs_blueprint.route('/vs/open_project', methods=['POST'])
def open_project():
    data = request.get_json()
    project_path = data.get("project_path")
    try:
        subprocess.run(["devenv", project_path], check=True)
        return jsonify({"message": f"Opened project: {project_path}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@vs_blueprint.route('/vs/create_project', methods=['POST'])
def create_project():
    data = request.get_json()
    project_name = data.get("project_name")
    directory = data.get("directory")
    try:
        full_path = os.path.join(directory, project_name)
        os.makedirs(full_path, exist_ok=True)
        with open(os.path.join(full_path, f"{project_name}.csproj"), 'w') as f:
            f.write("<Project Sdk=\"Microsoft.NET.Sdk\">")
        return jsonify({"message": f"Created project: {project_name} in {directory}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@vs_blueprint.route('/vs/list_projects', methods=['POST'])
def list_projects():
    data = request.get_json()
    directory = data.get("directory")
    try:
        projects = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".csproj"):
                    projects.append(os.path.join(root, file))
        return jsonify({"projects": projects}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@vs_blueprint.route('/vs/run_project', methods=['POST'])
def run_project():
    data = request.get_json()
    exe_path = data.get("executable_path")
    try:
        subprocess.Popen([exe_path], shell=True)
        return jsonify({"message": f"Running: {exe_path}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@vs_blueprint.route('/vs/commit_project', methods=['POST'])
def commit_project():
    data = request.get_json()
    repo_path = data.get("repo_path")
    message = data.get("commit_message")
    try:
        subprocess.run(["git", "-C", repo_path, "add", "."])
        subprocess.run(["git", "-C", repo_path, "commit", "-m", message])
        return jsonify({"message": f"Committed changes to {repo_path}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@vs_blueprint.route('/vs/fetch_logs', methods=['POST'])
def fetch_logs():
    data = request.get_json()
    log_path = data.get("log_path")
    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return jsonify({"logs": content}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- New Extensions ---

@vs_blueprint.route('/vs/open_file_location', methods=['POST'])
def open_file_location():
    data = request.get_json()
    filepath = data.get("filepath")
    line = data.get("line", 1)
    column = data.get("column", 1)
    try:
        subprocess.run(["devenv", filepath, f"/Command", f"Edit.GoTo {line}"], check=True)
        return jsonify({"message": f"Opened {filepath} at {line}:{column}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@vs_blueprint.route('/vs/insert_snippet', methods=['POST'])
def insert_snippet():
    data = request.get_json()
    filepath = data.get("filepath")
    marker = data.get("marker")
    snippet = data.get("snippet")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        content = content.replace(marker, marker + snippet)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return jsonify({"message": f"Snippet inserted at marker in {filepath}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@vs_blueprint.route('/vs/search_replace', methods=['POST'])
def search_replace():
    import re
    data = request.get_json()
    filepath = data.get("filepath")
    search_text = data.get("search_text")
    replace_text = data.get("replace_text")
    use_regex = data.get("regex", False)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        if use_regex:
            content = re.sub(search_text, replace_text, content)
        else:
            content = content.replace(search_text, replace_text)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return jsonify({"message": f"Replaced text in {filepath}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@vs_blueprint.route('/vs/refresh_solution', methods=['POST'])
def refresh_solution():
    try:
        subprocess.run(["devenv", "/RefreshSolution"], check=True)
        return jsonify({"message": "Solution refreshed."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

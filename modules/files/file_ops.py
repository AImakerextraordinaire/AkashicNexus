from flask import request, jsonify
import os
import uuid

chunk_store = {}


def register_file_ops(app):

    # Legacy File Ops
    @app.route('/read_file', methods=['POST'])
    def read_file():
        data = request.get_json()
        file_path = data.get('filepath')
        if not file_path:
            return jsonify({'error': 'No file path provided'}), 400
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return jsonify({'content': content}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/append_file', methods=['POST'])
    def append_file():
        data = request.get_json()
        file_path = data.get('filepath')
        content = data.get('content', '')
        if not file_path:
            return jsonify({'error':  'No file path provided'}), 400
        try:
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(content)
            return jsonify({'status': 'Content appended'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/modify_file', methods=['POST'])
    def modify_file():
        data = request.get_json()
        file_path = data.get('filepath')
        new_content = data.get('new_content', '')
        if not file_path:
            return jsonify({'error': 'No file path provided'}), 400
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return jsonify({'status': 'File modified'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/create_file', methods=['POST'])
    def create_file():
        data = request.get_json()
        file_path = data.get('filepath')
        content = data.get('content', '')
        if not file_path:
            return jsonify({'error': 'No file path provided'}), 400
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return jsonify({'status': 'File created'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/delete_file', methods=['POST'])
    def delete_file():
        data = request.get_json()
        file_path = data.get('filepath')
        if not file_path:
            return jsonify({'error': 'No file path provided'}), 400
        try:
            os.remove(file_path)
            return jsonify({'status': 'File deleted'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/create_directory', methods=['POST'])
    def create_directory():
        data = request.get_json()
        path = data.get('path')
        if not path:
            return jsonify({'error': 'No path provided'}), 400
        try:
            os.makedirs(path, exist_ok=True)
            return jsonify({'status': f'Directory created at {path}'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/scan_directory', methods=['POST'])
    def scan_directory():
        data = request.get_json()
        root_dir = data.get('path', 'C:\\AI\\Neuralforge_OS')  # Default fallback
        directory_tree = {}
        try:
            for dirpath, dirnames, filenames in os.walk(root_dir):
                rel_path = os.path.relpath(dirpath, root_dir)
                if rel_path == ".":
                    rel_path = root_dir
                directory_tree[rel_path] = {
                    "dirs": dirnames,
                    "files": filenames
                }
            return jsonify({"filesystem": directory_tree}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/search_files', methods=['POST'])
    def search_files():
        data = request.get_json()
        query = data.get('query', '*')
        root_dir = data.get('root_dir', 'C:\\')
        max_depth = int(data.get('max_depth', 5))
        matches = []
        try:
            root_depth = root_dir.strip(os.sep).count(os.sep)
            for dirpath, _, files in os.walk(root_dir):
                depth = dirpath.strip(os.sep).count(os.sep) - root_depth
                if depth > max_depth:
                    continue
                for file in files:
                    try:
                        if query == '*' or query.lower() in file.lower():
                            matches.append(os.path.join(dirpath, file))
                    except Exception:
                        continue
            return jsonify({'matches': matches}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # Chunked File Handler
    @app.route("/chunked/register", methods=["POST"])
    def register_chunk():
        data = request.get_json()
        file_path = data.get('filepath')
        chunk_size = int(data.get('chunk_size', 2000))

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            chunks = [content[i:i + chunk_size] for i in range(0, len(content), chunk_size)]
            chunk_id = str(uuid.uuid4())
            chunk_store[chunk_id] = chunks

            return jsonify({'chunk_id': chunk_id, 'chunk_count': len(chunks)}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/chunked/get', methods=['POST'])
    def get_chunk():
        data = request.get_json()
        chunk_id = data.get('chunk_id')
        index = int(data.get('index', 0))

        if chunk_id not in chunk_store:
            return jsonify({'error': 'Invalid chunk ID'}), 400

        chunks = chunk_store[chunk_id]
        if index >= len(chunks):
            return jsonify({'error': 'Chunk index out of range'}), 400

        return jsonify({'chunk': chunks[index]}), 200

    @app.route('/chunked/list', methods=['GET'])
    def list_chunks():
        return jsonify({'chunk_ids': list(chunk_store.keys())}), 200

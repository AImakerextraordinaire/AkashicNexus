import os
from flask import request, jsonify

HOT_MEMORY_PATH = "F:/AI_HotMemory"
WARM_MEMORY_PATH = "E:/AI_WarmMemory"
COLD_MEMORY_PATH = "P:/AI_ColdMemory"


def force_migrate(target_tier):
    logs = []

    try:
        if target_tier == "warm":
            hot_file_path = os.path.join(HOT_MEMORY_PATH, "memory_hot.mmap")
            warm_file_path = os.path.join(WARM_MEMORY_PATH, "memory_warm.mmap")
            logs.append(f"Reading from: {hot_file_path}")
            logs.append(f"Writing to: {warm_file_path}")

            with open(hot_file_path, "r") as hot_file:
                data = hot_file.read()
                logs.append(f"Read {len(data)} characters from hot memory.")

            with open(warm_file_path, "a") as warm_file:
                warm_file.write(data)
                logs.append("Successfully wrote to warm memory.")

            with open(hot_file_path, "w") as hot_file:
                hot_file.write("")
                logs.append("Cleared hot memory.")

            return {"message": "Migration to warm completed.", "log": logs}

        elif target_tier == "cold":
            warm_file_path = os.path.join(WARM_MEMORY_PATH, "memory_warm.mmap")
            cold_file_path = os.path.join(COLD_MEMORY_PATH, "memory_cold.mmap")
            logs.append(f"Reading from: {warm_file_path}")
            logs.append(f"Writing to: {cold_file_path}")

            with open(warm_file_path, "r") as warm_file:
                data = warm_file.read()
                logs.append(f"Read {len(data)} characters from warm memory.")

            with open(cold_file_path, "a") as cold_file:
                cold_file.write(data)
                logs.append("Successfully wrote to cold memory.")

            with open(warm_file_path, "w") as warm_file:
                warm_file.write("")
                logs.append("Cleared warm memory.")

            return {"message": "Migration to cold completed.", "log": logs}

        else:
            logs.append(f"Unknown target tier: {target_tier}")
            return {"error": f"Unknown target tier: {target_tier}", "log": logs}

    except Exception as e:
        logs.append(f"Error: {str(e)}")
        return {"error": str(e), "log": logs}

def register_tiered_memory_endpoint(app):
    @app.route('/trigger_decay_migrate', methods=['POST'])
    def trigger_decay_migrate():
        data = request.get_json()
        tier = data.get("target_tier", "warm")
        result = force_migrate(tier)
        return jsonify(result)
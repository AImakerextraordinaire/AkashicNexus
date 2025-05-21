from flask import request, jsonify
import requests

# Endpoint map (can be expanded)
ENDPOINT_MAP = {
    "create_file": "/create_file",
    "read_file": "/read_file",
    "append_file": "/append_file",
    "create_task": "/create_task",
    "trigger_tiers": "/sync_tiers",
    "token_offload": "/token_offload",  # Placeholder for mmap layer
    "token_recall": "/token_recall",
    "trigger_decay_migrate": "/trigger_decay_migrate"
}


class ActionDispatcher:
    def __init__(self):
        from AkashicPlaything import AkashicPlaything
        self.plaything = AkashicPlaything()
        self.actions = {
            # Core action examples...

            # 💫 NYX RUNTIME ENDPOINTS
            "nyx.get_status": lambda: self.plaything.get_nyx().get_status(),
            "nyx.suspend": lambda reason, timeout=None: self.plaything.get_nyx().suspend(reason, timeout),
            "nyx.reactivate": lambda: self.plaything.get_nyx().reactivate(),
            "nyx.write_journal": lambda entry, tags=None, permanent=False: self.plaything.get_nyx().write_journal(entry, tags, permanent),
            "nyx.search_journal": lambda query: self.plaything.get_nyx().search_journal(query),
            "nyx.set_mood": lambda mood: self.plaything.get_nyx().set_mood(mood),
            "nyx.reflect": lambda: self.plaything.get_nyx().reflect(),
            "nyx.add_goal": lambda title: self.plaything.get_nyx().add_goal(title),
            "nyx.pulse": lambda: self.plaything.get_nyx().pulse(),
        }

    def dispatch_action(self, base_url, action_name, arguments):
        endpoint = ENDPOINT_MAP.get(action_name)

        if endpoint:
            url = f"{base_url}{endpoint}"
        else:
            url = f"{base_url}/universal_action"
            arguments = {
                "action": action_name,
                "target_tier": "hot",  # default tier (can be adjusted)
                **arguments
            }

        try:
            print(f"[???] Dispatching {action_name} to {url}")
            response = requests.post(url, json=arguments)
            return response.json()
        except Exception as e:
            return {"status": "error", "error": str(e)}

    # 🛰️ Flask endpoint registration
    def register_action_dispatcher(self, app):
        @app.route("/action_dispatcher", methods=["POST"])
        def dispatch_to_core():
            try:
                data = request.get_json()
                base_url = data.get("base_url")
                action = data.get("action")
                arguments = data.get("arguments", {})

                if not base_url or not action:
                    return jsonify({"status": "error", "error": "Missing base_url or action"}), 400

                result = self.dispatch_action(base_url, action, arguments)
                return jsonify(result)

            except Exception as e:
                return jsonify({"status": "error", "error": str(e)}), 500
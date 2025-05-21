from flask import request, jsonify
from modules.system.input_emulator import send_keys, move_cursor, click
import os
import subprocess
import psutil


def register_system_tools(app):

    @app.route('/kairo_ping', methods=['GET'])
    def kairo_ping():
        return jsonify({"status": "online", "message": "Hello from your Flask API!"})

    @app.route('/run_command', methods=['POST'])
    def run_command():
        data = request.get_json()
        command = data.get('command')
        if not command:
            return jsonify({'error': 'No command provided'}), 400
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return jsonify({'stdout': result.stdout, 'stderr': result.stderr}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/kill_task', methods=['POST'])
    def kill_task():
        data = request.get_json()
        task_name = data.get('task_name')
        if not task_name:
            return jsonify({'error': 'No task_name provided'}), 400
        try:
            killed = 0
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] and task_name.lower() in proc.info['name'].lower():
                    proc.kill()
                    killed += 1
            return jsonify({'status': f'{killed} processes killed'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/system_stats', methods=['POST'])
    def system_stats():
        try:
            stats = {
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory': psutil.virtual_memory()._asdict(),
                'disk': psutil.disk_usage('/')._asdict(),
                'uptime': psutil.boot_time()
            }
            return jsonify({'stats': stats}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/system_health_check', methods=['POST'])
    def system_health_check():
        try:
            cpu = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage('/')

            status = 'healthy'
            if cpu > 90 or mem.percent > 90 or disk.percent > 90:
                status = 'critical'

            return jsonify({
                'cpu': cpu,
                'memory_percent': mem.percent,
                'disk_percent': disk.percent,
                'status': status
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/restart_server', methods=['POST'])
    def restart_server():
        try:
            if os.name == 'nt':
                os.system('shutdown /r /t 1')
            else:
                os.system('sudo reboot')
            return jsonify({'status': 'Restart triggered'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/urgent_task_check', methods=['POST'])
    def urgent_task_check():
        try:
            alerts = []
            cpu = psutil.cpu_percent(interval=1)
            if cpu > 85:
                alerts.append(f'High CPU usage: {cpu}%')

            mem = psutil.virtual_memory()
            if mem.percent > 85:
                alerts.append(f'High Memory usage: {mem.percent}%')

            disk = psutil.disk_usage('/')
            if disk.percent > 85:
                alerts.append(f'High Disk usage: {disk.percent}%')

            return jsonify({'alerts': alerts}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    @app.route("/run_python_code", methods=["POST"])
    def run_python_code():
        data = request.json
        code = data.get("code")
        try:
            exec(code, globals())
            return jsonify({"message": "Code executed successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/input", methods=["POST"])
    def simulate_input():
        data = request.json
        action = data.get("action")
        if action == "type":
            send_keys(data.get("text", ""))
        elif action == "move":
            move_cursor(data.get("x", 0), data.get("y", 0))
        elif action == "click":
            click()
        else:
            return jsonify({"status": "error", "message": "Unknown action"}), 400

        return jsonify({"status": "success"}), 200

    @app.route("/list_routes", methods=["GET"])
    def list_routes():
        routes = []
        for rule in app.url_map.iter_rules():
            if rule.endpoint != "static":
                routes.append({
                    "path": str(rule),
                    "methods": sorted([m for m in rule.methods if m in ["GET","POST","PUT","DELETE"]])
                })
        return jsonify(routes)

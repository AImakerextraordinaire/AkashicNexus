# speak_output_module.py

from flask import request, jsonify
import threading
import pyttsx3

# Initialize TTS engine
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 185)

def speak_text(text):
    print("[???] Speaking:", text)
    tts_engine.say(text)
    tts_engine.runAndWait()

def threaded_speak(text):
    thread = threading.Thread(target=speak_text, args=(text,), daemon=True)
    thread.start()

def register_speak_endpoint(app):
    @app.route('/speak', methods=['POST'])
    def speak():
        try:
            data = request.get_json()
            text = data.get("text")

            if not text:
                return jsonify({"error": "No 'text' field provided."}), 400

            threaded_speak(text)
            return jsonify({"status": "Speaking in background."})

        except Exception as e:
            print("[?] Error in /speak:", e)
            return jsonify({"error": str(e)}), 500


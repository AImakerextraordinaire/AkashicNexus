# stream_audio_module.py

import base64
import io
from flask import request, jsonify
from pydub import AudioSegment
from threading import Thread
import queue
import time
from modules.perception.speek_output import threaded_speak  # ? Needed for voice response

# Queues for audio processing
audio_queue = queue.Queue()

# Audio Processor Thread (with interpreter)
def audio_worker():
    from modules.perception.perception_core import interpret_audio  # ? Delayed import
    while True:
        audio_data = audio_queue.get()
        if audio_data is None:
            break

        print("[??] Processing audio chunk...")
        result = interpret_audio(audio_data)
        if result.get("status") == "processed":
            summary = result.get("transcript", "No transcript available.")
            if summary:
                threaded_speak(f"Heard: {summary[:100]}")
        else:
            threaded_speak("There was an error processing the audio.")

        audio_queue.task_done()
        time.sleep(0.1)

# Start the audio thread
audio_thread = Thread(target=audio_worker, daemon=True)
audio_thread.start()

def register_stream_audio_endpoint(app):
    @app.route('/stream_audio', methods=['POST'])
    def stream_audio():
        try:
            data = request.get_json()
            audio_base64 = data.get("audio_base64")

            if not audio_base64:
                return jsonify({"error": "No audio_base64 field provided."}), 400

            # Decode and load audio
            audio_bytes = base64.b64decode(audio_base64)
            audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format="wav")
            print("[??] Audio chunk received, duration:", len(audio), "ms")

            # Queue audio for processing
            audio_queue.put(audio)

            return jsonify({"status": "Audio chunk received and queued for processing."})

        except Exception as e:
            print("[?] Error in /stream_audio:", e)
            return jsonify({"error": str(e)}), 500

# stream_vision_module.py

import base64
import io
from flask import request, jsonify
from PIL import Image
from threading import Thread
import queue
import time

# Queues for perception processing
frame_queue = queue.Queue()

# Vision Processor Thread (placeholder for now)
def vision_worker():
    from modules.perception.perception_core import interpret_frame
    while True:
        frame_data = frame_queue.get()
        if frame_data is None:
            break

        # Simulate processing
        print("[???] Processing frame...")
        # Add computer vision stuff here in future (OCR, UI mapping, etc.)
        time.sleep(0.2)
        frame_queue.task_done()

# Start the vision thread
vision_thread = Thread(target=vision_worker, daemon=True)
vision_thread.start()

def register_stream_vision_endpoint(app):
    @app.route('/stream_vision', methods=['POST'])
    def stream_vision():
        try:
            data = request.get_json()
            image_data = data.get("image_base64")
            
            if not image_data:
                return jsonify({"error": "No image_base64 field provided."}), 400

            # Decode the image
            img_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(img_bytes))
            print("[??] Frame received, size:", image.size)

            # Send image to processing queue
            frame_queue.put(image)

            return jsonify({"status": "Frame received and queued for processing."})

        except Exception as e:
            print("[?] Error in /stream_vision:", e)
            return jsonify({"error": str(e)}), 500


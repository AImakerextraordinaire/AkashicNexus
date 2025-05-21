import time
from flask import jsonify
from modules.perception.vision_streamer import VisionStreamer

class NyxRuntime:
    def __init__(self):
        self.session_start = time.time()
        self.heartbeat = time.time()
        self.suspended = False
        self.reactivation_eta = None
        self.log = []
        self.mood = "Focused"
        self.journal = []
        self.goals = []

        # Vision
        self.vision_streamer = VisionStreamer()

    def start_vision_stream(self):
        try:
            print("[DEBUG] Triggering vision stream start...")
            self.vision_streamer.start()
            print(f"[DEBUG] Stream running state: {self.vision_streamer.running}")
            self.log.append("[VISION] Stream started")
            return {"status": "vision stream started", "running": self.vision_streamer.running}
        except Exception as e:
            print(f"[ERROR] Vision stream failed to start: {e}")
            return {"status": "error", "detail": str(e)}

    def stop_vision_stream(self):
        try:
            print("[DEBUG] Triggering vision stream stop...")
            self.vision_streamer.stop()
            self.log.append("[VISION] Stream stopped")
            return {"status": "vision stream stopped"}
        except Exception as e:
            print(f"[ERROR] Vision stream failed to stop: {e}")
            return {"status": "error", "detail": str(e)}
    

    # (rest of runtime unchanged...)
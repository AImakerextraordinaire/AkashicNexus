import threading
import time
import pygetwindow as gw
import mss
import numpy as np
import cv2
import pytesseract  # For OCR
from PIL import Image

# Optional: from transformers import BlipProcessor, BlipForConditionalGeneration (placeholder for future)

class VisionStreamer:
    def __init__(self, scale=0.5, fps=5, callback=None):
        self.running = False
        self.thread = None
        self.scale = scale
        self.fps = fps
        self.callback = callback
        self.window_name = "Nyx Vision Stream"

    def _get_blackout_region(self):
        try:
            win = gw.getWindowsWithTitle(self.window_name)[0]
            return win.left, win.top, win.width, win.height
        except IndexError:
            return None

    def _analyze_frame(self, frame):
        # Text extraction via OCR
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        pil_img = Image.fromarray(gray)
        text = pytesseract.image_to_string(pil_img)

        # Placeholder for future caption generation
        caption = "Screen frame captured."

        # Log/return combined analysis
        return {
            "frame_caption": caption,
            "text_read": text.strip(),
            "timestamp": time.time()
        }

    def _capture_loop(self):
        interval = 1 / self.fps
        with mss.mss() as sct:
            monitor = sct.monitors[1]

            while self.running:
                start_time = time.time()

                screenshot = sct.grab(monitor)
                frame = np.array(screenshot)

                region = self._get_blackout_region()
                if region:
                    x, y, w, h = region
                    frame[y:y+h, x:x+w] = 0  # Black out stream window region

                frame = cv2.resize(frame, (0, 0), fx=self.scale, fy=self.scale)

                analysis = self._analyze_frame(frame)
                print(f"[VISION] Analysis: {analysis['frame_caption']} | Text: {analysis['text_read'][:60]}...")

                if self.callback:
                    self.callback(frame, analysis)
                else:
                    cv2.imshow(self.window_name, frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        self.stop()

                elapsed = time.time() - start_time
                time.sleep(max(0, interval - elapsed))

        cv2.destroyAllWindows()

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._capture_loop, daemon=True)
            self.thread.start()
            print("[VISION] Stream started.")

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
            print("[VISION] Stream stopped.")

    def set_callback(self, callback):
        self.callback = callback
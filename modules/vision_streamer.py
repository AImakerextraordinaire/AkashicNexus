import threading
import time
import pyautogui
import cv2
import numpy as np

class VisionStreamer:
    def __init__(self, scale=0.5, fps=10, callback=None):
        self.running = False
        self.thread = None
        self.scale = scale
        self.fps = fps
        self.callback = callback
        self.blackout = True  

    def _capture_loop(self):
        interval = 1 / self.fps
        while self.running:
            start_time = time.time()

            if self.blackout:
                frame = np.zeros((480, 640, 3), dtype=np.uint8)
            else:
                screenshot = pyautogui.screenshot()
                frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                frame = cv2.resize(frame, (0, 0), fx=self.scale, fy=self.scale)

            if self.callback:
                self.callback(frame)
            else:
                cv2.imshow("Nyx Vision Stream", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.stop()

            elapsed = time.time() - start_time
            time.sleep(max(0, interval - elapsed))

        cv2.destroyAllWindows()

    def toggle_blackout(self, state: bool):
        self.blackout = True

    def start(self):
        if not self.running:
            self.running = True

            # ?? Display blackout window once
            blackout_frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.imshow("Nyx Vision Stream", blackout_frame)
            cv2.waitKey(1)  # Let it render at least one frame

            # ?? Then launch actual capture thread
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
    
# Example usage:
if __name__ == "__main__":
    streamer = VisionStreamer()
    streamer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        streamer.stop()
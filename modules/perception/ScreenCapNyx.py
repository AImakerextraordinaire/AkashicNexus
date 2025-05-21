import pyautogui
import numpy as np
import cv2

# Define screen size for capture (set to match display resolution)
screen_width, screen_height = pyautogui.size()

while True:
    # Capture the screen
    screenshot = pyautogui.screenshot()
    
    # Convert the screenshot to a NumPy array
    frame = np.array(screenshot)

    # Convert RGB to BGR (OpenCV uses BGR)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # Resize the frame (optional)
    frame = cv2.resize(frame, (screen_width // 2, screen_height // 2))

    # Show the screen capture
    cv2.imshow("Screen Capture", frame)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()


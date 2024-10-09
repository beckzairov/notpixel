import cv2
import time
import pyautogui
import numpy as np

def detect_and_click(image_path, timeout=7):
    """Detect an image and click on it if found, with retry mechanism."""
    start_time = time.time()  # Record the starting time

    # Continue trying to find the image until the timeout period is reached
    while True:
        # Take a screenshot
        screenshot = pyautogui.screenshot()
        img_rgb = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(image_path, 0)  # Load the image to detect
        w, h = template.shape[::-1]

        # Match template
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8  # Set a threshold for match quality
        loc = np.where(res >= threshold)

        # Check if any matches were found
        if len(loc[0]) > 0:  # If matches are found
            for pt in zip(*loc[::-1]):
                # Click the center of the detected image
                pyautogui.click(pt[0] + w // 2, pt[1] + h // 2)
                print(f"Clicked on {image_path} at position: ({pt[0] + w // 2}, {pt[1] + h // 2})")
                return True  # Image was found and clicked, so exit the function
        else:
            print(f"Image {image_path} not found. Retrying...")

        # Check if the timeout has been exceeded
        if time.time() - start_time > timeout:
            print(f"Timeout reached. {image_path} was not found within {timeout} seconds.")
            return False  # Exit if the timeout is reached

        time.sleep(0.5)  # Short delay before trying again
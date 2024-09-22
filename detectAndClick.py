import pyautogui
import time
from windowFocus import focus_app_by_executable
def detectAndClick(image_path, timeout=20, interval=0.5):
    focus_app_by_executable("telegram.exe")
    start_time = time.time()  # Record the start time
    while True:
        try:
            print("Waiting for image... ")
            # Locate the image on the screen
            location = pyautogui.locateOnScreen(image_path, confidence=0.8)

            if location:
                print(f"Found at: {location}")

                # Get the dimensions of the found image
                img_width = location.width
                img_height = location.height

                # Calculate the target position (right side of the image - 20 pixels)
                target_x = location.left + (img_width // 2)  # Move 15 pixels to the right of the image
                target_y = location.top + (img_height // 2)  # Vertically centered

                # Move the mouse to the target position
                pyautogui.moveTo(target_x, target_y)  # Instant movement
                pyautogui.click()  # Optional: Click at the target position
                break  # Exit the loop once the image is found and clicked

        except pyautogui.ImageNotFoundException:
            pass  # Simply ignore this exception and keep trying

        # Check if the timeout has been reached
        if time.time() - start_time > timeout:
            print("Timeout reached. Image not found.")
            break

        # Wait for a short interval before trying again
        time.sleep(interval)


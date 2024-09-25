import pyautogui
import time
import random
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

                # Calculate 80% of width and height
                usable_width = int(img_width * 0.95)
                usable_height = int(img_height * 0.95)

                # Determine the starting point for the random area
                start_x = location.left + (img_width - usable_width) // 2
                start_y = location.top + (img_height - usable_height) // 2

                # Generate a random pixel within the 80% area
                random_x = random.randint(start_x, start_x + usable_width - 1)
                random_y = random.randint(start_y, start_y + usable_height - 1)

                # Move the mouse to the random position and click
                pyautogui.moveTo(random_x, random_y, duration=0)  # Instant movement
                pyautogui.click()  # Click at the random position
                print(f"Clicked at: ({random_x}, {random_y})")
                break  # Exit the loop once the image is found and clicked

        except pyautogui.ImageNotFoundException:
            pass  # Simply ignore this exception and keep trying

        # Check if the timeout has been reached
        if time.time() - start_time > timeout:
            print("Timeout reached. Image not found.")
            break

        # Wait for a short interval before trying again
        time.sleep(interval)

detectAndClick(f"images/earn.png")
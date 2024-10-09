import pyautogui
import time
import random

def quitWebApp(image_path, sub_image_path, timeout=20, interval=0.5):
    start_time = time.time()  # Record the start time

    while True:
        try:
            print(f"Looking for main image: {image_path}")
            # Step 1: Locate the main image on the screen
            location = pyautogui.locateOnScreen(image_path, confidence=0.8)

            if location:
                print(f"Found main image at: {location}")

                # Step 2: Define the region of interest (ROI) for the secondary image (Close button)
                region = (location.left, location.top, location.width, location.height)

                print(f"Looking for close button in region: {region}")
                # Step 3: Try to locate the Close button image within the found main image region
                close_button_location = pyautogui.locateOnScreen(sub_image_path, region=region, confidence=0.8)

                if close_button_location:
                    print(f"Found close button at: {close_button_location}")

                    # Step 4: Calculate a random click position within the close button area
                    random_x = random.randint(close_button_location.left, close_button_location.left + close_button_location.width - 1)
                    random_y = random.randint(close_button_location.top, close_button_location.top + close_button_location.height - 1)

                    # Move the mouse to the random position within the "Close" button region
                    pyautogui.moveTo(random_x, random_y)
                    pyautogui.click()  # Click at the random position
                    print(f"Clicked at: ({random_x}, {random_y}) within the 'Close' button area.")
                    break  # Exit the loop once the image is found and clicked
                else:
                    print("Close button not found within main image. Retrying...")

        except Exception as e:
            print(f"Error: {e}")
            pass  # Continue trying

        # Check if the timeout has been reached
        if time.time() - start_time > timeout:
            print("Timeout reached. Image not found.")
            break

        # Wait for a short interval before trying again
        time.sleep(interval)

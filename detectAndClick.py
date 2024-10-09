import pyautogui
import time
import random

def detectAndClick(image_path, height=0.95, width=0.95, timeout=10, interval=1, cut_top_percentage=0):
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

                # Calculate the percentage of height to cut from the top
                cut_top_pixels = int(img_height * (cut_top_percentage / 100))

                # Calculate the usable area based on the height and width percentages
                usable_width = int(img_width * width)
                usable_height = int(img_height * height) - cut_top_pixels  # Reduce usable height by the cut percentage

                # Make sure the cut doesn't exceed the image height
                if usable_height <= 0:
                    print("Usable height is too small after applying cut_top_percentage. Skipping click.")
                    break

                # Adjust the starting point for random click area
                start_x = location.left + (img_width - usable_width) // 2
                start_y = location.top + cut_top_pixels  # Apply cut to the top

                # Generate a random pixel within the adjusted area
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

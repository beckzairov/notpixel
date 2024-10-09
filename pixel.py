import time
import random
import pyautogui
from windowFocus import focus_app_by_executable
from detectAndClick import detectAndClick

def get_random_coordinates_within_reduced_area(window, h_percent=60, w_percent=40):
    """Generate random coordinates within the symmetrically reduced area of the given window."""
    # Get the coordinates of the window
    x_start = window.rectangle().left
    y_start = window.rectangle().top
    width = window.rectangle().width()
    height = window.rectangle().height()

    # Calculate the symmetric reduced area dimensions
    # Reduce the width and height symmetrically from both sides
    width_reduction = width * (w_percent / 100) / 2
    height_reduction = height * (h_percent / 100) / 2

    x_start_reduced = int(x_start + width_reduction)  # Reduced start on x-axis
    x_end_reduced = int(x_start + width - width_reduction)  # Reduced end on x-axis

    y_start_reduced = int(y_start + height_reduction)  # Reduced start on y-axis
    y_end_reduced = int(y_start + height - height_reduction)  # Reduced end on y-axis

    # Generate random x and y within the reduced area
    random_x = random.randint(x_start_reduced, x_end_reduced)
    random_y = random.randint(y_start_reduced, y_end_reduced)

    return random_x, random_y

def random_click_in_reduced_window_area(window_title, function_to_call, h_percent=60, w_percent=40, click_interval=2, stop_after=None):
    """Perform random clicks within the reduced area of the window and call a function after each click."""
    window = focus_app_by_executable(window_title)  # Activate the web app window
    time.sleep(1)

    if not window:
        print(f"Cannot perform random clicks. Window titled '{window_title}' is not found or not active.")
        return

    click_count = 0
    stop_condition = False

    while not stop_condition:
        # Get random coordinates within the reduced area
        random_x, random_y = get_random_coordinates_within_reduced_area(window, h_percent, w_percent)

        # Perform the click at the random coordinates within the borders
        pyautogui.moveTo(random_x, random_y)
        print(f"Mouse moved to position: ({random_x}, {random_y}) within window: {window_title}")
        pyautogui.click()
        print(f"Clicked at position: ({random_x}, {random_y}) within window: {window_title}")

        # Call the provided function to detect the image
        stop_condition = function_to_call()

        # If timeout exceeded and image was not found, break the entire loop
        if stop_condition:
            print("Image detected, stopping the entire process.")
            break
        elif stop_condition is None:
            print("Timeout exceeded without finding the image, stopping the entire process.")
            break

        # Optional stop_after parameter to limit the number of clicks for testing
        if stop_after:
            click_count += 1
            if click_count >= stop_after:
                print("Stopping random clicker after reaching the limit.")
                break

        # Sleep for a defined interval before the next click
        time.sleep(click_interval)

# Updated function for detecting an image with a 5-second timeout
image_not_found_counter = 0
# Updated function for detecting an image with a 5-second timeout
def detect_and_click_image(timeout=5):
    global image_not_found_counter
    start_time = time.time()  # Record the start time

    print("Waiting for image...")  # Print this only once when detection starts

    # Attempt to find the image until timeout is exceeded
    while True:
        # Call the detectAndClick function, assuming it returns True if the image was clicked, False otherwise
        image_found = detectAndClick("images\\paint.png")

        if image_found:
            print("Image found and clicked.")
            image_not_found_counter = 0  # Reset the counter since the image was found
            return True  # Stop the random click loop

        # Check if timeout has been exceeded
        elapsed_time = time.time() - start_time
        if elapsed_time >= timeout:
            print(f"Timeout exceeded after {timeout} seconds. Image not found.")
            return None  # Return None to indicate timeout exceeded and no image found

        # Sleep a short interval before retrying
        time.sleep(0.5)


# Call the updated random clicker with reduced area logic
if __name__ == "__main__":
    random_click_in_reduced_window_area("telegram.exe", detect_and_click_image, h_percent=60, w_percent=40, click_interval=2, stop_after=10)

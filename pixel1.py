import random
import time
import pyautogui
from windowFocus import focus_app_by_executable
from detectAndClick import detectAndClick

def get_random_coordinates(window, h_percent=60, w_percent=65):
    """Generate random coordinates within the given window's boundaries."""
    x_start = window.rectangle().left
    y_start = window.rectangle().top
    width = window.rectangle().width()
    height = window.rectangle().height()
    
    x_end = x_start + int(width * (w_percent / 100))
    y_end = y_start + int(height * (h_percent / 100))
    
    random_x = random.randint(x_start, x_end)
    random_y = random.randint(y_start, y_end)
    
    return random_x, random_y

def random_click_in_window(window_title, function_to_call, click_interval=2, stop_after=None):
    """Perform random clicks within the web app window and call a function after each click."""
    window = focus_app_by_executable(window_title)  # Activate the web app window
    time.sleep(1)
    
    if not window:
        print(f"Cannot perform random clicks. Window titled '{window_title}' is not found or not active.")
        return
    
    click_count = 0
    stop_condition = False

    while not stop_condition:
        random_x, random_y = get_random_coordinates(window)
        
        # Perform the click at the random coordinates
        pyautogui.click(random_x, random_y)
        print(f"Clicked at position: ({random_x}, {random_y}) within window: {window_title}")
        
        # Call the provided function
        stop_condition = function_to_call()

        if stop_after:
            click_count += 1
            if click_count >= stop_after:
                print("Stopping random clicker after reaching the limit.")
                break

        # Sleep for a defined interval before the next click
        time.sleep(click_interval)

image_not_found_counter = 0
# Example function for detecting and clicking an image with retries
def detect_and_click_image(retries=5, timeout=5):
    global image_not_found_counter
    start_time = time.time()  # Record the start time

    # Retry mechanism: attempt to find the image multiple times or within the time limit
    for attempt in range(retries):
        # Call the detectAndClick function, assuming it returns True if the image was clicked, False otherwise
        image_found = detectAndClick("images\\paint.png")

        if image_found:
            print(f"Image found and clicked on attempt {attempt + 1}")
            image_not_found_counter = 0  # Reset the counter since the image was found
            return False  # Continue the random click loop

        # If the image was not found, increase the counter and check if timeout is exceeded
        image_not_found_counter += 1
        elapsed_time = time.time() - start_time
        print(f"waiting for image... ({image_not_found_counter} attempts, {elapsed_time:.2f}s elapsed)")

        # Check if timeout has been exceeded
        if elapsed_time >= timeout:
            print(f"Timeout exceeded after {timeout} seconds.")
            break

        # Sleep a short interval between retries
        time.sleep(0.5)

    # If the image wasn't found after retries or the timeout, stop the loop
    print(f"Stopping after {retries} attempts or {timeout} seconds.")
    return True  # Stop the random click loop

# Call random clicker with the updated logic and retry mechanism

detect_and_click_image()
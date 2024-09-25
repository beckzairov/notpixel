import cv2
import pyautogui
import numpy as np
import time
import pygetwindow as gw

# Set image path for template
template_path = f"images\\start-asus.png"

# Function to detect image on the screen
def detect_and_click_image(template_path):
    # Capture screenshot
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Load template image
    template = cv2.imread(template_path, 0)

    # Debug: Save the screenshot to check if it matches the template
    cv2.imwrite(f"images\\debug_screenshot.png", screenshot_gray)

    # Match template
    res = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.7  # Adjust threshold for more sensitivity
    loc = np.where(res >= threshold)

    # If image is found, click on the center
    if len(loc[0]) > 0:
        # Get center point of the matched region
        top_left = (loc[1][0], loc[0][0])
        width, height = template.shape[::-1]
        center_x = top_left[0] + width // 2
        center_y = top_left[1] + height // 2
        
        # Click the center of the image
        pyautogui.click(center_x, center_y)
        print(f"Clicked on image at ({center_x}, {center_y})")
        return True
    else:
        print("No image found")
        return False

# Function to scroll the window
def scroll_down():
    # Scroll down using pyautogui
    pyautogui.scroll(-100)  # Adjust scroll amount as needed
    print("Scrolled down")

# Main function to run the detection and click loop
def run_detection_cycle(template_path, original_window_title):
    while True:
        # Detect and click on image
        found = detect_and_click_image(template_path)
        
        if found:
            print("Image detected and clicked.")
        else:
            # Scroll down if no image found
            scroll_down()

        # Add a small delay to avoid excessive CPU usage
        time.sleep(1)

# Get the title of the original window
original_window = gw.getWindowsWithTitle('TelegramDesktop')[0]

# Run the detection loop
run_detection_cycle(template_path, original_window.title)

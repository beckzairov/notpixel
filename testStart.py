import cv2
import pyautogui
import numpy as np
import time
import pygetwindow as gw
from pywinauto.application import Application
import win32gui

# Set image path for template
template_path = 'path_to_image_template.png'

# Function to detect image on the screen
def detect_and_click_image(template_path):
    # Capture screenshot
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Load template image
    template = cv2.imread(template_path, 0)

    # Match template
    res = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8  # Set a threshold for image matching
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

# Function to close browser tab and refocus on the original window
def close_browser_and_refocus(original_window_title):
    time.sleep(2)  # Give time for the browser tab to open
    
    # Get all windows
    windows = gw.getWindowsWithTitle('')
    
    # Find and close the browser window
    for window in windows:
        if 'Google Chrome' in window.title or 'Firefox' in window.title:  # Adjust for your browser
            print(f"Closing browser window: {window.title}")
            window.close()
            break
    
    # Refocus on the original window
    original_window = gw.getWindowsWithTitle(original_window_title)[0]
    if original_window:
        original_window.activate()
        print(f"Refocused on original window: {original_window_title}")

# Function to scroll the window
def scroll_down():
    # Scroll down using pyautogui
    pyautogui.scroll(-500)  # Adjust scroll amount as needed
    print("Scrolled down")

# Main function to run the detection and click loop
def run_detection_cycle(template_path, original_window_title):
    while True:
        # Detect and click on image
        found = detect_and_click_image(template_path)
        
        if found:
            # Close browser tab and refocus
            close_browser_and_refocus(original_window_title)
        else:
            # Scroll down if no image found
            scroll_down()

        # Add a small delay to avoid excessive CPU usage
        time.sleep(1)

# Get the title of the original window
original_window = gw.getWindowsWithTitle('Your Original Window Title')[0]

# Run the detection loop
run_detection_cycle(template_path, original_window.title)

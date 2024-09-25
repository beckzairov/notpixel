import cv2
import pyautogui
import numpy as np
import time

# Set image path for template
template_path = f"images\\claim-asus.png"

# Function to detect and click on all instances of an image
def detect_and_click_images(template_path):
    # Capture screenshot (optimized to capture a region, not the entire screen)
    screen_width, screen_height = pyautogui.size()
    region = (0, 0, screen_width, int(screen_height * 0.8))  # Focus on top 80% of the screen
    screenshot = pyautogui.screenshot(region=region)
    screenshot = np.array(screenshot)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Load template image
    template = cv2.imread(template_path, 0)
    
    # Multi-scale template matching to handle size variations
    found_any = False
    for scale in np.linspace(0.7, 1.3, 20):  # Varying template size from 70% to 130%
        resized_template = cv2.resize(template, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
        res = cv2.matchTemplate(screenshot_gray, resized_template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)

        # If multiple locations found, click all of them
        for pt in zip(*loc[::-1]):  # Loop through all detected points
            found_any = True
            top_left = pt
            width, height = resized_template.shape[::-1]
            center_x = top_left[0] + width // 2
            center_y = top_left[1] + height // 2
            
            # Adjust coordinates since we captured a region of the screen
            pyautogui.click(center_x, center_y)
            print(f"Clicked on image at ({center_x}, {center_y})")

    return found_any

# Function to scroll the window dynamically
def scroll_down():
    # Check if scrolling reached the bottom by comparing window size and mouse position
    screen_height = pyautogui.size()[1]
    current_mouse_position = pyautogui.position()[1]
    
    if current_mouse_position > screen_height - 50:  # Near the bottom
        print("Reached the bottom of the page, no further scrolling possible")
        return False
    else:
        pyautogui.scroll(-100)  # Adjust scroll amount dynamically if needed
        print("Scrolled down")
        return True

# Main function to run the detection and click loop
def run_detection_cycle(template_path):
    while True:
        # Detect and click on all instances of the image
        found = detect_and_click_images(template_path)
        
        if not found:
            # Scroll down if no image found
            can_scroll = scroll_down()
            if not can_scroll:
                break  # Stop if there's no more room to scroll

        # Small sleep can be added here to avoid performance issues
        time.sleep(0.2)

# Run the detection loop
run_detection_cycle(template_path)

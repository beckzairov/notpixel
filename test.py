import cv2
import pyautogui
import numpy as np
import time
import pygetwindow as gw
from pywinauto.application import Application

# Set image paths for button templates
claim_button_path = 'claim-asus.png'
verify_button_path = 'verify-asus.png'
start_button_white_path = 'start-white-asus.png'
start_button_black_path = 'start-asus.png'

# Function to refocus on the main window if it loses focus
def refocus_on_main_window(window_title):
    window = gw.getWindowsWithTitle(window_title)
    if window:
        if not window[0].isActive:
            print(f"Refocusing on window: {window_title}")
            window[0].activate()
        return window[0]
    return None

# Function to detect and click only the claim buttons (skip verify and start buttons)
def detect_and_click_claim_buttons(claim_button_path, verify_button_path, start_button_white_path, start_button_black_path, window):
    # Capture screenshot of the window (not the whole screen)
    screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
    screenshot = np.array(screenshot)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Load the claim, verify, and start button templates
    claim_template = cv2.imread(claim_button_path, 0)
    verify_template = cv2.imread(verify_button_path, 0)
    start_template_white = cv2.imread(start_button_white_path, 0)
    start_template_black = cv2.imread(start_button_black_path, 0)

    # Match templates for claim, verify, and both start buttons
    claim_res = cv2.matchTemplate(screenshot_gray, claim_template, cv2.TM_CCOEFF_NORMED)
    verify_res = cv2.matchTemplate(screenshot_gray, verify_template, cv2.TM_CCOEFF_NORMED)
    start_res_white = cv2.matchTemplate(screenshot_gray, start_template_white, cv2.TM_CCOEFF_NORMED)
    start_res_black = cv2.matchTemplate(screenshot_gray, start_template_black, cv2.TM_CCOEFF_NORMED)

    # Set thresholds for image matching
    claim_threshold = 0.8
    verify_threshold = 0.8
    start_threshold_white = 0.8
    start_threshold_black = 0.8

    # Find the claim button locations
    claim_loc = np.where(claim_res >= claim_threshold)

    # Find the verify button locations (for ignoring)
    verify_loc = np.where(verify_res >= verify_threshold)

    # Find the white start button locations (for ignoring)
    start_loc_white = np.where(start_res_white >= start_threshold_white)

    # Find the black start button locations (for ignoring)
    start_loc_black = np.where(start_res_black >= start_threshold_black)

    # Track whether we found any claim buttons
    found_any_claims = False

    # Loop through all detected claim button locations
    for pt in zip(*claim_loc[::-1]):
        top_left = pt
        width, height = claim_template.shape[::-1]
        center_x = window.left + top_left[0] + width // 2
        center_y = window.top + top_left[1] + height // 2

        # Check if the detected claim button overlaps with verify or start buttons
        claim_is_valid = True

        # Check verify button overlap
        for verify_pt in zip(*verify_loc[::-1]):
            if abs(verify_pt[0] - top_left[0]) < width and abs(verify_pt[1] - top_left[1]) < height:
                print("Verify button detected near the claim button, skipping this one.")
                claim_is_valid = False
                break

        # Check white start button overlap
        for start_pt_white in zip(*start_loc_white[::-1]):
            if abs(start_pt_white[0] - top_left[0]) < width and abs(start_pt_white[1] - top_left[1]) < height:
                print("White start button detected near the claim button, skipping this one.")
                claim_is_valid = False
                break

        # Check black start button overlap
        for start_pt_black in zip(*start_loc_black[::-1]):
            if abs(start_pt_black[0] - top_left[0]) < width and abs(start_pt_black[1] - top_left[1]) < height:
                print("Black start button detected near the claim button, skipping this one.")
                claim_is_valid = False
                break

        # If no overlap with verify or start buttons, click the claim button
        if claim_is_valid:
            pyautogui.click(center_x, center_y)
            print(f"Clicked on claim button at ({center_x}, {center_y})")
            found_any_claims = True

    return found_any_claims

# Function to scroll down the window
def scroll_down(window):
    pyautogui.moveTo(window.left + window.width // 2, window.top + window.height // 2)  # Move cursor to the window's center
    pyautogui.scroll(-500)  # Scroll down
    print("Scrolled down")

# Function to scroll up the window
def scroll_up(window):
    pyautogui.moveTo(window.left + window.width // 2, window.top + window.height // 2)  # Move cursor to the window's center
    pyautogui.scroll(500)  # Scroll up
    print("Scrolled up")

# Main function to run the image detection and claim-clicking loop
def run_claim_clicker(claim_button_path, verify_button_path, start_button_white_path, start_button_black_path, main_window_title):
    # Get the main window
    main_window = refocus_on_main_window(main_window_title)
    if not main_window:
        print(f"Main window '{main_window_title}' not found!")
        return
    
    while True:
        # Ensure focus on the main window
        refocus_on_main_window(main_window_title)

        # Detect and click claim buttons (while ignoring verify/start buttons)
        found_any_claims = detect_and_click_claim_buttons(claim_button_path, verify_button_path, start_button_white_path, start_button_black_path, main_window)

        # If no claim buttons were found, scroll down and search again
        if not found_any_claims:
            scroll_down(main_window)
            time.sleep(1)
            continue

        # Scroll back up to check if any claims were missed above
        scroll_up(main_window)
        time.sleep(1)
        # Try finding the claim buttons again after scrolling up
        found_any_claims = detect_and_click_claim_buttons(claim_button_path, verify_button_path, start_button_white_path, start_button_black_path, main_window)

        # Stop condition: No claims found and scrolled through everything
        if not found_any_claims:
            print("No claim buttons left!")
            break

# Example usage inside your larger script:
main_window_title = "TelegramDesktop"
run_claim_clicker(claim_button_path, verify_button_path, start_button_white_path, start_button_black_path, main_window_title)

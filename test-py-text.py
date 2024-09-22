import pytesseract
import pyautogui
import time
import cv2
import numpy as np
import pygetwindow as gw
from pywinauto.application import Application

# Set the path to tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Function to refocus on the main window if it loses focus
def refocus_on_main_window(window_title):
    window = gw.getWindowsWithTitle(window_title)
    if window:
        if not window[0].isActive:
            print(f"Refocusing on window: {window_title}")
            window[0].activate()
        return window[0]
    return None

# Function to extract text from the screenshot using OCR
def extract_text_from_screenshot(window):
    # Capture screenshot of the window (not the whole screen)
    screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
    screenshot_np = np.array(screenshot)

    # Convert screenshot to grayscale for better OCR results
    screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)

    # Use Tesseract OCR to extract text
    extracted_text = pytesseract.image_to_string(screenshot_gray)

    # Clean up non-UTF-8 characters by encoding and decoding properly
    try:
        # This ensures that non-UTF-8 characters are removed or replaced
        cleaned_text = extracted_text.encode('utf-8', 'replace').decode('utf-8')
    except UnicodeDecodeError:
        # Fallback in case there's any further decoding issue
        cleaned_text = extracted_text.encode('ascii', 'ignore').decode('ascii')
    
    return cleaned_text

# Function to detect and click on buttons with specific text ("Claim")
def detect_and_click_by_text(window, target_text='Claim'):
    extracted_text = extract_text_from_screenshot(window)
    
    # Search for the target text (case-sensitive match)
    if target_text in extracted_text:
        print(f"Found '{target_text}' in the window. Clicking button...")
        
        # Detect the location of the target text using bounding boxes
        boxes = pytesseract.image_to_boxes(extract_text_from_screenshot(window))
        
        for b in boxes.splitlines():
            b = b.split()
            if b[0] == target_text:
                # Coordinates of the box containing the text
                left, top, right, bottom = int(b[1]), int(b[2]), int(b[3]), int(b[4])
                # In PyAutoGUI, the origin (0,0) is at the top left, but for Tesseract it’s inverted
                top = window.height - top
                bottom = window.height - bottom

                # Click at the center of the bounding box for the claim button
                center_x = window.left + left + (right - left) // 2
                center_y = window.top + bottom + (top - bottom) // 2
                
                # Perform the click
                pyautogui.click(center_x, center_y)
                print(f"Clicked on '{target_text}' at ({center_x}, {center_y})")
                return True  # Successfully clicked
    else:
        print(f"'{target_text}' not found in the current view.")
    
    return False  # No target text found

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

# Main function to run the detection and claim-clicking loop based on text detection
def run_claim_clicker_by_text(main_window_title, target_text='Claim'):
    # Get the main window
    main_window = refocus_on_main_window(main_window_title)
    if not main_window:
        print(f"Main window '{main_window_title}' not found!")
        return
    
    while True:
        # Ensure focus on the main window
        refocus_on_main_window(main_window_title)

        # Detect and click "Claim" buttons based on text (ignoring others like "Start")
        found_claim = detect_and_click_by_text(main_window, target_text=target_text)

        # If no claim buttons were found, scroll down and search again
        if not found_claim:
            scroll_down(main_window)
            time.sleep(1)
            continue

        # Scroll back up to check if any claims were missed above
        scroll_up(main_window)
        time.sleep(1)
        # Try finding the claim buttons again after scrolling up
        found_claim = detect_and_click_by_text(main_window, target_text=target_text)

        # Stop condition: No claims found and scrolled through everything
        if not found_claim:
            print("No claim buttons left!")
            break

# Example usage inside your larger script:
main_window_title = "TelegramDesktop"
run_claim_clicker_by_text(main_window_title, target_text='Claim')

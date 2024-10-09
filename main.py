import os
import cv2
import time
import subprocess
import pyautogui  # For mouse control and screenshots
import psutil  # To manage processes
import numpy as np
import pygetwindow as gw
from quitWebApp import quitWebApp
from detectAndClick import detectAndClick
from windowFocus import focus_app_by_executable

from pixel import *

ROOT_FOLDER = "D:\\Tgs\\Abd\\11acc-13sep"  # Set your root folder path
TELEGRAM_LINK = "https://t.me/dogs_ref_group/73"  # The link to open in Telegram

def wait_for_image(image_path, timeout=20, interval=0.5):
    """Wait for an image to appear on screen with a dynamic timeout."""
    start_time = time.time()  # Record the start time

    while True:
        if detect_and_click(image_path, timeout=interval):  # Try finding the image every `interval` seconds
            return True  # Image found and clicked
        
        # Check if timeout has been exceeded
        if time.time() - start_time > timeout:
            print(f"Timeout reached. {image_path} not found within {timeout} seconds.")
            return False  # Image not found within the given timeout

        time.sleep(interval)

def open_telegram(folder_path):
    """Open telegram.exe from the specified folder."""
    telegram_path = os.path.join(folder_path, "telegram.exe")
    subprocess.Popen(telegram_path)
    time.sleep(5) 

def open_telegram_link(link):
    """Open the specified Telegram link."""
    pyautogui.typewrite(link)  # Type the link in the chat input
    pyautogui.press('enter')    # Press Enter to navigate to the link
    print("link opened")
    time.sleep(5)  # Wait for the link to open

def detect_and_click(image_path, timeout=7):
    """Detect an image and click on it if found, with retry mechanism."""
    start_time = time.time()  # Record the starting time

    # Continue trying to find the image until the timeout period is reached
    while True:
        # Take a screenshot
        screenshot = pyautogui.screenshot()
        img_rgb = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(image_path, 0)  # Load the image to detect
        w, h = template.shape[::-1]

        # Match template
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8  # Set a threshold for match quality
        loc = np.where(res >= threshold)

        # Check if any matches were found
        if len(loc[0]) > 0:  # If matches are found
            for pt in zip(*loc[::-1]):
                # Click the center of the detected image
                pyautogui.click(pt[0] + w // 2, pt[1] + h // 2)
                print(f"Clicked on {image_path} at position: ({pt[0] + w // 2}, {pt[1] + h // 2})")
                return True  # Image was found and clicked, so exit the function
        else:
            print(f"Image {image_path} not found. Retrying...")

        # Check if the timeout has been exceeded
        if time.time() - start_time > timeout:
            print(f"Timeout reached. {image_path} was not found within {timeout} seconds.")
            return False  # Exit if the timeout is reached

        time.sleep(0.5)  # Short delay before trying again

def close_application(app_name):
    """Close an application by name."""
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        if proc.info['name'].lower() == app_name.lower():
            print(f"Terminating {proc.info['name']} with PID: {proc.info['pid']}")
            proc.terminate()  # Gracefully terminate the process
            proc.wait()  # Wait for the process to terminate
            print(f"{proc.info['name']} terminated.")
            return
    print(f"No process found with name: {app_name}")

def process_folder(folder_path):
    """Process a single Telegram clone folder."""
    open_telegram(folder_path)
    focus_app_by_executable("telegram.exe")

    # Detect and click on the specified image before opening the link
    target_image_path = f"images\\cancel.png"  # Path to the image to detect
    detect_and_click(target_image_path, timeout=5)  # Detect and click the image

    open_telegram_link(TELEGRAM_LINK)  # Open the specified link

    # Find and click the link after it has been opened
    link_image_path = f"images\\link-to-ref.png"  # Path to the link template image
    detectAndClick(link_image_path, cut_top_percentage=30)  # Find and click the link
    
    # focus_app_by_executable("telegram.exe")
    ref_image = f"images\\ref.png"  # Path to the link template image
    detectAndClick(ref_image)  # Find and click the link

    detect_and_click(f"images\\ok-modal.png", timeout=5)
    # time.sleep(3)
    
    detect_and_click(f"images\\promise.png", timeout=5)
    
    detect_and_click(f"images\\letsgo.png", timeout=2.5)
    # if not wait_for_image(f"images\\goback.png", timeout=20):
    #     print("Web app did not load properly. Exiting.")
    #     return
    # detect_and_click(f"images\\goback.png", timeout=5)
    quitWebApp("images\\blankscreenwait.png", "images\\kebapmenu.png")
    detect_and_click(f"images\\reload.png", timeout=2.5)


    random_click_in_window("telegram.exe", detect_and_click_image)

    quitWebApp("images\\notpixel-header.png", "images\\close-webapp.png")

    print("waiting for 5 seconds...")
    time.sleep(2.5)
    close_application("telegram.exe")  # Ensure Telegram is closed completely

def process_folders():
    """Process each Telegram clone folder one by one."""
    folders = [f for f in os.listdir(ROOT_FOLDER) if os.path.isdir(os.path.join(ROOT_FOLDER, f))]
    
    for folder in folders:
        folder_path = os.path.join(ROOT_FOLDER, folder)
        process_folder(folder_path)  # Process the folder sequentially

if __name__ == "__main__":
    process_folders()
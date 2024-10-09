import os
import cv2
import time
import subprocess
import pyautogui  # For mouse control and screenshots
import psutil  # To manage processes
import numpy as np
import threading  # For multithreading
import pygetwindow as gw

from quitWebApp import quitWebApp
from detectAndClick import detectAndClick
from windowFocus import focus_app_by_executable

from pixel import *

ROOT_FOLDER = "D:\\Tgs\\Abd\\11acc-13Sep"  # Set your root folder path
TELEGRAM_LINK = "https://t.me/dogs_ref_group/73"  # The link to open in Telegram

# Create a global lock for GUI operations
gui_lock = threading.Lock()

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the images directory
images_dir = os.path.join(script_dir, 'images')

# Path to the progress file
progress_file_path = os.path.join(script_dir, 'progress.txt')

def cleanup_previous_runs():
    """Check for running instances of Telegram and close them."""
    telegram_process_name = "telegram.exe"

    # Close Telegram
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        if proc.info['name'].lower() == telegram_process_name.lower():
            print(f"Terminating {proc.info['name']} with PID: {proc.info['pid']}")
            proc.terminate()
            proc.wait()
            print(f"{proc.info['name']} terminated.")

    print("Cleanup complete. All previous instances closed.")

def detect_image(image_path):
    """Detect if an image is present on the screen without clicking."""
    with gui_lock:
        # Take a screenshot
        screenshot = pyautogui.screenshot()
        img_rgb = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

        # Attempt to load the template image
        template = cv2.imread(image_path, 0)
        if template is None:
            print(f"Failed to load image at {image_path}")
            return False  # Image could not be loaded

        w, h = template.shape[::-1]

        # Match template
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8  # Set a threshold for match quality
        loc = np.where(res >= threshold)

        # Check if any matches were found
        if len(loc[0]) > 0:
            print(f"Image {image_path} detected on screen.")
            return True  # Image was found
        else:
            # Image not found
            return False

def handle_unexpected_image_type1():
    """Handler for the first type of unexpected images."""
    print("Handling unexpected image type 1...")
    quitWebApp(os.path.join(images_dir, "notpixel-header.png"),
               os.path.join(images_dir, "kebapmenu.png"))
    detect_and_click(os.path.join(images_dir, "reload.png"), timeout=2.5)

def handle_unexpected_image_type2():
    """Handler for the second type of unexpected images."""
    print("Handling unexpected image type 2...")
    if detect_image(os.path.join(images_dir, "goback-header.png")):
        quitWebApp(os.path.join(images_dir, "goback-header.png"),
                os.path.join(images_dir, "goback.png"))
    elif detect_image(os.path.join(images_dir, "notpixel-header.png")):
        detect_and_click(os.path.join(images_dir, "promise.png"), timeout=5)


def handle_unexpected_image_type3():
    """Handler for the third type of unexpected images."""
    print("Handling unexpected image type 3...")
    detect_and_click(os.path.join(images_dir, "cancel.png"), timeout=5)

def handle_unexpected_image_type4():
    """Handler for the third type of unexpected images."""
    print("Handling unexpected image type 4...")
    if detect_image(os.path.join(images_dir, 'ayo-taptopaint.png')):
        random_click_in_reduced_window_area("telegram.exe", detect_and_click_image)

unexpected_images = [
    # {
    #     'image_path': os.path.join(images_dir, 'blackscreenwait.png'),
    #     'handler': handle_unexpected_image_type1
    # },
    {
        'image_path': os.path.join(images_dir, 'inactive-quit.png'),
        'handler': handle_unexpected_image_type1
    },
    {
        'image_path': os.path.join(images_dir, 'letsgo.png'),
        'handler': handle_unexpected_image_type1
    },
    {
        'image_path': os.path.join(images_dir, 'newpixel.png'),
        'handler': handle_unexpected_image_type1
    },
    {
        'image_path': os.path.join(images_dir, 'flagisflag.png'),
        'handler': handle_unexpected_image_type2
    },
    {
        'image_path': os.path.join(images_dir, 'energyisover.png'),
        'handler': handle_unexpected_image_type2
    },
    {
        'image_path': os.path.join(images_dir, 'newpixel.png'),
        'handler': handle_unexpected_image_type2
    },
    {
        'image_path': os.path.join(images_dir, 'cancel.png'),
        'handler': handle_unexpected_image_type3
    },
    {
        'image_path': os.path.join(images_dir, 'ayo-taptopaint.png'),
        'handler': handle_unexpected_image_type4
    },
    # Add more as needed
]

def monitor_unexpected_images():
    """Continuously monitor for unexpected images and handle them."""
    while True:
        for item in unexpected_images:
            img_path = item['image_path']
            handler = item['handler']
            if detect_image(img_path):
                # Handle the unexpected image
                print(f"Unexpected image {img_path} detected. Handling...")
                handler()  # Call the associated handler function
                break  # Exit the loop after handling the unexpected image
        time.sleep(1)  # Adjust the sleep time as needed

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
    with gui_lock:
        pyautogui.typewrite(link)  # Type the link in the chat input
        pyautogui.press('enter')    # Press Enter to navigate to the link
        print("Link opened")
    time.sleep(5)  # Wait for the link to open

def detect_and_click(image_path, timeout=7):
    """Detect an image and click on it if found, with retry mechanism."""
    start_time = time.time()  # Record the starting time

    while True:
        with gui_lock:
            # Take a screenshot
            screenshot = pyautogui.screenshot()
            img_rgb = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
            template = cv2.imread(image_path, 0)  # Load the image to detect

            if template is None:
                print(f"Failed to load image at {image_path}")
                return False  # Image could not be loaded

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
    # target_image_path = os.path.join(images_dir, "cancel.png")
    # detect_and_click(target_image_path, timeout=5)  # Detect and click the image

    open_telegram_link(TELEGRAM_LINK)  # Open the specified link

    # Find and click the link after it has been opened
    link_image_path = os.path.join(images_dir, "link-to-ref.png")
    detectAndClick(link_image_path, cut_top_percentage=30)  # Find and click the link

    ref_image = os.path.join(images_dir, "ref.png")
    detectAndClick(ref_image)  # Find and click the link

    detect_and_click(os.path.join(images_dir, "ok-modal.png"), timeout=5)

    random_click_in_reduced_window_area("telegram.exe", detect_and_click_image)

    quitWebApp(os.path.join(images_dir, "notpixel-header.png"),
               os.path.join(images_dir, "close-webapp.png"))

    print("Waiting for 5 seconds...")
    time.sleep(2.5)
    close_application("telegram.exe")  # Ensure Telegram is closed completely

def process_folders():
    """Process each Telegram clone folder one by one."""
    # Load the list of processed folders
    processed_folders = set()
    if os.path.exists(progress_file_path):
        with open(progress_file_path, 'r') as f:
            processed_folders = set(line.strip() for line in f)

    folders = [f for f in os.listdir(ROOT_FOLDER) if os.path.isdir(os.path.join(ROOT_FOLDER, f))]

    for folder in folders:
        if folder in processed_folders:
            print(f"Skipping already processed folder: {folder}")
            continue  # Skip this folder

        folder_path = os.path.join(ROOT_FOLDER, folder)
        process_folder(folder_path)  # Process the folder sequentially

        # After processing, add the folder to the processed list and update the file
        processed_folders.add(folder)
        with open(progress_file_path, 'a') as f:
            f.write(folder + '\n')

    # After processing all folders, check if all have been processed
    if len(processed_folders) == len(folders):
        print("All folders have been processed. Clearing progress.txt.")
        if os.path.exists(progress_file_path):
            os.remove(progress_file_path)

if __name__ == "__main__":
    # First, perform cleanup of any previous runs
    cleanup_previous_runs()

    # Start the monitoring thread
    monitoring_thread = threading.Thread(target=monitor_unexpected_images, daemon=True)
    monitoring_thread.start()

    # Proceed with main code
    process_folders()

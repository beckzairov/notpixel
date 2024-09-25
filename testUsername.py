import pyautogui
import time
from randomuser import *
def change_telegram_username(username):
    # Allow a few seconds to manually focus on the Telegram window
    print("Focus on the Telegram window in the next 5 seconds...")
    time.sleep(5)

    # Open the settings by clicking on the hamburger menu (top left)
    # Get the correct coordinates by using pyautogui.position()
    # This example uses arbitrary coordinates (you need to adjust for your screen)
    pyautogui.click(x=30, y=50)  # Click on the Telegram hamburger menu
    time.sleep(1)

    # Click on "Settings" (again adjust coordinates according to your screen)
    pyautogui.click(x=100, y=200)  # Click on "Settings" option
    time.sleep(2)

    # Now scroll down to the "Username" section and click on it (adjust coordinates)
    pyautogui.click(x=500, y=400)  # Coordinates for the "Username" section
    time.sleep(1)

    # Select and clear the current username (if exists)
    pyautogui.click(x=600, y=250)  # Coordinates for the username input field
    pyautogui.hotkey('ctrl', 'a')  # Select the current username
    pyautogui.press('backspace')   # Delete it

    # Enter the new username
    pyautogui.write(username)
    time.sleep(1)

    # Press Enter to save the username
    pyautogui.press('enter')

    print(f"Username '{username}' has been set successfully.")

# Call the function with your desired username
change_telegram_username(final_username)

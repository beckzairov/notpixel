import pyautogui
import pyperclip
from random_username.generate import generate_username
from detectAndClick import detectAndClick

def makeUsername():
    # Generate a random username and copy it to the clipboard
    user = generate_username(1)[0]
    pyperclip.copy(user)
    return user  # Return the username for future use if needed

def newUser():
    # Generate a new username and detect the image
    username = makeUsername()

    # Detect the "nickname" image and click on it
    detectAndClick(f"images\\nickname.png")

    # After clicking the detected image, wait for a short moment
    pyautogui.sleep(1)

    # Simulate pressing CTRL+V to paste the clipboard content (username)
    pyautogui.hotkey('ctrl', 'v')

    # You can also press 'Enter' after pasting if required
    # pyautogui.press('enter')

# Example usage
newUser()

import time
import pyautogui
from windowFocus import focus_app_by_executable

def test_move_to_symmetric_reduced_area(window_title, h_percent=60, w_percent=40):
    """Move the mouse to different corners within the symmetrically reduced area of the specified window without clicking."""
    # Activate the window
    window = focus_app_by_executable(window_title)
    time.sleep(1)  # Give some time for the window to be focused

    if not window:
        print(f"Cannot move mouse. Window titled '{window_title}' is not found or not active.")
        return

    # Get the coordinates of the window
    x_start = window.rectangle().left
    y_start = window.rectangle().top
    width = window.rectangle().width()
    height = window.rectangle().height()

    # Calculate the symmetric reduced area dimensions
    # Reduce the width and height symmetrically from both sides
    width_reduction = width * (w_percent / 100) / 2
    height_reduction = height * (h_percent / 100) / 2

    x_start_reduced = int(x_start + width_reduction)  # Reduced start on x-axis
    x_end_reduced = int(x_start + width - width_reduction)  # Reduced end on x-axis

    y_start_reduced = int(y_start + height_reduction)  # Reduced start on y-axis
    y_end_reduced = int(y_start + height - height_reduction)  # Reduced end on y-axis

    # Print out the coordinates for the symmetrically reduced area
    print(f"Window '{window_title}' reduced area dimensions:")
    print(f"Top Left Corner of Reduced Area: ({x_start_reduced}, {y_start_reduced})")
    print(f"Bottom Right Corner of Reduced Area: ({x_end_reduced}, {y_end_reduced})")
    print(f"Width (Reduced): {x_end_reduced - x_start_reduced}, Height (Reduced): {y_end_reduced - y_start_reduced}")

    # Move the mouse to the corners of the reduced area
    positions = [
        (x_start_reduced, y_start_reduced),            # Top-left corner of reduced area
        (x_end_reduced, y_start_reduced),              # Top-right corner of reduced area
        (x_start_reduced, y_end_reduced),              # Bottom-left corner of reduced area
        (x_end_reduced, y_end_reduced),                # Bottom-right corner of reduced area
        (x_start_reduced + (x_end_reduced - x_start_reduced) // 2, y_start_reduced + (y_end_reduced - y_start_reduced) // 2)  # Center of the reduced area
    ]

    # Move mouse to each position and print out the position
    for position in positions:
        pyautogui.moveTo(position[0], position[1])
        print(f"Mouse moved to position: {position}")
        time.sleep(1)  # Pause for a moment to observe the movement

# Call the function to test
if __name__ == "__main__":
    # Replace 'Not Pixel' with your actual window title or executable name
    test_move_to_symmetric_reduced_area("telegram.exe")

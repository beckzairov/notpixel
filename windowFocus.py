import psutil
from pywinauto import Application

def focus_app_by_executable(executable_name):
    """Focus on the main parent window of the app by the executable name (e.g., 'telegram.exe')."""
    
    # Loop over all running processes
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] and executable_name.lower() == proc.info['name'].lower():
            try:
                # Connect to the application using the process ID
                app = Application(backend="uia").connect(process=proc.info['pid'])
                
                # Get all windows associated with the application
                all_windows = app.windows()

                # Loop through all windows and try to find the main window
                for window in all_windows:
                    # Check if the window is the main or parent window (not a child or popup)
                    if window.is_visible() and window.is_enabled():
                        window.set_focus()  # Bring the window to the front
                        print(f"Activated main window for {executable_name}")
                        return window

                print(f"No active main window found for {executable_name}")
                return None

            except Exception as e:
                print(f"Error: {e}")
                return None

    print(f"No process found for executable: {executable_name}")
    return None

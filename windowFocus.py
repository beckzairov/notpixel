import psutil
import win32gui
import win32con
from pywinauto import Application

def force_focus_window(hwnd):
    """Forcefully bring a window to the foreground and restore it if minimized."""
    if win32gui.IsIconic(hwnd):
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd)

def focus_app_by_executable(executable_name):
    """Focus on the main parent window of the app by the executable name (e.g., 'telegram.exe')."""
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] and executable_name.lower() == proc.info['name'].lower():
            try:
                app = Application(backend="uia").connect(process=proc.info['pid'])
                all_windows = app.windows()

                for window in all_windows:
                    if window.is_visible() and window.is_enabled():
                        hwnd = window.handle
                        force_focus_window(hwnd)
                        print(f"Activated and brought {executable_name} window to the front.")
                        return window  # Return the window object here

                print(f"No active main window found for {executable_name}")
                return None
            except Exception as e:
                print(f"Error: {e}")
                return None

    print(f"No process found for executable: {executable_name}")
    return None
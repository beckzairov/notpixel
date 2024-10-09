import time
import subprocess
import psutil
import os

SCRIPT_PATH = "D:\\py-codes\\notpixel\\main1.py"  # Path to your main script
VENV_PYTHON_PATH = "D:\\py-codes\\notpixel\\venv\\Scripts\\python.exe"  # Path to Python executable in your virtual environment
INTERVAL_MINUTES = 12  # Interval in minutes

def is_script_running(script_name):
    """Check if the script is already running."""
    for proc in psutil.process_iter(attrs=['pid', 'name', 'cmdline']):
        if script_name in proc.info['cmdline']:
            return True
    return False

def run_script():
    """Run the Python script using the virtual environment."""
    try:
        # Run the script as a subprocess
        subprocess.Popen([VENV_PYTHON_PATH, SCRIPT_PATH])
        print(f"Started script: {SCRIPT_PATH}")
    except Exception as e:
        print(f"Error starting script: {e}")

if __name__ == "__main__":
    while True:
        # Check if the script is already running
        if is_script_running("main1.py"):
            print("Script is already running. Waiting until it's finished...")
        else:
            # Run the script if it is not running
            run_script()

        # Wait for the specified interval before attempting to run again
        time.sleep(INTERVAL_MINUTES * 60)

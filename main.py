import os
import subprocess
import psutil
import time

# Path to the folder containing the clone directories
CLONE_FOLDERS_PATH = r"C:\Users\Acer\AppData\Roaming\Business_Partner_Abdul\2) 25 Accounts"
# Path to the MacroRecorder executable and the macro file
MACRO_RECORDER_PATH = r"C:\Program Files (x86)\MacroRecorder\MacroRecorder.exe"
MACRO_FILE = r"C:\blum-macro.mrf"

# Function to terminate a specific process (e.g., Telegram.exe, MacroRecorder)
def kill_process(process_name):
    found = False
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'].lower() == process_name.lower():
            found = True
            proc.kill()
            print(f"{process_name} terminated.")
    if not found:
        print(f"{process_name} not found.")

# Function to terminate the MacroRecorder if it stays in the background
def kill_macro_recorder():
    kill_process("MacroRecorder.exe")

# Function to terminate Telegram.exe
def kill_telegram():
    kill_process("Telegram.exe")

# Function to open a folder in File Explorer
def open_folder_in_explorer(folder_path):
    try:
        # Open the folder in File Explorer
        print(f"Opening folder: {folder_path}")
        subprocess.Popen(f'explorer "{folder_path}"')
        time.sleep(3)  # Wait for 3 seconds to ensure the window is opened and visible
    except Exception as e:
        print(f"Error opening folder in File Explorer: {str(e)}")

# Function to run the macro command in the current directory
def run_macro_in_folder(folder_path):
    cmd = f'"{MACRO_RECORDER_PATH}" -play="{MACRO_FILE}"'
    try:
        # Open the folder in File Explorer to make sure the macro can detect visual elements
        open_folder_in_explorer(folder_path)

        # Run the macro command
        print(f"Running macro in folder: {folder_path}")
        subprocess.run(cmd, shell=True)
        time.sleep(5)  # Increase the wait time to ensure the macro finishes

        # Kill the MacroRecorder after the macro finishes
        print("Attempting to kill MacroRecorder.exe...")
        kill_macro_recorder()

        # Kill Telegram.exe after the macro finishes
        print("Attempting to kill Telegram.exe...")
        kill_telegram()

    except Exception as e:
        print(f"Error running macro in {folder_path}: {str(e)}")

# Main function to iterate through clone folders and run the macro
def process_clone_folders():
    # Get all clone folder names in the directory
    clone_folders = [f for f in os.listdir(CLONE_FOLDERS_PATH) if os.path.isdir(os.path.join(CLONE_FOLDERS_PATH, f))]

    for folder in clone_folders:
        folder_path = os.path.join(CLONE_FOLDERS_PATH, folder)
        run_macro_in_folder(folder_path)  # Run macro

        # Go back to the root directory after running the macro in the current folder
        time.sleep(1)  # Short pause before proceeding to the next folder

if __name__ == "__main__":
    process_clone_folders()
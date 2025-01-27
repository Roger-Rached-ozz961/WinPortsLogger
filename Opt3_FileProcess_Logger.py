import time
import psutil
import os
from datetime import datetime
from threading import Thread
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging

# Define colors for terminal output
PURPLE = '\033[95m'
GREEN = '\033[32m'
CYAN = '\033[36m'
WHITE = '\033[37m'
RESET = '\033[0m'
RED = '\033[31m'
YELLOW = '\033[93m'
BOLD = '\033[1m'

# To keep track of previously connected drives
previous_drives = set()

# Default paths to monitor
default_paths = [os.path.join(os.path.expanduser("~"), "Desktop")]

# User-specified paths to monitor
user_paths = []

# List of active observers
observers = []

# Set the correct log directory and file path (relative to the script directory)
log_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "logs")
log_file_path = os.path.join(log_dir, "file_process_logs.txt")

# Ensure logs directory exists
os.makedirs(log_dir, exist_ok=True)

# Set up logging with a file handler
logging.basicConfig(level=logging.DEBUG, handlers=[logging.FileHandler(log_file_path)])

# Banner function
def print_banner():
    print(f"{PURPLE}{BOLD} \n████████████████████████████████████████████████████████████████████")
    print(f"{PURPLE}{BOLD} " * 10 + "File Operation Logger - Version 1.0" + " " * 10)
    print(f"{PURPLE}{BOLD} " * 8 + "  Author: Ozz961" + " " * 8)
    print(f"{YELLOW} " * 4 + "\nDescription: This script monitors file operations like creation, modification, and moving." + " " * 4)
    print(f"{YELLOW} " * 4 + "It logs the source and destination of files being moved or copied." + " " * 4)
    print(f"{YELLOW} " * 4 + "The log file will be saved as 'file_process_logs.txt' in the 'logs' folder." + " " * 4)
    print(f"{CYAN} " * 4 + "\n   [INFO] Press Ctrl + C to stop the monitoring." + " " * 4)
    print(f"{PURPLE}{BOLD} ████████████████████████████████████████████████████████████████████")
    print("\n")

def get_connected_drives():
    """Detect and return connected USB drives (removable media)."""
    partitions = psutil.disk_partitions()
    return {partition.device for partition in partitions if 'removable' in partition.opts.lower()}

def monitor_path(path):
    """Monitor a specific path for file changes."""
    print(f"\n{YELLOW}Monitoring file operations on {path}...{RESET}")
    observer = Observer()
    event_handler = FileMonitorHandler()
    observer.schedule(event_handler, path=path, recursive=True)
    observer.start()
    observers.append(observer)

def usb_detection_thread():
    """Continuously detect new USB drives and start monitoring them."""
    global previous_drives
    while True:
        connected_drives = get_connected_drives()
        new_drives = connected_drives - previous_drives
        removed_drives = previous_drives - connected_drives

        if new_drives:
            for drive in new_drives:
                print(f"{GREEN}[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] New USB drive detected: {drive}{RESET}")
                monitor_path(drive)

        if removed_drives:
            for drive in removed_drives:
                print(f"{RED}[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] USB drive disconnected: {drive}{RESET}")

        previous_drives = connected_drives
        time.sleep(1)

class FileMonitorHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        log_event("MODIFIED", event.src_path)

    def on_created(self, event):
        if event.is_directory:
            return
        log_event("CREATED", event.src_path)

    def on_moved(self, event):
        if event.is_directory:
            return
        log_event("MOVED", event.src_path, event.dest_path)

    def on_deleted(self, event):
        if event.is_directory:
            return
        log_event("DELETED", event.src_path)

def log_event(action_type, src_path, dest_path=None):
    """Log the file action based on the event."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message_console = ""
    log_message_file = ""

    # Determine the log message based on the action type
    if action_type == "MODIFIED":
        log_message_console = f"{CYAN}[{timestamp}] MODIFIED: {WHITE}{src_path}{RESET}"
        log_message_file = f"[{timestamp}] MODIFIED: {src_path}"
    elif action_type == "CREATED":
        log_message_console = f"{GREEN}[{timestamp}] CREATED: {WHITE}{src_path}{RESET}"
        log_message_file = f"[{timestamp}] CREATED: {src_path}"
    elif action_type == "MOVED":
        log_message_console = f"{YELLOW}[{timestamp}] MOVED: {WHITE}{src_path} -> {dest_path}{RESET}"
        log_message_file = f"[{timestamp}] MOVED: {src_path} -> {dest_path}"
    elif action_type == "DELETED":
        log_message_console = f"{RED}[{timestamp}] DELETED: {WHITE}{src_path}{RESET}"
        log_message_file = f"[{timestamp}] DELETED: {src_path}"

    # Print to console
    print(log_message_console)

    # Log to the file
    logging.info(log_message_file)

def get_user_paths():
    """Prompt the user for paths they want to monitor with an example."""
    print(f"\n{YELLOW}[INFO] Enter the paths you want to monitor (separated by commas). Press Enter to use default paths:{RESET}")
    print(f"\n{PURPLE}Example: C:\\Users\\User\\Documents, D:\\Photos, /home/user/Desktop{RESET}\n")
    paths_input = input(f"{YELLOW}Paths:{RESET} {PURPLE}").strip()
    
    if paths_input:
        paths = [path.strip() for path in paths_input.split(',')]
        for path in paths:
            if os.path.exists(path):
                user_paths.append(path)
                print(f"{GREEN}Added path: {path}{RESET}")
            else:
                print(f"{RED}Invalid path: {path}{RESET}")
    else:
        print(f"{YELLOW}No custom paths provided. The script will use the default path which is Desktop.{RESET}")

def stop_all_observers():
    """Stop all active observers."""
    for observer in observers:
        observer.stop()
        observer.join()
    print(f"{RED}\n[NOTICE] Exiting script...{RESET}")

def main():
    try:
        # Get user-specified paths to monitor
        get_user_paths()

        # Monitor default and user-specified paths
        for path in default_paths + user_paths:
            monitor_path(path)

        # Start USB detection in a separate thread
        detection_thread = Thread(target=usb_detection_thread, daemon=True)
        detection_thread.start()

        print(f"{YELLOW}Monitoring started... Press Ctrl+C to stop.{RESET}")
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n{YELLOW}[{timestamp}] Monitoring stopped by user.{RESET}")
        stop_all_observers()

if __name__ == "__main__":
    print_banner()
    main()

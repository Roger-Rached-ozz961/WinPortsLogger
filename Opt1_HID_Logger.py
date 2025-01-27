import os
import time
import hid
import sys
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

# Path to the logs folder
LOG_FOLDER = "logs"
LOG_FILE = os.path.join(LOG_FOLDER, "hid_device_log.txt")

# Ensure the logs folder exists
os.makedirs(LOG_FOLDER, exist_ok=True)

# Banner function
def print_banner():
    print(Fore.MAGENTA + Style.BRIGHT + " ████████████████████████████████████████████████████████████████████")
    print(Fore.MAGENTA + Style.BRIGHT + " " * 10 + "HID Device Logger - Version 1.0" + " " * 10)
    print(Fore.MAGENTA + Style.BRIGHT + " " * 8 + "Author: ozz961" + " " * 8)
    print(Fore.YELLOW + " " * 4 + "This script monitors HID devices, logs connection/disconnection events," + " " * 4)
    print(Fore.YELLOW + " " * 4 + "and provides detailed device information." + " " * 4)
    print(Fore.YELLOW + " " * 4 + "The log file will be saved as 'hid_device_log.txt' in the 'logs' folder." + " " * 4)
    print(Fore.CYAN + " " * 4 + "Press Ctrl + C to stop the monitoring." + " " * 4)
    print(Fore.MAGENTA + Style.BRIGHT + " ████████████████████████████████████████████████████████████████████")
    print("\n")

def log_event(message, color=Fore.GREEN):
    """Log events to the console and a log file."""
    timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]")
    log_message = f"{timestamp} {message}"
    print(color + log_message)
    with open(LOG_FILE, "a") as file:
        file.write(log_message + "\n")

def log_device_info(device, action):
    """Log HID device information with human-readable formatting."""
    log_event(f"{action.capitalize()} Event:", Fore.CYAN)
    log_event(f"Path: {device.get('path', 'Unknown')}", Fore.YELLOW)
    log_event(f"Vendor ID: {hex(device['vendor_id'])}", Fore.GREEN)
    log_event(f"Product ID: {hex(device['product_id'])}", Fore.GREEN)
    log_event(f"Manufacturer: {device.get('manufacturer_string', 'Unknown')}", Fore.MAGENTA)
    log_event(f"Product: {device.get('product_string', 'Unknown')}", Fore.MAGENTA)
    log_event(f"Serial Number: {device.get('serial_number', 'Unknown')}", Fore.YELLOW)
    log_event(f"Release Number: {device.get('release_number', 'Unknown')}", Fore.CYAN)
    log_event(f"Usage Page: {device.get('usage_page', 'Unknown')}", Fore.YELLOW)
    log_event(f"Usage: {device.get('usage', 'Unknown')}", Fore.GREEN)
    log_event(f"Interface Number: {device.get('interface_number', 'Unknown')}", Fore.GREEN)
    log_event("-" * 50, Fore.RED)  # Separator line for better readability

def get_hid_devices():
    """Fetch and log all currently connected HID devices."""
    try:
        devices = hid.enumerate()
        log_event("Enumerating connected HID devices...", Fore.YELLOW)
        for device in devices:
            log_device_info(device, "connected")
    except Exception as e:
        log_event(f"Error while enumerating HID devices: {e}", Fore.RED)

def monitor_devices():
    """Monitor HID devices for connection and disconnection events."""
    connected_devices = set()
    try:
        while True:
            current_devices = {device['path'] for device in hid.enumerate()}
            new_devices = current_devices - connected_devices
            removed_devices = connected_devices - current_devices

            for path in new_devices:
                log_event(f"Device Connected: {path}", Fore.CYAN)
                device = next((d for d in hid.enumerate() if d['path'] == path), None)
                if device:
                    log_device_info(device, "connected")

            for path in removed_devices:
                log_event(f"Device Disconnected: {path}", Fore.MAGENTA)

            connected_devices = current_devices
            time.sleep(1)
    except KeyboardInterrupt:
        log_event("Monitoring stopped by user.", Fore.YELLOW)
    except Exception as e:
        log_event(f"Error during monitoring: {e}", Fore.RED)

if __name__ == "__main__":
    # Display Banner
    print_banner()

    log_event("HID Device Logger Started.", Fore.GREEN)
    get_hid_devices()  # Log all connected devices at startup
    monitor_devices()  # Monitor devices for changes

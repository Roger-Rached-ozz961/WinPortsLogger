import os
import time
import logging
from termcolor import colored
import uuid
from datetime import datetime
import psutil
import win32file 
import win32con
import win32api

# Set up logging to a file and console
log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# INFO, DEBUG, and ERROR logs
logging.basicConfig(level=logging.DEBUG,  # Change to DEBUG for more detailed logging
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler(os.path.join(log_dir, 'usb_monitor_debugging_details.txt'))])

# USB connection/disconnection logs
connection_handler = logging.FileHandler(os.path.join(log_dir, 'usb_connections_log.txt'))
connection_handler.setLevel(logging.INFO)
connection_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
connection_logger = logging.getLogger('usb_connection_logger')
connection_logger.addHandler(connection_handler)

# Banner with professional info
def display_banner():
    banner = """
████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████

               USB Drive Monitor Script

Author: Ozz961 | Version: 1.0
Description: Monitors USB device connections and disconnections,
             logging detailed info like drive type, size, UUID,
             manufacturer, model, serial number, and access status.

████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████
"""
    print(colored(banner, 'magenta', attrs=['bold']))


# Function to get connected USB devices with detailed information
def get_usb_devices():
    """Get detailed information about connected USB drives."""
    usb_devices = []
    
    # Get the list of all connected drives
    try:
        drives = win32api.GetLogicalDriveStrings().split('\000')
        drives = [drive for drive in drives if drive]  # Remove empty strings from the list
        logging.debug(f"Detected Drives: {drives}")  # Log all detected drives
    except Exception as e:
        logging.error(f"Error retrieving drives: {e}")
        return usb_devices
    
    # Iterate over drives and check for removable ones
    for drive in drives:
        if drive:
            try:
                # Check if the drive is a removable device
                drive_type = win32file.GetDriveType(drive)
                logging.debug(f"Drive {drive} type: {drive_type}")  # Log drive type
                if drive_type == win32con.DRIVE_REMOVABLE:
                    # Get drive details
                    partitions = psutil.disk_partitions(all=True)
                    drive_info = next((p for p in partitions if p.device == drive), None)
                    if drive_info:
                        usb_devices.append({
                            'drive': drive,
                            'fstype': drive_info.fstype,
                            'total_size': psutil.disk_usage(drive).total,
                            'used_size': psutil.disk_usage(drive).used,
                            'free_size': psutil.disk_usage(drive).free,
                            'used_percentage': psutil.disk_usage(drive).percent,  # Added used percentage
                            'uuid': str(uuid.uuid4()),  # Placeholder for unique device UUID
                            'manufacturer': "Unknown",  # Placeholder for device manufacturer
                            'model': "Unknown",  # Placeholder for device model
                            'serial': "Unknown",  # Placeholder for serial number
                            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'readable': os.access(drive, os.R_OK),
                            'writable': os.access(drive, os.W_OK)
                        })
            except Exception as e:
                logging.error(f"Error retrieving information for {drive}: {e}")
    return usb_devices

# Function to monitor USB device connection and disconnection
def monitor_usb():
    display_banner()
    print(colored("USB Drive Monitor Script Started", 'cyan', attrs=['bold']))
    logging.info("USB Drive Monitor Script Started")
    
    previous_devices = set([device['drive'] for device in get_usb_devices()])
    connected_devices = set()  # To track connected devices
    
    try:
        while True:
            time.sleep(1)  # Check every second
            try:
                current_devices = set([device['drive'] for device in get_usb_devices()])
                
                # Check for newly connected devices
                new_devices = current_devices - previous_devices
                for device in new_devices:
                    if device not in connected_devices:
                        connected_devices.add(device)
                        device_info = next(d for d in get_usb_devices() if d['drive'] == device)
                        # Log the USB connection event
                        connection_logger.info(f"New USB device connected: {device_info['drive']} | {device_info['fstype']} | "
                                               f"Size: {device_info['total_size']} bytes | Used: {device_info['used_size']} bytes | "
                                               f"Free: {device_info['free_size']} bytes | Used %: {device_info['used_percentage']}% | "
                                               f"UUID: {device_info['uuid']} | Manufacturer: {device_info['manufacturer']} | "
                                               f"Model: {device_info['model']} | Serial: {device_info['serial']} | "
                                               f"Readable: {device_info['readable']} | Writable: {device_info['writable']} | "
                                               f"Timestamp: {device_info['timestamp']}")
                        print(colored(f"{device_info['timestamp']} - New USB device connected: {device_info['drive']} | "
                                       f"{device_info['fstype']} | Size: {device_info['total_size']} bytes | "
                                       f"Used: {device_info['used_size']} bytes | Free: {device_info['free_size']} bytes | "
                                       f"Used %: {device_info['used_percentage']}% | UUID: {device_info['uuid']} | "
                                       f"Manufacturer: {device_info['manufacturer']} | Model: {device_info['model']} | "
                                       f"Serial: {device_info['serial']} | Readable: {device_info['readable']} | "
                                       f"Writable: {device_info['writable']}", 'green'))
                
                # Check for disconnected devices
                removed_devices = previous_devices - current_devices
                for device in removed_devices:
                    if device in connected_devices:
                        connected_devices.remove(device)
                        try:
                            device_info = next(d for d in get_usb_devices() if d['drive'] == device)
                            # Log the USB disconnection event
                            connection_logger.info(f"USB device disconnected: {device_info['drive']} | {device_info['fstype']} | "
                                                   f"Size: {device_info['total_size']} bytes | Used: {device_info['used_size']} bytes | "
                                                   f"Free: {device_info['free_size']} bytes | Used %: {device_info['used_percentage']}% | "
                                                   f"UUID: {device_info['uuid']} | Manufacturer: {device_info['manufacturer']} | "
                                                   f"Model: {device_info['model']} | Serial: {device_info['serial']} | "
                                                   f"Readable: {device_info['readable']} | Writable: {device_info['writable']} | "
                                                   f"Timestamp: {device_info['timestamp']}")
                            print(colored(f"{device_info['timestamp']} - USB device disconnected: {device_info['drive']} | "
                                           f"{device_info['fstype']} | Size: {device_info['total_size']} bytes | "
                                           f"Used: {device_info['used_size']} bytes | Free: {device_info['free_size']} bytes | "
                                           f"Used %: {device_info['used_percentage']}% | UUID: {device_info['uuid']} | "
                                           f"Manufacturer: {device_info['manufacturer']} | Model: {device_info['model']} | "
                                           f"Serial: {device_info['serial']} | Readable: {device_info['readable']} | "
                                           f"Writable: {device_info['writable']}", 'red'))
                        except StopIteration:
                            connection_logger.info(f"USB device disconnected: {device}")
                            print(colored(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - USB device disconnected: {device}", 'red'))
                
                # Update the previous_devices for the next iteration
                previous_devices = current_devices

            except Exception as e:
                logging.error(f"Error occurred: {e}")
                print(colored(f"Error occurred: {e}", 'red'))
                
    except KeyboardInterrupt:
        print(colored("\nUSB Drive Monitor Script Stopped.", 'yellow', attrs=['bold']))
        logging.info("USB Drive Monitor Script Stopped.")

if __name__ == "__main__":
    monitor_usb()

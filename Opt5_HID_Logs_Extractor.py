import os
import time

# Display script banner and author information
print("\033[95m")
print("==============================================")
print("===        HID Logs Extractor Script       ===")
print("===           Author: Ozz961               ===")
print("==============================================")
print("\033[0m")
print("\033[94m[Info] This script will keep running until you press CTRL + C to stop it.\033[0m\n")

# Folder and File Settings
folder_name = 'logs'
file_name = 'hid_device_log.txt'

try:
    while True:
        # Check if the 'logs' folder exists
        if not os.path.exists(folder_name):
            print("\033[91m[Error] The folder 'logs' does not exist. Please ensure the 'logs' folder is in the same directory as this script.\033[0m")
            time.sleep(5)
            continue

        # Check if the log file exists inside the folder
        file_path = os.path.join(folder_name, file_name)
        if not os.path.isfile(file_path):
            print(f"\033[91m[Error] The file '{file_name}' does not exist in the folder '{folder_name}'.\033[0m")
            time.sleep(5)
            continue

        # Get user input for the number of events to extract
        try:
            print("\033[93m")
            num_events = int(input("Enter the number of recent events to extract (or press CTRL + C to stop): "))
            print("\033[0m")
            if num_events <= 0:
                raise ValueError
        except ValueError:
            print("\033[91m[Error] Invalid input. Please enter a positive integer.\033[0m")
            time.sleep(2)   
            continue

        # Read the log file
        try:
            with open(file_path, 'r') as log_file:
                logs = log_file.readlines()
        except Exception as e:
            print(f"\033[91m[Error] Unable to read the file: {e}\033[0m")
            time.sleep(5)
            continue

        # Extract events based on the delimiter
        delimiter = "--------------------------------------------------\n"
        event_blocks = []
        current_block = []

        # Parse the file into event blocks
        for line in logs:
            current_block.append(line)
            if delimiter in line:
                event_blocks.append(current_block)
                current_block = []

        # Handle insufficient events in the log
        if len(event_blocks) < num_events:
            print(f"\033[91m[Error] The log file contains only {len(event_blocks)} events, but you requested {num_events}.\033[0m")
            time.sleep(3)
            continue

        # Get the last `num_events` blocks
        selected_events = event_blocks[-num_events:]

        # Print the extracted events
        print("\033[92m[Success] Extracted Log Events:\033[0m\n")
        for idx, event in enumerate(selected_events, 1):
            print(f"\033[93m[Event {idx}]:\033[0m")
            print("\033[92m" + "".join(event).strip() + "\033[0m")
            print("\033[94m" + delimiter.strip() + "\033[0m")

        print("\033[92m[Extraction Completed] The requested events have been successfully extracted.\033[0m")
        print("\033[93m[Info] The script will repeat. Press CTRL + C to stop it.\033[0m\n")
        time.sleep(5)  # Delay before repeating

except KeyboardInterrupt:
    print("\n\033[91m[Info] Script was stopped by the user.\033[0m")

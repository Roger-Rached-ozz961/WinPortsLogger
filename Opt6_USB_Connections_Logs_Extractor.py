import os
import time

# Display script banner and author information
print("\033[95m")
print("================================================")
print("===     extracting usb connections log       ===")
print("===              Author: Ozz961              ===")
print("================================================")
print("\033[0m")  # Reset color

# Inform the user how to stop the tool
print("\033[93m[Info] This script will keep running until you stop it manually.\033[0m")
print("\033[91m[NOTICE] Press CTRL + C to stop the script.\033[0m\n")

# Folder and file settings
folder_name = 'logs'
file_name = 'usb_connections_log.txt'
file_path = os.path.join(folder_name, file_name)

try:
    while True:
        # Check if the 'logs' folder exists
        if not os.path.exists(folder_name):
            print("\033[91m[Error] The folder 'logs' does not exist. Please ensure the 'logs' folder is in the same directory as this script.\033[0m")
            time.sleep(5)
            continue

        # Check if the log file exists inside the folder
        if not os.path.isfile(file_path):
            print(f"\033[91m[Error] The file '{file_name}' does not exist in the folder '{folder_name}'.\033[0m")
            time.sleep(5)
            continue

        # Read the log file
        try:
            with open(file_path, 'r') as log_file:
                logs = log_file.readlines()
        except Exception as e:
            print(f"\033[91m[Error] Unable to read the file: {e}\033[0m")
            time.sleep(5)
            continue

        # Display the content of the log file
        if logs:
            print("\033[92m[Success] USB Connection Logs:\033[0m\n")
            for line in logs:
                print(f"\033[94m{line.strip()}\033[0m")  # Light blue for each log line
                print("------------------------------------------------")  # Line Seperator
        else:
            print("\033[93m[Info] The log file is currently empty.\033[0m")

        # Wait before repeating
        print("\033[93m\n[Info] Waiting for updates... Press CTRL + C to stop.\033[0m\n")
        time.sleep(10)

# End of script
except KeyboardInterrupt:
    print("\n\033[91m[Info] The Script was stopped by the user. \033[0m")

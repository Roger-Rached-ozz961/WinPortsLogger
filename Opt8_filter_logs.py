import os
import sys
from colorama import Fore, Style, init
import argparse

# Initialize Colorama for colored output
init(autoreset=True)

def print_banner():
    """Display a purple banner for the script."""
    banner = f"""
{Fore.MAGENTA}{Style.BRIGHT}████████████████████████████████████████████████████████████████████
#                     Log Filtering Script                    #
#                      Author: Ozz961                         #
████████████████████████████████████████████████████████████████████
"""
    print(banner)

def print_description():
    """Print the description and usage help."""
    print(f"""
{Fore.GREEN}Welcome to the Log Filtering Script!{Fore.RESET}
This script helps you filter different types of logs from the following log files in the "logs" folder:

- `hid_device_log.txt` (HID logs)
- `usb_connection_log.txt` (USB logs)
- `file_process_logs.txt` (File Process logs)

{Fore.YELLOW}Available options: {Fore.RESET}
1. --hid-type "Manufacturer" -c [number] : Filter HID logs by the manufacturer name (e.g., "SteelSeries").
2. --usb-type "Manufacturer" -c [number] : Filter USB logs by the manufacturer name (e.g., "Logitech").
3. --file-process --type "MODIFIED/DELETED/COPY" -c [number] : Filter file process logs for specific events.

Examples:
- To filter HID logs by "SteelSeries" and show the last 5 events:
  --hid-type "SteelSeries" -c 5
- To filter USB logs by "Logitech" and show the last 3 events:
  --usb-type "Logitech" -c 3
- To filter file process logs for "MODIFIED" events and show the last 4:
  --file-process --type "MODIFIED" -c 4

{Fore.RED}To stop the script, press CTRL+C at any time.{Fore.RESET}
    """)

def parse_arguments(user_input):
    """Parse user input arguments."""
    parser = argparse.ArgumentParser(description="Filter logs based on user input.")
    parser.add_argument("--hid-type", type=str, help='Filter HID logs by "Manufacturer" value.')
    parser.add_argument("--usb-type", type=str, help='Filter USB logs by "Manufacturer" value.')
    parser.add_argument("--file-process", action="store_true", help="Filter file process logs.")
    parser.add_argument("--type", type=str, choices=["MODIFIED", "DELETED", "COPY"], help="File process event type.")
    parser.add_argument("-c", type=int, help="Number of events to retrieve.", required=True)
    
    # This will parse the user's input from the input string
    return parser.parse_args(user_input.split())

def filter_hid_logs(manufacturer, count, log_file):
    """Filter HID logs based on manufacturer."""
    return filter_logs_by_key("Manufacturer", manufacturer, count, log_file)

def filter_usb_logs(manufacturer, count, log_file):
    """Filter USB logs based on manufacturer."""
    return filter_logs_by_key("Manufacturer", manufacturer, count, log_file)

def filter_file_process_logs(event_type, count, log_file):
    """Filter file process logs by event type."""
    try:
        with open(log_file, "r") as file:
            lines = file.readlines()
        filtered_events = [line for line in lines if event_type in line]
        return filtered_events[-count:] if count > 0 else filtered_events
    except FileNotFoundError:
        print(f"{Fore.RED}Error: Log file '{log_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}")
        sys.exit(1)

def filter_logs_by_key(key, value, count, log_file):
    """Filter logs by a key-value pair."""
    try:
        # Remove any extra quotation marks or spaces around the value
        value = value.strip('"').strip()

        with open(log_file, "r") as file:
            lines = file.readlines()

        filtered_events = []
        event = []
        capture = False

        for line in lines:
            if "--------------------------------------------------" in line:
                if capture and any(f"{key}: {value}" in e for e in event):
                    filtered_events.append("".join(event))
                event = []
                capture = False
            event.append(line)
            if f"{key}: {value}" in line:
                capture = True

        return filtered_events[-count:] if count > 0 else filtered_events
    except FileNotFoundError:
        print(f"{Fore.RED}Error: Log file '{log_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}")
        sys.exit(1)


        return filtered_events[-count:] if count > 0 else filtered_events
    except FileNotFoundError:
        print(f"{Fore.RED}Error: Log file '{log_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}")
        sys.exit(1)

def display_results(results):
    """Display filtered log results."""
    if not results:
        print(f"{Fore.YELLOW}No matching events found.")
    else:
        print(f"{Fore.GREEN}Filtered events:{Fore.RESET}")
        for event in results:
            print(event)
            print(f"{Fore.CYAN}{'-'*50}{Fore.RESET}")

def main():
    # Print the banner and description
    print_banner()
    print_description()

    # Continuously prompt the user for input
    while True:
        try:
            # Prompt user for input command
            user_input = input(f"{Fore.MAGENTA}Enter your command (e.g., --file-process --type 'MODIFIED' -c 4): {Fore.RESET}")
            args = parse_arguments(user_input)
            
            # Define log folder and files
            log_folder = "logs"
            hid_log_file = os.path.join(log_folder, "hid_device_log.txt")
            usb_log_file = os.path.join(log_folder, "usb_connection_log.txt")
            file_process_log_file = os.path.join(log_folder, "file_process_logs.txt")

            # Process arguments
            if args.hid_type:
                print(f"{Fore.YELLOW}Filtering HID logs for manufacturer '{args.hid_type}' with count {args.c}...\n")
                results = filter_hid_logs(args.hid_type, args.c, hid_log_file)
                display_results(results)
            elif args.usb_type:
                print(f"{Fore.YELLOW}Filtering USB logs for manufacturer '{args.usb_type}' with count {args.c}...\n")
                results = filter_usb_logs(args.usb_type, args.c, usb_log_file)
                display_results(results)
            elif args.file_process and args.type:
                print(f"{Fore.YELLOW}Filtering File Process logs for type '{args.type}' with count {args.c}...\n")
                results = filter_file_process_logs(args.type, args.c, file_process_log_file)
                display_results(results)
            else:
                print(f"{Fore.RED}Invalid arguments. Use --help to see usage details.")
        
        except KeyboardInterrupt:
            print(f"\n{Fore.RED}\n[NOTICE] Script terminated by user.{Fore.RESET}")
            sys.exit(0)

if __name__ == "__main__":
    main()

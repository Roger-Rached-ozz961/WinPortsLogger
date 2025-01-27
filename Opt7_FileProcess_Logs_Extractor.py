import os
import sys
from colorama import Fore, Style, init
import signal

# Initialize Colorama
init(autoreset=True)

def print_banner():
    """
    Prints an ASCII banner with the script title and author.
    """
    ascii_banner = f"""
{Fore.MAGENTA}{Style.BRIGHT}████████████████████████████████████████████████████████████████████
#                  Extracting Logs                         #
#                   Author: Ozz961                         #
████████████████████████████████████████████████████████████████████
"""
    print(ascii_banner)

def get_last_events(log_file, num_events):
    """
    Reads the last 'num_events' from the log file and returns them as a list.
    """
    try:
        with open(log_file, 'r') as file:
            lines = file.readlines()
        last_events = lines[-num_events:]
        return last_events
    except FileNotFoundError:
        return f"{Fore.RED}Error: The file '{log_file}' was not found."
    except Exception as e:
        return f"{Fore.RED}An error occurred: {str(e)}"

def graceful_exit(signal_received=None, frame=None):
    """
    Handles graceful exit when interrupted.
    """
    print(f"\n{Fore.RED}\n[NOTICE] Script was ended by user.{Fore.RESET}")
    sys.exit(0)

def main():
    # Attach signal handlers for graceful exit
    signal.signal(signal.SIGINT, graceful_exit)
    signal.signal(signal.SIGTERM, graceful_exit)

    # Print banner
    print_banner()

    # Define the log folder and file
    log_folder = 'logs'
    log_file_name = 'file_process_logs.txt'
    log_file_path = os.path.join(log_folder, log_file_name)

    # Explain purpose to the user
    print(f"{Fore.CYAN}The log file should be located in the 'logs' folder as '{log_file_name}'.\n")
    print(f"{Fore.CYAN}To exit the script, press    CTRL+C at any time.\n")

    while True:
        try:
            # Input: Number of last events to display
            num_events = input(f"{Fore.GREEN}Enter the number of last events you want to retrieve: {Fore.RESET}")
            if not num_events.isdigit() or int(num_events) <= 0:
                print(f"{Fore.RED}Please enter a positive integer.")
                continue
            
            num_events = int(num_events)
            print(f"{Fore.YELLOW}\nFetching the last {num_events} events...\n{Fore.RESET}")
            result = get_last_events(log_file_path, num_events)

            if isinstance(result, list):
                if not result:
                    print(f"{Fore.RED}No events found in the log file.")
                else:
                    print(f"{Fore.BLUE}Last {num_events} events:{Fore.RESET}")
                    for i, event in enumerate(result, 1):
                        print(f"{Fore.GREEN}{i}. {event.strip()}{Fore.RESET}")
            else:
                print(result)

            print(f"\n{Fore.YELLOW}[INFO] You can request more events or press CTRL+C to exit.{Fore.RESET}\n")

        except KeyboardInterrupt:
            graceful_exit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        graceful_exit()

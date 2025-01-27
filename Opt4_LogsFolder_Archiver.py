import os
import shutil
from datetime import datetime
from colorama import Fore, Style, init
import py7zr
import rarfile

# Initialize colorama
init(autoreset=True)

def archive_logs_folder():
    author_name = "Ozz961"
    folder_name = "logs"  # Fixed folder name

    # Light purple header
    print(Fore.LIGHTMAGENTA_EX + f"=== Archive Logs Script by {author_name} ===\n")
    
    # Light yellow for process info
    print(Fore.LIGHTYELLOW_EX + f"Starting the archiving process for the folder: '{folder_name}'\n")

    # Check if the folder exists
    if not os.path.isdir(folder_name):
        print(Fore.RED + f"Error: The folder '{folder_name}' does not exist.")
        input(Fore.CYAN + "\nPress Enter to exit...")
        return

    # Supported archive formats
    archive_formats = {
        "1": "zip",
        "2": "tar",
        "3": "tar.gz",
        "4": "rar",
        "5": "7z"
    }
    
    # Light yellow for archive options
    print(Fore.LIGHTYELLOW_EX + "Choose an archive format:")
    for key, value in archive_formats.items():
        print(Fore.WHITE + f" [{key}] .{value.upper()}")

    choice = input(Fore.YELLOW + "\nEnter your choice (1-5): ").strip()
    if choice not in archive_formats:
        print(Fore.RED + "Invalid choice. Exiting.")
        input(Fore.CYAN + "\nPress Enter to exit...")
        return

    # Get the chosen format
    chosen_format = archive_formats[choice]
    
    # Generate a timestamp for uniqueness
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = f"{folder_name}_archived_{timestamp}"
    archive_path = f"{base_name}.{chosen_format}"

    try:
        if chosen_format == "zip":
            print(Fore.GREEN + f"\nCreating .ZIP archive...\n")
            shutil.make_archive(base_name, "zip", folder_name)
        elif chosen_format == "tar":
            print(Fore.GREEN + f"\nCreating .TAR archive...\n")
            shutil.make_archive(base_name, "tar", folder_name)
        elif chosen_format == "tar.gz":
            print(Fore.GREEN + f"\nCreating .TAR.GZ archive...\n")
            shutil.make_archive(base_name, "gztar", folder_name)
        elif chosen_format == "rar":
            print(Fore.GREEN + f"\nCreating .RAR archive...\n")
            with rarfile.RarFile(archive_path, 'w') as rf:
                rf.add(folder_name, arcname=os.path.basename(folder_name))
        elif chosen_format == "7z":
            print(Fore.GREEN + f"\nCreating .7Z archive...\n")
            with py7zr.SevenZipFile(archive_path, 'w') as zf:
                zf.writeall(folder_name, arcname=os.path.basename(folder_name))
        else:
            raise ValueError("Unsupported archive format.")
        
        # Light green success message
        print(Fore.LIGHTGREEN_EX + f"Archive created successfully!\n")
        print(Fore.BLUE + "Details:")
        print(Fore.WHITE + f" - Folder archived: {Fore.MAGENTA}'{folder_name}'")
        print(Fore.WHITE + f" - Archive name: {Fore.MAGENTA}'{archive_path}'\n")
    except Exception as e:
        print(Fore.RED + f"An error occurred while archiving: {e}")
    
    input(Fore.CYAN + "Process completed. Press Enter to exit...")

# Call the function
archive_logs_folder()

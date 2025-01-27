@echo off
:: WinPortsLogger - Interactive tool.
:: Author: Roger Rached.
:: Version: 1.0
:: GitHub: https://github.com/roger-rached-ozz961/WinPortsLogger
:: Contact: roger_rached@outlook.com

:: Check if 'termcolor' module is installed
python -c "import termcolor" 2>nul || (
    echo "termcolor module not found, installing..."
    pip install termcolor
    if errorlevel 1 (
        echo Failed to install termcolor. Please check your Python environment and try again.
        pause
        exit /b
    )
    echo termcolor installed successfully.
)

:: Main menu
:menu
echo =======================================
echo        Welcome to WinPortsLogger
echo =======================================
echo [1] Run HID Logger Script
echo [2] Run USB Logger Script
echo [3] Run File Process Logger Script
echo [4] Run Logs Folder Archiver Script
echo [5] Run HID Logs Extractor Script
echo [6] Run USB Connections Logs Extractor Script
echo [7] Run File Process Logs Extractor Script
echo [8] Run Logs Filter Script
echo [9] Run All Monitoring Scripts (1, 2, 3)
echo [C] Help
echo [B] Credits
echo [X] Exit

:: Prompt the user for input to choose an option
set /p choice="Enter your choice: "

:: Handle the user input
if "%choice%"=="1" start powershell -NoExit -Command python Opt1_HID_Logger.py
if "%choice%"=="2" start powershell -NoExit -Command python Opt2_USB_Logger.py
if "%choice%"=="3" start powershell -NoExit -Command python Opt3_FileProcess_Logger.py
if "%choice%"=="4" start powershell -NoExit -Command python Opt4_LogsFolder_Archiver.py
if "%choice%"=="5" start powershell -NoExit -Command python Opt5_HID_Logs_Extractor.py
if "%choice%"=="6" start powershell -NoExit -Command python Opt6_USB_Connections_Logs_Extractor.py
if "%choice%"=="7" start powershell -NoExit -Command python Opt7_FileProcess_Logs_Extractor.py
if "%choice%"=="8" start powershell -NoExit -Command python Opt8_filter_logs.py
if "%choice%"=="9" (
    start powershell -NoExit -Command python Opt1_HID_Logger.py
    start powershell -NoExit -Command python Opt2_USB_Logger.py
    start powershell -NoExit -Command python Opt3_FileProcess_Logger.py
)
if /i "%choice%"=="C" goto help_menu
if /i "%choice%"=="B" goto credits
if /i "%choice%"=="X" goto exit

:: If the input is invalid, prompt the user again
echo Invalid choice. Try again!
goto menu

:: Help menu - detailed explanation
:help_menu
echo =======================================
echo               Help Menu
echo =======================================
echo Welcome to the WinPortsLogger tool.
echo 
echo To run the scripts, choose an option from the menu:
echo 
echo - Option 1: Run HID Logger Script (Logs HID devices)
echo - Option 2: Run USB Logger Script (Logs USB devices)
echo - Option 3: Run File Process Logger Script (Logs file processes between host and USB device)
echo - Option 4: Run Logs Folder Archiver Script (Archives logs into 5 different formats)
echo - Option 5: Run HID Logs Extractor Script (Extracts HID logs)
echo - Option 6: Run USB Connections Logs Extractor Script (Extracts USB connections logs)
echo - Option 7: Run File Process Logs Extractor Script (Extracts file process logs)
echo - Option 8: Run Logs Filter Script (Filters logs based on user input)
echo - Option 9: Run All Monitoring Scripts (1, 2, 3) in separate windows
echo 
echo ** Important Note: **
echo - You must run Options 1, 2, and 3 first, as Options 5, 6, 7, and 8 rely on their logs to generate meaningful results.
echo - To simplify the process, use Option 9 to run all 3 monitoring scripts simultaneously and get all the logs.
echo 
echo ** Examples of usage: **
echo - To only extract HID logs, run Option 5 (after running Option 1).
echo - To extract USB connections logs, run Option 6 (after running Option 2).
echo - To filter logs, run Option 8 (after running the respective logger script).
echo 
echo For any specific functionality, feel free to choose from the options and follow the on-screen instructions.
echo =======================================
pause
goto menu

:: Displays credits and author information
:credits
echo =======================================
echo        Credits and Author Info
echo =======================================
echo Created by: Ozz961
echo GitHub: https://github.com/roger-rached-ozz961/WinPortsLogger
echo Version: 1.0
echo =======================================
pause
goto menu

:: Exit the script
:exit
echo Exiting WinPortsLogger. Goodbye!
echo You can re-run the script whenever you're ready.
exit

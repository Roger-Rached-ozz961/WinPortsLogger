# WinPortsLogger

An **interactive and comprehensive batch file** for monitoring and logging USB, HID devices, and file-process operations. This tool provides several options for real-time device tracking and log management.

---

## Features

### Monitoring and Logging
1. **HID Logger (`HID_logger.py`)**  
   - Pulls HID devices and adds them to a `.txt` file.  
   - Actively monitors and appends new HID devices to the log file.

2. **USB Logger (`USB_logger.py`)**  
   - Pulls USB devices and adds them to a `.txt` file.  
   - Actively monitors and appends new USB devices to the log file.

3. **File-Process Logger (`FileProcess_logger.py`)**  
   - Monitors file-process operations (cut, move, copy) between connected USB drives and the host.  
   - Appends results to a `.txt` file.

### Log Management
4. **Archive Logs (`Archive_logs.py`)**  
   - Archives the entire logs folder into five different formats containing the `.txt` log files.

### Results and Filters
5. **Enhanced HID Logs Extractor**  
   - Displays detailed results from the HID Logger.

6. **USB Logs Viewer**  
   - Displays detailed results from the USB Logger.

7. **File-Process Logs Viewer**  
   - Displays detailed results from the File-Process Logger.

8. **Filter Logs**  
   - Provides three filter formats for the log files:
     - HID logs
     - USB logs
     - File-Process logs

### Combined Monitoring
9. **Run All Monitoring**  
   - Activates all monitoring functionalities simultaneously.

### Other Options
- **Detailed Help Menu**  
  - Provides a comprehensive guide on how to use the tool.  
- **Credits**  
  - Displays contributors or relevant acknowledgments.  
- **Exit**  
  - Terminates the program.

---

## Usage Instructions

1. **Run Required Options First**:  
   To ensure other options function correctly:  
   - Start with **Option 1 (HID Logger)**, **Option 2 (USB Logger)**, and **Option 3 (File-Process Logger)**.

2. **Archive Logs**:  
   Use **Option 4** to archive the logs folder only after running options 1, 2, and 3.

3. **View Results**:  
   View individual results using:
   - **Option 5** for HID logs.
   - **Option 6** for USB logs.
   - **Option 7** for File-Process logs.

4. **Apply Filters**:  
   Use **Option 8** to filter the combined logs into specific categories (HID, USB, or File-Process).

5. **Run All Monitoring**:  
   Use **Option 9** to activate all monitoring processes simultaneously.

---

## Requirements

This project requires the following Python packages:  

```text
Brotli==1.1.0  
colorama==0.4.6  
hidapi==0.14.0.post4  
inflate64==1.0.1  
multivolumefile==0.2.3  
psutil==6.1.1  
py7zr==0.22.0  
pybcj==1.0.3  
pycryptodomex==3.21.0  
pyppmd==1.1.1  
pywin32==308  
pyzstd==0.16.2  
rarfile==4.2  
termcolor==2.5.0  
texttable==1.7.0  
watchdog==6.0.0  
WMI==1.5.1  
```

---

## Installation

1. Clone the repository:  

   ```bash
   git clone https://github.com/Roger-Rached-ozz961/WinPortsLogger.git
   cd WinPortsLogger
   ```

2. Install the required dependencies:  

   ```bash
   pip install -r requirements.txt
   ```

3. Run the batch file to interact with the tool:  

   ```bash
   WinPortsLogger.bat
   ```

---

## Notes

- Running **Option 1, 2, and 3** is mandatory for **Option 4, 5, 6, 7, and 8** to work correctly.
- Ensure connected devices remain active during logging to capture all operations.
- Results are stored in `.txt` log files within the `logs` folder.

---

## Credits

Developed by Roger Rached.  

For questions or contributions, contact [Roger Rached](mailto:Roger_Rached@outlook.com).

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


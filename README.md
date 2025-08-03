# NSSECU2 Hacking Tool : Keylogger
    - Uses Tkinter for authorized use
    - Background keystroke logging with timestamps
    - Hotkey (Ctrl+Shift+Q) to stop keylogging
    - Session markers in log file for indication

    > Disclaimer : Must be used in sandbox enviroments only, Stay safe and Ethical!

# Requirement Features
    1. Captures all printable keystrokes in real time.  
    2. Logs keystrokes to keylog.txt with timestamps.  
    3. Runs silently in the background.  
    4. Can be safely stopped via (Ctrl+Shift+Q) hotkey.  
    5. Marks sessions with [SESSION START] and [SESSION END].  
    6. Designed for authorized lab/sandbox use only.  
    7. Handles errors gracefully with clear messages.  


# Installation and Usage

    Required dependencies:
     > pip instal pynput

    Installation:
    1. Download zip file in Github
    2. Clone repository in bash

    Usage: 
    1. Enter python keylogger.py in cmd of directory where you downloaded
    2. Confirm authorization message
    3. Keylogging will start, press (Ctrl+Shift+Q) to stop

    Note: Logs are stored in keylog.txt

    Sample Log File: 
    [SESSION START]
    2025-08-03 21:45:10 - h
    2025-08-03 21:45:11 - e
    2025-08-03 21:45:12 - l
    2025-08-03 21:45:12 - l
    2025-08-03 21:45:13 - o
    2025-08-03 21:45:14 - [Ctrl]
    2025-08-03 21:45:15 - [Shift]
    [SESSION END]

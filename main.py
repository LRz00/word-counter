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
paused = False  
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
    global word_count, tracking, paused
    if not tracking or paused:   
        return
    try:
        if key == keyboard.Key.space:
            word_count += 1
            label.config(text=f"Words typed: {word_count}")
    except AttributeError:
        pass

def toggle_tracking():
    global tracking, word_count, session_start, sessions, paused

    if not tracking:
        paused = False   
        tracking = True
        word_count = 0
        session_start = time.time()
        button.config(text="Turn Off")
        pause_button.config(state="normal", text="Pause")
        label.config(text="Words typed: 0")
    else: 
        save_session()
        button.config(text="Turn On")
        pause_button.config(state="disabled")
        label.config(text=f"Session saved! Words: {word_count}")

def on_close():
    save_session()
    root.destroy()
    sys.exit()


def show_sessions():
    log_window = tk.Toplevel(root)
    log_window.title("Session Log")
    log_window.geometry("400x300")

    text_area = tk.Text(log_window, wrap="word", state="normal")
    text_area.pack(expand=True, fill="both", padx=10, pady=10)

    if not sessions:
        text_area.insert("end", "No sessions recorded yet. \n")
    else:
        for i, s in enumerate(sessions, 1):
            text_area.insert(
                "end",
                f"Session {i}:\n"
                f"  Date: {s['date']}\n"
                f"  Words: {s['words']}\n"
                f"  Duration: {s['duration_minutes']} minutes\n\n"
            )

    text_area.config(state="disabled")


def toggle_pause():
    global paused

    if not paused:
        paused = True
        pause_button.config(text="Unpause")
        label.config(text=f"Paused - Words typed: {word_count}")
    else:
        paused = False
        pause_button.config(text="Pause")
        label.config(text=f"Words typed: {word_count}")


root = tk.Tk()
root.title("Word Counter")
root.attributes("-topmost", True)

label = tk.Label(root, text="Words typed: 0", font=("Arial", 16))
label.pack(pady=10)

button = tk.Button(root, text="Turn On", command=toggle_tracking)
button.pack(pady=10)

pause_button = tk.Button(root, text="Pause", command=toggle_pause, state="disabled")
pause_button.pack(pady=5)

options_button = tk.Button(root, text="📁", command=show_sessions, font=("Arial", 10), width=3)
options_button.pack(pady=5)

listener = keyboard.Listener(on_press=on_press)
listener.start()

root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()

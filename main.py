import tkinter as tk
from pynput import keyboard

word_count = 0
tracking = False

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
    global tracking
    tracking = not tracking
    button.config(text="Turn Off" if tracking else "Turn On")

root = tk.Tk()
root.title("Word Counter")
root.attributes("-topmost", True)

label = tk.Label(root, text="Words typed: 0", font=("Arial", 16))
label.pack(pady=10)

button = tk.Button(root, text="Turn On", command=toggle_tracking)
button.pack(pady=10)

listener = keyboard.Listener(on_press=on_press)
listener.start()

root.mainloop()

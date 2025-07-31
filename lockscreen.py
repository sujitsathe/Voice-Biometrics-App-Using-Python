import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

import tkinter as tk
from tkinter import messagebox
import threading
import os
from utils.recorder import record_voice
from utils.model_utils import verify_user
from utils.folder_locker import lock_folder, unlock_folder
from utils.website_blocker import block_websites, unblock_websites

# ===== CONFIGURATION =====
FOLDER_PATH = r"C:\New folder"  # Make sure this folder exists
BLOCKED_SITES = ["www.facebook.com", "www.instagram.com"]
PIN_FILE = "data/pins.txt"

# ===== FUNCTIONS =====

def load_pins():
    pins = {}
    if os.path.exists(PIN_FILE):
        with open(PIN_FILE, "r") as file:
            for line in file:
                if "," in line:
                    user, pin = line.strip().split(",")
                    pins[user.strip().lower()] = pin.strip()
    return pins

def auto_relock():
    print("🔒 Auto re-lock triggered.")
    lock_folder(FOLDER_PATH)
    block_websites(BLOCKED_SITES)

def handle_unlock():
    status_label.config(text="🎙️ Recording your voice...")
    root.update()

    record_voice("data/verify_lockscreen.wav", duration=5)
    status_label.config(text="🔍 Verifying voice...")
    root.update()

    try:
        user, score = verify_user("data/verify_lockscreen.wav")
        print(f"[DEBUG] Detected user: {user}, Confidence: {score}")

        if score > 0.75:
            pin = pin_entry.get()
            pins = load_pins()

            user_clean = user.strip().lower()
            pin_entered = pin.strip()

            if user_clean in pins and pin_entered == pins[user_clean]:
                status_label.config(text=f"✅ Welcome {user}! Folder Unlocked.")
                unlock_folder(FOLDER_PATH)
                unblock_websites(BLOCKED_SITES)
                os.startfile(FOLDER_PATH)
                threading.Timer(600, auto_relock).start()
                root.after(1500, root.destroy)
            else:
                messagebox.showerror("Access Denied", "❌ Incorrect PIN.")
                status_label.config(text="❌ Incorrect PIN")
        else:
            messagebox.showerror("Access Denied", f"❌ Voice not recognized. Confidence: {score:.2f}")
            status_label.config(text="❌ Voice Not Recognized")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        status_label.config(text="⚠️ Error Occurred")

# ===== UI SETUP =====
root = tk.Tk()
root.attributes('-fullscreen', True)
root.configure(bg='black')
root.title("Voice + PIN Unlock")

title_label = tk.Label(root, text="🔐 Speak & Enter PIN to Unlock", fg="white", bg="black", font=("Helvetica", 32))
title_label.pack(pady=40)

pin_label = tk.Label(root, text="Enter PIN:", fg="white", bg="black", font=("Helvetica", 20))
pin_label.pack(pady=10)

pin_entry = tk.Entry(root, show="*", font=("Helvetica", 20), width=10, justify='center')
pin_entry.pack(pady=10)

unlock_btn = tk.Button(root, text="🎤 Speak & Verify", font=("Helvetica", 24), command=handle_unlock)
unlock_btn.pack(pady=20)

status_label = tk.Label(root, text="", fg="green", bg="black", font=("Helvetica", 20))
status_label.pack(pady=30)

def close(event):
    root.destroy()

root.bind('<Escape>', close)

root.mainloop()

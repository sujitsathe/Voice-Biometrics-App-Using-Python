import os

PIN_FILE = "data/pins.txt"
os.makedirs("data", exist_ok=True)
if not os.path.exists(PIN_FILE):
    with open(PIN_FILE, "w") as f: f.write("")

def save_pin(username, pin):
    with open(PIN_FILE, "a") as f:
        f.write(f"{username}:{pin}\n")

def get_pin(username):
    with open(PIN_FILE, "r") as f:
        for line in f:
            if line.startswith(username + ":"):
                return line.strip().split(":")[1]
    return None
import streamlit as st
import sounddevice as sd
from scipy.io.wavfile import write
import os
import numpy as np
import time
from utils.model_utils import verify_user, list_registered_users

st.set_page_config(page_title="Voice Biometrics Dashboard", layout="centered")
st.title("🎙️ Voice Biometrics Registration & Verification")

st.markdown("---")

# ===== Utility Functions =====
def record_audio(filename, duration=5, fs=44100):
    st.info("🎤 Recording... Please speak clearly.")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    write(filename, fs, audio)
    st.success("✅ Recording complete.")
    return filename

def save_pin(username, pin):
    os.makedirs("data", exist_ok=True)
    lines = []
    if os.path.exists("data/pins.txt"):
        with open("data/pins.txt", "r") as f:
            lines = f.readlines()
        lines = [line for line in lines if not line.startswith(username + ",")]
    lines.append(f"{username},{pin}\n")
    with open("data/pins.txt", "w") as f:
        f.writelines(lines)

# ===== State =====
if "threshold" not in st.session_state:
    st.session_state.threshold = 0.75

# ===== Tabs =====
tabs = st.tabs(["🔐 Register", "🔎 Verify", "⚙️ Settings"])

with tabs[0]:
    st.header("Register Your Voice + PIN")
    username = st.text_input("👤 Enter your username:", value="sujit")
    pin = st.text_input("🔐 Create a PIN:", type="password")
    if st.button("🎙️ Record & Save"):
        if username.strip() == "" or pin.strip() == "":
            st.warning("Please enter both username and PIN.")
        else:
            path = f"data/data/{username}.wav"
            record_audio(path)
            save_pin(username.strip().lower(), pin.strip())
            st.success(f"✅ Voice & PIN saved for user: {username}")
            st.audio(path)

with tabs[1]:
    st.header("Verify Voice + PIN")
    users = list_registered_users("data/data")
    selected_user = st.selectbox("Select User to Verify Against:", users)
    if st.button("🧪 Verify Now"):
        path = "data/verify_lockscreen.wav"
        record_audio(path)
        st.audio(path)
        try:
            user, score = verify_user(path)
            st.write(f"Voice Match: {user} | Confidence: {score:.2f}")
            if user == selected_user and score > st.session_state.threshold:
                pin = st.text_input("🔐 Enter your PIN to unlock:", type="password")
                if pin:
                    with open("data/pins.txt", "r") as f:
                        pins = {u.strip().lower(): p.strip() for u, p in (line.strip().split(",") for line in f if "," in line)}
                    if user.strip().lower() in pins and pin.strip() == pins[user.strip().lower()]:
                        st.success("🔓 Access Granted!")
                    else:
                        st.error("❌ Incorrect PIN")
            else:
                st.error("❌ Voice verification failed or confidence too low")
        except Exception as e:
            st.error(f"Error: {e}")

with tabs[2]:
    st.header("System Settings")
    threshold = st.slider("Voice match threshold:", 0.5, 0.95, st.session_state.threshold, 0.01)
    if threshold != st.session_state.threshold:
        st.session_state.threshold = threshold
        st.success(f"Threshold updated to {threshold:.2f}")

    if st.button("🗑️ Reset All Voices & PINs"):
        import shutil
        try:
            shutil.rmtree("data/data")
            os.remove("data/pins.txt")
            st.success("✅ All data cleared.")
        except FileNotFoundError:
            st.warning("Nothing to delete.")

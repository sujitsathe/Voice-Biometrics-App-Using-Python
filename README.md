# 🔐 Voice Biometrics Authentication System

This project uses **SpeechBrain** for speaker verification and provides a **secure authentication system** that unlocks folders and grants website access based on the **user's voice and PIN**.

---

## 🎯 Features

- 🎙️ **Voice-based user authentication** using SpeechBrain
- 👥 **Multi-user support**
- 🔐 **PIN verification** after voice match
- 📁 **Folder unlocking** after successful authentication
- 🌐 **Website access control**
- 💻 **Streamlit dashboard** for registration and verification
- 🔒 **Tkinter lockscreen** for real-time secure access
- 🧠 Based on **state-of-the-art ECAPA-TDNN speaker recognition**

---

## 🚀 Getting Started

### 1. Clone this repository

```bash
git clone https://github.com/sujitsathe/Voice-Biometrics-App-Using-Python.git
cd Voice-Biometrics-App-Using-Python

### 2. Install Dependencies
pip install -r requirements.txt

🧪 How It Works
✅ Register
Launch the dashboard:
streamlit run app.py

Go to the Register tab.

Enter your username and PIN.

Record your voice.

Your voice and PIN are saved for verification.

🔓 Unlock
Run the lockscreen:
python lockscreen.py

Speak when prompted.

Enter your PIN.

If both match, your folder is unlocked and websites unblocked.

🛠️ Tech Stack
Technology	                   Purpose
Python	                       Core language
SpeechBrain	             Voice biometrics (ECAPA-TDNN)
Streamlit                      Web dashboard
Tkinter	                       Desktop lockscreen GUI
sounddevice	              Voice recording
threading	                  Auto-lock logic
os / webbrowser	          Folder & website control

🔐 Security Notes
No passwords or PINs are stored in plaintext online.

Voice models and verification done locally for privacy.

Hosts file is NOT modified; websites are controlled safely.





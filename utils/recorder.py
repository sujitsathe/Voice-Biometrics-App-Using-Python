import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import os

def record_voice(filepath, duration=5, fs=16000):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    print("🎤 Recording started...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    write(filepath, fs, audio)
    print("✅ Recording finished.")

# enroll_sujit_embed.py
from resemblyzer import VoiceEncoder, preprocess_wav
from pathlib import Path
import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wav
import os

SAMPLE_RATE = 16000
DURATION = 4
VOICE_DIR = "voiceprint"
os.makedirs(VOICE_DIR, exist_ok=True)

def record_and_enroll():
    print("🎙️ Recording your voice for enrollment...")
    audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1)
    sd.wait()
    wav.write("temp_enroll.wav", SAMPLE_RATE, audio)

    wav_f = preprocess_wav("temp_enroll.wav")
    encoder = VoiceEncoder()
    embed = encoder.embed_utterance(wav_f)

    np.save(os.path.join(VOICE_DIR, "sujit_embed.npy"), embed)
    print("✅ Sujit's speaker embedding saved.")

if __name__ == "__main__":
    record_and_enroll()

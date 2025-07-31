# verify_and_unlock_embed.py
from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wav
import os
from sklearn.metrics.pairwise import cosine_similarity

SAMPLE_RATE = 16000
DURATION = 4
FOLDER_PATH = r"C:\secure_folder"  # 🔁 your path here

def record_and_verify():
    print("🔒 Speak to verify...")
    audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1)
    sd.wait()
    wav.write("temp_verify.wav", SAMPLE_RATE, audio)

    encoder = VoiceEncoder()
    wav_f = preprocess_wav("temp_verify.wav")
    test_embed = encoder.embed_utterance(wav_f)

    registered_embed = np.load("voiceprint/sujit_embed.npy")
    score = cosine_similarity([test_embed], [registered_embed])[0][0]
    print(f"🔍 Similarity score: {score:.4f}")

    if score >= 0.75:
        print("✅ Verified! Unlocking folder...")
        os.startfile(FOLDER_PATH)
    else:
        print("❌ Access Denied. Voice doesn't match.")

if __name__ == "__main__":
    record_and_verify()

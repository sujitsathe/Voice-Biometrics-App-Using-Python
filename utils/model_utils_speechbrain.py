
import torch
import torchaudio
import os
from speechbrain.pretrained import SpeakerRecognition

# Load the pretrained model
verification = SpeakerRecognition.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir="pretrained_models/spkrec-ecapa-voxceleb")

# Function to verify a speaker
def verify_user(test_audio_path, reference_path="data/data/sujit.wav", threshold=0.75):
    score, prediction = verification.verify_files(reference_path, test_audio_path)
    return "sujit", float(score)

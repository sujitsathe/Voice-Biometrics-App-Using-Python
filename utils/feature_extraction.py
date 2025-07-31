import librosa
import numpy as np
import os

def extract_features(filepath, n_mfcc=13):
    y, sr = librosa.load(filepath, sr=None)
    
    # Extract features
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)

    # Mean pooling to reduce dimensions
    mfccs_mean = np.mean(mfccs.T, axis=0)
    chroma_mean = np.mean(chroma.T, axis=0)
    contrast_mean = np.mean(spectral_contrast.T, axis=0)

    # Combine all features
    combined = np.hstack([mfccs_mean, chroma_mean, contrast_mean])
    return combined

# Test
if __name__ == "__main__":
    test_path = os.path.join("data", "test_user.wav")
    features = extract_features(test_path)
    print("Feature vector shape:", features.shape)

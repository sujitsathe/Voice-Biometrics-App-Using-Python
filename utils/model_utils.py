import os
from speechbrain.inference import SpeakerRecognition
model = SpeakerRecognition.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb",
    savedir="pretrained_models/spkrec-ecapa-voxceleb"
)

def list_registered_users(folder="data/data"):
    return [f.replace(".wav", "") for f in os.listdir(folder) if f.endswith(".wav")]

def verify_user(test_path, user_folder="data/data"):
    best_score, best_user = 0, "unknown"
    for filename in os.listdir(user_folder):
        if filename.endswith(".wav"):
            ref_path = os.path.join(user_folder, filename)
            try:
                score, _ = model.verify_files(ref_path, test_path)
                if score.item() > best_score:
                    best_score = score.item()
                    best_user = filename.replace(".wav", "")
            except: continue
    return best_user, best_score
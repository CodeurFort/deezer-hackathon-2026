"""Étape 1 (PyTorch) : voix et instruments isolés par Demucs, temps par Beat This!, accords par lv-chordia si absents."""
import sys, os, json, warnings, numpy as np, torch, librosa, soundfile as sf
warnings.filterwarnings("ignore")
from demucs.api import Separator
from beat_this.inference import File2Beats
from lv_chordia.chord_recognition import chord_recognition
sep = Separator(model="htdemucs"); f2b = File2Beats(checkpoint_path="final0", device="cpu", dbn=False)
for fic in sys.argv[1:]:
    mp3 = os.path.abspath(f"extraits/{fic}.mp3")
    y, _ = librosa.load(mp3, sr=sep.samplerate, mono=False)
    if y.ndim == 1: y = np.stack([y, y])
    _, st = sep.separate_tensor(torch.tensor(y, dtype=torch.float32), sep.samplerate)
    for nom in ("vocals", "other"): sf.write(f"pistes/{fic}_{nom}.wav", st[nom].numpy().T, sep.samplerate)
    a, b = f2b(mp3); beats = a if len(a) >= len(b) else b
    json.dump([float(x) for x in beats], open(f"pistes/{fic}_temps.json", "w"))
    js = f"extraits/{fic}.accords.json"
    if not os.path.exists(js): json.dump(chord_recognition(audio_path=mp3, chord_dict_name="submission"), open(js, "w"))
    print("prêt :", fic)

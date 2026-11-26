"""Type de basse (808, reese, basse guitare, basse synthé) : basse isolée par Demucs, puis six signatures acoustiques.
Exploration du 26/11/2026 : on regarde si les types se séparent, sans encore de classifieur."""
import sys, os, warnings, numpy as np, torch, librosa, soundfile as sf
warnings.filterwarnings("ignore")
from demucs.api import Separator
sep = Separator(model="htdemucs")
def signatures(fic):
    y, sr = librosa.load(f"extraits/{fic}.mp3", sr=sep.samplerate, mono=False)
    if y.ndim == 1: y = np.stack([y, y])
    _, stems = sep.separate_tensor(torch.tensor(y, dtype=torch.float32), sep.samplerate)
    b = stems["bass"].numpy(); sf.write(f"basses/{fic}_basse.wav", b.T, sep.samplerate)
    mono = b.mean(axis=0); mid, side = (b[0] + b[1]) / 2, (b[0] - b[1]) / 2
    S = np.abs(librosa.stft(mono, n_fft=8192, hop_length=2048)) ** 2; f = librosa.fft_frequencies(sr=sep.samplerate, n_fft=8192)
    e = lambda lo, hi: S[(f >= lo) & (f < hi)].sum()
    sub = e(20, 80) / (e(20, 400) or 1)                                   # part de sub-basse
    riche = e(250, 2000) / (e(20, 250) or 1)                              # harmoniques au-dessus du fondamental
    y22 = librosa.resample(mono, orig_sr=sep.samplerate, target_sr=22050)
    f0, voiced, _ = librosa.pyin(y22, fmin=30, fmax=300, sr=22050, frame_length=4096, hop_length=512)
    st = 12 * np.log2(np.where(voiced, f0, np.nan) / 55.0)
    pente = np.abs(np.diff(st)) / (512 / 22050)                           # demi-tons par seconde
    continu = voiced[1:] & voiced[:-1]
    glisse = np.nanmean((pente[continu] > 8) & (pente[continu] < 60)) if continu.any() else np.nan  # glissés (pas les sauts de note)
    seg, n = [], 0                                                        # tenue : durée des passages voisés
    for v in voiced:
        if v: n += 1
        elif n: seg.append(n); n = 0
    tenue = np.median(seg) * 512 / 22050 if seg else np.nan
    env = librosa.feature.rms(y=y22, frame_length=1024, hop_length=220)[0]   # pulsation : modulation 2-12 Hz de l'enveloppe
    E = np.abs(np.fft.rfft(env - env.mean())); fe = np.fft.rfftfreq(len(env), 220 / 22050)
    puls = E[(fe >= 2) & (fe < 12)].sum() / (E[(fe > 0) & (fe < 2)].sum() or 1)
    largeur = (side ** 2).sum() / ((mid ** 2).sum() or 1)
    return sub, riche, glisse, tenue, puls, largeur
if __name__ == "__main__":
    print(f"{'extrait':18s} {'sub<80Hz':>8s} {'harmon.':>8s} {'glissés':>8s} {'tenue(s)':>8s} {'pulsat.':>8s} {'stéréo':>7s}")
    for fic in sys.argv[1:]:
        s = signatures(fic)
        print(f"{fic:18s} {s[0]:8.0%} {s[1]:8.2f} {s[2]:8.1%} {s[3]:8.2f} {s[4]:8.2f} {s[5]:7.2f}")

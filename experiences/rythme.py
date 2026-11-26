"""Rythme par bandes de fréquences : où tombent les frappes graves (kick), médiums (caisse claire, percussions)
et aiguës (charleston, shakers) sur une grille de 16 doubles-croches. Mesure du 26/11/2026."""
import sys, warnings, numpy as np, librosa, scipy.signal as sg
warnings.filterwarnings("ignore")
BANDES = {"graves (kick)": (30, 120), "médiums (caisse claire, percus)": (150, 2500), "aigus (charleston, shakers)": (6000, 11000)}
def filtre(y, sr, lo, hi):
    b, a = sg.butter(4, [lo / (sr / 2), min(hi / (sr / 2), 0.99)], btype='band'); return sg.filtfilt(b, a, y)
def analyse(f):
    y, sr = librosa.load(f, sr=22050, mono=True)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units='time')
    tempo = float(np.atleast_1d(tempo)[0])
    if len(beats) < 9: return None
    # grille : 4 doubles-croches par temps, mesures de 4 temps calées sur le premier temps détecté
    grille = np.concatenate([np.linspace(b0, b1, 4, endpoint=False) for b0, b1 in zip(beats[:-1], beats[1:])])
    nb = (len(grille) // 16) * 16; grille = grille[:nb]
    res = {"tempo": tempo}
    occupees = np.zeros(nb, bool)
    for nom, (lo, hi) in BANDES.items():
        env = librosa.onset.onset_strength(y=filtre(y, sr, lo, hi), sr=sr)
        on = librosa.onset.onset_detect(onset_envelope=env, sr=sr, units='time', backtrack=False)
        pas = np.zeros(nb)
        for t in on:
            i = np.argmin(np.abs(grille - t))
            if abs(grille[i] - t) < 0.06: pas[i] = 1
        occupees |= pas > 0
        motif = pas.reshape(-1, 16).mean(axis=0)                     # fréquence de frappe par position dans la mesure
        res[nom] = {"motif": motif, "densite": pas.sum() / (nb / 16),
                    "contretemps": pas.reshape(-1, 16)[:, [1, 3, 5, 7, 9, 11, 13, 15]].sum() / max(pas.sum(), 1)}
    res["air"] = 1 - occupees.mean()                                  # part des doubles-croches sans aucune frappe
    return res
if __name__ == "__main__":
    for f in sys.argv[1:]:
        r = analyse(f)
        if not r: print(f, ": pas assez de temps détectés"); continue
        print(f"\n{f.split('/')[-1]} | tempo {r['tempo']:.0f} | air {r['air']:.0%}")
        for nom in BANDES:
            m = r[nom]; ligne = "".join("X" if v >= .6 else "x" if v >= .3 else "." for v in m["motif"])
            print(f"  {nom:32s} {ligne[:4]} {ligne[4:8]} {ligne[8:12]} {ligne[12:]} | {m['densite']:4.1f} frappes/mesure | contretemps {m['contretemps']:.0%}")

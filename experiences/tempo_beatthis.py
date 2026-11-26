"""Tempo, mesure et rythme harmonique avec Beat This! (temps et débuts de mesure) et les accords de lv-chordia."""
import sys, json, os, warnings, numpy as np
warnings.filterwarnings("ignore")
from beat_this.inference import File2Beats
f2b = File2Beats(checkpoint_path="final0", device="cpu", dbn=False)
res = {}
for fic in sys.argv[1:]:
    a, b = f2b(os.path.abspath(f"extraits/{fic}.mp3"))
    beats, downs = (a, b) if len(a) >= len(b) else (b, a)
    ibi = np.median(np.diff(beats)); bpm = 60 / ibi
    par_mesure = float(np.median(np.diff(downs)) / ibi) if len(downs) > 1 else None
    rh = None
    js = f"extraits/{fic}.accords.json"
    if os.path.exists(js):
        segs = [x for x in json.load(open(js)) if x['chord'] not in ('N', 'X')]
        fusion = []
        for x in segs:
            if fusion and fusion[-1]['chord'] == x['chord']: fusion[-1]['end_time'] = x['end_time']
            else: fusion.append(dict(x))
        durees = [(x['end_time'] - x['start_time']) / ibi for x in fusion[1:-1]]   # premiers et derniers coupés par l'extrait
        rh = float(np.median(durees)) if durees else None
    res[fic] = {"bpm": bpm, "temps_par_mesure": par_mesure, "temps_par_accord": rh}
json.dump(res, open("tempo_beatthis.json", "w"))

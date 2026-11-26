"""Étape 2 (Basic Pitch) : notes seules ou accords dans les instruments, et appoggiatures dans la voix
(note étrangère à l'accord, posée sur un temps, qui se résout d'un demi-ton ou d'un ton vers une note de l'accord)."""
import sys, json, warnings, contextlib, io, numpy as np
warnings.filterwarnings("ignore")
from basic_pitch.inference import predict
NOTES = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
ALIAS = {'Db':'C#','Eb':'D#','Gb':'F#','Ab':'G#','Bb':'A#','Cb':'B','Fb':'E'}
TONS = {'maj': (0,4,7), 'min': (0,3,7), '7': (0,4,7,10), 'maj7': (0,4,7,11), 'min7': (0,3,7,10), 'dim': (0,3,6), 'hdim7': (0,3,6,10),
        'sus2': (0,2,7), 'sus4': (0,5,7), 'maj6': (0,4,7,9), 'min6': (0,3,7,9), '9': (0,4,7,10,2), 'aug': (0,4,8), 'dim7': (0,3,6,9), 'minmaj7': (0,3,7,11)}
def notes(wav, fmin=None):
    with contextlib.redirect_stdout(io.StringIO()):
        _, _, ev = predict(wav, minimum_frequency=fmin)
    return [(s, e, p, a) for s, e, p, a, _ in ev]
def accord_a(t, acc):
    for x in acc:
        if x['start_time'] <= t < x['end_time'] and x['chord'] not in ('N', 'X'):
            r, _, q = x['chord'].partition(':'); r = NOTES.index(ALIAS.get(r, r)); q = (q or 'maj').split('/')[0]
            return {(r + i) % 12 for i in TONS.get(q, TONS['min' if q.startswith('min') else 'maj'])}
    return None
def polyphonie(ev, duree):
    pas = np.arange(0, duree, .05); n = np.array([sum(1 for s, e, p, a in ev if s <= t < e) for t in pas])
    actif = n > 0
    if not actif.any(): return 0, 0, 0
    return (n[actif] == 1).mean(), (n[actif] == 2).mean(), (n[actif] >= 3).mean()
def melodie(ev):  # ligne la plus haute, notes d'au moins 120 ms
    ev = sorted([x for x in ev if x[1] - x[0] >= .12], key=lambda x: (x[0], -x[2]))
    ligne = []
    for s, e, p, a in ev:
        if ligne and s < ligne[-1][1] - .05:
            if p > ligne[-1][2]: ligne[-1] = (s, e, p, a)
            continue
        ligne.append((s, e, p, a))
    return ligne
def appoggiatures(ligne, acc, temps):
    temps = np.array(temps); ibi = np.median(np.diff(temps)) if len(temps) > 1 else .5
    trouvees, etrangeres = [], 0
    for (s, e, p, a), (s2, e2, p2, a2) in zip(ligne, ligne[1:]):
        tons = accord_a(s + .02, acc)
        if tons is None or not len(temps): continue
        sur_temps = np.min(np.abs(temps - s)) < .08
        if sur_temps and p % 12 not in tons:
            etrangeres += 1
            if s2 - e < ibi and abs(p2 - p) in (1, 2) and (accord_a(s2 + .02, acc) or set()) and p2 % 12 in accord_a(s2 + .02, acc):
                trouvees.append((round(float(s), 2), NOTES[p % 12], NOTES[p2 % 12]))
    return trouvees, etrangeres
if __name__ == "__main__":
    print(f"{'extrait':16s} | instruments : 1 note  2 notes  3+ (accords) | voix : notes  étrangères sur temps  appoggiatures (/min)")
    for fic in sys.argv[1:]:
        acc = json.load(open(f"extraits/{fic}.accords.json")); temps = json.load(open(f"pistes/{fic}_temps.json"))
        inst = notes(f"pistes/{fic}_other.wav", fmin=80)
        un, deux, trois = polyphonie(inst, 30.0)
        ligne = melodie(notes(f"pistes/{fic}_vocals.wav", fmin=80))
        app, etr = appoggiatures(ligne, acc, temps)
        print(f"{fic:16s} | {un:12.0%} {deux:7.0%} {trois:8.0%} | {len(ligne):10d} {etr:12d} {len(app) * 2:14d}   ex. {app[:3]}")

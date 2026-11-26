"""Compare lv-chordia (deep learning) aux accords attendus, sans tenir compte de la tonalité."""
import json, re, os, sys, time, urllib.request, urllib.parse, warnings
warnings.filterwarnings("ignore")
from lv_chordia.chord_recognition import chord_recognition
NOTES = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
ALIAS = {'Db':'C#','Eb':'D#','Gb':'F#','Ab':'G#','Bb':'A#','Cb':'B','Fb':'E','E#':'F','B#':'C'}
MINEURS = {'min','min7','minmaj7','min6','min9','min11','dim','dim7','hdim7'}
def racine(n): return NOTES.index(ALIAS.get(n, n))
def attendu(ch):  # "Am7" -> (racine, qualité au format Harte)
    m = re.match(r'^([A-G][#b]?)(.*)$', ch); q = m.group(2)
    table = {'': 'maj', 'm': 'min', 'm7': 'min7', '7': '7', 'maj7': 'maj7', 'm7b5': 'hdim7', '6': 'maj6'}
    return racine(m.group(1)), table[q]
def detecte(label):  # "A:min7/b3" -> (racine, qualité) ; "N" -> None
    if label in ('N', 'X'): return None
    r, _, q = label.partition(':'); q = (q or 'maj').split('/')[0].split('(')[0]
    return racine(r), q
CAS = {
 "triades": [("Let It Be","The Beatles","C G Am F"),("Hit the Road Jack","Ray Charles","Am G F E"),("Knockin' On Heaven's Door","Bob Dylan","G D Am C"),
             ("Stand By Me","Ben E. King","A F#m D E"),("Get Lucky","Daft Punk","Bm D F#m E"),("Someone Like You","Adele","A E F#m D"),
             ("Zombie","The Cranberries","Em C G D"),("Wake Me Up","Avicii","Bm G D A"),("Shape of You","Ed Sheeran","C#m F#m A B"),("Despacito","Luis Fonsi","Bm G D A")],
 "septiemes": [("Moondance","Van Morrison","Am7 Bm7"),("Isn't She Lovely","Stevie Wonder","C#m7 F#7 B E"),("Get Lucky","Daft Punk","Bm7 D F#m7 E"),
               ("Fly Me To The Moon","Frank Sinatra","Am7 Dm7 G7 Cmaj7"),("Smooth","Santana","Am F E7")]}
def extrait(titre, artiste):
    f = f"extraits/{re.sub(r'[^a-z0-9]', '', titre.lower())}.mp3"
    if os.path.exists(f): return f
    q = urllib.parse.urlencode({"q": f"{artiste} {titre}", "limit": 10})
    d = json.load(urllib.request.urlopen(urllib.request.Request("https://api.deezer.com/search?" + q, headers={"User-Agent": "Mozilla/5.0"}), timeout=15))
    for h in d.get('data', []):
        if artiste.lower().split()[-1] in h['artist']['name'].lower() and h.get('preview'):
            urllib.request.urlretrieve(h['preview'], f); return f
    return None
def evaluer(segs, exp):
    best = None
    for s in range(12):
        cible = {((r + s) % 12, q) for r, q in exp}
        cible_triade = {((r + s) % 12, q in MINEURS) for r, q in exp}
        tot = sum(d for _, d in segs) or 1
        triade = sum(d for c, d in segs if c and (c[0], c[1] in MINEURS) in cible_triade) / tot
        exact = sum(d for c, d in segs if c and c in cible) / tot
        if best is None or (triade, exact) > best[:2]: best = (triade, exact, s)
    return best
res = {}
for groupe, cas in CAS.items():
    for titre, artiste, att in cas:
        f = extrait(titre, artiste)
        if not f: print(f"- {titre} : pas d'extrait"); continue
        t0 = time.time(); out = chord_recognition(audio_path=os.path.abspath(f), chord_dict_name="submission"); dt = time.time() - t0
        segs = [(detecte(x['chord']), x['end_time'] - x['start_time']) for x in out]
        exp = [attendu(c) for c in att.split()]
        triade, exact, s = evaluer(segs, exp)
        res.setdefault(groupe, []).append((triade, exact))
        lab = " ".join(x['chord'] for x in out if x['chord'] != 'N')[:150]
        print(f"- [{groupe}] {titre} : temps sur les bonnes triades {triade:.0%} | sur l'accord exact (septièmes comprises) {exact:.0%} | {dt:.1f} s\n    attendu {att} | détecté : {lab}")
for g, v in res.items():
    print(f"=> {g} : bonnes triades {sum(x for x, _ in v)/len(v):.0%} | accord exact {sum(y for _, y in v)/len(v):.0%} (moyenne sur {len(v)} morceaux)")

# Part du temps sur des accords enrichis (septièmes, neuvièmes, sixtes, demi-diminués…), morceau par morceau
SIMPLES = {'maj', 'min'}
print("\nPart d'accords enrichis par morceau :")
for groupe, cas in CAS.items():
    for titre, artiste, _ in cas:
        f = extrait(titre, artiste)
        out = chord_recognition(audio_path=os.path.abspath(f), chord_dict_name="submission")
        tot = sum(x['end_time'] - x['start_time'] for x in out if x['chord'] != 'N') or 1
        riche = sum(x['end_time'] - x['start_time'] for x in out if x['chord'] != 'N' and detecte(x['chord'])[1] not in SIMPLES)
        print(f"  [{groupe}] {titre:28s} {riche/tot:5.0%}")

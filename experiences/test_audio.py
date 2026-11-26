import json, re, urllib.request, urllib.parse, os, warnings
warnings.filterwarnings("ignore")
import essentia; essentia.log.infoActive = False; essentia.log.warningActive = False
import essentia.standard as es
NOTES = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
ALIAS = {'Db':'C#','Eb':'D#','Gb':'F#','Ab':'G#','Bb':'A#'}
def parse(ch):
    m = re.match(r'^([A-G][#b]?)(m?)', ch); root = ALIAS.get(m.group(1), m.group(1)); return NOTES.index(root), m.group(2) == 'm'
def shift(ch, s): r, minor = ch; return ((r + s) % 12, minor)
CAS = [  # (titre, artiste, suite attendue, en tonalité d'origine)
 ("Let It Be", "The Beatles", "C G Am F"), ("Hit the Road Jack", "Ray Charles", "Am G F E"),
 ("Knockin' On Heaven's Door", "Bob Dylan", "G D Am C"), ("Stand By Me", "Ben E. King", "A F#m D E"),
 ("Get Lucky", "Daft Punk", "Bm D F#m E"), ("Someone Like You", "Adele", "A E F#m D"),
 ("Zombie", "The Cranberries", "Em C G D"), ("Wake Me Up", "Avicii", "Bm G D A"),
 ("Shape of You", "Ed Sheeran", "C#m F#m A B"), ("Despacito", "Luis Fonsi", "Bm G D A")]
def deezer_preview(t, a):
    d = json.load(urllib.request.urlopen(urllib.request.Request("https://api.deezer.com/search?" + urllib.parse.urlencode({"q": f"{a} {t}", "limit": 10}), headers={"User-Agent": "Mozilla/5.0"}), timeout=15))
    for h in d.get('data', []):
        if a.lower().split()[-1] in h['artist']['name'].lower() and h.get('preview'): return h['preview'], h['title']
    return None, None
resultats = []
for titre, artiste, attendu in CAS:
    url, trouve = deezer_preview(titre, artiste)
    if not url: print(f"- {titre} : pas d'extrait"); continue
    f = f"extraits/{re.sub(r'[^a-z0-9]', '', titre.lower())}.mp3"
    if not os.path.exists(f): urllib.request.urlretrieve(url, f)
    audio = es.MonoLoader(filename=f, sampleRate=44100)()
    te = es.TonalExtractor(); out = dict(zip(te.outputNames(), te(audio)))
    prog, key, scale = out['chords_progression'], out['key_key'], out['key_scale']
    # segments : fusion des trames identiques, on ignore les segments < 0,5 s (trame ~ 46 ms)
    segs = []
    for c in prog:
        if segs and segs[-1][0] == c: segs[-1][1] += 1
        else: segs.append([c, 1])
    segs = [(c, n) for c, n in segs if n >= 11]
    exp = [parse(c) for c in attendu.split()]
    best = (0, 0)
    for s in range(12):
        tgt = {shift(c, s) for c in exp}
        dur_ok = sum(n for c, n in segs if parse(c) in tgt); tot = sum(n for _, n in segs) or 1
        best = max(best, (dur_ok / tot, s))
    precision, s = best
    found = {shift(c, s) for c in exp} & {parse(c) for c, _ in segs}
    seq = " ".join(c for c, _ in segs[:14])
    resultats.append(precision)
    print(f"- {titre} ({trouve}) | tonalité détectée {key} {scale} | attendu {attendu} | accords attendus retrouvés {len(found)}/{len(exp)} | temps sur des accords attendus {precision:.0%}\n    détecté : {seq}")
print(f"=> moyenne du temps passé sur les bons accords : {sum(resultats)/len(resultats):.0%} sur {len(resultats)} morceaux")

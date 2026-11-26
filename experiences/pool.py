import json, urllib.request, os, time, warnings
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
warnings.filterwarnings("ignore")
UA = {"User-Agent": "deezer-hackathon-feasibility/0.1"}
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30))
def dl(t):
    f = f"pool/{t['id']}.mp3"
    if not os.path.exists(f): urllib.request.urlretrieve(t['preview'], f)
    return f
def analyse(arg):
    import essentia; essentia.log.infoActive = False; essentia.log.warningActive = False
    import essentia.standard as es
    from basse_audio import basse
    f, meta = arg
    tempo, seq, desc = basse(f)
    te = es.TonalExtractor(); out = dict(zip(te.outputNames(), te(es.MonoLoader(filename=f, sampleRate=44100)())))
    return {**meta, "lignes_desc": len(desc), "tonalite": f"{out['key_key']} {out['key_scale']}"}
if __name__ == "__main__":
    t0 = time.time(); tracks = []
    for name, pid in [("Top France", 1109890291), ("Top Monde", 3155776842)]:
        for t in get(f"https://api.deezer.com/playlist/{pid}?limit=100")['tracks']['data']:
            if t.get('preview'): tracks.append({"id": t['id'], "titre": t['title'], "artiste": t['artist']['name'], "liste": name, "preview": t['preview']})
    with ThreadPoolExecutor(8) as p: files = list(p.map(dl, tracks))
    t1 = time.time()
    with ProcessPoolExecutor(8) as p: res = list(p.map(analyse, [(f, {k: t[k] for k in ("titre", "artiste", "liste")}) for f, t in zip(files, tracks)]))
    t2 = time.time()
    json.dump(res, open('pool_resultats.json', 'w'), ensure_ascii=False)
    print(f"{len(res)} extraits | téléchargement {t1-t0:.0f} s | analyse {t2-t1:.0f} s ({(t2-t1)/len(res):.2f} s par extrait en parallèle)")
    for liste in ("Top France", "Top Monde"):
        r = [x for x in res if x["liste"] == liste]; d = [x for x in r if x["lignes_desc"] >= 2]
        print(f"{liste} : basse descendante (2 lignes ou plus) dans {len(d)}/{len(r)} | ex. : {[x['titre'] + ' / ' + x['artiste'] for x in sorted(d, key=lambda x: -x['lignes_desc'])[:6]]}")

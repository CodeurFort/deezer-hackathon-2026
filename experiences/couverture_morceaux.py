import json, urllib.request, urllib.parse, re, time
from concurrent.futures import ThreadPoolExecutor
d = json.load(open('couverture_artistes.json')); pl = json.load(open('playlists.json'))
ids, rows = d["ids"], d["rows"]
present = {n for n, v in ids.items() if any(rows.get(s) for s in v)}
def norm(s):
    s = (s or '').lower(); s = re.sub(r'\s*[\(\[].*?[\)\]]', '', s); s = re.sub(r'\s+-\s+.*$', '', s)
    return re.sub(r'[^a-z0-9]', '', s)
def title(song_id):
    for i in range(3):
        try:
            u = "https://open.spotify.com/oembed?url=" + urllib.parse.quote("https://open.spotify.com/track/" + song_id)
            return song_id, json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=15)).get('title')
        except Exception: time.sleep(1.5 * (i + 1))
    return song_id, None
todo = sorted({x for a in present for s in ids[a] for x in rows.get(s, []) if x})
with ThreadPoolExecutor(max_workers=4) as pool: titles = dict(pool.map(title, todo))
json.dump(titles, open('titres_spotify.json', 'w'), ensure_ascii=False)
print("titres récupérés :", sum(1 for v in titles.values() if v), "/", len(todo))
for name, tracks in pl.items():
    hits = []
    for t, a in tracks:
        if a not in present: continue
        catalogue = {norm(titles.get(x)) for s in ids[a] for x in rows.get(s, []) if x and titles.get(x)}
        if norm(t) in catalogue: hits.append(f"{t} / {a}")
    print(f"{name} : morceaux présents avec leurs accords : {len(hits)}/{len(tracks)} -> {hits}")

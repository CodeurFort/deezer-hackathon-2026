"""Les artistes du Top France et du Top Monde de Deezer sont-ils dans Chordonomicon ?

Identifiants Spotify des artistes retrouvés via Wikidata (propriété P1902), puis cherchés dans le jeu de données.
Écrit playlists.json et couverture_artistes.json, lus ensuite par couverture_morceaux.py.
Mesure du 25/11/2026 (docs/faisabilite.md, ligne « Les morceaux des tops actuels y sont-ils ? »).
"""
import json, urllib.request, urllib.parse, csv, collections
csv.field_size_limit(10**8)
UA = {"User-Agent": "deezer-hackathon-feasibility/0.1"}
def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r: return json.load(r)
pl = {}
for name, pid in [("Top France", 1109890291), ("Top Monde", 3155776842)]:
    d = get(f"https://api.deezer.com/playlist/{pid}?limit=100")
    pl[name] = [(t['title'], t['artist']['name']) for t in d['tracks']['data']]
    print(name, ":", len(pl[name]), "titres,", len({a for _, a in pl[name]}), "artistes")
json.dump(pl, open('playlists.json', 'w'), ensure_ascii=False)
names = sorted({a for tracks in pl.values() for _, a in tracks})
vals = " ".join(f'"{n.replace(chr(34), "")}"@{lg}' for n in names for lg in ("en", "fr", "mul"))
q = f"SELECT ?l ?sp WHERE {{ VALUES ?l {{ {vals} }} ?item rdfs:label ?l ; wdt:P1902 ?sp . }}"
headers = {**UA, "Accept": "application/sparql-results+json", "Content-Type": "application/x-www-form-urlencoded"}
req = urllib.request.Request("https://query.wikidata.org/sparql", data=urllib.parse.urlencode({"query": q}).encode(), headers=headers)
res = json.load(urllib.request.urlopen(req, timeout=180))  # POST : la requête est trop longue pour une URL
ids = collections.defaultdict(set)
for b in res["results"]["bindings"]: ids[b["l"]["value"]].add(b["sp"]["value"])
print(f"artistes avec identifiant Spotify trouvé dans Wikidata : {len(ids)}/{len(names)}")
want = {s for v in ids.values() for s in v}
rows = collections.defaultdict(list)
for r in csv.DictReader(open('chordonomicon_v2.csv', encoding='utf-8', errors='ignore')):
    if r.get('spotify_artist_id') in want: rows[r['spotify_artist_id']].append(r.get('spotify_song_id') or '')
present = {n for n, v in ids.items() if any(rows.get(s) for s in v)}
print(f"artistes présents dans Chordonomicon : {len(present)}")
json.dump({"ids": {k: sorted(v) for k, v in ids.items()}, "rows": rows}, open('couverture_artistes.json', 'w'))
for name, tracks in pl.items():
    print(f"{name} : morceaux dont l'artiste est présent : {sum(1 for _, a in tracks if a in present)}/{len(tracks)}")

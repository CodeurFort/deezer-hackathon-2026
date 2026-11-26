import csv, json, urllib.request, urllib.parse, random, time, re
csv.field_size_limit(10**8)
UA = {"User-Agent": "Mozilla/5.0"}
def get(url):
    for i in range(3):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=15))
        except Exception as e: err = e; time.sleep(1 + i)
    raise err
def norm(s): return re.sub(r'[^a-z0-9]', '', (s or '').lower())
def base_title(s):
    s = (s or '').lower()
    s = re.sub(r'\s*[\(\[].*?[\)\]]', '', s)          # (Live), [Remastered]
    s = re.sub(r'\s+-\s+.*$', '', s)                     # - Demo, - 2011 Remaster
    return norm(s)
def to_deezer(title, artist):
    d = get("https://api.deezer.com/search?" + urllib.parse.urlencode({"q": f"{artist} {base_title(title) and re.sub(r' - .*$', '', title)}", "limit": 10}))
    for h in d.get('data') or []:
        if norm(h['artist']['name']) == norm(artist) and base_title(h['title']) == base_title(title):
            return h
    return None
def spotify_names(song_id, artist_id, cache={}):
    t = get("https://open.spotify.com/oembed?url=" + urllib.parse.quote("https://open.spotify.com/track/" + song_id)).get('title')
    if artist_id not in cache:
        cache[artist_id] = get("https://open.spotify.com/oembed?url=" + urllib.parse.quote("https://open.spotify.com/artist/" + artist_id)).get('title')
    return t, cache[artist_id]
if __name__ == "__main__":
    random.seed(42); k = 40; res = []; n = 0
    for r in csv.DictReader(open('chordonomicon_v2.csv', encoding='utf-8', errors='ignore')):
        if not r.get('spotify_song_id') or not r.get('spotify_artist_id'): continue
        n += 1
        if len(res) < k: res.append(r)
        else:
            j = random.randrange(n)
            if j < k: res[j] = r
    ok = prev = 0; rates = []
    for r in res:
        t, a = spotify_names(r['spotify_song_id'], r['spotify_artist_id'])
        h = to_deezer(t, a) if t and a else None
        ok += bool(h); prev += bool(h and h.get('preview'))
        if not h: rates.append(f"{t} / {a}")
        time.sleep(0.2)
    print(f"échantillon {len(res)} : correspondance sûre sur Deezer {ok}/{len(res)}, avec extrait {prev}/{len(res)}")
    print("non trouvés :", rates[:12])

"""Combien de morceaux des tops sont sortis avant la publication de Chordonomicon (29/10/2024) ?

Un morceau sorti après ne peut pas y être : c'est un plafond sûr de couverture.
Attention au quota de l'API Deezer : trop d'appels simultanés renvoient des erreurs sans date,
ce qui avait faussé une première mesure. Ici, appels ralentis et chaque réponse contrôlée.
Mesure du 25/11/2026 (docs/faisabilite.md, ligne « Les morceaux des tops actuels y sont-ils ? »).
"""
import json, urllib.request, time
UA = {"User-Agent": "deezer-hackathon-feasibility/0.1"}
def get(u):
    for i in range(5):
        with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30) as r: d = json.load(r)
        if "error" not in d: return d
        time.sleep(5)
    raise RuntimeError(f"erreur Deezer persistante : {d['error']}")
for name, pid in [("Top France", 1109890291), ("Top Monde", 3155776842)]:
    ids = [t['id'] for t in get(f"https://api.deezer.com/playlist/{pid}?limit=100")['tracks']['data']]
    dates = []
    for i in ids:
        dates.append(get(f"https://api.deezer.com/track/{i}")['release_date']); time.sleep(0.13)
    vides = sum(1 for d in dates if not d or d.startswith('0000'))
    avant = [d for d in dates if d and not d.startswith('0000') and d < "2024-10-29"]
    print(f"{name} : sortis avant le 29/10/2024 : {len(avant)}/{len(dates)} | dates manquantes : {vides} | médiane : {sorted(dates)[len(dates)//2]}")

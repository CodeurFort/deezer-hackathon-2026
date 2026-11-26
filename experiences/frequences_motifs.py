"""Fréquence de chaque motif sur les 679 807 morceaux de Chordonomicon, par genre et par artiste.

Mesure du 25/11/2026 (docs/faisabilite.md, lignes « Les motifs sont-ils assez rares… »,
« Les artistes ont-ils une signature harmonique ? » et « La basse écrite suffit-elle ? »).
"""
import csv, collections
from motifs import motifs
csv.field_size_limit(10**8)
N = collections.Counter(); tot = 0; by_genre = collections.defaultdict(collections.Counter); gtot = collections.Counter()
slash_split = {True: collections.Counter(), False: collections.Counter()}; slash_tot = collections.Counter()
artist = collections.defaultdict(lambda: [0, 0])
for r in csv.DictReader(open('chordonomicon_v2.csv', encoding='utf-8', errors='ignore')):
    f = motifs(r['chords']); tot += 1
    has_slash = '/' in r['chords']; slash_tot[has_slash] += 1
    g = r.get('main_genre') or '(sans genre)'; gtot[g] += 1
    for k, v in f.items():
        if v: N[k] += 1; by_genre[g][k] += 1; slash_split[has_slash][k] += 1
    a = r.get('spotify_artist_id')
    if a: artist[a][0] += 1; artist[a][1] += f["basse_descend"]
print(f"morceaux analysés : {tot}")
for k in ["basse_descend", "andalouse", "axe_pop", "annees_50", "couleurs", "mineur"]:
    p = N[k] / tot
    chance = 5 * p**4 * (1 - p) + p**5  # 4 morceaux sur 5 (ou plus) qui partagent le motif par hasard
    print(f"  {k:14s} {p:6.1%} | si 4 morceaux sur 5 l'ont, probabilité que ce soit le hasard : {chance:.2%}")
print("basse descendante selon la notation : avec basses notées", f"{slash_split[True]['basse_descend']/slash_tot[True]:.1%}", "| sans", f"{slash_split[False]['basse_descend']/slash_tot[False]:.1%}")
print("par genre (basse descendante / andalouse / axe pop) :")
for g, n in gtot.most_common(9):
    c = by_genre[g]; print(f"  {g:14s} {c['basse_descend']/n:6.1%} {c['andalouse']/n:6.1%} {c['axe_pop']/n:6.1%}  ({n} morceaux)")
rates = sorted(b / n for n, b in artist.values() if n >= 20)
q = lambda x: rates[int(x * (len(rates) - 1))]
print(f"artistes avec 20 morceaux ou plus : {len(rates)} | part de leurs morceaux à basse descendante : 10e centile {q(.1):.0%}, médiane {q(.5):.0%}, 90e centile {q(.9):.0%}")

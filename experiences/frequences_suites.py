"""Fréquence des suites de degrés (IV–V–I, ii–V–I…) dans Chordonomicon, tonalité estimée morceau par morceau.

Un morceau sur 4 (environ 170 000). Mesure du 26/11/2026.
"""
import csv, re, collections
from degres import tonalite, suite, SUITES
csv.field_size_limit(10**8)
PC = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
TOK = re.compile(r'^([A-G])(s|b)?([^/]*)')
def accord(t):
    m = TOK.match(t)
    if not m: return None
    r = (PC[m.group(1)] + (1 if m.group(2) == 's' else -1 if m.group(2) == 'b' else 0)) % 12
    q = m.group(3)
    return (r, 'd' if ('dim' in q or 'b5' in q) else 'm' if q.startswith('min') else 'M')
compte = collections.Counter(); n = 0; ambigus = 0; majeur = 0
for i, row in enumerate(csv.DictReader(open('chordonomicon_v2.csv', encoding='utf-8', errors='ignore'))):
    if i % 4: continue
    seq = [a for a in (accord(t) for t in row['chords'].split() if not t.startswith('<')) if a]
    if len(seq) < 4: continue
    hist = collections.Counter(seq)
    t, mode, amb, _ = tonalite([(a, c) for a, c in hist.items()], extremes=[(seq[0], 1), (seq[-1], 1)], n=len(seq))
    s = suite([(a, 1) for a in seq], t)
    n += 1; ambigus += amb; majeur += mode == 'majeur'
    for nom, test in SUITES.items():
        if test(s, mode): compte[nom] += 1
print(f"morceaux analysés : {n} | tonalité majeure {majeur/n:.0%} | tonalité ambiguë (deux lectures à moins de 10 %) : {ambigus/n:.0%}")
for nom, c in compte.most_common():
    p = c / n; hasard = 5 * p**4 * (1 - p) + p**5
    print(f"  {nom:32s} {p:6.1%} | 4 morceaux sur 5 par hasard : {hasard:6.2%}")

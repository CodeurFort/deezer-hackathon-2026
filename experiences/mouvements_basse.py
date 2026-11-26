"""Les mouvements de la basse, au-delà de la descente : montée, note tenue, sauts, basse qui marche, chromatisme.

À partir de la suite des notes de basse temps par temps (basse_audio.basse). Mesure du 26/11/2026.
"""
import json, sys, glob, os, warnings
from collections import Counter
warnings.filterwarnings("ignore")
from basse_audio import basse
def mouvements(f):
    tempo, seq, _ = basse(f)
    if len(seq) < 5: return None
    iv = [((b - a + 6) % 12) - 6 for a, b in zip(seq, seq[1:])]          # intervalle signé le plus court, -5..+6
    n = len(iv)
    runs = lambda sgn: sum(1 for i in range(len(seq) - 3) if all(((seq[i+k+1] - seq[i+k] + 6) % 12 - 6) * sgn in (1, 2) for k in range(3)))
    return {"descentes": runs(-1), "montees": runs(+1),
            "pas_conjoints": sum(1 for x in iv if abs(x) in (1, 2)) / n,   # basse qui « marche »
            "sauts": sum(1 for x in iv if abs(x) >= 5) / n,                 # quinte, quarte, octave
            "chromatisme": sum(1 for x in iv if abs(x) == 1) / n,
            "notes_differentes": len(set(seq)), "changements_par_temps": n / max(len(seq), 1)}
def profil(m):
    if m["descentes"] >= 2 and m["descentes"] > m["montees"]: return "descend"
    if m["montees"] >= 2 and m["montees"] > m["descentes"]: return "monte"
    if m["notes_differentes"] <= 3: return "tient une note ou deux"
    if m["sauts"] >= 0.5: return "saute (quintes, octaves)"
    if m["pas_conjoints"] >= 0.5: return "marche (pas conjoints)"
    return "mixte"
if __name__ == "__main__":
    fichiers = sys.argv[1:] or sorted(glob.glob('pool/*.mp3'))
    res = []
    for f in fichiers:
        m = mouvements(f)
        if m: res.append((f, m))
    c = Counter(profil(m) for _, m in res)
    print(f"{len(res)} extraits | profils de basse :", ", ".join(f"{k} {v}" for k, v in c.most_common()))
    moy = lambda k: sum(m[k] for _, m in res) / len(res)
    print(f"moyennes : pas conjoints {moy('pas_conjoints'):.0%}, sauts {moy('sauts'):.0%}, chromatisme {moy('chromatisme'):.0%}, notes différentes {moy('notes_differentes'):.1f}")
    json.dump([(os.path.basename(f), m, profil(m)) for f, m in res], open('mouvements_basse.json', 'w'))

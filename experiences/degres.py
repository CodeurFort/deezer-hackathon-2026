"""Des accords aux degrés (I, IV, V…) : tonalité estimée, chiffrage, suites repérées.

Un accord est un couple (racine 0-11, famille) avec famille 'M' (majeur, septième de dominante, maj7, 6, sus, 9),
'm' (mineur, min7, min6, min9) ou 'd' (diminué, demi-diminué).
"""
NOMS = {0: 'I', 1: 'bII', 2: 'II', 3: 'bIII', 4: 'III', 5: 'IV', 6: '#IV', 7: 'V', 8: 'bVI', 9: 'VI', 10: 'bVII', 11: 'VII'}
# Poids des accords pour estimer la tonalité : le premier degré pèse le plus, puis la dominante et la sous-dominante.
POIDS = {
    'majeur': {(0, 'M'): 3.0, (7, 'M'): 2.0, (5, 'M'): 1.5, (9, 'm'): 1.2, (2, 'm'): 1.0, (4, 'm'): 0.8, (10, 'M'): 0.8, (11, 'd'): 0.5},
    'mineur': {(0, 'm'): 3.0, (7, 'M'): 1.5, (7, 'm'): 1.0, (5, 'm'): 1.5, (8, 'M'): 1.2, (10, 'M'): 1.2, (3, 'M'): 1.0, (2, 'd'): 0.5},
}
MINEURES = {'min', 'min7', 'minmaj7', 'min6', 'min9', 'min11', 'min13'}
DIMINUEES = {'dim', 'dim7', 'hdim7'}


def famille(qualite):
    q = qualite.split('/')[0]
    return 'd' if q in DIMINUEES else 'm' if q in MINEURES else 'M'


def tonalite(accords, extremes=None, n=None):
    """accords : liste de ((racine, famille), durée), éventuellement agrégée (alors extremes = premier et dernier accords,
    n = nombre d'accords joués). Renvoie (tonique, mode, ambigu, deuxième choix)."""
    total = sum(d for _, d in accords) or 1
    bonus = total / max(n or len(accords), 1)  # le premier et le dernier accord pèsent un accord de plus
    scores = []
    for t in range(12):
        for mode, poids in POIDS.items():
            s = sum(d * poids.get(((r - t) % 12, f), -0.5) for (r, f), d in accords)
            for (r, f), _ in (extremes if extremes is not None else accords[:1] + accords[-1:]):
                if (r - t) % 12 == 0 and f == ('m' if mode == 'mineur' else 'M'):
                    s += bonus
            scores.append((s, t, mode))
    scores.sort(reverse=True)
    (s1, t1, m1), (s2, t2, m2) = scores[0], scores[1]
    return t1, m1, s2 >= 0.9 * s1, (t2, m2)


def chiffre(accord, tonique):
    r, f = accord
    nom = NOMS[(r - tonique) % 12]
    prefixe, coeur = (nom[0], nom[1:]) if nom[0] in 'b#' else ('', nom)
    if f in ('m', 'd'): coeur = coeur.lower()
    return prefixe + coeur + ('°' if f == 'd' else '')


def suite(accords, tonique):
    """Chiffrage, répétitions fusionnées."""
    out = []
    for a, _ in accords:
        c = chiffre(a, tonique)
        if not out or out[-1] != c: out.append(c)
    return out


def contient(seq, motif):
    n = len(motif)
    return any(seq[i:i + n] == motif for i in range(len(seq) - n + 1))


def cyclique(seq, motif):
    return any(contient(seq, motif[i:] + motif[:i]) for i in range(len(motif)))


SUITES = {
    'IV–V–I': lambda s, m: contient(s, ['IV', 'V', 'I']) if m == 'majeur' else contient(s, ['iv', 'V', 'i']) or contient(s, ['iv', 'v', 'i']),
    'ii–V–I': lambda s, m: contient(s, ['ii', 'V', 'I']) if m == 'majeur' else contient(s, ['ii°', 'V', 'i']),
    'II–V–I (dominante secondaire)': lambda s, m: m == 'majeur' and contient(s, ['II', 'V', 'I']),
    'V–vi (cadence rompue)': lambda s, m: m == 'majeur' and contient(s, ['V', 'vi']),
    'IV–I (cadence plagale)': lambda s, m: contient(s, ['IV', 'I']) if m == 'majeur' else contient(s, ['iv', 'i']),
    'iv–I (mineur emprunté)': lambda s, m: m == 'majeur' and contient(s, ['iv', 'I']),
    'bVII–IV–I (rock)': lambda s, m: m == 'majeur' and contient(s, ['bVII', 'IV', 'I']),
    'boucle I–V–vi–IV': lambda s, m: cyclique(s, ['I', 'V', 'vi', 'IV']) or cyclique(s, ['i', 'bVI', 'bIII', 'bVII']),
    'I–vi–IV–V (années 50)': lambda s, m: cyclique(s, ['I', 'vi', 'IV', 'V']),
    'i–bVII–bVI–V (andalouse)': lambda s, m: contient(s, ['i', 'bVII', 'bVI', 'V']) or contient(s, ['I', 'bVII', 'bVI', 'V']),  # tolère un premier accord lu majeur
}


def analyse(accords):
    tonique, mode, ambigu, second = tonalite(accords)
    s = suite(accords, tonique)
    return {'tonique': tonique, 'mode': mode, 'ambigu': ambigu, 'second': second, 'suite': s,
            'suites': [nom for nom, test in SUITES.items() if test(s, mode)]}

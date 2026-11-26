import re
PC = {'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}
TOK = re.compile(r'^([A-G])(s|b)?(.*?)(?:/([A-G])(s|b)?)?$')
def parse(t):
    m = TOK.match(t)
    if not m: return None
    root = (PC[m.group(1)] + (1 if m.group(2) == 's' else -1 if m.group(2) == 'b' else 0)) % 12
    q = m.group(3) or ''
    minor = q.startswith('min') and not q.startswith('maj')
    bass = root if not m.group(4) else (PC[m.group(4)] + (1 if m.group(5) == 's' else -1 if m.group(5) == 'b' else 0)) % 12
    colour = bool(re.search(r'7|9|11|13|sus|add|dim|aug', q))
    return root, minor, bass, colour
def sections(chords):
    out, cur = [], []
    for t in chords.split():
        if t.startswith('<'):
            if cur: out.append(cur)
            cur = []
        else:
            p = parse(t)
            if p and (not cur or cur[-1] != p): cur.append(p)
    if cur: out.append(cur)
    return out
def rot(seq):
    return [seq[i:] + seq[:i] for i in range(len(seq))]
def rel(win):
    r0 = win[0][0]; return tuple(((c[0] - r0) % 12, c[1]) for c in win)
AXIS = {rel(s) for s in rot([(0,False),(7,False),(9,True),(5,False)])}
FIFTIES = {rel(s) for s in rot([(0,False),(9,True),(5,False),(7,False)])}
ANDALOUSE = {((0,True),(10,False),(8,False),(7,False))}
def motifs(chords):
    f = {"basse_descend": False, "andalouse": False, "axe_pop": False, "annees_50": False, "couleurs": False, "mineur": False}
    allc = []
    for sec in sections(chords):
        allc += sec
        b = [c[2] for c in sec]
        for i in range(len(b) - 3):
            if all((b[i+k] - b[i+k+1]) % 12 in (1, 2) for k in range(3)): f["basse_descend"] = True; break
        for i in range(len(sec) - 3):
            w = rel(sec[i:i+4])
            f["axe_pop"] |= w in AXIS; f["annees_50"] |= w in FIFTIES; f["andalouse"] |= w in ANDALOUSE
    if allc:
        f["couleurs"] = sum(c[3] for c in allc) / len(allc) >= 0.25
        from collections import Counter
        f["mineur"] = Counter((c[0], c[1]) for c in allc).most_common(1)[0][0][1]
    return f

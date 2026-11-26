"""Gamme et mode d'un extrait : tonique (basse + accords), notes utilisées (spectre + mélodie), mode tranché
sur les degrés qui distinguent les modes, comme un musicien l'expliquerait. Mesure du 26/11/2026."""
import json, os, sys, warnings, numpy as np
warnings.filterwarnings("ignore")
import essentia; essentia.log.infoActive = False; essentia.log.warningActive = False
import essentia.standard as es
from basse_audio import basse
NOTES = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
ALIAS = {'Db':'C#','Eb':'D#','Gb':'F#','Ab':'G#','Bb':'A#','Cb':'B','Fb':'E'}
REF = [("oyecomova", "A", "dorien"), ("scarboroughfair", "E", "dorien"), ("getlucky", "B", "dorien"), ("moondance", "A", "dorien"),
       ("sweethomealabama", "D", "mixolydien"), ("norwegianwood", "E", "mixolydien"), ("misirlou", "E", "phrygien dominant"),
       ("letitbe", "C", "ionien (majeur)"), ("standbyme", "A", "ionien (majeur)"), ("someonelikeyou", "A", "ionien (majeur)"),
       ("knockinonheavensdoor", "G", "ionien (majeur)"), ("zombie", "E", "éolien (mineur naturel)"), ("despacito", "B", "éolien (mineur naturel)"),
       ("wakemeup", "B", "éolien (mineur naturel)"), ("shapeofyou", "C#", "éolien (mineur naturel)"), ("smooth", "A", "mineur harmonique"),
       ("hittheroadjack", "G#", "mineur harmonique")]

def spectre_et_melodie(f):
    audio = es.MonoLoader(filename=f, sampleRate=44100)()
    w, sp = es.Windowing(type='blackmanharris62'), es.Spectrum()
    pk = es.SpectralPeaks(orderBy='magnitude', magnitudeThreshold=1e-5, minFrequency=40, maxFrequency=5000, maxPeaks=60)
    hp = es.HPCP(size=12, referenceFrequency=440 * 2 ** (-9 / 12))      # case 0 = do
    h = np.zeros(12)
    for fr in es.FrameGenerator(audio, frameSize=4096, hopSize=2048):
        fq, mg = pk(sp(w(fr)))
        h += hp(fq, mg)
    h /= h.sum() or 1
    pitch, conf = es.PredominantPitchMelodia(frameSize=2048, hopSize=256)(es.EqualLoudness()(audio))
    v = pitch[pitch > 0]
    m = np.zeros(12)
    for p in v: m[int(round(12 * np.log2(p / 440) + 69)) % 12] += 1
    m /= m.sum() or 1
    return h, m, len(v) / max(len(pitch), 1)
def tonique(f, accords):
    _, seq, _ = basse(f)
    b = np.bincount(seq, minlength=12).astype(float); b /= b.sum() or 1
    c = np.zeros(12); roots = []
    for x in accords:
        if x['chord'] in ('N', 'X'): continue
        r = NOTES.index(ALIAS.get(x['chord'].split(':')[0], x['chord'].split(':')[0])); roots.append(r)
        c[r] += x['end_time'] - x['start_time']
    c /= c.sum() or 1
    s = b + c
    if roots: s[roots[0]] += .15; s[roots[-1]] += .15
    return int(np.argmax(s))
def choix(P, t, a, b):  # degré a ou b (en demi-tons depuis la tonique) ?
    pa, pb = P[(t + a) % 12], P[(t + b) % 12]
    r = pa / (pa + pb) if pa + pb > 0 else .5
    return a if r > .6 else b if r < .4 else None
def mode(P, t):
    tierce = choix(P, t, 4, 3)
    if tierce == 3:
        seconde, sixte, septieme = choix(P, t, 1, 2), choix(P, t, 9, 8), choix(P, t, 11, 10)
        if seconde == 1: return "phrygien"
        if septieme == 11: return "mineur harmonique" if sixte != 9 else "mineur mélodique"
        if sixte == 9: return "dorien"
        if sixte == 8: return "éolien (mineur naturel)"
        return "mineur (sixte indécise)"
    if tierce == 4:
        seconde, quarte, septieme = choix(P, t, 1, 2), choix(P, t, 6, 5), choix(P, t, 10, 11)
        if seconde == 1: return "phrygien dominant"
        if quarte == 6: return "lydien"
        if septieme == 10: return "mixolydien"
        if septieme == 11: return "ionien (majeur)"
        return "majeur (septième indécise)"
    return "indécis"
def analyse(fic):
    f = f"extraits/{fic}.mp3"; acc = json.load(open(f"extraits/{fic}.accords.json"))
    h, m, voix = spectre_et_melodie(f)
    P = .5 * h + .5 * m
    t = tonique(f, acc)
    return NOTES[t], mode(P, t), voix
if __name__ == "__main__" and len(sys.argv) == 1:
    ok_t = ok_m = 0
    for fic, t_ref, m_ref in REF:
        t, md, voix = analyse(fic)
        ok_t += t == t_ref; ok_m += (t == t_ref and md == m_ref)
        print(f"  {fic:22s} {t:3s} {md:26s} | réf. {t_ref:3s} {m_ref:24s} {'OK' if (t == t_ref and md == m_ref) else ('tonique OK' if t == t_ref else 'NON')}")
    print(f"=> tonique juste {ok_t}/{len(REF)} | tonique et mode justes {ok_m}/{len(REF)}")

# --- Version 2 : tonique validée (accords, degres.tonalite) et notes des accords détectés ---
from degres import tonalite, famille
NOTES_ACCORD = {'maj': (0, 4, 7), 'min': (0, 3, 7), '7': (0, 4, 7, 10), 'maj7': (0, 4, 7, 11), 'min7': (0, 3, 7, 10),
                'dim': (0, 3, 6), 'dim7': (0, 3, 6, 9), 'hdim7': (0, 3, 6, 10), 'aug': (0, 4, 8), 'sus2': (0, 2, 7), 'sus4': (0, 5, 7),
                'maj6': (0, 4, 7, 9), 'min6': (0, 3, 7, 9), '9': (0, 4, 7, 10, 2), 'maj9': (0, 4, 7, 11, 2), 'min9': (0, 3, 7, 10, 2),
                'minmaj7': (0, 3, 7, 11), '11': (0, 4, 7, 10, 5), '13': (0, 4, 7, 10, 9)}
def notes_des_accords(acc):
    C = np.zeros(12); evid = []
    for x in acc:
        if x['chord'] in ('N', 'X'): continue
        r, _, q = x['chord'].partition(':'); r = NOTES.index(ALIAS.get(r, r)); q = (q or 'maj').split('/')[0]
        d = x['end_time'] - x['start_time']
        for i in NOTES_ACCORD.get(q, NOTES_ACCORD['min' if q.startswith('min') else 'maj']): C[(r + i) % 12] += d
        evid.append(((r, famille(q)), d))
    return C / (C.sum() or 1), evid
def analyse_v2(fic):
    f = f"extraits/{fic}.mp3"; acc = json.load(open(f"extraits/{fic}.accords.json"))
    C, evid = notes_des_accords(acc)
    t, mode_ton, _, _ = tonalite(evid)
    _, m, _ = spectre_et_melodie(f)
    P = .7 * C + .3 * m
    if mode_ton == 'mineur': P[(t + 4) % 12] = 0          # la famille vient de la tonalité validée
    else: P[(t + 3) % 12] = 0
    return NOTES[t], mode(P, t)
def cle_essentia(fic):
    k, s, _ = es.KeyExtractor(profileType='edma')(es.MonoLoader(filename=f"extraits/{fic}.mp3", sampleRate=44100)())
    return ALIAS.get(k, k), s
if __name__ == "__main__" and "--v2" in sys.argv:
    REF2 = {"getlucky": [("B", "dorien"), ("F#", "éolien (mineur naturel)")]}
    ok = okt = okk = 0
    for fic, t_ref, m_ref in REF:
        t, md = analyse_v2(fic); k, s = cle_essentia(fic)
        refs = REF2.get(fic, [(t_ref, m_ref)])
        bon = (t, md) in refs; ok += bon; okt += any(t == r[0] for r in refs); okk += any(k == r[0] for r in refs)
        print(f"  {fic:22s} {t:3s} {md:26s} | réf. {' ou '.join(a + ' ' + b for a, b in refs):42s} {'OK' if bon else 'NON'} | clé Essentia {k} {s}")
    print(f"=> v2 : tonique juste {okt}/{len(REF)}, tonique et mode justes {ok}/{len(REF)} | tonique Essentia (profil edma) juste {okk}/{len(REF)}")

# --- Version 3 : deux estimations de tonique (accords et spectre), la basse tranche quand elles divergent ---
def analyse_v3(fic):
    f = f"extraits/{fic}.mp3"; acc = json.load(open(f"extraits/{fic}.accords.json"))
    C, evid = notes_des_accords(acc)
    t1, m1, _, _ = tonalite(evid)
    k, s, force = es.KeyExtractor(profileType='edma')(es.MonoLoader(filename=f, sampleRate=44100)())
    t2, m2 = NOTES.index(ALIAS.get(k, k)), ('mineur' if s == 'minor' else 'majeur')
    if t1 == t2:
        t, fam = t1, (m2 if m1 != m2 else m1)
    else:
        _, seq, _ = basse(f)
        b = np.bincount(seq, minlength=12)
        t, fam = (t2, m2) if b[t2] >= b[t1] else (t1, m1)
    _, m, _ = spectre_et_melodie(f)
    P = .7 * C + .3 * m
    P[(t + (4 if fam == 'mineur' else 3)) % 12] = 0
    return NOTES[t], mode(P, t), t1 == t2
if __name__ == "__main__" and "--v3" in sys.argv:
    REF2 = {"getlucky": [("B", "dorien"), ("F#", "éolien (mineur naturel)")]}
    ok = okt = 0; accords_ok = accords_n = 0
    for fic, t_ref, m_ref in REF:
        t, md, accord = analyse_v3(fic)
        refs = REF2.get(fic, [(t_ref, m_ref)])
        bon = (t, md) in refs; ok += bon; okt += any(t == r[0] for r in refs)
        if accord: accords_n += 1; accords_ok += bon
        print(f"  {fic:22s} {t:3s} {md:26s} | réf. {' ou '.join(a + ' ' + b for a, b in refs):42s} {'OK' if bon else 'NON'}{'  (les deux estimations concordent)' if accord else ''}")
    print(f"=> v3 : tonique juste {okt}/{len(REF)}, tonique et mode justes {ok}/{len(REF)} | quand les deux estimations concordent : {accords_ok}/{accords_n}")

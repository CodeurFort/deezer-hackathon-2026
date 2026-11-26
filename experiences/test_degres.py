"""Degrés et suites détectés dans l'audio (lv-chordia), comparés à une analyse de référence."""
import os, json, warnings
warnings.filterwarnings("ignore")
from lv_chordia.chord_recognition import chord_recognition
from degres import analyse, famille
NOTES = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
ALIAS = {'Db':'C#','Eb':'D#','Gb':'F#','Ab':'G#','Bb':'A#','Cb':'B','Fb':'E'}
REF = [  # fichier, titre, tonalité de référence, suite attendue (lecture usuelle ; « ou » = lecture ambiguë admise)
 ("letitbe", "Let It Be", "C majeur", "boucle I–V–vi–IV, IV–I"),
 ("hittheroadjack", "Hit the Road Jack", "G# mineur", "andalouse"),
 ("knockinonheavensdoor", "Knockin' On Heaven's Door", "G majeur", "I–V–ii, I–V–IV"),
 ("standbyme", "Stand By Me", "A majeur", "années 50, IV–V–I"),
 ("getlucky", "Get Lucky", "B mineur ou D majeur ou F# mineur", "boucle vi–I–iii–II (dorien)"),
 ("someonelikeyou", "Someone Like You", "A majeur", "boucle I–V–vi–IV"),
 ("zombie", "Zombie", "E mineur ou G majeur", "boucle I–V–vi–IV"),
 ("wakemeup", "Wake Me Up", "B mineur ou D majeur", "boucle I–V–vi–IV"),
 ("shapeofyou", "Shape of You", "C# mineur", "i–iv–bVI–bVII"),
 ("despacito", "Despacito", "B mineur ou D majeur", "boucle I–V–vi–IV"),
 ("moondance", "Moondance", "A mineur (dorien)", "i–ii"),
 ("isntshelovely", "Isn't She Lovely", "C# mineur ou E majeur", "vi–II–V–I"),
 ("flymetothemoon", "Fly Me To The Moon", "C majeur ou A mineur", "ii–V–I"),
 ("smooth", "Smooth", "A mineur", "i–bVI–V"),
]
res = []
for fic, titre, ton_ref, suite_ref in REF:
    cache = f"extraits/{fic}.accords.json"
    out = json.load(open(cache)) if os.path.exists(cache) else chord_recognition(audio_path=os.path.abspath(f"extraits/{fic}.mp3"), chord_dict_name="submission")
    accords = []
    for x in out:
        if x['chord'] in ('N', 'X'): continue
        r, _, q = x['chord'].partition(':')
        accords.append(((NOTES.index(ALIAS.get(r, r)), famille(q or 'maj')), x['end_time'] - x['start_time']))
    a = analyse(accords)
    ton = f"{NOTES[a['tonique']]} {a['mode']}" + (" (ambiguë)" if a['ambigu'] else "")
    ok = any(t.strip().split(' (')[0] == f"{NOTES[a['tonique']]} {a['mode']}" for t in ton_ref.split(' ou '))
    res.append(ok)
    print(f"- {titre:26s} tonalité {ton:22s} réf. {ton_ref:24s} {'OK' if ok else 'DIFFÉRENTE'}\n    degrés : {' '.join(a['suite'][:12])}\n    suites : {a['suites']}   (réf. : {suite_ref})")
    json.dump(out, open(f"extraits/{fic}.accords.json", "w"))
print(f"=> tonalité conforme à la référence (lectures ambiguës admises) : {sum(res)}/{len(res)}")

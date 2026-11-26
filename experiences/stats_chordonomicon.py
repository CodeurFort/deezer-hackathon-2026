"""Ce que couvre Chordonomicon : genres, décennies, musique française, rap, basse notée.

Mesure du 25/11/2026 (docs/faisabilite.md, ligne « Que couvre Chordonomicon ? »).
"""
import csv, collections, re
csv.field_size_limit(10**8)
n = 0; with_song = 0; artists = set(); main = collections.Counter(); decades = collections.Counter()
fr = 0; fr_rap = 0; rap = 0; fr_terms = re.compile(r"french|francais|français|variete|chanson|quebec|belgian|rap francais|pop urbaine")
nchords = []; vocab = collections.Counter(); slash = 0
for r in csv.DictReader(open('chordonomicon_v2.csv', encoding='utf-8', errors='ignore')):
    n += 1
    if r.get('spotify_song_id'): with_song += 1
    if r.get('spotify_artist_id'): artists.add(r['spotify_artist_id'])
    main[r.get('main_genre') or '(vide)'] += 1
    decades[r.get('decade') or '(vide)'] += 1
    g = (r.get('genres') or '').lower()
    isfr = bool(fr_terms.search(g)); fr += isfr
    israp = 'rap' in g or 'hip hop' in g or (r.get('main_genre') == 'rap'); rap += israp; fr_rap += isfr and israp
    toks = [t for t in r['chords'].split() if not t.startswith('<')]
    nchords.append(len(toks)); vocab.update(toks); slash += any('/' in t for t in toks)
print(f"morceaux : {n} | avec id Spotify du morceau : {with_song} ({with_song/n:.0%}) | artistes distincts : {len(artists)}")
print("genre principal :", ", ".join(f"{k} {v/n:.1%}" for k, v in main.most_common(12)))
print("décennie :", ", ".join(f"{k} {v/n:.1%}" for k, v in sorted(decades.items(), key=lambda x: x[0])))
print(f"genres français (french, variété, chanson…) : {fr} ({fr/n:.1%}) | rap/hip-hop : {rap} ({rap/n:.1%}) | rap français : {fr_rap}")
nchords.sort(); print(f"accords par morceau : médiane {nchords[len(nchords)//2]} | morceaux avec basse notée (accord/basse) : {slash} ({slash/n:.1%})")
print("accords les plus fréquents :", ", ".join(f"{k} {v}" for k, v in vocab.most_common(15)))
print("vocabulaire distinct :", len(vocab))

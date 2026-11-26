# Expériences de faisabilité

Les scripts qui ont produit les chiffres de [`docs/faisabilite.md`](../docs/faisabilite.md), du 25 au 26 novembre 2026. Ce sont des mesures, pas le produit du hackathon. Les résultats et leur lecture sont dans l'étude et dans le [registre](../REGISTRE.md).

## Préparer

Deux environnements Python, à créer dans ce dossier :

```sh
# analyse audio de base (Python 3.9 ou plus)
python3 -m venv venv-audio && venv-audio/bin/pip install librosa soundfile essentia

# accords enrichis par deep learning (Python 3.10 ou plus, PyTorch)
python3.12 -m venv venv-accords && venv-accords/bin/pip install "lv-chordia @ git+https://github.com/openmirlab/lv-chordia.git"
```

Le jeu de données Chordonomicon (264 Mo, licence CC BY-NC 4.0) n'est pas dans le dépôt :

```sh
curl -L -o chordonomicon_v2.csv https://huggingface.co/datasets/ailsntua/Chordonomicon/resolve/main/chordonomicon_v2.csv
```

Les extraits audio sont téléchargés par les scripts depuis l'API publique de Deezer, sans clé, dans `extraits/` et `pool/`.

## Les scripts

| Script | Ce qu'il mesure | Lancer avec |
| --- | --- | --- |
| `motifs.py` | Repère les motifs dans des accords écrits : basse qui descend, cadence andalouse, suite pop I–V–vi–IV, suite des années 50, accords enrichis, tonalité mineure. Module utilisé par les autres scripts | `python3 -c "from motifs import motifs"` |
| `stats_chordonomicon.py` | Ce que couvre Chordonomicon : genres, décennies, musique française, rap, basse notée | `python3` |
| `frequences_motifs.py` | La fréquence de chaque motif sur les 679 807 morceaux, par genre et par artiste | `python3` |
| `mapping.py` | Relie 40 morceaux de Chordonomicon pris au hasard à Deezer, sans compte (aperçu public de Spotify puis recherche Deezer) | `python3` |
| `couverture_artistes.py` | Les artistes du Top France et du Top Monde présents dans Chordonomicon (identifiants Spotify via Wikidata) | `python3` |
| `couverture_morceaux.py` | La même chose, morceau par morceau ; lent (environ 2 900 appels), arrêté avant la fin le 25/11 | `python3`, après le précédent |
| `dates_sortie.py` | Les morceaux des tops sortis avant la publication de Chordonomicon : plafond sûr de couverture | `python3` |
| `test_audio.py` | Détection d'accords par Essentia sur 10 extraits aux accords connus | `venv-audio/bin/python` |
| `basse_audio.py` | Suivi de la basse dans l'audio et repérage des lignes qui descendent | `venv-audio/bin/python basse_audio.py extraits/*.mp3` |
| `pool.py` | Analyse des 200 extraits du Top France et du Top Monde : temps de calcul et basses descendantes | `venv-audio/bin/python` |
| `test_lvchordia.py` | Accords enrichis par deep learning (lv-chordia) sur 15 extraits, dont 5 riches en septièmes | `venv-accords/bin/python` |

## Pièges rencontrés

- La recherche avancée de Deezer (`artist:"…" track:"…"`) renvoie zéro résultat : utiliser la recherche simple.
- Au-delà d'une dizaine de requêtes par seconde, l'API Deezer renvoie des erreurs à la place des données : ralentir et contrôler chaque réponse.
- lv-chordia cherche les fichiers relatifs à côté de son propre code : lui passer des chemins absolus.
- Aucune donnée personnelle dans les en-têtes des requêtes envoyées aux services externes.

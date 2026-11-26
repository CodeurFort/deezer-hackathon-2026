# Registre du travail de Claude

Chaque étape du projet a ici une entrée datée, la plus récente en haut, avec ce qui a été fait, ce qu'on a trouvé et le commit correspondant. Les résultats détaillés sont dans [`docs/faisabilite.md`](docs/faisabilite.md) et l'idée dans [`docs/idee.md`](docs/idee.md).

## Où on en est

- **Idée en tête** : repérer les motifs musicaux qu'un auditeur aime (basse qui descend, suites d'accords, rythme) et lui proposer des morceaux qui ont les mêmes, en lui disant pourquoi.
- **Faisabilité** : établie en partant de l'audio des extraits Deezer ; la basse qui descend est validée à l'oreille par Aurian sur 5 morceaux.
- **En cours** : test d'un modèle de deep learning qui reconnaît les accords enrichis (septièmes, neuvièmes…).
- **À faire** : le test d'Aurian sur ses propres morceaux ; l'écoute des 4 morceaux restants ; les questions aux organisateurs (code préparé autorisé ? clé Gradium ?) ; l'inscription.

## 26 novembre 2026

### Test des modèles d'accords enrichis (en cours)

- **Demande** : savoir si un modèle existant reconnaît les accords de septième, neuvième ou onzième sur nos extraits Deezer, sans avoir à entraîner de modèle.
- **Fait** : installation isolée dans le dossier de travail de Claude (Python 3.12, PyTorch, [lv-chordia](https://github.com/openmirlab/lv-chordia)). Le système de permissions de Claude Code l'avait d'abord bloquée ; Aurian l'a autorisée.
- **Résultats** : à venir dans cette entrée.

### Écoute d'Aurian et recherche sur le deep learning audio

- **Écoute** des morceaux où l'analyse a repéré une basse qui descend : 5 sur 5 confirmés par Aurian, dont 2 où la basse monte puis descend sur le motif de fin. Commit `9d9cc65`.
- **Recherche**, vérifiée sur les pages sources :
  - accords enrichis : [lv-chordia](https://github.com/openmirlab/lv-chordia) (MIT, 5 réseaux pré-entraînés, environ 81 % de justesse sur le Billboard) et [ChordFormer](https://arxiv.org/abs/2502.11840) (2025, 301 accords, poids publiés non trouvés) ;
  - séparation des pistes : [Spleeter](https://research.deezer.com/projects/spleeter.html), publié par Deezer ;
  - batterie : [ADTOF](https://huggingface.co/thebluescreen/adtof-drums-onnx) (kick, caisse claire, toms, charleston, cymbales ; 359 h de musique ; licence non commerciale) et [Beat This!](https://github.com/CPJKU/beat_this) (temps et débuts de mesure) ;
  - avatar 3D en direct : [TalkingHead](https://github.com/met4citizen/talkinghead) (lèvres synchronisées en temps réel, français pris en charge), et [Gradium](https://docs.gradium.ai/guides/text-to-speech.md) fournit le minutage des mots qu'il demande.
- **Mise au point** : Try Holo (tryholo.ai) produit des vidéos d'avatar à l'avance. Ce n'est ni un avatar qui répond en direct, ni Holo de H Company.

## 25 novembre 2026

### Étude de faisabilité mesurée

- **Verdict** : faisable en une trentaine d'heures en partant de l'audio des extraits Deezer ; le jeu de données d'accords Chordonomicon ne sert que de complément. Commit `7924529`.
- **Mesures principales** :
  - détection d'accords (Essentia) sur 10 extraits : 77 % du temps sur les bons accords ;
  - suivi de la basse dans l'audio : « Hit the Road Jack » sort exactement, 10 lignes descendantes ;
  - analyse en 0,4 s par extrait ; 200 extraits des tops analysés en 24 s ;
  - fréquence des motifs sur 679 807 morceaux : basse qui descend 10,5 %, cadence andalouse 1,4 % ; 5 morceaux suffisent à faire ressortir un goût ;
  - Chordonomicon couvre au mieux 9 % du Top France actuel ; relié à Deezer pour 38 morceaux sur 40.
- **Erreurs corrigées en route** :
  - un premier taux de correspondance (2 sur 40) venait de la recherche avancée de Deezer, qui renvoie zéro résultat : remplacée par la recherche simple (38 sur 40) ;
  - une mesure de dates faussée par le dépassement du quota de l'API Deezer : refaite en ralentissant les appels et en contrôlant chaque réponse ;
  - l'adresse e-mail d'Aurian avait été mise dans l'en-tête des requêtes envoyées aux services externes : le système de permissions l'a bloqué, elle a été retirée.

## 24 novembre 2026

### Choix de l'idée

- **Piste d'Aurian** ajoutée en tête : les motifs musicaux qu'on aime, avec le texte anglais pour le formulaire d'inscription. Commit `65b61be`.
- **Doc de contexte** (Claude Docs) : le hackathon, Deezer en 2026, 29 fonctionnalités Deezer recensées, la concurrence, les besoins sans équivalent. [Lien](https://claude.ai/artifact/Lp3ErLQGPmYRccJXam1nt3).
- **Pistes A et B corrigées** : elles recoupaient des fonctions lancées par Spotify en 2026 (SongDNA, About the Song, Taste Profile). Commit `dad1dbd`.
- **Dépôt créé** (privé) avec le README et trois premières pistes. Commit `dc109c0`.

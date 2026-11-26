# Registre du travail de Claude

Chaque étape du projet a ici une entrée datée, la plus récente en haut, avec ce qui a été fait, ce qu'on a trouvé et le commit correspondant. Les résultats détaillés sont dans [`docs/faisabilite.md`](docs/faisabilite.md) et l'idée dans [`docs/idee.md`](docs/idee.md).

## Où on en est

- **Idée validée** : repérer ce qu'un auditeur aime dans trois piliers (suites d'accords, mouvements de la basse, rythme) et lui proposer des morceaux qui le partagent, en lui disant pourquoi, avec un agent vocal incarné par un avatar 3D.
- **Architecture** : proposée dans [`docs/architecture.md`](docs/architecture.md), à valider avec l'équipe.
- **Faisabilité** : établie en partant de l'audio des extraits Deezer ; la basse qui descend est validée à l'oreille par Aurian sur 5 morceaux.
- **Accords enrichis** : un modèle de deep learning existant (lv-chordia) mesure la part de septièmes et de neuvièmes d'un morceau ; testé sur 15 extraits.
- **Suites de degrés** : IV–V–I, ii–V–I, cadence rompue, iv emprunté… se repèrent dans l'audio ; les suites rares révèlent un goût dès 5 morceaux, IV–V–I en demande davantage.
- **Pistes ouvertes par Aurian le 26/11** : l'analyse du rythme (kick, charleston, espace), des réglages manuels façon Flow Tuner, un agent vocal avec avatar 3D.
- **À faire** : le test d'Aurian sur ses propres morceaux ; l'écoute des 4 morceaux restants ; les questions aux organisateurs (code préparé autorisé ? clé Gradium ?) ; l'inscription.

## 26 novembre 2026

### Architecture proposée

- **Demande d'Aurian** : si les trois piliers tiennent, penser l'architecture (web app, base de données, agent vocal avec avatar 3D).
- **Fait** : [`docs/architecture.md`](docs/architecture.md). On y trouve :
  - la vue d'ensemble : Next.js, API serveur, service d'analyse Python, Supabase ;
  - les critères de chaque pilier, et le cœur (profil, recommandation, curseurs) ;
  - l'agent vocal (Claude, Gradium) et l'avatar 3D (TalkingHead) ;
  - les tables, le catalogue, l'hébergement, le découpage en 30 heures et les questions à trancher.
- **Vérifié en route** : TalkingHead exige un avatar à squelette compatible Mixamo, avec les expressions ARKit et Oculus, et peut caler les lèvres directement sur le son (HeadAudio). Ready Player Me a fermé le 31 janvier 2026 ; restent notamment Avaturn, MetaPerson et VRoid.
- **À trancher** : le modèle de l'agent et sa latence, l'avatar, l'hébergement de l'analyse, le code préparé, le nom du produit.

### Les trois piliers validés : harmonie, basse, rythme

- **Demande d'Aurian** : exploiter trois piliers, les suites d'accords, les mouvements de la basse (pas seulement la descente) et le rythme (kick, caisse claire, charleston, percussions afro par les fréquences).
- **Fait** :
  - mouvements de basse sur 189 extraits des tops et 10 morceaux connus ([`mouvements_basse.py`](experiences/mouvements_basse.py)) ;
  - rythme par bandes de fréquences sur une grille de 16 doubles-croches, sur 6 styles ([`rythme.py`](experiences/rythme.py)).
- **Résultats** :
  - basse : 47 qui marchent, 30 qui sautent, 12 qui montent, 8 qui descendent, 5 qui tiennent une note, 87 mixtes ; Stand By Me ressort bien en basse qui marche ;
  - rythme : le rock a peu de contretemps (4 %) et beaucoup d'air (62 %), l'afrobeats est le plus syncopé (47 à 49 % de contretemps), le disco et le reggaeton sont les plus denses ;
  - limites : chromatisme gonflé par le kick dans les graves, tempo parfois faux du simple au double, médiums pollués par les voix.
- **Conclusion** : les trois piliers sont mesurables ; l'idée est validée. Pour la précision : isoler basse et batterie, puis Beat This! et ADTOF, encore à tester.

### Les suites de degrés : peut-on dire à quelqu'un qu'il aime les IV–V–I ?

- **Demande d'Aurian** : si on détecte les accords, peut-on aussi détecter les suites appréciées, en solfège (IV–V–I…) ?
- **Fait** : un module qui estime la tonalité, chiffre les accords en degrés et repère dix suites ([`experiences/degres.py`](experiences/degres.py)). Vérifié sur 10 suites écrites (8 lues comme attendu, 2 ambiguës par nature), puis sur l'audio de 14 extraits ([`test_degres.py`](experiences/test_degres.py)), puis sur 169 873 morceaux de Chordonomicon ([`frequences_suites.py`](experiences/frequences_suites.py)).
- **Résultats** :
  - audio : tonalité juste pour 11 morceaux sur 14 ; la boucle I–V–vi–IV est repérée sur les 5 morceaux qui l'ont, Stand By Me ressort en suite des années 50 avec IV–V–I, Hit the Road Jack en cadence andalouse ;
  - fréquences : IV–I 61,7 %, IV–V–I 34,6 %, cadence rompue 27,6 %, boucle I–V–vi–IV 17,5 %, années 50 13,8 %, ii–V–I 13,1 %, II–V–I 6,1 %, bVII–IV–I 4,5 %, iv emprunté 4,1 %, andalouse 1,3 % ;
  - la tonalité est ambiguë dans 32 % des morceaux (relative majeure ou mineure, modes).
- **Erreurs et corrections** :
  - le modèle de tonalité ignorait l'accord bVII du rock : ajouté ;
  - la cadence andalouse sautait quand le premier accord était lu majeur : rendue tolérante ;
  - ma référence pour Get Lucky était incomplète, puisque les sources hésitent entre si dorien et fa# mineur.
- **Conclusion** : oui, on peut dire à quelqu'un quelles suites il aime, avec deux règles. Une suite courante comme IV–V–I demande 5 morceaux sur 5 ou 8 sur 10 ; une suite rare (ii–V–I, iv emprunté, andalouse) se repère dès 4 sur 5. Et l'app annonce toujours le motif le plus rare, jamais les cadences contenues dans une boucle.

### Documentation : le registre et les scripts de mesure

- **Demande d'Aurian** : un registre sur GitHub pour suivre le travail.
- **Fait** : ce registre ; les 11 scripts de mesure dans [`experiences/`](experiences/), avec leur mode d'emploi et les pièges rencontrés. Ceux qui avaient été lancés directement dans le terminal y sont enregistrés tels qu'ils ont tourné.

### Test d'un modèle d'accords enrichis par deep learning

- **Demande** : savoir si un modèle existant reconnaît les septièmes et les neuvièmes sur nos extraits Deezer, sans avoir à entraîner de modèle.
- **Fait** : installation isolée de Python 3.12, PyTorch et [lv-chordia](https://github.com/openmirlab/lv-chordia), autorisée par Aurian après un premier blocage du système de permissions. Test sur 15 extraits : les 10 morceaux simples déjà mesurés avec Essentia, et 5 morceaux riches en septièmes (Moondance, Isn't She Lovely, Get Lucky, Fly Me to the Moon, Smooth). Script : [`experiences/test_lvchordia.py`](experiences/test_lvchordia.py).
- **Résultats** :
  - 96 % du temps sur les bonnes triades, contre 77 % pour Essentia ; « Hit the Road Jack » passe de 36 % à 76 %, avec ses quatre basses descendantes exactes ;
  - il reconnaît septièmes, neuvièmes et accords demi-diminués, mais l'accord exact n'est juste que 56 % du temps sur les morceaux à septièmes, avec des références approximatives ;
  - la part d'accords enrichis sépare bien les morceaux : 90 à 100 % pour Moondance, Isn't She Lovely et Fly Me to the Moon, 56 % pour Smooth, 0 à 23 % pour les 10 morceaux simples ; seul « Get Lucky » est raté (0 %) ;
  - 2 s par extrait de 30 s sur le processeur du Mac.
- **Conclusion** : le critère « couleurs d'accords » est mesurable à l'échelle d'un morceau ; nommer chaque accord à l'auditeur reste trop incertain. Étude mise à jour dans [`docs/faisabilite.md`](docs/faisabilite.md).

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

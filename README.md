# Hackathon Deezer 2026

Notre projet pour le [Deezer Hackathon](https://luma.com/0dfd8jau), organisé par Unaite avec Deezer, du samedi 28 novembre 2026 à 9 h 30 au dimanche 29 novembre à 19 h, chez Deezer (24 rue de Calais, Paris 9e).

**Ce dépôt est la préparation (24 au 26 novembre) ; le code du hackathon est dans [`hackdeezer-2026`](https://github.com/CodeurFort/hackdeezer-2026).** La piste retenue : Repérer les motifs musicaux qu'un auditeur aime (suites d'accords, couleurs d'accords, gammes) et lui proposer des morceaux qui ont les mêmes, en lui disant pourquoi. Le détail, les autres pistes et nos critères sont dans [`docs/idee.md`](docs/idee.md) ; le concept et ses arguments sont dans [`docs/concept.md`](docs/concept.md) ; l'architecture proposée est dans [`docs/architecture.md`](docs/architecture.md) ; le suivi du travail, étape par étape, est dans le [registre](REGISTRE.md) ; ce qui existe déjà chez Deezer et ses concurrents est dans le [doc de contexte](https://claude.ai/artifact/Lp3ErLQGPmYRccJXam1nt3).

## L'événement

| | |
|---|---|
| Piste visée | **New-gen audio experience** (« Listening personalization with generative AI » dans le formulaire) : l'expérience des auditeurs et des artistes, de nouvelles façons de créer des playlists et d'interagir avec la musique et les artistes, avec les modèles vocaux de Gradium |
| Autre piste | Data challenge : une compétition sur des données massives, préparée par Unaite et Deezer |
| Équipe | 3 à 4 personnes, sur place les deux jours, nuit comprise (pas de distanciel) |
| Inscription | individuelle pour chaque membre, validée par les organisateurs, gratuite |
| À apporter | ordinateur, chargeur, sac de couchage |

La question posée par Deezer : *« How does your app actually know what you want to hear next? And how could it get even better at it? »*

## Ce qu'on a vérifié (24 novembre 2026)

- **API publique Deezer, sans clé** : la recherche, les fiches morceau, les artistes proches, la radio d'un artiste, les classements et les extraits audio de 30 s répondent (testé). La création de nouvelles applications Deezer est suspendue : pas d'accès à l'historique d'écoute d'un utilisateur par l'API publique.
- **Gradium** (issu du labo Kyutai) : synthèse vocale, transcription, traduction vocale en direct, clonage de voix à partir de 10 s, création d'une voix à partir d'une description, modèle embarqué Phonon. Cinq langues dont le français et l'anglais, premier son en moins de 300 ms en streaming, SDK Python ([documentation](https://docs.gradium.ai/guides/introduction)).
- **Ce qui existe déjà** : chez Deezer, Flow, Flow Tuner, Playlist avec IA et un filtre pour écarter la musique générée par IA (annoncé en octobre 2026) ; chez Spotify, un DJ IA qui prend les demandes à la voix depuis mai 2025 et parle français.

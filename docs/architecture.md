# Architecture

Proposition du 26 novembre 2026, à valider avec l'équipe. Chaque brique porte son statut : **mesuré** (testé sur nos extraits, chiffres dans [`faisabilite.md`](faisabilite.md)), **vérifié** (lu dans la documentation officielle), ou **à tester**.

## En une phrase

L'auditeur donne cinq morceaux. L'analyse audio en tire trois familles de critères (harmonie, basse, rythme) et les compare au reste du catalogue pour trouver ce qui le distingue. Un agent vocal, incarné par un avatar 3D, lui explique ses goûts et lui fait écouter des morceaux qui les partagent. Des curseurs lui permettent d'ajuster.

## Vue d'ensemble

```
 Navigateur (Next.js, inspiré du web Deezer)
 ├─ recherche de morceaux, lecteur d'extraits, curseurs
 ├─ avatar 3D (TalkingHead, three.js) ◄── audio + minutage des mots
 └─ micro ──► Gradium STT (WebSocket, jeton court)        Gradium TTS ──┘
        │
        ▼
 API Next.js (routes serveur, TypeScript)
 ├─ /api/recherche   proxy de l'API Deezer, quota respecté
 ├─ /api/profil      fait analyser les 5 morceaux, calcule le profil
 ├─ /api/reco        classe le catalogue selon le profil et les curseurs
 ├─ /api/agent       Claude : explication et actions (curseurs, lecture)
 └─ /api/jeton-voix  jeton court Gradium pour le navigateur
        │                                   │
        ▼                                   ▼
 Service d'analyse (Python, FastAPI)    Supabase (Postgres + pgvector)
 extrait Deezer ─► pistes séparées      morceaux, caractéristiques,
 (Demucs) ─► notes (Basic Pitch),       sessions, profils,
 accords (lv-chordia), temps (Beat      recommandations, retours
 This!) ─► mélodie, harmonie, basse,
 rythme, tempo
        ▲
        └── catalogue pré-calculé : quelques milliers de titres Deezer
```

## Les cinq couches du squelette, critère par critère

Le concept et ses arguments sont dans [`concept.md`](concept.md). Les scripts cités ont servi aux mesures avant l'événement ; ils sont retirés du dépôt et le code sera réécrit pendant le hackathon.

| Couche | Critères calculés | Outils | Statut |
| --- | --- | --- | --- |
| Mélodie et gamme | Notes seules ou accords ; gamme et couleur modale, avec un niveau de confiance ; appoggiatures et notes étrangères sur les temps | Demucs (voix et instruments), Basic Pitch (notes), lv-chordia, Essentia (clé), `mode.py`, `notes_et_appoggiatures.py` | **Mesuré** : notes seules nettes (Mask Off 89 %) ; mode juste une fois sur deux ; appoggiatures en tête sur Someone Like You |
| Harmonie | Tonalité et ambiguïté ; suites (IV–V–I, ii–V–I, cadence rompue, iv emprunté, bVII–IV–I, boucle I–V–vi–IV, années 50, andalouse) ; part d'accords enrichis ; rythme harmonique (durée des accords en temps) ; surprise des enchaînements | lv-chordia, `degres.py`, Beat This! | **Mesuré** : 96 % du temps sur les bonnes triades, tonalité juste 11 fois sur 14, fréquences sur 169 873 morceaux, rythme harmonique cohérent. Surprise **à construire** |
| Basse | Mouvement : descentes, montées, pas conjoints, sauts, chromatisme. Type : 808, reese, guitare, synthé | Demucs (basse isolée), `basse_audio.py`, `mouvements_basse.py`, `type_basse.py` | Mouvement **mesuré**, validé à l'oreille 5 fois sur 5. Type **exploratoire** : la reese ressort, 808 et synthé confondues |
| Rythme | Densité de kick, caisse claire, charleston ; syncope ; air ; motif sur 16 pas ; percussions par bande de fréquence | `rythme.py` ; batterie isolée par Demucs ; ADTOF | Bandes **mesurées** sur 6 styles ; ADTOF **à tester** |
| Tempo | Tempo compté et tempo ressenti ; mesure | Beat This!, Essentia | **Mesuré** : juste 11 fois sur 11 en admettant les deux lectures que donnent les sites ; le rythme harmonique tranche le ressenti |

Pour l'afro, on ne nomme pas chaque percussion (conga, shaker) : on décrit ce qu'elle fait. Les aigus serrés et à contretemps signalent les shakers, les médiums syncopés les percussions, et le motif 3+3+2 se lit sur la grille de 16 pas.

## Le cœur : profil, recommandation, réglages

1. **Profil.** Pour chaque critère, on compare la valeur des cinq morceaux de l'auditeur à sa distribution dans le catalogue. On ne garde que les critères qui le distinguent vraiment : probabilité que ce soit le hasard sous 1 %, comme dans l'étude (4 morceaux sur 5 pour un motif rare, 5 sur 5 pour IV–V–I).
2. **Règle d'annonce.** On annonce le motif le plus rare, jamais les cadences contenues dans une boucle. Quand la tonalité est ambiguë (32 % des morceaux), on décrit le mouvement (« la basse descend d'un ton ») plutôt que des chiffres.
3. **Recommandation.** Le score d'un morceau est la proximité pondérée sur les critères distinctifs ; chaque poids vient de la force du critère et du réglage du curseur. On exclut les morceaux et les artistes donnés, et on évite trois titres du même artiste.
4. **Raisons.** Chaque recommandation porte ses raisons sous forme de données : les critères partagés et leurs valeurs. L'agent ne fait que les dire, il n'invente rien.
5. **Curseurs.** Un curseur par critère distinctif, plus trois toujours présents : aéré ↔ dense, percussions douces ↔ incisives, basse qui monte ↔ qui descend. Bouger un curseur reclasse le catalogue déjà chargé dans le navigateur, sans aller-retour serveur.

Une valeur non mesurée reste vide (`null`), jamais zéro : un morceau sans temps détectés n'est pas « sans syncope ».

## L'agent vocal

- **Cerveau** : Claude, par l'API Anthropic (SDK TypeScript), modèle `claude-opus-5` par défaut, réponses en streaming, avec le repli automatique côté serveur en cas de refus. Il reçoit le profil et les raisons en JSON, et répond en phrases courtes. Ses outils : régler un curseur, lancer un extrait, passer au morceau suivant. Ce que dit l'auditeur est traité comme une donnée, jamais comme une consigne. **À tester** : la latence d'un tour de parole.
- **Voix** : synthèse Gradium en streaming, en français, avec le minutage des mots. Transcription Gradium en streaming pour les commandes (« plus aéré », « pourquoi ce morceau ? »), avec détection de fin de phrase. Dans le navigateur, un jeton court évite d'exposer la clé. **Vérifié** dans la documentation, **à tester** avec une clé.

## L'avatar 3D

- **Moteur** : TalkingHead, un avatar 3D dans le navigateur avec three.js. Il synchronise les lèvres sur le minutage des mots, ou directement sur le son avec son module HeadAudio, et gère le français. **Vérifié** dans sa documentation.
- **Le modèle 3D** doit avoir un squelette compatible Mixamo et les expressions du visage ARKit et Oculus. Ready Player Me, la source habituelle, a fermé le 31 janvier 2026. Restent notamment Avaturn (TalkingHead fournit un exemple avec), MetaPerson et VRoid. Un avatar généré par une IA de modélisation 3D n'a pas ces expressions : trop risqué en 30 heures. **À tester** : un avatar Avaturn ou MetaPerson chargé dans TalkingHead.
- **Performance** :
  - la scène n'est redessinée que quand l'avatar est visible et qu'il parle ou bouge, et tout s'arrête quand l'onglet est caché ;
  - fichier 3D léger, textures compressées ;
  - aucun effet animé en boucle derrière un fond flouté ;
  - images par seconde mesurées sur un téléphone moyen, avec un mode dégradé (portrait fixe et onde sonore) sous 30 images par seconde.
- **Plan B** : si l'avatar n'est pas prêt, la voix et une onde sonore animée portent la démo.

## Les données (Supabase)

| Table | Contenu | Remarques |
| --- | --- | --- |
| `morceaux` | identifiant Deezer, ISRC, titre, artiste, adresse de l'extrait, date de sortie, origine (catalogue ou auditeur) | l'identifiant Deezer est la clé |
| `caracteristiques` | version de l'analyse ; harmonie, basse et rythme en JSON ; un vecteur pgvector pour chercher vite les morceaux proches | `null` = non mesuré ; la version permet de tout recalculer quand l'analyse change |
| `sessions` | morceaux donnés, réglages des curseurs | pas de compte : une session anonyme |
| `profils` | critères distinctifs, avec la valeur, la moyenne du catalogue et la probabilité de hasard | un profil par session |
| `recommandations` | morceau, rang, score, raisons | les raisons nourrissent l'agent |
| `retours` | « j'aime » ou non, remarque dite à voix haute | utile pour la démo et pour régler les poids |

Le navigateur ne lit que le catalogue ; toutes les écritures passent par l'API serveur.

## Le catalogue

- Quelques milliers de titres Deezer pris dans les playlists éditoriales par genre (rap français, afro, rock, jazz, pop…) et les radios d'artistes.
- Sans séparation des pistes, environ 2 à 3 secondes d'analyse par titre sur le processeur, en parallèle sur 8 cœurs : à lancer dès la première heure, en tâche de fond.
- La séparation des pistes (Demucs) prend 23 secondes par extrait sur le processeur (mesuré). Elle sert en direct pour les 5 morceaux de l'auditeur, lancée dès le premier morceau cité. Pour le catalogue, on choisit : une carte graphique louée, un catalogue réduit à quelques centaines de titres, ou les critères mesurables sans séparation.
- Métadonnées sous le quota de l'API Deezer, une dizaine de requêtes par seconde au plus ; les extraits audio ne sont pas concernés.
- Chordonomicon n'entre pas dans la première version.

## Hébergement

- **Écran et API Next.js** : Vercel.
- **Service d'analyse** : il charge PyTorch et plusieurs modèles, donc il lui faut quelques gigaoctets de mémoire. Toutes nos mesures tournent sur le processeur ; seule la séparation des pistes à grande échelle demande une carte graphique. Il tourne sur un portable de l'équipe exposé par un tunnel pendant la démo, ou sur une machine louée.
- **Base** : Supabase.
- **Secrets** : les clés Anthropic, Gradium et Supabase restent côté serveur ; le navigateur reçoit un jeton court pour la voix.

## Découpage pour 30 heures à 3 ou 4

| Bloc | Contenu | Langage |
| --- | --- | --- |
| 1. Analyse et catalogue | Assembler les modules mesurés en un service ; lancer le catalogue tôt | Python |
| 2. Profil, recommandation, curseurs | Le cœur : une démo complète sans voix ni avatar | TypeScript et Python |
| 3. Agent vocal | Claude, transcription et synthèse Gradium | TypeScript |
| 4. Écran et avatar | Next.js inspiré du web Deezer, TalkingHead | TypeScript |

Jalons :
- **6e heure** : un morceau analysé de bout en bout ;
- **12e heure** : profil et recommandations sur un catalogue partiel ;
- **18e heure** : la voix ;
- **24e heure** : l'écran et l'avatar ;
- **28e heure** : gel du code, répétition de la démo et du plan B.

Si l'équipe prend du retard, on coupe dans cet ordre : l'avatar, puis les curseurs, puis le rythme précis (on garde les bandes de fréquences).

## À trancher ensemble

1. **Le modèle de l'agent** : Claude Opus 5 par défaut. Si la latence d'un tour de parole est trop longue, on décide ensemble d'un effort plus bas ou d'un autre modèle.
2. **L'avatar** : un personnage générique (Avaturn ou MetaPerson), un avatar tiré d'un selfie, ou un style propre.
3. **Le service d'analyse** : un portable et un tunnel, ou une machine louée.
4. **Le code préparé avant l'événement** : à demander aux organisateurs.
5. **Le nom du produit** : à choisir avant de dessiner le premier écran ; trois pistes dans [`concept.md`](concept.md).
6. **Le catalogue** : carte graphique louée pour séparer les pistes, catalogue réduit, ou critères sans séparation.

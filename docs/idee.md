# Choisir l'idée

Ce document sert à se mettre d'accord. On y garde les pistes, les critères qui les départagent, ce qu'on ignore encore, et la décision finale avec sa date.

## Ce que le jury attend

La page de l'événement pose la question : comment ton app sait ce que tu veux entendre ensuite, et comment elle pourrait faire mieux ? La piste demande de travailler l'expérience des auditeurs **et** des artistes : créer des playlists autrement, interagir autrement avec la musique et les artistes, avec les voix de Gradium.

## Nos critères, dans l'ordre

1. **La démo fait réagir en trois minutes**, idéalement avec un membre du jury qui participe.
2. **Elle répond à la question du jury** (la personnalisation), pas à côté.
3. **La voix sert l'expérience** (mains libres, récit, langue) ; ce n'est pas un gadget ajouté à la fin.
4. **Deezer pourrait la livrer demain** sans renier ses choix : les artistes humains, l'auditeur aux commandes de l'algorithme (Flow Tuner), les vrais fans.
5. **Elle tient en une trentaine d'heures** à trois ou quatre, avec les données vraiment disponibles (API publique, extraits de 30 s).
6. **Ce n'est pas une copie** de ce qui existe chez Deezer ou ses concurrents : tout est recensé dans le [doc de contexte](https://claude.ai/artifact/Lp3ErLQGPmYRccJXam1nt3).

## La piste d'Aurian : les motifs musicaux qu'on aime

**L'idée.** Repérer les motifs musicaux qu'un auditeur aime sans savoir les nommer (suites d'accords, couleurs d'accords, gammes et modes), puis lui proposer des morceaux qui ont les mêmes, en lui disant pourquoi. Au départ, une intuition d'Aurian : « j'aime les suites d'accords qui descendent, je ne sais pas pourquoi ».

**La démo.** Un juré donne cinq morceaux qu'il adore, ou une playlist publique Deezer. Vingt secondes plus tard, une voix lui dit : « Quatre de tes cinq morceaux ont une basse qui descend. Écoute. » Elle joue la suite d'accords seule pendant que l'écran la montre, puis lance trois morceaux qu'il ne connaît pas et qui ont la même.

**Pourquoi ça peut gagner.**

- Elle répond à la question du jury par le pourquoi : « tu aimes les basses qui descendent, en voilà d'autres », et non « les gens comme toi écoutent ça ».
- La science la soutient : sur 745 tubes du Billboard, le plaisir musical dépend du dosage entre incertitude et surprise dans les suites d'accords ([Cheung et al., 2019](https://www.cell.com/current-biology/fulltext/S0960-9822(19)31258-8)).
- Elle prolonge ce que fait Deezer : un algorithme qu'on comprend et qu'on règle (paramètres de l'algorithme, Flow Tuner), et l'écriture des artistes humains mise en valeur. Deezer Research parle ce langage : elle a publié [Spleeter](https://research.deezer.com/projects/spleeter.html), qui sépare voix, batterie et basse.
- La voix et l'image y ont un vrai rôle : la voix Gradium explique en jouant la suite d'accords, l'écran montre la basse qui descend pendant l'écoute.

**Ce qui existe déjà** (recherches du 24 novembre 2026). Rien d'équivalent trouvé dans une app de streaming. Les plus proches :

- Pandora et son [Music Genome Project](https://en.wikipedia.org/wiki/Music_Genome_Project) : environ 450 caractéristiques par morceau, dont l'harmonie, notées à la main par des musiciens et utilisées pour recommander. Aucun profil harmonique montré à l'auditeur, d'après ce qu'on a vu.
- [Hooktheory](https://www.hooktheory.com/theorytab) : on construit une suite d'accords et on voit les morceaux qui l'utilisent. C'est fait pour les musiciens et n'apprend le goût de personne ; de petits outils font pareil ([Progressions](https://github.com/Ljfernando/Progressions)).
- Spotify : le Taste Profile (comment l'app comprend tes goûts) et SongDNA (samples, reprises, producteurs), rien sur l'harmonie.

**Comment.**

1. Entrée : cinq morceaux cherchés sur Deezer, ou une playlist publique Deezer, lisible sans clé avec les codes ISRC (testé).
2. Analyse de l'audio de chaque extrait de 30 secondes, en 2 à 3 secondes : la basse suivie temps par temps, les accords y compris enrichis (septièmes, neuvièmes) grâce à un modèle de deep learning pré-entraîné, et la tonalité. En complément, le jeu de données [Chordonomicon](https://huggingface.co/datasets/ailsntua/Chordonomicon) (679 807 morceaux, accords section par section, tirés d'Ultimate Guitar) donne les accords enrichis des morceaux plus anciens ; on le relie à Deezer par l'aperçu public de Spotify, sans compte (38 morceaux sur 40 retrouvés).
3. Motifs, calculés pour chaque morceau : basse qui descend, suites de degrés (IV–V–I, ii–V–I, cadence rompue, iv emprunté…), boucles de quatre accords, accords enrichis (septièmes, sus, add9), mode majeur ou mineur, modulations, degré de surprise des accords.
4. Profil : les motifs plus fréquents dans les morceaux aimés que dans l'ensemble du catalogue.
5. Recommandation : des morceaux qui partagent ces motifs, chacun avec sa raison.
6. Restitution : la voix Gradium explique, et un visuel de la suite d'accords suit l'extrait.

**Les risques.**

- La justesse de l'analyse : 96 % du temps sur les bons accords simples, mais l'accord enrichi exact n'est juste qu'une fois sur deux. On mesure donc la part d'accords enrichis d'un morceau sans nommer chaque accord. Et 30 secondes peuvent tomber à côté du refrain. Le détail est dans [`faisabilite.md`](faisabilite.md).
- Les données d'accords : Chordonomicon couvre mal la musique française récente (au mieux 9 % du Top France actuel) et note rarement la basse.
- La licence de Chordonomicon est CC BY-NC 4.0 : usage non commercial en citant la source. Ça convient pour un prototype de hackathon, pas pour un produit Deezer commercialisé tel quel.
- Le goût n'est pas que de l'harmonie : chez certains, c'est le rythme, la voix ou le son. L'app doit le dire franchement quand aucun motif ne ressort.
- L'API Deezer ne donne plus l'historique d'écoute : la démo part d'une playlist publique ou de morceaux cités.

**Faisabilité.** Étudiée et mesurée le 25 novembre 2026 dans [`faisabilite.md`](faisabilite.md) : faisable si l'on part de l'audio des extraits Deezer, le jeu de données d'accords ne servant que de complément.

**À vérifier avant le hackathon.**

- [x] L'accès à l'API Spotify : inutile, l'aperçu public de Spotify suffit pour relier Chordonomicon à Deezer.

    Vérifié le 25 novembre 2026.
- [x] Un outil open source de détection d'accords sur les extraits de 30 secondes : Essentia, 77 % du temps sur les bons accords.

    Vérifié le 25 novembre 2026, sur 10 morceaux.
- [ ] La suite est dans [`faisabilite.md`](faisabilite.md) : le test d'Aurian sur ses propres morceaux, l'écoute des morceaux signalés, la mesure des erreurs de la détection de basse, et les questions aux organisateurs.

## Les autres pistes (proposées par Claude)

Écrites le 24 novembre avant l'état de l'existant ; A et B recoupent des fonctions de Spotify.

### A. Le voyage : découvrir, guidé par une voix

**L'idée.** Tu donnes un artiste que tu aimes. Une voix t'emmène en cinq étapes vers une musique que tu n'aurais jamais écoutée, et raconte chaque passage : une influence, un sample, un producteur en commun, une même scène.

**La démo.** Un membre du jury dit un artiste à voix haute. Moins d'une minute après, le voyage commence : la voix parle sur la fin de chaque extrait, la carte du trajet se dessine à l'écran, et il peut dire « plus loin » ou « reviens » pour changer de route.

**Pourquoi ça peut gagner.** Ce que tu veux entendre ensuite, c'est parfois ce que tu ne connais pas encore, et l'app te dit pourquoi elle te le propose. La voix est le cœur du produit (le récit), et Deezer y trouve la découverte d'artistes humains.

**Comment.** L'API publique Deezer (artistes proches, radios, extraits), des faits tirés de sources (Wikipédia, MusicBrainz), un LLM qui écrit le récit à partir de ces sources seulement, la voix du guide créée avec Gradium (création de voix par description) et le pilotage à la voix (transcription Gradium).

**Le risque.** Le terrain est déjà occupé : Spotify relie samples, reprises et producteurs avec SongDNA et raconte les morceaux avec About the Song (2026), et YouTube Music teste des animateurs IA qui racontent les titres (Beyond the Beat). S'y ajoute le fait inventé, dit à voix haute devant le jury ; parade : aucune phrase sans source, comme dans un RAG.

### B. Ton profil, en clair : la personnalisation qui s'explique

**L'idée.** L'app te dit à voix haute ce qu'elle croit savoir de tes goûts. Tu la corriges en parlant (« le metal, c'était mon frère »), et chaque correction devient une règle durable, visible et modifiable.

**La démo.** Un membre du jury cite cinq artistes. L'app lui résume son profil en dix secondes ; il la corrige à voix haute ; la file d'écoute se réordonne devant lui, avec la raison de chaque morceau.

**Pourquoi ça peut gagner.** C'est la question du jury prise au pied de la lettre, et l'étape d'après Flow Tuner : des interrupteurs à la conversation.

**Comment.** La transcription et la synthèse Gradium en streaming pour une vraie conversation, l'API publique Deezer pour les morceaux candidats, un LLM qui tient le profil et classe les morceaux.

**Le risque.** Sans vrai historique d'écoute (la création d'apps Deezer est suspendue), le profil part de cinq artistes : c'est moins magique. Et l'idée existe déjà : Deezer montre les titres qui influencent son algorithme (2025), et Spotify teste depuis 2026 un Taste Profile pour voir et façonner son profil de goûts.

### C. La voix de l'artiste, dans ta langue : le lien entre l'artiste et ses fans

**L'idée.** L'artiste enregistre un message une fois, en français. Chaque fan le reçoit dans sa langue, avec la voix de l'artiste, et adapté à son écoute (« tu fais partie de ceux qui ont le plus écouté ce titre à Lisbonne »).

**La démo.** L'un de nous enregistre quinze secondes en français devant le jury, qui l'entend aussitôt en anglais, en espagnol ou en allemand, avec la même voix. Puis l'écran du fan.

**Pourquoi ça peut gagner.** C'est la moitié « artistes » de la piste, que la plupart des équipes laisseront de côté, et elle utilise les capacités les plus rares de Gradium. Spotify a testé en 2023 la traduction de podcasts dans la voix de l'animateur, pas les messages d'un artiste à ses fans.

**Comment.** Gradium fait le plus dur : transcription, puis synthèse dans la langue du fan avec la voix clonée de l'artiste (10 s d'échantillon suffisent). Il reste l'espace artiste, le consentement, le choix des fans et l'écran du fan.

**Le risque.** Le clonage de voix peut gêner Deezer, qui signale la musique générée par IA : le consentement de l'artiste et la mention « voix traduite par IA, validée par l'artiste » doivent être au centre du produit. Et la personnalisation y est plus faible que dans A et B.

## Ce qu'on ne sait pas encore

- Les critères du jury, les prix, la durée et le format du pitch : rien n'est publié.
- Des données Deezer fournies sur place (historiques d'écoute, API interne) ? Si oui, la piste B devient beaucoup plus forte.
- Le code préparé avant l'événement est-il autorisé ? À demander aux organisateurs.
- L'accès à Gradium (clés, crédits) : annoncé, conditions inconnues.
- Les morceaux complets : l'API publique ne donne que des extraits de 30 s.

## Décision

À prendre ensemble. On écrira ici l'idée retenue, la date, pourquoi elle, et ce qu'on a écarté.

En tête depuis le 24 novembre 2026 : la piste d'Aurian, les motifs musicaux qu'on aime. Elle reste à valider avec l'équipe.

Ma proposition de départ (A, le voyage) ne tient plus : les recherches du 24 novembre 2026 montrent que A et B recoupent des fonctions lancées par Spotify en 2026. Le [doc de contexte](https://claude.ai/artifact/Lp3ErLQGPmYRccJXam1nt3) recense ce qui existe chez Deezer et ses concurrents, et les besoins pour lesquels rien n'a été trouvé.

## Texte pour le formulaire d'inscription

Case « Which track are you most interested in? » : *Listening personalization with generative AI*.

Case « Do you already have a project idea? If so tell us about it! » :

> Yes. Most of us love musical patterns we can't name: I love descending chord progressions and never knew why. We want Deezer to tell listeners why they love what they love. From a few favourite songs or a public playlist, our app finds the patterns a listener keeps coming back to (chord progressions, chord colours, scales and modes). A Gradium voice explains them out loud while the progression plays on screen, then the app plays new tracks that share them, each with a reason you can hear. Research links musical pleasure to surprise in chord progressions (Cheung et al., 2019); we want to make that personal.

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

## Les pistes

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

Ma proposition de départ (A, le voyage) ne tient plus : les recherches du 24 novembre 2026 montrent que A et B recoupent des fonctions lancées par Spotify en 2026. Le [doc de contexte](https://claude.ai/artifact/Lp3ErLQGPmYRccJXam1nt3) recense ce qui existe chez Deezer et ses concurrents, et les besoins pour lesquels rien n'a été trouvé.

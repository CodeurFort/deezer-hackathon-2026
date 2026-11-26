# Le squelette du son

Proposition du 26 novembre 2026, construite sur l'idée d'Aurian : le squelette d'un morceau, c'est sa mélodie, son harmonie, sa basse, son rythme et son tempo. Chaque chiffre vient d'une mesure de [`faisabilite.md`](faisabilite.md), et chaque affirmation scientifique est liée à sa source. Le nom reste à choisir.

## La promesse

Tu aimes des morceaux sans savoir pourquoi, et ton app non plus ne le sait pas. Nous, on passe ta musique aux rayons X : on trouve ce que tes morceaux préférés ont en commun sous la peau, on te le fait **entendre**, puis on te fait découvrir d'autres morceaux qui ont le même squelette.

## Pourquoi ça touche : ce que dit la recherche

| Recherche | Ce qu'elle a montré | Ce qu'on en fait |
| --- | --- | --- |
| [Sloboda (1991)](https://journals.sagepub.com/doi/10.1177/0305735691192002), 83 auditeurs | Les larmes viennent surtout des séquences et des appoggiatures, dont le cycle de quintes qui descend vers la tonique. Les frissons viennent des harmonies nouvelles ou inattendues. La syncope répétée et les changements brusques de texture font aussi partie des déclencheurs | Détecteur d'appoggiatures, basse qui descend, syncope, changements de texture grâce aux pistes séparées |
| [NPR (2012)](https://www.npr.org/2012/02/13/146818461/the-ballad-of-the-tearful-why-some-songs-make-you-cry), sur Someone Like You | Le titre d'Adele fait pleurer grâce à ses appoggiatures, des notes qui frottent avant de se résoudre | Notre détecteur classe Someone Like You premier sur 10 morceaux, avec 16 appoggiatures par minute |
| [Salimpoor et al. (2011)](https://www.nature.com/articles/nn.2726), *Nature Neuroscience* | Le cerveau libère de la dopamine pendant l'attente du passage fort, puis au moment du frisson | Une frise qui montre où un morceau prépare et où il résout |
| [Gagnon et Peretz (2003)](https://www.researchgate.net/publication/233618417_Mode_and_tempo_relative_contributions_to_happy-sad_judgements_of_equitone_music) | Ce qui rend une musique gaie ou triste dépend du tempo et du mode, et le tempo pèse plus que le mode | Le tempo ressenti devient un critère et un curseur à part entière |
| [Cheung et al. (2019)](https://www.cell.com/current-biology/fulltext/S0960-9822(19)31258-8) | Le plaisir naît du dosage entre incertitude et surprise dans les suites d'accords | Une mesure de surprise des enchaînements, à construire sur 680 000 suites d'accords |
| [Afchar et al. (2022)](https://arxiv.org/abs/2201.10528), Deezer Research | L'explicabilité renforce la confiance et le pardon envers les recommandations | Chaque recommandation porte une raison qu'on peut écouter |
| [Sguerra et al. (2025)](https://arxiv.org/abs/2507.16708), Deezer Research | Les profils de goût écrits par un modèle de langage ne conviennent pas à tous de la même façon : ça dépend du caractère grand public, du genre, du pays | Notre profil se mesure dans le son ; le modèle de langage ne fait que le dire, pour le rap et l'afro comme pour le grand public |

## Le squelette, couche par couche

| Couche | Ce qu'on en tire | Ce qu'on a mesuré | Fiabilité aujourd'hui |
| --- | --- | --- | --- |
| Mélodie et gamme | Notes seules ou accords ; gamme et couleur modale ; appoggiatures et notes qui frottent | Mask Off : 89 % de notes seules, 0 % d'accords. Mode juste sur 8 morceaux sur 17 choisis difficiles. Appoggiatures : Someone Like You 16 par minute, 0 pour Get Lucky, Despacito, Shape of You et Mask Off | Notes seules : nette. Mode : une fois sur deux, donc présenté comme une couleur, avec un niveau de confiance. Appoggiatures : tendance nette, à confirmer sur plus de morceaux |
| Harmonie | Suites (IV–V–I, ii–V–I, cadence andalouse…) ; couleurs (septièmes, neuvièmes) ; rythme harmonique ; surprise | 96 % du temps sur les bons accords ; suites rares repérées dès 5 morceaux ; Let It Be change d'accord tous les 2 temps, Get Lucky tous les 4 | Solide |
| Basse | Mouvement (marche, saute, monte, descend) ; type (808, reese, guitare, synthé) | Descentes confirmées à l'oreille 5 fois sur 5. La reese ressort par sa pulsation (4,3 contre 1,9 au plus) ; la 808 de Mask Off a la signature attendue | Mouvement : solide. Type : la reese oui ; 808 et basse synthé encore confondues, et Demucs range parfois la 808 avec la batterie |
| Rythme | Densité de kick, caisse claire, charleston ; syncope ; air ; motif sur 16 pas | L'afrobeats ressort le plus syncopé (47 à 49 % de contretemps), le rock le plus aéré (62 % de doubles-croches vides) | Bon pour distinguer les styles ; le détail par instrument (ADTOF) reste à tester |
| Tempo | Tempo compté et tempo ressenti | Beat This! juste sur 11 morceaux sur 11 en admettant les deux lectures. Les sites eux-mêmes hésitent : Zombie 165 ou 83, Let It Be 144 ou 72, Someone Like You 135 ou 67,5 | Solide ; le rythme harmonique tranche le ressenti (des accords tous les 2 temps à 144 se ressentent à 72) |

## Les moments de la démo

1. **« Écoute ce que tu aimes, à nu. »** Le juré donne cinq morceaux. L'app isole la couche qui les relie et la joue enchaînée : seulement leurs basses, ou seulement les voix au moment des appoggiatures. Il entend un fil commun qu'il n'avait jamais remarqué. La séparation prend 23 secondes par extrait : elle démarre dès le premier morceau cité, pendant que l'agent parle.
2. **« Tes frissons, à la seconde près. »** Une frise de chaque morceau marque les passages que la recherche associe aux larmes et aux frissons : appoggiature, basse qui descend, harmonie inattendue, syncope, changement de texture. Un geste, et l'app saute au moment.
3. **« Même squelette, autre peau. »** Les recommandations partagent le squelette, pas le genre. La basse qui descend de Ninho, on la retrouve chez Ray Charles en 1961 : on fait découvrir des artistes humains par ce qu'ils ont écrit.
4. **« Règle la musique, pas les genres. »** Des curseurs en mots simples : tempo ressenti, air, basse qui monte ou qui descend, couleur sombre ou lumineuse. L'agent explique ce qui change à l'oreille.
5. **« Ton squelette musical. »** Une carte à partager, dans l'esprit de My Deezer Year : les cinq couches dessinées comme une radiographie, avec les trois marqueurs les plus rares de la personne.
6. **Le guide.** L'agent vocal, incarné par l'avatar 3D, raconte la radiographie pendant qu'elle s'anime.

## Les arguments pour le jury

- **On décrit la musique de l'intérieur.** Les autres la décrivent de l'extérieur : Spotify par les genres, les artistes, les samples et les anecdotes (Taste Profile, SongDNA, About the Song) ; Pandora par 450 caractéristiques notées à la main et invisibles pour l'auditeur. Nous, par sa structure, et on la fait entendre.
- **Une explication qu'on entend.** C'est l'explicabilité que Deezer Research défend, rendue audible.
- **Un profil mesuré, pas imaginé.** Il répond au biais des profils écrits par modèle de langage, que Deezer Research a mesuré.
- **La science des émotions musicales**, citée et appliquée : Sloboda, Salimpoor, Gagnon et Peretz, Cheung.
- **Le métier des artistes humains mis en lumière.** Appoggiatures, lignes de basse, accords tenus : l'inverse de la musique générée, et cohérent avec la politique de Deezer sur l'IA.
- **Le Flow Tuner, en musical.** On passe des interrupteurs de genres au réglage de la musique elle-même.
- **Dans la lignée de Deezer.** La séparation des pistes, cœur de la démo, est le domaine de Spleeter, publié en open source par Deezer.
- **Un prolongement pour les artistes.** Deezer for Creators donne des statistiques ; on pourrait y ajouter le squelette que leurs fans aiment.

## Ce qu'on ne promet pas

- **Le mode global** n'est juste qu'une fois sur deux sur des extraits de 30 secondes : on parle de couleur, avec un niveau de confiance.
- **Le type de basse** : la reese ressort, mais la 808 et la basse synthé sont encore confondues.
- **Les appoggiatures** : la tendance est nette sur 10 morceaux, il faut la confirmer.
- **Le catalogue** : séparer les pistes de milliers de titres demande une carte graphique ou un catalogue réduit. Sur le processeur, 3 000 titres prendraient 19 heures.

## Le nom

À choisir par Aurian. Trois pistes :
- **Squelette** : son image de départ, très visuelle ;
- **Radiographie** : le jeu de mots avec la radio ;
- **Sous la peau** : la promesse d'aller sous la surface.

## Avant le 28 novembre

- [ ] Le test d'Aurian : 5 morceaux aimés, 5 autres. L'app retrouve-t-elle son squelette ?
- [ ] Écouter les 9 basses isolées et juger le type de chacune.
- [ ] Tester ADTOF sur la batterie, et la mesure de surprise des accords.
- [ ] Poser aux organisateurs les questions du code préparé et de la clé Gradium.

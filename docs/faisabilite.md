# Faisabilité : les motifs musicaux qu'on aime

Étude du 25 novembre 2026. Chaque chiffre vient d'une mesure faite ce jour-là sur les vraies données (API Deezer, jeu de données Chordonomicon, extraits audio), pas d'une estimation.

## Verdict

**Faisable en une trentaine d'heures, à une condition : partir de l'audio des extraits Deezer, pas d'un jeu de données d'accords.** Le motif de départ, la basse qui descend, se repère dans l'audio de n'importe quel extrait de 30 secondes en moins d'une demi-seconde, rap français compris. Les jeux de données d'accords couvrent mal la musique française récente et notent rarement la basse : ils restent un complément.

Deux points restent à prouver avant le 28 novembre : que la basse détectée est juste à l'oreille sur une cinquantaine de morceaux, et que l'app retrouve le motif d'Aurian à partir de ses propres morceaux (voir « Ce qu'il reste à valider »).

## Ce qu'on a mesuré

| Question | Mesure | Résultat | Conséquence |
| --- | --- | --- | --- |
| Peut-on lire les accords d'un extrait Deezer ? | Essentia sur 10 extraits de 30 s aux accords connus, comparaison sans tenir compte de la tonalité | 77 % du temps sur les bons accords ; 7 suites complètes sur 10 (Let It Be 98 %, Despacito 94 %) ; échec sur Hit the Road Jack (36 %) | Bon pour les suites majeures et mineures simples ; l'outil ne voit ni les septièmes ni les accords sus |
| Peut-on repérer une basse qui descend dans l'audio ? | Graves isolés, note de basse suivie temps par temps, sur 5 extraits | Hit the Road Jack : 10 lignes descendantes (la basse sol#, fa#, mi, ré# sort exactement) ; Let It Be : 3 ; Despacito et Get Lucky : 1 ; Wake Me Up : 0 | Avec un seuil à 2 lignes, 5 morceaux sur 5 bien classés ; échantillon trop petit pour conclure, à élargir |
| Combien de temps prend l'analyse ? | 10 extraits, puis les 200 du Top France et du Top Monde | 0,4 s par extrait ; 200 extraits téléchargés en 5 s et analysés en 24 s (0,12 s par extrait sur 8 cœurs) | Analyse en direct possible pendant la démo |
| Peut-on proposer des morceaux pareils ? | Les 200 extraits des deux tops | Basse descendante dans 4 morceaux du Top France (Vacra, L2B, Ninho, Manon Lisa) et 5 du Top Monde (Ella Langley, Koe Wetzel, Lainey Wilson, Post Malone, Kacey Musgraves) | Il faut un catalogue de quelques milliers de titres pour proposer assez de morceaux par motif |
| Les motifs sont-ils assez rares pour révéler un goût ? | Repérage sur les accords écrits des 679 807 morceaux de Chordonomicon | Basse qui descend 10,5 %, cadence andalouse 1,4 %, suite pop I–V–vi–IV 17,9 %, suite des années 50 14,6 %, accords enrichis 15,4 %, tonalité mineure 20,2 % ; si 4 morceaux sur 5 partagent un motif, la probabilité que ce soit le hasard est sous 1 % | Cinq morceaux suffisent pour faire ressortir un motif |
| Les artistes ont-ils une signature harmonique ? | 5 676 artistes avec au moins 20 morceaux | Part de morceaux à basse descendante : 0 % au 10e centile, 9 % en médiane, 23 % au 90e centile | Le signal de style existe ; ça ne prouve pas encore qu'il explique le goût d'un auditeur |
| Que couvre Chordonomicon ? | Le fichier complet (264 Mo) | 679 807 morceaux, 91 556 artistes ; surtout pop, rock et country ; musique française 2 % ; rap français 557 morceaux ; basse notée dans 17 % des morceaux seulement | Dépendre de ce jeu de données ferait échouer la démo sur la musique française |
| La basse écrite suffit-elle ? | Taux de basse descendante selon la notation | 30,2 % quand la basse est notée (Am/G), 6,5 % sinon ; le même Let It Be est repéré écrit C G/B Am, raté écrit C G Am | Sur les accords écrits sans basse, on rate la plupart des basses qui descendent : il faut l'audio |
| Peut-on relier Chordonomicon à Deezer ? | 40 morceaux tirés au hasard | 38 sur 40 retrouvés sur Deezer avec leur extrait, sans aucun compte : titre et artiste par l'aperçu public de Spotify (oEmbed), puis recherche simple Deezer. La recherche avancée de Deezer (`artist:"…" track:"…"`) renvoie zéro résultat | Le jeu de données peut alimenter un catalogue de recommandation |
| Les morceaux des tops actuels y sont-ils ? | Top France et Top Monde : artistes retrouvés via Wikidata, dates de sortie lues sur Deezer | Artiste présent pour 49 morceaux sur 100 du Top France (Jul, SDM, Ninho, PLK, Aya Nakamura…) et 77 sur 100 du Top Monde. Mais seuls 9 morceaux du Top France et 22 du Top Monde sont sortis avant la publication du jeu de données (29 octobre 2024) ; date de sortie médiane : 24 août 2026 et 24 octobre 2025 | Au mieux 9 % des tubes français actuels ont leurs accords dans le jeu de données : l'audio est indispensable |
| L'API Spotify est-elle utilisable ? | [Guide officiel de février 2026](https://developer.spotify.com/documentation/web-api/tutorials/february-2026-migration-guide) | Compte Premium obligatoire pour le propriétaire de l'app, un appel par morceau, code ISRC revenu en mars 2026 | À éviter : l'aperçu public suffit |
| Que donne l'API Deezer sans clé ? | Appels réels | Playlists publiques avec codes ISRC, recherche, recherche par ISRC, extraits de 30 s ; pas d'historique d'écoute | Entrée de la démo : une playlist publique ou cinq morceaux cherchés |
| La voix Gradium convient-elle ? | [Documentation](https://docs.gradium.ai/guides/text-to-speech-rest.md) | Synthèse en un appel HTTP avec une clé, ou en streaming (premier son sous 300 ms) ; cinq langues dont le français | Clé et quotas à obtenir sur place |
| La licence des données ? | Fiche Hugging Face | Chordonomicon : CC BY-NC 4.0 | Convient à un prototype de hackathon, pas à un produit commercialisé tel quel |

## Les risques, classés

| Risque | Gravité | Parade | Statut |
| --- | --- | --- | --- |
| Le goût d'un juré n'est pas harmonique (rythme, voix, son) : rien ne ressort de ses cinq morceaux | Élevée, c'est la démo | L'app le dit franchement ; elle cherche plusieurs motifs (basse, cadences, suites, mode) ; on la teste avant sur une dizaine de personnes | À tester |
| La basse détectée est fausse | Élevée | Valider sur une cinquantaine de morceaux annotés à l'oreille par l'équipe, régler le seuil, montrer la basse à l'écran pour que l'auditeur l'entende | À faire avant le 28 |
| L'extrait de 30 s ne contient pas le motif | Moyenne | Parler de « cet extrait » ; analyser plusieurs morceaux par personne | Accepté |
| Les accords enrichis (septièmes, sus) échappent à l'audio | Moyenne | S'en tenir à la basse, aux suites majeures et mineures et au mode ; Chordonomicon pour les couleurs quand le morceau y est | Contourné |
| Chordonomicon couvre mal le français et note rarement la basse | Moyenne | L'audio d'abord ; le jeu de données en complément | Contourné |
| Pas d'historique d'écoute | Moyenne | Playlist publique ou cinq morceaux cités | Contourné |
| Quota de l'API Deezer : au-delà d'une dizaine de requêtes par seconde, elle renvoie des erreurs (constaté) | Moyenne | Ralentir et contrôler chaque réponse ; les extraits audio, servis à part, ne sont pas concernés (200 téléchargés en 5 s) | Contourné |
| Clé ou quotas Gradium insuffisants pendant l'événement | Moyenne | Phrases préparées à l'avance, voix de secours | À demander aux organisateurs |
| Le code préparé avant l'événement est interdit | Élevée si oui | Demander aux organisateurs ; le cœur tient en quelques centaines de lignes, refaisable sur place | À demander |
| Explication fausse ou jargonneuse | Moyenne | Phrases simples (« la basse descend »), vérifiées sur les morceaux de la démo | À écrire |
| Licences (Chordonomicon non commercial, extraits Deezer) | Faible pour un hackathon | Citer les sources ; pas d'usage commercial | Accepté |

## Le chemin technique le plus court

1. Entrée : cinq morceaux cherchés sur Deezer, ou une playlist publique.
2. Analyse de chaque extrait : basse suivie temps par temps (librosa), accords majeurs et mineurs et tonalité (Essentia), 0,4 s par extrait.
3. Profil : les motifs nettement plus fréquents dans les morceaux de la personne que dans le catalogue.
4. Catalogue : quelques milliers d'extraits Deezer (playlists éditoriales, radios d'artistes proches) analysés à l'avance ou à la volée, complétés par Chordonomicon pour les morceaux plus anciens.
5. Restitution : une phrase simple dite par la voix Gradium, la basse dessinée à l'écran pendant l'extrait, puis trois morceaux qui partagent le motif.

## Ce qu'il reste à valider avant le 28 novembre

- [ ] Le test d'Aurian : 5 à 10 morceaux qu'il aime « parce que ça descend » et 5 autres. L'app retrouve-t-elle son motif ?
- [x] L'écoute des 9 morceaux signalés dans les tops : ont-ils vraiment une basse qui descend ?

    Écoutés par Aurian le 26 novembre 2026 : 5 sur 5 confirmés. La basse descend nettement sur « Fille à Papa » (Vacra), « LES DIAMANTS DE BOKASSA » (Ninho) et « Weekend In Texas » (Kacey Musgraves). Sur « Dedans » (L2B) et « Phone, Keys, Wallet » (Lainey Wilson), elle monte par moments puis descend sur le motif de fin : une descente libre, pas mécanique, et c'est ce qu'on cherche. Pas encore écoutés : « Le Petit Pêcheur », « Loving Life Again », « Jaded », « I Had Some Help ».
- [ ] Une cinquantaine de morceaux annotés à l'oreille pour mesurer les erreurs de la détection de basse.
- [ ] Demander aux organisateurs si le code préparé est autorisé, et comment obtenir la clé Gradium.

Les scripts de mesure sont restés hors du dépôt, en attendant de savoir si le code préparé avant l'événement est autorisé.

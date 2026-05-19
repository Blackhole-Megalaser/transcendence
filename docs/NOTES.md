# Reunion 1
## Roles:
tlair: product owner
lvan-bre: project manager, savoir ce que tout le monde fait
cczerwin: dev, docs, communication "je veux que ce soit fait"
kcolin: tech lead
melaemp: dev + aide communication

tous en dev

*do not forget to document your work*, be it code comments or other documentation

## Choix du jeu

Idée melemp: scribl.io 2.0 "rapidement"
pas hyper compliqué
valide beaucoup de choses
desiner en ligne, essayer de deviner la chose qui est dessiné, on gagne des points si on trouve

Jeu 2: r/place projet plus investi

## Choix des modules

https://docs.google.com/spreadsheets/d/1-unfSmSeZFW78XxymSvcDQVJqaTeYh-l-Ek2GIyEvls/edit

## Organisation

Pour la semaine prochaine:
tous: se familiariser avec les frameworks, prototypes
mettre en place un repository (github) + projet minimal avec tous les framework fonctionels

kco: (si possible) autoformat and linting setup
https://docs.astral.sh/ruff/

naming des branche: pseud-nomfeature

Essayer d'avoir une réunion par semaine + planning par semaine

Deadline "pace 18": 31 mai (5 semaines)

## Choix de technologie

Back: Django
Front: Tailwind, Vue, Vite

# Reunion 2

Pendant cette reunion, le theme general du site a ete decide, reste a avoir une idee plus generale du site et de son arborescence

Les objectifs pour la semaine suivante:
- ~~Voir pour ajouter des couleurs customs sur tailwind~~
- Avoir la structure les donnees pour la BDD
- Avoir un debut de jeu
- Voir comment connecter front <--> back

## Resume de la reunion 2

- decider sur un design
- objectifs semaine pro
  - tailwind couleurs custom
  - info des choses a stocker dans la BDD
  - commencer a faire un debut de jeu
  - essayer d'avoir une esquise du site
  - plus de familiariser
  - savoir comment connecter le back et front
- retro sur cette semaine
  - une semaine ce n'est pas suffisant pour vraiment voir un groupe de nouveau languages
  - peut-etre echanger entre nous pour essayer de metter en commun les choses que l'on a apris
    - lvan-bre: js/css/html/tailwind
    - le web: un language a copier-coller
    - tailwind: pas d'interaction avec le css, seulement le html. c'est pas mal. facilement responsive
    - django: beaucoup de copier-coller et de tutoriel
    - tlair: vue pas trop regardé, surtout regardé le js

# Reunion 3

Pour la semaine prochaine, l'objectif c'est d'avoir un squelette de site fonctionnel (pour la navigation au moins) et d'avoir de la connexion entre front <--> back que ce soit pour utiliser les données ou afficher des éléments dynamiques dans les pages.

--> On garde le SSR et on ne touche pas au SPA même avec un baton
--> On push nos avancées sur Vue dans des components séparés sur le main pour avoir une vision globale sur ce qui est fait même si actuellement non fonctionnel
(on remplacera plus tard les boutons et autres éléments pour uniformiser les styles sur tout le site)

Si possible ajouter les ressources intéressantes dans des fichiers *.md dans le dossier docs avec éventuellement quelques explications rapides.

Au niveau des features intéressantes:

--> Tri des mots par thématiques et par difficulté pour le scribl
--> Ajouter quelques espaces avec des fausses pubs

## Resume de la reunion 3

Nous avons pris la decision de drop le SSR et le module associe en faveur du MPA (Multi Page Application) pour conserver toutes les pages cote frontend pour en simplifier la gestion.

Globalement toutes les parties avancent bien, le prochain enjeux est de connecter les front et le back avec les routes API qui ont ete mises en avant.


# GTA 6 Guide Radar

Outil indépendant de veille et de documentation pour préparer un guide communautaire GTA 6 sur PS5 et Xbox Series X|S.

> Projet non affilié à Rockstar Games. Les contenus ne sont publiés comme confirmés qu'après vérification et avec leurs sources.

## Versions du produit
- Interface web/PWA existante : dossier app/ à la racine.
- Backend prototype Python/SQLite : package gta6radar/.
- Nouvelle application mobile Android/iOS : dossier mobile/.
- Architecture et plan de transformation : docs/PLAN-MOBILE.md.

## Application mobile
Depuis le dossier mobile :

    npm install
    npx expo install --fix
    npx expo install --check
    npm run typecheck
    npx expo start

La structure mobile est un premier squelette. La carte native, les comptes, la synchronisation, les achats et les données hors connexion restent à développer.

## API prototype
Depuis la racine :

    python -m gta6radar.server

Routes actuellement disponibles :
- GET /api/health
- GET /api/markers
- GET /api/entries
- POST /api/markers (jeton administrateur)

Le serveur et sa base SQLite actuels ne constituent pas encore une infrastructure de production. Ne pas y enregistrer de données utilisateurs importantes avant migration vers une base persistante.

## Règles éditoriales
- Aucun emplacement n'est inventé.
- Les statuts de vérification restent visibles.
- Les sources et licences sont conservées.
- Les données de fuite ou obtenues illicitement sont exclues.
- Les images, cartes et données communautaires ne sont réutilisées qu'après vérification des droits.

## Documentation
- docs/STRATEGIE-PRODUIT.md
- docs/CARTE-LEONIDA.md
- docs/ARCHITECTURE-TECHNIQUE.md
- docs/INTERFACE-MVP.md
- docs/PLAN-MOBILE.md

## Séparation des projets
Ce dépôt est indépendant de JML Immobilier et de son infrastructure. Aucun serveur ni fichier JML ne doit être utilisé par ce projet.

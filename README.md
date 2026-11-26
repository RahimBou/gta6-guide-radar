# GTA 6 Guide Radar

Outil indépendant de veille et de documentation pour préparer un guide communautaire GTA 6 sur PS5 et Xbox Series X|S.

> Projet non affilié à Rockstar Games. Les contenus ne sont publiés comme confirmés qu'après vérification et avec leurs sources.

## Interface web / PWA
La première interface se trouve dans `app/` : tableau de bord, carte, catégories, favoris et progression.

## Lancement avec l'API SQLite
Depuis la racine du dépôt :
```bash
python -m gta6radar.server
```
Puis ouvrir http://127.0.0.1:8080.

API :
- `GET /api/health` — état du serveur.
- `GET /api/markers` — marqueurs cartographiques publics.
- `GET /api/entries` — fiches publiques.
- `POST /api/markers` — ajout/mise à jour protégé par un jeton administrateur.

Pour autoriser l'écriture, définir `GTA6_ADMIN_TOKEN` dans l'environnement du serveur. Ne jamais placer ce secret dans le code frontend. Pour exposer le serveur dans un environnement d'hébergement, configurer `GTA6_HOST=0.0.0.0`, le port fourni par l'hébergeur et un reverse proxy HTTPS.

## Import de la carte officielle
1. Ouvrir la page média officielle : https://www.rockstargames.com/VI/media.
2. Télécharger « Leonida Map - Printable » dans le bloc « Leonida Map & Cover Art Poster ».
3. Extraire le JPG du ZIP.
4. Ouvrir le module Carte et importer le JPG.

Dans cette première version, l'image est stockée dans IndexedDB sur le navigateur utilisé. Elle n'est pas téléversée au serveur. Les autres visiteurs devront importer leur propre copie. Avant d'héberger ou redistribuer l'image, vérifier les conditions d'utilisation et les droits applicables.

## Marqueurs et données
- Le fichier `app/data/markers.json` est volontairement vide.
- Aucun emplacement n'est inventé ou présenté comme vérifié.
- Les marqueurs utilisent des coordonnées normalisées x/y de 0 à 100 et une référence de grille facultative.
- Les statuts sont `unverified`, `to_check`, `corroborated`, `verified_in_game`, `official` et `false`.
- Les sources, dates de vérification et plateformes doivent être conservées.

## Collecteur de veille
Python 3.11 ou supérieur recommandé.
```bash
python -m venv .venv
# Windows : .venv\\Scripts\\activate
# macOS/Linux :
source .venv/bin/activate
pip install -r requirements.txt
python -m gta6radar init
python -m gta6radar add-source --name "Flux de test" --url "https://example.com/feed.xml" --kind rss
python -m gta6radar collect
python -m gta6radar list
```

Le collecteur RSS ne garantit pas que TikTok expose ses vidéos dans des flux publics. Les liens peuvent être ajoutés manuellement avec `add-item`. Aucun contournement de connexion, CAPTCHA ou mécanisme anti-robot n'est prévu.

## Documentation
- `docs/STRATEGIE-PRODUIT.md` — stratégie et modèle commercial.
- `docs/CARTE-LEONIDA.md` — carte, licences et coordonnées.
- `docs/ARCHITECTURE-TECHNIQUE.md` — architecture cible.
- `docs/INTERFACE-MVP.md` — fonctions de l'interface actuelle.

## Structure
```
app/                  # interface responsive et PWA
docs/                 # stratégie et architecture
gta6radar/            # collecteur, SQLite et API
data/                 # base SQLite locale ignorée par Git
```
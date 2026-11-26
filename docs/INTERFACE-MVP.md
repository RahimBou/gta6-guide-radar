# Interface MVP — version 0.1

## Fichiers
- `app/index.html` : structure des écrans.
- `app/styles.css` : identité visuelle responsive.
- `app/app.js` : navigation et interactions locales.
- `app/manifest.webmanifest` : installation PWA.
- `app/sw.js` : cache de l'interface.

## Écrans réalisés
- Tableau de bord.
- Carte interactive de démonstration.
- Découvertes.
- Véhicules.
- Missions et activités.
- Secrets et collections.
- Favoris.
- Progression.

## Interactions
- Navigation entre les écrans.
- Recherche globale (point d'entrée provisoire).
- Filtres et commandes de zoom de la maquette cartographique.
- Stockage local des compteurs de favoris et progression prévu dans le socle JS.
- Installation PWA et cache des ressources de l'interface.

## Limites explicites
- La carte visible est un schéma décoratif, pas la carte géographique officielle de Leonida.
- Aucun marqueur géographique réel n'est inclus dans cette version.
- Les listes de contenu sont vides : les fiches seront alimentées par la base validée.
- Les comptes, synchronisation multi-appareils, paiement, abonnement et génération PDF ne sont pas encore connectés.
- Les polices externes nécessitent une connexion ; le reste de l'interface reste fonctionnel sans elles.

## Lancement local
Servir le dossier `app` via un serveur HTTP statique, par exemple :
```bash
python -m http.server 8080 --directory app
```
Puis ouvrir `http://localhost:8080`.

## Incrément carte et API
- Import local du fond cartographique dans le navigateur (JPG/PNG/WebP, 60 Mo maximum).
- Stockage local dans IndexedDB ; l'image n'est pas téléversée sur le serveur.
- Chargement des marqueurs depuis GET /api/markers, avec repli vers app/data/markers.json.
- Filtres fonctionnels par catégorie et statut.
- Marqueurs interactifs avec détail, source, favori et statut trouvé.
- Panoramique tactile/souris et zoom.
- Favoris et progression stockés dans le navigateur.
- API serveur en lecture publique ; écriture des marqueurs protégée par GTA6_ADMIN_TOKEN.

## Lancement avec API
Depuis la racine du dépôt :
```bash
python -m gta6radar.server
```
Ouvrir http://127.0.0.1:8080.

La carte réelle et ses marqueurs ne sont pas encore fournis. Le fichier cartographique doit être importé dans chaque navigateur pour le prototype local, et les marqueurs doivent être ajoutés avec leurs sources et coordonnées contrôlées.
## Back-office des marqueurs
- Page `app/admin.html`, script `app/admin.js`.
- Import ou réutilisation du fond de carte local IndexedDB.
- Clic sur la carte pour calculer x/y normalisés.
- Saisie du nom, catégorie, statut, plateforme, région, référence de grille et source.
- Enregistrement par POST /api/markers avec jeton administrateur.
- Liste des marqueurs existants.
- Le jeton est conservé en sessionStorage pour l'onglet courant uniquement.
- Le back-office doit être servi derrière HTTPS dès qu'il est exposé hors de la machine locale.
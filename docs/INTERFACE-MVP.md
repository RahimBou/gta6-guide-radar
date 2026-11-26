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

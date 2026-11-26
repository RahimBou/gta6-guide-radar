# Carte interactive de Leonida

## Décision
La carte est un module central du site et de la PWA. Le système de marqueurs et de progression appartient à GTA 6 Guide Radar ; les fonds cartographiques et jeux de données externes gardent leurs licences et attributions propres.

## Sources à étudier
- Carte officielle imprimable Rockstar : https://www.rockstargames.com/VI/media
- Téléchargement direct annoncé du ZIP officiel : https://media-rockstargames-com.akamaized.net/VI/downloads/artwork_wallpapers/Leonida_Map_Poster_Printable.zip
- Carte communautaire et données de lieux GTADB : https://map.gtadb.org/
- Licence annoncée pour les tuiles et données communautaires GTADB : CC BY 4.0 ; vérifier le fichier de licence et les obligations d'attribution à chaque import.
- Exemple de carte communautaire interactive : https://www.gta6everything.com/map

## Distinction impérative des sources
1. **Carte officielle Rockstar** : poster de référence et toponymes visibles ; ce n'est pas une base de marqueurs de collectibles.
2. **Données communautaires** : lieux et coordonnées proposés par des contributeurs ; conserver l'attribution et la licence, et ne pas les présenter comme des données officielles.
3. **Vérifié en jeu** : position contrôlée directement dans le jeu avec une preuve et une date.
4. **Hypothèse / rumeur** : jamais affichée comme confirmée.

## Fonctions cartographiques
- Zoom et déplacement tactiles.
- Recherche par nom, région et catégorie.
- Filtres activables par couche.
- Fiche détaillée de chaque marqueur.
- Favoris, marqueurs personnels et progression.
- Compteur de complétion par catégorie et région.
- Partage d'un lien vers une vue ou un marqueur.
- Import/export des marqueurs personnels.
- Mode mobile plein écran.
- Cache des données et des zones sauvegardées lorsque la licence et la technique le permettent.

## Catégories initiales
Régions et quartiers, points d'intérêt, commerces, garages, véhicules, armes, missions, activités, collectibles, animaux, secrets, services et lieux communautaires.

## Modèle de données d'un marqueur
- id stable ;
- nom ;
- catégorie et sous-catégorie ;
- région ;
- coordonnées normalisées x/y relatives au fond de carte ;
- description et procédure ;
- plateforme ;
- statut de fiabilité ;
- sources et preuves ;
- date de collecte et date de vérification ;
- contributeur ;
- licence et attribution de la donnée source, si applicable.

## Règles d'intégration
- Ne pas copier les tuiles ou données d'un site tiers sans vérifier sa licence et ses conditions de réutilisation.
- Pour les données CC BY 4.0, afficher l'attribution, un lien vers la licence et les modifications apportées.
- Ne pas intégrer de contenu issu de fuites ou de données obtenues illicitement.
- Garder les marqueurs internes indépendants du fond de carte afin de pouvoir changer de fournisseur.
- Ne pas inventer des coordonnées : tout marqueur doit porter une source et un niveau de confiance.
- Les ressources Rockstar restent la propriété de leurs ayants droit ; leur usage doit respecter les conditions applicables.

## Première version cartographique (MVP)
1. Afficher un fond de carte dont l'usage est autorisé.
2. Charger les marqueurs depuis l'API/base de données.
3. Ajouter recherche et filtres.
4. Ouvrir une fiche depuis un marqueur.
5. Enregistrer favoris et progression.
6. Afficher le statut et les sources sur chaque fiche.

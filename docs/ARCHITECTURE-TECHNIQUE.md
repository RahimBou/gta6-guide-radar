# Architecture technique — GTA 6 Guide Radar

## Principes
- Une base métier unique pour le site, la PWA et les PDF.
- API centrale versionnée.
- Contenus sourcés et traçables.
- Collecte séparée de la validation éditoriale.
- Aucun accès à l'infrastructure JML Immobilier.
- Aucun contournement de mécanismes de protection des plateformes.

## Architecture cible

```
Sources publiques
  ├─ Flux RSS / Atom
  ├─ Liens TikTok / YouTube soumis ou accessibles publiquement
  ├─ Sites et forums autorisés
  └─ Contributions des joueurs
          |
          v
Collecteur -> File d'import -> Déduplication -> Base de veille
                                      |
                                      v
                              Console de vérification
                                      |
                            Validation éditoriale
                                      |
                    Base de connaissances structurée
                         /          |          \
                        v           v           v
                    API web     Générateur PDF   Exports
                        |
             Site responsive / PWA
                        |
             Application native ultérieure
```

## Stack proposée pour le MVP
- Frontend : HTML/CSS/TypeScript ou React selon le périmètre validé.
- PWA : Web App Manifest et Service Worker.
- Carte : moteur cartographique compatible avec une image raster et coordonnées relatives ; Leaflet peut être évalué pour le MVP.
- Backend : Python FastAPI ou Node.js ; choisir une seule pile avant le développement API.
- Base de données : PostgreSQL pour les données partagées ; SQLite reste adaptée au prototype local du collecteur.
- Recherche : PostgreSQL full-text au départ ; moteur dédié seulement si le volume le justifie.
- PDF : génération serveur à partir des fiches validées.
- Authentification : sessions sécurisées, mots de passe hachés, limitation des tentatives.
- Paiement : prestataire externe à sélectionner ; ne jamais stocker les numéros de carte.

## Entités principales
- users
- plans / subscriptions
- sources
- source_items
- evidence
- guide_entries
- categories
- platforms
- map_regions
- map_markers
- user_favorites
- user_progress
- pdf_editions
- reports / moderation_events

## Statuts de validation
- unverified : non vérifié ;
- to_check : contrôle nécessaire ;
- corroborated : plusieurs sources concordantes ;
- verified_in_game : testé dans le jeu ;
- official : publié par Rockstar ;
- false : réfuté.

Les statuts official et verified_in_game décrivent deux types de preuve différents et ne doivent pas être confondus.

## Sécurité et conformité
- Respect des licences des cartes, images et bases communautaires.
- Liens et citations vers les créateurs originaux.
- Pas de republication intégrale de vidéos ou d'images sans autorisation.
- Journalisation des modifications éditoriales.
- Sauvegardes et contrôle d'accès.
- Collecte limitée aux données publiques nécessaires.
- Mentions légales et politique de confidentialité avant ouverture publique.

## Phasage
1. Stabiliser le schéma de données et la console éditoriale.
2. Construire le site responsive et la PWA.
3. Intégrer la carte et les marqueurs sourcés.
4. Ajouter comptes, favoris et progression.
5. Générer le PDF premium.
6. Ajouter paiement et espace premium.
7. Évaluer une application native selon les usages.

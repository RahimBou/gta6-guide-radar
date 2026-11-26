# Plan de transformation mobile — GTA 6 Guide Radar

## Décisions produit
- Distribution payante à l'achat, sans abonnement obligatoire dans la première version.
- Cibles : Android téléphone/tablette et iOS iPhone/iPad.
- Un seul code mobile partagé.
- Produit indépendant de JML Immobilier et de toute son infrastructure.
- Les contenus restent sourcés et leur statut de vérification visible.

## Audit du socle existant
Le dépôt contient une interface HTML/CSS/JavaScript responsive/PWA dans app/, un serveur HTTP Python standard dans gta6radar/server.py, une base SQLite locale dans gta6radar/db.py et les tables sources, items, guide_entries et map_markers. La console cartographique utilise un jeton partagé. Favoris, progression et image de carte sont stockés localement dans le navigateur.

Limites constatées :
- aucune authentification utilisateur ;
- aucune synchronisation multi-appareils ;
- pas de modèle de commande ou de droit d'achat ;
- pas de base de production partagée ;
- le fond de carte est importé localement par chaque navigateur ;
- le contenu et les marqueurs sont encore vides ;
- l'API ne couvre que health, lecture de marqueurs/fiches et écriture de marqueurs ;
- le jeton partagé ne constitue pas un système complet de rôles et d'audit.

## Architecture cible
Android et iOS (React Native + Expo + TypeScript)
  -> HTTPS / API versionnée
  -> Backend Python FastAPI
  -> PostgreSQL + stockage objet
Le back-office web reste séparé de l'application publique et utilise les mêmes API avec des rôles d'administration.

## Stack retenue
- Mobile : Expo SDK 58, React Native 0.88, React 19.3, TypeScript, Expo Router.
- API : Python + FastAPI (à créer ; le serveur HTTP standard actuel reste le prototype jusqu'à migration).
- Données : PostgreSQL en production.
- Cache mobile : SQLite local ; synchronisation via une API idempotente.
- Fichiers : stockage objet compatible S3, après vérification des droits sur chaque média.
- Builds : EAS Build ; soumission via EAS Submit après validation des comptes développeur.
- Dépendances natives : utiliser npx expo install et contrôler avec npx expo install --check.

## Modèle de données cible
- users : identité, paramètres et état du compte.
- store_entitlements : preuve d'achat store et droit d'accès.
- sources : éditeur, URL, type, licence et état.
- source_items : éléments collectés et dédoublonnés.
- evidence : preuves liées aux fiches.
- guide_entries : fiches publiables et versions.
- map_markers : positions et lien vers les fiches.
- favorites : favoris par utilisateur.
- user_progress : état trouvé/à faire par utilisateur.
- sync_events : journal des opérations synchronisées.
- editorial_events : historique de modération et de validation.

Chaque fiche publiée conserve : statut de vérification, plateforme, sources, date de vérification, auteur/contributeur si connu et droits/licence associés.

## Achat unique et accès
- L'application est payante au téléchargement.
- Le backend ne doit pas supposer qu'une installation implique automatiquement un achat : il doit vérifier/restaurer le droit d'accès associé au compte/store.
- Aucun abonnement n'est requis dans la V1.
- Toute vente ultérieure de contenu numérique ou de fonctionnalités dans l'application devra être étudiée au regard des règles de facturation Apple et Google en vigueur.
- Les achats doivent être restaurables et testés avec les mécanismes officiels des stores.

## Exigences mobiles
- Navigation adaptée aux petits écrans et aux tablettes.
- Sur tablette : carte et fiche en vue à deux panneaux ; navigation latérale ou adaptée à la largeur.
- Mode hors connexion pour les fiches et données explicitement enregistrées.
- Synchronisation tolérante aux coupures réseau et aux conflits.
- États de chargement, erreurs, absence de données et accessibilité.
- Pas de contenu fictif : aucune coordonnée ou astuce inventée.

## Phases et critères de sortie

### Phase 0 — audit et préparation
Vérifier dépôt, dépendances, secrets, routes et déploiement. Geler les contrats de données et statuts éditoriaux. Écrire les migrations et la stratégie de sauvegarde.
Sortie : audit documenté, aucun secret versionné, schéma validé.

### Phase 1 — socle mobile
Initialiser Expo Router et TypeScript. Créer navigation, thème et gabarits responsive téléphone/tablette. Créer les écrans accueil, carte, recherche, favoris, progression et paramètres.
Sortie : application démarre sur Android et iOS ; tests de navigation réussis.

### Phase 2 — API et données
Créer FastAPI et PostgreSQL. Migrer les tables et routes avec tests. Ajouter authentification, rôles, pagination, validation et journalisation.
Sortie : API documentée, tests d'intégration et migrations reproductibles.

### Phase 3 — expérience de jeu
Brancher fiches et carte. Ajouter recherche et filtres, favoris, progression et synchronisation. Ajouter cache local et mode hors connexion.
Sortie : scénario complet testé sur téléphone et tablette, en ligne et hors ligne.

### Phase 4 — achat et conformité
Configurer les produits payants des stores. Vérifier achat, restauration et droits d'accès. Préparer confidentialité, support, mentions légales et déclarations de données. Vérifier les licences de la carte, des médias et des données tierces.
Sortie : parcours d'achat/restauration testé en sandbox.

### Phase 5 — bêta et publication
Tester sur appareils réels et tailles d'écran. Effectuer tests de sécurité, sauvegarde, performances et accessibilité. Préparer captures, descriptions, classification d'âge et notes de revue.
Sortie : soumissions complètes ; publication après approbation des boutiques.

## Risques et décisions à ne pas prendre trop tôt
1. Carte officielle Rockstar : sa mise à disposition en téléchargement ne prouve pas un droit de redistribution dans une application payante. Obtenir une autorisation ou choisir un fond dont la licence autorise cet usage.
2. Données communautaires : vérifier licence, attribution et droit d'utilisation commerciale avant import.
3. Contenu GTA : utiliser une identité visuelle originale et éviter toute présentation laissant croire à une affiliation Rockstar.
4. Achat unique : les règles des stores et la restauration doivent être implémentées avant commercialisation.
5. Hébergement : le stockage SQLite actuel sur système de fichiers éphémère ne convient pas à la production.

## Hors périmètre
- Pas de migration ni suppression de données existantes.
- Pas de modification de JML Immobilier.
- Pas d'ajout de services payants sans validation.
- Pas de marqueurs ou contenus inventés.
- Pas de publication store avant tests et conformité.

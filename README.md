# GTA 6 Guide Radar — Video Intelligence

Application indépendante consacrée à GTA VI sur PS5 et Xbox Series X|S.

## Nouveau produit
Le produit est reconstruit autour d'un robot analyste de vidéos de gameplay :
- collecte des sources accessibles (YouTube, TikTok, Twitch, RSS et import manuel) ;
- contrôle des droits et des conditions d'accès ;
- transcription horodatée ;
- extraction de captures sur médias autorisés ;
- analyse visuelle des scènes ;
- rédaction de fiches d'astuces et de missions avec preuves ;
- validation avant publication dans l'application.

## Lancer le serveur
```bash
python -m gta6radar.server
```
Le serveur utilise le port fourni par Render (`PORT`) ou `GTA6_PORT` en local.

## API actuelle
- `GET /api/health`
- `GET /api/robot/overview`
- `GET /api/robot/videos`
- `GET /api/robot/tips`
- `POST /api/robot/videos` : enregistre une URL YouTube/TikTok/Twitch et crée une tâche de contrôle des droits.
- `POST /api/robot/discover` : lance la découverte YouTube/Twitch via API officielles (jeton administrateur requis).
- `POST /api/robot/tips/review` : validation éditoriale avec jeton administrateur.

## État réel
La console web et l'enregistrement des URL sont implémentés. Les connecteurs automatiques, la transcription ASR, l'extraction d'images et l'analyse IA ne sont pas encore actifs : ils nécessitent les identifiants de plateforme, des droits d'accès au média et un fournisseur d'analyse configuré. Une URL seule n'autorise pas le téléchargement d'une vidéo.

## Configuration
Définir `GTA6_ADMIN_TOKEN` dans les variables d'environnement pour les actions d'administration. Ne jamais enregistrer de secret dans Git.

Connecteurs à configurer ensuite :
- YouTube Data API : `YOUTUBE_API_KEY`
- Twitch Helix : `TWITCH_CLIENT_ID`, `TWITCH_CLIENT_SECRET`
- TikTok Display : `TIKTOK_CLIENT_KEY`, `TIKTOK_CLIENT_SECRET` et autorisation OAuth des créateurs
- ASR et vision : fournisseur et clés séparés
- Stockage objet privé pour les fichiers autorisés

## Plateformes et droits
Aucun contournement de DRM, CAPTCHA, connexion ou restriction d'accès. Les captures, transcriptions et fiches conservent leur source et leur statut de preuve. Les contenus non confirmés ne sont jamais présentés comme confirmés en jeu.

## Déploiement
Le dépôt est relié au service Render existant. Render Free utilise un système de fichiers éphémère : les données SQLite ne sont pas garanties après redémarrage. Ne pas utiliser en production réelle avant configuration d'un stockage persistant ou migration PostgreSQL.

Projet indépendant, non affilié à Rockstar Games.

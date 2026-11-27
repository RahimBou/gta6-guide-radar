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
- `POST /api/robot/discover` : lance la découverte RSS, YouTube et Twitch (jeton administrateur requis). Un appel GET renvoie désormais 405 sans déclencher de collecte.
- `POST /api/robot/videos/transcript` : enregistre une transcription obtenue légalement, avec déclaration du statut de droits (jeton administrateur requis).\n- `POST /api/robot/process` : transforme une transcription autorisée en fiches candidates avec extraits de preuve (jeton administrateur requis).\n- `POST /api/robot/tips/review` : validation éditoriale avec jeton administrateur.

## État réel
La console web, la découverte de métadonnées RSS/YouTube/Twitch, l'enregistrement des URL et un premier moteur local d'extraction de fiches depuis une transcription sont implémentés. Le moteur local extrait des phrases candidates et les place en attente de validation. La transcription ASR automatique, l'extraction d'images et l'analyse visuelle IA ne sont pas encore actives ; elles nécessitent un fournisseur et des accès configurés. Une URL seule n'autorise pas le téléchargement d'une vidéo.

## Configuration
Définir `GTA6_ADMIN_TOKEN` dans les variables d'environnement pour les actions d'administration. Définir `GTA6_DATA_DIR` ou `GTA6_DB_PATH` uniquement après avoir configuré un stockage persistant. Ne jamais enregistrer de secret dans Git.

Connecteurs à configurer ensuite :
- YouTube Data API : `YOUTUBE_API_KEY`
- Twitch Helix : `TWITCH_CLIENT_ID`, `TWITCH_CLIENT_SECRET`
- TikTok Display : `TIKTOK_CLIENT_KEY`, `TIKTOK_CLIENT_SECRET` et autorisation OAuth des créateurs
- ASR et vision OpenAI : `OPENAI_API_KEY` (secret Render), `GTA6_ASR_MODEL` et `GTA6_VISION_MODEL` facultatifs\n- Médias autorisés : placer les fichiers audio et images dans `GTA6_MEDIA_DIR` (par défaut `/var/data/gta6-media`), puis appeler `POST /api/robot/analyse-media` avec `video_id`, `audio_path` et `frame_paths`\n- Le endpoint analyse uniquement des fichiers locaux sous `GTA6_MEDIA_DIR` ; aucun téléchargement d'URL arbitraire n'est effectué
- Stockage objet privé pour les fichiers autorisés

## Plateformes et droits
Aucun contournement de DRM, CAPTCHA, connexion ou restriction d'accès. Les captures, transcriptions et fiches conservent leur source et leur statut de preuve. Les contenus non confirmés ne sont jamais présentés comme confirmés en jeu.

## Déploiement
Le dépôt est relié au service Render existant. Render Free utilise un système de fichiers éphémère : les données SQLite ne sont pas garanties après redémarrage. Pour conserver SQLite, monter un disque persistant sur le service puis définir `GTA6_DATA_DIR` vers son point de montage (ou `GTA6_DB_PATH` vers le fichier SQLite). La simple définition de ces variables ne crée pas le disque. Sur Render Free, ne pas considérer la base comme durable. Une migration PostgreSQL reste l'option recommandée pour une exploitation multi-instance.

Projet indépendant, non affilié à Rockstar Games.

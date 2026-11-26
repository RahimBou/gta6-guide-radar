# Robot analyste GTA 6

Le robot transforme des sources vidéo publiques/autoriséess en propositions de fiches de guide vérifiables, avec preuves horodatées.

## Pipeline
discovery -> normalize -> rights_check -> transcript -> frame_sampling -> vision -> tip_extraction -> human_review -> publish

## Contrat d'accès
- Découverte de métadonnées par API officielle, RSS, embeds ou import manuel.
- Analyse du média uniquement si le fichier est fourni par l'utilisateur, appartient au projet, ou si une autorisation explicite permet cette analyse.
- Aucun contournement de protections ou de restrictions d'accès.
- Les captures et transcriptions gardent la source, le timecode et la base de droits.

## Connecteurs à configurer
- YouTube Data API : YOUTUBE_API_KEY
- Twitch Helix : TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET
- TikTok Display : TIKTOK_CLIENT_KEY, TIKTOK_CLIENT_SECRET et OAuth/consentement du créateur
- ASR : ASR_PROVIDER et identifiants du fournisseur
- Vision : VISION_PROVIDER et identifiants du fournisseur
- Stockage privé : OBJECT_STORAGE_*

TikTok Display nécessite l'autorisation OAuth du créateur pour lister ses vidéos. TikTok Research API est soumise à approbation et ne doit pas être supposée accessible à un service commercial ordinaire.

Le code initial fournit les contrats et contrôles d'accès. Les connecteurs API et modèles ASR/vision restent à brancher après configuration des identifiants et conditions d'utilisation.

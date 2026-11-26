# GTA 6 Guide Radar — application Android et iOS

Application mobile native construite avec Expo SDK 58, React Native et TypeScript.

## APK Android

Chaque modification de `mobile/**` sur `main` lance automatiquement le workflow **Build Android APK**.

1. Ouvrir l'onglet **Actions** du dépôt GitHub.
2. Ouvrir le dernier workflow **Build Android APK** terminé avec succès.
3. Dans **Artifacts**, télécharger `gta-6-guide-radar-android`.
4. Extraire le ZIP et installer `app-release.apk` sur Android.

Le workflow peut aussi être lancé manuellement depuis Actions → Build Android APK → Run workflow.

## Développement local

Node.js 22 et npm :

    npm install
    npx expo prebuild --platform android
    npm run typecheck
    npx expo start

## Modules

- Tableau de bord et état de connexion au robot.
- Carte : lecture des marqueurs présents dans l'API.
- Astuces et découvertes : lecture des fiches du robot.
- Missions, véhicules et secrets : lecture des fiches documentées par catégorie.
- Robot Radar : ajout de vidéos YouTube, TikTok et Twitch à la file de contrôle.

Les écrans n'inventent pas de lieux, de missions ou de secrets : ils affichent les données effectivement présentes dans la base du serveur.

## Serveur

API publique : `https://gta6-guide-radar.onrender.com`.

Les sources vidéo ajoutées créent une tâche de contrôle des droits. L'ajout d'une vidéo ne signifie pas que son contenu a déjà été analysé ou validé.

Projet indépendant, non affilié à Rockstar Games.

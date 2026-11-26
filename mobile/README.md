# GTA 6 Guide Radar — application mobile

Application native partagée Android/iOS, construite avec Expo SDK 58, React Native et TypeScript.

## Pré-requis
- Node.js compatible avec Expo SDK 58 (Node 22.13+ recommandé).
- npm.
- Compte Expo pour les builds cloud.
- Android Studio pour émulateur Android.
- macOS + Xcode pour les builds iOS locaux ; EAS Build peut compiler iOS dans le cloud.

## Installation
Depuis ce dossier :

    npm install
    npx expo install --fix
    npx expo install --check
    npm run typecheck
    npx expo start

## Démarrage
- Scanner le QR code avec un client Expo Go compatible, ou utiliser un development build.
- npm run android : démarrage Android.
- npm run ios : démarrage iOS.
- npm run web : aperçu web.

## État
Cette première structure est un squelette de navigation et d'interface. Les écrans de modules, la carte native, l'API, les comptes, la synchronisation, les achats et le mode hors connexion ne sont pas encore implémentés.

## Identifiants
Les identifiants natifs déclarés dans app.json sont provisoires et devront être vérifiés avant publication. Ne pas changer les identifiants après publication sans stratégie de migration.

## Sécurité
- Aucun secret API ou jeton administrateur dans l'application.
- Les URL et paramètres publics peuvent être configurés par environnement.
- Les droits d'achat doivent être vérifiés côté serveur et restaurables depuis les stores.

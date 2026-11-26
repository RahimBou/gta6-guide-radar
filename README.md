# GTA 6 Guide Radar

Outil indépendant de veille et de documentation pour préparer un guide communautaire GTA 6 (PS5 et Xbox Series X|S).

> Projet non affilié à Rockstar Games. Les contenus collectés restent des pistes tant qu'ils n'ont pas été vérifiés en jeu ou corroborés par une source fiable.

## Interface web / PWA
La première interface est dans le dossier `app/`.

Lancement local :
```bash
python -m http.server 8080 --directory app
```
Puis ouvrir `http://localhost:8080`.

Écrans : tableau de bord, carte de démonstration, découvertes, véhicules, missions, secrets, favoris et progression. La carte est actuellement un schéma non géographique : elle ne prétend pas reproduire la carte officielle du jeu.

## Documentation
- `docs/STRATEGIE-PRODUIT.md` — stratégie et modèle commercial.
- `docs/CARTE-LEONIDA.md` — sources, licences et conception cartographique.
- `docs/ARCHITECTURE-TECHNIQUE.md` — architecture cible.
- `docs/INTERFACE-MVP.md` — périmètre de l'interface actuelle.

## Collecteur de veille
Python 3.11 ou supérieur recommandé.

```bash
python -m venv .venv
# Windows : .venv\\Scripts\\activate
# macOS/Linux :
source .venv/bin/activate
pip install -r requirements.txt
python -m gta6radar init
python -m gta6radar add-source --name "Flux de test" --url "https://example.com/feed.xml" --kind rss
python -m gta6radar collect
python -m gta6radar list
```

La commande `add-source` accepte uniquement des flux RSS/Atom publics dans ce MVP. Les URL TikTok et autres liens publics peuvent être ajoutés manuellement dans la base via la commande `add-item`.

## Commandes
- `init` : initialise la base SQLite.
- `add-source --name NOM --url URL --kind rss` : ajoute un flux RSS/Atom.
- `collect` : collecte les flux configurés.
- `add-item --url URL --title TITRE --platform tiktok` : référence manuellement une publication.
- `list` : affiche les éléments enregistrés.
- `set-status --id ID --status STATUS` : met à jour le statut.

Statuts : `unverified`, `to_check`, `corroborated`, `verified`, `false`.

## Fiabilité éditoriale
Une vidéo TikTok seule ne constitue pas une preuve. Conserver systématiquement l'URL d'origine, la date de collecte, la plateforme, le thème, le résumé et le statut. Ne jamais présenter un code, emplacement, coffre, véhicule ou secret comme confirmé sans vérification indépendante.

## Périmètre et limites
- Pas de connexion à un compte TikTok.
- Pas de contournement de CAPTCHA, authentification, paywall ou mécanisme anti-robot.
- Le collecteur RSS ne garantit pas que TikTok expose ses vidéos dans des flux publics.
- Les descriptions et transcriptions accessibles devront être contrôlées avant publication.
- Respecter les droits d'auteur : citer les créateurs et utiliser ses propres textes et visuels.

## Structure
```
app/                  # interface web responsive et PWA
docs/                 # cadrage produit et architecture
gta6radar/            # collecteur et CLI Python
data/                 # base SQLite locale (ignorée par Git)
```

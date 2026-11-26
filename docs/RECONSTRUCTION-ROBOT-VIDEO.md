# Reconstruction — GTA 6 Guide Radar piloté par un robot vidéo

## Décision produit
Le produit est reconstruit autour d'une chaîne éditoriale automatisée : détecter des vidéos publiques liées à GTA VI, enregistrer leurs métadonnées, obtenir une transcription lorsqu'elle est légalement accessible, analyser les séquences visuelles autorisées, extraire des preuves horodatées, proposer des fiches, puis soumettre ces fiches à validation avant publication.

La valeur centrale est la transformation contrôlée d'une vidéo en guide structuré, illustré par des captures et traçable jusqu'à la source.

## Sources demandées
Périmètre : YouTube, TikTok, Twitch et autres sources accessibles, ainsi que les URL ajoutées manuellement.

### Connecteurs et limites
- YouTube : YouTube Data API pour rechercher et lire les métadonnées. La documentation consultée indique une limite standard de 100 appels search.list par jour. L'API ne donne pas automatiquement le droit de télécharger la vidéo ou ses sous-titres.
- TikTok : Display API pour afficher les vidéos d'un compte ayant autorisé l'accès. Research API soumise à éligibilité et approbation, non disponible comme API générale de veille commerciale.
- Twitch : Helix API pour les métadonnées des VOD par chaîne ou catégorie, avec authentification. Le traitement du fichier vidéo reste soumis aux droits et accès autorisés.
- Autres plateformes : connecteurs spécifiques uniquement si API officielle, flux RSS, embed ou accès autorisé disponible.
- Import manuel : URL publique, fichier vidéo fourni par l'utilisateur, transcription ou captures fournies par le créateur.

Aucun contournement de DRM, connexion, CAPTCHA, restriction d'accès ou limitation technique. Pas de téléchargement ou republication automatique d'une vidéo tierce sans droits.

## Chaîne de traitement
1. Discovery : recherche planifiée par mots-clés, chaînes suivies et sources autorisées.
2. Normalize/dedupe : URL canonique, plateforme, identifiant externe, titre, créateur, date, durée, langue.
3. Rights gate : source, mode d'accès, licence/autorisation, conditions d'analyse, statut de conservation.
4. Transcript : sous-titres autorisés ou transcription d'un fichier fourni/autorisé.
5. Frame sampling : extraction à intervalles et autour des segments parlés pertinents, avec FFmpeg lorsque le média peut légalement être traité.
6. Vision analysis : repérer carte, HUD, objectif, dialogue, inventaire, véhicule, lieu, étape et événement visible.
7. Tip extraction : proposition de fiche structurée avec étapes, prérequis, résultat, horodatages et preuves.
8. Quality gate : dédoublonnage, cohérence, score de confiance, détection de rumeurs, validation humaine.
9. Publish : mise à disposition dans l'app et indexation dans recherche/carte/progression.

## Contrat éditorial
Chaque affirmation exploitable conserve URL source, plateforme, créateur, titre, date, timecodes, transcription associée, captures et empreintes, statut, confiance et date de vérification.

Statuts de contenu distincts : observé dans une vidéo, corroboré par plusieurs sources, confirmé en jeu par test, officiel. Une vidéo seule ne transforme pas une astuce en fait confirmé en jeu.

## Produit public
Accueil, missions pas-à-pas, astuces gameplay, carte des lieux prouvés, véhicules, armes, équipements, commerces, secrets, collections, recherche globale, favoris, progression et fiches sources avec vidéos/timecodes/captures.

## Back-office robot
Sources et chaînes suivies ; file de vidéos détectées ; état des traitements ; lecteur de preuves ; transcription segmentée ; fiches proposées par l'IA ; validation/rejet/fusion/publication ; journal des erreurs, quotas et coûts.

## Architecture cible
- App : React Native / Expo Android, iOS, téléphones et tablettes.
- API : Python FastAPI (migration à faire depuis le serveur HTTP prototype).
- DB : PostgreSQL en production ; SQLite pour tests locaux.
- Worker : tâches asynchrones séparées de l'API, files de traitement et reprises idempotentes.
- Médias : stockage objet privé, rétention limitée et contrôle des droits.
- Analyse : transcription ASR + vision multimodale via fournisseurs configurables.
- Observabilité : état des jobs, durée, erreurs, coûts, quotas et provenance.

## Tables initiales
sources, source_accounts, source_items, processing_jobs, transcripts, transcript_segments, frame_captures, evidence, guide_entries, guide_entry_evidence, review_events, map_markers, favorites, user_progress.

## Sécurité et droits
Secrets uniquement en variables d'environnement ; authentification et rôles ; rate limits ; validation stricte des URL et protection SSRF ; contrôle MIME, taille et durée des fichiers ; conservation minimale ; pas de capture non autorisée publiée ; contenu non confirmé marqué clairement.

## Phasage
A. Socle robot : schéma, contrats, jobs, preuves, statut éditorial et interface de contrôle.
B. Connecteurs : YouTube Data API, Twitch Helix, TikTok Display avec consentement créateur, RSS/embeds et import manuel.
C. Analyse : transcription autorisée, extraction d'images depuis médias fournis/autorisé, analyse multimodale et propositions de fiches.
D. App : écrans branchés sur API, carte, missions, astuces, recherche, progression et hors connexion.
E. Bêta : qualité, droits, sécurité, quotas, coûts et stores.

## Limites actuelles
Cette première reconstruction crée les contrats et le socle du dépôt. Aucun connecteur n'est opérationnel sans identifiants/API ; aucune analyse IA n'est active sans fournisseur configuré ; aucun média n'est collecté par le simple fait d'ajouter ces fichiers.

"""Idempotent starter dataset sourced from public GTA VI guide pages.

Descriptions are paraphrased, source URLs are retained, and entries remain
unverified until corroborated in-game or by an authorized primary source.
"""
from .db import connect

SOURCES = [
    ("Promptowy — carte interactive GTA 6", "https://promptowy.com/fr/gta-6/carte-interactive/", "website"),
    ("GTA Guide — guides et fiches GTA 6", "https://gtaguide.fr/", "website"),
    ("GTA Guide — Mill Station Radar Base et Hostile Super400", "https://gtaguide.fr/articles/gta-6-hostile-super400-base-radar-mill-station-ou-trouver/", "guide"),
    ("Promptowy — mission Lab Fees", "https://promptowy.com/fr/gta-6/gta-6-soluce-lab-fees/", "guide"),
    ("Promptowy — mission Just a Scratch", "https://promptowy.com/fr/gta-6/gta-6-soluce-just-a-scratch/", "guide"),
    ("eGamersWorld — guide des régions de Leonida", "https://fr.egamersworld.com/blog/gta-6-map-guide-every-region-of-leonida-and-what-t-DBov8HSbda", "website"),
    ("IGN Wiki — GTA 6", "https://www.ign.com/wikis/gta-6/", "wiki"),
]

REGIONS = [
    ("vice-city", "Vice City", "Vice-Dale", "Métropole du sud-est de Leonida, dense et tournée vers les quartiers urbains, les plages, le port et les activités.", "Quartiers cités par les sources : Downtown, Ocean Beach, Little Cuba, Southside, Stockyard, Tequesta, Decor District, Crosstown, Heathcliff Heights, La Perle et Watson Bay. Les noms et limites sont à contrôler sur la carte en jeu.", "https://fr.egamersworld.com/blog/gta-6-map-guide-every-region-of-leonida-and-what-t-DBov8HSbda", "eGamersWorld / Promptowy"),
    ("leonida-keys", "Leonida Keys", "Mariana", "Archipel tropical du sud de Leonida, composé d'îles reliées par des ponts et des voies nautiques.", "La source Promptowy cite Key Lento, la maison de Jason, la marina de Brian Heder, le Rusty Anchor et la boutique de plongée de Kenton. Elle signale aussi des épaves et découvertes sous-marines. Détails à confirmer en jeu.", "https://promptowy.com/fr/gta-6/carte-interactive/", "Promptowy / eGamersWorld"),
    ("grassrivers", "Grassrivers", "Mariana", "Région de marécages et de zones humides inspirées des Everglades, avec faune sauvage et déplacements sur l'eau.", "Les sources citent Pelican Valley, les Kingfishers, les missions Gone Fishing et Swamped ainsi que des recherches de paquets perdus. Le guide GTA Guide situe Mill Station au nord de Watson Bay ; le point précis reste à localiser.", "https://fr.egamersworld.com/blog/gta-6-map-guide-every-region-of-leonida-and-what-t-DBov8HSbda", "eGamersWorld / GTA Guide / Promptowy"),
    ("port-gellhorn", "Port Gellhorn", "Kelly", "Région côtière du nord-ouest de Leonida, ancien secteur touristique décrit avec motels, commerces délaissés et activités motorisées.", "Repères cités : Draper Island, Emerald Springs, Buckskin Swamp, Frogswater, le circuit international de Gellhorn et le Thrillbilly Mud Club. Informations issues du guide eGamersWorld.", "https://fr.egamersworld.com/blog/gta-6-map-guide-every-region-of-leonida-and-what-t-DBov8HSbda", "eGamersWorld"),
    ("ambrosia", "Ambrosia", "Leonida centrale", "Région intérieure industrielle et agricole autour de la raffinerie Allied Crystal et du lac Leonida.", "Les sources citent aussi Ambrosia Raceway, Store n' Bolt et Wyatt Motors. L'attribution administrative reste divergente dans les sources consultées : ne pas figer un comté.", "https://fr.egamersworld.com/blog/gta-6-map-guide-every-region-of-leonida-and-what-t-DBov8HSbda", "eGamersWorld / Promptowy"),
    ("mount-kalaga", "Mount Kalaga National Park", "Lummox", "Parc national du nord de Leonida, caractérisé par ses forêts, rivières, routes de canyon et sentiers isolés.", "Repères cités : Millport, Grayson, Yorktown, Bonanza, Adler Creek et la cabane de Bret. La source évoque chasse, pêche et observation de la faune.", "https://fr.egamersworld.com/blog/gta-6-map-guide-every-region-of-leonida-and-what-t-DBov8HSbda", "eGamersWorld / Promptowy"),
]

ENTRIES = [
    {
        "id": "base-mill-station-radar",
        "slug": "mill-station-radar-base",
        "title": "Mill Station Radar Base",
        "summary": "Base radar au nord de Watson Bay ; le guide GTA Guide y situe une opération illégale avec une arme et un coffre.",
        "body": "Procédure rapportée par GTA Guide : accéder au toit, entrer par la trappe ouverte et descendre dans la salle de stockage. Une mallette contenant le fusil à pompe Hostile Super400 serait posée sur une étagère. Les doubles portes conduisent au bureau voisin ; le coffre serait à droite en sortant de la salle de stockage.\n\nLa page source situe le bâtiment au nord de Watson Bay, dans la zone des Grassrivers. Aucune coordonnée précise n'a été extraite : le repère cartographique reste à créer après vérification.\n\nStatut : information rapportée par une source tierce, non confirmée indépendamment en jeu.",
        "category": "base_radar",
        "region": "Grassrivers",
        "source_url": "https://gtaguide.fr/articles/gta-6-hostile-super400-base-radar-mill-station-ou-trouver/",
        "source_label": "GTA Guide",
        "status": "unverified",
    },
    {
        "id": "weapon-hostile-super400",
        "slug": "hostile-super400",
        "title": "Hostile Super400",
        "summary": "Variante du fusil à pompe Super400, signalée comme butin de l'opération Mill Station Radar Base.",
        "body": "GTA Guide décrit le Hostile Super400 comme une variante unique du Girardi Super400. La fiche indique un chargeur de 7 cartouches et une arme non personnalisable. L'article de localisation décrit une récupération gratuite dans une mallette située sur une étagère de la salle de stockage de Mill Station Radar Base.\n\nCes caractéristiques sont reprises de la source et restent à vérifier en jeu. Aucun visuel tiers n'est copié dans la base.",
        "category": "weapon",
        "region": "Grassrivers",
        "source_url": "https://gtaguide.fr/armes/hostile-super400/",
        "source_label": "GTA Guide",
        "status": "unverified",
    },
    {
        "id": "base-wild-hog-point-radar",
        "slug": "wild-hog-point-radar-base",
        "title": "Wild Hog Point Radar Base",
        "summary": "Fiche IGN référencée ; contenu détaillé et emplacement précis à récupérer.",
        "body": "Source IGN enregistrée pour enrichissement. Le contenu de la page n'a pas pu être récupéré lors de cette collecte. Aucune localisation, récompense, procédure d'accès ou coordonnée n'est déduite du seul titre.",
        "category": "base_radar",
        "region": None,
        "source_url": "https://www.ign.com/wikis/gta-6/Wild_Hog_Point_Radar_Base",
        "source_label": "IGN Wiki",
        "status": "source_pending",
    },

    {
        "id": "mission-lab-fees",
        "slug": "lab-fees",
        "title": "Lab Fees — codes 0420 et 7700",
        "summary": "Mission du chapitre 1 à Key Lento : prérequis, deux codes de digicode et récupération de la récompense de 600 $.",
        "body": "PRÉREQUIS\nTerminer Gone Fishing. La mission est donnée par Brian Heder et se déroule à Key Lento.\n\nÉTAPES\n1. Rejoindre Key Lento après Gone Fishing.\n2. Entrer dans le magasin de souvenirs pour faire avancer l'objectif.\n3. Utiliser les codes 0420 et 7700 sur les verrous à digicode des zones de stockage.\n4. Terminer les interactions dans la boutique et les locaux de stockage.\n\nRÉCOMPENSE\nLa mission rapporte 600 $. Selon la source, la somme est déposée dans la boîte aux lettres devant la maison de Jason et non créditée immédiatement. L'accès au compte bancaire arrive plus tard avec Buck Me.\n\nSTATUT\nProcédure reprise et reformulée à partir de Promptowy ; à confirmer en jeu.",
        "category": "mission",
        "region": "Leonida Keys",
        "source_url": "https://promptowy.com/fr/gta-6/gta-6-soluce-lab-fees/",
        "source_label": "Promptowy",
        "status": "unverified",
    },
    {
        "id": "mission-just-a-scratch",
        "slug": "just-a-scratch",
        "title": "Just a Scratch — réparer le pickup Ganado",
        "summary": "Mission du chapitre 1 : conduire le pickup de Jason au garage Coastal Auto Care et obtenir une réparation moteur et une peinture gratuites.",
        "body": "PRÉREQUIS\nLa source indique que la mission est accessible après Gone Fishing. Elle introduit les garages de réparation et de peinture.\n\nÉTAPES\n1. Prendre le pickup '70 Ganado stationné devant la maison de Jason.\n2. Suivre le repère jusqu'au garage Coastal Auto Care à Key Lento.\n3. Entrer dans l'atelier et faire réparer gratuitement le moteur.\n4. Choisir une nouvelle couleur de peinture pour terminer l'objectif.\n\nÀ SAVOIR\nLa source indique que le pickup est remplacé à la fin du chapitre 1 : investir dans des améliorations durables avant ce remplacement peut être inutile. Elle propose aussi de sauvegarder puis recharger si le véhicule est très endommagé avant le trajet.\n\nSTATUT\nProcédure reprise et reformulée à partir de Promptowy ; à confirmer en jeu.",
        "category": "mission",
        "region": "Leonida Keys",
        "source_url": "https://promptowy.com/fr/gta-6/gta-6-soluce-just-a-scratch/",
        "source_label": "Promptowy",
        "status": "unverified",
    },
    {
        "id": "location-mill-station",
        "slug": "mill-station-radar-base",
        "title": "Mill Station Radar Base — arme et coffre",
        "summary": "Opération illégale au nord de Watson Bay : la source décrit une entrée par le toit, un Hostile Super400 et un coffre dans le bureau voisin.",
        "body": "EMPLACEMENT RAPPORTÉ\nGTA Guide situe le bâtiment au nord de Watson Bay, dans le secteur des Grassrivers. La position exacte n'est pas fournie ici : consulte la carte externe pour chercher le secteur, sans considérer un point approximatif comme une coordonnée vérifiée.\n\nACCÈS ET BUTIN\n1. Rejoindre le bâtiment de la base radar.\n2. Monter sur le toit et utiliser la trappe ouverte.\n3. Descendre dans la salle de stockage et ouvrir la mallette posée sur une étagère pour récupérer le Hostile Super400.\n4. Passer par les doubles portes vers le bureau voisin.\n5. En sortant de la salle de stockage, prendre à droite pour trouver le coffre et récupérer l'argent.\n\nLa source indique que cette opération n'est liée à aucun chapitre. Aucun repère GPS n'est publié dans cette fiche tant que les coordonnées ne sont pas confirmées.",
        "category": "base_radar",
        "region": "Grassrivers",
        "source_url": "https://gtaguide.fr/articles/gta-6-hostile-super400-base-radar-mill-station-ou-trouver/",
        "source_label": "GTA Guide",
        "status": "unverified",
    },
]

def seed_reference_data():
    conn = connect()
    try:
        # Safe additive migrations for databases created by earlier app versions.
        columns = {row["name"] for row in conn.execute("PRAGMA table_info(guide_entries)").fetchall()}
        for name, sql_type in (("source_url", "TEXT"), ("source_label", "TEXT"), ("media_url", "TEXT")):
            if name not in columns:
                conn.execute(f"ALTER TABLE guide_entries ADD COLUMN {name} {sql_type}")

        for name, url, kind in SOURCES:
            conn.execute(
                "INSERT OR IGNORE INTO sources(name,url,kind,enabled) VALUES(?,?,?,1)",
                (name, url, kind),
            )

        for slug, name, county, summary, body, source_url, source_label in REGIONS:
            conn.execute(
                """INSERT OR IGNORE INTO guide_entries
                (id,slug,title,summary,body,category,platform,status,region,source_url,source_label)
                VALUES(?,?,?,?,?,'region','both','unverified',?,?,?)""",
                ("region-" + slug, "region-" + slug, name, summary, body, name, source_url, source_label),
            )

        for item in ENTRIES:
            conn.execute(
                """INSERT OR IGNORE INTO guide_entries
                (id,slug,title,summary,body,category,platform,status,region,source_url,source_label)
                VALUES(?,?,?,?,?,?, 'both',?,?,?,?)""",
                (item["id"], item["slug"], item["title"], item["summary"], item["body"],
                 item["category"], item["status"], item["region"], item["source_url"], item["source_label"]),
            )

        conn.commit()
        count = conn.execute("SELECT COUNT(*) FROM guide_entries").fetchone()[0]
        sources_count = conn.execute("SELECT COUNT(*) FROM sources WHERE enabled=1").fetchone()[0]
        return {"seeded": True, "guide_entries": count, "sources": sources_count}
    finally:
        conn.close()

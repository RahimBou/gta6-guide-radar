"""Idempotent starter dataset sourced from public GTA VI guide pages.

Descriptions are paraphrased, source URLs are retained, and entries remain
unverified until corroborated in-game or by an authorized primary source.
"""
from .db import connect

SOURCES = [
    ("Promptowy — carte interactive GTA 6", "https://promptowy.com/fr/gta-6/carte-interactive/", "website"),
    ("GTA Guide — guides et fiches GTA 6", "https://gtaguide.fr/", "website"),
    ("eGamersWorld — guide des régions de Leonida", "https://fr.egamersworld.com/blog/gta-6-map-guide-every-region-of-leonida-and-what-t-DBov8HSbda", "website"),
    ("IGN Wiki — GTA 6", "https://www.ign.com/wikis/gta-6/", "wiki"),
]

REGIONS = [
    ("vice-city", "Vice City", "Vice-Dale", "Zone urbaine majeure de Leonida. Promptowy la répertorie comme région ; eGamersWorld décrit aussi Vice Beach séparément.", "Downtown, Ocean Beach, Little Cuba, Southside, Stockyard, Tequesta et Decor District sont cités par eGamersWorld. À confirmer en jeu.", "https://promptowy.com/fr/gta-6/carte-interactive/", "Promptowy / eGamersWorld"),
    ("leonida-keys", "Leonida Keys", "Mariana", "Archipel du sud de Leonida, associé aux déplacements nautiques et aux activités côtières.", "Noms de lieux et activités détaillés à enrichir à partir de fiches dédiées.", "https://promptowy.com/fr/gta-6/carte-interactive/", "Promptowy / eGamersWorld"),
    ("grassrivers", "Grassrivers", "Mariana", "Région de zones humides et de marécages, associée à la faune et aux déplacements sur l'eau.", "Watson Bay est cité au nord de la zone dans le guide GTA Guide consacré à Mill Station Radar Base.", "https://fr.egamersworld.com/blog/gta-6-map-guide-every-region-of-leonida-and-what-t-DBov8HSbda", "eGamersWorld / GTA Guide"),
    ("port-gellhorn", "Port Gellhorn", "Kelly", "Région côtière décrite comme une zone touristique en déclin, avec motels, routes secondaires et activités motorisées.", "Draper Island et le circuit international de Gellhorn sont cités par eGamersWorld ; détails à confirmer.", "https://fr.egamersworld.com/blog/gta-6-map-guide-every-region-of-leonida-and-what-t-DBov8HSbda", "eGamersWorld"),
    ("ambrosia", "Ambrosia", "Leonida centrale / attribution à confirmer", "Région industrielle et agricole associée à la raffinerie Allied Crystal et au lac Leonida.", "L'appartenance administrative d'Ambrosia est signalée comme divergente dans l'article eGamersWorld. Ne pas figer le comté sans vérification.", "https://fr.egamersworld.com/blog/gta-6-map-guide-every-region-of-leonida-and-what-t-DBov8HSbda", "eGamersWorld"),
    ("mount-kalaga", "Mount Kalaga National Park", "Lummox (selon eGamersWorld)", "Zone du nord décrite comme un parc naturel avec forêts, reliefs, sentiers et faune sauvage.", "Millport, Grayson, Yorktown et Bonanza sont cités dans l'article ; à corroborer.", "https://fr.egamersworld.com/blog/gta-6-map-guide-every-region-of-leonida-and-what-t-DBov8HSbda", "eGamersWorld"),
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

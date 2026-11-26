import argparse
from .db import connect
from .collector import collect_feeds

STATUSES = {"unverified", "to_check", "corroborated", "verified_in_game", "official", "false"}
PLATFORMS = {"tiktok", "youtube", "reddit", "website", "other"}

def main():
    parser = argparse.ArgumentParser(prog="gta6radar")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init")
    p = sub.add_parser("add-source")
    p.add_argument("--name", required=True)
    p.add_argument("--url", required=True)
    p.add_argument("--kind", choices=["rss"], default="rss")
    p = sub.add_parser("add-item")
    p.add_argument("--url", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--platform", choices=sorted(PLATFORMS), default="other")
    p.add_argument("--category", default="to_classify")
    p.add_argument("--summary", default="")
    p = sub.add_parser("set-status")
    p.add_argument("--id", type=int, required=True)
    p.add_argument("--status", choices=sorted(STATUSES), required=True)
    sub.add_parser("collect")
    sub.add_parser("list")
    args = parser.parse_args()

    conn = connect()
    if args.command == "init":
        print("Base SQLite initialisée.")
    elif args.command == "add-source":
        conn.execute("INSERT OR IGNORE INTO sources(name, url, kind) VALUES (?, ?, ?)",
                     (args.name, args.url, args.kind))
        conn.commit()
        print("Source enregistrée (ou déjà présente).")
    elif args.command == "add-item":
        conn.execute("""INSERT OR IGNORE INTO items(url, title, platform, category, summary)
                        VALUES (?, ?, ?, ?, ?)""",
                     (args.url, args.title, args.platform, args.category, args.summary))
        conn.commit()
        print("Publication enregistrée (ou déjà présente).")
    elif args.command == "set-status":
        cur = conn.execute("UPDATE items SET status = ? WHERE id = ?",
                           (args.status, args.id))
        conn.commit()
        print("Statut mis à jour." if cur.rowcount else "Identifiant introuvable.")
    elif args.command == "collect":
        conn.close()
        count, errors = collect_feeds()
        print(f"{count} nouvelle(s) publication(s) importée(s).")
        for error in errors:
            print(f"ERREUR: {error}")
        return
    elif args.command == "list":
        for row in conn.execute("""SELECT id, platform, status, category, title, url
                                  FROM items ORDER BY collected_at DESC"""):
            print(f'#{row["id"]} [{row["status"]}] {row["platform"]} / {row["category"]} — {row["title"]}\n  {row["url"]}')
    conn.close()

if __name__ == "__main__":
    main()

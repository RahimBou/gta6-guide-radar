import feedparser
from .db import connect

def collect_feeds():
    conn = connect()
    sources = conn.execute(
        "SELECT id, name, url FROM sources WHERE enabled = 1 AND kind = 'rss'"
    ).fetchall()
    inserted = 0
    errors = []
    for source in sources:
        try:
            feed = feedparser.parse(source["url"])
            if feed.bozo and not feed.entries:
                raise ValueError(str(feed.bozo_exception))
            for entry in feed.entries:
                url = entry.get("link", "").strip()
                title = entry.get("title", "").strip() or url
                if not url:
                    continue
                summary = entry.get("summary", "") or ""
                published = entry.get("published", None)
                platform = "other"
                lowered = url.lower()
                if "tiktok.com" in lowered:
                    platform = "tiktok"
                elif "youtube.com" in lowered or "youtu.be" in lowered:
                    platform = "youtube"
                elif "reddit.com" in lowered:
                    platform = "reddit"
                cur = conn.execute(
                    """INSERT OR IGNORE INTO items
                    (source_id, platform, url, title, summary, published_at)
                    VALUES (?, ?, ?, ?, ?, ?)""",
                    (source["id"], platform, url, title, summary, published)
                )
                inserted += cur.rowcount
        except Exception as exc:
            errors.append(f'{source["name"]}: {exc}')
    conn.commit()
    conn.close()
    return inserted, errors

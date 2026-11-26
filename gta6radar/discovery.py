"""Official-API discovery adapters for GTA 6 gameplay videos.

This module discovers metadata only. It never downloads third-party media.
"""
import json
import os
import urllib.parse
import urllib.request
import urllib.error
import uuid
import xml.etree.ElementTree as ET
from .db import connect

TIMEOUT = 15
QUERIES = [
    "GTA 6 gameplay tips",
    "GTA VI mission walkthrough",
    "GTA 6 secrets locations",
    "GTA VI vehicles guide",
    "GTA 6 hidden details",
    "GTA 6 beginner tips settings money police",
    "GTA 6 Chapter 1 mission walkthrough",
    "GTA 6 Chapter 2 mission walkthrough",
    "GTA 6 collectibles 100 percent guide",
    "GTA 6 map locations easter eggs",
    "GTA 6 weapons rare vehicles locations",
    "GTA 6 gameplay astuces guide français",
    "GTA 6 solution missions français",
    "GTA 6 secrets easter eggs français",
    "GTA 6 carte objets cachés collectibles français",
]

def _get_json(url, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": "GTA6GuideRadar/1.0", **(headers or {})})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
        return json.loads(response.read().decode("utf-8"))

def discover_youtube():
    key = os.environ.get("YOUTUBE_API_KEY", "").strip()
    if not key:
        return {"platform": "youtube", "added": 0, "skipped": "YOUTUBE_API_KEY missing"}
    added = 0
    conn = connect()
    try:
        for query in QUERIES:
            params = urllib.parse.urlencode({
                "part": "snippet", "type": "video", "maxResults": 15,
                "order": "date", "q": query, "key": key
            })
            data = _get_json("https://www.googleapis.com/youtube/v3/search?" + params)
            for item in data.get("items", []):
                video_id = item.get("id", {}).get("videoId")
                snippet = item.get("snippet", {})
                if not video_id:
                    continue
                url = "https://www.youtube.com/watch?v=" + video_id
                cur = conn.execute("""
                    INSERT OR IGNORE INTO robot_videos
                    (id,platform,url,title,creator,status,rights_status)
                    VALUES(?,?,?,?,?,'detected','unknown')
                """, (str(uuid.uuid4()), "youtube", url, snippet.get("title") or "Vidéo YouTube", snippet.get("channelTitle") or ""))
                if cur.rowcount:
                    video_pk = conn.execute("SELECT id FROM robot_videos WHERE url=?", (url,)).fetchone()["id"]
                    conn.execute("""
                        INSERT INTO robot_jobs(id,video_id,stage,status,message)
                        VALUES(?,?,'rights_check','waiting','Métadonnées collectées via YouTube Data API. Vérifier les droits avant analyse média.')
                    """, (str(uuid.uuid4()), video_pk))
                    added += 1
        conn.commit()
    finally:
        conn.close()
    return {"platform": "youtube", "added": added}

def _twitch_token(client_id, client_secret):
    data = urllib.parse.urlencode({
        "client_id": client_id, "client_secret": client_secret,
        "grant_type": "client_credentials"
    }).encode()
    req = urllib.request.Request("https://id.twitch.tv/oauth2/token", data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
        return json.loads(response.read().decode("utf-8"))["access_token"]

def discover_twitch():
    client_id = os.environ.get("TWITCH_CLIENT_ID", "").strip()
    client_secret = os.environ.get("TWITCH_CLIENT_SECRET", "").strip()
    if not client_id or not client_secret:
        return {"platform": "twitch", "added": 0, "skipped": "TWITCH_CLIENT_ID/SECRET missing"}
    token = _twitch_token(client_id, client_secret)
    headers = {"Client-ID": client_id, "Authorization": "Bearer " + token}
    params = urllib.parse.urlencode({"query": "GTA VI", "first": 25})
    channels = _get_json("https://api.twitch.tv/helix/search/channels?" + params, headers).get("data", [])
    added = 0
    conn = connect()
    try:
        for channel in channels[:12]:
            user_id = channel.get("id")
            if not user_id:
                continue
            video_params = urllib.parse.urlencode({"user_id": user_id, "first": 20, "type": "archive"})
            videos = _get_json("https://api.twitch.tv/helix/videos?" + video_params, headers).get("data", [])
            for item in videos:
                video_id = str(item.get("id", ""))
                if not video_id:
                    continue
                url = item.get("url") or ("https://www.twitch.tv/videos/" + video_id)
                cur = conn.execute("""
                    INSERT OR IGNORE INTO robot_videos
                    (id,platform,url,title,creator,status,rights_status)
                    VALUES(?,?,?,?,?,'detected','unknown')
                """, (str(uuid.uuid4()), "twitch", url, item.get("title") or "VOD Twitch", item.get("user_name") or channel.get("display_name") or ""))
                if cur.rowcount:
                    video_pk = conn.execute("SELECT id FROM robot_videos WHERE url=?", (url,)).fetchone()["id"]
                    conn.execute("""
                        INSERT INTO robot_jobs(id,video_id,stage,status,message)
                        VALUES(?,?,'rights_check','waiting','Métadonnées collectées via Twitch Helix. Vérifier les droits avant analyse média.')
                    """, (str(uuid.uuid4()), video_pk))
                    added += 1
        conn.commit()
    finally:
        conn.close()
    return {"platform": "twitch", "added": added}


NEWS_QUERIES = [
    '"Grand Theft Auto VI" guide',
    '"GTA 6" mission walkthrough',
    '"GTA 6" map locations collectibles',
    '"GTA 6" vehicles weapons secrets',
    'site:rockstargames.com/newswire "Grand Theft Auto VI"',
    '"GTA 6" astuces guide français',
    '"GTA 6" solution mission chapitre',
    '"GTA 6" argent braquage codes coffre',
    '"GTA 6" véhicules rares armes uniques',
    '"GTA 6" trophées 100% collectibles',
    '"GTA VI" gameplay tips secrets',
    '"GTA 6" mise à jour patch notes',
]

def discover_public_news():
    """Index public RSS metadata and links only; never copies article bodies."""
    added, errors = 0, []
    conn = connect()
    try:
        for query in NEWS_QUERIES:
            params = urllib.parse.urlencode({"q": query, "hl": "en-US", "gl": "US", "ceid": "US:en"})
            request = urllib.request.Request(
                "https://news.google.com/rss/search?" + params,
                headers={"User-Agent": "GTA6GuideRadar/1.0"})
            try:
                with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
                    root = ET.fromstring(response.read())
                for node in root.findall("./channel/item"):
                    title = (node.findtext("title") or "").strip()[:300]
                    link = (node.findtext("link") or "").strip()
                    summary = (node.findtext("description") or "").strip()[:1200]
                    published = (node.findtext("pubDate") or "").strip()
                    if not title or not link.startswith("https://"):
                        continue
                    low = title.lower()
                    category = "news"
                    if any(k in low for k in ("mission", "walkthrough", "chapter", "story")):
                        category = "mission_guide"
                    elif any(k in low for k in ("map", "location", "collectible", "secret")):
                        category = "map_discovery"
                    elif any(k in low for k in ("vehicle", "car", "weapon")):
                        category = "vehicle_gear"
                    elif any(k in low for k in ("update", "patch", "fix")):
                        category = "updates"
                    cur = conn.execute("""
                        INSERT OR IGNORE INTO items
                        (platform,url,title,summary,category,status,published_at)
                        VALUES('news_rss',?,?,?,?, 'unverified',?)
                    """, (link, title, summary, category, published))
                    added += max(cur.rowcount, 0)
            except (urllib.error.URLError, TimeoutError, ET.ParseError, ValueError) as exc:
                errors.append(str(exc)[:180])
        conn.commit()
    finally:
        conn.close()
    return {"platform": "public_news_rss", "added": added, "queries": len(NEWS_QUERIES), "errors": errors[:3]}

def discover_all():
    results = []
    for fn in (discover_public_news, discover_youtube, discover_twitch):
        try:
            results.append(fn())
        except (urllib.error.URLError, TimeoutError, ValueError, KeyError) as exc:
            results.append({"platform": fn.__name__.replace("discover_", ""), "added": 0, "error": str(exc)[:240]})
    results.append({
        "platform": "tiktok",
        "added": 0,
        "skipped": "Connecteur en attente de l'OAuth TikTok et du consentement des créateurs."
    })
    return results

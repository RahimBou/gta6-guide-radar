"""Official-API discovery adapters for GTA 6 gameplay videos.

This module discovers metadata only. It never downloads third-party media.
"""
import json
import os
import urllib.parse
import urllib.request
import urllib.error
import uuid
from .db import connect

TIMEOUT = 15
QUERIES = [
    "GTA 6 gameplay tips",
    "GTA VI mission walkthrough",
    "GTA 6 secrets locations",
    "GTA VI vehicles guide",
    "GTA 6 hidden details",
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
    params = urllib.parse.urlencode({"query": "GTA VI", "first": 50})
    data = _get_json("https://api.twitch.tv/helix/videos?" + params, {
        "Client-ID": client_id, "Authorization": "Bearer " + token
    })
    added = 0
    conn = connect()
    try:
        for item in data.get("data", []):
            video_id = str(item.get("id", ""))
            if not video_id:
                continue
            url = item.get("url") or ("https://www.twitch.tv/videos/" + video_id)
            cur = conn.execute("""
                INSERT OR IGNORE INTO robot_videos
                (id,platform,url,title,creator,status,rights_status)
                VALUES(?,?,?, ?,?,'detected','unknown')
            """, (str(uuid.uuid4()), "twitch", url, item.get("title") or "VOD Twitch", item.get("user_name") or ""))
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

def discover_all():
    results = []
    for fn in (discover_youtube, discover_twitch):
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

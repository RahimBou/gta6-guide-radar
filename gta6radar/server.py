"""GTA 6 Guide Radar — API and static application server."""
import json
import os
import re
import secrets
import uuid
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
from .db import connect

ROOT = Path(__file__).resolve().parent.parent / "app"
PLATFORM_HOSTS = {
    "youtube": {"youtube.com", "www.youtube.com", "youtu.be", "m.youtube.com"},
    "tiktok": {"tiktok.com", "www.tiktok.com", "vm.tiktok.com"},
    "twitch": {"twitch.tv", "www.twitch.tv", "m.twitch.tv"},
}

def detect_platform(url):
    host = (urlparse(url).hostname or "").lower()
    for platform, hosts in PLATFORM_HOSTS.items():
        if host in hosts or any(host.endswith("." + h) for h in hosts):
            return platform
    return "other"

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def read_json(self, max_bytes=20000):
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0 or length > max_bytes:
            raise ValueError("invalid_payload_size")
        return json.loads(self.rfile.read(length))

    def authorized(self):
        token = os.environ.get("GTA6_ADMIN_TOKEN", "")
        supplied = self.headers.get("Authorization", "").removeprefix("Bearer ").strip()
        return bool(token) and secrets.compare_digest(token, supplied)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/health":
            return self.send_json(200, {"ok": True, "service": "gta6-guide-radar", "mode": "video-first"})
        if path == "/api/robot/overview":
            conn = connect()
            result = {
                "videos": conn.execute("SELECT COUNT(*) FROM robot_videos").fetchone()[0],
                "waiting": conn.execute("SELECT COUNT(*) FROM robot_jobs WHERE status='waiting'").fetchone()[0],
                "tips": conn.execute("SELECT COUNT(*) FROM robot_tips").fetchone()[0],
                "published": conn.execute("SELECT COUNT(*) FROM robot_tips WHERE status='published'").fetchone()[0],
            }
            conn.close()
            return self.send_json(200, result)
        if path == "/api/robot/videos":
            conn = connect()
            rows = conn.execute("""
                SELECT v.*, (SELECT COUNT(*) FROM robot_evidence e WHERE e.video_id=v.id) AS evidence_count,
                (SELECT COUNT(*) FROM robot_tips t WHERE t.video_id=v.id) AS tip_count
                FROM robot_videos v ORDER BY v.created_at DESC LIMIT 100
            """).fetchall()
            conn.close()
            return self.send_json(200, {"items": [dict(row) for row in rows]})
        if path == "/api/robot/tips":
            conn = connect()
            rows = conn.execute("""
                SELECT t.*, v.title AS video_title, v.url AS video_url
                FROM robot_tips t JOIN robot_videos v ON v.id=t.video_id
                ORDER BY t.created_at DESC LIMIT 100
            """).fetchall()
            conn.close()
            return self.send_json(200, {"items": [dict(row) for row in rows]})
        return super().do_GET()

    def do_POST(self):
        path = urlparse(self.path).path
        if path == "/api/robot/videos":
            try:
                data = self.read_json()
                url = str(data.get("url", "")).strip()
                parsed = urlparse(url)
                if parsed.scheme != "https" or not parsed.hostname:
                    return self.send_json(400, {"error": "https_url_required"})
                if detect_platform(url) == "other" and not data.get("allow_other"):
                    return self.send_json(400, {"error": "unsupported_video_host"})
                title = str(data.get("title") or "Vidéo à analyser").strip()[:200]
                creator = str(data.get("creator") or "").strip()[:120]
                platform = detect_platform(url)
                video_id, job_id = str(uuid.uuid4()), str(uuid.uuid4())
                conn = connect()
                conn.execute("""
                    INSERT INTO robot_videos(id,platform,url,title,creator,status)
                    VALUES(?,?,?,?,?,'detected')
                """, (video_id, platform, url, title, creator))
                conn.execute("""
                    INSERT INTO robot_jobs(id,video_id,stage,status,message)
                    VALUES(?,?,'rights_check','waiting','Vérifier les droits et les conditions d’accès avant toute analyse média.')
                """, (job_id, video_id))
                conn.commit()
                conn.close()
                return self.send_json(201, {"ok": True, "id": video_id, "job_id": job_id, "platform": platform, "status": "detected"})
            except sqlite3.IntegrityError:
                return self.send_json(409, {"error": "video_already_added"})
            except (ValueError, TypeError, json.JSONDecodeError):
                return self.send_json(400, {"error": "invalid_payload"})
        if path == "/api/robot/tips/review":
            if not self.authorized():
                return self.send_json(401, {"error": "unauthorized"})
            try:
                data = self.read_json()
                tip_id, action = str(data.get("id", "")), str(data.get("action", ""))
                if action not in {"approve", "reject", "publish"}:
                    return self.send_json(400, {"error": "invalid_action"})
                next_status = {"approve": "approved", "reject": "rejected", "publish": "published"}[action]
                conn = connect()
                cur = conn.execute("UPDATE robot_tips SET status=? WHERE id=?", (next_status, tip_id))
                conn.commit()
                conn.close()
                return self.send_json(200 if cur.rowcount else 404, {"ok": bool(cur.rowcount), "status": next_status})
            except (ValueError, TypeError, json.JSONDecodeError):
                return self.send_json(400, {"error": "invalid_payload"})
        return self.send_json(404, {"error": "not_found"})

    def log_message(self, fmt, *args):
        print("%s - %s" % (self.address_string(), fmt % args))

def main():
    host = os.environ.get("GTA6_HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", os.environ.get("GTA6_PORT", "8080")))
    connect().close()
    print(f"GTA 6 Guide Radar disponible sur http://{host}:{port}")
    ThreadingHTTPServer((host, port), Handler).serve_forever()

if __name__ == "__main__":
    import sqlite3
    main()

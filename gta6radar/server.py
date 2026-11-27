"""GTA 6 Guide Radar — API and static application server."""
import json
import os
import re
import secrets
import sqlite3
import uuid
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
from .db import connect
from .discovery import discover_all
from .seed import seed_reference_data

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
            return self.send_json(200, {
                "ok": True,
                "service": "gta6-guide-radar",
                "mode": "video-first",
                "storage": "configured" if os.environ.get("GTA6_DB_PATH") or os.environ.get("GTA6_DATA_DIR") else "local_default",
            })
        if path == "/api/map/markers":
            conn = connect()
            rows = conn.execute("""
                SELECT id,title,description,category,status,platform,region,grid_ref,
                       x,y,source_url,source_label,verified_at
                FROM map_markers ORDER BY title COLLATE NOCASE
            """).fetchall()
            conn.close()
            return self.send_json(200, {"items": [dict(row) for row in rows]})
        if path == "/api/guide/entries":
            from urllib.parse import parse_qs
            category = parse_qs(urlparse(self.path).query).get("category", [""])[0].strip()
            conn = connect()
            if category:
                rows = conn.execute("""
                    SELECT id,slug,title,summary,body,category,platform,status,region,grid_ref,source_url,source_label,media_url
                    FROM guide_entries WHERE category=? ORDER BY title COLLATE NOCASE
                """, (category,)).fetchall()
            else:
                rows = conn.execute("""
                    SELECT id,slug,title,summary,body,category,platform,status,region,grid_ref,source_url,source_label,media_url
                    FROM guide_entries ORDER BY title COLLATE NOCASE
                """).fetchall()
            conn.close()
            return self.send_json(200, {"items": [dict(row) for row in rows]})
        if path == "/api/guide/sources":
            conn = connect()
            rows = conn.execute("""
                SELECT id,name,url,kind,enabled,created_at
                FROM sources ORDER BY name COLLATE NOCASE
            """).fetchall()
            conn.close()
            return self.send_json(200, {"items": [dict(row) for row in rows]})
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
        if path == "/api/robot/discover":
            return self.send_json(405, {"error": "method_not_allowed", "message": "Utilisez POST pour lancer une collecte."})
        if path == "/api/robot/items":
            conn = connect()
            rows = conn.execute("""
                SELECT id,platform,url,title,summary,category,status,published_at,collected_at
                FROM items ORDER BY COALESCE(published_at,collected_at) DESC LIMIT 200
            """).fetchall()
            conn.close()
            return self.send_json(200, {"items": [dict(row) for row in rows]})
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
        if path in ("/api/map/markers", "/api/markers"):
            if not self.authorized():
                return self.send_json(401, {"error": "unauthorized"})
            try:
                data = self.read_json(max_bytes=12000)
                marker_id = str(data.get("id") or uuid.uuid4()).strip()[:80]
                title = str(data.get("title") or "").strip()[:160]
                category = str(data.get("category") or "other").strip()[:40]
                status = str(data.get("status") or "unverified").strip()[:40]
                platform = str(data.get("platform") or "both").strip()[:20]
                region = str(data.get("region") or "").strip()[:100]
                grid_ref = str(data.get("grid_ref") or "").strip()[:20]
                description = str(data.get("description") or "").strip()[:3000]
                source_url = str(data.get("source_url") or "").strip()[:1000]
                source_label = str(data.get("source_label") or "").strip()[:120]
                x, y = float(data.get("x")), float(data.get("y"))
                if not title or not category or not (0 <= x <= 100 and 0 <= y <= 100):
                    return self.send_json(400, {"error": "title_category_and_valid_coordinates_required"})
                if source_url and urlparse(source_url).scheme not in ("http", "https"):
                    return self.send_json(400, {"error": "invalid_source_url"})
                conn = connect()
                conn.execute("""
                    INSERT INTO map_markers
                    (id,title,description,category,status,platform,region,grid_ref,x,y,source_url,source_label,verified_at)
                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
                    ON CONFLICT(id) DO UPDATE SET
                    title=excluded.title, description=excluded.description,
                    category=excluded.category, status=excluded.status,
                    platform=excluded.platform, region=excluded.region,
                    grid_ref=excluded.grid_ref, x=excluded.x, y=excluded.y,
                    source_url=excluded.source_url, source_label=excluded.source_label,
                    verified_at=excluded.verified_at, updated_at=CURRENT_TIMESTAMP
                """, (marker_id,title,description,category,status,platform,region,grid_ref,x,y,source_url,source_label,data.get("verified_at")))
                conn.commit()
                conn.close()
                return self.send_json(201, {"ok": True, "id": marker_id})
            except (ValueError, TypeError, sqlite3.Error, json.JSONDecodeError):
                return self.send_json(400, {"error": "invalid_marker_payload"})
        if path == "/api/robot/discover":
            if not self.authorized():
                return self.send_json(401, {"error": "unauthorized"})
            try:
                return self.send_json(200, {"ok": True, "results": discover_all()})
            except Exception as exc:
                return self.send_json(500, {"error": "discovery_failed", "message": str(exc)[:240]})
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
        if path == "/api/robot/analyse-media":
            if not self.authorized():
                return self.send_json(401, {"error": "unauthorized"})
            try:
                data = self.read_json(max_bytes=30000)
                video_id = str(data.get("video_id", "")).strip()
                audio_path = str(data.get("audio_path", "")).strip()
                frame_paths = data.get("frame_paths", [])
                if not video_id or not audio_path or not isinstance(frame_paths, list):
                    return self.send_json(400, {"error": "video_id_audio_path_and_frame_paths_required"})
                conn = connect()
                video = conn.execute("SELECT rights_status FROM robot_videos WHERE id=?", (video_id,)).fetchone()
                conn.close()
                if not video:
                    return self.send_json(404, {"error": "video_not_found"})
                if video["rights_status"] not in ("owned", "licensed", "authorized"):
                    return self.send_json(409, {"error": "rights_not_cleared"})
                from .ai import transcribe_audio, analyse_video
                asr = transcribe_audio(audio_path)
                tips = analyse_video(asr["text"], frame_paths)
                conn = connect()
                conn.execute("UPDATE robot_videos SET transcript=?,status='analysed',updated_at=CURRENT_TIMESTAMP WHERE id=?",
                             (asr["text"], video_id))
                created = 0
                for tip in tips[:20]:
                    title = str(tip.get("title") or "Astuce à vérifier")[:180]
                    category = str(tip.get("category") or "astuce")[:40]
                    body = json.dumps(tip, ensure_ascii=False)
                    confidence = {"low": 0.25, "medium": 0.55, "high": 0.8}.get(str(tip.get("confidence", "low")).lower(), 0.25)
                    conn.execute("INSERT INTO robot_tips(id,video_id,title,category,body,status,confidence) VALUES(?,?,?,?,?,'pending',?)",
                                 (str(uuid.uuid4()), video_id, title, category, body, confidence))
                    created += 1
                conn.commit()
                conn.close()
                return self.send_json(200, {"ok": True, "transcript_chars": len(asr["text"]), "language": asr.get("language"), "tips_created": created, "status": "pending_review"})
            except Exception as exc:
                return self.send_json(502, {"error": "ai_processing_failed", "message": str(exc)[:500]})
        if path == "/api/robot/videos/transcript":
            if not self.authorized():
                return self.send_json(401, {"error": "unauthorized"})
            try:
                data = self.read_json(max_bytes=500000)
                video_id = str(data.get("video_id", "")).strip()
                transcript = str(data.get("transcript", "")).strip()
                rights_status = str(data.get("rights_status", "")).strip()
                if not video_id or len(transcript) < 80 or rights_status not in {"owned", "licensed", "authorized", "public_text"}:
                    return self.send_json(400, {"error": "video_id_transcript_and_cleared_rights_required"})
                conn = connect()
                cur = conn.execute("""
                    UPDATE robot_videos
                    SET transcript=?, rights_status=?, status='transcript_ready', updated_at=CURRENT_TIMESTAMP
                    WHERE id=?
                """, (transcript, rights_status, video_id))
                conn.commit()
                conn.close()
                return self.send_json(200 if cur.rowcount else 404, {"ok": bool(cur.rowcount), "status": "transcript_ready"})
            except (ValueError, TypeError, json.JSONDecodeError):
                return self.send_json(400, {"error": "invalid_payload"})
        if path == "/api/robot/process":
            if not self.authorized():
                return self.send_json(401, {"error": "unauthorized"})
            try:
                data = self.read_json()
                video_id = str(data.get("video_id", "")).strip()
                if not video_id:
                    return self.send_json(400, {"error": "video_id_required"})
                from .pipeline import process_video
                result = process_video(video_id)
                return self.send_json(200 if result.get("ok") else 409, result)
            except Exception as exc:
                return self.send_json(500, {"error": "processing_failed", "message": str(exc)[:240]})
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
    seed_result = seed_reference_data()
    print(f"Données de référence chargées : {seed_result}")
    print(f"GTA 6 Guide Radar disponible sur http://{host}:{port}")
    ThreadingHTTPServer((host, port), Handler).serve_forever()

if __name__ == "__main__":
    main()

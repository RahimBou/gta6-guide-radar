"""Serveur local léger pour l'interface et l'API GTA 6 Guide Radar."""
import json
import os
import re
import secrets
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
from .db import connect

ROOT = Path(__file__).resolve().parent.parent / "app"
STATUSES = {"unverified", "to_check", "corroborated", "verified_in_game", "official", "false"}
CATEGORIES = {"regions", "vehicles", "missions", "collectibles", "secrets", "weapons", "shops", "activities", "other"}

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

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/health":
            return self.send_json(200, {"ok": True, "service": "gta6-guide-radar"})
        if path == "/api/markers":
            conn = connect()
            rows = conn.execute("""
                SELECT id,title,description,category,status,platform,region,grid_ref,x,y,
                       entry_id,source_url,source_label,verified_at
                FROM map_markers WHERE status != 'false' ORDER BY title COLLATE NOCASE
            """).fetchall()
            conn.close()
            return self.send_json(200, {"items": [dict(row) for row in rows]})
        if path == "/api/entries":
            conn = connect()
            rows = conn.execute("""
                SELECT id,slug,title,summary,category,platform,status,region,grid_ref,updated_at
                FROM guide_entries WHERE status != 'false' ORDER BY updated_at DESC
            """).fetchall()
            conn.close()
            return self.send_json(200, {"items": [dict(row) for row in rows]})
        return super().do_GET()

    def do_POST(self):
        if urlparse(self.path).path != "/api/markers":
            return self.send_json(404, {"error": "not_found"})
        token = os.environ.get("GTA6_ADMIN_TOKEN", "")
        supplied = self.headers.get("Authorization", "").removeprefix("Bearer ").strip()
        if not token or not secrets.compare_digest(token, supplied):
            return self.send_json(401, {"error": "unauthorized"})
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 20000:
                return self.send_json(413, {"error": "invalid_payload_size"})
            data = json.loads(self.rfile.read(length))
            required = ("id", "title", "category", "x", "y")
            if any(key not in data for key in required):
                return self.send_json(400, {"error": "missing_required_fields"})
            if data["category"] not in CATEGORIES or data.get("status", "unverified") not in STATUSES:
                return self.send_json(400, {"error": "invalid_category_or_status"})
            x, y = float(data["x"]), float(data["y"])
            if not (0 <= x <= 100 and 0 <= y <= 100):
                return self.send_json(400, {"error": "coordinates_out_of_range"})
            source_url = str(data.get("source_url") or "").strip()
            source_label = str(data.get("source_label") or "").strip()
            if data.get("status") in {"official", "corroborated"} and not source_url:
                return self.send_json(400, {"error": "source_url_required_for_status"})
            if data.get("status") == "verified_in_game" and not (source_url or source_label):
                return self.send_json(400, {"error": "proof_reference_required_for_verified_marker"})
            if source_url and urlparse(source_url).scheme not in {"http", "https"}:
                return self.send_json(400, {"error": "source_url_must_be_http_or_https"})
            conn = connect()
            conn.execute("""
                INSERT INTO map_markers
                (id,title,description,category,status,platform,region,grid_ref,x,y,
                 source_url,source_label,verified_at,updated_at)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,CURRENT_TIMESTAMP)
                ON CONFLICT(id) DO UPDATE SET
                title=excluded.title, description=excluded.description,
                category=excluded.category, status=excluded.status,
                platform=excluded.platform, region=excluded.region,
                grid_ref=excluded.grid_ref, x=excluded.x, y=excluded.y,
                source_url=excluded.source_url, source_label=excluded.source_label,
                verified_at=excluded.verified_at, updated_at=CURRENT_TIMESTAMP
            """, (
                str(data["id"]), str(data["title"])[:160], str(data.get("description", ""))[:3000],
                data["category"], data.get("status", "unverified"), data.get("platform", "both"),
                data.get("region"), data.get("grid_ref"), x, y,
                source_url or None, source_label or None, data.get("verified_at")
            ))
            conn.commit()
            conn.close()
            return self.send_json(201, {"ok": True, "id": data["id"]})
        except (ValueError, TypeError, json.JSONDecodeError):
            return self.send_json(400, {"error": "invalid_json_or_value"})

    def log_message(self, fmt, *args):
        print("%s - %s" % (self.address_string(), fmt % args))

def main():
    # Render fournit PORT et exige une écoute sur toutes les interfaces.
    host = os.environ.get("GTA6_HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", os.environ.get("GTA6_PORT", "8080")))
    connect().close()
    print(f"GTA 6 Guide Radar disponible sur http://{host}:{port}")
    ThreadingHTTPServer((host, port), Handler).serve_forever()

if __name__ == "__main__":
    main()

from pathlib import Path
import os
import sqlite3

# Configure GTA6_DB_PATH to an absolute file path on a persistent mounted disk.
# GTA6_DATA_DIR is a convenient alternative directory setting. Without either,
# the repository-local data directory is used (ephemeral on Render Free).
_configured_db = os.environ.get("GTA6_DB_PATH", "").strip()
_configured_dir = os.environ.get("GTA6_DATA_DIR", "").strip()
if _configured_db:
    DB_PATH = Path(_configured_db).expanduser()
elif _configured_dir:
    DB_PATH = Path(_configured_dir).expanduser() / "gta6radar.sqlite3"
else:
    DB_PATH = Path(__file__).resolve().parent.parent / "data" / "gta6radar.sqlite3"

def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA busy_timeout = 5000")
    conn.execute("PRAGMA journal_mode = WAL")
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS robot_videos (
      id TEXT PRIMARY KEY,
      platform TEXT NOT NULL,
      url TEXT NOT NULL UNIQUE,
      title TEXT NOT NULL,
      creator TEXT NOT NULL DEFAULT '',
      status TEXT NOT NULL DEFAULT 'detected',
      rights_status TEXT NOT NULL DEFAULT 'unknown',
      transcript TEXT NOT NULL DEFAULT '',
      notes TEXT NOT NULL DEFAULT '',
      created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
      updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS robot_jobs (
      id TEXT PRIMARY KEY,
      video_id TEXT NOT NULL REFERENCES robot_videos(id) ON DELETE CASCADE,
      stage TEXT NOT NULL DEFAULT 'rights_check',
      status TEXT NOT NULL DEFAULT 'waiting',
      message TEXT NOT NULL DEFAULT '',
      created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
      updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS robot_evidence (
      id TEXT PRIMARY KEY,
      video_id TEXT NOT NULL REFERENCES robot_videos(id) ON DELETE CASCADE,
      timecode TEXT NOT NULL DEFAULT '',
      capture_path TEXT,
      transcript_excerpt TEXT NOT NULL DEFAULT '',
      description TEXT NOT NULL DEFAULT '',
      created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS robot_tips (
      id TEXT PRIMARY KEY,
      video_id TEXT NOT NULL REFERENCES robot_videos(id) ON DELETE CASCADE,
      title TEXT NOT NULL,
      category TEXT NOT NULL DEFAULT 'astuce',
      body TEXT NOT NULL DEFAULT '',
      status TEXT NOT NULL DEFAULT 'pending',
      confidence REAL,
      created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS sources (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      url TEXT NOT NULL UNIQUE,
      kind TEXT NOT NULL DEFAULT 'rss',
      enabled INTEGER NOT NULL DEFAULT 1,
      created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS items (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      source_id INTEGER REFERENCES sources(id),
      platform TEXT NOT NULL DEFAULT 'other',
      url TEXT NOT NULL UNIQUE,
      title TEXT NOT NULL,
      summary TEXT NOT NULL DEFAULT '',
      category TEXT NOT NULL DEFAULT 'to_classify',
      status TEXT NOT NULL DEFAULT 'unverified',
      published_at TEXT,
      collected_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS guide_entries (
      id TEXT PRIMARY KEY, slug TEXT NOT NULL UNIQUE, title TEXT NOT NULL,
      summary TEXT NOT NULL DEFAULT '', body TEXT NOT NULL DEFAULT '',
      category TEXT NOT NULL, platform TEXT NOT NULL DEFAULT 'both',
      status TEXT NOT NULL DEFAULT 'unverified', region TEXT, grid_ref TEXT,
      created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
      updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS map_markers (
      id TEXT PRIMARY KEY, title TEXT NOT NULL, description TEXT NOT NULL DEFAULT '',
      category TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'unverified',
      platform TEXT NOT NULL DEFAULT 'both', region TEXT, grid_ref TEXT,
      x REAL NOT NULL CHECK (x >= 0 AND x <= 100),
      y REAL NOT NULL CHECK (y >= 0 AND y <= 100),
      entry_id TEXT REFERENCES guide_entries(id) ON DELETE SET NULL,
      source_url TEXT, source_label TEXT, verified_at TEXT,
      created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
      updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    CREATE INDEX IF NOT EXISTS idx_robot_jobs_status ON robot_jobs(status, stage);
    CREATE INDEX IF NOT EXISTS idx_robot_videos_status ON robot_videos(status);
    """)
    conn.commit()
    return conn

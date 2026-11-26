PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS sources (
 id TEXT PRIMARY KEY, platform TEXT NOT NULL CHECK(platform IN ('youtube','tiktok','twitch','rss','manual','other')),
 name TEXT NOT NULL, base_url TEXT, access_mode TEXT NOT NULL DEFAULT 'manual',
 enabled INTEGER NOT NULL DEFAULT 1, credentials_ref TEXT, rights_note TEXT NOT NULL DEFAULT '',
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS source_accounts (
 id TEXT PRIMARY KEY, source_id TEXT NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
 external_account_id TEXT, handle TEXT, display_name TEXT NOT NULL, profile_url TEXT NOT NULL,
 consent_status TEXT NOT NULL DEFAULT 'unknown' CHECK(consent_status IN ('unknown','pending','granted','revoked','not_required')),
 enabled INTEGER NOT NULL DEFAULT 1, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 UNIQUE(source_id, external_account_id)
);
CREATE TABLE IF NOT EXISTS source_items (
 id TEXT PRIMARY KEY, source_id TEXT REFERENCES sources(id), account_id TEXT REFERENCES source_accounts(id),
 platform TEXT NOT NULL, external_id TEXT, url TEXT NOT NULL UNIQUE, title TEXT NOT NULL, creator TEXT,
 description TEXT NOT NULL DEFAULT '', published_at TEXT, duration_seconds INTEGER, language TEXT, thumbnail_url TEXT,
 access_status TEXT NOT NULL DEFAULT 'metadata_only' CHECK(access_status IN ('metadata_only','authorized_media','user_supplied','blocked','removed')),
 rights_status TEXT NOT NULL DEFAULT 'unknown' CHECK(rights_status IN ('unknown','allowed_analysis','creator_permission','user_owned','not_allowed')),
 discovered_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, last_seen_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS processing_jobs (
 id TEXT PRIMARY KEY, source_item_id TEXT NOT NULL REFERENCES source_items(id) ON DELETE CASCADE,
 stage TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'queued' CHECK(status IN ('queued','running','succeeded','failed','blocked','canceled')),
 attempts INTEGER NOT NULL DEFAULT 0, error_code TEXT, error_message TEXT, started_at TEXT, finished_at TEXT,
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS transcripts (
 id TEXT PRIMARY KEY, source_item_id TEXT NOT NULL REFERENCES source_items(id) ON DELETE CASCADE,
 language TEXT, provider TEXT NOT NULL, full_text TEXT NOT NULL DEFAULT '', rights_basis TEXT NOT NULL,
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS transcript_segments (
 id TEXT PRIMARY KEY, transcript_id TEXT NOT NULL REFERENCES transcripts(id) ON DELETE CASCADE,
 start_ms INTEGER NOT NULL, end_ms INTEGER NOT NULL, text TEXT NOT NULL, confidence REAL,
 CHECK(end_ms >= start_ms)
);
CREATE TABLE IF NOT EXISTS frame_captures (
 id TEXT PRIMARY KEY, source_item_id TEXT NOT NULL REFERENCES source_items(id) ON DELETE CASCADE,
 timestamp_ms INTEGER NOT NULL, storage_key TEXT, sha256 TEXT, frame_type TEXT NOT NULL DEFAULT 'candidate',
 description TEXT NOT NULL DEFAULT '', rights_basis TEXT NOT NULL, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS evidence (
 id TEXT PRIMARY KEY, source_item_id TEXT NOT NULL REFERENCES source_items(id),
 capture_id TEXT REFERENCES frame_captures(id) ON DELETE SET NULL,
 segment_id TEXT REFERENCES transcript_segments(id) ON DELETE SET NULL,
 start_ms INTEGER, end_ms INTEGER,
 evidence_type TEXT NOT NULL CHECK(evidence_type IN ('spoken','visual','metadata','creator_note','in_game_test','official')),
 excerpt TEXT NOT NULL DEFAULT '', confidence REAL, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS guide_entries (
 id TEXT PRIMARY KEY, slug TEXT NOT NULL UNIQUE, title TEXT NOT NULL, summary TEXT NOT NULL DEFAULT '',
 body TEXT NOT NULL DEFAULT '', category TEXT NOT NULL, platform TEXT NOT NULL DEFAULT 'both',
 verification_status TEXT NOT NULL DEFAULT 'observed_video',
 editorial_status TEXT NOT NULL DEFAULT 'pending' CHECK(editorial_status IN ('pending','needs_review','approved','rejected','published')),
 confidence REAL, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS guide_entry_evidence (
 guide_entry_id TEXT NOT NULL REFERENCES guide_entries(id) ON DELETE CASCADE,
 evidence_id TEXT NOT NULL REFERENCES evidence(id) ON DELETE CASCADE,
 PRIMARY KEY(guide_entry_id,evidence_id)
);
CREATE TABLE IF NOT EXISTS review_events (
 id TEXT PRIMARY KEY, guide_entry_id TEXT NOT NULL REFERENCES guide_entries(id) ON DELETE CASCADE,
 actor TEXT NOT NULL, action TEXT NOT NULL, note TEXT NOT NULL DEFAULT '', created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS map_markers (
 id TEXT PRIMARY KEY, guide_entry_id TEXT REFERENCES guide_entries(id) ON DELETE SET NULL,
 title TEXT NOT NULL, category TEXT NOT NULL, x REAL, y REAL, location_note TEXT NOT NULL DEFAULT '',
 evidence_id TEXT REFERENCES evidence(id), created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 CHECK((x IS NULL AND y IS NULL) OR (x BETWEEN 0 AND 100 AND y BETWEEN 0 AND 100))
);
CREATE INDEX IF NOT EXISTS idx_source_items_platform ON source_items(platform);
CREATE INDEX IF NOT EXISTS idx_jobs_status ON processing_jobs(status, stage);
CREATE INDEX IF NOT EXISTS idx_entries_editorial ON guide_entries(editorial_status, verification_status);
CREATE INDEX IF NOT EXISTS idx_segments_time ON transcript_segments(transcript_id,start_ms);

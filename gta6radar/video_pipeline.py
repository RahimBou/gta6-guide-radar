"""Validation helpers for the GTA 6 video-analysis pipeline.

No third-party video is downloaded here. Connectors must use official APIs,
RSS/embeds, creator-authorized media, or user-supplied files.
"""
from __future__ import annotations
from dataclasses import dataclass
from urllib.parse import urlparse
import hashlib
import uuid

ALLOWED_PLATFORMS = {"youtube", "tiktok", "twitch", "rss", "manual", "other"}

@dataclass(frozen=True)
class VideoCandidate:
    platform: str
    url: str
    title: str
    creator: str = ""
    external_id: str = ""
    description: str = ""
    published_at: str | None = None
    duration_seconds: int | None = None
    access_status: str = "metadata_only"
    rights_status: str = "unknown"

def validate_candidate(candidate: VideoCandidate) -> None:
    if candidate.platform not in ALLOWED_PLATFORMS:
        raise ValueError("unsupported_platform")
    parsed = urlparse(candidate.url)
    if parsed.scheme != "https" or not parsed.hostname:
        raise ValueError("https_url_required")
    if not candidate.title.strip():
        raise ValueError("title_required")
    if candidate.duration_seconds is not None and candidate.duration_seconds < 0:
        raise ValueError("invalid_duration")
    if candidate.access_status not in {"metadata_only", "authorized_media", "user_supplied", "blocked", "removed"}:
        raise ValueError("invalid_access_status")
    if candidate.rights_status not in {"unknown", "allowed_analysis", "creator_permission", "user_owned", "not_allowed"}:
        raise ValueError("invalid_rights_status")

def canonical_candidate_id(platform: str, url: str) -> str:
    raw = f"{platform}:{url.strip()}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:32]

def new_job_id() -> str:
    return str(uuid.uuid4())

def can_analyze_media(candidate: VideoCandidate) -> bool:
    return (
        candidate.access_status in {"authorized_media", "user_supplied"}
        and candidate.rights_status in {"allowed_analysis", "creator_permission", "user_owned"}
    )

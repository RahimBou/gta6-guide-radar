"""Local, evidence-first processing pipeline for GTA 6 Guide Radar.

This module turns an explicitly supplied, lawfully obtained transcript into
reviewable tip candidates. It does not download media or claim game verification.
"""
import re
import uuid
from .db import connect

CATEGORY_RULES = [
    ("mission", ("mission", "objectif", "chapitre", "walkthrough", "solution")),
    ("vehicle", ("voiture", "véhicule", "vehicle", "car", "garage", "moto")),
    ("secret", ("secret", "easter egg", "cache", "caché", "hidden", "mystère")),
    ("collectible", ("collectible", "objet", "ramasser", "collection", "100%")),
    ("location", ("lieu", "emplacement", "localisation", "map", "carte", "coordonnée")),
    ("combat", ("arme", "combat", "police", "poursuite", "tir", "weapon")),
]

def classify(text):
    low = text.lower()
    scores = [(category, sum(1 for word in words if word in low)) for category, words in CATEGORY_RULES]
    category, score = max(scores, key=lambda x: x[1])
    return category if score else "astuce"

def extract_candidates(transcript, max_candidates=12):
    """Split transcript into useful, reviewable evidence excerpts."""
    clean = re.sub(r"\s+", " ", str(transcript or "")).strip()
    if len(clean) < 80:
        return []
    # Prefer sentence boundaries; preserve exact source wording as evidence.
    sentences = re.split(r"(?<=[.!?])\s+(?=[A-ZÀ-ÖØ-Þ0-9])", clean)
    candidates = []
    seen = set()
    keywords = re.compile(
        r"\b(comment|pour|il faut|vous devez|astuce|secret|mission|emplacement|"
        r"trouver|récupérer|débloquer|aller|conduire|garage|arme|véhicule|"
        r"how to|you need|find|unlock|location|secret|mission|vehicle)\b", re.I
    )
    for sentence in sentences:
        sentence = sentence.strip(" -•")
        if len(sentence) < 55 or len(sentence) > 700 or not keywords.search(sentence):
            continue
        key = sentence.casefold()
        if key in seen:
            continue
        seen.add(key)
        candidates.append({
            "title": sentence[:110].rstrip(" .!?") or "Astuce à vérifier",
            "category": classify(sentence),
            "body": sentence,
            "confidence": 0.35,
        })
        if len(candidates) >= max_candidates:
            break
    return candidates

def process_video(video_id):
    conn = connect()
    try:
        video = conn.execute(
            "SELECT id,title,url,rights_status,transcript FROM robot_videos WHERE id=?",
            (video_id,)
        ).fetchone()
        if not video:
            return {"ok": False, "error": "video_not_found"}
        if video["rights_status"] not in ("owned", "licensed", "authorized", "public_text"):
            return {"ok": False, "error": "rights_not_cleared", "rights_status": video["rights_status"]}
        transcript = video["transcript"] or ""
        candidates = extract_candidates(transcript)
        if not candidates:
            return {"ok": False, "error": "transcript_has_no_extractable_candidates"}
        created = 0
        for item in candidates:
            exists = conn.execute(
                "SELECT 1 FROM robot_tips WHERE video_id=? AND title=?",
                (video_id, item["title"])
            ).fetchone()
            if exists:
                continue
            conn.execute("""
                INSERT INTO robot_tips(id,video_id,title,category,body,status,confidence)
                VALUES(?,?,?,?,?,'pending',?)
            """, (str(uuid.uuid4()), video_id, item["title"], item["category"],
                  item["body"], item["confidence"]))
            created += 1
        conn.execute(
            "UPDATE robot_videos SET status='analysed',updated_at=CURRENT_TIMESTAMP WHERE id=?",
            (video_id,)
        )
        conn.commit()
        return {"ok": True, "created": created, "candidates": len(candidates), "status": "pending_review"}
    finally:
        conn.close()

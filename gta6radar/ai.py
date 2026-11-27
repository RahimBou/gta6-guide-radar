"""OpenAI-compatible ASR and vision analysis for authorized local media only."""
import base64
import json
import mimetypes
import os
import urllib.error
import urllib.request
from pathlib import Path

API_BASE = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
ASR_MODEL = os.environ.get("GTA6_ASR_MODEL", "gpt-4o-mini-transcribe")
VISION_MODEL = os.environ.get("GTA6_VISION_MODEL", "gpt-4.1-mini")
MEDIA_DIR = Path(os.environ.get("GTA6_MEDIA_DIR", "/var/data/gta6-media")).expanduser().resolve()
MAX_AUDIO_BYTES = 24 * 1024 * 1024
MAX_IMAGE_BYTES = 8 * 1024 * 1024

class AIError(RuntimeError):
    pass

def _key():
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not key:
        raise AIError("OPENAI_API_KEY_missing")
    return key

def _safe_media_path(value, max_bytes):
    path = Path(str(value)).expanduser().resolve()
    try:
        path.relative_to(MEDIA_DIR)
    except ValueError:
        raise AIError("media_path_outside_GTA6_MEDIA_DIR")
    if not path.is_file():
        raise AIError("media_file_not_found")
    if path.stat().st_size > max_bytes:
        raise AIError("media_file_too_large")
    return path

def transcribe_audio(audio_path):
    path = _safe_media_path(audio_path, MAX_AUDIO_BYTES)
    boundary = "----GTA6RadarBoundary7MA4YWxkTrZu0gW"
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    fields = [
        ("model", ASR_MODEL),
        ("response_format", "verbose_json"),
        ("timestamp_granularities[]", "segment"),
    ]
    chunks = []
    for name, value in fields:
        chunks.extend([
            ("--" + boundary + "\r\n").encode(),
            ('Content-Disposition: form-data; name="' + name + '"\r\n\r\n').encode(),
            value.encode(), b"\r\n"
        ])
    chunks.extend([
        ("--" + boundary + "\r\n").encode(),
        ('Content-Disposition: form-data; name="file"; filename="' + path.name.replace('"', '') + '"\r\n').encode(),
        ("Content-Type: " + mime + "\r\n\r\n").encode(),
        path.read_bytes(), b"\r\n",
        ("--" + boundary + "--\r\n").encode()
    ])
    req = urllib.request.Request(
        API_BASE + "/audio/transcriptions", data=b"".join(chunks),
        headers={"Authorization": "Bearer " + _key(), "Content-Type": "multipart/form-data; boundary=" + boundary},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise AIError("ASR_provider_error_" + str(exc.code) + ":" + exc.read(1000).decode("utf-8", "replace"))
    transcript = str(result.get("text", "")).strip()
    if not transcript:
        raise AIError("empty_transcription")
    return {"text": transcript, "segments": result.get("segments", []), "language": result.get("language")}

def analyse_video(transcript, frame_paths):
    content = [{
        "type": "text",
        "text": (
            "Analyse ce contenu GTA VI. Sépare strictement ce qui est dit dans la transcription "
            "de ce qui est réellement visible dans les images. N'invente aucun lieu, mission, "
            "véhicule ni mécanisme. Retourne du JSON avec une clé tips contenant des objets "
            "{title,category,steps,location,confidence,evidence_text,visual_evidence}. "
            "Catégories autorisées: mission, vehicle, secret, collectible, location, combat, astuce. "
            "Si l'information est incertaine, indique confidence low et formule-la comme hypothèse. "
            "Transcription: " + str(transcript)[:18000]
        )
    }]
    for frame in frame_paths[:6]:
        path = _safe_media_path(frame, MAX_IMAGE_BYTES)
        mime = mimetypes.guess_type(path.name)[0] or "image/jpeg"
        encoded = base64.b64encode(path.read_bytes()).decode("ascii")
        content.append({"type": "image_url", "image_url": {"url": "data:" + mime + ";base64," + encoded}})
    payload = json.dumps({
        "model": VISION_MODEL,
        "messages": [{"role": "user", "content": content}],
        "response_format": {"type": "json_object"},
        "temperature": 0.1
    }).encode("utf-8")
    req = urllib.request.Request(
        API_BASE + "/chat/completions", data=payload,
        headers={"Authorization": "Bearer " + _key(), "Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise AIError("vision_provider_error_" + str(exc.code) + ":" + exc.read(1000).decode("utf-8", "replace"))
    raw = result["choices"][0]["message"]["content"]
    parsed = json.loads(raw)
    return parsed.get("tips", [])

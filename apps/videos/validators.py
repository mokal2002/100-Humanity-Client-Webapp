"""
Server-side YouTube URL validator and Video ID extractor.
Supports:
- https://www.youtube.com/watch?v=VIDEO_ID
- https://youtu.be/VIDEO_ID
- https://www.youtube.com/shorts/VIDEO_ID
Never accepts raw <iframe> HTML or non-YouTube domains.
"""
import re
from urllib.parse import parse_qs, urlparse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

YOUTUBE_VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")
ALLOWED_YOUTUBE_HOSTS = {
    "youtube.com",
    "www.youtube.com",
    "m.youtube.com",
    "youtu.be",
    "www.youtu.be",
}


def extract_youtube_video_id(url: str) -> str:
    """
    Validates a YouTube URL and extracts its 11-character video ID.
    Raises django.core.exceptions.ValidationError if the URL is invalid or unsafe.
    """
    if not url or not isinstance(url, str):
        raise ValidationError(_("Please provide a valid YouTube URL."))

    cleaned_url = url.strip()
    if "<" in cleaned_url or ">" in cleaned_url or "iframe" in cleaned_url.lower():
        raise ValidationError(
            _("Raw HTML or iframe code is not allowed. Please paste only the YouTube link.")
        )

    parsed = urlparse(cleaned_url)
    if parsed.scheme not in ("http", "https"):
        raise ValidationError(_("YouTube URL must start with https:// or http://."))

    host = (parsed.hostname or "").lower()
    if host not in ALLOWED_YOUTUBE_HOSTS:
        raise ValidationError(
            _("Only official YouTube URLs (youtube.com or youtu.be) are supported.")
        )

    video_id = ""
    path = parsed.path or ""

    if host in ("youtu.be", "www.youtu.be"):
        # Format: https://youtu.be/VIDEO_ID
        segments = [seg for seg in path.split("/") if seg]
        if segments:
            video_id = segments[0]
    else:
        if path == "/watch" or path.startswith("/watch/"):
            # Format: https://www.youtube.com/watch?v=VIDEO_ID
            qs = parse_qs(parsed.query)
            video_id = (qs.get("v") or [""])[0]
        elif path.startswith("/shorts/"):
            # Format: https://www.youtube.com/shorts/VIDEO_ID
            segments = [seg for seg in path.split("/") if seg]
            if len(segments) >= 2 and segments[0] == "shorts":
                video_id = segments[1]
        elif path.startswith("/embed/"):
            segments = [seg for seg in path.split("/") if seg]
            if len(segments) >= 2 and segments[0] == "embed":
                video_id = segments[1]

    if not video_id or not YOUTUBE_VIDEO_ID_RE.match(video_id):
        raise ValidationError(
            _(
                "Could not extract a valid 11-character YouTube Video ID. Supported formats: "
                "https://www.youtube.com/watch?v=VIDEO_ID, https://youtu.be/VIDEO_ID, "
                "or https://www.youtube.com/shorts/VIDEO_ID."
            )
        )

    return video_id

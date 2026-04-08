"""YouTubeShortsPublisher — real YouTube Data API v3 resumable upload.

This adapter is a **complete real implementation** when the three
OAuth2 env vars are set:

    YT_REFRESH_TOKEN   — long-lived refresh token for the target channel
    YT_CLIENT_ID       — OAuth client id
    YT_CLIENT_SECRET   — OAuth client secret

Flow (all via `httpx`, no `google-api-python-client` dependency):

    1. Exchange the refresh token for a fresh access token at
       `https://oauth2.googleapis.com/token` (grant_type=refresh_token).
    2. Initiate a resumable upload:
          POST https://www.googleapis.com/upload/youtube/v3/videos
              ?uploadType=resumable&part=snippet,status
          Authorization: Bearer <access_token>
          X-Upload-Content-Type: video/mp4
          Content-Type: application/json
          body: {snippet: {...}, status: {...}}
       The response `Location` header carries the session URI.
    3. PUT the video bytes at the session URI with
          Content-Type: video/mp4
       The final 200/201 response body is a video resource with an
       `id` field — that's the YouTube video id.

Category id 23 is YouTube's "Comedy" category (verified against the
public videoCategories list). The description has `#shorts` appended
so YouTube treats the upload as a Short.

If any of the env vars are missing the adapter reports
`is_available() == False` and `publish()` returns with `error` set
without touching the network. Same for any HTTP failure along the way.
"""
from __future__ import annotations

import json
import logging
import os
import time
from pathlib import Path
from typing import Any, Dict, Optional

from publishing.adapter import Publisher, PublishResult
from state.store import Sketch, Store


LOG = logging.getLogger("publishing.adapters.youtube_shorts")

TOKEN_URL = "https://oauth2.googleapis.com/token"
UPLOAD_URL = (
    "https://www.googleapis.com/upload/youtube/v3/videos"
    "?uploadType=resumable&part=snippet,status"
)
WATCH_URL_TEMPLATE = "https://www.youtube.com/watch?v={video_id}"

ENV_REFRESH = "YT_REFRESH_TOKEN"
ENV_CLIENT_ID = "YT_CLIENT_ID"
ENV_CLIENT_SECRET = "YT_CLIENT_SECRET"


def _refresh_access_token(httpx_mod: Any, timeout_sec: int = 30) -> str:
    """Exchange a refresh token for a fresh access token. Raises on failure."""
    resp = httpx_mod.post(
        TOKEN_URL,
        data={
            "client_id": os.environ[ENV_CLIENT_ID],
            "client_secret": os.environ[ENV_CLIENT_SECRET],
            "refresh_token": os.environ[ENV_REFRESH],
            "grant_type": "refresh_token",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=timeout_sec,
    )
    if resp.status_code != 200:
        raise RuntimeError(
            f"youtube token exchange status {resp.status_code}: {resp.text[:300]}"
        )
    payload = resp.json()
    token = payload.get("access_token")
    if not token:
        raise RuntimeError(f"youtube token response missing access_token: {payload}")
    return str(token)


class YouTubeShortsPublisher(Publisher):
    destination_id = "youtube_shorts"

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self.default_privacy: str = str(self.config.get("default_privacy", "private"))
        self.category_id: str = str(self.config.get("category_id", "23"))  # 23 = Comedy
        self.timeout_sec: int = int(self.config.get("timeout_sec", 300))
        self.chunk_size: int = int(self.config.get("chunk_size", 8 * 1024 * 1024))

    def is_available(self) -> bool:
        return all(
            os.environ.get(key) for key in (ENV_REFRESH, ENV_CLIENT_ID, ENV_CLIENT_SECRET)
        )

    # ----------------------------------------------------------------- helpers

    def _build_metadata(self, sketch: Sketch) -> Dict[str, Any]:
        premise = sketch.premise or {}
        title = str(premise.get("logline") or f"sketch {sketch.id}")[:100]
        synopsis = str(premise.get("synopsis") or "")
        tone = str(premise.get("tone") or "").strip()
        description_lines = [synopsis.strip()] if synopsis.strip() else []
        description_lines.append(f"Generated sketch: {sketch.id}")
        if tone:
            description_lines.append(f"Tone: {tone}")
        description_lines.append("")
        description_lines.append("#shorts #AIComedy")
        description = "\n".join(description_lines)[:5000]
        tags = ["ai", "comedy", "shorts"]
        if tone:
            tags.append(tone.replace(" ", "-")[:30])
        return {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": self.category_id,
            },
            "status": {
                "privacyStatus": self.default_privacy,
                "selfDeclaredMadeForKids": False,
            },
        }

    # ----------------------------------------------------------------- publish

    def publish(self, sketch: Sketch, store: Store) -> PublishResult:
        result = PublishResult(
            destination_id=self.destination_id,
            success=False,
        )
        if not self.is_available():
            result.error = (
                f"{ENV_REFRESH}/{ENV_CLIENT_ID}/{ENV_CLIENT_SECRET} not all set"
            )
            return result

        final_path = store.sketch_final_path(sketch.id)
        if not final_path.exists() or final_path.stat().st_size == 0:
            result.error = f"final.mp4 missing or empty: {final_path}"
            return result

        try:
            import httpx
        except ImportError as exc:
            result.error = f"httpx unavailable: {exc}"
            return result

        # Step 1: refresh the access token.
        try:
            access_token = _refresh_access_token(httpx)
        except Exception as exc:
            result.error = f"youtube token refresh failed: {exc}"
            return result

        metadata = self._build_metadata(sketch)

        # Step 2: initiate the resumable upload.
        try:
            init_resp = httpx.post(
                UPLOAD_URL,
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json; charset=UTF-8",
                    "X-Upload-Content-Type": "video/mp4",
                    "X-Upload-Content-Length": str(final_path.stat().st_size),
                },
                json=metadata,
                timeout=self.timeout_sec,
            )
        except Exception as exc:
            result.error = f"youtube init upload failed: {exc}"
            return result

        if init_resp.status_code != 200:
            result.error = (
                f"youtube init status {init_resp.status_code}: "
                f"{init_resp.text[:300]}"
            )
            return result

        session_uri = init_resp.headers.get("location") or init_resp.headers.get(
            "Location"
        )
        if not session_uri:
            result.error = "youtube init response missing Location header"
            return result

        # Step 3: PUT the video bytes. For simplicity we upload the
        # whole file in one request rather than streaming chunks —
        # Google documents both flows and single-request is fine for
        # Shorts (<= 60s).
        try:
            with final_path.open("rb") as handle:
                raw = handle.read()
            put_resp = httpx.put(
                session_uri,
                headers={
                    "Content-Type": "video/mp4",
                    "Content-Length": str(len(raw)),
                },
                content=raw,
                timeout=self.timeout_sec,
            )
        except Exception as exc:
            result.error = f"youtube upload PUT failed: {exc}"
            return result

        if put_resp.status_code not in (200, 201):
            result.error = (
                f"youtube upload status {put_resp.status_code}: "
                f"{put_resp.text[:300]}"
            )
            return result

        try:
            body = put_resp.json()
        except Exception as exc:
            result.error = f"youtube upload response json decode failed: {exc}"
            return result

        video_id = body.get("id") if isinstance(body, dict) else None
        if not video_id:
            result.error = f"youtube upload response missing id: {body}"
            return result

        result.success = True
        result.url = WATCH_URL_TEMPLATE.format(video_id=video_id)
        result.extra = {
            "video_id": video_id,
            "privacy_status": metadata["status"]["privacyStatus"],
            "category_id": metadata["snippet"]["categoryId"],
        }
        return result


__all__ = ["YouTubeShortsPublisher"]

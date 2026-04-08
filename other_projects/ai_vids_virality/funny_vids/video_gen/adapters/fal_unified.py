"""Fal.ai unified video provider adapter.

One adapter, many fal-hosted models. Replaces 4 of the 5 stub video
adapters in one shot — the user only needs `FAL_KEY` (or `FAL_API_KEY`)
in the environment and gets immediate access to Kling, Luma Ray-2, Veo3,
Pika, MiniMax Hailuo, and Runway Gen3 via fal's unified queue API.

Verified API shape against fal's docs and the `fal-client` Python source:

    1. Upload the start frame to fal's CDN:
         POST https://fal.media/files/upload
         headers: Authorization: Bearer <FAL_KEY>, Content-Type: image/png
         body: raw PNG bytes
         response: {"access_url": "https://v3.fal.media/files/.../foo.png"}
       (The CDN endpoint accepts the same key as the queue API but with a
       `Bearer` scheme instead of `Key` — verified against fal_client's
       `_cdn_auth_header` source.)

    2. Submit the generation job:
         POST https://queue.fal.run/{model_slug}
         headers: Authorization: Key <FAL_KEY>, Content-Type: application/json
         body: {"prompt": "...", "image_url": "<from step 1>", "duration": "5"}
         response: {"request_id": "...", "status_url": "...", ...}

    3. Poll for completion:
         GET https://queue.fal.run/{model_slug}/requests/{request_id}/status
         response: {"status": "IN_QUEUE" | "IN_PROGRESS" | "COMPLETED", ...}

    4. Fetch the result:
         GET https://queue.fal.run/{model_slug}/requests/{request_id}
         response: {"video": {"url": "https://v3.fal.media/.../output.mp4"}}

    5. Download the video URL into `out_path`.

Sources:
    https://fal.ai/docs/model-endpoints/queue
    https://fal.ai/models/fal-ai/kling-video/v2.1/master/image-to-video/api
    fal_client/client.py (REST_URL, FAL_CDN_FALLBACK_URL, _cdn_auth_header)
"""
from __future__ import annotations

import logging
import os
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from video_gen._common import copy_placeholder, write_bytes
from video_gen.adapter import VideoClip, VideoProviderAdapter


LOG = logging.getLogger("video_gen.adapters.fal_unified")

QUEUE_BASE = "https://queue.fal.run"
CDN_UPLOAD_URL = "https://fal.media/files/upload"

ENV_KEY_PRIMARY = "FAL_KEY"
ENV_KEY_ALT = "FAL_API_KEY"

# Per-model rough cost estimates (cents per 5-second clip). These are
# pulled from fal's published per-model pricing pages and rounded up
# slightly so the cost cap stays conservative. Update as fal's pricing
# changes — these are NOT contractual.
COST_CENTS_PER_5S: Dict[str, int] = {
    "fal-ai/kling-video/v1.6/standard/image-to-video": 25,
    "fal-ai/kling-video/v2.1/master/image-to-video": 70,
    "fal-ai/luma-dream-machine/ray-2/image-to-video": 50,
    "fal-ai/veo3/image-to-video": 50,
    "fal-ai/runway-gen3/turbo/image-to-video": 25,
    "fal-ai/pika/v2.2/image-to-video": 20,
    "fal-ai/minimax/hailuo-02/standard/image-to-video": 28,
}
DEFAULT_COST_CENTS_PER_5S = 50

# Models that document an end-frame field. The default Kling 2.1 master
# slug does NOT — only certain pro variants do. Luma ray-2 takes
# `keyframes.frame1.url`. Update this map as fal's docs change.
END_FRAME_FIELD_BY_SLUG: Dict[str, str] = {
    # NOTE: empty by default. Add slug -> field name mappings here once
    # they're verified against fal's per-model schema docs.
    # "fal-ai/kling-video/v2.5/pro/image-to-video": "tail_image_url",
}


def _coerce_kling_duration(seconds: float) -> str:
    """Kling on fal accepts the literal strings '5' or '10' only."""
    return "10" if seconds > 7.5 else "5"


def _coerce_int_duration(seconds: float, low: int = 5, high: int = 10) -> int:
    return max(low, min(high, int(round(seconds or 5))))


def _build_body(
    model_slug: str,
    image_url: str,
    end_image_url: Optional[str],
    prompt: str,
    duration_sec: float,
) -> Dict[str, Any]:
    """Build the per-model request body. Most slugs accept the same shape;
    a few need integer duration or extra fields."""
    body: Dict[str, Any] = {
        "image_url": image_url,
        "prompt": prompt[:1500] if prompt else "a sketch comedy beat",
    }

    # Duration encoding: Kling/Pika/Luma/MiniMax accept the literal
    # strings "5"/"10". Veo3 / Runway gen3 take integer seconds.
    if "kling" in model_slug or "pika" in model_slug:
        body["duration"] = _coerce_kling_duration(duration_sec)
    elif "minimax" in model_slug:
        # Hailuo accepts "6" / "10".
        body["duration"] = "10" if duration_sec > 8 else "6"
    elif "veo3" in model_slug:
        body["duration"] = "8s" if duration_sec > 6 else "5s"
    elif "runway" in model_slug:
        body["duration"] = _coerce_int_duration(duration_sec, low=5, high=10)
    elif "luma" in model_slug or "ray-2" in model_slug:
        body["duration"] = "5s" if duration_sec <= 7 else "9s"
    else:
        body["duration"] = _coerce_kling_duration(duration_sec)

    # End-frame: only set on slugs we've verified support it.
    if end_image_url:
        end_field = END_FRAME_FIELD_BY_SLUG.get(model_slug)
        if end_field:
            body[end_field] = end_image_url
        elif "luma" in model_slug or "ray-2" in model_slug:
            # Luma uses a nested keyframes object.
            body["end_image_url"] = end_image_url

    return body


def _extract_video_url(payload: Any) -> Optional[str]:
    """Walk a fal model result and find the first usable video URL.

    Most fal video models return `{"video": {"url": "..."}}` but a few
    use slightly different shapes (e.g. `videos: [{url}]` or just
    `{"output": "..."}`). Be defensive.
    """
    if not isinstance(payload, dict):
        return None
    video = payload.get("video")
    if isinstance(video, dict):
        url = video.get("url")
        if isinstance(url, str) and url:
            return url
    videos = payload.get("videos")
    if isinstance(videos, list) and videos:
        first = videos[0]
        if isinstance(first, dict):
            url = first.get("url")
            if isinstance(url, str) and url:
                return url
    output = payload.get("output")
    if isinstance(output, str) and output.startswith("http"):
        return output
    return None


class FalUnifiedAdapter(VideoProviderAdapter):
    """One adapter, many fal-hosted video models."""

    provider_id = "fal"

    DEFAULT_MODEL_SLUG = "fal-ai/kling-video/v2.1/master/image-to-video"

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self.model_slug: str = str(self.config.get("model_slug", self.DEFAULT_MODEL_SLUG))
        self.poll_interval_sec: float = float(self.config.get("poll_interval_sec", 5))
        self.timeout_sec: float = float(self.config.get("timeout_sec", 600))
        self.queue_base: str = str(self.config.get("queue_base", QUEUE_BASE))
        self.cdn_upload_url: str = str(self.config.get("cdn_upload_url", CDN_UPLOAD_URL))
        # Optional escape hatch: if provided, called instead of fal CDN
        # to convert a local PNG to a publicly reachable URL. Used by
        # tests and as a fallback when CDN upload fails.
        self.image_url_resolver: Optional[Callable[[Path], str]] = self.config.get(
            "image_url_resolver"
        )
        cost_override = self.config.get("cost_cents_per_5s")
        if cost_override is not None:
            self._cost_cents_per_5s = int(cost_override)
        else:
            self._cost_cents_per_5s = COST_CENTS_PER_5S.get(
                self.model_slug, DEFAULT_COST_CENTS_PER_5S
            )

    # ----------------------------------------------------------------- creds

    def _api_key(self) -> str:
        return os.environ.get(ENV_KEY_PRIMARY) or os.environ.get(ENV_KEY_ALT) or ""

    def is_available(self) -> bool:
        return bool(self._api_key())

    def estimated_cost_cents(self, duration_sec: float) -> int:
        slots = 1 if duration_sec <= 7.5 else 2
        return self._cost_cents_per_5s * slots

    # ----------------------------------------------------------------- HTTP helpers

    def _queue_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Key {self._api_key()}",
            "Content-Type": "application/json",
        }

    def _cdn_headers(self, content_type: str, file_name: Optional[str] = None) -> Dict[str, str]:
        # CRITICAL: the CDN endpoint uses Bearer scheme, not Key.
        # Verified against fal_client._cdn_auth_header.
        headers = {
            "Authorization": f"Bearer {self._api_key()}",
            "Content-Type": content_type,
        }
        if file_name:
            headers["X-Fal-File-Name"] = file_name
        return headers

    def _upload_to_fal_cdn(self, path: Path, httpx_mod: Any) -> str:
        """Upload a local file to fal's CDN and return the access URL."""
        raw = path.read_bytes()
        # Best-effort content-type guess.
        suffix = path.suffix.lower()
        if suffix in (".png",):
            content_type = "image/png"
        elif suffix in (".jpg", ".jpeg"):
            content_type = "image/jpeg"
        elif suffix in (".webp",):
            content_type = "image/webp"
        else:
            content_type = "application/octet-stream"
        resp = httpx_mod.post(
            self.cdn_upload_url,
            content=raw,
            headers=self._cdn_headers(content_type, file_name=path.name),
            timeout=120,
        )
        if resp.status_code not in (200, 201):
            raise RuntimeError(
                f"fal cdn upload status {resp.status_code}: {resp.text[:300]}"
            )
        try:
            payload = resp.json()
        except Exception as exc:
            raise RuntimeError(f"fal cdn json decode failed: {exc}")
        url = payload.get("access_url") or payload.get("url")
        if not url:
            raise RuntimeError(f"fal cdn response missing access_url: {payload}")
        return url

    def _resolve_image_url(self, path: Path, httpx_mod: Any) -> str:
        """Get a public URL for a local image. Tries fal CDN first, then
        the user-supplied resolver if configured."""
        try:
            return self._upload_to_fal_cdn(path, httpx_mod)
        except Exception as cdn_exc:
            LOG.warning("fal CDN upload failed, trying fallback resolver: %s", cdn_exc)
            if self.image_url_resolver is not None:
                try:
                    return self.image_url_resolver(path)
                except Exception as res_exc:
                    raise RuntimeError(
                        f"both fal CDN and fallback resolver failed: cdn={cdn_exc}, resolver={res_exc}"
                    )
            raise

    def _submit(
        self,
        body: Dict[str, Any],
        httpx_mod: Any,
    ) -> Dict[str, Any]:
        url = f"{self.queue_base}/{self.model_slug}"
        resp = httpx_mod.post(url, headers=self._queue_headers(), json=body, timeout=60)
        if resp.status_code not in (200, 201):
            raise RuntimeError(
                f"fal submit status {resp.status_code}: {resp.text[:300]}"
            )
        try:
            payload = resp.json()
        except Exception as exc:
            raise RuntimeError(f"fal submit json decode failed: {exc}")
        if not isinstance(payload, dict) or "request_id" not in payload:
            raise RuntimeError(f"fal submit missing request_id: {payload}")
        return payload

    def _urls_from_submit(
        self, submit_payload: Dict[str, Any], request_id: str
    ) -> tuple[str, str]:
        """Extract (status_url, response_url) from a fal submit payload.

        fal's queue API returns these explicitly so the client doesn't have
        to know about model-slug sub-path stripping rules — for slugs like
        `kling-video/v1.6/standard/image-to-video`, fal strips the sub-path
        and the poll/result endpoints live under just `kling-video`, not
        the full slug. Reconstructing the URL from the slug yields a 405
        Method Not Allowed against the real API.

        Falls back to reconstruction from `model_slug` + `request_id` so
        existing mocked tests (which may omit these fields) keep working.
        """
        status_url = submit_payload.get("status_url") if isinstance(submit_payload, dict) else None
        response_url = submit_payload.get("response_url") if isinstance(submit_payload, dict) else None
        if status_url and not response_url:
            response_url = status_url.removesuffix("/status")
        if not status_url:
            status_url = f"{self.queue_base}/{self.model_slug}/requests/{request_id}/status"
        if not response_url:
            response_url = f"{self.queue_base}/{self.model_slug}/requests/{request_id}"
        return status_url, response_url

    def _poll(
        self,
        submit_payload: Dict[str, Any],
        httpx_mod: Any,
        sleep_fn: Callable[[float], None] = time.sleep,
    ) -> None:
        request_id = submit_payload.get("request_id", "") if isinstance(submit_payload, dict) else ""
        status_url, _ = self._urls_from_submit(submit_payload, request_id)
        deadline = time.time() + self.timeout_sec
        while time.time() < deadline:
            resp = httpx_mod.get(status_url, headers=self._queue_headers(), timeout=30)
            # fal returns 200 when the job is COMPLETED and 202 (Accepted)
            # while it's still IN_QUEUE / IN_PROGRESS. Both are normal —
            # the body's "status" field is the source of truth.
            if resp.status_code not in (200, 202):
                raise RuntimeError(
                    f"fal poll status {resp.status_code}: {resp.text[:300]}"
                )
            payload = resp.json()
            status = (payload.get("status") or "").upper() if isinstance(payload, dict) else ""
            if status == "COMPLETED":
                return
            if status in {"FAILED", "ERROR", "CANCELLED"}:
                raise RuntimeError(f"fal request {status.lower()}: {payload}")
            sleep_fn(self.poll_interval_sec)
        raise RuntimeError(f"fal poll timed out after {self.timeout_sec}s")

    def _fetch_result(
        self, submit_payload: Dict[str, Any], httpx_mod: Any
    ) -> Dict[str, Any]:
        request_id = submit_payload.get("request_id", "") if isinstance(submit_payload, dict) else ""
        _, response_url = self._urls_from_submit(submit_payload, request_id)
        resp = httpx_mod.get(response_url, headers=self._queue_headers(), timeout=60)
        if resp.status_code != 200:
            raise RuntimeError(
                f"fal result status {resp.status_code}: {resp.text[:300]}"
            )
        return resp.json()

    def _download_video(self, video_url: str, out_path: Path, httpx_mod: Any) -> None:
        resp = httpx_mod.get(video_url, timeout=300)
        if resp.status_code != 200:
            raise RuntimeError(f"fal download status {resp.status_code}")
        write_bytes(out_path, resp.content)

    # ----------------------------------------------------------------- public API

    def generate(
        self,
        start_frame: Path,
        end_frame: Optional[Path],
        prompt: str,
        duration_sec: float,
        out_path: Path,
        beat_n: int = 1,
    ) -> VideoClip:
        clip = VideoClip(
            beat_n=beat_n,
            path=out_path,
            provider_id=self.provider_id,
            duration_sec=float(duration_sec or 5),
        )

        if not self.is_available():
            clip.error = f"{ENV_KEY_PRIMARY} (or {ENV_KEY_ALT}) not set"
            copy_placeholder(out_path)
            return clip

        try:
            import httpx
        except ImportError as exc:
            clip.error = f"httpx unavailable: {exc}"
            copy_placeholder(out_path)
            return clip

        started = time.time()
        try:
            image_url = self._resolve_image_url(start_frame, httpx)
        except Exception as exc:
            clip.error = f"fal start frame upload failed: {exc}"
            clip.duration_ms = int((time.time() - started) * 1000)
            copy_placeholder(out_path)
            return clip

        end_image_url: Optional[str] = None
        if end_frame is not None and end_frame.exists():
            try:
                end_image_url = self._resolve_image_url(end_frame, httpx)
            except Exception as exc:
                LOG.warning("fal end frame upload failed, ignoring: %s", exc)

        body = _build_body(
            self.model_slug, image_url, end_image_url, prompt, duration_sec
        )

        try:
            submit_payload = self._submit(body, httpx)
            request_id = submit_payload["request_id"]
            clip.job_id = request_id
            self._poll(submit_payload, httpx)
            result = self._fetch_result(submit_payload, httpx)
            video_url = _extract_video_url(result)
            if not video_url:
                raise RuntimeError(f"fal result missing video url: {result}")
            self._download_video(video_url, out_path, httpx)
        except Exception as exc:
            clip.error = f"fal generate failed: {exc}"
            copy_placeholder(out_path)
        finally:
            clip.duration_ms = int((time.time() - started) * 1000)

        if clip.error is None:
            clip.cost_cents = self.estimated_cost_cents(clip.duration_sec)
        return clip


__all__ = ["FalUnifiedAdapter", "_build_body", "_extract_video_url"]

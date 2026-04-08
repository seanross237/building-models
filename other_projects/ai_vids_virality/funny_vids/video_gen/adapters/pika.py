"""Pika video provider adapter (via fal.ai).

In 2026 Pika's official public API is hosted on fal.ai. We call the
queue-based REST endpoints directly:

    POST  https://queue.fal.run/fal-ai/pika/v2.2/image-to-video
        headers: Authorization: Key <FAL_KEY>
        body: { image_url, prompt, duration, resolution, seed?, negative_prompt? }
        -> 200 { request_id }

    GET   https://queue.fal.run/fal-ai/pika/requests/{request_id}/status
        -> { status: "IN_QUEUE" | "IN_PROGRESS" | "COMPLETED", ... }

    GET   https://queue.fal.run/fal-ai/pika/requests/{request_id}
        -> { video: { url } }

`image_url` accepts either a public HTTPS URL or a `data:image/png;base64,...`
data URI.

Verified against:
    https://fal.ai/models/fal-ai/pika/v2.2/image-to-video/api
    https://blog.fal.ai/pika-api-is-now-powered-by-fal/
"""
from __future__ import annotations

import logging
import os
import time
from pathlib import Path
from typing import Any, Dict, Optional

from video_gen._common import base64_file, copy_placeholder, write_bytes
from video_gen.adapter import VideoClip, VideoProviderAdapter


LOG = logging.getLogger("video_gen.adapters.pika")

QUEUE_BASE = "https://queue.fal.run"
SUBMIT_PATH = "/fal-ai/pika/v2.2/image-to-video"
STATUS_PATH = "/fal-ai/pika/requests/{request_id}/status"
RESULT_PATH = "/fal-ai/pika/requests/{request_id}"

ENV_KEY = "FAL_KEY"
ENV_KEY_ALT = "PIKA_API_KEY"  # accept either name


def _coerce_duration(seconds: float) -> int:
    """Pika 2.2 accepts 5 or 10 second clips."""
    return 5 if seconds <= 7.5 else 10


def _coerce_resolution(value: str) -> str:
    if value not in ("720p", "1080p"):
        return "720p"
    return value


class PikaAdapter(VideoProviderAdapter):
    provider_id = "pika"

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self.resolution: str = _coerce_resolution(str(self.config.get("resolution", "720p")))
        self.poll_interval_sec: float = float(self.config.get("poll_interval_sec", 5))
        self.timeout_sec: float = float(self.config.get("timeout_sec", 600))
        self.api_base: str = str(self.config.get("api_base", QUEUE_BASE))
        # 5s/720p ~= 20 cents, 5s/1080p ~= 45 cents per fal pricing.
        self.cost_cents_per_5s: int = int(
            self.config.get("cost_cents_per_5s", 45 if self.resolution == "1080p" else 20)
        )

    def _api_key(self) -> str:
        return os.environ.get(ENV_KEY) or os.environ.get(ENV_KEY_ALT) or ""

    def is_available(self) -> bool:
        return bool(self._api_key())

    def estimated_cost_cents(self, duration_sec: float) -> int:
        return self.cost_cents_per_5s * (1 if duration_sec <= 7.5 else 2)

    # ----------------------------------------------------------------- HTTP

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Key {self._api_key()}",
            "Content-Type": "application/json",
        }

    def _submit(self, body: Dict[str, Any], httpx_mod: Any) -> str:
        url = self.api_base + SUBMIT_PATH
        resp = httpx_mod.post(url, headers=self._headers(), json=body, timeout=60)
        if resp.status_code not in (200, 201):
            raise RuntimeError(f"pika submit status {resp.status_code}: {resp.text[:300]}")
        payload = resp.json()
        request_id = payload.get("request_id")
        if not request_id:
            raise RuntimeError(f"pika submit missing request_id: {payload}")
        return request_id

    def _poll(
        self,
        request_id: str,
        httpx_mod: Any,
        sleep_fn: Any = time.sleep,
    ) -> None:
        deadline = time.time() + self.timeout_sec
        url = self.api_base + STATUS_PATH.format(request_id=request_id)
        while time.time() < deadline:
            resp = httpx_mod.get(url, headers=self._headers(), timeout=30)
            if resp.status_code != 200:
                raise RuntimeError(f"pika poll status {resp.status_code}: {resp.text[:300]}")
            payload = resp.json()
            status = (payload.get("status") or "").upper()
            if status == "COMPLETED":
                return
            if status in {"FAILED", "ERROR", "CANCELLED"}:
                raise RuntimeError(f"pika request {status.lower()}: {payload}")
            sleep_fn(self.poll_interval_sec)
        raise RuntimeError(f"pika poll timed out after {self.timeout_sec}s")

    def _fetch_result(self, request_id: str, httpx_mod: Any) -> Dict[str, Any]:
        url = self.api_base + RESULT_PATH.format(request_id=request_id)
        resp = httpx_mod.get(url, headers=self._headers(), timeout=60)
        if resp.status_code != 200:
            raise RuntimeError(f"pika result status {resp.status_code}: {resp.text[:300]}")
        return resp.json()

    def _download(self, video_url: str, out_path: Path, httpx_mod: Any) -> None:
        resp = httpx_mod.get(video_url, timeout=120)
        if resp.status_code != 200:
            raise RuntimeError(f"pika download status {resp.status_code}")
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
            clip.error = f"{ENV_KEY} (or {ENV_KEY_ALT}) not set"
            copy_placeholder(out_path)
            return clip

        try:
            import httpx
        except ImportError as exc:
            clip.error = f"httpx unavailable: {exc}"
            copy_placeholder(out_path)
            return clip

        body: Dict[str, Any] = {
            "image_url": f"data:image/png;base64,{base64_file(start_frame)}",
            "prompt": (prompt or "")[:1000],
            "duration": _coerce_duration(duration_sec),
            "resolution": self.resolution,
        }
        # Pika 2.2 image-to-video does not currently expose end_frame; we
        # ignore it. Phase 6+ may need to switch to Pikaframes for that.

        started = time.time()
        try:
            request_id = self._submit(body, httpx)
            clip.job_id = request_id
            self._poll(request_id, httpx)
            result = self._fetch_result(request_id, httpx)
            video = result.get("video") if isinstance(result, dict) else None
            if not isinstance(video, dict):
                raise RuntimeError(f"pika result missing video object: {result}")
            video_url = video.get("url")
            if not video_url:
                raise RuntimeError(f"pika video missing url: {video}")
            self._download(video_url, out_path, httpx)
        except Exception as exc:
            clip.error = f"pika generate failed: {exc}"
            copy_placeholder(out_path)
        finally:
            clip.duration_ms = int((time.time() - started) * 1000)

        if clip.error is None:
            clip.cost_cents = self.estimated_cost_cents(clip.duration_sec)
        return clip


__all__ = ["PikaAdapter"]

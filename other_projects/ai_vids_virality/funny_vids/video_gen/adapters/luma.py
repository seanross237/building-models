"""Luma Dream Machine video provider adapter.

Real implementation against the official Luma API:

    POST https://api.lumalabs.ai/dream-machine/v1/generations/video
        body: { prompt, model, aspect_ratio, duration, keyframes: {
                 frame0: { type: "image", url }, frame1?: { ... } } }
    GET  https://api.lumalabs.ai/dream-machine/v1/generations/{id}
        response: { id, state, assets?: { video } }

Auth: `Authorization: Bearer <LUMA_API_KEY>`.

Limitation: Luma's keyframes.frame0.url must be a publicly reachable HTTPS
URL. This adapter expects the caller to pass an `image_url_resolver` in
the config that uploads the local PNG somewhere reachable and returns the
URL. If no resolver is configured, the adapter falls back to passing the
local file path as a `file://` URL — which Luma will reject — and the
adapter will return cleanly with `error` set. The intention is that a
later phase wires in cloud storage (S3/GCS).

Verified against:
    https://github.com/lumalabs/lumaai-api/blob/main/openapi.yaml
"""
from __future__ import annotations

import logging
import os
import time
from pathlib import Path
from typing import Any, Callable, Dict, Optional

from video_gen._common import copy_placeholder, write_bytes
from video_gen.adapter import VideoClip, VideoProviderAdapter


LOG = logging.getLogger("video_gen.adapters.luma")

API_BASE = "https://api.lumalabs.ai/dream-machine/v1"
SUBMIT_PATH = "/generations/video"
QUERY_PATH = "/generations"  # /{id}

ENV_KEY = "LUMA_API_KEY"


def _coerce_duration(seconds: float) -> str:
    """Luma's video models accept `5s` or `9s` per the OpenAPI spec."""
    if seconds <= 7:
        return "5s"
    return "9s"


class LumaAdapter(VideoProviderAdapter):
    provider_id = "luma"

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self.model: str = str(self.config.get("model", "ray-2"))
        self.aspect_ratio: str = str(self.config.get("aspect_ratio", "16:9"))
        self.poll_interval_sec: float = float(self.config.get("poll_interval_sec", 5))
        self.timeout_sec: float = float(self.config.get("timeout_sec", 600))
        self.api_base: str = str(self.config.get("api_base", API_BASE))
        self.cost_cents_per_5s: int = int(self.config.get("cost_cents_per_5s", 70))
        # Optional callable that uploads a local PNG and returns its public URL.
        self.image_url_resolver: Optional[Callable[[Path], str]] = self.config.get(
            "image_url_resolver"
        )

    def is_available(self) -> bool:
        return bool(os.environ.get(ENV_KEY))

    def estimated_cost_cents(self, duration_sec: float) -> int:
        return self.cost_cents_per_5s * (1 if duration_sec <= 7 else 2)

    # ----------------------------------------------------------------- HTTP

    def _auth_header(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {os.environ.get(ENV_KEY, '')}",
            "Content-Type": "application/json",
        }

    def _resolve_url(self, frame: Path) -> str:
        if self.image_url_resolver is not None:
            return self.image_url_resolver(frame)
        # Fallback: local file URL — Luma will reject it, which is fine.
        # The adapter will catch the error and return cleanly.
        return f"file://{frame.resolve()}"

    def _submit(self, body: Dict[str, Any], httpx_mod: Any) -> Dict[str, Any]:
        url = self.api_base + SUBMIT_PATH
        resp = httpx_mod.post(url, headers=self._auth_header(), json=body, timeout=60)
        if resp.status_code not in (200, 201):
            raise RuntimeError(f"luma submit status {resp.status_code}: {resp.text[:300]}")
        payload = resp.json()
        if not isinstance(payload, dict) or "id" not in payload:
            raise RuntimeError(f"luma submit missing id: {payload}")
        return payload

    def _poll(self, generation_id: str, httpx_mod: Any, sleep_fn: Any = time.sleep) -> Dict[str, Any]:
        deadline = time.time() + self.timeout_sec
        url = f"{self.api_base}{QUERY_PATH}/{generation_id}"
        while time.time() < deadline:
            resp = httpx_mod.get(url, headers=self._auth_header(), timeout=30)
            if resp.status_code != 200:
                raise RuntimeError(f"luma poll status {resp.status_code}: {resp.text[:300]}")
            payload = resp.json()
            state = payload.get("state")
            if state == "completed":
                return payload
            if state == "failed":
                raise RuntimeError(
                    f"luma generation failed: {payload.get('failure_reason', 'unknown')}"
                )
            sleep_fn(self.poll_interval_sec)
        raise RuntimeError(f"luma poll timed out after {self.timeout_sec}s")

    def _download(self, video_url: str, out_path: Path, httpx_mod: Any) -> None:
        resp = httpx_mod.get(video_url, timeout=120)
        if resp.status_code != 200:
            raise RuntimeError(f"luma download status {resp.status_code}")
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
            clip.error = f"{ENV_KEY} not set"
            copy_placeholder(out_path)
            return clip

        try:
            import httpx
        except ImportError as exc:
            clip.error = f"httpx unavailable: {exc}"
            copy_placeholder(out_path)
            return clip

        try:
            frame0_url = self._resolve_url(start_frame)
        except Exception as exc:
            clip.error = f"luma image_url_resolver failed: {exc}"
            copy_placeholder(out_path)
            return clip

        body: Dict[str, Any] = {
            "model": self.model,
            "aspect_ratio": self.aspect_ratio,
            "duration": _coerce_duration(duration_sec),
            "keyframes": {
                "frame0": {"type": "image", "url": frame0_url},
            },
        }
        if prompt:
            body["prompt"] = prompt[:1000]
        if end_frame is not None and end_frame.exists():
            try:
                frame1_url = self._resolve_url(end_frame)
                body["keyframes"]["frame1"] = {"type": "image", "url": frame1_url}
            except Exception as exc:
                LOG.warning("luma end_frame resolve failed, continuing without it: %s", exc)

        started = time.time()
        try:
            submit = self._submit(body, httpx)
            generation_id = submit["id"]
            clip.job_id = generation_id
            done = self._poll(generation_id, httpx)
            assets = done.get("assets") or {}
            video_url = assets.get("video")
            if not video_url:
                raise RuntimeError("luma response had no video asset")
            self._download(video_url, out_path, httpx)
        except Exception as exc:
            clip.error = f"luma generate failed: {exc}"
            copy_placeholder(out_path)
        finally:
            clip.duration_ms = int((time.time() - started) * 1000)

        if clip.error is None:
            clip.cost_cents = self.estimated_cost_cents(clip.duration_sec)
        return clip


__all__ = ["LumaAdapter"]

"""Runway video provider adapter.

Real implementation against the official Runway dev API:

    POST https://api.dev.runwayml.com/v1/image_to_video
        headers: Authorization: Bearer <key>, X-Runway-Version: 2024-11-06
        body: { model, promptImage, ratio, duration, promptText? }
    GET  https://api.dev.runwayml.com/v1/tasks/{id}
        response: { id, status, output?: [url, ...] }

`promptImage` accepts either an https URL or a `data:image/png;base64,...`
data URI. We send a data URI so the local PNG works without an external
host.

Verified against the runwayml/sdk-python source:
    src/runwayml/_client.py     (base_url + auth + X-Runway-Version)
    src/runwayml/resources/image_to_video.py    (POST /v1/image_to_video)
    src/runwayml/resources/tasks.py             (GET /v1/tasks/{id})
    src/runwayml/types/task_retrieve_response.py (Succeeded.output: List[str])
"""
from __future__ import annotations

import logging
import os
import time
from pathlib import Path
from typing import Any, Dict, Optional

from video_gen._common import base64_file, copy_placeholder, write_bytes
from video_gen.adapter import VideoClip, VideoProviderAdapter


LOG = logging.getLogger("video_gen.adapters.runway")

API_BASE = "https://api.dev.runwayml.com"
SUBMIT_PATH = "/v1/image_to_video"
QUERY_PATH = "/v1/tasks"  # /{id}
RUNWAY_VERSION = "2024-11-06"

ENV_KEY = "RUNWAY_API_KEY"


def _coerce_duration(seconds: float) -> int:
    """Runway gen-4 accepts integer seconds in 2..10."""
    return max(2, min(10, int(round(seconds or 5))))


class RunwayAdapter(VideoProviderAdapter):
    provider_id = "runway"

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self.model: str = str(self.config.get("model", "gen4_turbo"))
        self.ratio: str = str(self.config.get("ratio", "1280:720"))
        self.poll_interval_sec: float = float(self.config.get("poll_interval_sec", 5))
        self.timeout_sec: float = float(self.config.get("timeout_sec", 600))
        self.api_base: str = str(self.config.get("api_base", API_BASE))
        self.cost_cents_per_5s: int = int(self.config.get("cost_cents_per_5s", 100))

    def is_available(self) -> bool:
        return bool(os.environ.get(ENV_KEY))

    def estimated_cost_cents(self, duration_sec: float) -> int:
        slots = max(1, int(round((duration_sec or 5) / 5)))
        return self.cost_cents_per_5s * slots

    # ----------------------------------------------------------------- HTTP

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {os.environ.get(ENV_KEY, '')}",
            "X-Runway-Version": RUNWAY_VERSION,
            "Content-Type": "application/json",
        }

    def _submit(self, body: Dict[str, Any], httpx_mod: Any) -> Dict[str, Any]:
        url = self.api_base + SUBMIT_PATH
        resp = httpx_mod.post(url, headers=self._headers(), json=body, timeout=60)
        if resp.status_code not in (200, 201):
            raise RuntimeError(f"runway submit status {resp.status_code}: {resp.text[:300]}")
        payload = resp.json()
        if not isinstance(payload, dict) or "id" not in payload:
            raise RuntimeError(f"runway submit missing id: {payload}")
        return payload

    def _poll(self, task_id: str, httpx_mod: Any, sleep_fn: Any = time.sleep) -> Dict[str, Any]:
        deadline = time.time() + self.timeout_sec
        url = f"{self.api_base}{QUERY_PATH}/{task_id}"
        while time.time() < deadline:
            resp = httpx_mod.get(url, headers=self._headers(), timeout=30)
            if resp.status_code != 200:
                raise RuntimeError(f"runway poll status {resp.status_code}: {resp.text[:300]}")
            payload = resp.json()
            status = (payload.get("status") or "").upper()
            if status == "SUCCEEDED":
                return payload
            if status in {"FAILED", "CANCELLED"}:
                raise RuntimeError(f"runway task {status.lower()}: {payload}")
            sleep_fn(self.poll_interval_sec)
        raise RuntimeError(f"runway poll timed out after {self.timeout_sec}s")

    def _download(self, video_url: str, out_path: Path, httpx_mod: Any) -> None:
        resp = httpx_mod.get(video_url, timeout=120)
        if resp.status_code != 200:
            raise RuntimeError(f"runway download status {resp.status_code}")
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

        # Runway accepts a data URI for promptImage.
        prompt_image = f"data:image/png;base64,{base64_file(start_frame)}"
        body: Dict[str, Any] = {
            "model": self.model,
            "promptImage": prompt_image,
            "ratio": self.ratio,
            "duration": _coerce_duration(duration_sec),
        }
        if prompt:
            body["promptText"] = prompt[:1000]
        if end_frame is not None and end_frame.exists():
            # Runway gen-4 supports an end-frame via the same promptImage
            # field with a `position: "last"` object form. We send both as
            # an array per the 2024-11-06 spec.
            body["promptImage"] = [
                {"uri": prompt_image, "position": "first"},
                {
                    "uri": f"data:image/png;base64,{base64_file(end_frame)}",
                    "position": "last",
                },
            ]

        started = time.time()
        try:
            submit = self._submit(body, httpx)
            task_id = submit["id"]
            clip.job_id = task_id
            done = self._poll(task_id, httpx)
            output = done.get("output") or []
            if not output:
                raise RuntimeError("runway response had no output URLs")
            video_url = output[0] if isinstance(output[0], str) else None
            if not video_url:
                raise RuntimeError(f"runway output[0] was not a URL: {output[0]}")
            self._download(video_url, out_path, httpx)
        except Exception as exc:
            clip.error = f"runway generate failed: {exc}"
            copy_placeholder(out_path)
        finally:
            clip.duration_ms = int((time.time() - started) * 1000)

        if clip.error is None:
            clip.cost_cents = self.estimated_cost_cents(clip.duration_sec)
        return clip


__all__ = ["RunwayAdapter"]

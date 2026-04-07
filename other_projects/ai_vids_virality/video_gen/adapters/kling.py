"""Kling video provider adapter.

Real implementation against the official Kling API:

    POST https://api.klingai.com/v1/videos/image2video
        body: { model_name, image (base64 or URL), image_tail?, prompt,
                 negative_prompt?, cfg_scale?, mode, duration }
    GET  https://api.klingai.com/v1/videos/image2video/{task_id}
        response: { code, data: { task_id, task_status, task_result?: {
                     videos: [{ url, duration }] } } }

Auth is JWT (HS256) with the payload:
    { "iss": <AccessKey>, "exp": now+1800, "nbf": now-5 }
signed with the SecretKey. The token is sent as
`Authorization: Bearer <jwt>`. We require both `KLING_AK` and `KLING_SK`
to be set in the environment to consider the adapter available.

Verified against:
    https://github.com/betasecond/KlingDemo/blob/main/APIDoc.md
    https://github.com/betasecond/KlingDemo/blob/main/APIDoc_Auth.md
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import json as _json
import logging
import os
import time
from pathlib import Path
from typing import Any, Dict, Optional

from video_gen._common import base64_file, copy_placeholder, write_bytes
from video_gen.adapter import VideoClip, VideoProviderAdapter


LOG = logging.getLogger("video_gen.adapters.kling")

API_BASE = "https://api.klingai.com"
SUBMIT_PATH = "/v1/videos/image2video"
QUERY_PATH = "/v1/videos/image2video"  # /{task_id}

ENV_AK = "KLING_AK"
ENV_SK = "KLING_SK"


def _b64url(raw: bytes) -> bytes:
    return base64.urlsafe_b64encode(raw).rstrip(b"=")


def make_jwt(access_key: str, secret_key: str, ttl_sec: int = 1800) -> str:
    """Build a Kling JWT (HS256) from an AccessKey/SecretKey pair.

    The Kling API expects the AccessKey as the `iss` claim, an `exp` set
    to now + ttl, and an `nbf` set to now - 5 to absorb clock skew.
    """
    header = {"alg": "HS256", "typ": "JWT"}
    now = int(time.time())
    payload = {
        "iss": access_key,
        "exp": now + int(ttl_sec),
        "nbf": now - 5,
    }
    header_b64 = _b64url(_json.dumps(header, separators=(",", ":")).encode("utf-8"))
    payload_b64 = _b64url(_json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    signing_input = header_b64 + b"." + payload_b64
    signature = hmac.new(secret_key.encode("utf-8"), signing_input, hashlib.sha256).digest()
    sig_b64 = _b64url(signature)
    return (signing_input + b"." + sig_b64).decode("ascii")


def _coerce_duration(seconds: float) -> str:
    """Kling only supports `5` or `10` second clips. Round to nearest."""
    if seconds <= 7.5:
        return "5"
    return "10"


class KlingAdapter(VideoProviderAdapter):
    provider_id = "kling"

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self.model_name: str = str(self.config.get("model", "kling-v1-6"))
        self.mode: str = str(self.config.get("mode", "std"))
        self.cfg_scale: float = float(self.config.get("cfg_scale", 0.5))
        self.poll_interval_sec: float = float(self.config.get("poll_interval_sec", 5))
        self.timeout_sec: float = float(self.config.get("timeout_sec", 600))
        self.api_base: str = str(self.config.get("api_base", API_BASE))
        self.cost_cents_per_5s: int = int(self.config.get("cost_cents_per_5s", 50))

    def is_available(self) -> bool:
        return bool(os.environ.get(ENV_AK) and os.environ.get(ENV_SK))

    def estimated_cost_cents(self, duration_sec: float) -> int:
        slots = 1 if duration_sec <= 7.5 else 2
        return self.cost_cents_per_5s * slots

    # ----------------------------------------------------------------- HTTP

    def _auth_header(self) -> Dict[str, str]:
        ak = os.environ.get(ENV_AK, "")
        sk = os.environ.get(ENV_SK, "")
        token = make_jwt(ak, sk)
        return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    def _submit(self, body: Dict[str, Any], httpx_mod: Any) -> Dict[str, Any]:
        url = self.api_base + SUBMIT_PATH
        resp = httpx_mod.post(url, headers=self._auth_header(), json=body, timeout=60)
        if resp.status_code != 200:
            raise RuntimeError(f"kling submit status {resp.status_code}: {resp.text[:300]}")
        payload = resp.json()
        if not isinstance(payload, dict) or payload.get("code") not in (0, 200, None):
            raise RuntimeError(f"kling submit error: {payload}")
        data = payload.get("data") or {}
        task_id = data.get("task_id")
        if not task_id:
            raise RuntimeError(f"kling submit missing task_id: {payload}")
        return data

    def _poll(self, task_id: str, httpx_mod: Any, sleep_fn: Any = time.sleep) -> Dict[str, Any]:
        deadline = time.time() + self.timeout_sec
        url = f"{self.api_base}{QUERY_PATH}/{task_id}"
        while time.time() < deadline:
            resp = httpx_mod.get(url, headers=self._auth_header(), timeout=30)
            if resp.status_code != 200:
                raise RuntimeError(f"kling poll status {resp.status_code}: {resp.text[:300]}")
            payload = resp.json()
            data = payload.get("data") or {}
            status = data.get("task_status")
            if status == "succeed":
                return data
            if status == "failed":
                raise RuntimeError(
                    f"kling task failed: {data.get('task_status_msg', 'unknown')}"
                )
            sleep_fn(self.poll_interval_sec)
        raise RuntimeError(f"kling poll timed out after {self.timeout_sec}s")

    def _download(self, video_url: str, out_path: Path, httpx_mod: Any) -> None:
        resp = httpx_mod.get(video_url, timeout=120)
        if resp.status_code != 200:
            raise RuntimeError(f"kling download status {resp.status_code}")
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
            clip.error = f"{ENV_AK}/{ENV_SK} not set"
            copy_placeholder(out_path)
            return clip

        try:
            import httpx
        except ImportError as exc:
            clip.error = f"httpx unavailable: {exc}"
            copy_placeholder(out_path)
            return clip

        body: Dict[str, Any] = {
            "model_name": self.model_name,
            "mode": self.mode,
            "duration": _coerce_duration(duration_sec),
            "cfg_scale": self.cfg_scale,
            "image": base64_file(start_frame),
        }
        if prompt:
            body["prompt"] = prompt[:2500]
        if end_frame is not None and end_frame.exists():
            body["image_tail"] = base64_file(end_frame)
            # When a tail frame is supplied Kling only supports 5s output.
            body["duration"] = "5"

        started = time.time()
        try:
            data = self._submit(body, httpx)
            task_id = data["task_id"]
            clip.job_id = task_id
            done = self._poll(task_id, httpx)
            videos = ((done.get("task_result") or {}).get("videos")) or []
            if not videos:
                raise RuntimeError("kling response had no videos")
            video_url = videos[0].get("url")
            if not video_url:
                raise RuntimeError("kling response video missing url")
            self._download(video_url, out_path, httpx)
            try:
                clip.duration_sec = float(videos[0].get("duration") or duration_sec)
            except (TypeError, ValueError):
                pass
        except Exception as exc:
            clip.error = f"kling generate failed: {exc}"
            copy_placeholder(out_path)
        finally:
            clip.duration_ms = int((time.time() - started) * 1000)

        if clip.error is None:
            clip.cost_cents = self.estimated_cost_cents(clip.duration_sec)
        return clip


__all__ = ["KlingAdapter", "make_jwt"]

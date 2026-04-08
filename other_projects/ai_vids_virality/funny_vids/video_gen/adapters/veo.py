"""Veo (Google Vertex AI) video provider adapter — PARTIAL.

# TODO: This adapter is intentionally partial. Two reasons:
#
# 1. Vertex AI requires OAuth2 service-account access tokens (the
#    standard `google-auth` flow). We don't ship the `google-auth`
#    dependency yet — adding it touches `requirements.txt` and the
#    Hetzner deploy story, both of which are out of scope for Phase 5.
#
# 2. The Veo `predictLongRunning` preview endpoint was deprecated on
#    2026-04-02. The GA endpoint shape has been moving and I refuse to
#    invent JSON field names — per the Phase 5 plan, "Do not invent
#    endpoints or parameter names you can't confirm." Better to ship a
#    clean error than guess.
#
# What IS implemented:
#   - The `is_available()` gate checks for `GOOGLE_VERTEX_KEY` (a raw
#     access token) or `GOOGLE_APPLICATION_CREDENTIALS` (a path to a
#     service-account JSON). Both are recognized.
#   - The cost estimator returns a placeholder figure.
#   - `generate()` returns immediately with `error` set explaining what's
#     missing, copies the placeholder MP4, and never raises.
#
# What's needed to finish:
#   - Pull a fresh access token from the service-account JSON via
#     `google.auth.default()` + `google.auth.transport.requests.Request()`,
#     OR honor a pre-baked `GOOGLE_VERTEX_KEY` token.
#   - Confirm the GA endpoint:
#       POST https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{PROJECT}/locations/{LOCATION}/publishers/google/models/{MODEL}:predictLongRunning
#     and the LRO polling path:
#       GET  https://{LOCATION}-aiplatform.googleapis.com/v1/{operation_name}
#   - Re-verify the request body schema (instances + parameters) against
#     the post-2026-04-02 GA documentation.
#
# Reference:
#   https://docs.cloud.google.com/vertex-ai/generative-ai/docs/model-reference/veo-video-generation
"""
from __future__ import annotations

import logging
import os
import time
from pathlib import Path
from typing import Any, Dict, Optional

from video_gen._common import copy_placeholder
from video_gen.adapter import VideoClip, VideoProviderAdapter


LOG = logging.getLogger("video_gen.adapters.veo")

ENV_TOKEN = "GOOGLE_VERTEX_KEY"
ENV_SERVICE_ACCOUNT = "GOOGLE_APPLICATION_CREDENTIALS"


class VeoAdapter(VideoProviderAdapter):
    provider_id = "veo"

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self.model: str = str(self.config.get("model", "veo-3.0-generate-001"))
        self.project: str = str(self.config.get("project", os.environ.get("GOOGLE_CLOUD_PROJECT", "")))
        self.location: str = str(self.config.get("location", "us-central1"))
        self.poll_interval_sec: float = float(self.config.get("poll_interval_sec", 10))
        self.timeout_sec: float = float(self.config.get("timeout_sec", 900))
        self.cost_cents_per_5s: int = int(self.config.get("cost_cents_per_5s", 150))

    def is_available(self) -> bool:
        token_env = bool(os.environ.get(ENV_TOKEN))
        sa_env = bool(os.environ.get(ENV_SERVICE_ACCOUNT))
        # Even if the auth is present, we still need a project ID.
        return (token_env or sa_env) and bool(self.project)

    def estimated_cost_cents(self, duration_sec: float) -> int:
        slots = max(1, int(round((duration_sec or 5) / 5)))
        return self.cost_cents_per_5s * slots

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
        copy_placeholder(out_path)

        if not self.is_available():
            clip.error = (
                f"veo unavailable: need {ENV_TOKEN} or {ENV_SERVICE_ACCOUNT} "
                f"and a project ID"
            )
            return clip

        # TODO: implement the Vertex AI predictLongRunning call. See module
        # docstring for the missing pieces. Until then we return cleanly
        # with an error so the routing layer falls through to the next
        # adapter (typically the stub).
        clip.error = (
            "veo adapter not yet wired to the Vertex AI predictLongRunning "
            "endpoint — partial implementation, see module TODO"
        )
        return clip


__all__ = ["VeoAdapter"]

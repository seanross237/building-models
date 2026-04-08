"""Stub video provider adapter.

Always copies `video_gen/placeholder.mp4` to `out_path`. Always available,
zero cost. This is the fallback the pipeline routes to when no real
provider adapter reports `is_available()`.
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

from video_gen._common import copy_placeholder
from video_gen.adapter import VideoClip, VideoProviderAdapter


class StubVideoAdapter(VideoProviderAdapter):
    provider_id = "stub-video-v1"

    def is_available(self) -> bool:
        return True

    def estimated_cost_cents(self, duration_sec: float) -> int:
        return 0

    def generate(
        self,
        start_frame: Path,
        end_frame: Optional[Path],
        prompt: str,
        duration_sec: float,
        out_path: Path,
        beat_n: int = 1,
    ) -> VideoClip:
        copy_placeholder(out_path)
        return VideoClip(
            beat_n=beat_n,
            path=out_path,
            provider_id=self.provider_id,
            duration_sec=float(duration_sec or 2),
            cost_cents=0,
        )


__all__ = ["StubVideoAdapter"]

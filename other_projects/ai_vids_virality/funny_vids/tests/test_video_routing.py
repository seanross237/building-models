"""Tests for video_gen.pipeline routing logic."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

import pytest

from video_gen.adapter import VideoClip, VideoProviderAdapter
from video_gen.adapters.stub_video import StubVideoAdapter
from video_gen.pipeline import load_adapters, select_video_adapter


class _Always(VideoProviderAdapter):
    def __init__(self, provider_id: str, available: bool = True) -> None:
        super().__init__(config={"id": provider_id})
        self._available = available

    def is_available(self) -> bool:
        return self._available

    def estimated_cost_cents(self, duration_sec: float) -> int:
        return 10

    def generate(
        self,
        start_frame: Path,
        end_frame: Optional[Path],
        prompt: str,
        duration_sec: float,
        out_path: Path,
        beat_n: int = 1,
    ) -> VideoClip:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(b"FAKE")
        return VideoClip(
            beat_n=beat_n,
            path=out_path,
            provider_id=self.provider_id,
            duration_sec=duration_sec,
            cost_cents=10,
        )


def test_select_picks_first_available() -> None:
    cfg = {
        "routing": {"default": ["kling", "luma", "stub"]},
        "adapters": [],
    }
    adapters = {
        "kling": _Always("kling", available=False),
        "luma": _Always("luma", available=True),
        "stub": StubVideoAdapter(),
    }
    chosen = select_video_adapter(cfg, adapters)
    assert chosen.provider_id == "luma"


def test_select_falls_back_to_stub_when_none_available() -> None:
    cfg = {"routing": {"default": ["kling", "luma"]}, "adapters": []}
    adapters = {
        "kling": _Always("kling", available=False),
        "luma": _Always("luma", available=False),
    }
    chosen = select_video_adapter(cfg, adapters)
    assert isinstance(chosen, StubVideoAdapter)


def test_select_skips_missing_routing_entries() -> None:
    cfg = {"routing": {"default": ["nonexistent", "kling"]}, "adapters": []}
    adapters = {"kling": _Always("kling", available=True)}
    chosen = select_video_adapter(cfg, adapters)
    assert chosen.provider_id == "kling"


def test_select_skips_adapter_whose_is_available_raises() -> None:
    class _Boom(VideoProviderAdapter):
        provider_id = "boom"

        def is_available(self) -> bool:
            raise RuntimeError("kaboom")

        def estimated_cost_cents(self, duration_sec: float) -> int:
            return 0

        def generate(self, *args, **kwargs):
            return VideoClip(beat_n=1, path=Path("x"), provider_id="boom", duration_sec=1)

    cfg = {"routing": {"default": ["boom", "kling"]}, "adapters": []}
    adapters = {"boom": _Boom(), "kling": _Always("kling", available=True)}
    chosen = select_video_adapter(cfg, adapters)
    assert chosen.provider_id == "kling"


def test_load_adapters_skips_disabled_entries() -> None:
    cfg = {
        "routing": {"default": ["stub"]},
        "adapters": [
            {
                "id": "stub",
                "enabled": True,
                "adapter": "video_gen.adapters.stub_video.StubVideoAdapter",
                "config": {},
            },
            {
                "id": "kling",
                "enabled": False,
                "adapter": "video_gen.adapters.kling.KlingAdapter",
                "config": {},
            },
        ],
    }
    adapters = load_adapters(cfg)
    assert "stub" in adapters
    assert "kling" not in adapters


def test_load_adapters_loads_real_classes_from_video_yaml() -> None:
    """Verify the production config/video.yaml imports cleanly."""
    adapters = load_adapters()
    # Every adapter id from the production yaml should be present.
    for expected in ("kling", "luma", "runway", "pika", "veo", "stub"):
        assert expected in adapters, f"adapter {expected} missing from production config"


def test_select_returns_stub_for_empty_config() -> None:
    chosen = select_video_adapter({"routing": {"default": []}, "adapters": []}, {})
    assert isinstance(chosen, StubVideoAdapter)

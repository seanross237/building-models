"""Video provider adapter contract.

Every video provider implements `generate(start_frame, end_frame, prompt,
duration_sec, out_path) -> VideoClip`. Adapters submit a job to the
provider, poll until the clip is ready, download the MP4 to `out_path`,
and return a `VideoClip` with cost and timing metadata.

Adapters MUST NOT raise from `generate()`. On any failure path they
return a `VideoClip` with `error` set, and copy the placeholder MP4 to
`out_path` so the downstream stitcher always has a file to concatenate.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional


@dataclass
class VideoClip:
    beat_n: int
    path: Path
    provider_id: str
    duration_sec: float
    cost_cents: int = 0
    seed: Optional[int] = None
    job_id: Optional[str] = None
    duration_ms: int = 0  # wall-clock spent calling the provider
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["path"] = str(self.path)
        return data


class VideoProviderAdapter(ABC):
    """Base class every concrete video provider adapter inherits from."""

    provider_id: str = "unknown"

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config: Dict[str, Any] = dict(config or {})
        if "id" in self.config:
            self.provider_id = str(self.config["id"])

    @abstractmethod
    def is_available(self) -> bool:
        """True if this adapter can currently dispatch a real job."""

    @abstractmethod
    def estimated_cost_cents(self, duration_sec: float) -> int:
        """Rough cost estimate in cents for a clip of this length."""

    @abstractmethod
    def generate(
        self,
        start_frame: Path,
        end_frame: Optional[Path],
        prompt: str,
        duration_sec: float,
        out_path: Path,
        beat_n: int = 1,
    ) -> VideoClip:
        """Submit a job, poll, download, return a VideoClip. Must not raise."""


__all__ = ["VideoClip", "VideoProviderAdapter"]

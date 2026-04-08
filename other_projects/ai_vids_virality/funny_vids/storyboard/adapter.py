"""Storyboard adapter contract.

Every storyboard adapter produces two things: a `CharacterRef` (one image
per character across the sketch) and a `Frame` (one image per beat).
Both calls take an `out_path` and the adapter writes the PNG there. On
failure, the adapter MUST copy the placeholder PNG to `out_path` so the
downstream pipeline always has a file to point at, and return the
dataclass with `error` set. Adapters never raise from these methods.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class CharacterRef:
    name: str
    slug: str
    path: Path
    prompt: str
    adapter_id: str = "unknown"
    cost_cents: int = 0
    duration_ms: int = 0
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["path"] = str(self.path)
        return data


@dataclass
class Frame:
    beat_n: int
    path: Path
    prompt: str
    adapter_id: str = "unknown"
    seed: Optional[int] = None
    cost_cents: int = 0
    duration_ms: int = 0
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["path"] = str(self.path)
        return data


class StoryboardAdapter(ABC):
    """Contract every storyboard adapter implements."""

    adapter_id: str = "unknown"

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config: Dict[str, Any] = dict(config or {})

    @abstractmethod
    def is_available(self) -> bool:
        """True if this adapter can currently generate images."""

    @abstractmethod
    def generate_character_ref(
        self,
        character: Dict[str, Any],
        style_guide: str,
        out_path: Path,
    ) -> CharacterRef:
        """Generate a single character reference image. Must not raise."""

    @abstractmethod
    def generate_frame(
        self,
        beat: Dict[str, Any],
        character_refs: List[CharacterRef],
        style_guide: str,
        out_path: Path,
    ) -> Frame:
        """Generate a per-beat start frame conditioned on the char refs. Must not raise."""


__all__ = ["CharacterRef", "Frame", "StoryboardAdapter"]

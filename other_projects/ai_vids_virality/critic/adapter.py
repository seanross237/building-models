"""Critic adapter contract.

Phase 6 introduces a two-layer AI critic:

1. Per-clip shot check (`check_shot`) — verifies a single beat clip
   matches its storyboard frame, has no obvious artifacts, and the
   character is consistent. The video pipeline retries clip generation
   up to N times when this returns `passed=False`.

2. Full-sketch critique (`critique_sketch`) — runs on the assembled
   final cut and scores comedic timing, pacing, punchline landing, audio
   clarity, and the headline `is_funny` judgment.

Adapters MUST NOT raise from either method. On any failure path they
return the dataclass with `error` set, and the shot check returns
`passed=True` so infrastructure problems don't cause infinite retries.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class ShotReport:
    beat_n: int
    passed: bool
    score: int
    issues: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    adapter_id: str = "unknown"
    duration_ms: int = 0
    cost_cents: int = 0
    raw_response: Optional[str] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SketchCritique:
    sketch_id: str
    overall_score: int
    axes: Dict[str, int] = field(default_factory=dict)
    issues: List[str] = field(default_factory=list)
    fix_suggestions: List[str] = field(default_factory=list)
    is_funny: bool = False
    verdict: str = ""
    adapter_id: str = "unknown"
    duration_ms: int = 0
    cost_cents: int = 0
    raw_response: Optional[str] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class CriticAdapter(ABC):
    adapter_id: str = "unknown"

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config: Dict[str, Any] = dict(config or {})
        if "id" in self.config:
            self.adapter_id = str(self.config["id"])

    @abstractmethod
    def is_available(self) -> bool: ...

    @abstractmethod
    def check_shot(
        self,
        clip_path: Path,
        expected_frame: Path,
        character_refs: List[Path],
        beat_metadata: Dict[str, Any],
    ) -> ShotReport: ...

    @abstractmethod
    def critique_sketch(
        self,
        final_cut_path: Path,
        sketch_metadata: Dict[str, Any],
    ) -> SketchCritique: ...


__all__ = ["CriticAdapter", "ShotReport", "SketchCritique"]

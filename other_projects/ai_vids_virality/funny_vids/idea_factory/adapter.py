"""Model adapter contract for the multi-model idea factory.

Every adapter implements the same interface: `generate(signal, prompt, n)`
returns a `PremiseResult`. Adapters never raise from `generate()` — on any
failure they return a `PremiseResult` with `error` set and `premises=[]`.

Phase 3 ships three adapters:
    - ClaudeCLIAdapter   (real, via the `claude -p --output-format json` CLI)
    - OpenAIAdapter      (real if OPENAI_API_KEY set, else deterministic stub)
    - GeminiAdapter      (real if GEMINI_API_KEY set, else deterministic stub)

Phase 4+ will swap or extend by adding new adapter classes — the factory
doesn't care which model is which as long as the contract holds.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Premise:
    logline: str
    synopsis: str
    tone: str
    target_length_sec: int
    characters: List[Dict[str, Any]] = field(default_factory=list)
    twist: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Premise":
        return cls(
            logline=str(data.get("logline", "")).strip(),
            synopsis=str(data.get("synopsis", "")).strip(),
            tone=str(data.get("tone", "")).strip(),
            target_length_sec=int(data.get("target_length_sec", 30) or 30),
            characters=list(data.get("characters") or []),
            twist=str(data.get("twist", "")).strip(),
        )


@dataclass
class PremiseResult:
    model_id: str
    signal_id: str
    premises: List[Premise] = field(default_factory=list)
    cost_cents: int = 0
    duration_ms: int = 0
    raw_response: Optional[str] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "model_id": self.model_id,
            "signal_id": self.signal_id,
            "premises": [p.to_dict() for p in self.premises],
            "cost_cents": self.cost_cents,
            "duration_ms": self.duration_ms,
            "raw_response": self.raw_response,
            "error": self.error,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PremiseResult":
        return cls(
            model_id=str(data.get("model_id", "")),
            signal_id=str(data.get("signal_id", "")),
            premises=[Premise.from_dict(p) for p in (data.get("premises") or [])],
            cost_cents=int(data.get("cost_cents", 0) or 0),
            duration_ms=int(data.get("duration_ms", 0) or 0),
            raw_response=data.get("raw_response"),
            error=data.get("error"),
        )


class ModelAdapter(ABC):
    """Base class. Subclasses set `model_id` and implement the two methods."""

    model_id: str = "unknown"

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config: Dict[str, Any] = dict(config or {})

    @abstractmethod
    def generate(self, signal: Dict[str, Any], prompt: str, n_premises: int = 3) -> PremiseResult:
        """Return a PremiseResult. Must never raise."""

    @abstractmethod
    def is_available(self) -> bool:
        """True if the adapter can call a real model right now (CLI present, key set, etc)."""


__all__ = ["ModelAdapter", "Premise", "PremiseResult"]

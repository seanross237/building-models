"""Publisher contract for Phase 7.

A `Publisher` pushes a finished sketch to some destination — a local
archive directory, YouTube Shorts, TikTok, X, etc. Every publisher
returns a `PublishResult` describing whether the push succeeded and,
if so, where the published artifact can be reached.

Adapters MUST NOT raise from `publish()`. On any failure path they
return a `PublishResult` with `success=False` and `error` set so the
backend can surface the failure without losing the other publishers'
results.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Optional

from state.store import Sketch, Store


@dataclass
class PublishResult:
    destination_id: str
    success: bool
    url: Optional[str] = None
    error: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class Publisher(ABC):
    destination_id: str = "unknown"

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config: Dict[str, Any] = dict(config or {})
        if "id" in self.config:
            self.destination_id = str(self.config["id"])

    @abstractmethod
    def is_available(self) -> bool: ...

    @abstractmethod
    def publish(self, sketch: Sketch, store: Store) -> PublishResult: ...


__all__ = ["PublishResult", "Publisher"]

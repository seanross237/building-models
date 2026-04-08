"""File-based store for sketches, signals, and queues.

Everything is JSON on disk. Each sketch lives at:
    {root}/sketches/{sketch_id}/sketch.json

with adjacent directories for refs/, storyboard/, clips/, and a final.mp4.

Concurrency note: this is intentionally simple. Phase 1 is single-process.
Later phases can layer locking on top of these primitives.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from .machine import Status, assert_transition


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass
class Sketch:
    id: str
    status: Status
    signal_id: Optional[str] = None
    premise: Optional[Dict[str, Any]] = None
    premises: List[Dict[str, Any]] = field(default_factory=list)
    beats: List[Dict[str, Any]] = field(default_factory=list)
    storyboard_frames: List[Dict[str, Any]] = field(default_factory=list)
    video_clips: List[Dict[str, Any]] = field(default_factory=list)
    final_cut_path: Optional[str] = None
    critic_report: Optional[Dict[str, Any]] = None
    cost_cents_total: int = 0
    history: List[Dict[str, Any]] = field(default_factory=list)
    created_at: str = field(default_factory=_now)
    updated_at: str = field(default_factory=_now)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["status"] = self.status.value
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Sketch":
        payload = dict(data)
        payload["status"] = Status(payload["status"])
        return cls(**payload)


class Store:
    """File-backed sketch store. Pass the data root (e.g. Path('data'))."""

    def __init__(self, root: Path) -> None:
        self.root = Path(root)
        self.sketches_dir = self.root / "sketches"
        self.signals_dir = self.root / "signals"
        self.queues_dir = self.root / "queues"
        self.published_dir = self.root / "published"
        self._ensure_layout()

    # ----------------------------------------------------------------- layout

    def _ensure_layout(self) -> None:
        for path in (
            self.sketches_dir,
            self.signals_dir,
            self.queues_dir,
            self.published_dir,
            self.queues_dir / "idea-factory",
            self.queues_dir / "premise-review",
            self.queues_dir / "manual-ideas",
            self.queues_dir / "scripted",
            self.queues_dir / "storyboard-review",
            self.queues_dir / "video-gen",
            self.queues_dir / "final-review",
            self.signals_dir / "reddit_stub" / "items",
        ):
            path.mkdir(parents=True, exist_ok=True)
        seen = self.signals_dir / "reddit_stub" / ".seen-ids"
        if not seen.exists():
            seen.write_text("", encoding="utf-8")

    # ----------------------------------------------------------------- paths

    def sketch_dir(self, sketch_id: str) -> Path:
        return self.sketches_dir / sketch_id

    def sketch_json_path(self, sketch_id: str) -> Path:
        return self.sketch_dir(sketch_id) / "sketch.json"

    def sketch_refs_dir(self, sketch_id: str) -> Path:
        return self.sketch_dir(sketch_id) / "refs"

    def sketch_storyboard_dir(self, sketch_id: str) -> Path:
        return self.sketch_dir(sketch_id) / "storyboard"

    def sketch_clips_dir(self, sketch_id: str) -> Path:
        return self.sketch_dir(sketch_id) / "clips"

    def sketch_final_path(self, sketch_id: str) -> Path:
        return self.sketch_dir(sketch_id) / "final.mp4"

    def signal_path(self, source: str, signal_id: str) -> Path:
        return self.signals_dir / source / "items" / f"{signal_id}.md"

    def seen_ids_path(self, source: str) -> Path:
        return self.signals_dir / source / ".seen-ids"

    # ----------------------------------------------------------------- IO

    def list_sketches(self) -> List[Sketch]:
        if not self.sketches_dir.exists():
            return []
        sketches: List[Sketch] = []
        for sub in sorted(self.sketches_dir.iterdir()):
            if not sub.is_dir():
                continue
            json_path = sub / "sketch.json"
            if not json_path.exists():
                continue
            sketches.append(Sketch.from_dict(json.loads(json_path.read_text(encoding="utf-8"))))
        return sketches

    def get_sketch(self, sketch_id: str) -> Sketch:
        path = self.sketch_json_path(sketch_id)
        if not path.exists():
            raise FileNotFoundError(f"sketch not found: {sketch_id}")
        return Sketch.from_dict(json.loads(path.read_text(encoding="utf-8")))

    def save_sketch(self, sketch: Sketch) -> None:
        sketch.updated_at = _now()
        sketch_dir = self.sketch_dir(sketch.id)
        sketch_dir.mkdir(parents=True, exist_ok=True)
        for sub in ("refs", "storyboard", "clips"):
            (sketch_dir / sub).mkdir(parents=True, exist_ok=True)
        path = self.sketch_json_path(sketch.id)
        path.write_text(json.dumps(sketch.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")

    def transition(
        self,
        sketch_id: str,
        new_status: Status,
        payload: Optional[Dict[str, Any]] = None,
    ) -> Sketch:
        sketch = self.get_sketch(sketch_id)
        assert_transition(sketch.status, new_status)
        previous = sketch.status
        sketch.status = new_status
        sketch.history.append(
            {
                "from": previous.value,
                "to": new_status.value,
                "at": _now(),
                "payload": payload or {},
            }
        )
        self.save_sketch(sketch)
        return sketch

    # ----------------------------------------------------------------- queues

    def queue_dir(self, name: str) -> Path:
        return self.queues_dir / name

    def write_queue_marker(self, queue: str, marker_id: str, payload: Dict[str, Any]) -> Path:
        directory = self.queue_dir(queue)
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / f"{marker_id}.json"
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return path

    def list_queue(self, queue: str) -> List[Path]:
        directory = self.queue_dir(queue)
        if not directory.exists():
            return []
        return sorted(p for p in directory.glob("*.json") if p.name != ".gitkeep")

    def read_queue_marker(self, path: Path) -> Dict[str, Any]:
        return json.loads(path.read_text(encoding="utf-8"))

    def remove_queue_marker(self, queue: str, marker_id: str) -> None:
        path = self.queue_dir(queue) / f"{marker_id}.json"
        if path.exists():
            path.unlink()

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .event_schema import EventRecord, event_from_dict, validate_event_record


class AppendOnlyJsonlWriter:
    """Small append-only JSONL writer for event and record streams."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path).expanduser().resolve()

    def append_event(self, event: EventRecord) -> None:
        validate_event_record(event)
        self._append_line(event.to_dict())

    def append_event_dict(self, data: dict[str, Any]) -> None:
        event = event_from_dict(data)
        self.append_event(event)

    def append_json_record(self, data: dict[str, Any]) -> None:
        self._append_line(data)

    def read_all(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        return [
            json.loads(line)
            for line in self.path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    def _append_line(self, data: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(data, sort_keys=True) + "\n")

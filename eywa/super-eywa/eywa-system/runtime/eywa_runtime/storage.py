"""Storage helpers for the file-first v1 runtime."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rendered = "\n".join(json.dumps(row, sort_keys=False) for row in rows)
    if rendered:
        rendered += "\n"
    path.write_text(rendered, encoding="utf-8")


def relative_ref(path: Path, base: Path) -> str:
    return str(path.relative_to(base))

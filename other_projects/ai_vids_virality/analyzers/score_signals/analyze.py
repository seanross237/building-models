"""Stub analyzer that scores raw signals using a deterministic rule.

Phase 1 deliberately uses a length-based scorer so we can test queue
transitions without any LLM calls. Phase 2 will swap this for a real
prompt + schema-validated Claude call (see analyze-items.py in
research-radar for the pattern we'll mirror).
"""
from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from state.store import Store


SOURCE_DIR_NAME = "signals"


def _parse_frontmatter(text: str) -> Dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    block = text[4:end]
    out: Dict[str, str] = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        out[key.strip()] = value.strip()
    return out


def _parse_summary(text: str) -> str:
    match = re.search(r"^## Summary\n\n(.+?)(?=\n## |\Z)", text, flags=re.MULTILINE | re.DOTALL)
    if not match:
        return ""
    return match.group(1).strip()


def stub_score(title: str) -> int:
    """Deterministic scorer used in Phase 1.

    Anchored at 5 with a length-derived bump so different titles get
    different scores in the 5..14 range, then clamped to 1..10.
    """
    base = 5 + (len(title) % 10)
    return max(1, min(10, base))


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _iter_signal_files(store: Store) -> List[Path]:
    paths: List[Path] = []
    if not store.signals_dir.exists():
        return paths
    for source_dir in sorted(p for p in store.signals_dir.iterdir() if p.is_dir()):
        items_dir = source_dir / "items"
        if not items_dir.exists():
            continue
        for item in sorted(items_dir.glob("*.md")):
            paths.append(item)
    return paths


def analyze_pending(store: Store, threshold: int = 7) -> List[str]:
    """Find unanalyzed signals, score them, and promote any above threshold.

    Returns the list of signal IDs that were promoted to the idea-factory queue.
    Idempotent: a signal that already has a marker in any downstream queue is
    skipped.
    """
    promoted: List[str] = []
    idea_queue = store.queue_dir("idea-factory")
    idea_queue.mkdir(parents=True, exist_ok=True)

    for path in _iter_signal_files(store):
        text = path.read_text(encoding="utf-8")
        meta = _parse_frontmatter(text)
        signal_id = meta.get("id") or path.stem
        marker_path = idea_queue / f"{signal_id}.json"
        if marker_path.exists() or _signal_already_consumed(store, signal_id):
            continue

        title = meta.get("title", path.stem)
        score = stub_score(title)
        if score < threshold:
            continue

        payload = {
            "signal_id": signal_id,
            "source": meta.get("source", "unknown"),
            "source_url": meta.get("source_url", ""),
            "title": title,
            "summary": _parse_summary(text),
            "sketchability_score": score,
            "comedy_angles": [
                {"angle": "absurdist", "note": "stub angle from rule-based scorer"}
            ],
            "character_archetypes": ["everyman", "authority figure"],
            "topical_window_hours": 48,
            "should_promote": True,
            "analyzed_at": _now(),
            "source_item_path": str(path),
        }
        store.write_queue_marker("idea-factory", signal_id, payload)
        promoted.append(signal_id)
    return promoted


def _signal_already_consumed(store: Store, signal_id: str) -> bool:
    """True if any sketch already references this signal."""
    for sketch in store.list_sketches():
        if sketch.signal_id == signal_id:
            return True
    return False

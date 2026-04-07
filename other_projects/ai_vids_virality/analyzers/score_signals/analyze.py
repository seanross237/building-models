"""Rule-based signal analyzer.

Phase 2 reads `config/comedy-lens.md` and `config/thresholds.yaml`, then
applies the keyword scorer in `lens_rules.py` to every unanalyzed signal
across every source directory under `data/signals/`. Signals at or above
the threshold get promoted to the idea-factory queue.

Phase 3 will swap `lens_rules.score_text(...)` for an LLM call but the
function signatures here will not change.
"""
from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from analyzers.score_signals.lens_rules import Lens, load_lens, score_text
from state.store import Store


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_LENS_PATH = PROJECT_ROOT / "config" / "comedy-lens.md"
DEFAULT_THRESHOLDS_PATH = PROJECT_ROOT / "config" / "thresholds.yaml"
DEFAULT_THRESHOLD = 7


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


def _parse_body(text: str) -> str:
    match = re.search(r"^## Source content\n\n(.+?)(?=\n## |\Z)", text, flags=re.MULTILINE | re.DOTALL)
    if not match:
        return ""
    return match.group(1).strip()


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


def _load_threshold(thresholds_path: Path) -> int:
    if not thresholds_path.exists():
        return DEFAULT_THRESHOLD
    try:
        import yaml  # type: ignore
        data = yaml.safe_load(thresholds_path.read_text(encoding="utf-8")) or {}
    except Exception:
        return DEFAULT_THRESHOLD
    scoring = data.get("scoring") if isinstance(data, dict) else None
    if isinstance(scoring, dict) and "promote_to_factory" in scoring:
        try:
            return int(scoring["promote_to_factory"])
        except (TypeError, ValueError):
            return DEFAULT_THRESHOLD
    return DEFAULT_THRESHOLD


def _signal_already_consumed(store: Store, signal_id: str) -> bool:
    for sketch in store.list_sketches():
        if sketch.signal_id == signal_id:
            return True
    return False


def stub_score(title: str) -> int:
    """Phase 1 deterministic length-based scorer.

    Kept for backwards compatibility with the Phase 1 tests; the production
    pipeline now uses `lens_rules.score_text` via `analyze_pending`.
    """
    base = 5 + (len(title) % 10)
    return max(1, min(10, base))


def analyze_pending(
    store: Store,
    threshold: Optional[int] = None,
    lens: Optional[Lens] = None,
) -> List[str]:
    """Score every unanalyzed signal and promote any at-or-above threshold.

    Returns the list of signal IDs that were promoted to the idea-factory
    queue. Idempotent: signals already in the queue or already attached to
    a sketch are skipped.
    """
    if threshold is None:
        threshold = _load_threshold(DEFAULT_THRESHOLDS_PATH)
    if lens is None:
        lens = load_lens(DEFAULT_LENS_PATH)

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
        body = _parse_body(text) or _parse_summary(text)
        score = score_text(title, body, lens)
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
                {"angle": "rule-based", "note": "lens-driven keyword scorer"},
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

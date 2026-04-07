"""Reddit stub collector — KEPT AS A TEST FIXTURE ONLY (Phase 2+).

Originally this was the Phase 1 stub that emitted three hardcoded signal
markdown files into `data/signals/reddit_stub/items/`. As of Phase 2 the
real collectors live under `collectors/reddit/`, `collectors/hacker_news/`,
`collectors/google_news/`, and `collectors/youtube_trending/`. This module
is **disabled in `config/sources.yaml`** and is no longer wired into the
default pipeline run.

It is preserved (and still tested) because:
1. Several tests depend on its deterministic three-signal output as a
   convenient fixture for the analyzer / idea-factory / end-to-end paths.
2. It documents the seam shape (`fetch(store) -> list[str]`) that all
   Phase 2 collectors follow.

Do not run this in production. If you find yourself enabling it again,
prefer one of the real collectors instead.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

from state.store import Store


SOURCE_NAME = "reddit_stub"

STUB_SIGNALS: List[Dict[str, str]] = [
    {
        "id": "reddit-stub-001",
        "title": "Senator caught using spoon as wifi antenna in committee hearing",
        "source_url": "https://example.com/reddit/stub/001",
        "summary": (
            "During a televised infrastructure hearing, a senator was filmed "
            "duct-taping a soup spoon to the back of his laptop and pointing "
            "it at the ceiling, insisting it improved his connection."
        ),
        "tags": "political, absurd",
    },
    {
        "id": "reddit-stub-002",
        "title": "Tech CEO announces 4-day work week, then 5-day, then 6-day in same press conference",
        "source_url": "https://example.com/reddit/stub/002",
        "summary": (
            "A founder walked on stage promising a four-day work week, "
            "answered three questions, and by the end of the press conference "
            "had escalated all the way to a six-day mandatory schedule."
        ),
        "tags": "tech, satire",
    },
    {
        "id": "reddit-stub-003",
        "title": "Local man discovers he's been pronouncing his own name wrong for 40 years",
        "source_url": "https://example.com/reddit/stub/003",
        "summary": (
            "A man in Ohio learned at his mother's funeral that his first name "
            "is pronounced with a silent J. He has been correcting people his "
            "entire adult life."
        ),
        "tags": "human, absurd",
    },
]


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _read_seen_ids(path: Path) -> set:
    if not path.exists():
        return set()
    return {line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()}


def _append_seen_id(path: Path, signal_id: str) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(signal_id + "\n")


def _render_signal_markdown(signal: Dict[str, str]) -> str:
    return (
        "---\n"
        f"id: {signal['id']}\n"
        f"source: {SOURCE_NAME}\n"
        f"source_url: {signal['source_url']}\n"
        f"title: {signal['title']}\n"
        f"captured_at: {_now()}\n"
        "heat_score_raw: 0.5\n"
        "freshness_hours: 1\n"
        f"tags: [{signal['tags']}]\n"
        "---\n\n"
        "## Summary\n\n"
        f"{signal['summary']}\n\n"
        "## Source content\n\n"
        f"Stubbed source text for {signal['id']}.\n"
    )


def fetch(store: Store) -> List[str]:
    """Write the stub signals into the store and return the new signal IDs."""
    items_dir = store.signals_dir / SOURCE_NAME / "items"
    items_dir.mkdir(parents=True, exist_ok=True)
    seen_path = store.seen_ids_path(SOURCE_NAME)
    seen_path.touch(exist_ok=True)
    seen = _read_seen_ids(seen_path)

    new_ids: List[str] = []
    for signal in STUB_SIGNALS:
        signal_id = signal["id"]
        if signal_id in seen:
            continue
        out_path = items_dir / f"{signal_id}.md"
        out_path.write_text(_render_signal_markdown(signal), encoding="utf-8")
        _append_seen_id(seen_path, signal_id)
        seen.add(signal_id)
        new_ids.append(signal_id)
    return new_ids

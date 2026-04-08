"""Tests for the reddit_stub collector."""
from __future__ import annotations

from pathlib import Path

from collectors.reddit_stub import fetch as reddit_stub
from state.store import Store


def test_fetch_creates_three_signals_on_first_run(tmp_path: Path) -> None:
    store = Store(root=tmp_path)
    new_ids = reddit_stub.fetch(store)
    assert len(new_ids) == 3

    items_dir = tmp_path / "signals" / "reddit_stub" / "items"
    files = sorted(p for p in items_dir.glob("*.md"))
    assert len(files) == 3
    for f in files:
        text = f.read_text(encoding="utf-8")
        assert text.startswith("---\n")
        assert "title:" in text
        assert "## Summary" in text


def test_fetch_is_idempotent(tmp_path: Path) -> None:
    store = Store(root=tmp_path)
    first = reddit_stub.fetch(store)
    second = reddit_stub.fetch(store)
    assert len(first) == 3
    assert second == []

    items_dir = tmp_path / "signals" / "reddit_stub" / "items"
    files = list(items_dir.glob("*.md"))
    assert len(files) == 3


def test_fetch_records_seen_ids(tmp_path: Path) -> None:
    store = Store(root=tmp_path)
    reddit_stub.fetch(store)
    seen_path = tmp_path / "signals" / "reddit_stub" / ".seen-ids"
    text = seen_path.read_text(encoding="utf-8")
    assert "reddit-stub-001" in text
    assert "reddit-stub-002" in text
    assert "reddit-stub-003" in text

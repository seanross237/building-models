"""Tests for the score_signals analyzer."""
from __future__ import annotations

import json
from pathlib import Path

from analyzers.score_signals.analyze import analyze_pending, stub_score
from collectors.reddit_stub import fetch as reddit_stub
from state.store import Store


def test_stub_score_in_range() -> None:
    for title in [
        "short",
        "Senator caught using spoon as wifi antenna in committee hearing",
        "x" * 200,
    ]:
        score = stub_score(title)
        assert 1 <= score <= 10


def test_analyzer_promotes_high_scoring_signals(tmp_path: Path) -> None:
    store = Store(root=tmp_path)
    reddit_stub.fetch(store)

    promoted = analyze_pending(store, threshold=0)
    assert len(promoted) == 3

    queue_dir = tmp_path / "queues" / "idea-factory"
    files = sorted(p for p in queue_dir.glob("*.json"))
    assert len(files) == 3

    payload = json.loads(files[0].read_text(encoding="utf-8"))
    assert "signal_id" in payload
    assert "title" in payload
    assert "sketchability_score" in payload
    assert payload["should_promote"] is True


def test_analyzer_is_idempotent(tmp_path: Path) -> None:
    store = Store(root=tmp_path)
    reddit_stub.fetch(store)

    first = analyze_pending(store, threshold=0)
    second = analyze_pending(store, threshold=0)
    assert len(first) == 3
    assert second == []


def test_analyzer_respects_threshold(tmp_path: Path) -> None:
    store = Store(root=tmp_path)
    reddit_stub.fetch(store)
    promoted = analyze_pending(store, threshold=11)
    assert promoted == []

"""Tests for the Phase 2 /api/signals endpoints."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator

import pytest
from fastapi.testclient import TestClient

import backend.main as backend_main
from collectors._common import render_signal_markdown, write_signal_file
from state.store import Store


def _seed_signals(root: Path) -> None:
    store = Store(root=root)
    now = datetime.now(timezone.utc)
    items = [
        {
            "source": "reddit",
            "id": "reddit-fake1",
            "title": "Senator caught with spoon antenna in committee hearing",
            "summary": "An aide rolled tape and handed it back.",
            "body": "An aide rolled tape and handed it back.",
            "url": "https://example.com/r/1",
            "tags": ["popular", "reddit"],
        },
        {
            "source": "hacker_news",
            "id": "hn-fake2",
            "title": "Show HN: a button that announces every press out loud",
            "summary": "Built in two evenings.",
            "body": "Built in two evenings.",
            "url": "https://example.com/hn/2",
            "tags": ["hacker_news"],
        },
        {
            "source": "google_news",
            "id": "gn-fake3",
            "title": "Mayor accidentally bans pigeons in three-paragraph release",
            "summary": "Officials are reviewing the bird population.",
            "body": "Officials are reviewing the bird population.",
            "url": "https://example.com/gn/3",
            "tags": ["google_news"],
        },
        {
            "source": "youtube_trending",
            "id": "yt-fake4",
            "title": "CEO unveils 4-day work week then 6-day during same press conference",
            "summary": "Investors filed out one by one.",
            "body": "Investors filed out one by one.",
            "url": "https://example.com/yt/4",
            "tags": ["youtube_trending"],
        },
    ]
    for item in items:
        items_dir = store.signals_dir / item["source"] / "items"
        markdown = render_signal_markdown(
            signal_id=item["id"],
            source=item["source"],
            source_url=item["url"],
            title=item["title"],
            summary=item["summary"],
            body=item["body"],
            published_at=now,
            heat_score_raw=0.7,
            tags=item["tags"],
        )
        write_signal_file(items_dir, item["id"], markdown)


@pytest.fixture()
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("AI_VIDS_DATA_ROOT", str(tmp_path))
    _seed_signals(tmp_path)
    with TestClient(backend_main.app) as test_client:
        yield test_client


def test_list_signals_returns_seeded_items(client: TestClient) -> None:
    res = client.get("/api/signals")
    assert res.status_code == 200
    data = res.json()
    assert "signals" in data
    ids = sorted(s["id"] for s in data["signals"])
    assert ids == ["gn-fake3", "hn-fake2", "reddit-fake1", "yt-fake4"]
    for sig in data["signals"]:
        assert "source" in sig
        assert "title" in sig
        assert "url" in sig
        assert "score" in sig
        assert "promoted" in sig
        assert "rejected" in sig


def test_signals_sorted_by_score_desc(client: TestClient) -> None:
    data = client.get("/api/signals").json()
    scores = [s["score"] for s in data["signals"]]
    assert scores == sorted(scores, reverse=True)


def test_promote_signal_marks_promoted(client: TestClient) -> None:
    res = client.post("/api/signals/reddit-fake1/promote")
    assert res.status_code == 200
    body = res.json()
    assert body["promoted"] is True
    assert body["signal_id"] == "reddit-fake1"

    listing = client.get("/api/signals").json()
    found = [s for s in listing["signals"] if s["id"] == "reddit-fake1"][0]
    assert found["promoted"] is True


def test_promote_unknown_signal_404(client: TestClient) -> None:
    res = client.post("/api/signals/does-not-exist/promote")
    assert res.status_code == 404


def test_promote_creates_sketch(client: TestClient) -> None:
    client.post("/api/signals/reddit-fake1/promote")
    kanban = client.get("/api/kanban").json()
    # The stub idea factory should have created a new sketch in PREMISE_REVIEW.
    assert any(c["signal_id"] == "reddit-fake1" for c in kanban["premise_review"])


def test_reject_signal_persists(client: TestClient, tmp_path: Path) -> None:
    res = client.post("/api/signals/hn-fake2/reject")
    assert res.status_code == 200
    assert res.json()["rejected"] is True

    listing = client.get("/api/signals").json()
    rejected = [s for s in listing["signals"] if s["id"] == "hn-fake2"][0]
    assert rejected["rejected"] is True

    persisted = (tmp_path / "rejected-signals.json").read_text(encoding="utf-8")
    payload = json.loads(persisted)
    assert "hn-fake2" in payload["ids"]


def test_signals_page_count_matches_kanban_consumer(client: TestClient) -> None:
    """The Phase 2 UI uses /api/signals to populate the Signals nav badge.
    This test just confirms the endpoint stays stable for the count call.
    """
    data = client.get("/api/signals").json()
    assert isinstance(data["signals"], list)
    assert len(data["signals"]) >= 1

"""Tests for the Phase 7 /api/signals/bulk_reject endpoint."""
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


def _seed_signal(root: Path, source: str, signal_id: str, title: str) -> None:
    store = Store(root=root)
    items_dir = store.signals_dir / source / "items"
    items_dir.mkdir(parents=True, exist_ok=True)
    markdown = render_signal_markdown(
        signal_id=signal_id,
        source=source,
        source_url=f"https://example.com/{signal_id}",
        title=title,
        summary="short",
        body="body",
        published_at=datetime.now(timezone.utc),
        heat_score_raw=0.5,
        tags=[source],
    )
    write_signal_file(items_dir, signal_id, markdown)


@pytest.fixture()
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("AI_VIDS_DATA_ROOT", str(tmp_path))
    _seed_signal(tmp_path, "reddit", "reddit-fake-1", "first signal title")
    _seed_signal(tmp_path, "reddit", "reddit-fake-2", "second signal title")
    _seed_signal(tmp_path, "hacker_news", "hn-fake-3", "third signal title")
    with TestClient(backend_main.app) as test_client:
        test_client.tmp_path = tmp_path  # type: ignore[attr-defined]
        yield test_client


def test_bulk_reject_marks_signals(client: TestClient) -> None:
    res = client.post(
        "/api/signals/bulk_reject",
        json={"signal_ids": ["reddit-fake-1", "reddit-fake-2"]},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["rejected_count"] == 2
    assert data["total_rejected_now"] >= 2

    # The signals endpoint should now mark those two as rejected.
    listing = client.get("/api/signals").json()
    by_id = {s["id"]: s for s in listing["signals"]}
    assert by_id["reddit-fake-1"]["rejected"] is True
    assert by_id["reddit-fake-2"]["rejected"] is True
    assert by_id["hn-fake-3"]["rejected"] is False


def test_bulk_reject_persists_to_disk(client: TestClient) -> None:
    tmp_path: Path = client.tmp_path  # type: ignore[attr-defined]
    client.post(
        "/api/signals/bulk_reject",
        json={"signal_ids": ["reddit-fake-1"]},
    )
    path = tmp_path / "rejected-signals.json"
    assert path.exists()
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert "reddit-fake-1" in payload.get("ids", [])


def test_bulk_reject_empty_list_is_noop(client: TestClient) -> None:
    res = client.post("/api/signals/bulk_reject", json={"signal_ids": []})
    assert res.status_code == 200
    data = res.json()
    assert data["rejected_count"] == 0


def test_bulk_reject_dedupes_ids(client: TestClient) -> None:
    res = client.post(
        "/api/signals/bulk_reject",
        json={"signal_ids": ["reddit-fake-1", "reddit-fake-1", "reddit-fake-1"]},
    )
    # `rejected_count` reports how many ids were processed; dedup happens in
    # the stored set, not in the request body.
    assert res.status_code == 200
    data = res.json()
    assert data["rejected_count"] == 3
    assert data["total_rejected_now"] == 1

"""Phase 10: POST /api/signals/{id}/promote now accepts optional guidance.

The body `{"guidance": "..."}` is stored on the idea-factory queue manifest
as `user_guidance`. Missing / empty guidance omits the field entirely so
the behavior is identical to Phase 2 unannotated promotes.
"""
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


def _seed_one_signal(root: Path, signal_id: str = "reddit-guide-1") -> None:
    store = Store(root=root)
    now = datetime.now(timezone.utc)
    markdown = render_signal_markdown(
        signal_id=signal_id,
        source="reddit",
        source_url="https://example.com/r/guide",
        title="City council accidentally votes to replace stoplights with flags",
        summary="Officials are reviewing the traffic situation.",
        body="Officials are reviewing the traffic situation and want to assure residents.",
        published_at=now,
        heat_score_raw=0.7,
        tags=["popular", "reddit"],
    )
    items_dir = store.signals_dir / "reddit" / "items"
    write_signal_file(items_dir, signal_id, markdown)


@pytest.fixture()
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("AI_VIDS_DATA_ROOT", str(tmp_path))
    _seed_one_signal(tmp_path)
    with TestClient(backend_main.app) as test_client:
        test_client.test_data_root = tmp_path  # type: ignore[attr-defined]
        yield test_client


def _read_manifest(tmp_path: Path, signal_id: str) -> dict:
    path = tmp_path / "queues" / "idea-factory" / f"{signal_id}.json"
    assert path.exists(), f"queue marker missing: {path}"
    return json.loads(path.read_text(encoding="utf-8"))


def test_promote_with_guidance_writes_user_guidance_field(client: TestClient) -> None:
    """When the body carries non-empty guidance, it lands on the manifest."""
    res = client.post(
        "/api/signals/reddit-guide-1/promote",
        json={"guidance": "Lean into the traffic-cop deadpan angle, one location."},
    )
    assert res.status_code == 200
    body = res.json()
    assert body["promoted"] is True
    assert body["user_guidance"] == "Lean into the traffic-cop deadpan angle, one location."

    manifest = _read_manifest(client.test_data_root, "reddit-guide-1")  # type: ignore[attr-defined]
    assert manifest["user_guidance"] == "Lean into the traffic-cop deadpan angle, one location."
    assert manifest["signal_id"] == "reddit-guide-1"


def test_promote_without_body_omits_user_guidance(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The Phase 2 no-body promote path is unchanged: no `user_guidance` key."""
    monkeypatch.setenv("AI_VIDS_DATA_ROOT", str(tmp_path))
    _seed_one_signal(tmp_path, signal_id="reddit-guide-2")

    with TestClient(backend_main.app) as client:
        res = client.post("/api/signals/reddit-guide-2/promote")
        assert res.status_code == 200
        assert res.json()["promoted"] is True

    manifest = _read_manifest(tmp_path, "reddit-guide-2")
    assert "user_guidance" not in manifest


def test_promote_with_empty_guidance_omits_user_guidance(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """An empty string / whitespace-only guidance is treated as no guidance."""
    monkeypatch.setenv("AI_VIDS_DATA_ROOT", str(tmp_path))
    _seed_one_signal(tmp_path, signal_id="reddit-guide-3")

    with TestClient(backend_main.app) as client:
        res = client.post(
            "/api/signals/reddit-guide-3/promote",
            json={"guidance": "   "},
        )
        assert res.status_code == 200

    manifest = _read_manifest(tmp_path, "reddit-guide-3")
    assert "user_guidance" not in manifest


def test_promote_with_guidance_still_creates_sketch(client: TestClient) -> None:
    """Sketch creation still runs after the manifest is written."""
    res = client.post(
        "/api/signals/reddit-guide-1/promote",
        json={"guidance": "traffic flag angle"},
    )
    assert res.status_code == 200
    kanban = client.get("/api/kanban").json()
    assert any(
        c["signal_id"] == "reddit-guide-1"
        for c in kanban.get("premise_review", [])
    )

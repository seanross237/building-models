"""Tests for the Phase 7 /api/sketch/{id}/publish endpoint envelope."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterator

import pytest
from fastapi.testclient import TestClient

import backend.main as backend_main
from idea_factory.adapter import ModelAdapter, Premise, PremiseResult
from idea_factory.factory import run_factory
from state.leaderboard import Leaderboard
from state.machine import Status
from state.store import Store


FIXTURES = Path(__file__).resolve().parent / "fixtures"


class _FakeAdapter(ModelAdapter):
    def __init__(self, model_id: str) -> None:
        super().__init__(config={})
        self.model_id = model_id

    def is_available(self) -> bool:
        return True

    def generate(self, signal: Dict[str, Any], prompt: str, n_premises: int = 3) -> PremiseResult:
        premise_dict = json.loads((FIXTURES / "sample_premise.json").read_text(encoding="utf-8"))
        return PremiseResult(
            model_id=self.model_id,
            signal_id=str(signal.get("signal_id", "")),
            premises=[Premise.from_dict(premise_dict)],
        )


@pytest.fixture()
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("AI_VIDS_DATA_ROOT", str(tmp_path))
    monkeypatch.setenv("AI_VIDS_OFFLINE_STORYBOARD", "1")
    monkeypatch.setenv("AI_VIDS_OFFLINE_VIDEO", "1")
    monkeypatch.setenv("AI_VIDS_OFFLINE_CRITIC", "1")
    monkeypatch.setenv("AI_VIDS_OFFLINE_PUBLISH", "1")

    store = Store(root=tmp_path)
    store.write_queue_marker(
        "idea-factory",
        "test-signal-001",
        {
            "signal_id": "test-signal-001",
            "source": "reddit",
            "source_url": "https://example.com/r/1",
            "title": "Senator stands normally",
            "summary": "short summary",
        },
    )
    leaderboard = Leaderboard(tmp_path / "leaderboard.json")
    sketch_ids = run_factory(
        store,
        prompt_template="prompt {signal_title}",
        lens_text="lens",
        leaderboard=leaderboard,
        adapters=[_FakeAdapter("claude-opus")],
    )
    assert len(sketch_ids) == 1

    with TestClient(backend_main.app) as test_client:
        test_client.sketch_id = sketch_ids[0]  # type: ignore[attr-defined]
        test_client.tmp_path = tmp_path  # type: ignore[attr-defined]
        yield test_client


def _walk_to_critic_review(client: TestClient) -> str:
    sketch_id = client.sketch_id  # type: ignore[attr-defined]
    client.post(
        f"/api/sketch/{sketch_id}/approve_premise",
        json={"model_id": "claude-opus", "premise_index": 0},
    )
    client.post(f"/api/sketch/{sketch_id}/approve_storyboard")
    return sketch_id


def test_publish_returns_envelope(client: TestClient) -> None:
    sketch_id = _walk_to_critic_review(client)
    res = client.post(f"/api/sketch/{sketch_id}/publish")
    assert res.status_code == 200
    body = res.json()
    # Phase 7 envelope fields
    for key in ("sketch", "results", "success_count", "destination_count"):
        assert key in body
    assert body["sketch"]["id"] == sketch_id
    assert body["sketch"]["status"] == "published"
    assert body["success_count"] >= 1
    assert body["destination_count"] == 1  # offline mode forces local_archive only
    assert body["results"][0]["destination_id"] == "local_archive"
    assert body["results"][0]["success"] is True


def test_publish_creates_archive_directory(client: TestClient) -> None:
    sketch_id = _walk_to_critic_review(client)
    client.post(f"/api/sketch/{sketch_id}/publish")
    tmp_path: Path = client.tmp_path  # type: ignore[attr-defined]
    archive_dir = tmp_path / "published" / sketch_id
    assert archive_dir.is_dir()
    assert (archive_dir / "sketch.json").exists()
    assert (archive_dir / "critic.json").exists()
    assert (archive_dir / "final.mp4").exists()
    assert (archive_dir / "published_at.txt").exists()


def test_publish_from_premise_review_returns_409(client: TestClient) -> None:
    """Invalid state transition short-circuits before any publisher runs."""
    sketch_id = client.sketch_id  # type: ignore[attr-defined]
    res = client.post(f"/api/sketch/{sketch_id}/publish")
    assert res.status_code == 409

    # Confirm no archive directory was created (we don't do work on invalid state).
    tmp_path: Path = client.tmp_path  # type: ignore[attr-defined]
    assert not (tmp_path / "published" / sketch_id).exists()


def test_publish_unknown_sketch_404(client: TestClient) -> None:
    res = client.post("/api/sketch/sk-does-not-exist/publish")
    assert res.status_code == 404

"""Tests for the Phase 6 critic HTTP endpoints + send-back transition."""
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
    res = client.post(
        f"/api/sketch/{sketch_id}/approve_premise",
        json={"model_id": "claude-opus", "premise_index": 0},
    )
    assert res.status_code == 200, res.text
    res = client.post(f"/api/sketch/{sketch_id}/approve_storyboard")
    assert res.status_code == 200, res.text
    return sketch_id


def test_get_critic_returns_full_report(client: TestClient) -> None:
    sketch_id = _walk_to_critic_review(client)
    res = client.get(f"/api/sketch/{sketch_id}/critic")
    assert res.status_code == 200
    data = res.json()
    assert data["sketch_id"] == sketch_id
    assert data["status"] == "critic_review"
    report = data["critic_report"]
    assert report["adapter_id"] == "stub"
    assert report["overall_score"] >= 1
    assert "axes" in report
    assert "comedic_timing" in report["axes"]
    assert isinstance(report["issues"], list)
    assert isinstance(report["fix_suggestions"], list)
    assert "verdict" in report
    assert "scored_at" in report


def test_get_critic_unknown_404(client: TestClient) -> None:
    res = client.get("/api/sketch/sk-does-not-exist/critic")
    assert res.status_code == 404


def test_send_back_for_regen_returns_to_video_pending(client: TestClient) -> None:
    sketch_id = _walk_to_critic_review(client)
    res = client.post(f"/api/sketch/{sketch_id}/send_back_for_regen")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "video_pending"

    # The history trail records the new transition.
    history_steps = [(h["from"], h["to"]) for h in data["history"]]
    assert ("critic_review", "video_pending") in history_steps


def test_send_back_for_regen_unknown_404(client: TestClient) -> None:
    res = client.post("/api/sketch/sk-does-not-exist/send_back_for_regen")
    assert res.status_code == 404


def test_send_back_invalid_transition_409(client: TestClient) -> None:
    """Sending back from a non-CRITIC_REVIEW status should 409."""
    sketch_id = client.sketch_id  # type: ignore[attr-defined]
    # Sketch is still in PREMISE_REVIEW.
    res = client.post(f"/api/sketch/{sketch_id}/send_back_for_regen")
    assert res.status_code == 409


def test_critic_json_persists_on_disk(client: TestClient) -> None:
    sketch_id = _walk_to_critic_review(client)
    tmp_path: Path = client.tmp_path  # type: ignore[attr-defined]
    critic_json = tmp_path / "sketches" / sketch_id / "critic.json"
    assert critic_json.exists()
    payload = json.loads(critic_json.read_text(encoding="utf-8"))
    assert payload["sketch_id"] == sketch_id
    assert payload["adapter_id"] == "stub"
    assert payload["is_funny"] is True

"""Tests for the Phase 5 critic-review HTTP endpoints + Critic Review page wiring."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterator, List

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


def test_approve_storyboard_advances_to_critic_review(client: TestClient) -> None:
    sketch_id = _walk_to_critic_review(client)
    res = client.get(f"/api/sketch/{sketch_id}")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "critic_review"
    assert data["video_clips"]
    assert data["final_cut_path"]
    assert data["critic_report"]


def test_get_clips_endpoint_shape(client: TestClient) -> None:
    sketch_id = _walk_to_critic_review(client)
    res = client.get(f"/api/sketch/{sketch_id}/clips")
    assert res.status_code == 200
    data = res.json()
    assert data["sketch_id"] == sketch_id
    assert data["status"] == "critic_review"
    assert data["adapter_id"]
    assert data["clip_count"] >= 1
    assert data["final_url"]
    assert data["final_url"].endswith("final.mp4")
    for clip in data["clips"]:
        assert "beat_n" in clip
        assert "provider_id" in clip
        assert "url" in clip
        assert clip["url"].startswith("/data/sketches/")
        assert clip["url"].endswith(".mp4")


def test_clips_endpoint_404_for_unknown(client: TestClient) -> None:
    res = client.get("/api/sketch/sk-does-not-exist/clips")
    assert res.status_code == 404


def test_data_mount_serves_final_mp4(client: TestClient) -> None:
    sketch_id = _walk_to_critic_review(client)
    data = client.get(f"/api/sketch/{sketch_id}/clips").json()
    final_url = data["final_url"]
    res = client.get(final_url)
    assert res.status_code == 200
    assert len(res.content) > 0


def test_data_mount_serves_individual_clip(client: TestClient) -> None:
    sketch_id = _walk_to_critic_review(client)
    data = client.get(f"/api/sketch/{sketch_id}/clips").json()
    first = data["clips"][0]
    res = client.get(first["url"])
    assert res.status_code == 200
    assert len(res.content) > 0


def test_clips_json_persists_per_clip_metadata(client: TestClient) -> None:
    sketch_id = _walk_to_critic_review(client)
    tmp_path: Path = client.tmp_path  # type: ignore[attr-defined]
    clips_json = tmp_path / "sketches" / sketch_id / "clips.json"
    assert clips_json.exists()
    payload = json.loads(clips_json.read_text(encoding="utf-8"))
    assert payload["adapter_id"] == "stub-video-v1"
    assert payload["clip_count"] >= 1
    assert "max_cost_cents_per_sketch" in payload


def test_publish_after_critic_review_cleans_marker(client: TestClient) -> None:
    sketch_id = _walk_to_critic_review(client)
    res = client.post(f"/api/sketch/{sketch_id}/publish")
    assert res.status_code == 200
    assert res.json()["sketch"]["status"] == "published"

"""FastAPI endpoint tests."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Iterator

import pytest
from fastapi.testclient import TestClient

import backend.main as backend_main
from pipelines import run_skeleton
from state.machine import Status
from state.store import Store


@pytest.fixture()
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("AI_VIDS_DATA_ROOT", str(tmp_path))
    # Phase 4/5/6: force offline storyboard + video + critic pipelines
    # so test_api never shells out to Claude / Gemini / providers / critics.
    monkeypatch.setenv("AI_VIDS_OFFLINE_STORYBOARD", "1")
    monkeypatch.setenv("AI_VIDS_OFFLINE_VIDEO", "1")
    monkeypatch.setenv("AI_VIDS_OFFLINE_CRITIC", "1")
    monkeypatch.setenv("AI_VIDS_OFFLINE_PUBLISH", "1")
    with TestClient(backend_main.app) as test_client:
        yield test_client


FIXTURE_SOURCES = Path(__file__).resolve().parent / "fixtures" / "sources_stub_only.yaml"


@pytest.fixture()
def populated_client(client: TestClient) -> TestClient:
    root = Path(os.environ["AI_VIDS_DATA_ROOT"])
    run_skeleton.run(
        root=root,
        sources_path=FIXTURE_SOURCES,
        analyzer_threshold=0,
        use_stub_factory=True,
    )
    return client


def test_kanban_empty(client: TestClient) -> None:
    res = client.get("/api/kanban")
    assert res.status_code == 200
    data = res.json()
    for status in Status:
        assert status.value in data
        assert data[status.value] == []


def test_kanban_after_pipeline(populated_client: TestClient) -> None:
    res = populated_client.get("/api/kanban")
    assert res.status_code == 200
    data = res.json()
    assert len(data["premise_review"]) == 3


def test_get_sketch_404(client: TestClient) -> None:
    res = client.get("/api/sketch/sk-does-not-exist")
    assert res.status_code == 404


def test_get_sketch_ok(populated_client: TestClient) -> None:
    kanban = populated_client.get("/api/kanban").json()
    sketch_id = kanban["premise_review"][0]["id"]
    res = populated_client.get(f"/api/sketch/{sketch_id}")
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == sketch_id
    assert data["status"] == "premise_review"
    assert "premise" in data


def test_approve_premise_moves_to_storyboard_review(populated_client: TestClient) -> None:
    kanban = populated_client.get("/api/kanban").json()
    sketch_id = kanban["premise_review"][0]["id"]
    res = populated_client.post(f"/api/sketch/{sketch_id}/approve_premise")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "storyboard_review"
    assert data["beats"]
    assert data["storyboard_frames"]


def test_approve_storyboard_moves_to_critic_review(populated_client: TestClient) -> None:
    sketch_id = populated_client.get("/api/kanban").json()["premise_review"][0]["id"]
    populated_client.post(f"/api/sketch/{sketch_id}/approve_premise")
    res = populated_client.post(f"/api/sketch/{sketch_id}/approve_storyboard")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "critic_review"
    assert data["video_clips"]
    assert data["critic_report"]
    assert data["final_cut_path"]


def test_publish_moves_to_published(populated_client: TestClient) -> None:
    sketch_id = populated_client.get("/api/kanban").json()["premise_review"][0]["id"]
    populated_client.post(f"/api/sketch/{sketch_id}/approve_premise")
    populated_client.post(f"/api/sketch/{sketch_id}/approve_storyboard")
    res = populated_client.post(f"/api/sketch/{sketch_id}/publish")
    assert res.status_code == 200
    body = res.json()
    # Phase 7 wraps the sketch in a {sketch, results, ...} envelope.
    assert body["sketch"]["status"] == "published"
    assert body["success_count"] >= 1


def test_reject_from_premise_review(populated_client: TestClient) -> None:
    sketch_id = populated_client.get("/api/kanban").json()["premise_review"][0]["id"]
    res = populated_client.post(f"/api/sketch/{sketch_id}/reject")
    assert res.status_code == 200
    assert res.json()["status"] == "rejected"


def test_invalid_transition_returns_409(populated_client: TestClient) -> None:
    sketch_id = populated_client.get("/api/kanban").json()["premise_review"][0]["id"]
    # Try to publish straight from premise_review.
    res = populated_client.post(f"/api/sketch/{sketch_id}/publish")
    assert res.status_code == 409


def test_manual_idea_creates_sketch(client: TestClient) -> None:
    res = client.post("/api/manual_idea", json={"text": "a man buys a single grape on monday"})
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "premise_review"
    assert data["premise"]["logline"] == "a man buys a single grape on monday"


def test_manual_idea_rejects_empty(client: TestClient) -> None:
    res = client.post("/api/manual_idea", json={"text": "  "})
    assert res.status_code == 400


def test_index_serves_html(client: TestClient) -> None:
    res = client.get("/")
    assert res.status_code == 200
    assert "ai_vids_virality" in res.text

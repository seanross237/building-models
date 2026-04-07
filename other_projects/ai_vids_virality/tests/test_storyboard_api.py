"""Tests for the Phase 4 storyboard HTTP endpoints."""
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
from state.store import Sketch, Store


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
    # Seed a sketch in PREMISE_REVIEW with a variant file so approve_premise works.
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


def test_approve_premise_triggers_storyboard_pipeline(client: TestClient) -> None:
    sketch_id = client.sketch_id  # type: ignore[attr-defined]
    res = client.post(
        f"/api/sketch/{sketch_id}/approve_premise",
        json={"model_id": "claude-opus", "premise_index": 0},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "storyboard_review"
    assert data["beats"]
    assert data["storyboard_frames"]

    # Real files on disk (from the offline stub adapter).
    tmp_path: Path = client.tmp_path  # type: ignore[attr-defined]
    storyboard_dir = tmp_path / "sketches" / sketch_id / "storyboard"
    files = sorted(storyboard_dir.glob("*.png"))
    assert len(files) >= 1
    assert files[0].stat().st_size > 0

    refs_dir = tmp_path / "sketches" / sketch_id / "refs"
    assert refs_dir.exists()


def test_get_storyboard_endpoint_shape(client: TestClient) -> None:
    sketch_id = client.sketch_id  # type: ignore[attr-defined]
    client.post(
        f"/api/sketch/{sketch_id}/approve_premise",
        json={"model_id": "claude-opus", "premise_index": 0},
    )
    res = client.get(f"/api/sketch/{sketch_id}/storyboard")
    assert res.status_code == 200
    data = res.json()
    assert data["sketch_id"] == sketch_id
    assert data["status"] == "storyboard_review"
    assert isinstance(data["frames"], list)
    assert len(data["frames"]) >= 1
    for frame in data["frames"]:
        assert "beat_n" in frame
        assert "url" in frame
        assert frame["url"].startswith("/data/sketches/")
        assert frame["url"].endswith(".png")
    assert "characters" in data
    assert "beats" in data


def test_get_storyboard_unknown_404(client: TestClient) -> None:
    res = client.get("/api/sketch/sk-does-not-exist/storyboard")
    assert res.status_code == 404


def test_regenerate_frame_updates_file(client: TestClient) -> None:
    sketch_id = client.sketch_id  # type: ignore[attr-defined]
    tmp_path: Path = client.tmp_path  # type: ignore[attr-defined]
    client.post(
        f"/api/sketch/{sketch_id}/approve_premise",
        json={"model_id": "claude-opus", "premise_index": 0},
    )

    # Figure out an existing beat number.
    meta = client.get(f"/api/sketch/{sketch_id}/storyboard").json()
    beat_n = meta["frames"][0]["beat_n"]

    res = client.post(
        f"/api/sketch/{sketch_id}/storyboard/regenerate",
        json={"beat": beat_n},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["beat_n"] == beat_n
    assert data["url"].endswith(f"beat-{beat_n:02d}-start.png")

    # Frame file still exists.
    path = tmp_path / "sketches" / sketch_id / "storyboard" / f"beat-{beat_n:02d}-start.png"
    assert path.exists()
    assert path.stat().st_size > 0


def test_regenerate_frame_unknown_beat_400(client: TestClient) -> None:
    sketch_id = client.sketch_id  # type: ignore[attr-defined]
    client.post(
        f"/api/sketch/{sketch_id}/approve_premise",
        json={"model_id": "claude-opus", "premise_index": 0},
    )
    res = client.post(
        f"/api/sketch/{sketch_id}/storyboard/regenerate",
        json={"beat": 99},
    )
    assert res.status_code == 400


def test_data_mount_serves_generated_frame(client: TestClient) -> None:
    """The `/data` static mount should let the browser load generated PNGs."""
    sketch_id = client.sketch_id  # type: ignore[attr-defined]
    client.post(
        f"/api/sketch/{sketch_id}/approve_premise",
        json={"model_id": "claude-opus", "premise_index": 0},
    )
    meta = client.get(f"/api/sketch/{sketch_id}/storyboard").json()
    url = meta["frames"][0]["url"]
    res = client.get(url)
    assert res.status_code == 200
    assert res.headers["content-type"].startswith("image/")
    assert len(res.content) > 0

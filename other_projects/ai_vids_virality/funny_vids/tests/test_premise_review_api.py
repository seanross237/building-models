"""Tests for the Phase 3 premise-review API endpoints + leaderboard wiring."""
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
from state.store import Store


class FakeAdapter(ModelAdapter):
    def __init__(self, model_id: str, n: int = 3) -> None:
        super().__init__(config={})
        self.model_id = model_id
        self.n = n

    def is_available(self) -> bool:
        return True

    def generate(self, signal: Dict[str, Any], prompt: str, n_premises: int = 3) -> PremiseResult:
        return PremiseResult(
            model_id=self.model_id,
            signal_id=str(signal.get("signal_id", "")),
            premises=[
                Premise(
                    logline=f"{self.model_id} pitch #{i}",
                    synopsis=f"{self.model_id} synopsis #{i}",
                    tone=f"{self.model_id} tone",
                    target_length_sec=30,
                    characters=[{"name": "Riley", "description": "intern"}],
                    twist=f"{self.model_id} twist",
                )
                for i in range(min(n_premises, self.n))
            ],
        )


@pytest.fixture()
def populated_client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("AI_VIDS_DATA_ROOT", str(tmp_path))
    # Phase 4/5/6/7: force every downstream pipeline into offline mode.
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
            "title": "Senator caught using spoon as wifi antenna in committee hearing",
            "summary": "Brief summary",
        },
    )
    adapters: List[ModelAdapter] = [
        FakeAdapter("claude-opus"),
        FakeAdapter("gpt-5"),
        FakeAdapter("gemini-2.5-pro"),
    ]
    leaderboard = Leaderboard(tmp_path / "leaderboard.json")
    sketch_ids = run_factory(
        store,
        prompt_template="prompt {signal_title}",
        lens_text="lens",
        leaderboard=leaderboard,
        adapters=adapters,
    )
    assert len(sketch_ids) == 1

    with TestClient(backend_main.app) as client:
        client.test_sketch_id = sketch_ids[0]  # type: ignore[attr-defined]
        client.test_data_root = tmp_path  # type: ignore[attr-defined]
        yield client


def test_get_sketch_premises_returns_variants(populated_client: TestClient) -> None:
    sketch_id = populated_client.test_sketch_id  # type: ignore[attr-defined]
    res = populated_client.get(f"/api/sketch/{sketch_id}/premises")
    assert res.status_code == 200
    data = res.json()
    assert data["sketch_id"] == sketch_id
    assert data["status"] == "premise_review"
    variant_ids = sorted(v["model_id"] for v in data["variants"])
    assert variant_ids == ["claude-opus", "gemini-2.5-pro", "gpt-5"]
    for variant in data["variants"]:
        assert "premises" in variant
        assert len(variant["premises"]) == 3
        for p in variant["premises"]:
            assert "logline" in p
            assert "synopsis" in p
            assert "tone" in p


def test_get_sketch_premises_404_for_unknown(populated_client: TestClient) -> None:
    res = populated_client.get("/api/sketch/sk-does-not-exist/premises")
    assert res.status_code == 404


def test_approve_premise_with_model_id_picks_variant(populated_client: TestClient) -> None:
    sketch_id = populated_client.test_sketch_id  # type: ignore[attr-defined]
    res = populated_client.post(
        f"/api/sketch/{sketch_id}/approve_premise",
        json={"model_id": "gpt-5", "premise_index": 1},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "storyboard_review"
    assert data["premise"]["logline"] == "gpt-5 pitch #1"

    # Variant marker files should be cleared after approval.
    queue_dir = populated_client.test_data_root / "queues" / "premise-review"  # type: ignore[attr-defined]
    files = list(queue_dir.glob(f"{sketch_id}__*.json"))
    assert files == []


def test_approve_premise_updates_leaderboard(populated_client: TestClient) -> None:
    sketch_id = populated_client.test_sketch_id  # type: ignore[attr-defined]
    populated_client.post(
        f"/api/sketch/{sketch_id}/approve_premise",
        json={"model_id": "gpt-5", "premise_index": 0},
    )
    res = populated_client.get("/api/leaderboard")
    assert res.status_code == 200
    rows = {r["model_id"]: r for r in res.json()["models"]}
    assert rows["gpt-5"]["approved"] == 1
    assert rows["claude-opus"]["rejected"] == 1
    assert rows["gemini-2.5-pro"]["rejected"] == 1


def test_approve_premise_invalid_model_id_400(populated_client: TestClient) -> None:
    sketch_id = populated_client.test_sketch_id  # type: ignore[attr-defined]
    res = populated_client.post(
        f"/api/sketch/{sketch_id}/approve_premise",
        json={"model_id": "not-a-real-model", "premise_index": 0},
    )
    assert res.status_code == 400


def test_approve_premise_index_out_of_range_400(populated_client: TestClient) -> None:
    sketch_id = populated_client.test_sketch_id  # type: ignore[attr-defined]
    res = populated_client.post(
        f"/api/sketch/{sketch_id}/approve_premise",
        json={"model_id": "gpt-5", "premise_index": 99},
    )
    assert res.status_code == 400


def test_reject_increments_all_contributors(populated_client: TestClient) -> None:
    sketch_id = populated_client.test_sketch_id  # type: ignore[attr-defined]
    res = populated_client.post(f"/api/sketch/{sketch_id}/reject")
    assert res.status_code == 200
    rows = {r["model_id"]: r for r in populated_client.get("/api/leaderboard").json()["models"]}
    for model in ("claude-opus", "gpt-5", "gemini-2.5-pro"):
        assert rows[model]["rejected"] == 1


def test_leaderboard_endpoint_shape(populated_client: TestClient) -> None:
    res = populated_client.get("/api/leaderboard")
    assert res.status_code == 200
    data = res.json()
    assert "models" in data
    assert isinstance(data["models"], list)
    rows = {r["model_id"]: r for r in data["models"]}
    for model in ("claude-opus", "gpt-5", "gemini-2.5-pro"):
        assert rows[model]["total"] == 1
        assert "approval_rate" in rows[model]

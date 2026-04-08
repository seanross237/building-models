"""Phase 10: POST /api/sketch/{id}/premise adds a human-authored variant.

Also verifies the leaderboard counts the `human` row when the new premise
is approved downstream.
"""
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
    def __init__(self, model_id: str) -> None:
        super().__init__(config={})
        self.model_id = model_id

    def is_available(self) -> bool:
        return True

    def generate(
        self, signal: Dict[str, Any], prompt: str, n_premises: int = 3
    ) -> PremiseResult:
        return PremiseResult(
            model_id=self.model_id,
            signal_id=str(signal.get("signal_id", "")),
            premises=[
                Premise(
                    logline=f"{self.model_id} logline #{i}",
                    synopsis=f"{self.model_id} synopsis #{i}",
                    tone="dry",
                    target_length_sec=30,
                    characters=[],
                    twist="",
                )
                for i in range(n_premises)
            ],
        )


@pytest.fixture()
def populated_client(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> Iterator[TestClient]:
    monkeypatch.setenv("AI_VIDS_DATA_ROOT", str(tmp_path))
    monkeypatch.setenv("AI_VIDS_OFFLINE_STORYBOARD", "1")
    monkeypatch.setenv("AI_VIDS_OFFLINE_VIDEO", "1")
    monkeypatch.setenv("AI_VIDS_OFFLINE_CRITIC", "1")
    monkeypatch.setenv("AI_VIDS_OFFLINE_PUBLISH", "1")
    store = Store(root=tmp_path)
    store.write_queue_marker(
        "idea-factory",
        "sig-add-001",
        {
            "signal_id": "sig-add-001",
            "source": "reddit",
            "source_url": "https://example.com/r/1",
            "title": "Stoplight replaced with flag",
            "summary": "",
        },
    )
    adapters: List[ModelAdapter] = [FakeAdapter("gpt-5"), FakeAdapter("claude-opus")]
    sketch_ids = run_factory(
        store,
        prompt_template="prompt {signal_title}",
        lens_text="lens",
        leaderboard=Leaderboard(tmp_path / "leaderboard.json"),
        adapters=adapters,
    )
    assert len(sketch_ids) == 1

    with TestClient(backend_main.app) as client:
        client.test_sketch_id = sketch_ids[0]  # type: ignore[attr-defined]
        client.test_data_root = tmp_path  # type: ignore[attr-defined]
        yield client


def _read_human_variant(tmp_path: Path, sketch_id: str) -> Dict[str, Any]:
    path = tmp_path / "queues" / "premise-review" / f"{sketch_id}__human.json"
    return json.loads(path.read_text(encoding="utf-8"))


def _read_sketch(tmp_path: Path, sketch_id: str) -> Dict[str, Any]:
    return json.loads(
        (tmp_path / "sketches" / sketch_id / "sketch.json").read_text(encoding="utf-8")
    )


HUMAN_PREMISE = {
    "logline": "A human-written premise about traffic flags",
    "synopsis": "The city replaces stoplights with tiny colored flags. Chaos ensues.",
    "tone": "mockumentary",
    "target_length_sec": 30,
    "characters": [{"name": "Martha", "description": "crosswalk volunteer"}],
    "twist": "the flags were her idea",
}


def test_add_human_premise_creates_human_variant_marker(
    populated_client: TestClient,
) -> None:
    sketch_id = populated_client.test_sketch_id  # type: ignore[attr-defined]
    res = populated_client.post(
        f"/api/sketch/{sketch_id}/premise",
        json={"premise": HUMAN_PREMISE},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["model_id"] == "human"
    assert data["premise_index"] == 0
    assert data["variant_premise_count"] == 1

    variant = _read_human_variant(populated_client.test_data_root, sketch_id)  # type: ignore[attr-defined]
    assert variant["model_id"] == "human"
    assert len(variant["premises"]) == 1
    assert (
        variant["premises"][0]["logline"]
        == "A human-written premise about traffic flags"
    )


def test_add_human_premise_appends_to_existing_human_variant(
    populated_client: TestClient,
) -> None:
    sketch_id = populated_client.test_sketch_id  # type: ignore[attr-defined]
    populated_client.post(
        f"/api/sketch/{sketch_id}/premise",
        json={"premise": HUMAN_PREMISE},
    )
    second = dict(HUMAN_PREMISE)
    second["logline"] = "A second human premise"
    res2 = populated_client.post(
        f"/api/sketch/{sketch_id}/premise",
        json={"premise": second},
    )
    assert res2.status_code == 200
    assert res2.json()["premise_index"] == 1

    variant = _read_human_variant(populated_client.test_data_root, sketch_id)  # type: ignore[attr-defined]
    assert len(variant["premises"]) == 2
    assert variant["premises"][1]["logline"] == "A second human premise"


def test_add_human_premise_writes_history_event(populated_client: TestClient) -> None:
    sketch_id = populated_client.test_sketch_id  # type: ignore[attr-defined]
    populated_client.post(
        f"/api/sketch/{sketch_id}/premise",
        json={"premise": HUMAN_PREMISE},
    )
    sketch = _read_sketch(populated_client.test_data_root, sketch_id)  # type: ignore[attr-defined]
    events = [h.get("event") for h in sketch.get("history", []) if isinstance(h, dict)]
    assert "human_add_premise" in events


def test_approving_human_premise_increments_leaderboard(
    populated_client: TestClient,
) -> None:
    sketch_id = populated_client.test_sketch_id  # type: ignore[attr-defined]
    # Add the human premise first.
    populated_client.post(
        f"/api/sketch/{sketch_id}/premise",
        json={"premise": HUMAN_PREMISE},
    )
    # Now approve it with model_id="human".
    res = populated_client.post(
        f"/api/sketch/{sketch_id}/approve_premise",
        json={"model_id": "human", "premise_index": 0},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "storyboard_review"
    assert data["premise"]["logline"] == HUMAN_PREMISE["logline"]

    # Leaderboard should now have a `human` row with approved=1.
    board = populated_client.get("/api/leaderboard").json()
    rows = {r["model_id"]: r for r in board.get("models", [])}
    assert "human" in rows, f"expected human row, got {list(rows.keys())}"
    assert rows["human"]["approved"] == 1
    # The losing AI variants get rejected on the same call.
    for loser in ("gpt-5", "claude-opus"):
        assert rows[loser]["rejected"] == 1

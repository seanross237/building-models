"""Phase 10: PATCH /api/sketch/{id}/premise inline-edits a variant premise."""
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
                    characters=[{"name": "Riley", "description": "intern"}],
                    twist=f"{self.model_id} twist",
                )
                for i in range(n_premises)
            ],
        )


@pytest.fixture()
def populated_client(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> Iterator[TestClient]:
    monkeypatch.setenv("AI_VIDS_DATA_ROOT", str(tmp_path))
    store = Store(root=tmp_path)
    store.write_queue_marker(
        "idea-factory",
        "sig-edit-001",
        {
            "signal_id": "sig-edit-001",
            "source": "reddit",
            "source_url": "https://example.com/r/1",
            "title": "Senator caught with spoon antenna",
            "summary": "",
        },
    )
    adapters: List[ModelAdapter] = [
        FakeAdapter("claude-opus"),
        FakeAdapter("gpt-5"),
    ]
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


def _read_variant(tmp_path: Path, sketch_id: str, model_id: str) -> Dict[str, Any]:
    path = tmp_path / "queues" / "premise-review" / f"{sketch_id}__{model_id}.json"
    return json.loads(path.read_text(encoding="utf-8"))


def _read_sketch(tmp_path: Path, sketch_id: str) -> Dict[str, Any]:
    path = tmp_path / "sketches" / sketch_id / "sketch.json"
    return json.loads(path.read_text(encoding="utf-8"))


def test_edit_premise_updates_variant_in_place(populated_client: TestClient) -> None:
    sketch_id = populated_client.test_sketch_id  # type: ignore[attr-defined]
    res = populated_client.patch(
        f"/api/sketch/{sketch_id}/premise",
        json={
            "model_id": "gpt-5",
            "premise_index": 1,
            "premise": {
                "logline": "A human-edited logline",
                "synopsis": "edited synopsis",
                "tone": "producer-edited",
                "target_length_sec": 45,
                "characters": [{"name": "Alex", "description": "auditor"}],
                "twist": "producer twist",
            },
        },
    )
    assert res.status_code == 200
    data = res.json()
    assert data["model_id"] == "gpt-5"
    assert data["premise_index"] == 1
    assert data["premise"]["logline"] == "A human-edited logline"

    variant = _read_variant(populated_client.test_data_root, sketch_id, "gpt-5")  # type: ignore[attr-defined]
    assert variant["premises"][1]["logline"] == "A human-edited logline"
    assert variant["premises"][1]["tone"] == "producer-edited"
    assert variant["premises"][1]["target_length_sec"] == 45
    # Siblings unchanged.
    assert variant["premises"][0]["logline"] == "gpt-5 logline #0"
    assert variant["premises"][2]["logline"] == "gpt-5 logline #2"


def test_edit_premise_writes_human_edit_history_event(
    populated_client: TestClient,
) -> None:
    sketch_id = populated_client.test_sketch_id  # type: ignore[attr-defined]
    populated_client.patch(
        f"/api/sketch/{sketch_id}/premise",
        json={
            "model_id": "claude-opus",
            "premise_index": 0,
            "premise": {
                "logline": "new logline",
                "synopsis": "new synopsis",
                "tone": "new tone",
                "target_length_sec": 30,
                "characters": [],
                "twist": "",
            },
        },
    )
    sketch = _read_sketch(populated_client.test_data_root, sketch_id)  # type: ignore[attr-defined]
    events = [h.get("event") for h in sketch.get("history", []) if isinstance(h, dict)]
    assert "human_edit_premise" in events
    # The event payload should record which variant + which index.
    matching = [
        h
        for h in sketch.get("history", [])
        if isinstance(h, dict) and h.get("event") == "human_edit_premise"
    ]
    assert matching
    payload = matching[-1].get("payload") or {}
    assert payload.get("model_id") == "claude-opus"
    assert payload.get("premise_index") == 0
    assert payload.get("logline") == "new logline"


def test_edit_unknown_variant_returns_404(populated_client: TestClient) -> None:
    sketch_id = populated_client.test_sketch_id  # type: ignore[attr-defined]
    res = populated_client.patch(
        f"/api/sketch/{sketch_id}/premise",
        json={
            "model_id": "does-not-exist",
            "premise_index": 0,
            "premise": {
                "logline": "x",
                "synopsis": "y",
                "tone": "z",
                "target_length_sec": 30,
                "characters": [],
                "twist": "",
            },
        },
    )
    assert res.status_code == 404


def test_edit_out_of_range_index_returns_400(populated_client: TestClient) -> None:
    sketch_id = populated_client.test_sketch_id  # type: ignore[attr-defined]
    res = populated_client.patch(
        f"/api/sketch/{sketch_id}/premise",
        json={
            "model_id": "gpt-5",
            "premise_index": 999,
            "premise": {
                "logline": "x",
                "synopsis": "y",
                "tone": "z",
                "target_length_sec": 30,
                "characters": [],
                "twist": "",
            },
        },
    )
    assert res.status_code == 400


def test_edit_unknown_sketch_returns_404(populated_client: TestClient) -> None:
    res = populated_client.patch(
        "/api/sketch/sk-nope/premise",
        json={
            "model_id": "gpt-5",
            "premise_index": 0,
            "premise": {
                "logline": "x",
                "synopsis": "y",
                "tone": "z",
                "target_length_sec": 30,
                "characters": [],
                "twist": "",
            },
        },
    )
    assert res.status_code == 404

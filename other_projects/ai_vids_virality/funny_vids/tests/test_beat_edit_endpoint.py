"""Phase 10: PATCH /api/sketch/{id}/beat/{n} updates a single beat in place.

The endpoint writes the edited beat back into `sketch.beats` on
`sketch.json`, mirrors the full list into a new `beats.json` sidecar, and
appends a `human_edit_beat` event onto the sketch history.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterator

import pytest
from fastapi.testclient import TestClient

import backend.main as backend_main
from state.machine import Status
from state.store import Sketch, Store


def _seed_sketch_with_beats(store: Store, sketch_id: str) -> None:
    premise = {
        "logline": "A local cafe reckons with a surprise health inspection",
        "synopsis": "Three employees realize the inspector is here",
        "tone": "dry workplace",
        "target_length_sec": 30,
        "characters": [],
        "twist": "the inspector was a regular",
    }
    beats = [
        {
            "n": 1,
            "duration_sec": 6,
            "location": "cafe",
            "characters": [],
            "action": "establish: cafe mid-shift",
            "dialogue": None,
            "camera": "wide",
            "visual_note": "morning light",
        },
        {
            "n": 2,
            "duration_sec": 12,
            "location": "cafe",
            "characters": [],
            "action": "inspector arrives and clipboard appears",
            "dialogue": "just here for a muffin",
            "camera": "two-shot",
            "visual_note": "fluorescent",
        },
        {
            "n": 3,
            "duration_sec": 12,
            "location": "cafe",
            "characters": [],
            "action": "reveal the inspector was the regular",
            "dialogue": "you guys know me",
            "camera": "close-up",
            "visual_note": "punchline",
        },
    ]
    sketch = Sketch(
        id=sketch_id,
        status=Status.STORYBOARD_REVIEW,
        signal_id="sig-beat-001",
        premise=premise,
        premises=[premise],
        beats=beats,
    )
    # history starts empty; we just persist the pre-existing sketch
    store.save_sketch(sketch)


@pytest.fixture()
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("AI_VIDS_DATA_ROOT", str(tmp_path))
    store = Store(root=tmp_path)
    _seed_sketch_with_beats(store, "sk-beat-test-1")
    with TestClient(backend_main.app) as test_client:
        test_client.test_sketch_id = "sk-beat-test-1"  # type: ignore[attr-defined]
        test_client.test_data_root = tmp_path  # type: ignore[attr-defined]
        yield test_client


def _read_sketch(tmp_path: Path, sketch_id: str) -> Dict[str, Any]:
    return json.loads(
        (tmp_path / "sketches" / sketch_id / "sketch.json").read_text(encoding="utf-8")
    )


def _read_beats_sidecar(tmp_path: Path, sketch_id: str) -> Dict[str, Any]:
    return json.loads(
        (tmp_path / "sketches" / sketch_id / "beats.json").read_text(encoding="utf-8")
    )


def test_edit_beat_updates_sketch_beats_in_place(client: TestClient) -> None:
    sketch_id = client.test_sketch_id  # type: ignore[attr-defined]
    res = client.patch(
        f"/api/sketch/{sketch_id}/beat/2",
        json={
            "action": "inspector appears, entire cafe freezes",
            "dialogue": "just here for a scone",
            "location": "cafe counter",
        },
    )
    assert res.status_code == 200
    data = res.json()
    assert data["beat_n"] == 2
    assert data["beat"]["action"] == "inspector appears, entire cafe freezes"
    assert data["beat"]["dialogue"] == "just here for a scone"
    assert data["beat"]["location"] == "cafe counter"
    # Fields we didn't touch are preserved.
    assert data["beat"]["camera"] == "two-shot"

    # sketch.json on disk reflects the change.
    sketch = _read_sketch(client.test_data_root, sketch_id)  # type: ignore[attr-defined]
    beat2 = next(b for b in sketch["beats"] if b["n"] == 2)
    assert beat2["action"] == "inspector appears, entire cafe freezes"
    assert beat2["camera"] == "two-shot"
    # Siblings unchanged.
    beat1 = next(b for b in sketch["beats"] if b["n"] == 1)
    assert beat1["action"] == "establish: cafe mid-shift"


def test_edit_beat_writes_beats_json_sidecar(client: TestClient) -> None:
    sketch_id = client.test_sketch_id  # type: ignore[attr-defined]
    client.patch(
        f"/api/sketch/{sketch_id}/beat/3",
        json={"action": "close on the regular laughing"},
    )
    sidecar = _read_beats_sidecar(client.test_data_root, sketch_id)  # type: ignore[attr-defined]
    assert sidecar["sketch_id"] == sketch_id
    beat3 = next(b for b in sidecar["beats"] if b["n"] == 3)
    assert beat3["action"] == "close on the regular laughing"


def test_edit_beat_writes_human_edit_beat_history_event(client: TestClient) -> None:
    sketch_id = client.test_sketch_id  # type: ignore[attr-defined]
    client.patch(
        f"/api/sketch/{sketch_id}/beat/1",
        json={"visual_note": "afternoon light, dusty blinds"},
    )
    sketch = _read_sketch(client.test_data_root, sketch_id)  # type: ignore[attr-defined]
    matching = [
        h
        for h in sketch.get("history", [])
        if isinstance(h, dict) and h.get("event") == "human_edit_beat"
    ]
    assert matching, "expected at least one human_edit_beat event"
    payload = matching[-1].get("payload") or {}
    assert payload.get("beat_n") == 1
    assert "visual_note" in (payload.get("fields_updated") or [])


def test_edit_beat_unknown_sketch_returns_404(client: TestClient) -> None:
    res = client.patch(
        "/api/sketch/sk-does-not-exist/beat/1",
        json={"action": "x"},
    )
    assert res.status_code == 404


def test_edit_beat_unknown_beat_n_returns_404(client: TestClient) -> None:
    sketch_id = client.test_sketch_id  # type: ignore[attr-defined]
    res = client.patch(
        f"/api/sketch/{sketch_id}/beat/99",
        json={"action": "x"},
    )
    assert res.status_code == 404

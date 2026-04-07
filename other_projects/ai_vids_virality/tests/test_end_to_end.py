"""Headline integration test.

Walks a sketch from collection all the way to PUBLISHED via the API and
asserts that a real `final.mp4` file exists on disk at the end.
"""
from __future__ import annotations

import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import backend.main as backend_main
from pipelines import run_skeleton
from state.machine import Status
from state.store import Store


FIXTURE_SOURCES = Path(__file__).resolve().parent / "fixtures" / "sources_stub_only.yaml"


def test_full_pipeline_to_published(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AI_VIDS_DATA_ROOT", str(tmp_path))
    monkeypatch.setenv("AI_VIDS_OFFLINE_STORYBOARD", "1")
    monkeypatch.setenv("AI_VIDS_OFFLINE_VIDEO", "1")
    monkeypatch.setenv("AI_VIDS_OFFLINE_CRITIC", "1")
    monkeypatch.setenv("AI_VIDS_OFFLINE_PUBLISH", "1")

    summary = run_skeleton.run(
        root=tmp_path,
        sources_path=FIXTURE_SOURCES,
        analyzer_threshold=0,
        use_stub_factory=True,
    )
    assert len(summary["new_signals"]) == 3
    assert len(summary["analyzed"]) == 3
    assert len(summary["new_sketches"]) == 3

    store = Store(root=tmp_path)
    sketches = store.list_sketches()
    assert len(sketches) == 3
    assert all(s.status == Status.PREMISE_REVIEW for s in sketches)

    with TestClient(backend_main.app) as client:
        kanban = client.get("/api/kanban").json()
        assert len(kanban["premise_review"]) == 3
        sketch_id = kanban["premise_review"][0]["id"]

        res = client.post(f"/api/sketch/{sketch_id}/approve_premise")
        assert res.status_code == 200
        assert res.json()["status"] == "storyboard_review"

        res = client.post(f"/api/sketch/{sketch_id}/approve_storyboard")
        assert res.status_code == 200
        assert res.json()["status"] == "critic_review"

        res = client.post(f"/api/sketch/{sketch_id}/publish")
        assert res.status_code == 200
        body = res.json()
        # Phase 7: publish returns {sketch, results, success_count, destination_count}.
        assert body["sketch"]["status"] == "published"
        assert body["success_count"] >= 1
        assert any(r["destination_id"] == "local_archive" for r in body["results"])

    final_path = Store(root=tmp_path).sketch_final_path(sketch_id)
    assert final_path.exists(), f"expected final.mp4 at {final_path}"
    assert final_path.stat().st_size > 0

    final_sketch = Store(root=tmp_path).get_sketch(sketch_id)
    assert final_sketch.status == Status.PUBLISHED
    assert final_sketch.video_clips
    assert final_sketch.critic_report
    history_steps = [(h["from"], h["to"]) for h in final_sketch.history]
    assert ("premise_review", "scripted") in history_steps
    assert ("scripted", "storyboard_review") in history_steps
    assert ("storyboard_review", "video_pending") in history_steps
    assert ("video_pending", "critic_review") in history_steps
    assert ("critic_review", "published") in history_steps

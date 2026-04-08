"""Tests for the Phase 7 /api/stats/cost and /api/stats/insights endpoints."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Iterator

import pytest
from fastapi.testclient import TestClient

import backend.main as backend_main
from backend.stats import cost_stats, insights_stats
from state.machine import Status
from state.store import Sketch, Store


@pytest.fixture()
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("AI_VIDS_DATA_ROOT", str(tmp_path))
    with TestClient(backend_main.app) as test_client:
        test_client.tmp_path = tmp_path  # type: ignore[attr-defined]
        yield test_client


def _write_storyboard_json(store: Store, sketch_id: str, cost: int) -> None:
    (store.sketch_dir(sketch_id) / "storyboard.json").write_text(
        json.dumps(
            {
                "adapter_id": "gemini-2.5-flash-image",
                "characters": [{"cost_cents": cost}],
                "frames": [{"cost_cents": cost}, {"cost_cents": cost}],
            }
        ),
        encoding="utf-8",
    )


def _write_clips_json(store: Store, sketch_id: str, cost: int) -> None:
    (store.sketch_dir(sketch_id) / "clips.json").write_text(
        json.dumps(
            {
                "adapter_id": "kling",
                "clips": [
                    {"cost_cents": cost, "beat_n": 1},
                    {"cost_cents": cost, "beat_n": 2},
                ],
            }
        ),
        encoding="utf-8",
    )


def _write_critic_json(store: Store, sketch_id: str, cost: int) -> None:
    (store.sketch_dir(sketch_id) / "critic.json").write_text(
        json.dumps({"adapter_id": "gemini-2.5-pro", "cost_cents": cost}),
        encoding="utf-8",
    )


def _seed_sketch(
    store: Store,
    sketch_id: str,
    status: Status,
    premise_cost: int = 0,
    storyboard_cost: int = 0,
    video_cost: int = 0,
    critic_cost: int = 0,
    signal_prefix: str = "reddit-",
) -> Sketch:
    sketch = Sketch(
        id=sketch_id,
        status=status,
        signal_id=f"{signal_prefix}fake-{sketch_id}",
        premise={"logline": f"logline for {sketch_id}", "tone": "dry"},
    )
    if premise_cost > 0:
        sketch.history.append(
            {
                "from": None,
                "to": "premise_review",
                "at": "2026-04-06T10:00:00Z",
                "payload": {"variants": [{"model_id": "claude-opus", "cost_cents": premise_cost}]},
            }
        )
    store.save_sketch(sketch)
    if storyboard_cost > 0:
        _write_storyboard_json(store, sketch_id, storyboard_cost)
    if video_cost > 0:
        _write_clips_json(store, sketch_id, video_cost)
    if critic_cost > 0:
        _write_critic_json(store, sketch_id, critic_cost)
    return store.get_sketch(sketch_id)


# ----------------------------------------------------------------- cost_stats


def test_cost_stats_empty_store(tmp_path: Path) -> None:
    store = Store(root=tmp_path)
    data = cost_stats(store)
    assert data["sketch_count"] == 0
    for bucket in data["buckets"].values():
        assert bucket["total"] == 0
        assert all(v == 0 for v in bucket["per_stage"].values())
        assert bucket["per_provider"] == {}


def test_cost_stats_aggregates_per_stage(tmp_path: Path) -> None:
    store = Store(root=tmp_path)
    _seed_sketch(
        store,
        "sk-cost-001",
        Status.PREMISE_REVIEW,
        premise_cost=10,  # 1 variant × 10 cents
        storyboard_cost=5,  # 1 character + 2 frames × 5 = 15 total
        video_cost=50,  # 2 clips × 50 = 100 total
        critic_cost=4,
    )
    data = cost_stats(store)
    assert data["sketch_count"] == 1
    all_time = data["buckets"]["all_time"]
    assert all_time["per_stage"]["premise"] == 10
    assert all_time["per_stage"]["storyboard"] == 15
    assert all_time["per_stage"]["video"] == 100
    assert all_time["per_stage"]["critic"] == 4
    assert all_time["total"] == 10 + 15 + 100 + 4
    # Per-provider keys should carry the stage prefix.
    assert all_time["per_provider"]["video:kling"] == 100
    assert all_time["per_provider"]["premise:claude-opus"] == 10


def test_cost_stats_today_bucket_matches_recent_sketch(tmp_path: Path) -> None:
    store = Store(root=tmp_path)
    sketch = _seed_sketch(store, "sk-cost-today", Status.CRITIC_REVIEW, video_cost=25)
    # Force the sketch's updated_at to now so it lands in today's bucket.
    sketch.updated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    store.save_sketch(sketch)
    data = cost_stats(store)
    assert data["buckets"]["today"]["total"] >= 25
    assert data["buckets"]["all_time"]["total"] >= 25


def test_cost_stats_api_endpoint(client: TestClient) -> None:
    res = client.get("/api/stats/cost")
    assert res.status_code == 200
    data = res.json()
    for key in ("generated_at", "sketch_count", "buckets", "per_sketch"):
        assert key in data
    for bucket_key in ("today", "yesterday", "this_week", "all_time"):
        assert bucket_key in data["buckets"]


# ----------------------------------------------------------------- insights_stats


def test_insights_empty_store(tmp_path: Path) -> None:
    store = Store(root=tmp_path)
    data = insights_stats(store)
    assert data["top_approved"] == []
    assert data["per_source"] == []


def test_insights_groups_by_source_prefix(tmp_path: Path) -> None:
    store = Store(root=tmp_path)
    # Two published reddit sketches, one rejected hn sketch.
    _seed_sketch(store, "sk-ins-r1", Status.PUBLISHED, signal_prefix="reddit-")
    _seed_sketch(store, "sk-ins-r2", Status.PUBLISHED, signal_prefix="reddit-")
    _seed_sketch(store, "sk-ins-h1", Status.REJECTED, signal_prefix="hn-")
    _seed_sketch(store, "sk-ins-g1", Status.PUBLISHED, signal_prefix="gn-")
    _seed_sketch(store, "sk-ins-y1", Status.PUBLISHED, signal_prefix="yt-")
    _seed_sketch(store, "sk-ins-m1", Status.PUBLISHED, signal_prefix="manual-")

    data = insights_stats(store)
    rows = {row["source"]: row for row in data["per_source"]}
    assert rows["reddit"]["published"] == 2
    assert rows["reddit"]["approval_rate"] == 1.0
    assert rows["hacker_news"]["rejected"] == 1
    assert rows["hacker_news"]["approval_rate"] == 0.0
    assert rows["google_news"]["published"] == 1
    assert rows["youtube_trending"]["published"] == 1
    assert rows["manual"]["published"] == 1

    # Top approved loglines should include every published sketch (5 total).
    assert len(data["top_approved"]) == 5
    sources_in_top = {row["source"] for row in data["top_approved"]}
    assert sources_in_top == {"reddit", "google_news", "youtube_trending", "manual"}


def test_insights_top_n_respected(tmp_path: Path) -> None:
    store = Store(root=tmp_path)
    for i in range(15):
        _seed_sketch(store, f"sk-many-{i:02d}", Status.PUBLISHED)
    data = insights_stats(store, top_n=5)
    assert len(data["top_approved"]) == 5


def test_insights_api_endpoint(client: TestClient) -> None:
    res = client.get("/api/stats/insights")
    assert res.status_code == 200
    data = res.json()
    for key in ("generated_at", "window_days", "top_approved", "per_source"):
        assert key in data
    assert data["window_days"] == 30

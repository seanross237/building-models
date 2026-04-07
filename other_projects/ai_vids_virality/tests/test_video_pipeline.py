"""Tests for video_gen.pipeline.run_video_pipeline."""
from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional

import pytest

from state.machine import Status
from state.store import Sketch, Store
from storyboard.adapters.stub_storyboard import StubStoryboardAdapter
from video_gen.adapter import VideoClip, VideoProviderAdapter
from video_gen.adapters.stub_video import StubVideoAdapter
from video_gen.pipeline import run_video_pipeline


FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _make_video_pending_sketch(store: Store, sketch_id: str = "sk-test-video-001") -> Sketch:
    sketch = Sketch(
        id=sketch_id,
        status=Status.PREMISE_REVIEW,
        signal_id="test-signal-001",
        premise={
            "logline": "test logline",
            "synopsis": "test synopsis",
            "tone": "dry workplace",
            "target_length_sec": 30,
            "characters": [{"name": "Brent", "description": "press sec"}],
            "twist": "the twist",
        },
        beats=[
            {
                "n": 1,
                "duration_sec": 5,
                "location": "office",
                "characters": [{"name": "Brent", "description": "press sec"}],
                "action": "Brent enters",
                "dialogue": None,
                "camera": "wide",
                "visual_note": "morning light",
            },
            {
                "n": 2,
                "duration_sec": 5,
                "location": "office",
                "characters": [{"name": "Brent", "description": "press sec"}],
                "action": "Brent freezes",
                "dialogue": "log me",
                "camera": "close-up",
                "visual_note": "rigid pose",
            },
            {
                "n": 3,
                "duration_sec": 5,
                "location": "office",
                "characters": [{"name": "Brent", "description": "press sec"}],
                "action": "intern panics",
                "dialogue": None,
                "camera": "two-shot",
                "visual_note": "punchline framing",
            },
        ],
    )
    store.save_sketch(sketch)
    # Walk the state machine to VIDEO_PENDING.
    store.transition(sketch_id, Status.SCRIPTED, {"action": "test"})
    store.transition(sketch_id, Status.STORYBOARD_REVIEW, {"action": "test"})
    store.transition(sketch_id, Status.VIDEO_PENDING, {"action": "test"})
    return store.get_sketch(sketch_id)


def _seed_storyboard_frames(store: Store, sketch_id: str, beats: int) -> None:
    storyboard_dir = store.sketch_storyboard_dir(sketch_id)
    storyboard_dir.mkdir(parents=True, exist_ok=True)
    placeholder = Path(__file__).resolve().parents[1] / "storyboard" / "placeholder.png"
    for n in range(1, beats + 1):
        shutil.copyfile(placeholder, storyboard_dir / f"beat-{n:02d}-start.png")


# ----------------------------------------------------------------- happy path


def test_pipeline_end_to_end_with_stub(tmp_path: Path) -> None:
    store = Store(root=tmp_path)
    sketch = _make_video_pending_sketch(store)
    _seed_storyboard_frames(store, sketch.id, beats=3)

    meta = run_video_pipeline(
        store,
        sketch.id,
        adapter=StubVideoAdapter(),
    )

    reloaded = store.get_sketch(sketch.id)
    assert reloaded.status == Status.CRITIC_REVIEW
    assert len(reloaded.video_clips) == 3
    assert reloaded.final_cut_path

    # Per-beat clip files exist on disk.
    clips_dir = store.sketch_clips_dir(sketch.id)
    files = sorted(clips_dir.glob("beat-*.mp4"))
    assert len(files) == 3
    for f in files:
        assert f.stat().st_size > 0

    # final.mp4 exists.
    final = store.sketch_final_path(sketch.id)
    assert final.exists()
    assert final.stat().st_size > 0

    # clips.json metadata.
    clips_json = store.sketch_dir(sketch.id) / "clips.json"
    assert clips_json.exists()
    payload = json.loads(clips_json.read_text(encoding="utf-8"))
    assert payload["clip_count"] == 3
    assert payload["successful_clip_count"] == 3
    assert payload["adapter_id"] == "stub-video-v1"
    assert payload["cap_hit"] is False
    assert meta == payload


def test_pipeline_handles_missing_storyboard_frames(tmp_path: Path) -> None:
    """If the storyboard frames are missing, the pipeline still produces clips."""
    store = Store(root=tmp_path)
    sketch = _make_video_pending_sketch(store)
    # Intentionally do not seed any storyboard frames.

    run_video_pipeline(store, sketch.id, adapter=StubVideoAdapter())
    reloaded = store.get_sketch(sketch.id)
    assert reloaded.status == Status.CRITIC_REVIEW
    assert len(reloaded.video_clips) == 3
    for clip in reloaded.video_clips:
        # Each clip's error is set explaining the missing frame.
        assert clip.get("error")


# ----------------------------------------------------------------- cost cap


class _ExpensiveAdapter(VideoProviderAdapter):
    """Reports a fixed cost; useful for triggering the cap."""

    provider_id = "expensive"

    def __init__(self, cost: int) -> None:
        super().__init__(config={})
        self._cost = cost

    def is_available(self) -> bool:
        return True

    def estimated_cost_cents(self, duration_sec: float) -> int:
        return self._cost

    def generate(
        self,
        start_frame: Path,
        end_frame: Optional[Path],
        prompt: str,
        duration_sec: float,
        out_path: Path,
        beat_n: int = 1,
    ) -> VideoClip:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(b"FAKE_CLIP_BYTES")
        return VideoClip(
            beat_n=beat_n,
            path=out_path,
            provider_id=self.provider_id,
            duration_sec=duration_sec,
            cost_cents=self._cost,
        )


def test_cost_cap_stops_generation_early(tmp_path: Path) -> None:
    store = Store(root=tmp_path)
    sketch = _make_video_pending_sketch(store)
    _seed_storyboard_frames(store, sketch.id, beats=3)

    # Cap = 250 cents, each clip = 100 cents -> only 2 clips fit
    # (cumulative 0 + 100 = 100 OK, 100 + 100 = 200 OK, 200 + 100 = 300 > 250 STOP).
    cfg = {
        "routing": {"default": ["expensive"]},
        "budget": {"max_cost_cents_per_sketch": 250},
        "adapters": [],
    }
    adapter = _ExpensiveAdapter(cost=100)

    meta = run_video_pipeline(
        store,
        sketch.id,
        adapter=adapter,
        config=cfg,
    )

    assert meta["cap_hit"] is True
    assert meta["cap_hit_at_beat"] == 3
    assert meta["clip_count"] == 2
    assert meta["successful_clip_count"] == 2
    assert meta["total_cost_cents"] == 200

    # Sketch still transitioned to CRITIC_REVIEW so the pipeline isn't stuck.
    reloaded = store.get_sketch(sketch.id)
    assert reloaded.status == Status.CRITIC_REVIEW


def test_cost_cap_zero_disables_check(tmp_path: Path) -> None:
    """A cap of 0 should be treated as 'no cap' (matches yaml default ergonomics)."""
    store = Store(root=tmp_path)
    sketch = _make_video_pending_sketch(store)
    _seed_storyboard_frames(store, sketch.id, beats=3)

    cfg = {
        "routing": {"default": ["expensive"]},
        "budget": {"max_cost_cents_per_sketch": 0},
        "adapters": [],
    }
    meta = run_video_pipeline(
        store,
        sketch.id,
        adapter=_ExpensiveAdapter(cost=999),
        config=cfg,
    )
    assert meta["cap_hit"] is False
    assert meta["clip_count"] == 3


# ----------------------------------------------------------------- error isolation


class _FailingAdapter(VideoProviderAdapter):
    """Returns a clip with error set on every call. The pipeline must
    keep going and use the placeholder file the adapter copied."""

    provider_id = "failing"

    def is_available(self) -> bool:
        return True

    def estimated_cost_cents(self, duration_sec: float) -> int:
        return 0

    def generate(
        self,
        start_frame: Path,
        end_frame: Optional[Path],
        prompt: str,
        duration_sec: float,
        out_path: Path,
        beat_n: int = 1,
    ) -> VideoClip:
        from video_gen._common import copy_placeholder
        copy_placeholder(out_path)
        return VideoClip(
            beat_n=beat_n,
            path=out_path,
            provider_id=self.provider_id,
            duration_sec=duration_sec,
            error="simulated provider failure",
        )


def test_pipeline_continues_when_every_adapter_call_errors(tmp_path: Path) -> None:
    store = Store(root=tmp_path)
    sketch = _make_video_pending_sketch(store)
    _seed_storyboard_frames(store, sketch.id, beats=3)

    meta = run_video_pipeline(
        store,
        sketch.id,
        adapter=_FailingAdapter(),
    )

    reloaded = store.get_sketch(sketch.id)
    assert reloaded.status == Status.CRITIC_REVIEW
    assert meta["clip_count"] == 3
    assert meta["successful_clip_count"] == 0
    # Final cut still exists (placeholder bytes).
    assert store.sketch_final_path(sketch.id).exists()


def test_pipeline_no_transition_when_disabled(tmp_path: Path) -> None:
    store = Store(root=tmp_path)
    sketch = _make_video_pending_sketch(store)
    _seed_storyboard_frames(store, sketch.id, beats=3)
    run_video_pipeline(
        store,
        sketch.id,
        adapter=StubVideoAdapter(),
        transition=False,
    )
    reloaded = store.get_sketch(sketch.id)
    assert reloaded.status == Status.VIDEO_PENDING
    # Clips still made it to disk (one per beat).
    assert len(reloaded.video_clips) == 3

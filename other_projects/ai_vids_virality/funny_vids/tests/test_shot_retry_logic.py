"""Tests for the Phase 6 shot-level retry loop in video_gen.pipeline."""
from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional

import pytest

from critic.adapter import CriticAdapter, ShotReport, SketchCritique
from state.machine import Status
from state.store import Sketch, Store
from video_gen.adapter import VideoClip, VideoProviderAdapter
from video_gen.pipeline import run_video_pipeline


# ----------------------------------------------------------------- doubles


class _CountingVideoAdapter(VideoProviderAdapter):
    """Counts how many times generate() is called per beat."""

    provider_id = "counting"

    def __init__(self) -> None:
        super().__init__(config={})
        self.calls_per_beat: Dict[int, int] = {}

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
        self.calls_per_beat[beat_n] = self.calls_per_beat.get(beat_n, 0) + 1
        # Write a tiny non-empty file so the stitcher has something to chew on.
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(b"FAKE_CLIP_BYTES")
        return VideoClip(
            beat_n=beat_n,
            path=out_path,
            provider_id=self.provider_id,
            duration_sec=duration_sec,
        )


class _ScriptedCritic(CriticAdapter):
    """Returns a scripted sequence of pass/fail responses keyed by beat number."""

    adapter_id = "scripted"

    def __init__(self, script: Dict[int, List[bool]]) -> None:
        super().__init__(config={})
        self.script: Dict[int, List[bool]] = {k: list(v) for k, v in script.items()}
        self.calls_per_beat: Dict[int, int] = {}

    def is_available(self) -> bool:
        return True

    def check_shot(
        self,
        clip_path: Path,
        expected_frame: Path,
        character_refs: List[Path],
        beat_metadata: Dict[str, Any],
    ) -> ShotReport:
        beat_n = int(beat_metadata.get("n", 1) or 1)
        self.calls_per_beat[beat_n] = self.calls_per_beat.get(beat_n, 0) + 1
        sequence = self.script.get(beat_n, [True])
        idx = self.calls_per_beat[beat_n] - 1
        passed = sequence[idx] if idx < len(sequence) else sequence[-1]
        return ShotReport(
            beat_n=beat_n,
            passed=passed,
            score=8 if passed else 3,
            issues=[] if passed else [f"scripted failure attempt {idx + 1}"],
            adapter_id=self.adapter_id,
        )

    def critique_sketch(
        self,
        final_cut_path: Path,
        sketch_metadata: Dict[str, Any],
    ) -> SketchCritique:
        return SketchCritique(
            sketch_id=str(sketch_metadata.get("sketch_id", "")),
            overall_score=7,
            adapter_id=self.adapter_id,
        )


# ----------------------------------------------------------------- fixture


def _seed_sketch(store: Store, beat_count: int = 2, sketch_id: str = "sk-test-retry-001") -> Sketch:
    sketch = Sketch(
        id=sketch_id,
        status=Status.PREMISE_REVIEW,
        signal_id="test-sig",
        premise={
            "logline": "x",
            "synopsis": "y",
            "tone": "dry",
            "target_length_sec": 30,
            "characters": [],
            "twist": "z",
        },
        beats=[
            {
                "n": i + 1,
                "duration_sec": 5,
                "location": "office",
                "characters": [],
                "action": f"beat {i + 1}",
                "dialogue": None,
                "camera": "wide",
                "visual_note": "",
            }
            for i in range(beat_count)
        ],
    )
    store.save_sketch(sketch)
    store.transition(sketch_id, Status.SCRIPTED, {})
    store.transition(sketch_id, Status.STORYBOARD_REVIEW, {})
    store.transition(sketch_id, Status.VIDEO_PENDING, {})
    # Seed storyboard frames so the pipeline doesn't fall back to placeholders.
    storyboard_dir = store.sketch_storyboard_dir(sketch_id)
    storyboard_dir.mkdir(parents=True, exist_ok=True)
    placeholder = Path(__file__).resolve().parents[1] / "storyboard" / "placeholder.png"
    for i in range(beat_count):
        shutil.copyfile(placeholder, storyboard_dir / f"beat-{i + 1:02d}-start.png")
    return store.get_sketch(sketch_id)


# ----------------------------------------------------------------- tests


def test_pipeline_regenerates_twice_when_critic_fails_twice(tmp_path: Path) -> None:
    """The headline retry test: critic fails on attempts 1 + 2, passes on 3."""
    store = Store(root=tmp_path)
    _seed_sketch(store, beat_count=1)

    video = _CountingVideoAdapter()
    critic = _ScriptedCritic({1: [False, False, True]})

    meta = run_video_pipeline(
        store,
        "sk-test-retry-001",
        adapter=video,
        critic_adapter=critic,
        max_retries=2,
    )

    # Three total generate() calls: initial + 2 retries.
    assert video.calls_per_beat[1] == 3
    assert critic.calls_per_beat[1] == 3
    # Pipeline should have advanced to CRITIC_REVIEW since the third attempt
    # passed and the clip is good.
    sketch = store.get_sketch("sk-test-retry-001")
    assert sketch.status == Status.CRITIC_REVIEW
    assert len(sketch.video_clips) == 1
    assert sketch.video_clips[0].get("error") is None
    # The shot_reports trail should record all three attempts.
    assert len(meta["shot_reports"]) == 3
    assert [r["passed"] for r in meta["shot_reports"]] == [False, False, True]
    assert [r["attempt"] for r in meta["shot_reports"]] == [1, 2, 3]


def test_pipeline_stops_at_first_pass(tmp_path: Path) -> None:
    """If the critic passes on the first try, no retry."""
    store = Store(root=tmp_path)
    _seed_sketch(store, beat_count=2)

    video = _CountingVideoAdapter()
    critic = _ScriptedCritic({1: [True], 2: [True]})

    meta = run_video_pipeline(
        store,
        "sk-test-retry-001",
        adapter=video,
        critic_adapter=critic,
        max_retries=2,
    )

    assert video.calls_per_beat == {1: 1, 2: 1}
    assert critic.calls_per_beat == {1: 1, 2: 1}
    assert len(meta["shot_reports"]) == 2
    assert all(r["passed"] for r in meta["shot_reports"])


def test_pipeline_gives_up_after_max_retries(tmp_path: Path) -> None:
    """When all attempts fail, the clip's error is set and the pipeline moves on."""
    store = Store(root=tmp_path)
    _seed_sketch(store, beat_count=1)

    video = _CountingVideoAdapter()
    critic = _ScriptedCritic({1: [False, False, False]})

    meta = run_video_pipeline(
        store,
        "sk-test-retry-001",
        adapter=video,
        critic_adapter=critic,
        max_retries=2,
    )

    # 3 total attempts (1 initial + 2 retries), all failed.
    assert video.calls_per_beat[1] == 3
    assert critic.calls_per_beat[1] == 3

    # The pipeline must keep going. Sketch ends in CRITIC_REVIEW so a
    # human can decide what to do next.
    sketch = store.get_sketch("sk-test-retry-001")
    assert sketch.status == Status.CRITIC_REVIEW
    # The clip's error field surfaces the failure for the UI.
    assert len(sketch.video_clips) == 1
    assert sketch.video_clips[0].get("error")
    assert "shot check failed after 3 attempts" in sketch.video_clips[0]["error"]
    assert len(meta["shot_reports"]) == 3
    assert not any(r["passed"] for r in meta["shot_reports"])


def test_pipeline_retries_disabled_when_max_retries_zero(tmp_path: Path) -> None:
    """`max_retries=0` skips the critic check entirely (one attempt per beat)."""
    store = Store(root=tmp_path)
    _seed_sketch(store, beat_count=2)

    video = _CountingVideoAdapter()
    critic = _ScriptedCritic({1: [False], 2: [False]})  # would fail if called

    meta = run_video_pipeline(
        store,
        "sk-test-retry-001",
        adapter=video,
        critic_adapter=critic,
        max_retries=0,
    )

    assert video.calls_per_beat == {1: 1, 2: 1}
    # Critic was never invoked because retries are disabled.
    assert critic.calls_per_beat == {}
    assert meta["shot_reports"] == []


def test_pipeline_skips_retries_on_provider_error(tmp_path: Path) -> None:
    """Provider errors short-circuit the retry loop — we don't retry on our own bugs."""
    store = Store(root=tmp_path)
    _seed_sketch(store, beat_count=1)

    class _ErrorAdapter(VideoProviderAdapter):
        provider_id = "error"

        def __init__(self) -> None:
            super().__init__(config={})
            self.calls = 0

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
            self.calls += 1
            from video_gen._common import copy_placeholder
            copy_placeholder(out_path)
            return VideoClip(
                beat_n=beat_n,
                path=out_path,
                provider_id=self.provider_id,
                duration_sec=duration_sec,
                error="simulated provider failure",
            )

    video = _ErrorAdapter()
    critic = _ScriptedCritic({1: [False, False, True]})

    run_video_pipeline(
        store,
        "sk-test-retry-001",
        adapter=video,
        critic_adapter=critic,
        max_retries=2,
    )

    # Provider returned an error on the first call -> no retry.
    assert video.calls == 1
    assert critic.calls_per_beat == {}


def test_critic_check_exception_does_not_retry(tmp_path: Path) -> None:
    """If the critic itself raises, we keep the clip and move on."""
    store = Store(root=tmp_path)
    _seed_sketch(store, beat_count=1)

    class _RaisingCritic(CriticAdapter):
        adapter_id = "raises"

        def __init__(self) -> None:
            super().__init__(config={})
            self.calls = 0

        def is_available(self) -> bool:
            return True

        def check_shot(self, clip_path, expected_frame, character_refs, beat_metadata):
            self.calls += 1
            raise RuntimeError("critic kaboom")

        def critique_sketch(self, final_cut_path, sketch_metadata):
            return SketchCritique(sketch_id="x", overall_score=0, adapter_id=self.adapter_id)

    video = _CountingVideoAdapter()
    critic = _RaisingCritic()

    run_video_pipeline(
        store,
        "sk-test-retry-001",
        adapter=video,
        critic_adapter=critic,
        max_retries=2,
    )

    assert video.calls_per_beat[1] == 1  # no retry on critic exception
    assert critic.calls == 1

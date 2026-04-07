"""Tests for critic.pipeline orchestration."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import pytest

from critic.adapter import CriticAdapter, ShotReport, SketchCritique
from critic.adapters.stub_critic import StubCritic
from critic.pipeline import (
    get_max_retries,
    load_critic_adapters,
    load_critic_config,
    run_full_critique,
    select_critic_adapter,
)
from state.machine import Status
from state.store import Sketch, Store


def _seed_sketch_with_final_cut(store: Store, sketch_id: str = "sk-critic-pipe-001") -> Sketch:
    sketch = Sketch(
        id=sketch_id,
        status=Status.CRITIC_REVIEW,
        signal_id="test-sig",
        premise={
            "logline": "intern types statement",
            "synopsis": "x",
            "tone": "dry workplace",
            "target_length_sec": 30,
            "characters": [],
            "twist": "they all freeze",
        },
        beats=[{"n": 1, "duration_sec": 5}, {"n": 2, "duration_sec": 5}],
    )
    store.save_sketch(sketch)
    final = store.sketch_final_path(sketch_id)
    final.parent.mkdir(parents=True, exist_ok=True)
    final.write_bytes(b"\x00\x00\x00\x18ftypisom\x00\x00\x02\x00isomiso2mp41")
    return store.get_sketch(sketch_id)


# ----------------------------------------------------------------- config


def test_load_critic_config_returns_defaults_when_missing(tmp_path: Path) -> None:
    cfg = load_critic_config(tmp_path / "nonexistent.yaml")
    assert "shot_check" in cfg
    assert "routing" in cfg
    assert cfg["shot_check"]["max_retries"] == 2


def test_get_max_retries_default() -> None:
    assert get_max_retries() == 2


def test_get_max_retries_zero_when_disabled() -> None:
    cfg = {"shot_check": {"enabled": False, "max_retries": 5}}
    assert get_max_retries(cfg) == 0


# ----------------------------------------------------------------- adapter selection


def test_select_critic_falls_back_to_stub_when_unavailable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.setattr(
        "critic.adapters.claude_frame.shutil.which",
        lambda name: None,
    )
    adapter = select_critic_adapter()
    # The yaml `id` field overrides the class-level adapter_id, so the
    # routed stub instance carries the yaml id "stub" not "stub-critic-v1".
    assert adapter.adapter_id == "stub"


def test_select_critic_prefers_gemini_when_key_set(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")
    adapter = select_critic_adapter()
    assert adapter.adapter_id == "gemini-video"


def test_load_critic_adapters_loads_all_enabled() -> None:
    adapters = load_critic_adapters()
    for expected in ("gemini-video", "claude-frame", "stub"):
        assert expected in adapters


# ----------------------------------------------------------------- run_full_critique


def test_run_full_critique_writes_critic_json(tmp_path: Path) -> None:
    store = Store(root=tmp_path)
    sketch = _seed_sketch_with_final_cut(store)

    critique = run_full_critique(store, sketch.id, adapter=StubCritic())

    assert isinstance(critique, SketchCritique)
    assert critique.sketch_id == sketch.id
    assert critique.adapter_id == "stub-critic-v1"  # bare StubCritic() instance, not yaml-routed
    assert critique.is_funny is True

    critic_json = store.sketch_dir(sketch.id) / "critic.json"
    assert critic_json.exists()
    payload = json.loads(critic_json.read_text(encoding="utf-8"))
    assert payload["sketch_id"] == sketch.id
    assert payload["overall_score"] >= 1
    assert "axes" in payload
    assert payload["adapter_id"] == "stub-critic-v1"  # bare StubCritic() instance
    assert "scored_at" in payload

    # The sketch's critic_report field is populated as well.
    reloaded = store.get_sketch(sketch.id)
    assert reloaded.critic_report
    assert reloaded.critic_report["overall_score"] == payload["overall_score"]


def test_run_full_critique_handles_adapter_error(tmp_path: Path) -> None:
    store = Store(root=tmp_path)
    sketch = _seed_sketch_with_final_cut(store)

    class _ErrorCritic(CriticAdapter):
        adapter_id = "error-critic"

        def is_available(self) -> bool:
            return True

        def check_shot(self, clip_path, expected_frame, character_refs, beat_metadata):
            return ShotReport(beat_n=1, passed=True, score=0, adapter_id=self.adapter_id)

        def critique_sketch(self, final_cut_path, sketch_metadata):
            return SketchCritique(
                sketch_id=str(sketch_metadata.get("sketch_id", "")),
                overall_score=0,
                adapter_id=self.adapter_id,
                error="simulated error",
            )

    critique = run_full_critique(store, sketch.id, adapter=_ErrorCritic())
    assert critique.error == "simulated error"
    # critic.json is still written so the UI has something to show.
    critic_json = store.sketch_dir(sketch.id) / "critic.json"
    assert critic_json.exists()
    payload = json.loads(critic_json.read_text(encoding="utf-8"))
    assert payload["error"] == "simulated error"


def test_run_full_critique_metadata_passes_premise(tmp_path: Path) -> None:
    """The metadata dict handed to the adapter includes the premise fields."""
    store = Store(root=tmp_path)
    sketch = _seed_sketch_with_final_cut(store)

    captured: Dict[str, Any] = {}

    class _CapturingCritic(CriticAdapter):
        adapter_id = "capturing"

        def is_available(self) -> bool:
            return True

        def check_shot(self, *args, **kwargs):
            return ShotReport(beat_n=1, passed=True, score=0, adapter_id=self.adapter_id)

        def critique_sketch(self, final_cut_path, sketch_metadata):
            captured.update(sketch_metadata)
            return SketchCritique(
                sketch_id=str(sketch_metadata.get("sketch_id", "")),
                overall_score=7,
                adapter_id=self.adapter_id,
            )

    run_full_critique(store, sketch.id, adapter=_CapturingCritic())
    assert captured["logline"] == "intern types statement"
    assert captured["tone"] == "dry workplace"
    assert captured["twist"] == "they all freeze"
    assert captured["beat_count"] == 2

"""Tests for storyboard.pipeline.run_storyboard."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import pytest

from idea_factory.adapter import ModelAdapter, PremiseResult
from state.machine import Status
from state.store import Sketch, Store
from storyboard.adapters.stub_storyboard import StubStoryboardAdapter
from storyboard.pipeline import regenerate_frame, run_storyboard, select_storyboard_adapter


FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _load_premise() -> Dict[str, Any]:
    return json.loads((FIXTURES / "sample_premise.json").read_text(encoding="utf-8"))


def _make_scripted_sketch(store: Store, sketch_id: str = "sk-test-storyboard-001") -> Sketch:
    sketch = Sketch(
        id=sketch_id,
        status=Status.PREMISE_REVIEW,
        signal_id="test-signal-001",
        premise=_load_premise(),
    )
    store.save_sketch(sketch)
    # Transition PREMISE_REVIEW -> SCRIPTED manually so run_storyboard sees it
    # in the right state (it's a valid transition even though the pipeline
    # itself doesn't advance SCRIPTED -> STORYBOARD_REVIEW until the end).
    store.transition(sketch_id, Status.SCRIPTED, {"action": "test_setup"})
    return store.get_sketch(sketch_id)


class FakeClaude(ModelAdapter):
    """Returns a fixed beat sheet JSON so the test is deterministic."""

    model_id = "fake-claude"

    def is_available(self) -> bool:
        return True

    def generate(self, signal, prompt, n_premises=3):  # type: ignore[override]
        return PremiseResult(
            model_id=self.model_id,
            signal_id=str(signal.get("signal_id", "")),
            raw_response=json.dumps(
                {
                    "beats": [
                        {
                            "n": 1,
                            "duration_sec": 5,
                            "location": "beige office",
                            "characters": [{"name": "Brent", "description": "press sec"}],
                            "action": "Brent hands Kyle the clipboard",
                            "dialogue": None,
                            "camera": "wide",
                            "visual_note": "fluorescent",
                        },
                        {
                            "n": 2,
                            "duration_sec": 6,
                            "location": "beige office",
                            "characters": [{"name": "Kyle", "description": "intern"}],
                            "action": "Kyle checks the first box",
                            "dialogue": None,
                            "camera": "close-up",
                            "visual_note": "nervous fingers",
                        },
                        {
                            "n": 3,
                            "duration_sec": 6,
                            "location": "beige office",
                            "characters": [
                                {"name": "Brent", "description": "press sec"},
                                {"name": "Kyle", "description": "intern"},
                            ],
                            "action": "Brent freezes rigid",
                            "dialogue": "Log me.",
                            "camera": "two-shot",
                            "visual_note": "stillness",
                        },
                    ]
                }
            ),
        )


def test_run_storyboard_end_to_end_with_stub(tmp_path: Path) -> None:
    store = Store(root=tmp_path)
    sketch = _make_scripted_sketch(store)
    sketch_id = sketch.id

    meta = run_storyboard(
        store,
        sketch_id,
        model_adapter=FakeClaude(),
        storyboard_adapter=StubStoryboardAdapter(),
    )

    reloaded = store.get_sketch(sketch_id)
    assert reloaded.status == Status.STORYBOARD_REVIEW
    assert len(reloaded.beats) == 3
    assert len(reloaded.storyboard_frames) == 3

    # Frame files exist on disk with the expected naming.
    for beat_n in (1, 2, 3):
        path = store.sketch_storyboard_dir(sketch_id) / f"beat-{beat_n:02d}-start.png"
        assert path.exists()
        assert path.stat().st_size > 0

    # Character ref files exist — one per unique character.
    refs_dir = store.sketch_refs_dir(sketch_id)
    ref_files = sorted(refs_dir.glob("*.png"))
    assert len(ref_files) == 2  # Brent + Kyle
    slugs = {f.stem for f in ref_files}
    assert slugs == {"brent", "kyle"}

    # storyboard.json metadata matches.
    storyboard_json = store.sketch_dir(sketch_id) / "storyboard.json"
    assert storyboard_json.exists()
    meta = json.loads(storyboard_json.read_text(encoding="utf-8"))
    assert len(meta["frames"]) == 3
    assert len(meta["characters"]) == 2
    assert meta["adapter_id"] == "stub-storyboard-v1"


def test_run_storyboard_uses_fallback_beat_when_model_errors(tmp_path: Path) -> None:
    """When the LLM returns an error, beats.generate_beats falls back to a
    single beat and the pipeline still produces a valid storyboard."""
    store = Store(root=tmp_path)
    sketch = _make_scripted_sketch(store)

    class ErrorAdapter(ModelAdapter):
        model_id = "error-llm"

        def is_available(self) -> bool:
            return True

        def generate(self, signal, prompt, n_premises=3):  # type: ignore[override]
            return PremiseResult(
                model_id=self.model_id,
                signal_id=str(signal.get("signal_id", "")),
                error="simulated error",
            )

    run_storyboard(
        store,
        sketch.id,
        model_adapter=ErrorAdapter(),
        storyboard_adapter=StubStoryboardAdapter(),
    )
    reloaded = store.get_sketch(sketch.id)
    assert reloaded.status == Status.STORYBOARD_REVIEW
    assert len(reloaded.beats) >= 1
    assert len(reloaded.storyboard_frames) >= 1


def test_select_storyboard_adapter_without_gemini_key(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    adapter = select_storyboard_adapter()
    assert adapter.adapter_id == "stub-storyboard-v1"


def test_select_storyboard_adapter_prefers_gemini_when_key_set(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")
    adapter = select_storyboard_adapter()
    assert adapter.adapter_id == "gemini-2.5-flash-image"


def test_regenerate_frame_rewrites_single_file(tmp_path: Path) -> None:
    store = Store(root=tmp_path)
    sketch = _make_scripted_sketch(store)
    run_storyboard(
        store,
        sketch.id,
        model_adapter=FakeClaude(),
        storyboard_adapter=StubStoryboardAdapter(),
    )

    beat_n = 2
    path = store.sketch_storyboard_dir(sketch.id) / f"beat-{beat_n:02d}-start.png"
    original_mtime = path.stat().st_mtime_ns
    original_size = path.stat().st_size

    new_frame = regenerate_frame(
        store,
        sketch.id,
        beat_n,
        storyboard_adapter=StubStoryboardAdapter(),
    )
    assert new_frame["beat_n"] == beat_n
    assert new_frame["error"] is None
    # File exists, same size (stub just rewrites the placeholder).
    assert path.exists()
    assert path.stat().st_size == original_size

    # storyboard.json now has the regenerated marker.
    storyboard_json = store.sketch_dir(sketch.id) / "storyboard.json"
    meta = json.loads(storyboard_json.read_text(encoding="utf-8"))
    assert meta["regenerated_beat"] == beat_n


def test_regenerate_frame_unknown_beat_raises(tmp_path: Path) -> None:
    store = Store(root=tmp_path)
    sketch = _make_scripted_sketch(store)
    run_storyboard(
        store,
        sketch.id,
        model_adapter=FakeClaude(),
        storyboard_adapter=StubStoryboardAdapter(),
    )
    with pytest.raises(ValueError):
        regenerate_frame(
            store,
            sketch.id,
            99,
            storyboard_adapter=StubStoryboardAdapter(),
        )


def test_run_storyboard_without_transition(tmp_path: Path) -> None:
    """When transition=False the pipeline leaves the sketch in SCRIPTED."""
    store = Store(root=tmp_path)
    sketch = _make_scripted_sketch(store)
    run_storyboard(
        store,
        sketch.id,
        model_adapter=FakeClaude(),
        storyboard_adapter=StubStoryboardAdapter(),
        transition=False,
    )
    reloaded = store.get_sketch(sketch.id)
    assert reloaded.status == Status.SCRIPTED
    assert len(reloaded.beats) == 3

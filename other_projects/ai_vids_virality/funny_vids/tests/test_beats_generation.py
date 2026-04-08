"""Tests for storyboard.beats.generate_beats."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import pytest

from idea_factory.adapter import ModelAdapter, PremiseResult
from state.machine import Status
from state.store import Sketch
from storyboard.beats import generate_beats


FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _load_sample_premise() -> Dict[str, Any]:
    return json.loads((FIXTURES / "sample_premise.json").read_text(encoding="utf-8"))


class FakeModelAdapter(ModelAdapter):
    """Returns a pre-baked raw_response string, letting tests simulate any LLM output."""

    model_id = "fake-llm"

    def __init__(self, raw_response: str = "", error: str = None, raises: bool = False) -> None:
        super().__init__(config={})
        self._raw = raw_response
        self._error = error
        self._raises = raises

    def is_available(self) -> bool:
        return True

    def generate(self, signal: Dict[str, Any], prompt: str, n_premises: int = 3) -> PremiseResult:
        if self._raises:
            raise RuntimeError("boom")
        return PremiseResult(
            model_id=self.model_id,
            signal_id=str(signal.get("signal_id", "")),
            raw_response=self._raw,
            error=self._error,
        )


def _make_sketch() -> Sketch:
    return Sketch(
        id="sk-test-beats-001",
        status=Status.SCRIPTED,
        signal_id="test-signal-001",
        premise=_load_sample_premise(),
    )


def _valid_beat_json() -> str:
    return json.dumps(
        {
            "beats": [
                {
                    "n": 1,
                    "duration_sec": 5,
                    "location": "beige office",
                    "characters": [{"name": "Brent", "description": "press sec"}],
                    "action": "Brent hands Kyle a clipboard titled POSTURE LOG",
                    "dialogue": "Log me every fifteen minutes.",
                    "camera": "wide",
                    "visual_note": "fluorescent lighting",
                },
                {
                    "n": 2,
                    "duration_sec": 6,
                    "location": "beige office",
                    "characters": [{"name": "Kyle", "description": "intern"}],
                    "action": "Kyle nervously marks the first box",
                    "dialogue": None,
                    "camera": "close-up",
                    "visual_note": "clipboard held at chest height",
                },
                {
                    "n": 3,
                    "duration_sec": 6,
                    "location": "beige office",
                    "characters": [
                        {"name": "Brent", "description": "press sec"},
                        {"name": "Kyle", "description": "intern"},
                    ],
                    "action": "Brent freezes mid-sentence and refuses to move",
                    "dialogue": "Log me.",
                    "camera": "two-shot",
                    "visual_note": "rigid stillness",
                },
            ]
        }
    )


def test_beats_parsed_from_valid_response() -> None:
    sketch = _make_sketch()
    adapter = FakeModelAdapter(raw_response=_valid_beat_json())
    beats = generate_beats(sketch, adapter)
    assert len(beats) == 3
    assert [b["n"] for b in beats] == [1, 2, 3]
    assert beats[0]["action"].startswith("Brent hands")
    assert beats[2]["dialogue"] == "Log me."
    for beat in beats:
        assert isinstance(beat["duration_sec"], int)
        assert beat["location"]
        assert beat["camera"]


def test_beats_parsed_from_fenced_response() -> None:
    sketch = _make_sketch()
    fenced = "```json\n" + _valid_beat_json() + "\n```"
    adapter = FakeModelAdapter(raw_response=fenced)
    beats = generate_beats(sketch, adapter)
    assert len(beats) == 3


def test_beats_fallback_on_malformed_json() -> None:
    sketch = _make_sketch()
    adapter = FakeModelAdapter(raw_response="sorry I can't do that")
    beats = generate_beats(sketch, adapter)
    assert len(beats) == 1
    assert "fallback" in beats[0]["action"].lower()


def test_beats_fallback_on_empty_response() -> None:
    sketch = _make_sketch()
    adapter = FakeModelAdapter(raw_response="")
    beats = generate_beats(sketch, adapter)
    assert len(beats) == 1


def test_beats_fallback_on_adapter_exception() -> None:
    sketch = _make_sketch()
    adapter = FakeModelAdapter(raises=True)
    beats = generate_beats(sketch, adapter)
    assert len(beats) >= 1
    for beat in beats:
        assert isinstance(beat, dict)
        assert "n" in beat


def test_beats_truncated_to_max() -> None:
    sketch = _make_sketch()
    huge = {
        "beats": [
            {
                "n": i,
                "duration_sec": 3,
                "location": "office",
                "characters": [],
                "action": f"action {i}",
                "dialogue": None,
                "camera": "wide",
                "visual_note": "",
            }
            for i in range(1, 16)
        ]
    }
    adapter = FakeModelAdapter(raw_response=json.dumps(huge))
    beats = generate_beats(sketch, adapter, n_beats_max=8)
    assert len(beats) == 8
    # Beats should be renumbered contiguously from 1.
    assert [b["n"] for b in beats] == list(range(1, 9))


def test_beats_coerce_missing_fields() -> None:
    sketch = _make_sketch()
    partial = {"beats": [{"action": "only action"}, {"action": "also action"}]}
    adapter = FakeModelAdapter(raw_response=json.dumps(partial))
    beats = generate_beats(sketch, adapter)
    assert len(beats) == 2
    for beat in beats:
        assert isinstance(beat["n"], int)
        assert isinstance(beat["duration_sec"], int)
        assert beat["location"]
        assert beat["camera"]


def test_beats_accept_bare_beats_array() -> None:
    sketch = _make_sketch()
    bare = {
        "output": [
            {"n": 1, "duration_sec": 4, "location": "x", "action": "a", "camera": "wide"},
            {"n": 2, "duration_sec": 4, "location": "y", "action": "b", "camera": "close"},
        ]
    }
    # The parser looks for `beats` specifically — verify that a nested envelope
    # without `beats` falls back gracefully rather than silently using garbage.
    adapter = FakeModelAdapter(raw_response=json.dumps(bare))
    beats = generate_beats(sketch, adapter)
    assert len(beats) == 1  # fallback

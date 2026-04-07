"""Phase 10: the idea factory prompt includes `## Human guidance` when set.

Black-box test of `idea_factory.factory._format_prompt` via a tiny prompt
template that exercises the `{user_guidance_section}` placeholder.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

import pytest

from idea_factory.adapter import ModelAdapter, Premise, PremiseResult
from idea_factory.factory import _build_user_guidance_section, run_factory
from state.leaderboard import Leaderboard
from state.store import Store


class RecordingAdapter(ModelAdapter):
    """Captures the prompt it receives so we can assert on its contents."""

    def __init__(self, model_id: str = "recording") -> None:
        super().__init__(config={})
        self.model_id = model_id
        self.last_prompt: str = ""

    def is_available(self) -> bool:
        return True

    def generate(
        self, signal: Dict[str, Any], prompt: str, n_premises: int = 3
    ) -> PremiseResult:
        self.last_prompt = prompt
        return PremiseResult(
            model_id=self.model_id,
            signal_id=str(signal.get("signal_id", "")),
            premises=[
                Premise(
                    logline="placeholder logline",
                    synopsis="placeholder synopsis",
                    tone="dry",
                    target_length_sec=30,
                    characters=[],
                    twist="",
                )
            ],
        )


# -------------------------------------------------------- unit helper tests


def test_build_user_guidance_section_present() -> None:
    section = _build_user_guidance_section(
        {"user_guidance": "lean into the workplace angle"}
    )
    assert section == "## Human guidance\n\nlean into the workplace angle\n"


def test_build_user_guidance_section_missing_returns_empty() -> None:
    assert _build_user_guidance_section({}) == ""
    assert _build_user_guidance_section({"user_guidance": ""}) == ""
    assert _build_user_guidance_section({"user_guidance": "   "}) == ""


# -------------------------------------------------------- full factory path


TEMPLATE = (
    "Prompt: {signal_title} / {signal_source} / {signal_url} / {signal_summary}"
    " / {n_premises} / {comedy_lens}\n"
    "{user_guidance_section}"
    "Task: write premises"
)


def _seed_signal(
    store: Store, signal_id: str = "sig-guide-001", **extra: Any
) -> None:
    payload: Dict[str, Any] = {
        "signal_id": signal_id,
        "source": "reddit",
        "source_url": "https://example.com/r/1",
        "title": "Senator caught using spoon as wifi antenna",
        "summary": "An aide rolled tape.",
    }
    payload.update(extra)
    store.write_queue_marker("idea-factory", signal_id, payload)


def test_prompt_contains_guidance_block_when_user_guidance_set(
    tmp_path: Path,
) -> None:
    store = Store(root=tmp_path)
    _seed_signal(store, user_guidance="mockumentary office energy, one location")
    adapter = RecordingAdapter()

    run_factory(
        store,
        prompt_template=TEMPLATE,
        lens_text="lens",
        leaderboard=Leaderboard(tmp_path / "leaderboard.json"),
        adapters=[adapter],
    )

    assert "## Human guidance" in adapter.last_prompt
    assert "mockumentary office energy, one location" in adapter.last_prompt


def test_prompt_guidance_section_empty_when_not_set(tmp_path: Path) -> None:
    store = Store(root=tmp_path)
    _seed_signal(store)
    adapter = RecordingAdapter()

    run_factory(
        store,
        prompt_template=TEMPLATE,
        lens_text="lens",
        leaderboard=Leaderboard(tmp_path / "leaderboard.json"),
        adapters=[adapter],
    )

    assert "## Human guidance" not in adapter.last_prompt


def test_factory_stamps_human_promote_event_when_guidance_present(
    tmp_path: Path,
) -> None:
    """When user_guidance is set, the sketch history gains an event."""
    store = Store(root=tmp_path)
    _seed_signal(store, user_guidance="the angle is absurd escalation")
    adapter = RecordingAdapter()

    sketch_ids = run_factory(
        store,
        prompt_template=TEMPLATE,
        lens_text="lens",
        leaderboard=Leaderboard(tmp_path / "leaderboard.json"),
        adapters=[adapter],
    )
    assert len(sketch_ids) == 1
    sketch = store.get_sketch(sketch_ids[0])
    events = [h.get("event") for h in sketch.history if isinstance(h, dict)]
    assert "human_promote_with_guidance" in events


def test_factory_omits_human_promote_event_without_guidance(tmp_path: Path) -> None:
    store = Store(root=tmp_path)
    _seed_signal(store)
    adapter = RecordingAdapter()

    sketch_ids = run_factory(
        store,
        prompt_template=TEMPLATE,
        lens_text="lens",
        leaderboard=Leaderboard(tmp_path / "leaderboard.json"),
        adapters=[adapter],
    )
    assert len(sketch_ids) == 1
    sketch = store.get_sketch(sketch_ids[0])
    events = [h.get("event") for h in sketch.history if isinstance(h, dict)]
    assert "human_promote_with_guidance" not in events


def test_bundled_premise_generation_md_has_user_guidance_section_placeholder() -> None:
    """The real prompt template on disk carries the new placeholder."""
    prompts = Path(__file__).resolve().parents[1] / "idea_factory" / "prompts"
    template = (prompts / "premise_generation.md").read_text(encoding="utf-8")
    assert "{user_guidance_section}" in template

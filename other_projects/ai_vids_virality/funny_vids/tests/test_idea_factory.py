"""Tests for the multi-model idea factory loop."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import pytest

from idea_factory.adapter import ModelAdapter, Premise, PremiseResult
from idea_factory.factory import run_factory
from state.leaderboard import Leaderboard
from state.machine import Status
from state.store import Store


def _seed_signal(store: Store, signal_id: str = "test-signal-001") -> None:
    """Drop one signal marker into the idea-factory queue."""
    store.write_queue_marker(
        "idea-factory",
        signal_id,
        {
            "signal_id": signal_id,
            "source": "reddit",
            "source_url": "https://example.com/r/1",
            "title": "Senator caught using spoon as wifi antenna in committee hearing",
            "summary": "An aide rolled tape and handed it back. The senator continued.",
            "sketchability_score": 9,
        },
    )


def _make_premise(model: str, idx: int) -> Premise:
    return Premise(
        logline=f"{model} logline #{idx}",
        synopsis=f"{model} synopsis #{idx}",
        tone=f"{model} tone",
        target_length_sec=30,
        characters=[{"name": "Riley", "description": "intern"}],
        twist=f"{model} twist",
    )


class FakeAdapter(ModelAdapter):
    """In-memory ModelAdapter for testing the factory loop."""

    def __init__(self, model_id: str, n: int = 3, fail: bool = False, raise_exc: bool = False) -> None:
        super().__init__(config={})
        self.model_id = model_id
        self.n = n
        self.fail = fail
        self.raise_exc = raise_exc
        self.calls = 0

    def is_available(self) -> bool:
        return True

    def generate(self, signal: Dict[str, Any], prompt: str, n_premises: int = 3) -> PremiseResult:
        self.calls += 1
        if self.raise_exc:
            raise RuntimeError("boom")
        if self.fail:
            return PremiseResult(
                model_id=self.model_id,
                signal_id=str(signal.get("signal_id", "")),
                error="simulated failure",
            )
        return PremiseResult(
            model_id=self.model_id,
            signal_id=str(signal.get("signal_id", "")),
            premises=[_make_premise(self.model_id, i) for i in range(min(n_premises, self.n))],
        )


def test_factory_runs_all_adapters_on_signal(tmp_path: Path) -> None:
    store = Store(root=tmp_path)
    _seed_signal(store)
    adapters = [
        FakeAdapter("claude-opus"),
        FakeAdapter("gpt-5"),
        FakeAdapter("gemini-2.5-pro"),
    ]
    leaderboard = Leaderboard(tmp_path / "leaderboard.json")

    sketch_ids = run_factory(
        store,
        prompt_template="prompt {signal_title}",
        lens_text="lens",
        leaderboard=leaderboard,
        adapters=adapters,
    )

    assert len(sketch_ids) == 1
    sketch_id = sketch_ids[0]
    sketch = store.get_sketch(sketch_id)
    assert sketch.status == Status.PREMISE_REVIEW
    for adapter in adapters:
        assert adapter.calls == 1

    queue_dir = store.queue_dir("premise-review")
    files = sorted(queue_dir.glob(f"{sketch_id}__*.json"))
    assert len(files) == 3
    for path in files:
        payload = json.loads(path.read_text(encoding="utf-8"))
        assert payload["sketch_id"] == sketch_id
        assert payload["model_id"] in {"claude-opus", "gpt-5", "gemini-2.5-pro"}
        assert payload["premise_count"] == 3

    rows = {r["model_id"]: r for r in leaderboard.get_leaderboard()["models"]}
    for model in ("claude-opus", "gpt-5", "gemini-2.5-pro"):
        assert rows[model]["total"] == 1


def test_one_adapter_failure_does_not_block_others(tmp_path: Path) -> None:
    store = Store(root=tmp_path)
    _seed_signal(store)
    adapters = [
        FakeAdapter("claude-opus", fail=True),
        FakeAdapter("gpt-5"),
        FakeAdapter("gemini-2.5-pro", raise_exc=True),
    ]
    leaderboard = Leaderboard(tmp_path / "leaderboard.json")

    sketch_ids = run_factory(
        store,
        prompt_template="prompt {signal_title}",
        lens_text="lens",
        leaderboard=leaderboard,
        adapters=adapters,
    )

    assert len(sketch_ids) == 1
    queue_dir = store.queue_dir("premise-review")
    files = sorted(queue_dir.glob(f"{sketch_ids[0]}__*.json"))
    # All three variant files exist (failed ones are persisted with error set).
    assert len(files) == 3
    payloads = {json.loads(p.read_text(encoding="utf-8"))["model_id"]: json.loads(p.read_text(encoding="utf-8")) for p in files}
    assert payloads["claude-opus"]["error"] == "simulated failure"
    assert payloads["claude-opus"]["premises"] == []
    assert payloads["gpt-5"]["error"] is None
    assert payloads["gpt-5"]["premise_count"] == 3
    assert "boom" in (payloads["gemini-2.5-pro"]["error"] or "")

    # Only the successful model should have a leaderboard total.
    rows = {r["model_id"]: r for r in leaderboard.get_leaderboard()["models"]}
    assert rows["gpt-5"]["total"] == 1
    assert rows.get("claude-opus", {}).get("total", 0) == 0
    assert rows.get("gemini-2.5-pro", {}).get("total", 0) == 0


def test_all_adapters_failing_creates_no_sketch(tmp_path: Path) -> None:
    store = Store(root=tmp_path)
    _seed_signal(store)
    adapters = [
        FakeAdapter("claude-opus", fail=True),
        FakeAdapter("gpt-5", fail=True),
    ]

    sketch_ids = run_factory(
        store,
        prompt_template="prompt",
        lens_text="lens",
        leaderboard=Leaderboard(tmp_path / "leaderboard.json"),
        adapters=adapters,
    )
    assert sketch_ids == []
    assert store.list_sketches() == []


def test_factory_is_idempotent(tmp_path: Path) -> None:
    store = Store(root=tmp_path)
    _seed_signal(store)
    adapters = [FakeAdapter("claude-opus")]

    first = run_factory(
        store,
        prompt_template="prompt",
        lens_text="lens",
        leaderboard=Leaderboard(tmp_path / "leaderboard.json"),
        adapters=adapters,
    )
    second = run_factory(
        store,
        prompt_template="prompt",
        lens_text="lens",
        leaderboard=Leaderboard(tmp_path / "leaderboard.json"),
        adapters=adapters,
    )
    assert len(first) == 1
    assert second == []


def test_no_adapters_is_noop(tmp_path: Path) -> None:
    store = Store(root=tmp_path)
    _seed_signal(store)
    sketch_ids = run_factory(
        store,
        prompt_template="prompt",
        lens_text="lens",
        leaderboard=Leaderboard(tmp_path / "leaderboard.json"),
        adapters=[],
    )
    assert sketch_ids == []


def test_factory_factory_canonical_premise_is_first_successful(tmp_path: Path) -> None:
    store = Store(root=tmp_path)
    _seed_signal(store)
    adapters = [
        FakeAdapter("claude-opus", fail=True),
        FakeAdapter("gpt-5"),
    ]
    sketch_ids = run_factory(
        store,
        prompt_template="prompt",
        lens_text="lens",
        leaderboard=Leaderboard(tmp_path / "leaderboard.json"),
        adapters=adapters,
    )
    assert len(sketch_ids) == 1
    sketch = store.get_sketch(sketch_ids[0])
    assert sketch.premise is not None
    assert sketch.premise["logline"].startswith("gpt-5")

"""Tests for the sketch state machine and file-based store."""
from __future__ import annotations

from pathlib import Path

import pytest

from state.machine import (
    InvalidTransition,
    Status,
    VALID_TRANSITIONS,
    assert_transition,
    can_transition,
)
from state.store import Sketch, Store


HAPPY_PATH = [
    (Status.SIGNAL, Status.IDEA_PENDING),
    (Status.IDEA_PENDING, Status.PREMISE_REVIEW),
    (Status.PREMISE_REVIEW, Status.SCRIPTED),
    (Status.SCRIPTED, Status.STORYBOARD_REVIEW),
    (Status.STORYBOARD_REVIEW, Status.VIDEO_PENDING),
    (Status.VIDEO_PENDING, Status.CRITIC_REVIEW),
    (Status.CRITIC_REVIEW, Status.PUBLISHED),
]


@pytest.mark.parametrize("current,target", HAPPY_PATH)
def test_happy_path_transitions_are_valid(current: Status, target: Status) -> None:
    assert can_transition(current, target)
    assert_transition(current, target)


@pytest.mark.parametrize(
    "current",
    [
        Status.SIGNAL,
        Status.IDEA_PENDING,
        Status.PREMISE_REVIEW,
        Status.SCRIPTED,
        Status.STORYBOARD_REVIEW,
        Status.VIDEO_PENDING,
        Status.CRITIC_REVIEW,
    ],
)
def test_reject_is_always_allowed_from_non_terminal(current: Status) -> None:
    assert can_transition(current, Status.REJECTED)


def test_published_is_terminal() -> None:
    assert VALID_TRANSITIONS[Status.PUBLISHED] == set()
    for target in Status:
        assert not can_transition(Status.PUBLISHED, target)


def test_rejected_is_terminal() -> None:
    assert VALID_TRANSITIONS[Status.REJECTED] == set()
    for target in Status:
        assert not can_transition(Status.REJECTED, target)


def test_invalid_transitions_raise() -> None:
    with pytest.raises(InvalidTransition):
        assert_transition(Status.SIGNAL, Status.PUBLISHED)
    with pytest.raises(InvalidTransition):
        assert_transition(Status.PREMISE_REVIEW, Status.PUBLISHED)
    with pytest.raises(InvalidTransition):
        assert_transition(Status.PREMISE_REVIEW, Status.IDEA_PENDING)


def test_invalid_transition_carries_states() -> None:
    try:
        assert_transition(Status.SIGNAL, Status.PUBLISHED)
    except InvalidTransition as exc:
        assert exc.current == Status.SIGNAL
        assert exc.attempted == Status.PUBLISHED
    else:
        pytest.fail("expected InvalidTransition")


# ----------------------------------------------------------------- store

def test_store_creates_layout(tmp_path: Path) -> None:
    store = Store(root=tmp_path)
    assert (tmp_path / "sketches").is_dir()
    assert (tmp_path / "signals" / "reddit_stub" / "items").is_dir()
    assert (tmp_path / "signals" / "reddit_stub" / ".seen-ids").exists()
    assert (tmp_path / "queues" / "premise-review").is_dir()


def test_store_save_and_get_sketch(tmp_path: Path) -> None:
    store = Store(root=tmp_path)
    sketch = Sketch(id="sk-test-001", status=Status.PREMISE_REVIEW, signal_id="sig-1")
    store.save_sketch(sketch)
    loaded = store.get_sketch("sk-test-001")
    assert loaded.id == "sk-test-001"
    assert loaded.status == Status.PREMISE_REVIEW
    assert loaded.signal_id == "sig-1"


def test_store_transition_appends_history(tmp_path: Path) -> None:
    store = Store(root=tmp_path)
    sketch = Sketch(id="sk-test-002", status=Status.PREMISE_REVIEW)
    store.save_sketch(sketch)
    updated = store.transition("sk-test-002", Status.SCRIPTED, {"note": "approved"})
    assert updated.status == Status.SCRIPTED
    assert len(updated.history) == 1
    assert updated.history[0]["from"] == "premise_review"
    assert updated.history[0]["to"] == "scripted"
    assert updated.history[0]["payload"] == {"note": "approved"}


def test_store_transition_rejects_invalid(tmp_path: Path) -> None:
    store = Store(root=tmp_path)
    sketch = Sketch(id="sk-test-003", status=Status.PREMISE_REVIEW)
    store.save_sketch(sketch)
    with pytest.raises(InvalidTransition):
        store.transition("sk-test-003", Status.PUBLISHED, {})


def test_store_list_sketches(tmp_path: Path) -> None:
    store = Store(root=tmp_path)
    store.save_sketch(Sketch(id="sk-a", status=Status.PREMISE_REVIEW))
    store.save_sketch(Sketch(id="sk-b", status=Status.PUBLISHED))
    ids = sorted(s.id for s in store.list_sketches())
    assert ids == ["sk-a", "sk-b"]

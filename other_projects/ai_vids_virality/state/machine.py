"""Sketch lifecycle state machine.

This is the contract that every later phase depends on. The status enum,
the transition table, and the InvalidTransition error are intentionally
explicit so that real implementations can plug in without ambiguity.
"""
from __future__ import annotations

from enum import Enum
from typing import Dict, Set


class Status(str, Enum):
    SIGNAL = "signal"
    IDEA_PENDING = "idea_pending"
    PREMISE_REVIEW = "premise_review"
    SCRIPTED = "scripted"
    STORYBOARD_REVIEW = "storyboard_review"
    VIDEO_PENDING = "video_pending"
    CRITIC_REVIEW = "critic_review"
    PUBLISHED = "published"
    REJECTED = "rejected"


# Forward transitions only. REJECTED is allowed from any non-terminal state
# and is added programmatically below so the table stays readable.
VALID_TRANSITIONS: Dict[Status, Set[Status]] = {
    Status.SIGNAL: {Status.IDEA_PENDING, Status.REJECTED},
    Status.IDEA_PENDING: {Status.PREMISE_REVIEW, Status.REJECTED},
    Status.PREMISE_REVIEW: {Status.SCRIPTED, Status.REJECTED},
    Status.SCRIPTED: {Status.STORYBOARD_REVIEW, Status.REJECTED},
    Status.STORYBOARD_REVIEW: {Status.VIDEO_PENDING, Status.REJECTED},
    Status.VIDEO_PENDING: {Status.CRITIC_REVIEW, Status.REJECTED},
    Status.CRITIC_REVIEW: {Status.PUBLISHED, Status.REJECTED},
    Status.PUBLISHED: set(),
    Status.REJECTED: set(),
}


class InvalidTransition(ValueError):
    """Raised when a sketch is asked to move along an unsupported edge."""

    def __init__(self, current: Status, attempted: Status) -> None:
        super().__init__(
            f"Invalid transition from {current.value} to {attempted.value}"
        )
        self.current = current
        self.attempted = attempted


def can_transition(current: Status, target: Status) -> bool:
    """True if `current` -> `target` is a legal edge."""
    return target in VALID_TRANSITIONS.get(current, set())


def assert_transition(current: Status, target: Status) -> None:
    """Raise InvalidTransition unless the move is legal."""
    if not can_transition(current, target):
        raise InvalidTransition(current, target)

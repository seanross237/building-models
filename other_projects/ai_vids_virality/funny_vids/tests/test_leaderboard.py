"""Tests for the file-backed leaderboard."""
from __future__ import annotations

from pathlib import Path

import pytest

from state.leaderboard import Leaderboard


@pytest.fixture()
def board(tmp_path: Path) -> Leaderboard:
    return Leaderboard(tmp_path / "leaderboard.json")


def test_empty_leaderboard(board: Leaderboard) -> None:
    payload = board.get_leaderboard()
    assert payload == {"models": []}


def test_record_generation_increments_total(board: Leaderboard) -> None:
    board.record_generation("claude-opus")
    board.record_generation("claude-opus")
    board.record_generation("gpt-5")

    payload = board.get_leaderboard()
    rows = {row["model_id"]: row for row in payload["models"]}
    assert rows["claude-opus"]["total"] == 2
    assert rows["gpt-5"]["total"] == 1
    assert rows["claude-opus"]["approved"] == 0
    assert rows["claude-opus"]["rejected"] == 0


def test_record_decision_approved(board: Leaderboard) -> None:
    board.record_generation("claude-opus")
    board.record_decision("claude-opus", approved=True)

    rows = {row["model_id"]: row for row in board.get_leaderboard()["models"]}
    assert rows["claude-opus"]["approved"] == 1
    assert rows["claude-opus"]["rejected"] == 0
    assert rows["claude-opus"]["approval_rate"] == 1.0


def test_record_decision_rejected(board: Leaderboard) -> None:
    board.record_generation("gemini-2.5-pro")
    board.record_decision("gemini-2.5-pro", approved=False)

    rows = {row["model_id"]: row for row in board.get_leaderboard()["models"]}
    assert rows["gemini-2.5-pro"]["rejected"] == 1
    assert rows["gemini-2.5-pro"]["approval_rate"] == 0.0


def test_approval_rate_math(board: Leaderboard) -> None:
    for _ in range(4):
        board.record_generation("claude-opus")
    board.record_decision("claude-opus", approved=True)
    board.record_decision("claude-opus", approved=True)
    board.record_decision("claude-opus", approved=True)
    board.record_decision("claude-opus", approved=False)

    rows = {row["model_id"]: row for row in board.get_leaderboard()["models"]}
    assert rows["claude-opus"]["approved"] == 3
    assert rows["claude-opus"]["rejected"] == 1
    assert rows["claude-opus"]["approval_rate"] == 0.75


def test_persists_across_instances(tmp_path: Path) -> None:
    path = tmp_path / "leaderboard.json"
    Leaderboard(path).record_generation("claude-opus")
    Leaderboard(path).record_decision("claude-opus", approved=True)

    rows = {row["model_id"]: row for row in Leaderboard(path).get_leaderboard()["models"]}
    assert rows["claude-opus"]["total"] == 1
    assert rows["claude-opus"]["approved"] == 1

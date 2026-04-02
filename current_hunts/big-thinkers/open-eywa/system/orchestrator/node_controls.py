from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .node_lifecycle import transition_node
from .node_record import node_status, node_computation_result_note, update_node_record


@dataclass(frozen=True)
class ResumeComputationResult:
    resumed: bool
    previous_status: str
    current_status: str


def record_computation_result(
    node_path: str | Path,
    *,
    result_text: str,
) -> None:
    def updater(record: dict[str, object]) -> None:
        lifecycle = record["lifecycle"]
        assert isinstance(lifecycle, dict)
        lifecycle["computation_result_note"] = result_text.rstrip()

    update_node_record(node_path, updater)


def resume_waiting_node_if_ready(node_path: str | Path) -> ResumeComputationResult:
    previous_status = node_status(node_path) or ""
    if previous_status != "waiting_on_computation":
        return ResumeComputationResult(
            resumed=False,
            previous_status=previous_status,
            current_status=previous_status,
        )
    if not node_computation_result_note(node_path):
        return ResumeComputationResult(
            resumed=False,
            previous_status=previous_status,
            current_status=previous_status,
        )

    transition_node(
        node_path,
        next_status="active",
        expected_current_status="waiting_on_computation",
    )
    return ResumeComputationResult(
        resumed=True,
        previous_status="waiting_on_computation",
        current_status="active",
    )


def cancel_node(
    node_path: str | Path,
    *,
    cancellation_reason: str,
) -> None:
    current_status = node_status(node_path) or ""
    if current_status == "finished":
        raise RuntimeError("Cannot cancel a node that is already finished.")
    if current_status == "failed":
        raise RuntimeError("Cannot cancel a node that has already failed.")

    if current_status == "pending":
        transition_node(node_path, next_status="active", expected_current_status="pending")

    transition_node(
        node_path,
        next_status="finished",
        expected_current_status="active",
        terminal_outcome="cancelled",
        cancellation_reason=cancellation_reason,
    )

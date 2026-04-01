from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .node_contract import node_layout, unlink_if_exists, write_text
from .node_lifecycle import transition_node


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
    layout = node_layout(node_path)
    write_text(layout.computation_result_file, result_text.rstrip() + "\n")


def resume_waiting_node_if_ready(node_path: str | Path) -> ResumeComputationResult:
    layout = node_layout(node_path)
    previous_status = (layout.status_file.read_text(encoding="utf-8").strip()
                       if layout.status_file.exists() else "")
    if previous_status != "waiting_on_computation":
        return ResumeComputationResult(
            resumed=False,
            previous_status=previous_status,
            current_status=previous_status,
        )
    if not layout.computation_result_file.exists():
        return ResumeComputationResult(
            resumed=False,
            previous_status=previous_status,
            current_status=previous_status,
        )

    transition_node(
        layout.root,
        next_status="active",
        expected_current_status="waiting_on_computation",
    )
    unlink_if_exists(layout.computation_result_file)
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
    layout = node_layout(node_path)
    current_status = layout.status_file.read_text(encoding="utf-8").strip()
    if current_status == "finished":
        raise RuntimeError("Cannot cancel a node that is already finished.")
    if current_status == "failed":
        raise RuntimeError("Cannot cancel a node that has already failed.")

    if current_status == "pending":
        transition_node(layout.root, next_status="active", expected_current_status="pending")

    transition_node(
        layout.root,
        next_status="finished",
        expected_current_status="active",
        terminal_outcome="cancelled",
        cancellation_reason=cancellation_reason,
    )

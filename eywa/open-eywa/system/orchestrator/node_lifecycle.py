from __future__ import annotations

from pathlib import Path

from .node_contract import NODE_STATUSES, TERMINAL_OUTCOMES, NodeStatus, TerminalOutcome, node_layout
from .node_record import read_node_record, write_node_record

LEGAL_STATUS_TRANSITIONS: dict[NodeStatus, tuple[NodeStatus, ...]] = {
    "pending": ("active", "finished", "failed"),
    "active": ("waiting_on_computation", "finished", "failed"),
    "waiting_on_computation": ("active", "finished", "failed"),
    "finished": (),
    "failed": (),
}


class NodeTransitionError(RuntimeError):
    """Raised when a node transition violates the contract."""


def can_transition(current_status: NodeStatus, next_status: NodeStatus) -> bool:
    return next_status in LEGAL_STATUS_TRANSITIONS[current_status]


def transition_node(
    node_path: str | Path,
    *,
    next_status: NodeStatus,
    expected_current_status: NodeStatus | None = None,
    terminal_outcome: TerminalOutcome | None = None,
    failure_reason: str | None = None,
    cancellation_reason: str | None = None,
    waiting_note: str | None = None,
) -> None:
    layout = node_layout(node_path)
    record = read_node_record(layout)
    lifecycle = record["lifecycle"]
    current_status = lifecycle.get("status")
    if current_status is None:
        raise NodeTransitionError("Cannot transition a node without a node record status.")
    if current_status not in NODE_STATUSES:
        raise NodeTransitionError(f"Current node status is invalid: {current_status!r}.")
    if next_status not in NODE_STATUSES:
        raise NodeTransitionError(f"Next node status is invalid: {next_status!r}.")
    if expected_current_status is not None and current_status != expected_current_status:
        raise NodeTransitionError(
            f"Expected current status {expected_current_status!r}, found {current_status!r}."
        )
    if not can_transition(current_status, next_status):
        raise NodeTransitionError(
            f"Illegal node transition: {current_status!r} -> {next_status!r}."
        )

    if next_status == "finished":
        _validate_finished_transition(layout, terminal_outcome, cancellation_reason)
        lifecycle["terminal_outcome"] = terminal_outcome
        lifecycle["failure_reason"] = None
        lifecycle["waiting_on_computation_note"] = None
        lifecycle["computation_result_note"] = None
        lifecycle["cancellation_reason"] = (
            cancellation_reason.strip() if terminal_outcome == "cancelled" else None
        )
    elif next_status == "failed":
        _validate_failed_transition(failure_reason)
        lifecycle["terminal_outcome"] = None
        lifecycle["failure_reason"] = failure_reason.strip()
        lifecycle["cancellation_reason"] = None
        lifecycle["waiting_on_computation_note"] = None
        lifecycle["computation_result_note"] = None
    elif next_status == "waiting_on_computation":
        lifecycle["terminal_outcome"] = None
        lifecycle["failure_reason"] = None
        lifecycle["cancellation_reason"] = None
        lifecycle["waiting_on_computation_note"] = (
            waiting_note or "waiting for background computation"
        ).strip()
        lifecycle["computation_result_note"] = None
    else:
        lifecycle["terminal_outcome"] = None
        lifecycle["failure_reason"] = None
        lifecycle["cancellation_reason"] = None
        lifecycle["waiting_on_computation_note"] = None
        lifecycle["computation_result_note"] = None

    lifecycle["status"] = next_status
    write_node_record(layout, record)


def _validate_finished_transition(
    layout,
    terminal_outcome: TerminalOutcome | None,
    cancellation_reason: str | None,
) -> None:
    if terminal_outcome not in TERMINAL_OUTCOMES:
        raise NodeTransitionError("finished transitions require a valid terminal outcome.")
    if terminal_outcome == "completed" and not layout.final_output_file.exists():
        raise NodeTransitionError(
            "completed transitions require output/final-output.md to exist."
        )
    if terminal_outcome == "escalated" and not layout.escalation_file.exists():
        raise NodeTransitionError(
            "escalated transitions require output/escalation.md to exist."
        )
    if terminal_outcome == "cancelled" and not (cancellation_reason or "").strip():
        raise NodeTransitionError(
            "cancelled transitions require a non-empty cancellation reason."
        )


def _validate_failed_transition(failure_reason: str | None) -> None:
    if not (failure_reason or "").strip():
        raise NodeTransitionError("failed transitions require a non-empty failure reason.")

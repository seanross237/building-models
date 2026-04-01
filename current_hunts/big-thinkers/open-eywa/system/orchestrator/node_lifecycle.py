from __future__ import annotations

from pathlib import Path

from .node_contract import NODE_STATUSES, TERMINAL_OUTCOMES, NodeStatus, TerminalOutcome, node_layout, read_trimmed_text, unlink_if_exists, write_text

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
    current_status = read_trimmed_text(layout.status_file)
    if current_status is None:
        raise NodeTransitionError("Cannot transition a node without a status file.")
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
        write_text(layout.terminal_outcome_file, terminal_outcome + "\n")
        unlink_if_exists(layout.failure_reason_file)
        unlink_if_exists(layout.waiting_marker_file)
        unlink_if_exists(layout.computation_result_file)
        if terminal_outcome == "cancelled":
            write_text(layout.cancellation_reason_file, cancellation_reason.strip() + "\n")
        else:
            unlink_if_exists(layout.cancellation_reason_file)
    elif next_status == "failed":
        _validate_failed_transition(failure_reason)
        write_text(layout.failure_reason_file, failure_reason.strip() + "\n")
        unlink_if_exists(layout.terminal_outcome_file)
        unlink_if_exists(layout.cancellation_reason_file)
        unlink_if_exists(layout.waiting_marker_file)
        unlink_if_exists(layout.computation_result_file)
    elif next_status == "waiting_on_computation":
        note = (waiting_note or "waiting for background computation").strip()
        write_text(layout.waiting_marker_file, note + "\n")
        unlink_if_exists(layout.terminal_outcome_file)
        unlink_if_exists(layout.failure_reason_file)
        unlink_if_exists(layout.cancellation_reason_file)
        unlink_if_exists(layout.computation_result_file)
    else:
        unlink_if_exists(layout.terminal_outcome_file)
        unlink_if_exists(layout.failure_reason_file)
        unlink_if_exists(layout.cancellation_reason_file)
        unlink_if_exists(layout.waiting_marker_file)
        unlink_if_exists(layout.computation_result_file)

    write_text(layout.status_file, next_status + "\n")


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

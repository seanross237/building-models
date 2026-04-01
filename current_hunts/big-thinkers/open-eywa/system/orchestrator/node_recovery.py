from __future__ import annotations

from dataclasses import dataclass
import json
import shutil
from pathlib import Path

from .event_schema import EventRecord
from .event_writer import AppendOnlyJsonlWriter
from .node_contract import node_layout, read_trimmed_text, unlink_if_exists, write_text


@dataclass(frozen=True)
class NodeRecoveryResult:
    recovery_id: str
    previous_status: str
    current_status: str
    next_role: str | None


class NodeRecoveryError(RuntimeError):
    """Raised when a node cannot be safely prepared for a fresh attempt."""


def prepare_node_for_fresh_attempt(
    node_path: str | Path,
    *,
    recovery_reason: str,
    next_role: str | None = None,
    mission_id: str | None = None,
    node_id: str | None = None,
) -> NodeRecoveryResult:
    layout = node_layout(node_path)
    previous_status = read_trimmed_text(layout.status_file)
    if previous_status is None:
        raise NodeRecoveryError("Cannot recover a node without a status file.")
    if previous_status == "pending":
        raise NodeRecoveryError("Pending nodes do not need recovery.")

    terminal_outcome = read_trimmed_text(layout.terminal_outcome_file)
    if previous_status == "finished" and terminal_outcome == "completed":
        raise NodeRecoveryError("Completed nodes cannot be retried with fresh-attempt recovery.")

    previous_role = read_trimmed_text(layout.agent_mode_file)
    recovery_id = _next_recovery_id(layout)
    recovery_dir = layout.recoveries_dir / recovery_id
    recovery_dir.mkdir(parents=True, exist_ok=False)

    _archive_directory(layout.output_dir, recovery_dir / "output")
    _archive_directory(layout.children_dir, recovery_dir / "children")

    archived_orchestrator_dir = recovery_dir / "for-orchestrator"
    archived_orchestrator_dir.mkdir(parents=True, exist_ok=True)
    for path in (
        layout.agent_mode_file,
        layout.status_file,
        layout.next_action_after_child_report_file,
        layout.terminal_outcome_file,
        layout.failure_reason_file,
        layout.cancellation_reason_file,
        layout.waiting_marker_file,
        layout.computation_result_file,
    ):
        _archive_file_if_exists(path, archived_orchestrator_dir / path.name)

    _archive_file_if_exists(
        layout.progression_state_file,
        recovery_dir / layout.progression_state_file.name,
    )
    _archive_file_if_exists(
        layout.latest_child_node_report_file,
        recovery_dir / layout.latest_child_node_report_file.name,
    )

    recovery_record = {
        "recovery_id": recovery_id,
        "recovery_reason": recovery_reason,
        "previous_status": previous_status,
        "previous_terminal_outcome": terminal_outcome,
        "previous_failure_reason": read_trimmed_text(layout.failure_reason_file),
        "previous_cancellation_reason": read_trimmed_text(layout.cancellation_reason_file),
        "previous_role": previous_role,
        "next_role": next_role or previous_role,
    }
    write_text(
        recovery_dir / "recovery-record.json",
        json.dumps(recovery_record, indent=2, sort_keys=True) + "\n",
    )

    layout.output_dir.mkdir(parents=True, exist_ok=True)
    layout.children_dir.mkdir(parents=True, exist_ok=True)
    unlink_if_exists(layout.next_action_after_child_report_file)
    unlink_if_exists(layout.terminal_outcome_file)
    unlink_if_exists(layout.failure_reason_file)
    unlink_if_exists(layout.cancellation_reason_file)
    unlink_if_exists(layout.waiting_marker_file)
    unlink_if_exists(layout.computation_result_file)
    unlink_if_exists(layout.progression_state_file)
    unlink_if_exists(layout.latest_child_node_report_file)

    write_text(layout.status_file, "pending\n")
    if next_role or previous_role:
        write_text(layout.agent_mode_file, (next_role or previous_role or "").strip() + "\n")
    else:
        unlink_if_exists(layout.agent_mode_file)

    AppendOnlyJsonlWriter(layout.events_log_file).append_event(
        EventRecord(
            event_type="node_recovery_prepared",
            mission_id=mission_id or "unknown",
            node_id=node_id or layout.root.name,
            node_path=str(layout.root),
            role=next_role or previous_role,
            payload={
                "recovery_reason": recovery_reason,
                "recovery_attempt": recovery_id,
                "previous_status": previous_status,
                "previous_terminal_outcome": terminal_outcome,
            },
        )
    )

    return NodeRecoveryResult(
        recovery_id=recovery_id,
        previous_status=previous_status,
        current_status="pending",
        next_role=next_role or previous_role,
    )


def _next_recovery_id(layout) -> str:
    existing_numbers: list[int] = []
    if layout.recoveries_dir.exists():
        for child in layout.recoveries_dir.iterdir():
            if child.is_dir() and child.name.startswith("recovery-"):
                suffix = child.name.removeprefix("recovery-")
                if suffix.isdigit():
                    existing_numbers.append(int(suffix))
    next_number = (max(existing_numbers) + 1) if existing_numbers else 1
    return f"recovery-{next_number:03d}"


def _archive_directory(source: Path, destination: Path) -> None:
    if not source.exists():
        return
    shutil.move(str(source), str(destination))


def _archive_file_if_exists(source: Path, destination: Path) -> None:
    if not source.exists():
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(source), str(destination))

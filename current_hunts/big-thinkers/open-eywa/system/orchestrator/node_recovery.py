from __future__ import annotations

from dataclasses import dataclass
import json
import shutil
from pathlib import Path

from .event_schema import EventRecord
from .event_writer import AppendOnlyJsonlWriter
from .node_contract import node_layout, write_text
from .node_record import node_next_role, read_node_record, write_node_record


@dataclass(frozen=True)
class NodeRecoveryResult:
    recovery_id: str
    previous_status: str
    current_status: str
    next_role: str | None
    retry_count: int


class NodeRecoveryError(RuntimeError):
    """Raised when a node cannot be safely prepared for recovery."""


def prepare_node_for_retry(
    node_path: str | Path,
    *,
    recovery_reason: str,
    next_role: str | None = None,
    mission_id: str | None = None,
    node_id: str | None = None,
) -> NodeRecoveryResult:
    return _prepare_node_recovery(
        node_path,
        recovery_reason=recovery_reason,
        next_role=next_role,
        mission_id=mission_id,
        node_id=node_id,
        recovery_mode="retry",
    )


def prepare_node_for_fresh_attempt(
    node_path: str | Path,
    *,
    recovery_reason: str,
    next_role: str | None = None,
    mission_id: str | None = None,
    node_id: str | None = None,
) -> NodeRecoveryResult:
    return _prepare_node_recovery(
        node_path,
        recovery_reason=recovery_reason,
        next_role=next_role,
        mission_id=mission_id,
        node_id=node_id,
        recovery_mode="fresh_attempt",
    )


def _prepare_node_recovery(
    node_path: str | Path,
    *,
    recovery_reason: str,
    next_role: str | None,
    mission_id: str | None,
    node_id: str | None,
    recovery_mode: str,
) -> NodeRecoveryResult:
    layout = node_layout(node_path)
    record = read_node_record(layout)
    lifecycle = dict(record.get("lifecycle") or {})
    previous_status = lifecycle.get("status")
    if previous_status is None:
        raise NodeRecoveryError("Cannot recover a node without a node record status.")
    if previous_status == "pending":
        raise NodeRecoveryError("Pending nodes do not need recovery.")

    terminal_outcome = lifecycle.get("terminal_outcome")
    if previous_status == "finished" and terminal_outcome == "completed":
        raise NodeRecoveryError("Completed nodes cannot be retried through node recovery.")
    if recovery_mode == "retry" and previous_status != "failed":
        raise NodeRecoveryError("Narrow retry recovery only applies to failed nodes.")

    previous_role = node_next_role(layout)
    retry_count = _read_retry_count(lifecycle) + 1
    recovery_id = _next_recovery_id(layout)
    recovery_dir = layout.recoveries_dir / recovery_id
    recovery_dir.mkdir(parents=True, exist_ok=False)

    if recovery_mode == "fresh_attempt":
        _archive_directory(layout.output_dir, recovery_dir / "output")
        _archive_directory(layout.children_dir, recovery_dir / "children")
        _archive_file_if_exists(layout.node_record_file, recovery_dir / "node.json")
    else:
        _snapshot_directory_if_exists(layout.output_dir, recovery_dir / "output")
        _snapshot_file_if_exists(layout.node_record_file, recovery_dir / "node.json")

    recovery_record = {
        "recovery_id": recovery_id,
        "recovery_mode": recovery_mode,
        "recovery_reason": recovery_reason,
        "previous_status": previous_status,
        "previous_terminal_outcome": terminal_outcome,
        "previous_failure_reason": lifecycle.get("failure_reason"),
        "previous_cancellation_reason": lifecycle.get("cancellation_reason"),
        "previous_role": previous_role,
        "next_role": next_role or previous_role,
        "retry_count": retry_count,
    }
    write_text(
        recovery_dir / "recovery-record.json",
        json.dumps(recovery_record, indent=2, sort_keys=True) + "\n",
    )

    if recovery_mode == "fresh_attempt":
        layout.output_dir.mkdir(parents=True, exist_ok=True)
        layout.children_dir.mkdir(parents=True, exist_ok=True)

    control = dict(record.get("control") or {})
    progression = dict(record.get("progression") or {})
    control["next_role"] = next_role or previous_role
    control["next_action_after_child_report"] = None
    if recovery_mode == "fresh_attempt":
        progression["current_step_index"] = None
        progression["steps"] = []
        progression["latest_child_report"] = None

    lifecycle["status"] = "pending"
    lifecycle["terminal_outcome"] = None
    lifecycle["failure_reason"] = None
    lifecycle["cancellation_reason"] = None
    lifecycle["waiting_on_computation_note"] = None
    lifecycle["computation_result_note"] = None
    lifecycle["retry_count"] = retry_count
    record["lifecycle"] = lifecycle
    record["control"] = control
    record["progression"] = progression
    write_node_record(layout, record)

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
                "recovery_mode": recovery_mode,
                "previous_status": previous_status,
                "previous_terminal_outcome": terminal_outcome,
                "retry_count": retry_count,
            },
        )
    )

    return NodeRecoveryResult(
        recovery_id=recovery_id,
        previous_status=previous_status,
        current_status="pending",
        next_role=next_role or previous_role,
        retry_count=retry_count,
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


def _snapshot_directory_if_exists(source: Path, destination: Path) -> None:
    if not source.exists():
        return
    shutil.copytree(source, destination)


def _snapshot_file_if_exists(source: Path, destination: Path) -> None:
    if not source.exists():
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def _read_retry_count(lifecycle: dict[str, object]) -> int:
    retry_count = lifecycle.get("retry_count")
    if isinstance(retry_count, int) and retry_count >= 0:
        return retry_count
    return 0

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .node_contract import (
    NODE_STATUSES,
    TERMINAL_OUTCOMES,
    NODE_SUBDIRECTORIES,
    NodeLayout,
    node_layout,
)
from .node_record import ASSIGNMENT_SOURCES, NODE_RECORD_SCHEMA_VERSION, read_node_record


@dataclass(frozen=True)
class NodeValidationIssue:
    code: str
    message: str
    path: str | None = None


@dataclass
class NodeValidationReport:
    node_root: Path
    issues: list[NodeValidationIssue] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return not self.issues

    def add_issue(self, code: str, message: str, path: Path | None = None) -> None:
        self.issues.append(
            NodeValidationIssue(code=code, message=message, path=str(path) if path else None)
        )


def validate_node(node_path: str | Path) -> NodeValidationReport:
    layout = node_layout(node_path)
    report = NodeValidationReport(node_root=layout.root)

    if not layout.root.exists():
        report.add_issue("node_root_missing", "Node root does not exist.", layout.root)
        return report
    if not layout.root.is_dir():
        report.add_issue("node_root_not_directory", "Node root is not a directory.", layout.root)
        return report

    _validate_required_directories(layout, report)
    _validate_task_source(layout, report)
    record = _validate_node_record(layout, report)
    if record is not None:
        _validate_lifecycle(layout, record, report)
        _validate_parameters(layout, record, report)

    return report


def _validate_required_directories(layout: NodeLayout, report: NodeValidationReport) -> None:
    for subdirectory in NODE_SUBDIRECTORIES:
        directory = layout.root / subdirectory
        if not directory.exists():
            report.add_issue("required_directory_missing", "Required directory is missing.", directory)
        elif not directory.is_dir():
            report.add_issue(
                "required_directory_not_directory",
                "Required node entry is not a directory.",
                directory,
            )


def _validate_task_source(layout: NodeLayout, report: NodeValidationReport) -> None:
    task_sources = [
        path for path in (layout.goal_file, layout.parent_instructions_file) if path.exists()
    ]
    if len(task_sources) != 1:
        report.add_issue(
            "task_source_count",
            "A node must have exactly one task source file.",
            layout.input_dir,
        )


def _validate_node_record(
    layout: NodeLayout,
    report: NodeValidationReport,
) -> dict[str, object] | None:
    if not layout.node_record_file.exists():
        report.add_issue(
            "node_record_missing",
            "The node is missing its authoritative system/node.json record.",
            layout.node_record_file,
        )
        return None

    try:
        record = read_node_record(layout)
    except Exception as exc:  # pragma: no cover - defensive parsing path
        report.add_issue(
            "node_record_invalid_json",
            f"system/node.json could not be parsed: {exc}",
            layout.node_record_file,
        )
        return None

    required_top_level = (
        "schema_version",
        "identity",
        "task",
        "lifecycle",
        "control",
        "parameters",
        "progression",
    )
    for key in required_top_level:
        if key not in record:
            report.add_issue(
                "node_record_missing_field",
                f"system/node.json is missing top-level field {key!r}.",
                layout.node_record_file,
            )

    if record.get("schema_version") != NODE_RECORD_SCHEMA_VERSION:
        report.add_issue(
            "node_record_schema_version_invalid",
            f"Unsupported node schema version: {record.get('schema_version')!r}.",
            layout.node_record_file,
        )

    identity = record.get("identity")
    if not isinstance(identity, dict) or not isinstance(identity.get("node_id"), str):
        report.add_issue(
            "node_identity_invalid",
            "system/node.json must include identity.node_id.",
            layout.node_record_file,
        )

    task = record.get("task")
    if not isinstance(task, dict):
        report.add_issue(
            "node_task_invalid",
            "system/node.json must include a task block.",
            layout.node_record_file,
        )
    else:
        source_name = task.get("source_name")
        source_path = task.get("source_path")
        if source_name not in ("goal", "parent-instructions"):
            report.add_issue(
                "task_source_name_invalid",
                f"Unknown task.source_name: {source_name!r}.",
                layout.node_record_file,
            )
        if not isinstance(source_path, str) or not source_path.strip():
            report.add_issue(
                "task_source_path_invalid",
                "task.source_path must be a non-empty string.",
                layout.node_record_file,
            )

    progression = record.get("progression")
    if not isinstance(progression, dict):
        report.add_issue(
            "node_progression_invalid",
            "system/node.json must include a progression block.",
            layout.node_record_file,
        )

    control = record.get("control")
    if not isinstance(control, dict):
        report.add_issue(
            "node_control_invalid",
            "system/node.json must include a control block.",
            layout.node_record_file,
        )

    parameters = record.get("parameters")
    if not isinstance(parameters, dict):
        report.add_issue(
            "node_parameters_invalid",
            "system/node.json must include a parameters block.",
            layout.node_record_file,
        )

    return record


def _validate_lifecycle(
    layout: NodeLayout,
    record: dict[str, object],
    report: NodeValidationReport,
) -> None:
    lifecycle = record.get("lifecycle")
    if not isinstance(lifecycle, dict):
        report.add_issue(
            "node_lifecycle_invalid",
            "system/node.json must include a lifecycle block.",
            layout.node_record_file,
        )
        return

    status = lifecycle.get("status")
    if status not in NODE_STATUSES:
        report.add_issue(
            "status_invalid",
            f"Unknown node status: {status!r}.",
            layout.node_record_file,
        )
        return

    terminal_outcome = lifecycle.get("terminal_outcome")
    failure_reason = lifecycle.get("failure_reason")
    cancellation_reason = lifecycle.get("cancellation_reason")
    waiting_note = lifecycle.get("waiting_on_computation_note")
    computation_result_note = lifecycle.get("computation_result_note")
    retry_count = lifecycle.get("retry_count")

    if retry_count is not None and (not isinstance(retry_count, int) or retry_count < 0):
        report.add_issue(
            "retry_count_invalid",
            "lifecycle.retry_count must be a non-negative integer when present.",
            layout.node_record_file,
        )

    if status == "finished":
        if terminal_outcome not in TERMINAL_OUTCOMES:
            report.add_issue(
                "terminal_outcome_missing",
                "finished nodes must have a valid terminal outcome in system/node.json.",
                layout.node_record_file,
            )
        elif terminal_outcome == "completed" and not layout.final_output_file.exists():
            report.add_issue(
                "completed_output_missing",
                "Completed nodes must have output/final-output.md.",
                layout.final_output_file,
            )
        elif terminal_outcome == "escalated" and not layout.escalation_file.exists():
            report.add_issue(
                "escalation_output_missing",
                "Escalated nodes must have output/escalation.md.",
                layout.escalation_file,
            )
        elif terminal_outcome == "cancelled" and not isinstance(cancellation_reason, str):
            report.add_issue(
                "cancellation_reason_missing",
                "Cancelled nodes must have a cancellation reason in system/node.json.",
                layout.node_record_file,
            )
    elif terminal_outcome is not None:
        report.add_issue(
            "stale_terminal_outcome",
            "Non-finished nodes must not keep a terminal outcome in system/node.json.",
            layout.node_record_file,
        )

    if status == "failed":
        if not isinstance(failure_reason, str) or not failure_reason.strip():
            report.add_issue(
                "failure_reason_missing",
                "failed nodes must have a non-empty failure reason in system/node.json.",
                layout.node_record_file,
            )
    elif failure_reason is not None:
        report.add_issue(
            "stale_failure_reason",
            "Non-failed nodes must not keep a failure reason in system/node.json.",
            layout.node_record_file,
        )

    if status == "waiting_on_computation":
        if not isinstance(waiting_note, str) or not waiting_note.strip():
            report.add_issue(
                "waiting_note_missing",
                "waiting_on_computation nodes must have a waiting note in system/node.json.",
                layout.node_record_file,
            )
    elif waiting_note is not None:
        report.add_issue(
            "stale_waiting_note",
            "Only waiting_on_computation nodes may keep a waiting note in system/node.json.",
            layout.node_record_file,
        )

    if status != "waiting_on_computation" and computation_result_note is not None:
        report.add_issue(
            "stale_computation_result_note",
            "Only waiting_on_computation nodes may keep a computation result note.",
            layout.node_record_file,
        )

    if status != "finished" and cancellation_reason is not None:
        report.add_issue(
            "stale_cancellation_reason",
            "Only finished/cancelled nodes may keep a cancellation reason.",
            layout.node_record_file,
        )


def _validate_parameters(
    layout: NodeLayout,
    record: dict[str, object],
    report: NodeValidationReport,
) -> None:
    parameters = record.get("parameters")
    if not isinstance(parameters, dict):
        return

    sources = parameters.get("sources")
    if not isinstance(sources, dict):
        report.add_issue(
            "parameter_sources_invalid",
            "parameters.sources must be a dictionary.",
            layout.node_record_file,
        )
        return

    for key, value in sources.items():
        if value is None:
            continue
        if value not in ASSIGNMENT_SOURCES:
            report.add_issue(
                "parameter_source_invalid",
                f"parameters.sources[{key!r}] has invalid source {value!r}.",
                layout.node_record_file,
            )

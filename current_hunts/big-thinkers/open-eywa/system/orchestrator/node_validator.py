from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .node_contract import NODE_STATUSES, TERMINAL_OUTCOMES, NodeLayout, node_layout, read_trimmed_text


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
    _validate_status_block(layout, report)

    return report


def _validate_required_directories(layout: NodeLayout, report: NodeValidationReport) -> None:
    required_directories = (
        layout.input_dir,
        layout.output_dir,
        layout.orchestrator_dir,
        layout.system_dir,
        layout.children_dir,
    )
    for directory in required_directories:
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
        path
        for path in (layout.goal_file, layout.parent_instructions_file)
        if path.exists()
    ]
    if len(task_sources) != 1:
        report.add_issue(
            "task_source_count",
            "A node must have exactly one task source file.",
            layout.input_dir,
        )


def _validate_status_block(layout: NodeLayout, report: NodeValidationReport) -> None:
    status = read_trimmed_text(layout.status_file)
    if status is None:
        report.add_issue(
            "status_missing",
            "The node is missing its authoritative status file.",
            layout.status_file,
        )
        return
    if status not in NODE_STATUSES:
        report.add_issue(
            "status_invalid",
            f"Unknown node status: {status!r}.",
            layout.status_file,
        )
        return

    if status == "finished":
        _validate_finished_node(layout, report)
    else:
        if layout.terminal_outcome_file.exists():
            report.add_issue(
                "stale_terminal_outcome",
                "Non-finished nodes must not keep a terminal outcome file.",
                layout.terminal_outcome_file,
            )
        if layout.cancellation_reason_file.exists():
            report.add_issue(
                "stale_cancellation_reason",
                "Only cancelled nodes may keep a cancellation reason file.",
                layout.cancellation_reason_file,
            )

    if status == "failed":
        _validate_failed_node(layout, report)
    else:
        if layout.failure_reason_file.exists():
            report.add_issue(
                "stale_failure_reason",
                "Non-failed nodes must not keep a failure reason file.",
                layout.failure_reason_file,
            )

    if status == "waiting_on_computation":
        if not layout.waiting_marker_file.exists():
            report.add_issue(
                "waiting_marker_missing",
                "waiting_on_computation nodes must have a WAITING_FOR_COMPUTATION marker.",
                layout.waiting_marker_file,
            )
    elif layout.waiting_marker_file.exists():
        report.add_issue(
            "stale_waiting_marker",
            "Only waiting_on_computation nodes may keep a WAITING_FOR_COMPUTATION marker.",
            layout.waiting_marker_file,
        )

    if status != "waiting_on_computation" and layout.computation_result_file.exists():
        report.add_issue(
            "stale_computation_result",
            "Only waiting_on_computation nodes may keep a computation result marker.",
            layout.computation_result_file,
        )


def _validate_finished_node(layout: NodeLayout, report: NodeValidationReport) -> None:
    outcome = read_trimmed_text(layout.terminal_outcome_file)
    if outcome is None:
        report.add_issue(
            "terminal_outcome_missing",
            "finished nodes must have a terminal outcome file.",
            layout.terminal_outcome_file,
        )
        return
    if outcome not in TERMINAL_OUTCOMES:
        report.add_issue(
            "terminal_outcome_invalid",
            f"Unknown terminal outcome: {outcome!r}.",
            layout.terminal_outcome_file,
        )
        return
    if outcome == "completed" and not layout.final_output_file.exists():
        report.add_issue(
            "completed_output_missing",
            "Completed nodes must have output/final-output.md.",
            layout.final_output_file,
        )
    if outcome == "escalated" and not layout.escalation_file.exists():
        report.add_issue(
            "escalation_output_missing",
            "Escalated nodes must have output/escalation.md.",
            layout.escalation_file,
        )
    if outcome == "cancelled":
        cancellation_reason = read_trimmed_text(layout.cancellation_reason_file)
        if cancellation_reason is None:
            report.add_issue(
                "cancellation_reason_missing",
                "Cancelled nodes must have a cancellation reason file.",
                layout.cancellation_reason_file,
            )
        elif not cancellation_reason:
            report.add_issue(
                "cancellation_reason_blank",
                "Cancelled nodes must have a non-empty cancellation reason.",
                layout.cancellation_reason_file,
            )
    elif layout.cancellation_reason_file.exists():
        report.add_issue(
            "stale_cancellation_reason",
            "Only cancelled nodes may keep a cancellation reason file.",
            layout.cancellation_reason_file,
        )


def _validate_failed_node(layout: NodeLayout, report: NodeValidationReport) -> None:
    failure_reason = read_trimmed_text(layout.failure_reason_file)
    if failure_reason is None:
        report.add_issue(
            "failure_reason_missing",
            "failed nodes must have a failure reason file.",
            layout.failure_reason_file,
        )
    elif not failure_reason:
        report.add_issue(
            "failure_reason_blank",
            "failed nodes must have a non-empty failure reason.",
            layout.failure_reason_file,
        )

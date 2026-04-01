from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

NodeStatus = Literal["pending", "active", "waiting_on_computation", "finished", "failed"]
TaskSourceName = Literal["goal", "parent-instructions"]
TerminalOutcome = Literal["completed", "escalated", "cancelled"]

NODE_STATUSES: tuple[NodeStatus, ...] = (
    "pending",
    "active",
    "waiting_on_computation",
    "finished",
    "failed",
)

TERMINAL_OUTCOMES: tuple[TerminalOutcome, ...] = (
    "completed",
    "escalated",
    "cancelled",
)

NODE_SUBDIRECTORIES = ("input", "output", "for-orchestrator", "system", "children")
SYSTEM_SUBDIRECTORIES = ("runs", "artifacts", "jobs", "recoveries")


@dataclass(frozen=True)
class NodeLayout:
    root: Path

    @property
    def input_dir(self) -> Path:
        return self.root / "input"

    @property
    def output_dir(self) -> Path:
        return self.root / "output"

    @property
    def orchestrator_dir(self) -> Path:
        return self.root / "for-orchestrator"

    @property
    def system_dir(self) -> Path:
        return self.root / "system"

    @property
    def children_dir(self) -> Path:
        return self.root / "children"

    @property
    def runs_dir(self) -> Path:
        return self.system_dir / "runs"

    @property
    def artifacts_dir(self) -> Path:
        return self.system_dir / "artifacts"

    @property
    def jobs_dir(self) -> Path:
        return self.system_dir / "jobs"

    @property
    def recoveries_dir(self) -> Path:
        return self.system_dir / "recoveries"

    @property
    def events_log_file(self) -> Path:
        return self.system_dir / "events.jsonl"

    @property
    def usage_summary_file(self) -> Path:
        return self.system_dir / "usage-summary.json"

    @property
    def cost_summary_file(self) -> Path:
        return self.system_dir / "cost-summary.json"

    @property
    def progression_state_file(self) -> Path:
        return self.system_dir / "progression-state.json"

    @property
    def latest_child_node_report_file(self) -> Path:
        return self.system_dir / "latest-child-node-report.json"

    @property
    def goal_file(self) -> Path:
        return self.input_dir / "goal.md"

    @property
    def parent_instructions_file(self) -> Path:
        return self.input_dir / "parent-instructions.md"

    @property
    def context_file(self) -> Path:
        return self.input_dir / "context.md"

    @property
    def retrieved_knowledge_file(self) -> Path:
        return self.input_dir / "retrieved_relevant_knowledge_from_library.md"

    @property
    def plan_file(self) -> Path:
        return self.output_dir / "plan.md"

    @property
    def review_file(self) -> Path:
        return self.output_dir / "review.md"

    @property
    def final_output_file(self) -> Path:
        return self.output_dir / "final-output.md"

    @property
    def state_file(self) -> Path:
        return self.output_dir / "state.md"

    @property
    def escalation_file(self) -> Path:
        return self.output_dir / "escalation.md"

    @property
    def agent_mode_file(self) -> Path:
        return self.orchestrator_dir / "agent-mode"

    @property
    def status_file(self) -> Path:
        return self.orchestrator_dir / "this-nodes-current-status"

    @property
    def next_action_after_child_report_file(self) -> Path:
        return self.orchestrator_dir / "next-action-after-child-report"

    @property
    def terminal_outcome_file(self) -> Path:
        return self.orchestrator_dir / "terminal-outcome"

    @property
    def failure_reason_file(self) -> Path:
        return self.orchestrator_dir / "failure-reason"

    @property
    def cancellation_reason_file(self) -> Path:
        return self.orchestrator_dir / "cancellation-reason"

    @property
    def waiting_marker_file(self) -> Path:
        return self.orchestrator_dir / "WAITING_FOR_COMPUTATION"

    @property
    def computation_result_file(self) -> Path:
        return self.orchestrator_dir / "computation_result"

    def run_dir(self, run_id: str) -> Path:
        return self.runs_dir / run_id

    def run_request_file(self, run_id: str) -> Path:
        return self.run_dir(run_id) / "request.json"

    def run_result_file(self, run_id: str) -> Path:
        return self.run_dir(run_id) / "result.json"

    def run_summary_file(self, run_id: str) -> Path:
        return self.run_dir(run_id) / "summary.json"

    def run_usage_file(self, run_id: str) -> Path:
        return self.run_dir(run_id) / "usage.json"

    def run_prepared_node_context_file(self, run_id: str) -> Path:
        return self.run_dir(run_id) / "prepared-node-context.json"


def node_layout(node_path: str | Path) -> NodeLayout:
    return NodeLayout(Path(node_path).expanduser().resolve())


def read_trimmed_text(path: Path) -> str | None:
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8").strip()


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def unlink_if_exists(path: Path) -> None:
    if path.exists():
        path.unlink()


def create_node(
    node_path: str | Path,
    *,
    task_source_name: TaskSourceName,
    task_text: str,
    initial_status: NodeStatus = "pending",
    agent_mode: str | None = None,
    terminal_outcome: TerminalOutcome | None = None,
    failure_reason: str | None = None,
    cancellation_reason: str | None = None,
    waiting_note: str | None = None,
) -> NodeLayout:
    if initial_status not in NODE_STATUSES:
        raise ValueError(f"Unknown node status: {initial_status}")
    if task_source_name not in ("goal", "parent-instructions"):
        raise ValueError(f"Unknown task source name: {task_source_name}")
    if initial_status == "finished" and terminal_outcome not in TERMINAL_OUTCOMES:
        raise ValueError("finished nodes require a valid terminal outcome")
    if initial_status == "finished" and terminal_outcome == "cancelled" and not (cancellation_reason or "").strip():
        raise ValueError("cancelled nodes require a cancellation reason")
    if initial_status == "failed" and not (failure_reason or "").strip():
        raise ValueError("failed nodes require a failure reason")

    layout = node_layout(node_path)
    layout.root.mkdir(parents=True, exist_ok=True)

    for subdirectory in NODE_SUBDIRECTORIES:
        (layout.root / subdirectory).mkdir(parents=True, exist_ok=True)
    for subdirectory in SYSTEM_SUBDIRECTORIES:
        (layout.system_dir / subdirectory).mkdir(parents=True, exist_ok=True)

    task_path = layout.goal_file if task_source_name == "goal" else layout.parent_instructions_file
    other_task_path = (
        layout.parent_instructions_file if task_source_name == "goal" else layout.goal_file
    )
    write_text(task_path, task_text.rstrip() + "\n")
    unlink_if_exists(other_task_path)

    write_text(layout.status_file, initial_status + "\n")

    if agent_mode:
        write_text(layout.agent_mode_file, agent_mode.strip() + "\n")
    else:
        unlink_if_exists(layout.agent_mode_file)

    if initial_status == "finished":
        write_text(layout.terminal_outcome_file, terminal_outcome + "\n")
    else:
        unlink_if_exists(layout.terminal_outcome_file)

    if initial_status == "finished" and terminal_outcome == "cancelled":
        write_text(layout.cancellation_reason_file, cancellation_reason.strip() + "\n")
    else:
        unlink_if_exists(layout.cancellation_reason_file)

    if initial_status == "failed":
        write_text(layout.failure_reason_file, failure_reason.strip() + "\n")
    else:
        unlink_if_exists(layout.failure_reason_file)

    if initial_status == "waiting_on_computation":
        note = (waiting_note or "waiting for background computation").strip()
        write_text(layout.waiting_marker_file, note + "\n")
    else:
        unlink_if_exists(layout.waiting_marker_file)

    return layout

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from .node_record import AssignmentSource, build_initial_node_record, write_node_record

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

NODE_SUBDIRECTORIES = ("input", "output", "system", "children")
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
    def node_record_file(self) -> Path:
        return self.system_dir / "node.json"

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

    def run_node_record_file(self, run_id: str) -> Path:
        return self.run_dir(run_id) / "node.json"


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
    next_role: str | None = None,
    agent_mode: str | None = None,
    terminal_outcome: TerminalOutcome | None = None,
    failure_reason: str | None = None,
    cancellation_reason: str | None = None,
    waiting_note: str | None = None,
    node_id: str | None = None,
    parent_node_id: str | None = None,
    model: str | None = None,
    variant: str | None = None,
    model_source: AssignmentSource | None = None,
    variant_source: AssignmentSource | None = None,
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

    resolved_next_role = (next_role or agent_mode or "").strip() or None
    waiting_on_computation_note = (
        (waiting_note or "waiting for background computation").strip()
        if initial_status == "waiting_on_computation"
        else None
    )
    record = build_initial_node_record(
        node_id=node_id or layout.root.name,
        parent_node_id=parent_node_id,
        task_source_name=task_source_name,
        task_source_path=str(task_path.relative_to(layout.root)),
        initial_status=initial_status,
        next_role=resolved_next_role,
        terminal_outcome=terminal_outcome if initial_status == "finished" else None,
        failure_reason=failure_reason.strip() if initial_status == "failed" else None,
        cancellation_reason=(
            cancellation_reason.strip()
            if initial_status == "finished" and terminal_outcome == "cancelled"
            else None
        ),
        waiting_on_computation_note=waiting_on_computation_note,
        model=model,
        variant=variant,
        model_source=model_source,
        variant_source=variant_source,
    )
    write_node_record(layout, record)
    return layout

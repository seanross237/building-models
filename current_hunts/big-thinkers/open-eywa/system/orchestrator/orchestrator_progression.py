from __future__ import annotations

from dataclasses import dataclass
import json
import re
from pathlib import Path
from typing import Any, Callable

from system.runtime.runtime_interface import RuntimeAdapter

from .event_schema import EventRecord
from .event_writer import AppendOnlyJsonlWriter
from .node_contract import create_node, node_layout, read_trimmed_text, unlink_if_exists, write_text
from .node_controls import resume_waiting_node_if_ready
from .node_lifecycle import transition_node
from .node_recovery import prepare_node_for_fresh_attempt
from .orchestrator_core import NodeOrchestratorCore, NodeRunStepResult
from .node_validator import validate_node

RuntimeMetadataResolver = Callable[[str, str, str, Path], dict[str, Any]]


class OrchestratorProgressionError(RuntimeError):
    """Raised when multi-run node progression cannot safely continue."""


@dataclass(frozen=True)
class NodeProgressionResult:
    mission_id: str
    node_id: str
    node_path: str
    final_status: str
    terminal_outcome: str | None
    failure_reason: str | None
    iterations: int


class NodeProgressionEngine:
    def __init__(
        self,
        runtime: RuntimeAdapter,
        *,
        runtime_metadata_resolver: RuntimeMetadataResolver | None = None,
    ) -> None:
        self.core = NodeOrchestratorCore(runtime)
        self.runtime_metadata_resolver = runtime_metadata_resolver

    def drive_until_stable(
        self,
        node_path: str | Path,
        *,
        mission_id: str,
        node_id: str,
        max_iterations: int = 100,
    ) -> NodeProgressionResult:
        layout = node_layout(node_path)
        for iteration in range(1, max_iterations + 1):
            status = read_trimmed_text(layout.status_file)
            if status == "waiting_on_computation":
                if self._maybe_resume_waiting_node(layout, mission_id=mission_id, node_id=node_id):
                    continue
                return self._stable_result(
                    layout,
                    mission_id=mission_id,
                    node_id=node_id,
                    iterations=iteration - 1,
                )

            if status in ("finished", "failed"):
                return self._stable_result(
                    layout,
                    mission_id=mission_id,
                    node_id=node_id,
                    iterations=iteration - 1,
                )

            made_progress = self._advance_once(layout, mission_id=mission_id, node_id=node_id)
            if not made_progress:
                raise OrchestratorProgressionError(
                    f"Node {node_id!r} could not make progress from status {status!r}."
                )

        raise OrchestratorProgressionError(
            f"Node {node_id!r} did not stabilize within {max_iterations} iterations."
        )

    def _stable_result(
        self,
        layout,
        *,
        mission_id: str,
        node_id: str,
        iterations: int,
    ) -> NodeProgressionResult:
        return NodeProgressionResult(
            mission_id=mission_id,
            node_id=node_id,
            node_path=str(layout.root),
            final_status=read_trimmed_text(layout.status_file) or "failed",
            terminal_outcome=read_trimmed_text(layout.terminal_outcome_file),
            failure_reason=read_trimmed_text(layout.failure_reason_file),
            iterations=iterations,
        )

    def _advance_once(self, layout, *, mission_id: str, node_id: str) -> bool:
        if read_trimmed_text(layout.status_file) in (
            "finished",
            "failed",
            "waiting_on_computation",
        ):
            return False

        if self._should_run_direct_role(layout):
            role = read_trimmed_text(layout.agent_mode_file) or "planner"
            write_text(layout.agent_mode_file, role + "\n")
            self._run_role(layout, mission_id=mission_id, node_id=node_id, role=role)
            return True

        if layout.plan_file.exists() and not layout.progression_state_file.exists():
            self._initialize_progression_state(layout, mission_id=mission_id, node_id=node_id)
            return True

        if layout.progression_state_file.exists():
            return self._advance_planned_parent(layout, mission_id=mission_id, node_id=node_id)

        return False

    def _should_run_direct_role(self, layout) -> bool:
        return (
            not layout.plan_file.exists()
            and not layout.progression_state_file.exists()
            and not layout.final_output_file.exists()
            and not layout.escalation_file.exists()
        )

    def _run_role(
        self,
        layout,
        *,
        mission_id: str,
        node_id: str,
        role: str,
    ) -> NodeRunStepResult:
        metadata = (
            self.runtime_metadata_resolver(mission_id, node_id, role, layout.root)
            if self.runtime_metadata_resolver
            else {}
        )
        return self.core.run_once(
            layout.root,
            mission_id=mission_id,
            node_id=node_id,
            role=role,
            runtime_metadata=metadata,
        )

    def _initialize_progression_state(self, layout, *, mission_id: str, node_id: str) -> None:
        steps = self._parse_plan_steps(layout.plan_file.read_text(encoding="utf-8"))
        if not steps:
            raise OrchestratorProgressionError("Planner produced a plan with no executable steps.")
        state = {
            "steps": [
                {
                    "index": index,
                    "title": step["title"],
                    "goal": step["goal"],
                    "child_name": f"step-{index + 1:02d}-{self._slugify(step['title'])}",
                    "latest_child_status": None,
                    "latest_terminal_outcome": None,
                    "latest_failure_reason": None,
                }
                for index, step in enumerate(steps)
            ],
            "current_step_index": 0,
        }
        write_text(layout.progression_state_file, json.dumps(state, indent=2, sort_keys=True) + "\n")
        self._emit_event(
            layout,
            EventRecord(
                event_type="plan_parsed",
                mission_id=mission_id,
                node_id=node_id,
                node_path=str(layout.root),
                payload={"step_count": len(steps)},
            ),
        )
        for step in state["steps"]:
            self._emit_event(
                layout,
                EventRecord(
                    event_type="plan_step_registered",
                    mission_id=mission_id,
                    node_id=node_id,
                    node_path=str(layout.root),
                    payload={
                        "step_index": step["index"],
                        "step_title": step["title"],
                        "child_name": step["child_name"],
                    },
                ),
            )

    def _advance_planned_parent(self, layout, *, mission_id: str, node_id: str) -> bool:
        state = self._read_progression_state(layout)
        steps = state["steps"]
        current_step_index = state["current_step_index"]

        if current_step_index >= len(steps):
            write_text(layout.agent_mode_file, "synthesizer\n")
            self._run_role(layout, mission_id=mission_id, node_id=node_id, role="synthesizer")
            return True

        step = steps[current_step_index]
        child_name = step["child_name"]
        child_path = layout.children_dir / child_name
        child_node_id = f"{node_id}.{child_name}"

        if not child_path.exists():
            self._create_child_node(
                layout,
                child_path,
                mission_id=mission_id,
                parent_node_id=node_id,
                child_node_id=child_node_id,
                step_index=step["index"],
                step_title=step["title"],
                step_goal=step["goal"],
            )
            return True

        child_layout = node_layout(child_path)
        child_status = read_trimmed_text(child_layout.status_file)
        if child_status not in ("finished", "failed", "waiting_on_computation"):
            self.drive_until_stable(
                child_path,
                mission_id=mission_id,
                node_id=child_node_id,
            )
            return True

        child_terminal_outcome = read_trimmed_text(child_layout.terminal_outcome_file)
        child_failure_reason = read_trimmed_text(child_layout.failure_reason_file)
        self._write_latest_child_report(
            layout,
            child_node_id=child_node_id,
            child_layout=child_layout,
            step=step,
            child_status=child_status,
            child_terminal_outcome=child_terminal_outcome,
            child_failure_reason=child_failure_reason,
        )
        self._emit_event(
            layout,
            EventRecord(
                event_type="child_node_report_received",
                mission_id=mission_id,
                node_id=node_id,
                node_path=str(layout.root),
                payload={
                    "child_node_id": child_node_id,
                    "child_status": child_status,
                    "terminal_outcome": child_terminal_outcome,
                    "failure_reason": child_failure_reason,
                },
            ),
        )

        if child_status == "waiting_on_computation":
            current_status = read_trimmed_text(layout.status_file)
            if current_status == "active":
                transition_node(
                    layout.root,
                    next_status="waiting_on_computation",
                    expected_current_status="active",
                    waiting_note=f"waiting on child node {child_node_id}",
                )
                self._emit_status_change(
                    layout,
                    mission_id=mission_id,
                    node_id=node_id,
                    role="mid-plan-evaluator",
                    status_before="active",
                    status_after="waiting_on_computation",
                )
            self._emit_parent_next_action(
                layout,
                mission_id=mission_id,
                node_id=node_id,
                child_node_id=child_node_id,
                next_action="wait",
            )
            return True

        write_text(layout.agent_mode_file, "mid-plan-evaluator\n")
        self._run_role(layout, mission_id=mission_id, node_id=node_id, role="mid-plan-evaluator")
        return self._consume_next_action_after_child_report(
            layout,
            mission_id=mission_id,
            node_id=node_id,
            state=state,
            step=step,
            child_node_id=child_node_id,
            child_status=child_status,
            child_terminal_outcome=child_terminal_outcome,
        )

    def _consume_next_action_after_child_report(
        self,
        layout,
        *,
        mission_id: str,
        node_id: str,
        state: dict[str, Any],
        step: dict[str, Any],
        child_node_id: str,
        child_status: str,
        child_terminal_outcome: str | None,
    ) -> bool:
        next_action = read_trimmed_text(layout.next_action_after_child_report_file)
        if not next_action:
            raise OrchestratorProgressionError(
                "Evaluator completed without next-action-after-child-report."
            )

        self._emit_parent_next_action(
            layout,
            mission_id=mission_id,
            node_id=node_id,
            child_node_id=child_node_id,
            next_action=next_action,
        )

        if next_action == "continue":
            if child_status == "finished" and child_terminal_outcome == "completed":
                self._emit_event(
                    layout,
                    EventRecord(
                        event_type="plan_step_completed",
                        mission_id=mission_id,
                        node_id=node_id,
                        node_path=str(layout.root),
                        payload={
                            "step_index": step["index"],
                            "child_node_id": child_node_id,
                        },
                    ),
                )
            elif child_status in ("failed", "finished"):
                self._emit_event(
                    layout,
                    EventRecord(
                        event_type="plan_step_failed",
                        mission_id=mission_id,
                        node_id=node_id,
                        node_path=str(layout.root),
                        payload={
                            "step_index": step["index"],
                            "child_node_id": child_node_id,
                            "child_status": child_status,
                            "terminal_outcome": child_terminal_outcome,
                        },
                    ),
                )
            state["steps"][step["index"]]["latest_child_status"] = child_status
            state["steps"][step["index"]]["latest_terminal_outcome"] = child_terminal_outcome
            state["current_step_index"] += 1
            write_text(
                layout.progression_state_file,
                json.dumps(state, indent=2, sort_keys=True) + "\n",
            )
            unlink_if_exists(layout.next_action_after_child_report_file)
            return True

        if next_action == "replan":
            self._emit_event(
                layout,
                EventRecord(
                    event_type="plan_step_failed",
                    mission_id=mission_id,
                    node_id=node_id,
                    node_path=str(layout.root),
                    payload={
                        "step_index": step["index"],
                        "child_node_id": child_node_id,
                        "child_status": child_status,
                        "terminal_outcome": child_terminal_outcome,
                    },
                ),
            )
            prepare_node_for_fresh_attempt(
                layout.root,
                recovery_reason="evaluator_requested_replan",
                next_role="planner",
                mission_id=mission_id,
                node_id=node_id,
            )
            return True

        if next_action == "escalate":
            self._emit_event(
                layout,
                EventRecord(
                    event_type="plan_step_failed",
                    mission_id=mission_id,
                    node_id=node_id,
                    node_path=str(layout.root),
                    payload={
                        "step_index": step["index"],
                        "child_node_id": child_node_id,
                        "child_status": child_status,
                        "terminal_outcome": child_terminal_outcome,
                    },
                ),
            )
            if read_trimmed_text(layout.status_file) == "finished":
                unlink_if_exists(layout.next_action_after_child_report_file)
                return True
            if not layout.escalation_file.exists():
                raise OrchestratorProgressionError(
                    "Evaluator requested escalate without creating output/escalation.md."
                )
            transition_node(
                layout.root,
                next_status="finished",
                expected_current_status="active",
                terminal_outcome="escalated",
            )
            self._emit_status_change(
                layout,
                mission_id=mission_id,
                node_id=node_id,
                role="mid-plan-evaluator",
                status_before="active",
                status_after="finished",
            )
            self._emit_event(
                layout,
                EventRecord(
                    event_type="node_escalated",
                    mission_id=mission_id,
                    node_id=node_id,
                    node_path=str(layout.root),
                    role="mid-plan-evaluator",
                    payload={"terminal_outcome": "escalated"},
                )
            )
            unlink_if_exists(layout.next_action_after_child_report_file)
            return True

        raise OrchestratorProgressionError(
            f"Unsupported next-action-after-child-report value: {next_action!r}."
        )

    def _create_child_node(
        self,
        parent_layout,
        child_path: Path,
        *,
        mission_id: str,
        parent_node_id: str,
        child_node_id: str,
        step_index: int,
        step_title: str,
        step_goal: str,
    ) -> None:
        child_layout = create_node(
            child_path,
            task_source_name="parent-instructions",
            task_text=step_goal,
            agent_mode="worker",
        )
        child_context = self._build_child_context(
            parent_layout,
            step_index=step_index,
        )
        if child_context:
            write_text(child_layout.context_file, child_context)
        self._emit_event(
            parent_layout,
            EventRecord(
                event_type="child_node_created",
                mission_id=mission_id,
                node_id=parent_node_id,
                node_path=str(parent_layout.root),
                payload={
                    "child_node_id": child_node_id,
                    "child_node_path": str(child_layout.root),
                    "step_index": step_index,
                    "step_title": step_title,
                },
            ),
        )
        AppendOnlyJsonlWriter(child_layout.events_log_file).append_event(
            EventRecord(
                event_type="node_created",
                mission_id=mission_id,
                node_id=child_node_id,
                node_path=str(child_layout.root),
                payload={"task_source": "parent-instructions"},
            )
        )
        report = validate_node(child_layout.root)
        if not report.is_valid:
            raise OrchestratorProgressionError(f"Created child node is invalid: {report.issues!r}")

    def _build_child_context(
        self,
        parent_layout,
        *,
        step_index: int,
    ) -> str:
        sections: list[str] = []

        parent_task = self._task_source_text(parent_layout)
        if parent_task:
            sections.append("## Parent Task\n" + parent_task)

        if parent_layout.plan_file.exists():
            sections.append("## Parent Plan\n" + parent_layout.plan_file.read_text(encoding="utf-8").strip())

        if parent_layout.state_file.exists():
            sections.append("## Parent State\n" + parent_layout.state_file.read_text(encoding="utf-8").strip())

        completed_child_sections: list[str] = []
        state = self._read_progression_state(parent_layout) if parent_layout.progression_state_file.exists() else None
        previous_steps = state["steps"][:step_index] if state else []
        for previous_step in previous_steps:
            child_layout = node_layout(parent_layout.children_dir / previous_step["child_name"])
            if child_layout.final_output_file.exists():
                completed_child_sections.append(
                    "\n".join(
                        [
                            f"### {previous_step['title']}",
                            child_layout.final_output_file.read_text(encoding="utf-8").strip(),
                        ]
                    )
                )
            elif child_layout.escalation_file.exists():
                completed_child_sections.append(
                    "\n".join(
                        [
                            f"### {previous_step['title']} (Escalated)",
                            child_layout.escalation_file.read_text(encoding="utf-8").strip(),
                        ]
                    )
                )
        if completed_child_sections:
            sections.append("## Prior Completed Step Results\n" + "\n\n".join(completed_child_sections))

        if not sections:
            return ""
        return "\n\n".join(sections).strip() + "\n"

    def _task_source_text(self, layout) -> str:
        if layout.goal_file.exists():
            return layout.goal_file.read_text(encoding="utf-8").strip()
        if layout.parent_instructions_file.exists():
            return layout.parent_instructions_file.read_text(encoding="utf-8").strip()
        return ""

    def _maybe_resume_waiting_node(self, layout, *, mission_id: str, node_id: str) -> bool:
        resume_result = resume_waiting_node_if_ready(layout.root)
        if resume_result.resumed:
            self._emit_status_change(
                layout,
                mission_id=mission_id,
                node_id=node_id,
                role=read_trimmed_text(layout.agent_mode_file) or "worker",
                status_before="waiting_on_computation",
                status_after="active",
            )
            return True

        if not layout.progression_state_file.exists():
            return False

        state = self._read_progression_state(layout)
        current_step_index = state["current_step_index"]
        steps = state["steps"]
        if current_step_index >= len(steps):
            return False

        child_path = layout.children_dir / steps[current_step_index]["child_name"]
        if not child_path.exists():
            return False

        child_layout = node_layout(child_path)
        child_status = read_trimmed_text(child_layout.status_file)
        child_node_id = f"{node_id}.{steps[current_step_index]['child_name']}"
        if child_status == "waiting_on_computation" and child_layout.computation_result_file.exists():
            self.drive_until_stable(
                child_path,
                mission_id=mission_id,
                node_id=child_node_id,
            )
            child_status = read_trimmed_text(child_layout.status_file)
        if child_status in ("finished", "failed"):
            transition_node(
                layout.root,
                next_status="active",
                expected_current_status="waiting_on_computation",
            )
            self._emit_status_change(
                layout,
                mission_id=mission_id,
                node_id=node_id,
                role="mid-plan-evaluator",
                status_before="waiting_on_computation",
                status_after="active",
            )
            return True

        return False

    def _write_latest_child_report(
        self,
        layout,
        *,
        child_node_id: str,
        child_layout,
        step: dict[str, Any],
        child_status: str,
        child_terminal_outcome: str | None,
        child_failure_reason: str | None,
    ) -> None:
        report = {
            "child_node_id": child_node_id,
            "child_node_path": str(child_layout.root),
            "step_index": step["index"],
            "step_title": step["title"],
            "child_status": child_status,
            "terminal_outcome": child_terminal_outcome,
            "failure_reason": child_failure_reason,
        }
        write_text(
            layout.latest_child_node_report_file,
            json.dumps(report, indent=2, sort_keys=True) + "\n",
        )

    def _emit_parent_next_action(
        self,
        layout,
        *,
        mission_id: str,
        node_id: str,
        child_node_id: str,
        next_action: str,
    ) -> None:
        self._emit_event(
            layout,
            EventRecord(
                event_type="parent_next_action_chosen",
                mission_id=mission_id,
                node_id=node_id,
                node_path=str(layout.root),
                payload={
                    "child_node_id": child_node_id,
                    "next_action": next_action,
                },
            ),
        )

    def _emit_status_change(
        self,
        layout,
        *,
        mission_id: str,
        node_id: str,
        role: str,
        status_before: str,
        status_after: str,
    ) -> None:
        self._emit_event(
            layout,
            EventRecord(
                event_type="node_status_changed",
                mission_id=mission_id,
                node_id=node_id,
                node_path=str(layout.root),
                role=role,
                payload={"status_before": status_before, "status_after": status_after},
            ),
        )

    def _emit_event(self, layout, event: EventRecord) -> None:
        AppendOnlyJsonlWriter(layout.events_log_file).append_event(event)

    def _read_progression_state(self, layout) -> dict[str, Any]:
        return json.loads(layout.progression_state_file.read_text(encoding="utf-8"))

    def _parse_plan_steps(self, plan_text: str) -> list[dict[str, str]]:
        structured_steps = self._parse_structured_plan_steps(plan_text)
        if structured_steps:
            return structured_steps
        return self._parse_list_plan_steps(plan_text)

    def _parse_structured_plan_steps(self, plan_text: str) -> list[dict[str, str]]:
        steps: list[dict[str, str]] = []
        current_title: str | None = None
        current_goal: str | None = None
        for line in plan_text.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            step_match = re.match(r"^#{3,}\s*Step\s+\d+\s*:\s*(.+?)\s*$", stripped, re.IGNORECASE)
            if step_match:
                if current_title and current_goal:
                    steps.append({"title": current_title, "goal": current_goal})
                current_title = step_match.group(1).strip()
                current_goal = None
                continue
            if current_title and current_goal is None:
                goal_match = re.match(r"^Goal:\s*(.+?)\s*$", stripped, re.IGNORECASE)
                if goal_match:
                    current_goal = goal_match.group(1).strip()
        if current_title and current_goal:
            steps.append({"title": current_title, "goal": current_goal})
        return steps

    def _parse_list_plan_steps(self, plan_text: str) -> list[dict[str, str]]:
        steps: list[dict[str, str]] = []
        for line in plan_text.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            numbered_match = re.match(r"^\d+\.\s+(.*)$", stripped)
            if numbered_match:
                title = numbered_match.group(1).strip()
                steps.append({"title": title, "goal": title})
                continue
            bullet_match = re.match(r"^[-*]\s+(.*)$", stripped)
            if bullet_match:
                title = bullet_match.group(1).strip()
                steps.append({"title": title, "goal": title})
        return steps

    def _slugify(self, text: str) -> str:
        slug = re.sub(r"[^A-Za-z0-9]+", "-", text).strip("-").lower()
        return slug or "step"

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

from .event_schema import EventRecord
from .event_writer import AppendOnlyJsonlWriter
from .mission_contract import MissionLayout, create_mission, mission_layout
from .node_contract import node_layout, read_trimmed_text, write_text
from .orchestrator_progression import (
    NodeProgressionEngine,
    NodeProgressionResult,
    OrchestratorProgressionError,
)
from .summary_schema import MissionSummary
from .usage_schema import CostRecord, UsageRecord


@dataclass(frozen=True)
class MissionDriveResult:
    mission_id: str
    mission_path: str
    root_node_id: str
    root_node_path: str
    final_status: str
    terminal_outcome: str | None
    failure_reason: str | None
    node_count: int
    run_count: int


class MissionDriverError(RuntimeError):
    """Raised when mission-level tree driving cannot safely continue."""


class MissionDriver:
    def __init__(self, progression_engine: NodeProgressionEngine) -> None:
        self.progression_engine = progression_engine

    def drive_until_stable(
        self,
        mission_path: str | Path,
        *,
        mission_id: str | None = None,
        max_iterations: int = 100,
    ) -> MissionDriveResult:
        layout = mission_layout(mission_path)
        mission_name = mission_id or layout.root.name
        self._ensure_mission_root_exists(layout)

        self._emit_mission_event(
            layout,
            mission_name,
            EventRecord(
                event_type="mission_drive_started",
                mission_id=mission_name,
                node_id="root",
                node_path=str(layout.root_node_dir),
                payload={
                    "mission_path": str(layout.root),
                    "root_node_id": "root",
                },
            ),
        )

        try:
            root_result = self.progression_engine.drive_until_stable(
                layout.root_node_dir,
                mission_id=mission_name,
                node_id="root",
                max_iterations=max_iterations,
            )
        except OrchestratorProgressionError as exc:
            self._emit_mission_event(
                layout,
                mission_name,
                EventRecord(
                    event_type="mission_drive_failed",
                    mission_id=mission_name,
                    node_id="root",
                    node_path=str(layout.root_node_dir),
                    payload={
                        "mission_path": str(layout.root),
                        "root_node_id": "root",
                        "failure_reason": str(exc),
                    },
                ),
            )
            raise MissionDriverError(str(exc)) from exc

        summary = self._build_mission_summary(layout, mission_name, root_result)
        write_text(layout.mission_summary_file, json.dumps(summary.to_dict(), indent=2, sort_keys=True) + "\n")

        self._emit_mission_event(
            layout,
            mission_name,
            EventRecord(
                event_type="mission_drive_completed",
                mission_id=mission_name,
                node_id="root",
                node_path=str(layout.root_node_dir),
                payload={
                    "mission_path": str(layout.root),
                    "root_node_id": "root",
                    "final_status": root_result.final_status,
                    "terminal_outcome": root_result.terminal_outcome,
                },
            ),
        )

        return MissionDriveResult(
            mission_id=mission_name,
            mission_path=str(layout.root),
            root_node_id="root",
            root_node_path=str(layout.root_node_dir),
            final_status=root_result.final_status,
            terminal_outcome=root_result.terminal_outcome,
            failure_reason=root_result.failure_reason,
            node_count=summary.node_count,
            run_count=summary.run_count,
        )

    def _ensure_mission_root_exists(self, layout: MissionLayout) -> None:
        if layout.root_node_dir.exists():
            return
        if not layout.mission_goal_file.exists():
            raise MissionDriverError(
                "Mission is missing both tree/root and mission-goal.md."
            )
        create_mission(layout.root, goal_text=layout.mission_goal_file.read_text(encoding="utf-8"))

    def _emit_mission_event(
        self,
        layout: MissionLayout,
        mission_id: str,
        event: EventRecord,
    ) -> None:
        del mission_id
        AppendOnlyJsonlWriter(layout.mission_events_log_file).append_event(event)

    def _build_mission_summary(
        self,
        layout: MissionLayout,
        mission_id: str,
        root_result: NodeProgressionResult,
    ) -> MissionSummary:
        node_roots = self._collect_node_roots(layout.tree_dir)
        usage = UsageRecord()
        cost = CostRecord()
        role_names: set[str] = set()
        model_names: set[str] = set()
        run_count = 0
        completed_count = 0
        escalated_count = 0
        cancelled_count = 0
        failed_count = 0
        total_duration_seconds = 0.0
        saw_duration = False
        failure_reasons: Counter[str] = Counter()

        for node_root in node_roots:
            node = node_layout(node_root)
            status = read_trimmed_text(node.status_file)
            terminal_outcome = read_trimmed_text(node.terminal_outcome_file)
            failure_reason = read_trimmed_text(node.failure_reason_file)

            if status == "finished" and terminal_outcome == "completed":
                completed_count += 1
            if status == "finished" and terminal_outcome == "escalated":
                escalated_count += 1
            if status == "finished" and terminal_outcome == "cancelled":
                cancelled_count += 1
            if status == "failed":
                failed_count += 1
                if failure_reason:
                    failure_reasons[failure_reason] += 1

            if node.usage_summary_file.exists():
                usage_data = json.loads(node.usage_summary_file.read_text(encoding="utf-8"))
                usage = UsageRecord(
                    prompt_tokens=usage.prompt_tokens + usage_data.get("prompt_tokens", 0),
                    completion_tokens=usage.completion_tokens
                    + usage_data.get("completion_tokens", 0),
                    reasoning_tokens=usage.reasoning_tokens
                    + usage_data.get("reasoning_tokens", 0),
                    cached_prompt_tokens=usage.cached_prompt_tokens
                    + usage_data.get("cached_prompt_tokens", 0),
                    total_cost_usd=usage.total_cost_usd + usage_data.get("total_cost_usd", 0.0),
                )
                cost = CostRecord(direct_usd=usage.total_cost_usd)

            for run_dir in sorted(node.runs_dir.glob("run-*")):
                summary_file = run_dir / "summary.json"
                if not summary_file.exists():
                    continue
                run_count += 1
                summary_data = json.loads(summary_file.read_text(encoding="utf-8"))
                role = summary_data.get("role")
                model = summary_data.get("model")
                if role:
                    role_names.add(role)
                if model:
                    model_names.add(model)
                duration = summary_data.get("duration_seconds")
                if isinstance(duration, (int, float)):
                    total_duration_seconds += float(duration)
                    saw_duration = True

        return MissionSummary(
            mission_id=mission_id,
            root_node_id="root",
            final_status=root_result.final_status,
            terminal_outcome=root_result.terminal_outcome,
            failure_reason=root_result.failure_reason,
            node_count=len(node_roots),
            completed_node_count=completed_count,
            escalated_node_count=escalated_count,
            cancelled_node_count=cancelled_count,
            failed_node_count=failed_count,
            run_count=run_count,
            total_duration_seconds=total_duration_seconds if saw_duration else None,
            usage=usage,
            cost=cost,
            roles_used=tuple(sorted(role_names)),
            models_used=tuple(sorted(model_names)),
            top_failure_reasons=tuple(reason for reason, _ in failure_reasons.most_common()),
        )

    def _collect_node_roots(self, tree_dir: Path) -> list[Path]:
        status_files = sorted(tree_dir.rglob("for-orchestrator/this-nodes-current-status"))
        return [status_file.parents[1] for status_file in status_files]

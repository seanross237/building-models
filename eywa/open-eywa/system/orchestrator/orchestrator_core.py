from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from system.runtime.runtime_interface import RuntimeAdapter, RuntimeRequest, RuntimeResult

from .event_schema import EventRecord
from .event_writer import AppendOnlyJsonlWriter
from .node_contract import NodeLayout, node_layout, write_text
from .node_lifecycle import transition_node
from .node_preparation import prepare_node_context_packet
from .node_record import (
    AssignmentSource,
    node_next_role,
    node_status,
    node_waiting_on_computation_note,
    read_node_record,
    snapshot_node_record,
    update_node_record,
)
from .node_validator import validate_node
from .role_contracts import RoleContract, role_contract_for
from .summary_schema import RunSummary
from .usage_schema import CostRecord, UsageRecord


class OrchestratorCoreError(RuntimeError):
    """Raised when the rebuilt orchestrator core cannot safely advance a node."""


@dataclass(frozen=True)
class NodeRunStepResult:
    mission_id: str
    node_id: str
    node_path: str
    run_id: str
    role: str
    status_after: str
    terminal_outcome: str | None
    failure_reason: str | None
    artifacts_produced: tuple[str, ...]
    run_summary: RunSummary


class NodeOrchestratorCore:
    def __init__(self, runtime: RuntimeAdapter) -> None:
        self.runtime = runtime

    def run_once(
        self,
        node_path: str | Path,
        *,
        mission_id: str,
        node_id: str,
        role: str | None = None,
        model: str | None = None,
        variant: str | None = None,
        runtime_metadata: dict[str, Any] | None = None,
    ) -> NodeRunStepResult:
        layout = node_layout(node_path)
        self._assert_node_valid_before_run(layout)

        requested_role = role or node_next_role(layout)
        if not requested_role:
            raise OrchestratorCoreError("A node run requires an explicit role or next_role.")
        contract = role_contract_for(requested_role)
        resolved_model, resolved_model_source = self._resolve_model_assignment(
            requested_role,
            explicit_model=model,
        )
        resolved_variant = variant
        resolved_variant_source: AssignmentSource | None = "manual" if variant is not None else None

        status_before = node_status(layout)
        if status_before == "pending":
            transition_node(layout.root, next_status="active", expected_current_status="pending")
            self._emit_event(
                layout,
                EventRecord(
                    event_type="node_status_changed",
                    mission_id=mission_id,
                    node_id=node_id,
                    node_path=str(layout.root),
                    role=requested_role,
                    payload={"status_before": "pending", "status_after": "active"},
                ),
            )
        elif status_before != "active":
            raise OrchestratorCoreError(
                f"Node must be pending or active to run, found {status_before!r}."
            )

        self._persist_resolved_run_state(
            layout,
            next_role=requested_role,
            model=resolved_model,
            variant=resolved_variant,
            model_source=resolved_model_source,
            variant_source=resolved_variant_source,
        )

        run_id = self._next_run_id(layout)
        run_dir = layout.run_dir(run_id)
        run_dir.mkdir(parents=True, exist_ok=True)
        snapshot_node_record(layout, layout.run_node_record_file(run_id))

        prepared_context = prepare_node_context_packet(
            layout,
            run_id=run_id,
            role=requested_role,
        )

        from system.runtime.runtime_interface import RuntimeRequest

        request = RuntimeRequest(
            mission_id=mission_id,
            node_id=node_id,
            node_path=str(layout.root),
            run_id=run_id,
            role=requested_role,
            model=resolved_model,
            variant=resolved_variant,
            prepared_inputs=(prepared_context.packet_path,),
            metadata=dict(runtime_metadata or {}),
        )
        self._write_json(layout.run_request_file(run_id), self._request_to_dict(request))
        self._emit_event(
            layout,
            EventRecord(
                event_type="run_started",
                mission_id=mission_id,
                node_id=node_id,
                node_path=str(layout.root),
                run_id=run_id,
                role=requested_role,
                model=resolved_model,
                variant=resolved_variant,
            ),
        )

        result = self.runtime.run(request)
        self._persist_runtime_result_parameters(
            layout,
            next_role=requested_role,
            request=request,
            result=result,
            fallback_model_source=resolved_model_source,
            fallback_variant_source=resolved_variant_source,
        )
        self._write_json(layout.run_result_file(run_id), self._result_to_dict(result))
        self._write_json(layout.run_summary_file(run_id), result.to_run_summary().to_dict())
        self._write_json(layout.run_usage_file(run_id), result.usage.to_dict())

        self._apply_runtime_detail_updates(layout, result)

        self._emit_event(
            layout,
            EventRecord(
                event_type=self._run_finished_event_type(result.exit_reason),
                mission_id=mission_id,
                node_id=node_id,
                node_path=str(layout.root),
                run_id=run_id,
                role=requested_role,
                model=result.model or resolved_model,
                variant=result.variant or resolved_variant,
                payload={"exit_reason": result.exit_reason},
            ),
        )
        for artifact_path in result.artifacts_produced:
            self._emit_event(
                layout,
                EventRecord(
                    event_type="artifact_written",
                    mission_id=mission_id,
                    node_id=node_id,
                    node_path=str(layout.root),
                    run_id=run_id,
                    role=requested_role,
                    payload={"artifact_path": artifact_path},
                ),
            )
        self._emit_event(
            layout,
            EventRecord(
                event_type="usage_recorded",
                mission_id=mission_id,
                node_id=node_id,
                node_path=str(layout.root),
                run_id=run_id,
                role=requested_role,
                payload={"usage": result.usage.to_dict()},
            ),
        )
        self._emit_event(
            layout,
            EventRecord(
                event_type="cost_recorded",
                mission_id=mission_id,
                node_id=node_id,
                node_path=str(layout.root),
                run_id=run_id,
                role=requested_role,
                payload={"cost": {"direct_usd": result.usage.total_cost_usd}},
            ),
        )
        self._update_usage_summary(layout, result.usage)

        status_after, terminal_outcome, failure_reason = self._resolve_post_run_state(
            layout,
            mission_id=mission_id,
            node_id=node_id,
            role=requested_role,
            contract=contract,
            run_id=run_id,
            result=result,
        )

        self._assert_node_valid_after_run(layout, mission_id=mission_id, node_id=node_id)

        return NodeRunStepResult(
            mission_id=mission_id,
            node_id=node_id,
            node_path=str(layout.root),
            run_id=run_id,
            role=requested_role,
            status_after=status_after,
            terminal_outcome=terminal_outcome,
            failure_reason=failure_reason,
            artifacts_produced=result.artifacts_produced,
            run_summary=result.to_run_summary(),
        )

    def _persist_resolved_run_state(
        self,
        layout: NodeLayout,
        *,
        next_role: str,
        model: str | None,
        variant: str | None,
        model_source: AssignmentSource | None = None,
        variant_source: AssignmentSource | None = None,
    ) -> None:
        def updater(record: dict[str, Any]) -> None:
            control = record.setdefault("control", {})
            parameters = record.setdefault("parameters", {})
            resolved = parameters.setdefault("resolved", {})
            sources = parameters.setdefault("sources", {})
            control["next_role"] = next_role
            if model is not None:
                resolved["model"] = model
                sources["model"] = model_source
            if variant is not None:
                resolved["variant"] = variant
                sources["variant"] = variant_source

        update_node_record(layout, updater)

    def _resolve_model_assignment(
        self,
        role: str,
        *,
        explicit_model: str | None,
    ) -> tuple[str | None, AssignmentSource | None]:
        if explicit_model is not None:
            return explicit_model, "manual"

        config = getattr(self.runtime, "config", None)
        default_models = getattr(config, "default_models", None)
        if isinstance(default_models, dict):
            default_model = default_models.get(role)
            if isinstance(default_model, str) and default_model.strip():
                return default_model.strip(), "default"

        return None, None

    def _persist_runtime_result_parameters(
        self,
        layout: NodeLayout,
        *,
        next_role: str,
        request: RuntimeRequest,
        result: RuntimeResult,
        fallback_model_source: AssignmentSource | None,
        fallback_variant_source: AssignmentSource | None,
    ) -> None:
        model = result.model or request.model
        variant = result.variant or request.variant
        if model is None and variant is None:
            return

        self._persist_resolved_run_state(
            layout,
            next_role=next_role,
            model=model,
            variant=variant,
            model_source=fallback_model_source if model is not None else None,
            variant_source=fallback_variant_source if variant is not None else None,
        )

    def _apply_runtime_detail_updates(self, layout: NodeLayout, result: RuntimeResult) -> None:
        control_updates = dict(result.details.get("node_control_updates") or {})
        lifecycle_updates = dict(result.details.get("node_lifecycle_updates") or {})
        if not control_updates and not lifecycle_updates:
            return

        def updater(record: dict[str, Any]) -> None:
            control = record.setdefault("control", {})
            lifecycle = record.setdefault("lifecycle", {})
            if "next_action_after_child_report" in control_updates:
                control["next_action_after_child_report"] = control_updates[
                    "next_action_after_child_report"
                ]
            if "next_role" in control_updates:
                control["next_role"] = control_updates["next_role"]
            if "waiting_on_computation_note" in lifecycle_updates:
                lifecycle["waiting_on_computation_note"] = lifecycle_updates[
                    "waiting_on_computation_note"
                ]
            if "computation_result_note" in lifecycle_updates:
                lifecycle["computation_result_note"] = lifecycle_updates[
                    "computation_result_note"
                ]

        update_node_record(layout, updater)

    def _resolve_post_run_state(
        self,
        layout: NodeLayout,
        *,
        mission_id: str,
        node_id: str,
        role: str,
        contract: RoleContract,
        run_id: str,
        result: RuntimeResult,
    ) -> tuple[str, str | None, str | None]:
        if result.exit_reason != "completed":
            failure_reason = f"runtime_{result.exit_reason}"
            self._fail_node(layout, mission_id, node_id, role, run_id, failure_reason)
            return "failed", None, failure_reason

        if contract.allowed_waiting and node_waiting_on_computation_note(layout):
            transition_node(
                layout.root,
                next_status="waiting_on_computation",
                expected_current_status="active",
                waiting_note=node_waiting_on_computation_note(layout),
            )
            self._emit_status_change(
                layout,
                mission_id,
                node_id,
                role,
                "active",
                "waiting_on_computation",
            )
            return "waiting_on_computation", None, None

        if contract.allowed_escalation and layout.escalation_file.exists():
            transition_node(
                layout.root,
                next_status="finished",
                expected_current_status="active",
                terminal_outcome="escalated",
            )
            self._emit_status_change(layout, mission_id, node_id, role, "active", "finished")
            self._emit_event(
                layout,
                EventRecord(
                    event_type="node_escalated",
                    mission_id=mission_id,
                    node_id=node_id,
                    node_path=str(layout.root),
                    run_id=run_id,
                    role=role,
                    payload={"terminal_outcome": "escalated"},
                ),
            )
            return "finished", "escalated", None

        missing_artifacts = contract.missing_required_artifacts(layout)
        invalid_decision = contract.invalid_decision_value(layout)
        if missing_artifacts:
            failure_reason = "missing_required_artifact"
            self._fail_node(
                layout,
                mission_id,
                node_id,
                role,
                run_id,
                failure_reason,
                extra_payload={"missing_artifacts": missing_artifacts},
            )
            return "failed", None, failure_reason
        if invalid_decision is not None:
            failure_reason = "invalid_decision_value"
            self._fail_node(
                layout,
                mission_id,
                node_id,
                role,
                run_id,
                failure_reason,
                extra_payload={"decision_value": invalid_decision},
            )
            return "failed", None, failure_reason

        if contract.success_mode == "terminal":
            transition_node(
                layout.root,
                next_status="finished",
                expected_current_status="active",
                terminal_outcome="completed",
            )
            self._emit_status_change(layout, mission_id, node_id, role, "active", "finished")
            self._emit_event(
                layout,
                EventRecord(
                    event_type="node_completed",
                    mission_id=mission_id,
                    node_id=node_id,
                    node_path=str(layout.root),
                    run_id=run_id,
                    role=role,
                    payload={"terminal_outcome": "completed"},
                ),
            )
            return "finished", "completed", None

        self._emit_event(
            layout,
            EventRecord(
                event_type="node_validated",
                mission_id=mission_id,
                node_id=node_id,
                node_path=str(layout.root),
                run_id=run_id,
                role=role,
                payload={"artifacts_produced": result.artifacts_produced},
            ),
        )
        return "active", None, None

    def _fail_node(
        self,
        layout: NodeLayout,
        mission_id: str,
        node_id: str,
        role: str,
        run_id: str,
        failure_reason: str,
        extra_payload: dict[str, Any] | None = None,
    ) -> None:
        transition_node(
            layout.root,
            next_status="failed",
            expected_current_status="active",
            failure_reason=failure_reason,
        )
        self._emit_status_change(layout, mission_id, node_id, role, "active", "failed")
        payload = {"failure_reason": failure_reason, **dict(extra_payload or {})}
        self._emit_event(
            layout,
            EventRecord(
                event_type="node_failed",
                mission_id=mission_id,
                node_id=node_id,
                node_path=str(layout.root),
                run_id=run_id,
                role=role,
                payload=payload,
            ),
        )

    def _update_usage_summary(self, layout: NodeLayout, usage: UsageRecord) -> None:
        existing_data: dict[str, Any]
        if layout.usage_summary_file.exists():
            existing_data = json.loads(layout.usage_summary_file.read_text(encoding="utf-8"))
        else:
            existing_data = UsageRecord().to_dict()

        combined = UsageRecord(
            prompt_tokens=existing_data.get("prompt_tokens", 0) + usage.prompt_tokens,
            completion_tokens=existing_data.get("completion_tokens", 0) + usage.completion_tokens,
            reasoning_tokens=existing_data.get("reasoning_tokens", 0) + usage.reasoning_tokens,
            cached_prompt_tokens=existing_data.get("cached_prompt_tokens", 0)
            + usage.cached_prompt_tokens,
            total_cost_usd=existing_data.get("total_cost_usd", 0.0) + usage.total_cost_usd,
        )
        cost = CostRecord(direct_usd=combined.total_cost_usd)
        self._write_json(layout.usage_summary_file, combined.to_dict())
        self._write_json(layout.cost_summary_file, cost.to_dict())

    def _assert_node_valid_before_run(self, layout: NodeLayout) -> None:
        report = validate_node(layout.root)
        if not report.is_valid:
            raise OrchestratorCoreError(f"Node is invalid before run: {report.issues!r}")

    def _assert_node_valid_after_run(
        self,
        layout: NodeLayout,
        *,
        mission_id: str,
        node_id: str,
    ) -> None:
        report = validate_node(layout.root)
        if report.is_valid:
            return
        self._emit_event(
            layout,
            EventRecord(
                event_type="node_validation_failed",
                mission_id=mission_id,
                node_id=node_id,
                node_path=str(layout.root),
                payload={"issues": [issue.code for issue in report.issues]},
            ),
        )
        raise OrchestratorCoreError(f"Node is invalid after run: {report.issues!r}")

    def _next_run_id(self, layout: NodeLayout) -> str:
        existing_numbers: list[int] = []
        if layout.runs_dir.exists():
            for child in layout.runs_dir.iterdir():
                if child.is_dir() and child.name.startswith("run-"):
                    suffix = child.name.removeprefix("run-")
                    if suffix.isdigit():
                        existing_numbers.append(int(suffix))
        next_number = (max(existing_numbers) + 1) if existing_numbers else 1
        return f"run-{next_number:03d}"

    def _emit_status_change(
        self,
        layout: NodeLayout,
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

    def _emit_event(self, layout: NodeLayout, event: EventRecord) -> None:
        AppendOnlyJsonlWriter(layout.events_log_file).append_event(event)

    def _request_to_dict(self, request: RuntimeRequest) -> dict[str, Any]:
        return {
            "mission_id": request.mission_id,
            "node_id": request.node_id,
            "node_path": request.node_path,
            "run_id": request.run_id,
            "role": request.role,
            "model": request.model,
            "variant": request.variant,
            "prepared_inputs": list(request.prepared_inputs),
            "metadata": request.metadata,
        }

    def _result_to_dict(self, result: RuntimeResult) -> dict[str, Any]:
        return {
            "mission_id": result.mission_id,
            "node_id": result.node_id,
            "node_path": result.node_path,
            "run_id": result.run_id,
            "role": result.role,
            "exit_reason": result.exit_reason,
            "started_at_utc": result.started_at_utc,
            "finished_at_utc": result.finished_at_utc,
            "duration_seconds": result.duration_seconds,
            "model": result.model,
            "variant": result.variant,
            "artifacts_produced": list(result.artifacts_produced),
            "tool_call_count": result.tool_call_count,
            "usage": result.usage.to_dict(),
            "details": result.details,
        }

    def _write_json(self, path: Path, data: dict[str, Any]) -> None:
        write_text(path, json.dumps(data, sort_keys=True, indent=2) + "\n")

    def _run_finished_event_type(self, exit_reason: str) -> str:
        if exit_reason == "completed":
            return "run_finished"
        if exit_reason == "timed_out":
            return "run_timed_out"
        return "run_failed"

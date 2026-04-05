from __future__ import annotations

from pathlib import Path
from time import perf_counter

from system.orchestrator import AppendOnlyJsonlWriter
from system.orchestrator.event_schema import EventRecord, utc_now_iso
from system.orchestrator.node_contract import node_layout
from system.tools import FileToolExecutor, ToolExecutionError
from .runtime_interface import RuntimeRequest, RuntimeResult
from .simulation_scenarios import ScenarioAction, SimulatedScenario


class SimulatedRuntimeError(RuntimeError):
    """Raised when the simulated runtime cannot safely execute a scenario."""


class SimulatedRuntime:
    def __init__(
        self,
        scenarios: dict[str, SimulatedScenario],
        *,
        file_tools: FileToolExecutor | None = None,
    ) -> None:
        self.scenarios = dict(scenarios)
        self.file_tools = file_tools or FileToolExecutor()

    def run(self, request: RuntimeRequest) -> RuntimeResult:
        scenario = self._resolve_scenario(request)
        layout = node_layout(request.node_root)
        started_at = utc_now_iso()
        start_clock = perf_counter()
        artifacts_produced: list[str] = []
        tool_results: list[dict[str, object]] = []
        tool_call_count = 0

        try:
            for action in scenario.actions:
                action_artifacts, used_tool, tool_output = self._apply_action(request, action)
                artifacts_produced.extend(action_artifacts)
                if used_tool:
                    tool_call_count += 1
                    if tool_output is not None:
                        tool_results.append(tool_output)
        except ToolExecutionError as exc:
            self._emit_tool_failed_event(request, action, str(exc))
            finished_at = utc_now_iso()
            duration_seconds = perf_counter() - start_clock
            return RuntimeResult(
                mission_id=request.mission_id,
                node_id=request.node_id,
                node_path=request.node_path,
                run_id=request.run_id,
                role=request.role,
                model=request.model,
                variant=request.variant,
                exit_reason="failed",
                started_at_utc=started_at,
                finished_at_utc=finished_at,
                duration_seconds=duration_seconds,
                artifacts_produced=tuple(artifacts_produced),
                tool_call_count=tool_call_count,
                usage=scenario.usage,
                details={
                    "scenario_name": scenario.name,
                    "prepared_inputs": list(request.prepared_inputs),
                    "tool_results": tool_results,
                    "tool_error": str(exc),
                    **scenario.details,
                },
            )

        finished_at = utc_now_iso()
        duration_seconds = perf_counter() - start_clock

        details = {
            "scenario_name": scenario.name,
            "prepared_inputs": list(request.prepared_inputs),
            "tool_results": tool_results,
            **scenario.details,
        }
        return RuntimeResult(
            mission_id=request.mission_id,
            node_id=request.node_id,
            node_path=request.node_path,
            run_id=request.run_id,
            role=request.role,
            model=request.model,
            variant=request.variant,
            exit_reason=scenario.exit_reason,
            started_at_utc=started_at,
            finished_at_utc=finished_at,
            duration_seconds=duration_seconds,
            artifacts_produced=tuple(artifacts_produced),
            tool_call_count=tool_call_count,
            usage=scenario.usage,
            details=details,
        )

    def _resolve_scenario(self, request: RuntimeRequest) -> SimulatedScenario:
        scenario_name = request.metadata.get("scenario_name")
        if isinstance(scenario_name, str) and scenario_name in self.scenarios:
            return self.scenarios[scenario_name]
        if len(self.scenarios) == 1:
            return next(iter(self.scenarios.values()))
        raise SimulatedRuntimeError(
            "Simulated runtime could not determine which scenario to run."
        )

    def _apply_action(
        self,
        request: RuntimeRequest,
        action: ScenarioAction,
    ) -> tuple[list[str], bool, dict[str, object] | None]:
        action_type = action.type
        if action_type == "noop":
            return [], False, None

        if action_type == "call_tool":
            return self._call_tool(request, action)

        resolved_path = self._resolve_node_relative_path(request.node_root, action.path or "")
        relative_path = str(resolved_path.relative_to(request.node_root))

        if action_type == "write_text":
            resolved_path.parent.mkdir(parents=True, exist_ok=True)
            resolved_path.write_text(action.content or "", encoding="utf-8")
            return [relative_path], False, None
        if action_type == "touch_file":
            resolved_path.parent.mkdir(parents=True, exist_ok=True)
            resolved_path.touch()
            return [relative_path], False, None
        if action_type == "delete_file":
            if resolved_path.exists():
                resolved_path.unlink()
            return [relative_path], False, None

        raise SimulatedRuntimeError(f"Unsupported simulated action type: {action_type!r}.")

    def _call_tool(
        self,
        request: RuntimeRequest,
        action: ScenarioAction,
    ) -> tuple[list[str], bool, dict[str, object]]:
        tool_name = action.tool_name or ""
        arguments = dict(action.arguments or {})
        self._emit_tool_called_event(request, tool_name, arguments)
        result = self.file_tools.execute(request.node_root, tool_name, arguments)
        self._emit_tool_finished_event(request, tool_name, result.output)
        return (
            list(result.artifact_paths),
            True,
            {
                "tool_name": tool_name,
                "arguments": arguments,
                "output": result.output,
                "artifact_paths": list(result.artifact_paths),
            },
        )

    def _resolve_node_relative_path(self, node_root: Path, relative_path: str) -> Path:
        if not relative_path.strip():
            raise SimulatedRuntimeError("Scenario action paths must be non-empty.")
        candidate = (node_root / relative_path).resolve()
        try:
            candidate.relative_to(node_root)
        except ValueError as exc:
            raise SimulatedRuntimeError(
                f"Scenario attempted to write outside the node boundary: {relative_path!r}."
            ) from exc
        return candidate

    def _emit_tool_called_event(
        self,
        request: RuntimeRequest,
        tool_name: str,
        arguments: dict[str, object],
    ) -> None:
        AppendOnlyJsonlWriter(node_layout(request.node_root).events_log_file).append_event(
            EventRecord(
                event_type="tool_called",
                mission_id=request.mission_id,
                node_id=request.node_id,
                node_path=request.node_path,
                run_id=request.run_id,
                role=request.role,
                model=request.model,
                variant=request.variant,
                payload={"tool_name": tool_name, "arguments": arguments},
            )
        )

    def _emit_tool_finished_event(
        self,
        request: RuntimeRequest,
        tool_name: str,
        output: dict[str, object],
    ) -> None:
        AppendOnlyJsonlWriter(node_layout(request.node_root).events_log_file).append_event(
            EventRecord(
                event_type="tool_finished",
                mission_id=request.mission_id,
                node_id=request.node_id,
                node_path=request.node_path,
                run_id=request.run_id,
                role=request.role,
                model=request.model,
                variant=request.variant,
                payload={"tool_name": tool_name, "output": output},
            )
        )

    def _emit_tool_failed_event(
        self,
        request: RuntimeRequest,
        action: ScenarioAction,
        error_message: str,
    ) -> None:
        tool_name = action.tool_name or "<unknown>"
        AppendOnlyJsonlWriter(node_layout(request.node_root).events_log_file).append_event(
            EventRecord(
                event_type="tool_failed",
                mission_id=request.mission_id,
                node_id=request.node_id,
                node_path=request.node_path,
                run_id=request.run_id,
                role=request.role,
                model=request.model,
                variant=request.variant,
                payload={
                    "tool_name": tool_name,
                    "arguments": dict(action.arguments or {}),
                    "error": error_message,
                },
            )
        )

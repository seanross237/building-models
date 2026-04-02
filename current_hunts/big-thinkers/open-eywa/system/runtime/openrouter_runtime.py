from __future__ import annotations

from dataclasses import dataclass, replace
import json
import os
from pathlib import Path
from time import perf_counter
from typing import Any

from system.orchestrator.event_schema import EventRecord, utc_now_iso
from system.orchestrator.event_writer import AppendOnlyJsonlWriter
from system.orchestrator.node_contract import node_layout
from system.orchestrator.role_contracts import role_contract_for
from system.orchestrator.usage_schema import UsageRecord
from system.tools import FileToolExecutor, ToolExecutionError

from .openrouter_client import (
    OpenRouterChatClient,
    OpenRouterClientConfig,
    OpenRouterClientError,
)
from .prompt_loader import PromptBundle, PromptLoader, PromptLoaderError
from .runtime_interface import RuntimeRequest, RuntimeResult

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class OpenRouterRuntimeError(RuntimeError):
    """Raised when the OpenRouter-backed runtime cannot safely complete a run."""


@dataclass(frozen=True)
class OpenRouterRuntimeConfig:
    api_key: str
    default_models: dict[str, str]
    base_url: str = "https://openrouter.ai/api/v1"
    referer_url: str | None = None
    title: str | None = "Open-Eywa"
    max_turns: int = 6
    max_tokens: int = 1600
    temperature: float = 0.0
    fetch_generation_stats: bool = True

    @classmethod
    def from_environment(
        cls,
        *,
        default_models: dict[str, str],
        base_url: str = "https://openrouter.ai/api/v1",
        dotenv_path: str | Path | None = None,
        referer_url: str | None = None,
        title: str | None = "Open-Eywa",
        max_turns: int = 6,
        max_tokens: int = 1600,
        temperature: float = 0.0,
        fetch_generation_stats: bool = True,
    ) -> "OpenRouterRuntimeConfig":
        api_key = os.environ.get("OPENROUTER_API_KEY", "").strip()
        if not api_key:
            api_key = _load_env_file_value("OPENROUTER_API_KEY", dotenv_path=dotenv_path).strip()
        if not api_key:
            raise OpenRouterRuntimeError("OPENROUTER_API_KEY is not set in the environment or repo .env file.")
        return cls(
            api_key=api_key,
            default_models=dict(default_models),
            base_url=base_url,
            referer_url=referer_url,
            title=title,
            max_turns=max_turns,
            max_tokens=max_tokens,
            temperature=temperature,
            fetch_generation_stats=fetch_generation_stats,
        )


def _load_env_file_value(
    name: str,
    *,
    dotenv_path: str | Path | None = None,
) -> str:
    path = Path(dotenv_path).expanduser().resolve() if dotenv_path else PROJECT_ROOT / ".env"
    if not path.exists():
        return ""

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key.strip() != name:
            continue
        cleaned = value.strip()
        if len(cleaned) >= 2 and cleaned[0] == cleaned[-1] and cleaned[0] in {'"', "'"}:
            return cleaned[1:-1]
        return cleaned
    return ""


class OpenRouterRuntime:
    def __init__(
        self,
        config: OpenRouterRuntimeConfig,
        *,
        client: OpenRouterChatClient | None = None,
        prompt_loader: PromptLoader | None = None,
        file_tools: FileToolExecutor | None = None,
    ) -> None:
        self.config = config
        self.client = client or OpenRouterChatClient(
            OpenRouterClientConfig(
                api_key=config.api_key,
                base_url=config.base_url,
                referer_url=config.referer_url,
                title=config.title,
            )
        )
        self.prompt_loader = prompt_loader or PromptLoader()
        self.file_tools = file_tools or FileToolExecutor()

    def run(self, request: RuntimeRequest) -> RuntimeResult:
        model = request.model or self.config.default_models.get(request.role)
        if not model:
            raise OpenRouterRuntimeError(
                f"No model was provided and no default model is configured for role {request.role!r}."
            )

        try:
            prompt_bundle = self.prompt_loader.load(request.role)
        except PromptLoaderError as exc:
            raise OpenRouterRuntimeError(str(exc)) from exc

        started_at = utc_now_iso()
        start_clock = perf_counter()
        messages = self._build_initial_messages(request, prompt_bundle)
        artifacts_produced: list[str] = []
        tool_call_count = 0
        assistant_messages: list[str] = []
        response_ids: list[str] = []
        usage = UsageRecord()

        for _turn in range(1, self.config.max_turns + 1):
            try:
                response = self.client.create_chat_completion(
                    model=model,
                    messages=messages,
                    tools=self._tool_schemas(),
                    tool_choice="auto",
                    max_tokens=self.config.max_tokens,
                    temperature=self.config.temperature,
                )
            except OpenRouterClientError as exc:
                return self._failed_result(
                    request,
                    model=model,
                    started_at=started_at,
                    start_clock=start_clock,
                    usage=usage,
                    artifacts_produced=artifacts_produced,
                    tool_call_count=tool_call_count,
                    details={
                        "error": str(exc),
                        "prompt_bundle_paths": list(prompt_bundle.source_paths),
                        "prepared_inputs": list(request.prepared_inputs),
                    },
                )

            response_id = response.get("id")
            if isinstance(response_id, str) and response_id.strip():
                response_ids.append(response_id)
            usage = self._merge_usage(
                usage,
                self._usage_from_response(response, response_id=response_id),
            )
            if self.config.fetch_generation_stats and isinstance(response_id, str) and response_id.strip():
                usage = self._merge_usage(usage, self._usage_from_generation_stats(response_id))

            choice = response["choices"][0]
            message = dict(choice.get("message") or {})
            tool_calls = list(message.get("tool_calls") or [])
            assistant_content = self._normalize_message_content(message.get("content"))
            if assistant_content:
                assistant_messages.append(assistant_content)

            assistant_message: dict[str, Any] = {"role": "assistant"}
            if assistant_content:
                assistant_message["content"] = assistant_content
            if tool_calls:
                assistant_message["tool_calls"] = tool_calls
            messages.append(assistant_message)

            if tool_calls:
                for tool_call in tool_calls:
                    try:
                        execution = self._execute_tool_call(request, tool_call, model=model)
                    except OpenRouterRuntimeError as exc:
                        return self._failed_result(
                            request,
                            model=model,
                            started_at=started_at,
                            start_clock=start_clock,
                            usage=usage,
                            artifacts_produced=artifacts_produced,
                            tool_call_count=tool_call_count,
                            details={
                                "error": str(exc),
                                "response_ids": response_ids,
                                "assistant_messages": assistant_messages,
                                "prompt_bundle_paths": list(prompt_bundle.source_paths),
                                "prepared_inputs": list(request.prepared_inputs),
                            },
                        )
                    tool_call_count += 1
                    artifacts_produced.extend(execution["artifact_paths"])
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": execution["tool_call_id"],
                            "content": json.dumps(execution["tool_output"], sort_keys=True),
                        }
                    )
                continue

            finish_reason = choice.get("finish_reason")
            exit_reason = self._map_finish_reason_to_exit_reason(finish_reason)
            node_updates = self._extract_node_updates(assistant_content)
            materialized_artifact = self._maybe_materialize_required_artifact(
                request,
                role=request.role,
                assistant_content=assistant_content,
                model=model,
            )
            if materialized_artifact is not None:
                artifacts_produced.append(materialized_artifact)
            return RuntimeResult(
                mission_id=request.mission_id,
                node_id=request.node_id,
                node_path=request.node_path,
                run_id=request.run_id,
                role=request.role,
                model=model,
                variant=request.variant,
                exit_reason=exit_reason,
                started_at_utc=started_at,
                finished_at_utc=utc_now_iso(),
                duration_seconds=perf_counter() - start_clock,
                artifacts_produced=tuple(dict.fromkeys(artifacts_produced)),
                tool_call_count=tool_call_count,
                usage=usage,
                details={
                    "response_ids": response_ids,
                    "assistant_messages": assistant_messages,
                    "prompt_bundle_paths": list(prompt_bundle.source_paths),
                    "prepared_inputs": list(request.prepared_inputs),
                    "finish_reason": finish_reason,
                    **(
                        {"assistant_content_materialized_to": materialized_artifact}
                        if materialized_artifact is not None
                        else {}
                    ),
                    **node_updates,
                },
            )

        return RuntimeResult(
            mission_id=request.mission_id,
            node_id=request.node_id,
            node_path=request.node_path,
            run_id=request.run_id,
            role=request.role,
            model=model,
            variant=request.variant,
            exit_reason="no_progress",
            started_at_utc=started_at,
            finished_at_utc=utc_now_iso(),
            duration_seconds=perf_counter() - start_clock,
            artifacts_produced=tuple(dict.fromkeys(artifacts_produced)),
            tool_call_count=tool_call_count,
            usage=usage,
            details={
                "response_ids": response_ids,
                "assistant_messages": assistant_messages,
                "prompt_bundle_paths": list(prompt_bundle.source_paths),
                "prepared_inputs": list(request.prepared_inputs),
                "reason": "max_turns_exceeded",
            },
        )

    def _build_initial_messages(
        self,
        request: RuntimeRequest,
        prompt_bundle: PromptBundle,
    ) -> list[dict[str, Any]]:
        prepared_packets = [self._load_prepared_packet(path) for path in request.prepared_inputs]
        support_docs_text = "\n\n".join(
            f"## Supporting Doc: {relative_path}\n\n{content.strip()}"
            for relative_path, content in prompt_bundle.support_documents
        ).strip()
        runtime_note = (
            "Runtime note: only these tools are currently enabled in this live runtime: "
            "read_file, write_file, edit_file, glob, grep. "
            "Do not assume shell, Python, Sage, Lean, or background-job tools are available here."
        )

        system_prompt = prompt_bundle.system_prompt.strip()
        if support_docs_text:
            system_prompt = f"{system_prompt}\n\n{support_docs_text}"
        system_prompt = f"{system_prompt}\n\n{runtime_note}"

        return [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": self._build_user_message(request, prepared_packets, prompt_bundle),
            },
        ]

    def _build_user_message(
        self,
        request: RuntimeRequest,
        prepared_packets: list[dict[str, Any]],
        prompt_bundle: PromptBundle,
    ) -> str:
        packet_text = json.dumps(prepared_packets, indent=2, sort_keys=True)
        contract = role_contract_for(request.role)
        required_artifacts = ", ".join(contract.required_artifacts) or "none"
        return (
            f"You are running one Open-Eywa node.\n\n"
            f"Role: {request.role}\n"
            f"Node root: {request.node_path}\n"
            f"Run id: {request.run_id}\n"
            f"Prompt bundle files: {', '.join(prompt_bundle.source_paths)}\n\n"
            f"Role contract required artifacts: {required_artifacts}\n"
            f"These exact artifact paths are enforced by code.\n"
            f"If the task or any context mentions a different output filename, still write the required artifact path for your role.\n"
            f"You may write additional files only if they help, but they do not replace the required artifacts.\n\n"
            f"Your job is to use the available file tools to read what you need and write the required artifacts for your role.\n"
            f"If the task is impossible under the node's assumptions, write output/escalation.md.\n"
            f"Do not write outside the node boundary.\n\n"
            f"Prepared context packet(s):\n{packet_text}\n"
        )

    def _load_prepared_packet(self, path: str) -> dict[str, Any]:
        packet_path = Path(path).expanduser().resolve()
        if not packet_path.exists():
            raise OpenRouterRuntimeError(
                f"Prepared input packet does not exist: {packet_path!s}."
            )
        try:
            return json.loads(packet_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise OpenRouterRuntimeError(
                f"Prepared input packet is not valid JSON: {packet_path!s}."
            ) from exc

    def _usage_from_response(
        self,
        response: dict[str, Any],
        *,
        response_id: str | None,
    ) -> UsageRecord:
        usage_data = dict(response.get("usage") or {})
        prompt_details = dict(usage_data.get("prompt_tokens_details") or {})
        completion_details = dict(usage_data.get("completion_tokens_details") or {})
        return UsageRecord(
            prompt_tokens=int(usage_data.get("prompt_tokens", 0) or 0),
            completion_tokens=int(usage_data.get("completion_tokens", 0) or 0),
            total_tokens=int(usage_data.get("total_tokens", 0) or 0) or None,
            cached_prompt_tokens=int(prompt_details.get("cached_tokens", 0) or 0),
            reasoning_tokens=int(completion_details.get("reasoning_tokens", 0) or 0),
            total_cost_usd=float(usage_data.get("cost", 0.0) or 0.0),
            provider_details={
                "response_id": response_id,
                "model": response.get("model"),
                "usage_from": "chat_completions",
                "response_cost_usd": float(usage_data.get("cost", 0.0) or 0.0),
            },
        )

    def _extract_node_updates(self, assistant_content: str | None) -> dict[str, Any]:
        if not assistant_content:
            return {}

        control_updates: dict[str, Any] = {}
        lifecycle_updates: dict[str, Any] = {}
        for raw_line in assistant_content.splitlines():
            line = raw_line.strip()
            if not line:
                continue
            if line.startswith("NEXT_ACTION_AFTER_CHILD_REPORT:"):
                control_updates["next_action_after_child_report"] = (
                    line.split(":", 1)[1].strip().lower()
                )
            if line.startswith("WAITING_ON_COMPUTATION:"):
                lifecycle_updates["waiting_on_computation_note"] = (
                    line.split(":", 1)[1].strip()
                )

        details: dict[str, Any] = {}
        if control_updates:
            details["node_control_updates"] = control_updates
        if lifecycle_updates:
            details["node_lifecycle_updates"] = lifecycle_updates
        return details

    def _usage_from_generation_stats(self, response_id: str) -> UsageRecord:
        try:
            generation = self.client.get_generation_stats(response_id)
        except OpenRouterClientError:
            return UsageRecord()

        data = dict(generation.get("data") or {})
        tokens_prompt = int(data.get("tokens_prompt", 0) or 0)
        tokens_completion = int(data.get("tokens_completion", 0) or 0)
        total_tokens = int(data.get("native_tokens_prompt", 0) or 0) + int(
            data.get("native_tokens_completion", 0) or 0
        )
        if not total_tokens:
            total_tokens = tokens_prompt + tokens_completion
        return UsageRecord(
            prompt_tokens=tokens_prompt,
            completion_tokens=tokens_completion,
            total_tokens=total_tokens or None,
            total_cost_usd=float(data.get("total_cost", 0.0) or 0.0),
            provider_details={
                "response_id": response_id,
                "provider_name": data.get("provider_name"),
                "latency_ms": data.get("latency"),
                "usage_from": "generation_stats",
            },
        )

    def _merge_usage(self, current: UsageRecord, update: UsageRecord) -> UsageRecord:
        provider_details = dict(current.provider_details)
        if update.provider_details:
            response_id = update.provider_details.get("response_id")
            if response_id:
                provider_details.setdefault("responses", []).append(update.provider_details)
            else:
                provider_details.update(update.provider_details)
        total_tokens = None
        if current.total_tokens is not None or update.total_tokens is not None:
            total_tokens = int(current.total_tokens or 0) + int(update.total_tokens or 0)
        return UsageRecord(
            prompt_tokens=current.prompt_tokens + update.prompt_tokens,
            completion_tokens=current.completion_tokens + update.completion_tokens,
            reasoning_tokens=current.reasoning_tokens + update.reasoning_tokens,
            cached_prompt_tokens=current.cached_prompt_tokens + update.cached_prompt_tokens,
            total_tokens=total_tokens,
            total_cost_usd=current.total_cost_usd + update.total_cost_usd,
            provider_details=provider_details,
        )

    def _map_finish_reason_to_exit_reason(self, finish_reason: Any) -> str:
        if finish_reason in (None, "stop"):
            return "completed"
        if finish_reason == "length":
            return "timed_out"
        if finish_reason == "error":
            return "failed"
        if finish_reason == "content_filter":
            return "failed"
        if finish_reason == "tool_calls":
            return "no_progress"
        return "completed"

    def _execute_tool_call(
        self,
        request: RuntimeRequest,
        tool_call: dict[str, Any],
        *,
        model: str,
    ) -> dict[str, Any]:
        tool_call_id = str(tool_call.get("id") or "")
        function_block = dict(tool_call.get("function") or {})
        tool_name = str(function_block.get("name") or "")
        arguments_text = function_block.get("arguments")
        if not tool_name:
            raise OpenRouterRuntimeError("Tool call is missing function name.")
        if not isinstance(arguments_text, str):
            raise OpenRouterRuntimeError("Tool call arguments must be a JSON string.")
        try:
            arguments = json.loads(arguments_text)
        except json.JSONDecodeError as exc:
            raise OpenRouterRuntimeError(
                f"Tool call arguments for {tool_name!r} are not valid JSON."
            ) from exc
        if not isinstance(arguments, dict):
            raise OpenRouterRuntimeError("Tool call arguments must decode to an object.")

        self._emit_tool_event(
            request,
            event_type="tool_called",
            model=model,
            payload={"tool_name": tool_name, "arguments": arguments},
        )
        try:
            result = self.file_tools.execute(request.node_root, tool_name, arguments)
        except ToolExecutionError as exc:
            self._emit_tool_event(
                request,
                event_type="tool_failed",
                model=model,
                payload={"tool_name": tool_name, "arguments": arguments, "error": str(exc)},
            )
            raise OpenRouterRuntimeError(str(exc)) from exc

        self._emit_tool_event(
            request,
            event_type="tool_finished",
            model=model,
            payload={"tool_name": tool_name, "output": result.output},
        )
        return {
            "tool_call_id": tool_call_id,
            "tool_name": tool_name,
            "tool_output": result.output,
            "artifact_paths": list(result.artifact_paths),
        }

    def _maybe_materialize_required_artifact(
        self,
        request: RuntimeRequest,
        *,
        role: str,
        assistant_content: str | None,
        model: str,
    ) -> str | None:
        text = (assistant_content or "").strip()
        if not text:
            return None

        contract = role_contract_for(role)
        if len(contract.required_artifacts) != 1:
            return None

        relative_path = contract.required_artifacts[0]
        artifact_path = request.node_root / relative_path
        if artifact_path.exists():
            return None

        artifact_path.parent.mkdir(parents=True, exist_ok=True)
        artifact_path.write_text(text + "\n", encoding="utf-8")
        self._emit_event(
            request,
            event_type="artifact_written",
            model=model,
            payload={"artifact_path": relative_path},
        )
        return relative_path

    def _emit_tool_event(
        self,
        request: RuntimeRequest,
        *,
        event_type: str,
        model: str,
        payload: dict[str, Any],
    ) -> None:
        AppendOnlyJsonlWriter(node_layout(request.node_root).events_log_file).append_event(
            EventRecord(
                event_type=event_type,  # type: ignore[arg-type]
                mission_id=request.mission_id,
                node_id=request.node_id,
                node_path=request.node_path,
                run_id=request.run_id,
                role=request.role,
                model=model,
                variant=request.variant,
                payload=payload,
            )
        )

    def _emit_event(
        self,
        request: RuntimeRequest,
        *,
        event_type: str,
        model: str,
        payload: dict[str, Any],
    ) -> None:
        AppendOnlyJsonlWriter(node_layout(request.node_root).events_log_file).append_event(
            EventRecord(
                event_type=event_type,  # type: ignore[arg-type]
                mission_id=request.mission_id,
                node_id=request.node_id,
                node_path=request.node_path,
                run_id=request.run_id,
                role=request.role,
                model=model,
                variant=request.variant,
                payload=payload,
            )
        )

    def _failed_result(
        self,
        request: RuntimeRequest,
        *,
        model: str,
        started_at: str,
        start_clock: float,
        usage: UsageRecord,
        artifacts_produced: list[str],
        tool_call_count: int,
        details: dict[str, Any],
    ) -> RuntimeResult:
        return RuntimeResult(
            mission_id=request.mission_id,
            node_id=request.node_id,
            node_path=request.node_path,
            run_id=request.run_id,
            role=request.role,
            model=model,
            variant=request.variant,
            exit_reason="failed",
            started_at_utc=started_at,
            finished_at_utc=utc_now_iso(),
            duration_seconds=perf_counter() - start_clock,
            artifacts_produced=tuple(dict.fromkeys(artifacts_produced)),
            tool_call_count=tool_call_count,
            usage=usage,
            details=details,
        )

    def _normalize_message_content(self, content: Any) -> str:
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            parts: list[str] = []
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    text = item.get("text")
                    if isinstance(text, str):
                        parts.append(text)
            return "\n".join(part for part in parts if part.strip())
        return ""

    def _tool_schemas(self) -> list[dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "read_file",
                    "description": "Read a file inside the current node directory.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string"},
                        },
                        "required": ["path"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "write_file",
                    "description": "Write a file inside the current node directory.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string"},
                            "content": {"type": "string"},
                        },
                        "required": ["path", "content"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "edit_file",
                    "description": "Replace text inside a file in the current node directory.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string"},
                            "find_text": {"type": "string"},
                            "replace_text": {"type": "string"},
                            "replace_all": {"type": "boolean"},
                        },
                        "required": ["path", "find_text", "replace_text"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "glob",
                    "description": "List files inside the current node directory by glob pattern.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "pattern": {"type": "string"},
                            "include_directories": {"type": "boolean"},
                        },
                        "required": ["pattern"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "grep",
                    "description": "Search file contents inside the current node directory.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "pattern": {"type": "string"},
                            "start_path": {"type": "string"},
                            "case_sensitive": {"type": "boolean"},
                        },
                        "required": ["pattern"],
                    },
                },
            },
        ]

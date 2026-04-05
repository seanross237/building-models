"""Deterministic and live executors for Super-Eywa v1."""

from __future__ import annotations

from dataclasses import dataclass
import json
import re
from typing import Any, Dict, Iterable, List

from .authored_response import AuthoredResponseError, parse_authored_response_text, validate_authored_response
from .openrouter_client import OpenRouterChatClient, OpenRouterClientConfig, OpenRouterClientError
from .prompting import build_turn_prompt
from .secrets import load_openrouter_api_key


@dataclass
class ExecutionStep:
    """One authored response turn from an executor."""

    authored_response: Dict[str, Any]
    note: str
    prompt_snapshot: str
    provider_payload: Dict[str, Any] | None = None
    usage: Dict[str, Any] | None = None


class DeterministicLocalExecutor:
    """A minimal local executor that keeps v1 runnable without external model keys."""

    provider_name = "deterministic-local-v1"

    def author_node_response(
        self,
        *,
        node_packet: Dict[str, Any],
        depth: int,
        turn_index: int,
        allowed_decisions: Iterable[str],
        child_summaries: List[Dict[str, str]] | None = None,
        synthesis_brief: str | None = None,
    ) -> ExecutionStep:
        prompt_bundle = build_turn_prompt(
            node_packet,
            allowed_decisions=allowed_decisions,
            turn_index=turn_index,
            depth=depth,
            child_results=child_summaries,
            synthesis_brief=synthesis_brief,
        )
        max_helpers = int(
            node_packet["variable_resolution"]["resolved_variables"]
            .get("budget_policy", {})
            .get("max_helpers_per_node", 3)
        )
        authored_response = self._build_deterministic_response(
            instructions=str(node_packet["input"]["instructions"]),
            child_summaries=child_summaries,
            allowed_decisions=allowed_decisions,
            max_helpers=max_helpers,
        )
        validated = validate_authored_response(
            authored_response,
            allowed_decisions=allowed_decisions,
            max_helpers=max_helpers,
        )
        note = self._note_for_decision(validated["orchestration_decision"], bool(child_summaries))
        rendered_response = json.dumps(validated, indent=2)
        return ExecutionStep(
            authored_response=validated,
            note=note,
            prompt_snapshot=prompt_bundle["snapshot_text"],
            provider_payload={
                "provider": self.provider_name,
                "request": {
                    "system_prompt": prompt_bundle["system_prompt"],
                    "user_prompt": prompt_bundle["user_prompt"],
                },
                "response": {
                    "content": rendered_response,
                },
                "parsed_response": validated,
            },
            usage=self._zero_usage(),
        )

    def _build_deterministic_response(
        self,
        *,
        instructions: str,
        child_summaries: List[Dict[str, str]] | None,
        allowed_decisions: Iterable[str],
        max_helpers: int,
    ) -> Dict[str, Any]:
        allowed = set(allowed_decisions)
        lowered = instructions.lower()

        if "report_problem" in allowed and ("impossible" in lowered or "unachievable" in lowered):
            return {
                "schema_name": "eywa_node_response",
                "schema_version": "v1",
                "orchestration_decision": "report_problem",
                "decision_notes": "The instructions explicitly describe an impossible or unachievable case.",
                "response": f"Deterministic runtime marked this task as a problem case: {instructions}",
            }

        if child_summaries:
            return {
                "schema_name": "eywa_node_response",
                "schema_version": "v1",
                "orchestration_decision": "execute_locally",
                "decision_notes": "Child results are available, so the parent can synthesize locally.",
                "response": self._synthesized_local_response(instructions, child_summaries),
                "result_type": "summary",
            }

        if "delegate" in allowed:
            subtasks = self._split_instructions(instructions, max_helpers)
            if subtasks:
                return {
                    "schema_name": "eywa_node_response",
                    "schema_version": "v1",
                    "orchestration_decision": "delegate",
                    "decision_notes": "The instructions separate cleanly into helper-sized subtasks.",
                    "helpers": [
                        {
                            "label": f"helper_{index + 1:02d}",
                            "instructions": subtask,
                            "variable_overrides": {},
                        }
                        for index, subtask in enumerate(subtasks)
                    ],
                    "synthesis_brief": "Combine the helper results into one concise final response.",
                }

        return {
            "schema_name": "eywa_node_response",
            "schema_version": "v1",
            "orchestration_decision": "execute_locally",
            "decision_notes": "The task is narrow enough to complete in one local step.",
            "response": self._local_response(instructions),
            "result_type": "summary",
        }

    def _local_response(self, instructions: str) -> str:
        if "FINAL_ANSWER:" in instructions:
            return (
                "FINAL_ANSWER: deterministic-placeholder\n"
                "JUSTIFICATION: This is a deterministic local scaffold result."
            )
        return (
            f"Completed local deterministic work for: {instructions}\n"
            "This is a v1 scaffold result produced without a live model provider."
        )

    def _synthesized_local_response(self, instructions: str, child_summaries: List[Dict[str, str]]) -> str:
        lines = [
            f"Completed synthesized work for: {instructions}",
            "Combined child results:",
        ]
        for item in child_summaries:
            lines.append(f"- {item['node_id']}: {item['summary']}")
        return "\n".join(lines)

    def _split_instructions(self, instructions: str, max_helpers: int) -> List[str]:
        splitter_patterns = [
            r"\sand\s",
            r";",
            r"\b[Tt]hen\b",
            r"\n-\s+",
            r"\n\d+\.\s+",
        ]
        for pattern in splitter_patterns:
            pieces = [piece.strip(" .\n\t-") for piece in re.split(pattern, instructions) if piece.strip(" .\n\t-")]
            if len(pieces) > 1:
                return pieces[:max_helpers]
        return []

    def _note_for_decision(self, decision: str, has_child_summaries: bool) -> str:
        if decision == "delegate":
            return "authored delegate decision deterministically"
        if decision == "report_problem":
            return "authored problem report deterministically"
        if has_child_summaries:
            return "authored local execution after reviewing child results deterministically"
        return "authored local execution deterministically"

    def _zero_usage(self) -> Dict[str, Any]:
        return {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "reasoning_tokens": 0,
            "cached_prompt_tokens": 0,
            "total_tokens": 0,
            "cost_usd": 0.0,
            "provider_details": {"responses": [{"provider": self.provider_name}]},
        }


class OpenRouterLiveExecutor(DeterministicLocalExecutor):
    """Live OpenRouter-backed executor for authored orchestration decisions."""

    provider_name = "openrouter"

    def __init__(
        self,
        *,
        api_key: str | None = None,
        model: str,
        title: str = "Super-Eywa v1",
    ) -> None:
        resolved_api_key = api_key or load_openrouter_api_key()
        if not resolved_api_key:
            raise OpenRouterClientError("OPENROUTER_API_KEY was not found in env or keychain.")
        self.client = OpenRouterChatClient(
            OpenRouterClientConfig(api_key=resolved_api_key, title=title)
        )
        self.model = model

    def author_node_response(
        self,
        *,
        node_packet: Dict[str, Any],
        depth: int,
        turn_index: int,
        allowed_decisions: Iterable[str],
        child_summaries: List[Dict[str, str]] | None = None,
        synthesis_brief: str | None = None,
    ) -> ExecutionStep:
        prompt_bundle = build_turn_prompt(
            node_packet,
            allowed_decisions=allowed_decisions,
            turn_index=turn_index,
            depth=depth,
            child_results=child_summaries,
            synthesis_brief=synthesis_brief,
        )
        max_helpers = int(
            node_packet["variable_resolution"]["resolved_variables"]
            .get("budget_policy", {})
            .get("max_helpers_per_node", 3)
        )
        recovery_policy = str(
            node_packet["variable_resolution"]["resolved_variables"].get("recovery_policy", "report_problem")
        )

        attempts: List[Dict[str, Any]] = []
        generated = self._generate_text(
            system_prompt=prompt_bundle["system_prompt"],
            user_prompt=prompt_bundle["user_prompt"],
        )
        attempts.append(
            self._attempt_record(
                phase="initial_generation",
                generated=generated,
                parse_error=None,
                parsed_response=None,
            )
        )
        combined_usage = dict(generated["usage"])

        authored_response, parse_error = self._try_parse_response(
            generated["content"],
            allowed_decisions=allowed_decisions,
            max_helpers=max_helpers,
        )

        if authored_response is None and recovery_policy == "report_problem":
            repaired = self._repair_response(
                raw_text=generated["content"],
                allowed_decisions=allowed_decisions,
            )
            attempts.append(
                self._attempt_record(
                    phase="json_repair",
                    generated=repaired,
                    parse_error=None,
                    parsed_response=None,
                )
            )
            combined_usage = self._accumulate_usage(combined_usage, repaired["usage"])
            authored_response, parse_error = self._try_parse_response(
                repaired["content"],
                allowed_decisions=allowed_decisions,
                max_helpers=max_helpers,
            )
            attempts[-1]["parse_error"] = parse_error
            attempts[-1]["parsed_response"] = authored_response
        else:
            attempts[-1]["parse_error"] = parse_error
            attempts[-1]["parsed_response"] = authored_response

        if authored_response is None:
            authored_response = self._runtime_problem_response(
                parse_error=parse_error or "runtime could not parse a valid authored response",
                raw_text=generated["content"],
            )

        note = self._note_for_decision(authored_response["orchestration_decision"], bool(child_summaries))
        return ExecutionStep(
            authored_response=authored_response,
            note=note,
            prompt_snapshot=prompt_bundle["snapshot_text"],
            provider_payload={
                "provider": self.provider_name,
                "attempts": attempts,
                "final_authored_response": authored_response,
            },
            usage=combined_usage,
        )

    def _repair_response(self, *, raw_text: str, allowed_decisions: Iterable[str]) -> Dict[str, Any]:
        allowed_display = ", ".join(str(item) for item in allowed_decisions)
        repair_prompt = (
            "Rewrite the following content as valid JSON only for the eywa_node_response v1 schema. "
            f"Allowed orchestration_decision values for this turn: {allowed_display}. "
            "Do not add commentary or markdown fences."
        )
        return self._generate_text(
            system_prompt=(
                "You repair invalid Super-Eywa node responses into strict JSON. "
                "Return only valid JSON."
            ),
            user_prompt=f"{repair_prompt}\n\nOriginal content:\n{raw_text}",
        )

    def _runtime_problem_response(self, *, parse_error: str, raw_text: str) -> Dict[str, Any]:
        excerpt = raw_text.strip()
        if len(excerpt) > 500:
            excerpt = excerpt[:500] + "..."
        return {
            "schema_name": "eywa_node_response",
            "schema_version": "v1",
            "orchestration_decision": "report_problem",
            "decision_notes": "Runtime converted an invalid authored response into a problem report.",
            "response": f"Invalid node-authored response: {parse_error}. Raw response excerpt: {excerpt}",
        }

    def _try_parse_response(
        self,
        raw_text: str,
        *,
        allowed_decisions: Iterable[str],
        max_helpers: int,
    ) -> tuple[Dict[str, Any] | None, str | None]:
        try:
            payload = parse_authored_response_text(raw_text)
            normalized = validate_authored_response(
                payload,
                allowed_decisions=allowed_decisions,
                max_helpers=max_helpers,
            )
        except AuthoredResponseError as exc:
            return None, str(exc)
        return normalized, None

    def _attempt_record(
        self,
        *,
        phase: str,
        generated: Dict[str, Any],
        parse_error: str | None,
        parsed_response: Dict[str, Any] | None,
    ) -> Dict[str, Any]:
        provider_payload = dict(generated["provider_payload"] or {})
        return {
            "phase": phase,
            "request": provider_payload.get("request"),
            "response": provider_payload.get("response"),
            "raw_content": generated["content"],
            "parse_error": parse_error,
            "parsed_response": parsed_response,
        }

    def _generate_text(self, *, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        request_body = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "stream": False,
            "max_tokens": 800,
            "temperature": 0.2,
        }
        response = self.client.create_chat_completion(
            model=self.model,
            messages=request_body["messages"],
            max_tokens=800,
            temperature=0.2,
        )
        response_id = response.get("id")
        usage = self._usage_from_response(response, response_id=response_id)
        if isinstance(response_id, str) and response_id.strip():
            usage = self._merge_usage_with_generation_stats(usage, self._usage_from_generation_stats(response_id))
        choice = response["choices"][0]
        message = dict(choice.get("message") or {})
        content = self._normalize_content(message.get("content"))
        return {
            "content": content or "(empty live-model response)",
            "provider_payload": {
                "provider": self.provider_name,
                "request": request_body,
                "response": response,
            },
            "usage": usage,
        }

    def _normalize_content(self, content: Any) -> str:
        if isinstance(content, str):
            return content.strip()
        if isinstance(content, list):
            parts: List[str] = []
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    parts.append(str(item.get("text", "")))
            return "\n".join(part.strip() for part in parts if part.strip())
        return ""

    def _usage_from_response(self, response: Dict[str, Any], *, response_id: str | None) -> Dict[str, Any]:
        usage_data = dict(response.get("usage") or {})
        prompt_details = dict(usage_data.get("prompt_tokens_details") or {})
        completion_details = dict(usage_data.get("completion_tokens_details") or {})
        prompt_tokens = int(usage_data.get("prompt_tokens", 0) or 0)
        completion_tokens = int(usage_data.get("completion_tokens", 0) or 0)
        total_tokens = int(usage_data.get("total_tokens", 0) or 0) or (prompt_tokens + completion_tokens)
        return {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "reasoning_tokens": int(completion_details.get("reasoning_tokens", 0) or 0),
            "cached_prompt_tokens": int(prompt_details.get("cached_tokens", 0) or 0),
            "total_tokens": total_tokens,
            "cost_usd": float(usage_data.get("cost", 0.0) or 0.0),
            "provider_details": {
                "responses": [
                    {
                        "response_id": response_id,
                        "model": response.get("model"),
                        "usage_from": "chat_completions",
                        "response_cost_usd": float(usage_data.get("cost", 0.0) or 0.0),
                    }
                ]
            },
        }

    def _usage_from_generation_stats(self, response_id: str) -> Dict[str, Any]:
        try:
            generation = self.client.get_generation_stats(response_id)
        except OpenRouterClientError:
            return {}
        data = dict(generation.get("data") or {})
        prompt_tokens = int(data.get("tokens_prompt", 0) or 0)
        completion_tokens = int(data.get("tokens_completion", 0) or 0)
        total_tokens = int(data.get("native_tokens_prompt", 0) or 0) + int(
            data.get("native_tokens_completion", 0) or 0
        )
        if not total_tokens:
            total_tokens = prompt_tokens + completion_tokens
        return {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "cost_usd": float(data.get("total_cost", 0.0) or 0.0),
            "provider_details": {
                "responses": [
                    {
                        "response_id": response_id,
                        "provider_name": data.get("provider_name"),
                        "latency_ms": data.get("latency"),
                        "usage_from": "generation_stats",
                    }
                ]
            },
        }

    def _accumulate_usage(self, current: Dict[str, Any], update: Dict[str, Any]) -> Dict[str, Any]:
        if not update:
            return current
        provider_details = dict(current.get("provider_details") or {})
        current_responses = list(provider_details.get("responses") or [])
        current_responses.extend((update.get("provider_details") or {}).get("responses", []))
        provider_details["responses"] = current_responses
        return {
            "prompt_tokens": int(current.get("prompt_tokens", 0) or 0) + int(update.get("prompt_tokens", 0) or 0),
            "completion_tokens": int(current.get("completion_tokens", 0) or 0)
            + int(update.get("completion_tokens", 0) or 0),
            "reasoning_tokens": int(current.get("reasoning_tokens", 0) or 0)
            + int(update.get("reasoning_tokens", 0) or 0),
            "cached_prompt_tokens": int(current.get("cached_prompt_tokens", 0) or 0)
            + int(update.get("cached_prompt_tokens", 0) or 0),
            "total_tokens": int(current.get("total_tokens", 0) or 0) + int(update.get("total_tokens", 0) or 0),
            "cost_usd": float(current.get("cost_usd", 0.0) or 0.0) + float(update.get("cost_usd", 0.0) or 0.0),
            "provider_details": provider_details,
        }

    def _merge_usage_with_generation_stats(self, current: Dict[str, Any], update: Dict[str, Any]) -> Dict[str, Any]:
        if not update:
            return current
        provider_details = dict(current.get("provider_details") or {})
        current_responses = list(provider_details.get("responses") or [])
        current_responses.extend((update.get("provider_details") or {}).get("responses", []))
        provider_details["responses"] = current_responses
        return {
            "prompt_tokens": self._prefer_numeric(update, current, "prompt_tokens"),
            "completion_tokens": self._prefer_numeric(update, current, "completion_tokens"),
            "reasoning_tokens": self._prefer_numeric(current, update, "reasoning_tokens"),
            "cached_prompt_tokens": self._prefer_numeric(current, update, "cached_prompt_tokens"),
            "total_tokens": self._prefer_numeric(update, current, "total_tokens"),
            "cost_usd": self._prefer_numeric(update, current, "cost_usd"),
            "provider_details": provider_details,
        }

    def _prefer_numeric(self, primary: Dict[str, Any], secondary: Dict[str, Any], key: str) -> int | float:
        primary_value = primary.get(key)
        if primary_value not in (None, 0, 0.0):
            return primary_value
        secondary_value = secondary.get(key)
        if secondary_value is None:
            return 0
        return secondary_value


def build_executor(run_level_variables: Dict[str, Any]) -> DeterministicLocalExecutor:
    runtime_provider = str(run_level_variables.get("runtime_provider", "deterministic")).strip().lower()
    model = str(run_level_variables.get("model", "deterministic-local-v1")).strip()

    if runtime_provider == "deterministic":
        return DeterministicLocalExecutor()
    if runtime_provider == "openrouter":
        return OpenRouterLiveExecutor(model=model)
    raise ValueError(f"Unsupported runtime_provider: {runtime_provider}")

"""Deterministic and live executors for Super-Eywa v1."""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any, Dict, List

from .contracts import validate_node_output
from .openrouter_client import OpenRouterChatClient, OpenRouterClientConfig, OpenRouterClientError
from .secrets import load_openrouter_api_key


@dataclass
class ExecutionStep:
    """One authored output step from an executor."""

    output: Dict[str, object]
    note: str
    provider_payload: Dict[str, Any] | None = None
    usage: Dict[str, Any] | None = None


class DeterministicLocalExecutor:
    """A minimal local executor that keeps v1 runnable without external model keys."""

    provider_name = "deterministic-local-v1"

    def should_decompose(self, instructions: str, depth: int, max_depth: int) -> bool:
        if depth >= max_depth:
            return False
        separators = [" and ", ";", "\n- ", "\n1.", " Then ", " then "]
        return any(separator in instructions for separator in separators)

    def split_instructions(self, instructions: str, max_helpers: int) -> List[str]:
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

    def recruit_help(
        self,
        *,
        run_id: str,
        node_id: str,
        helper_node_ids: List[str],
        subtasks: List[str],
    ) -> ExecutionStep:
        packets = []
        for helper_node_id, subtask in zip(helper_node_ids, subtasks):
            packets.append(
                {
                    "message_type": "helper_assignment",
                    "target": {
                        "target_type": "new_helper",
                        "target_ref": helper_node_id,
                    },
                    "message": subtask,
                    "attachment_refs": [],
                }
            )
        payload = {
            "contract_name": "node_output",
            "contract_version": "v1",
            "run_id": run_id,
            "node_id": node_id,
            "action_type": "recruit_help",
            "results": [
                {
                    "result_type": "plan",
                    "content": f"Split work into {len(subtasks)} helper tasks.",
                    "attachment_refs": [],
                }
            ],
            "outgoing_packets": packets,
        }
        validate_node_output(payload)
        return ExecutionStep(
            output=payload,
            note="deterministic split into helper tasks",
            provider_payload={"provider": self.provider_name},
            usage=self._zero_usage(),
        )

    def report_problem(self, *, run_id: str, node_id: str, creation_parent_node_id: str | None, message: str) -> ExecutionStep:
        packets = []
        if creation_parent_node_id is not None:
            packets.append(
                {
                    "message_type": "problem_report",
                    "target": {
                        "target_type": "creating_parent",
                        "target_ref": creation_parent_node_id,
                    },
                    "message": message,
                    "attachment_refs": [],
                }
            )
        payload = {
            "contract_name": "node_output",
            "contract_version": "v1",
            "run_id": run_id,
            "node_id": node_id,
            "action_type": "report_problem",
            "results": [
                {
                    "result_type": "failure_explanation",
                    "content": message,
                    "attachment_refs": [],
                }
            ],
            "outgoing_packets": packets,
        }
        validate_node_output(payload)
        return ExecutionStep(
            output=payload,
            note="reported problem deterministically",
            provider_payload={"provider": self.provider_name},
            usage=self._zero_usage(),
        )

    def report_success(
        self,
        *,
        run_id: str,
        node_id: str,
        creation_parent_node_id: str | None,
        instructions: str,
        child_summaries: List[Dict[str, str]] | None = None,
    ) -> ExecutionStep:
        if child_summaries:
            content_lines = [
                f"Completed synthesized work for: {instructions}",
                "Combined child results:",
            ]
            for item in child_summaries:
                content_lines.append(f"- {item['node_id']}: {item['summary']}")
            content = "\n".join(content_lines)
        else:
            content = (
                f"Completed local deterministic work for: {instructions}\n"
                "This is a v1 scaffold result produced without a live model provider."
            )

        packets = []
        if creation_parent_node_id is not None:
            packets.append(
                {
                    "message_type": "success_report",
                    "target": {
                        "target_type": "creating_parent",
                        "target_ref": creation_parent_node_id,
                    },
                    "message": content,
                    "attachment_refs": [],
                }
            )
        payload = {
            "contract_name": "node_output",
            "contract_version": "v1",
            "run_id": run_id,
            "node_id": node_id,
            "action_type": "report_success",
            "results": [
                {
                    "result_type": "summary",
                    "content": content,
                    "attachment_refs": [],
                }
            ],
            "outgoing_packets": packets,
        }
        validate_node_output(payload)
        note = "reported success after synthesizing helper results" if child_summaries else "reported local success deterministically"
        return ExecutionStep(
            output=payload,
            note=note,
            provider_payload={"provider": self.provider_name},
            usage=self._zero_usage(),
        )

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
    """Live OpenRouter-backed executor for local work and synthesis."""

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

    def report_problem(self, *, run_id: str, node_id: str, creation_parent_node_id: str | None, message: str) -> ExecutionStep:
        generated = self._generate_text(
            system_prompt="You are one Super-Eywa node. Explain the problem briefly and clearly. Return only the explanation text.",
            user_prompt=message,
        )
        packets = []
        if creation_parent_node_id is not None:
            packets.append(
                {
                    "message_type": "problem_report",
                    "target": {
                        "target_type": "creating_parent",
                        "target_ref": creation_parent_node_id,
                    },
                    "message": generated["content"],
                    "attachment_refs": [],
                }
            )
        payload = {
            "contract_name": "node_output",
            "contract_version": "v1",
            "run_id": run_id,
            "node_id": node_id,
            "action_type": "report_problem",
            "results": [
                {
                    "result_type": "failure_explanation",
                    "content": generated["content"],
                    "attachment_refs": [],
                }
            ],
            "outgoing_packets": packets,
        }
        validate_node_output(payload)
        return ExecutionStep(
            output=payload,
            note="reported problem via live OpenRouter model",
            provider_payload=generated["provider_payload"],
            usage=generated["usage"],
        )

    def report_success(
        self,
        *,
        run_id: str,
        node_id: str,
        creation_parent_node_id: str | None,
        instructions: str,
        child_summaries: List[Dict[str, str]] | None = None,
    ) -> ExecutionStep:
        if child_summaries:
            child_lines = "\n".join(f"- {item['node_id']}: {item['summary']}" for item in child_summaries)
            user_prompt = (
                f"Top-level assignment:\n{instructions}\n\n"
                f"Child results:\n{child_lines}\n\n"
                "Synthesize these into one concise, useful result."
            )
            system_prompt = (
                "You are one Super-Eywa node synthesizing child node outputs. "
                "Return only the synthesized result text."
            )
        else:
            user_prompt = (
                f"Node assignment:\n{instructions}\n\n"
                "Produce a concise, useful result for this node. Return only the result text."
            )
            system_prompt = (
                "You are one Super-Eywa node doing local work. "
                "Return only the work result text."
            )

        generated = self._generate_text(system_prompt=system_prompt, user_prompt=user_prompt)
        packets = []
        if creation_parent_node_id is not None:
            packets.append(
                {
                    "message_type": "success_report",
                    "target": {
                        "target_type": "creating_parent",
                        "target_ref": creation_parent_node_id,
                    },
                    "message": generated["content"],
                    "attachment_refs": [],
                }
            )
        payload = {
            "contract_name": "node_output",
            "contract_version": "v1",
            "run_id": run_id,
            "node_id": node_id,
            "action_type": "report_success",
            "results": [
                {
                    "result_type": "summary",
                    "content": generated["content"],
                    "attachment_refs": [],
                }
            ],
            "outgoing_packets": packets,
        }
        validate_node_output(payload)
        note = (
            "reported success after live-model synthesis of helper results"
            if child_summaries
            else "reported local success via live OpenRouter model"
        )
        return ExecutionStep(
            output=payload,
            note=note,
            provider_payload=generated["provider_payload"],
            usage=generated["usage"],
        )

    def _generate_text(self, *, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        request_body = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "stream": False,
            "max_tokens": 600,
            "temperature": 0.2,
        }
        response = self.client.create_chat_completion(
            model=self.model,
            messages=request_body["messages"],
            max_tokens=600,
            temperature=0.2,
        )
        response_id = response.get("id")
        usage = self._usage_from_response(response, response_id=response_id)
        if isinstance(response_id, str) and response_id.strip():
            usage = self._merge_usage(usage, self._usage_from_generation_stats(response_id))
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

    def _merge_usage(self, current: Dict[str, Any], update: Dict[str, Any]) -> Dict[str, Any]:
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

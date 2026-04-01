from __future__ import annotations

import json
import re
import time
from pathlib import Path
from typing import Any

from runtime.config import load_config, openrouter_api_key, repo_root, role_model, role_tools
from runtime.openrouter_client import OpenRouterClient, OpenRouterError
from tools.registry import ToolRegistry


ROLE_PROMPTS = {
    "librarian": "stuff-for-agents/librarian/system-prompt.md",
    "planner": "stuff-for-agents/planning/planner/system-prompt.md",
    "worker": "stuff-for-agents/worker/system-prompt.md",
    "plan-reviewer": "stuff-for-agents/planning/plan-reviewer/system-prompt.md",
    "plan-decider": "stuff-for-agents/planning/plan-decider/system-prompt.md",
    "mid-plan-evaluator": "stuff-for-agents/planning/mid-plan-evaluator/system-prompt.md",
    "synthesizer": "stuff-for-agents/synthesizer/system-prompt.md",
}

AUTO_CAPTURE_TARGETS = {
    "librarian": "input/retrieved_relevant_knowledge_from_library.md",
    "planner": "output/plan.md",
    "worker": "output/final-output.md",
    "plan-reviewer": "output/review.md",
    "synthesizer": "output/final-output.md",
}

ROLE_REQUIRED_OUTPUTS = {
    "librarian": ["input/retrieved_relevant_knowledge_from_library.md"],
    "planner": ["output/plan.md"],
    "worker": ["output/final-output.md"],
    "plan-reviewer": ["output/review.md"],
    "mid-plan-evaluator": ["for-orchestrator/eval-decision"],
    "synthesizer": ["output/final-output.md", "for-orchestrator/eval-decision"],
}


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _loop_log_path(node_path: Path) -> Path:
    return node_path / "system" / "agent-loop.jsonl"


def _summary_path(node_path: Path) -> Path:
    return node_path / "system" / "usage-summary.json"


def _usage_totals() -> dict[str, float]:
    return {
        "requests": 0,
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "reasoning_tokens": 0,
        "cached_tokens": 0,
        "total_tokens": 0,
        "cost": 0.0,
    }


def _merge_usage(totals: dict[str, float], usage: dict[str, Any]) -> dict[str, float]:
    totals["requests"] += 1
    totals["prompt_tokens"] += usage.get("prompt_tokens", 0)
    totals["completion_tokens"] += usage.get("completion_tokens", 0)
    totals["total_tokens"] += usage.get("total_tokens", 0)
    totals["cost"] += float(usage.get("cost", 0.0))
    totals["reasoning_tokens"] += usage.get("completion_tokens_details", {}).get("reasoning_tokens", 0)
    totals["cached_tokens"] += usage.get("prompt_tokens_details", {}).get("cached_tokens", 0)
    return totals


def _append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=True) + "\n")


def _record_usage(
    *,
    mission_dir: Path,
    node_path: Path,
    role: str,
    model: str,
    iteration: int,
    usage: dict[str, Any],
    response_id: str | None,
) -> None:
    entry = {
        "ts": _now(),
        "node": str(node_path.relative_to(mission_dir)),
        "role": role,
        "model": model,
        "iteration": iteration,
        "response_id": response_id,
        "usage": usage,
    }
    _append_jsonl(mission_dir / "usage.jsonl", entry)
    _append_jsonl(_loop_log_path(node_path), {**entry, "kind": "usage"})


def _record_event(node_path: Path, payload: dict[str, Any]) -> None:
    _append_jsonl(_loop_log_path(node_path), payload)


def _expected_instruction_path(node_path: Path, role: str) -> Path:
    return node_path / "input" / f"instructions-{role}.md"


def _extract_eval_decision(text: str) -> str | None:
    normalized = text.strip().lower()
    if normalized in {"continue", "replan", "escalate", "synthesize"}:
        return normalized
    for candidate in ("continue", "replan", "escalate", "synthesize"):
        if re.search(rf"\b{candidate}\b", normalized):
            return candidate
    return None


def _default_retrieval_note() -> str:
    return (
        "## Factual Knowledge\n\n"
        "No relevant material was found in the library for this node.\n"
        "Source: none\n\n"
        "## Meta Knowledge\n\n"
        "No reusable planning or execution guidance was identified beyond the current node instructions.\n"
        "Source: none\n"
    )


def _role_outputs_satisfied(role: str, node_path: Path) -> bool:
    escalation_path = node_path / "output" / "escalation.md"
    if role in {"planner", "worker", "plan-decider", "mid-plan-evaluator", "synthesizer"} and escalation_path.exists():
        return True
    required = ROLE_REQUIRED_OUTPUTS.get(role, [])
    return all((node_path / rel_path).exists() for rel_path in required)


def _missing_output_paths(role: str, node_path: Path) -> list[str]:
    return [
        rel_path
        for rel_path in ROLE_REQUIRED_OUTPUTS.get(role, [])
        if not (node_path / rel_path).exists()
    ]


def _missing_output_reminder(role: str, node_path: Path) -> str:
    missing = _missing_output_paths(role, node_path)
    if role == "librarian":
        return (
            "You have not finished yet. Write `input/retrieved_relevant_knowledge_from_library.md` now. "
            "If nothing useful is available, write a short note saying so plainly."
        )
    if role == "planner":
        return (
            "You have not finished yet. Write `output/plan.md` in the required strict plan format now. "
            "If the task is impossible, write `output/escalation.md` instead."
        )
    if role == "worker":
        return (
            "You have not finished yet. Write `output/final-output.md` now. "
            "If the task cannot be completed, write `output/escalation.md` instead."
        )
    if role == "plan-reviewer":
        return "You have not finished yet. Write `output/review.md` now."
    if role == "mid-plan-evaluator":
        return (
            "You have not finished yet. Write `for-orchestrator/eval-decision` with exactly one of "
            "`continue`, `replan`, or `escalate`, and update `output/state.md`."
        )
    if role == "synthesizer":
        return (
            "You have not finished yet. Write `output/final-output.md` and write "
            "`for-orchestrator/eval-decision` containing exactly `synthesize`."
        )
    return (
        "You have not finished yet. Required output files are still missing: "
        + ", ".join(missing)
    )


def _apply_role_fallbacks(role: str, node_path: Path, last_assistant_content: str) -> None:
    auto_target = AUTO_CAPTURE_TARGETS.get(role)
    escalation_path = node_path / "output" / "escalation.md"
    if auto_target and last_assistant_content.strip() and not escalation_path.exists():
        target_path = node_path / auto_target
        if not target_path.exists():
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_text(last_assistant_content, encoding="utf-8")
            if role == "synthesizer":
                (node_path / "for-orchestrator" / "eval-decision").write_text(
                    "synthesize", encoding="utf-8"
                )
    if role == "mid-plan-evaluator" and last_assistant_content.strip():
        decision_path = node_path / "for-orchestrator" / "eval-decision"
        state_path = node_path / "output" / "state.md"
        if not state_path.exists():
            state_path.parent.mkdir(parents=True, exist_ok=True)
            state_path.write_text(last_assistant_content, encoding="utf-8")
        if not decision_path.exists():
            decision = _extract_eval_decision(last_assistant_content)
            if decision:
                decision_path.write_text(decision, encoding="utf-8")
    if role == "librarian":
        retrieval_path = node_path / "input" / "retrieved_relevant_knowledge_from_library.md"
        if not retrieval_path.exists():
            retrieval_path.parent.mkdir(parents=True, exist_ok=True)
            retrieval_path.write_text(
                last_assistant_content.strip() or _default_retrieval_note(),
                encoding="utf-8",
            )


def run_agent(role: str, node_path: Path, mission_dir: Path) -> int:
    config = load_config()
    node_path = node_path.resolve()
    mission_dir = mission_dir.resolve()
    node_system_dir = node_path / "system"
    node_system_dir.mkdir(parents=True, exist_ok=True)
    (node_system_dir / "artifacts").mkdir(parents=True, exist_ok=True)
    (node_system_dir / "jobs").mkdir(parents=True, exist_ok=True)

    prompt_path = repo_root() / ROLE_PROMPTS[role]
    instructions_path = _expected_instruction_path(node_path, role)
    if not instructions_path.exists():
        raise RuntimeError(f"Instructions file not found: {instructions_path}")

    system_prompt = _read_text(prompt_path)
    instructions = _read_text(instructions_path)
    model = role_model(role, config)
    enabled_tools = role_tools(role, config)
    registry = ToolRegistry(
        repo_root=repo_root(),
        mission_dir=mission_dir,
        node_path=node_path,
        role=role,
        tool_names=enabled_tools,
        preview_chars=config["runtime"]["tool_output_preview_chars"],
    )

    client = OpenRouterClient(
        api_key=openrouter_api_key(),
        api_base_url=config["runtime"]["api_base_url"],
        chat_endpoint=config["runtime"]["chat_endpoint"],
        timeout_seconds=config["runtime"]["timeout_seconds"],
        max_retries=int(config["runtime"].get("request_max_retries", 3)),
        retry_backoff_seconds=float(config["runtime"].get("request_retry_backoff_seconds", 2.0)),
        app_name=config["runtime"]["app_name"],
        app_url=config["runtime"]["app_url"],
    )

    messages: list[dict[str, Any]] = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": (
                f"Working directory: {node_path}\n"
                f"Mission directory: {mission_dir}\n\n"
                "Follow these instructions exactly:\n\n"
                f"{instructions}"
            ),
        },
    ]
    totals = _usage_totals()
    max_iterations = int(config["runtime"]["max_iterations"])
    last_assistant_content = ""

    _record_event(
        node_path,
        {
            "ts": _now(),
            "kind": "spawn",
            "role": role,
            "model": model,
            "node": str(node_path.relative_to(mission_dir)),
        },
    )

    for iteration in range(1, max_iterations + 1):
        try:
            response = client.chat_completion(
                model=model,
                messages=messages,
                tools=registry.schemas(),
                temperature=float(config["runtime"]["temperature"]),
                max_completion_tokens=int(config["runtime"]["max_completion_tokens"]),
            )
        except OpenRouterError as exc:
            _record_event(
                node_path,
                {
                    "ts": _now(),
                    "kind": "model_error",
                    "iteration": iteration,
                    "role": role,
                    "model": model,
                    "error": str(exc),
                },
            )
            raise
        usage = response.get("usage", {})
        totals = _merge_usage(totals, usage)
        response_id = response.get("id")
        _record_usage(
            mission_dir=mission_dir,
            node_path=node_path,
            role=role,
            model=model,
            iteration=iteration,
            usage=usage,
            response_id=response_id,
        )

        choice = response["choices"][0]
        message = choice["message"]
        tool_calls = message.get("tool_calls") or []
        last_assistant_content = message.get("content") or ""
        messages.append(
            {
                "role": "assistant",
                "content": message.get("content"),
                "tool_calls": tool_calls if tool_calls else None,
            }
        )
        _record_event(
            node_path,
            {
                "ts": _now(),
                "kind": "assistant",
                "iteration": iteration,
                "finish_reason": choice.get("finish_reason"),
                "tool_call_count": len(tool_calls),
                "response_id": response_id,
            },
        )

        if tool_calls:
            for tool_call in tool_calls:
                arguments = json.loads(tool_call["function"]["arguments"] or "{}")
                try:
                    result = registry.execute(tool_call["function"]["name"], arguments)
                except Exception as exc:  # noqa: BLE001
                    result = {
                        "error": str(exc),
                        "type": type(exc).__name__,
                        "tool": tool_call["function"]["name"],
                    }
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "content": json.dumps(result, ensure_ascii=True),
                    }
                )
            continue

        _apply_role_fallbacks(role, node_path, last_assistant_content)
        if _role_outputs_satisfied(role, node_path):
            break
        if iteration < max_iterations:
            _record_event(
                node_path,
                {
                    "ts": _now(),
                    "kind": "missing_artifacts",
                    "iteration": iteration,
                    "role": role,
                    "missing": _missing_output_paths(role, node_path),
                },
            )
            messages.append(
                {
                    "role": "user",
                    "content": _missing_output_reminder(role, node_path),
                }
            )
            continue
        break

    _summary_path(node_path).write_text(json.dumps(totals, indent=2), encoding="utf-8")
    _apply_role_fallbacks(role, node_path, last_assistant_content)
    return 0

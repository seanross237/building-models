"""Prompt-optimization tutor for Mission Exploration 1 loops."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from typing import Any, Dict, Iterable, List, Tuple


THIS_DIR = Path(__file__).resolve().parent
RUNTIME_DIR = THIS_DIR.parents[1] / "eywa-system" / "runtime"
if str(RUNTIME_DIR) not in sys.path:
    sys.path.insert(0, str(RUNTIME_DIR))

from eywa_runtime.openrouter_client import OpenRouterChatClient, OpenRouterClientConfig, OpenRouterClientError  # noqa: E402
from eywa_runtime.secrets import load_openrouter_api_key  # noqa: E402
from mx1_loop_v1 import build_loop_manifest_path, load_json, write_json  # noqa: E402


MX1_TUTOR_SCHEMA_NAME = "mx1_prompt_tutor"
MX1_TUTOR_SCHEMA_VERSION = "v1"


class MX1TutorError(ValueError):
    """Raised when the MX1 tutor cannot produce a valid recommendation."""


def build_tutor_record_path(
    *,
    tutoring_root: Path,
    question_id: str,
    family: str,
    loop_id: str,
    iteration_index: int,
) -> Path:
    root = tutoring_root.resolve()
    return root / question_id / family / f"{loop_id}__iter_{iteration_index:02d}.json"


def build_prior_attempts(manifest: dict[str, Any], current_iteration_index: int) -> list[dict[str, Any]]:
    attempts = list(manifest.get("attempts") or [])
    return [
        attempt
        for attempt in attempts
        if int(attempt.get("iteration_index") or 0) < current_iteration_index
    ]


def run_mx1_tutor(
    *,
    manifest_path: Path,
    grading_record_path: Path,
    tutoring_root: Path,
    tutor_provider: str,
    tutor_model: str | None,
) -> dict[str, Any]:
    manifest = load_json(manifest_path)
    grading_record = load_json(grading_record_path)

    if not manifest.get("attempts"):
        raise MX1TutorError("The loop manifest does not contain any attempts to review.")

    target_attempt = _latest_attempt(manifest)
    iteration_index = int(target_attempt.get("iteration_index") or 0)
    tutor_provider = str(tutor_provider or grading_record.get("runtime_provider") or "deterministic").strip()
    tutor_model = str(tutor_model or grading_record.get("model") or "deterministic-mx1-tutor-v1").strip()

    if tutor_provider == "same":
        tutor_provider = str(grading_record.get("runtime_provider") or "deterministic").strip()
        tutor_model = str(grading_record.get("model") or tutor_model).strip()

    prior_attempts = build_prior_attempts(manifest, iteration_index)
    if tutor_provider == "deterministic":
        tutor, provider_payload = _build_deterministic_tutor(
            manifest=manifest,
            grading_record=grading_record,
            current_attempt=target_attempt,
            prior_attempts=prior_attempts,
        )
    elif tutor_provider == "openrouter":
        tutor, provider_payload = _build_openrouter_tutor(
            manifest=manifest,
            grading_record=grading_record,
            current_attempt=target_attempt,
            prior_attempts=prior_attempts,
            tutor_model=tutor_model,
        )
    else:
        raise MX1TutorError(f"Unsupported tutor_provider: {tutor_provider}")

    tutor_record = {
        "schema_name": MX1_TUTOR_SCHEMA_NAME,
        "schema_version": MX1_TUTOR_SCHEMA_VERSION,
        "question_id": manifest.get("question_id"),
        "question_title": manifest.get("question_title"),
        "question_file": manifest.get("question_file"),
        "family": manifest.get("family"),
        "loop_id": manifest.get("loop_id"),
        "loop_manifest_path": str(manifest_path),
        "iteration_index": iteration_index,
        "run_id": target_attempt.get("run_id"),
        "run_dir": target_attempt.get("run_dir"),
        "grading_record_path": str(grading_record_path),
        "runtime_provider": grading_record.get("runtime_provider"),
        "model": grading_record.get("model"),
        "tutor_provider": tutor_provider,
        "tutor_model": tutor_model,
        "current_prompt_text": target_attempt.get("prompt_text"),
        "current_prompt_file": target_attempt.get("prompt_file"),
        "metrics": {
            "score": target_attempt.get("score"),
            "correct": target_attempt.get("correct"),
            "total_tokens": target_attempt.get("total_tokens"),
            "total_wall_time_ms": target_attempt.get("total_wall_time_ms"),
            "total_cost_usd": target_attempt.get("total_cost_usd"),
        },
        "history_summary": manifest.get("history_summary") or {},
        "prior_attempts": [
            _compact_attempt(attempt)
            for attempt in prior_attempts
        ],
        "tutor": tutor,
        "provider_payload": provider_payload,
    }

    tutor_record_path = build_tutor_record_path(
        tutoring_root=tutoring_root,
        question_id=str(manifest.get("question_id") or "unknown-question"),
        family=str(manifest.get("family") or "unknown-family"),
        loop_id=str(manifest.get("loop_id") or "unknown-loop"),
        iteration_index=iteration_index,
    )
    tutor_record["tutor_record_path"] = str(tutor_record_path)
    write_json(tutor_record_path, tutor_record)
    return tutor_record


def build_tutor_prompt(
    *,
    manifest: dict[str, Any],
    grading_record: dict[str, Any],
    current_attempt: dict[str, Any],
    prior_attempts: list[dict[str, Any]],
) -> str:
    exploration_iterations = int(manifest.get("exploration_iterations") or 3)
    current_iteration = int(current_attempt.get("iteration_index") or 0)
    family = str(manifest.get("family") or "transmute").strip()
    history_summary = manifest.get("history_summary") or {}
    starter_prompt_text = str(manifest.get("starter_prompt_text") or "")
    current_prompt_text = str(current_attempt.get("prompt_text") or "")
    current_score = float(current_attempt.get("score") or 0.0)
    current_correct = grading_record.get("grading", {}).get("correct")
    current_metrics = {
        "score": current_attempt.get("score"),
        "correct": current_attempt.get("correct"),
        "total_tokens": current_attempt.get("total_tokens"),
        "total_wall_time_ms": current_attempt.get("total_wall_time_ms"),
        "total_cost_usd": current_attempt.get("total_cost_usd"),
    }
    current_run_context = {
        "validation_status": grading_record.get("validation_status"),
        "node_count": grading_record.get("node_count"),
        "root_orchestration": grading_record.get("root_orchestration"),
        "root_result_excerpt": grading_record.get("root_result_excerpt"),
        "final_result_excerpt": grading_record.get("final_result_excerpt"),
    }
    compact_history = [_compact_attempt(attempt) for attempt in prior_attempts]
    exploration_note = (
        "For the first few iterations, favor meaningfully different prompt directions over tiny edits."
        if current_iteration <= exploration_iterations
        else "Prefer refinement unless the history shows a plateau."
    )
    if current_correct is None:
        efficiency_note = (
            "This task uses a continuous score. If the score is still zero, prioritize getting to any valid positive score first. "
            "After that, optimize score before using tokens and wall-clock time as tie-breakers."
            if current_score <= 0.0
            else "This task uses a continuous score. Optimize score first, and use tokens and wall-clock time only as tie-breakers after preserving or improving score."
        )
    else:
        efficiency_note = (
            "Because the current answer is still wrong, treat tokens and wall-clock time as background only; prioritize finding a prompt that improves correctness."
            if current_score <= 0.0
            else "Only after preserving score should you use tokens and wall-clock time as tie-breakers."
        )

    return (
        "You are the MX1 prompt tutor. Your job is to recommend the next prompt text for the current prompt family.\n"
        "Optimize for correctness first.\n"
        f"{efficiency_note}\n"
        f"{exploration_note}\n"
        "Recommend a reusable family-level prompt, not a question-specific rewrite.\n"
        "Do not bake in problem details such as concrete numbers, equations, named subproblems, candidate answers, or a fixed helper count.\n"
        "The next prompt should describe how to approach this family of task in general, while leaving the actual problem content to the question that will be injected later.\n"
        "If the last two attempts have not improved tokens or time by at least 10% without hurting score, "
        "lean toward a new direction.\n"
        f"Do not change the family-level output contract. The recommended prompt must remain a valid {family} prompt.\n"
        "Return only valid JSON matching the required schema.\n\n"
        f"Question:\n{grading_record.get('task_text') or ''}\n\n"
        f"Family: {family}\n"
        f"Loop id: {manifest.get('loop_id')}\n"
        f"Current iteration: {current_iteration}\n"
        f"Starter prompt:\n{starter_prompt_text}\n\n"
        f"Current prompt:\n{current_prompt_text}\n\n"
        f"Current metrics:\n{json.dumps(current_metrics, indent=2)}\n\n"
        f"Current run context:\n{json.dumps(current_run_context, indent=2)}\n\n"
        f"Loop history summary:\n{json.dumps(history_summary, indent=2)}\n\n"
        f"Prior attempts:\n{json.dumps(compact_history, indent=2)}\n\n"
        "Explain what helped, what hurt, and recommend the next prompt text."
    )


def _build_deterministic_tutor(
    *,
    manifest: dict[str, Any],
    grading_record: dict[str, Any],
    current_attempt: dict[str, Any],
    prior_attempts: list[dict[str, Any]],
) -> tuple[dict[str, Any], dict[str, Any]]:
    current_iteration = int(current_attempt.get("iteration_index") or 0)
    family = str(manifest.get("family") or "transmute").strip()
    score = float(current_attempt.get("score") or 0.0)
    current_tokens = float(current_attempt.get("total_tokens") or 0.0)
    current_time = float(current_attempt.get("total_wall_time_ms") or 0.0)
    best_before = _best_before(prior_attempts)
    best_before_score = float(best_before.get("score") or 0.0) if best_before else None
    plateau_streak = int((manifest.get("history_summary") or {}).get("plateau_streak") or 0)
    exploration_iterations = int(manifest.get("exploration_iterations") or 3)
    wrong_so_far = score <= 0.0 and (best_before_score is None or best_before_score <= 0.0)

    if wrong_so_far and current_iteration <= exploration_iterations:
        action = "adjust"
        reason = "The answers are still wrong, so this phase should keep exploring meaningfully different prompt directions."
        new_prompt_text = _exploration_prompt_text(family, direction="simplify")
    elif wrong_so_far and plateau_streak >= 2:
        action = "pivot"
        reason = "The answers are still wrong across multiple attempts, so the next prompt should pivot hard to a different reasoning strategy."
        new_prompt_text = _exploration_prompt_text(family, direction="feasibility_checks")
    elif wrong_so_far:
        action = "adjust"
        reason = "The answers are still wrong, so the next prompt should keep pushing on correctness rather than efficiency."
        new_prompt_text = _exploration_prompt_text(family, direction="formalize")
    elif current_iteration <= exploration_iterations:
        action = "adjust"
        reason = "This iteration should still explore a meaningfully different prompt direction."
        new_prompt_text = _exploration_prompt_text(family, direction="simplify")
    elif plateau_streak >= 2:
        action = "pivot"
        reason = "The loop appears to have plateaued on efficiency, so the next prompt should change direction."
        new_prompt_text = _exploration_prompt_text(family, direction="formalize")
    elif best_before_score is not None and score >= best_before_score:
        action = "keep"
        reason = "The current direction is not worse on score, so a small refinement is safer than a full pivot."
        new_prompt_text = _exploration_prompt_text(family, direction="compress")
    else:
        action = "adjust"
        reason = "The current prompt is not clearly improving the run, so the next one should be a sharper transmutation."
        new_prompt_text = _exploration_prompt_text(family, direction="simplify")

    score_direction = _direction(score, best_before_score)
    token_direction = _direction_decrease(
        previous=float(best_before.get("total_tokens") or 0.0) if best_before else None,
        current=current_tokens,
    )
    time_direction = _direction_decrease(
        previous=float(best_before.get("total_wall_time_ms") or 0.0) if best_before else None,
        current=current_time,
    )

    tutor = {
        "correctness_assessment": _correctness_assessment(grading_record),
        "assessment": {
            "score_direction": score_direction,
            "token_direction": token_direction,
            "time_direction": time_direction,
            "summary": _build_summary(score, best_before_score, plateau_streak),
        },
        "what_helped": [
            "The loop preserved the question and family boundary so changes stay interpretable.",
            "The current prompt is isolated as the only variable being optimized.",
        ],
        "what_hurt": [
            "The run still has room to improve in either correctness or efficiency.",
        ],
        "recommendation": {
            "action": action,
            "reason": reason,
            "new_prompt_text": new_prompt_text,
        },
        "history_observations": _history_observations(manifest, prior_attempts),
        "confidence": "medium" if current_iteration <= exploration_iterations else "high",
    }

    provider_payload = {
        "provider": "deterministic",
        "request": None,
        "response": {"content": json.dumps(tutor, indent=2)},
        "parse_error": None,
    }
    return tutor, provider_payload


def _correctness_assessment(grading_record: dict[str, Any]) -> str:
    grading = grading_record.get("grading", {}) or {}
    score = grading.get("score")
    correct = grading.get("correct")
    if score is None:
        return "ungraded"
    if correct is True:
        return "correct"
    if correct is False:
        return "incorrect"
    return "scored"


def _exploration_prompt_text(family: str, *, direction: str) -> str:
    if family == "execute":
        if direction == "feasibility_checks":
            return (
                "Solve the problem directly, but first test the smallest or simplest candidate answers before expanding the search. "
                "Use direct contradiction or quick feasibility checks when possible."
            )
        if direction == "formalize":
            return (
                "Solve the problem directly by restating it as a precise mathematical target, then carry out only the deductions or calculations needed for the final answer."
            )
        if direction == "compress":
            return (
                "Solve the problem directly with a shorter, tighter reasoning chain that still preserves the exact target and final answer format."
            )
        return (
            "Solve the problem directly, keep attention on the core mathematical step, and avoid wandering into side explanations that do not change the final answer."
        )

    if family == "delegate":
        if direction == "feasibility_checks":
            return (
                "Decompose the problem into helper tasks that directly test small answer possibilities, rule out impossible cases, "
                "and compute the first viable case. Make each helper responsible for one concrete mathematical check."
            )
        if direction == "formalize":
            return (
                "Break the problem into a small set of precise mathematical subproblems with explicit goals, so the parent can combine "
                "the results into a final proof or computation."
            )
        if direction == "compress":
            return (
                "Keep the same decomposition structure, but make each helper instruction shorter and more concrete so the helpers focus on the exact subproblem."
            )
        return (
            "Decompose the problem into a few genuinely useful subproblems that expose the key mathematical checks needed for the final answer."
        )

    if family == "review":
        if direction == "feasibility_checks":
            return (
                "Write a draft answer and send one reviewer child a focused request to test the weakest assumptions, check small candidate cases, and correct the draft if needed."
            )
        if direction == "formalize":
            return (
                "Write a compact draft answer, then send one reviewer child a precise critique request that checks the logic, the exact target, and the final answer format before you finalize."
            )
        if direction == "compress":
            return (
                "Keep the same draft-and-review structure, but make the review request shorter and more targeted so the child focuses on the highest-risk part of the draft."
            )
        return (
            "Write a tentative answer and ask one reviewer child to poke holes in it, verify the reasoning, and improve any weak step before the final response is produced."
        )

    if direction == "feasibility_checks":
        return (
            "Rewrite the problem so the next agent first checks whether the smallest candidate answer values are even possible, using modular arithmetic or direct contradiction before searching more broadly."
        )
    if direction == "formalize":
        return (
            "Rewrite the problem into a precise, high-density mathematical statement that highlights the exact constraints and the key theorem or computation the next agent should use."
        )
    if direction == "compress":
        return (
            "Keep the same overall reframing, but compress it into fewer words while preserving the exact mathematical target and critical constraints."
        )
    return (
        "Simplify the question into its essential parts, keep the exact objective intact, and remove any wording that could distract the next agent from the main reasoning step."
    )


def _build_openrouter_tutor(
    *,
    manifest: dict[str, Any],
    grading_record: dict[str, Any],
    current_attempt: dict[str, Any],
    prior_attempts: list[dict[str, Any]],
    tutor_model: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    api_key = load_openrouter_api_key()
    if not api_key:
        raise MX1TutorError("OPENROUTER_API_KEY was not found for MX1 tutor.")

    client = OpenRouterChatClient(OpenRouterClientConfig(api_key=api_key, title="Super-Eywa MX1 Tutor"))
    prompt = build_tutor_prompt(
        manifest=manifest,
        grading_record=grading_record,
        current_attempt=current_attempt,
        prior_attempts=prior_attempts,
    )
    expected_shape = {
        "correctness_assessment": "incorrect",
        "assessment": {
            "score_direction": "better",
            "token_direction": "worse",
            "time_direction": "same",
            "summary": "string",
        },
        "what_helped": ["string"],
        "what_hurt": ["string"],
        "recommendation": {
            "action": "keep",
            "reason": "string",
            "new_prompt_text": "string",
        },
        "history_observations": ["string"],
        "confidence": "medium",
    }
    request_messages = [
        {
            "role": "system",
            "content": (
                "You are the MX1 prompt tutor for Super-Eywa. "
                "Return only valid JSON and do not use markdown fences."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Return exactly one JSON object matching this shape:\n{json.dumps(expected_shape, indent=2)}\n\n"
                f"{prompt}"
            ),
        },
    ]
    try:
        response = client.create_chat_completion(
            model=tutor_model,
            messages=request_messages,
            max_tokens=1200,
            temperature=0.2,
        )
    except OpenRouterClientError as exc:
        tutor, fallback_payload = _build_deterministic_tutor(
            manifest=manifest,
            grading_record=grading_record,
            current_attempt=current_attempt,
            prior_attempts=prior_attempts,
        )
        return tutor, {
            "provider": "openrouter",
            "request": request_messages,
            "response": None,
            "repair_response": None,
            "parse_error": str(exc),
            "fallback_provider_payload": fallback_payload,
            "fallback_reason": "openrouter_request_failed",
        }
    choice = dict(response.get("choices", [{}])[0])
    message = dict(choice.get("message") or {})
    content = str(message.get("content") or "")
    repair_response = None
    repair_parse_error = None
    try:
        tutor = _parse_json_or_repair(content)
    except MX1TutorError as exc:
        repair_parse_error = str(exc)
        try:
            repair_response = _repair_tutor_json(
                client=client,
                tutor_model=tutor_model,
                expected_shape=expected_shape,
                original_content=content,
            )
        except OpenRouterClientError as repair_exc:
            tutor, fallback_payload = _build_deterministic_tutor(
                manifest=manifest,
                grading_record=grading_record,
                current_attempt=current_attempt,
                prior_attempts=prior_attempts,
            )
            return tutor, {
                "provider": "openrouter",
                "request": request_messages,
                "response": response,
                "repair_response": None,
                "parse_error": repair_parse_error,
                "repair_parse_error": str(repair_exc),
                "fallback_provider_payload": fallback_payload,
                "fallback_reason": "repair_request_failed",
            }
        repair_choice = dict(repair_response.get("choices", [{}])[0])
        repair_message = dict(repair_choice.get("message") or {})
        repair_content = str(repair_message.get("content") or "")
        try:
            tutor = _parse_json_or_repair(repair_content)
        except MX1TutorError as repair_exc:
            tutor, fallback_payload = _build_deterministic_tutor(
                manifest=manifest,
                grading_record=grading_record,
                current_attempt=current_attempt,
                prior_attempts=prior_attempts,
            )
            return tutor, {
                "provider": "openrouter",
                "request": request_messages,
                "response": response,
                "repair_response": repair_response,
                "parse_error": repair_parse_error,
                "repair_parse_error": str(repair_exc),
                "fallback_provider_payload": fallback_payload,
                "fallback_reason": "repair_response_could_not_be_parsed",
            }
    return tutor, {
        "provider": "openrouter",
        "request": request_messages,
        "response": response,
        "repair_response": repair_response,
        "parse_error": repair_parse_error,
    }


def _parse_json_or_repair(content: str) -> dict[str, Any]:
    text = content.strip()
    if not text:
        raise MX1TutorError("Tutor response was empty.")
    for candidate in _json_parse_candidates(text):
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            continue
    raise MX1TutorError("Tutor response could not be parsed as JSON.")


def _json_parse_candidates(text: str) -> list[str]:
    candidates = [text]
    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        candidates.append(text[start : end + 1])
    sanitized = [_escape_invalid_json_backslashes(candidate) for candidate in candidates]
    ordered: list[str] = []
    for candidate in candidates + sanitized:
        if candidate not in ordered:
            ordered.append(candidate)
    return ordered


def _escape_invalid_json_backslashes(text: str) -> str:
    return re.sub(r'\\(?!["\\/bfnrt]|u[0-9a-fA-F]{4})', r"\\\\", text)


def _repair_tutor_json(
    *,
    client: OpenRouterChatClient,
    tutor_model: str,
    expected_shape: dict[str, Any],
    original_content: str,
) -> dict[str, Any]:
    return client.create_chat_completion(
        model=tutor_model,
        messages=[
            {
                "role": "system",
                "content": "You repair invalid MX1 tutor responses into strict JSON. Return only valid JSON.",
            },
            {
                "role": "user",
                "content": (
                    f"Rewrite the following content as valid JSON only. It must match this shape exactly:\n"
                    f"{json.dumps(expected_shape, indent=2)}\n\n"
                    "Return one JSON object only. Do not use markdown fences.\n\n"
                    f"Original content:\n{original_content}"
                ),
            },
        ],
        max_tokens=1200,
        temperature=0.2,
    )


def _latest_attempt(manifest: dict[str, Any]) -> dict[str, Any]:
    attempts = list(manifest.get("attempts") or [])
    if not attempts:
        raise MX1TutorError("The loop manifest has no attempts.")
    return sorted(attempts, key=lambda item: (int(item.get("iteration_index") or 0), str(item.get("kind") or ""))) [-1]


def _best_before(prior_attempts: list[dict[str, Any]]) -> dict[str, Any] | None:
    scored = [attempt for attempt in prior_attempts if attempt.get("score") is not None]
    if not scored:
        return None
    return sorted(
        scored,
        key=lambda item: (
            float(item.get("score") or 0.0),
            -float(item.get("total_tokens") or 0.0),
            -float(item.get("total_wall_time_ms") or 0.0),
        ),
        reverse=True,
    )[0]


def _direction(current: float, previous: float | None) -> str:
    if previous is None:
        return "same"
    if current > previous:
        return "better"
    if current < previous:
        return "worse"
    return "same"


def _direction_decrease(previous: float | None, current: float) -> str:
    if previous is None:
        return "same"
    if current < previous:
        return "better"
    if current > previous:
        return "worse"
    return "same"


def _build_summary(current_score: float, best_before_score: float | None, plateau_streak: int) -> str:
    if best_before_score is None:
        return "This is the first scored attempt in the loop history."
    if current_score > best_before_score:
        return "The current attempt improved score relative to earlier history."
    if current_score < best_before_score:
        return "The current attempt regressed on score relative to earlier history."
    if plateau_streak >= 2:
        return "The loop is plateauing on efficiency and should try a different prompt direction."
    return "The current attempt is not yet clearly better than earlier attempts."


def _history_observations(manifest: dict[str, Any], prior_attempts: list[dict[str, Any]]) -> list[str]:
    family = str(manifest.get("family") or "unknown").strip()
    observations = [
        f"iterations_completed={len([attempt for attempt in manifest.get('attempts') or [] if attempt.get('kind') == family])}",
        f"exploration_iterations={manifest.get('exploration_iterations')}",
    ]
    if prior_attempts:
        observations.append(f"prior_attempts_seen={len(prior_attempts)}")
    if manifest.get("history_summary", {}).get("needs_new_direction"):
        observations.append("the loop has plateaued enough to justify a new direction")
    return observations


def looks_question_specific(prompt_text: str) -> bool:
    text = str(prompt_text or "").strip()
    if not text:
        return False
    lowered = text.lower()
    if any(marker in lowered for marker in ("problem:", "original problem:", "subproblem 1:", "subproblem 2:")):
        return True
    if re.search(
        r"\b(?:split|break|decompose)\b.*\b(?:into|to|at most)\s+(?:\d+|one|two|three|four|five)\b",
        lowered,
    ):
        return True
    if re.search(
        r"\b(?:\d+|one|two|three|four|five)\s+(?:helpers?|parts?|subproblems?)\b",
        lowered,
    ):
        return True
    return False


def _compact_attempt(attempt: dict[str, Any]) -> dict[str, Any]:
    return {
        "iteration_index": attempt.get("iteration_index"),
        "kind": attempt.get("kind"),
        "run_id": attempt.get("run_id"),
        "score": attempt.get("score"),
        "correct": attempt.get("correct"),
        "total_tokens": attempt.get("total_tokens"),
        "total_wall_time_ms": attempt.get("total_wall_time_ms"),
        "total_cost_usd": attempt.get("total_cost_usd"),
        "prompt_text": attempt.get("prompt_text"),
        "prompt_file": attempt.get("prompt_file"),
        "is_best": attempt.get("is_best"),
        "root_orchestration": attempt.get("root_orchestration"),
        "root_result_excerpt": attempt.get("root_result_excerpt"),
        "final_result_excerpt": attempt.get("final_result_excerpt"),
    }

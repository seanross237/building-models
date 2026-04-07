"""Agent-based grading helpers for Super-Eywa v1."""

from __future__ import annotations

import ast
import json
from pathlib import Path
import re
import sys
from typing import Any


THIS_DIR = Path(__file__).resolve().parent
GRADING_DIR = THIS_DIR.parent
RUNTIME_DIR = GRADING_DIR.parents[1] / "eywa-system" / "runtime"
if str(GRADING_DIR) not in sys.path:
    sys.path.insert(0, str(GRADING_DIR))
if str(RUNTIME_DIR) not in sys.path:
    sys.path.insert(0, str(RUNTIME_DIR))

from eywa_runtime.openrouter_client import OpenRouterChatClient, OpenRouterClientConfig, OpenRouterClientError  # noqa: E402
from eywa_runtime.secrets import load_openrouter_api_key  # noqa: E402
from grading_methods.coding_grade_v1 import maybe_grade_coding_submission  # noqa: E402
from grading_methods.simple_grade_v1 import grade_result as reference_grade_result  # noqa: E402
from question_bank_v1 import QuestionCase  # noqa: E402


AGENT_GRADING_SCHEMA_NAME = "eywa_agent_grading"
AGENT_GRADING_SCHEMA_VERSION = "v1"


class AgentGradeError(ValueError):
    """Raised when the agent grader cannot produce a usable result."""


REPAIRABLE_CODING_MARKERS = (
    "out of range",
    "unexpected eof",
    "too many outputs",
    "invalid output",
    "parse failed",
    "failed to parse",
)


def grade_result(
    question_case: QuestionCase,
    result_text: str,
    *,
    grading_provider: str,
    grading_model: str,
    run_dir: Path | None = None,
    final_output: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    provider = str(grading_provider or "").strip()
    model = str(grading_model or "").strip()
    coding_grade = maybe_grade_coding_submission(
        question_case,
        run_dir=run_dir,
        final_output=final_output,
        result_text=result_text,
    )
    if coding_grade is not None:
        grading, trace = coding_grade
        repaired = _maybe_repair_coding_submission(
            question_case=question_case,
            grading=grading,
            trace=trace,
            grading_provider=provider,
            grading_model=model,
            run_dir=run_dir,
        )
        if repaired is not None:
            return repaired
        return grading, trace

    if provider == "deterministic":
        grading = _grade_with_reference(question_case, result_text)
        return grading, {
            "provider": "deterministic",
            "model": model or "deterministic-agent-grader-v1",
            "request": None,
            "response": {"content": json.dumps(grading, indent=2)},
            "repair_response": None,
            "parse_error": None,
            "fallback_reason": "deterministic_reference_grader",
        }
    if provider != "openrouter":
        raise AgentGradeError(f"Unsupported grading_provider: {provider}")
    return _grade_with_openrouter(question_case, result_text, grading_model=model)


def _maybe_repair_coding_submission(
    *,
    question_case: QuestionCase,
    grading: dict[str, Any],
    trace: dict[str, Any],
    grading_provider: str,
    grading_model: str,
    run_dir: Path | None,
) -> tuple[dict[str, Any], dict[str, Any]] | None:
    if grading_provider != "openrouter" or run_dir is None:
        return None
    if not _should_attempt_coding_repair(grading=grading, trace=trace):
        return None

    api_key = load_openrouter_api_key()
    if not api_key:
        return None

    submission_info = dict(trace.get("submission") or {})
    submission_path_text = str(submission_info.get("submission_path") or "").strip()
    if not submission_path_text:
        return None
    submission_path = Path(submission_path_text)
    if not submission_path.exists():
        return None

    current_code = submission_path.read_text(encoding="utf-8")
    client = OpenRouterChatClient(OpenRouterClientConfig(api_key=api_key, title="Super-Eywa Coding Repair"))
    repair_attempts: list[dict[str, Any]] = []

    for attempt_index in range(1, 3):
        repair_response = client.create_chat_completion(
            model=grading_model,
            messages=_build_coding_repair_messages(
                question_case=question_case,
                current_code=current_code,
                trace=trace,
                attempt_index=attempt_index,
            ),
            max_tokens=4000,
            temperature=0.1,
        )
        repair_choice = dict(repair_response.get("choices", [{}])[0])
        repair_message = dict(repair_choice.get("message") or {})
        repair_content = str(repair_message.get("content") or "")
        repaired_code = _extract_python_repair_candidate(repair_content)
        attempt_record: dict[str, Any] = {
            "attempt_index": attempt_index,
            "response": repair_response,
            "extracted_code": repaired_code is not None,
        }
        if repaired_code is None:
            repair_attempts.append(attempt_record)
            continue

        repaired_ref, repaired_path = _write_repaired_submission(
            run_dir=run_dir,
            question_id=question_case.question_id,
            attempt_index=attempt_index,
            code_text=repaired_code,
        )
        attempt_record["artifact_ref"] = repaired_ref
        attempt_record["submission_path"] = str(repaired_path)
        repair_attempts.append(attempt_record)

        repaired_grade = maybe_grade_coding_submission(
            question_case,
            run_dir=run_dir,
            final_output={"result": {"attachment_refs": [repaired_ref]}},
            result_text="",
        )
        if repaired_grade is None:
            continue
        repaired_grading, repaired_trace = repaired_grade
        if _should_attempt_coding_repair(grading=repaired_grading, trace=repaired_trace):
            current_code = repaired_code
            continue

        repaired_trace = dict(repaired_trace)
        repaired_trace["repair_attempts"] = repair_attempts
        repaired_trace["repaired_from_invalid_output"] = True
        repaired_trace["original_coding_trace"] = trace
        return repaired_grading, repaired_trace

    trace = dict(trace)
    trace["repair_attempts"] = repair_attempts
    trace["repaired_from_invalid_output"] = False
    return None


def _should_attempt_coding_repair(*, grading: dict[str, Any], trace: dict[str, Any]) -> bool:
    if grading.get("grading_status") != "graded":
        return False
    if float(grading.get("task_score") or 0.0) != 0.0:
        return False
    execution = dict(trace.get("execution") or {})
    instances = list(execution.get("instance_results") or [])
    if not instances:
        return False
    for instance in instances:
        scorer_payload = dict(instance.get("scorer_payload") or {})
        text = " ".join(
            [
                str(scorer_payload.get("stdout") or ""),
                str(scorer_payload.get("stderr") or ""),
                str(scorer_payload.get("notes") or ""),
                str(instance.get("scorer_notes") or ""),
            ]
        ).lower()
        if any(marker in text for marker in REPAIRABLE_CODING_MARKERS):
            return True
    return False


def _build_coding_repair_messages(
    *,
    question_case: QuestionCase,
    current_code: str,
    trace: dict[str, Any],
    attempt_index: int,
) -> list[dict[str, str]]:
    feedback_lines = []
    execution = dict(trace.get("execution") or {})
    for instance in list(execution.get("instance_results") or [])[:3]:
        scorer_payload = dict(instance.get("scorer_payload") or {})
        feedback_lines.append(
            "\n".join(
                [
                    f"Instance: {instance.get('name')}",
                    f"Scorer stdout: {str(scorer_payload.get('stdout') or '').strip()}",
                    f"Scorer stderr: {str(scorer_payload.get('stderr') or '').strip()}",
                    f"Candidate stdout head: {str(instance.get('stdout') or '')[:400]}",
                ]
            ).strip()
        )
    repair_shape = {
        "main_py": "full Python file contents as one escaped string",
        "notes": "brief repair summary",
    }
    return [
        {
            "role": "system",
            "content": (
                "You are repairing a Python contest submission. "
                "Return a corrected main.py that produces valid contestant output. "
                "Prefer a simple valid baseline solution over an ambitious invalid one. "
                "Return only valid JSON. Do not use markdown fences."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Attempt {attempt_index}. Return exactly one JSON object in this shape:\n"
                f"{json.dumps(repair_shape, indent=2)}\n\n"
                f"Question ID: {question_case.question_id}\n"
                f"Title: {question_case.title}\n\n"
                f"Problem:\n{question_case.sections.get('problem') or ''}\n\n"
                "Repair goal:\n"
                "- Fix invalid contestant output.\n"
                "- Print exactly the required Output format and nothing else.\n"
                "- Do not print the objective score unless the Output section explicitly requires it.\n"
                "- If the task allows a trivial valid baseline output, use it instead of risking malformed output.\n\n"
                f"Current main.py:\n{current_code}\n\n"
                f"Official scorer feedback:\n{chr(10).join(feedback_lines)}"
            ),
        },
    ]


def _extract_python_repair_candidate(content: str) -> str | None:
    text = str(content or "").strip()
    if not text:
        return None
    try:
        parsed = _parse_json_or_repair(text)
        if isinstance(parsed, dict):
            candidate = str(parsed.get("main_py") or "").strip()
            if candidate:
                try:
                    ast.parse(candidate)
                except SyntaxError:
                    candidate = ""
            if candidate:
                return candidate
    except AgentGradeError:
        pass

    fence_match = re.search(r"```(?:python|py)?\s*\n(?P<code>[\s\S]*?)```", text, flags=re.IGNORECASE)
    if fence_match:
        candidate = str(fence_match.group("code") or "").strip()
        try:
            ast.parse(candidate)
        except SyntaxError:
            candidate = ""
        if candidate:
            return candidate

    try:
        ast.parse(text)
    except SyntaxError:
        return None
    return text


def _write_repaired_submission(
    *,
    run_dir: Path,
    question_id: str,
    attempt_index: int,
    code_text: str,
) -> tuple[str, Path]:
    repaired_dir = run_dir / "grading-artifacts" / question_id / "repair-attempts" / f"attempt_{attempt_index:02d}"
    repaired_dir.mkdir(parents=True, exist_ok=True)
    repaired_path = repaired_dir / "main.py"
    repaired_path.write_text(code_text.rstrip() + "\n", encoding="utf-8")
    return str(repaired_path.relative_to(run_dir)), repaired_path


def _grade_with_reference(question_case: QuestionCase, result_text: str) -> dict[str, Any]:
    grading = dict(reference_grade_result(question_case, result_text))
    grading.setdefault("normalized_answer", None)
    grading["grading_method"] = "deterministic_reference_v1"
    grading["confidence"] = "high" if grading.get("grading_status") == "graded" else "low"
    return grading


def _grade_with_openrouter(
    question_case: QuestionCase,
    result_text: str,
    *,
    grading_model: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    api_key = load_openrouter_api_key()
    if not api_key:
        raise AgentGradeError("OPENROUTER_API_KEY was not found for agent grading.")

    authoritative_reference = _build_authoritative_reference(question_case)
    expected_shape = {
        "grading_status": "graded",
        "correct": False,
        "score": 0.0,
        "expected": authoritative_reference.get("expected"),
        "extracted_answer": "string",
        "normalized_answer": "string or null",
        "grading_notes": "string",
        "confidence": "medium",
    }
    request_messages = [
        {
            "role": "system",
            "content": (
                "You are the grading agent for Super-Eywa benchmark questions. "
                "Judge whether the submitted answer should count as correct under the authoritative benchmark reference. "
                "Be tolerant of harmless formatting differences, extra prose, punctuation, and equivalent surface forms. "
                "If the benchmark lacks enough authoritative information or requires execution/hidden tests you cannot perform, "
                "set grading_status to 'ungraded' and set correct and score to null. "
                "Return only valid JSON. Do not use markdown fences."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Return exactly one JSON object matching this shape:\n{json.dumps(expected_shape, indent=2)}\n\n"
                f"{build_grading_prompt(question_case, result_text, authoritative_reference)}"
            ),
        },
    ]

    client = OpenRouterChatClient(OpenRouterClientConfig(api_key=api_key, title="Super-Eywa Agent Grader"))
    response = client.create_chat_completion(
        model=grading_model,
        messages=request_messages,
        max_tokens=1200,
        temperature=0.1,
    )
    choice = dict(response.get("choices", [{}])[0])
    message = dict(choice.get("message") or {})
    content = str(message.get("content") or "")

    repair_response = None
    parse_error = None
    fallback_reason = None
    try:
        grading = _parse_json_or_repair(content)
    except AgentGradeError as exc:
        parse_error = str(exc)
        repair_response = _repair_grading_json(
            client=client,
            grading_model=grading_model,
            expected_shape=expected_shape,
            original_content=content,
        )
        repair_choice = dict(repair_response.get("choices", [{}])[0])
        repair_message = dict(repair_choice.get("message") or {})
        repair_content = str(repair_message.get("content") or "")
        try:
            grading = _parse_json_or_repair(repair_content)
        except AgentGradeError as repair_exc:
            grading = _ungraded_fallback(
                question_case=question_case,
                result_text=result_text,
                authoritative_reference=authoritative_reference,
                note=(
                    "Agent grader response was not valid JSON after repair. "
                    f"Initial parse error: {parse_error}. Repair parse error: {repair_exc}."
                ),
            )
            fallback_reason = "repair_response_could_not_be_parsed"

    grading = _normalize_grading_payload(
        grading=grading,
        question_case=question_case,
        authoritative_reference=authoritative_reference,
        result_text=result_text,
    )
    return grading, {
        "provider": "openrouter",
        "model": grading_model,
        "request": request_messages,
        "response": response,
        "repair_response": repair_response,
        "parse_error": parse_error,
        "fallback_reason": fallback_reason,
    }


def build_grading_prompt(
    question_case: QuestionCase,
    result_text: str,
    authoritative_reference: dict[str, Any],
) -> str:
    return (
        f"Question ID: {question_case.question_id}\n"
        f"Title: {question_case.title}\n"
        f"Family: {question_case.family}\n"
        f"Entry type: {question_case.entry_type}\n"
        f"Grader type hint: {question_case.grader_type}\n"
        f"Grader config hint:\n{json.dumps(question_case.grader_config or {}, indent=2)}\n\n"
        f"Problem:\n{question_case.sections.get('problem') or ''}\n\n"
        f"Grading target:\n{question_case.sections.get('grading') or ''}\n\n"
        f"Authoritative reference:\n{json.dumps(authoritative_reference, indent=2)}\n\n"
        "Submitted final result text:\n"
        f"{result_text}\n\n"
        "Judge whether the submitted answer should count as correct. "
        "Do not penalize harmless formatting or extra explanation if the actual answer is clearly right. "
        "If the answer is wrong or the benchmark is not gradeable from the reference above, say so."
    )


def _build_authoritative_reference(question_case: QuestionCase) -> dict[str, Any]:
    correct_answer = str(question_case.sections.get("correct_answer") or "").strip()
    grader_config = dict(question_case.grader_config or {})
    expected = grader_config.get("expected")
    if expected is None and correct_answer:
        expected = correct_answer
    return {
        "correct_answer": correct_answer or None,
        "expected": expected,
        "grader_type": question_case.grader_type,
        "grader_config": grader_config,
        "grading_target": str(question_case.sections.get("grading") or "").strip() or None,
        "has_authoritative_reference": bool(correct_answer or expected is not None),
        "requires_external_execution": question_case.grader_type in {"continuous_score", "binary_hidden_tests"},
    }


def _normalize_grading_payload(
    *,
    grading: dict[str, Any],
    question_case: QuestionCase,
    authoritative_reference: dict[str, Any],
    result_text: str,
) -> dict[str, Any]:
    normalized = dict(grading)
    normalized["grading_method"] = "agent_v1"
    normalized.setdefault("grading_status", "ungraded")
    normalized.setdefault("correct", None)
    normalized.setdefault("score", None)
    normalized.setdefault("expected", authoritative_reference.get("expected"))
    normalized.setdefault("extracted_answer", _extract_first_answer_line(result_text))
    normalized.setdefault("normalized_answer", None)
    normalized.setdefault("grading_notes", "")
    normalized.setdefault("confidence", "low")

    status = str(normalized.get("grading_status") or "ungraded").strip().lower()
    if status not in {"graded", "ungraded"}:
        status = "ungraded"
    normalized["grading_status"] = status

    if status == "ungraded":
        normalized["correct"] = None
        normalized["score"] = None
        return normalized

    correct = normalized.get("correct")
    if isinstance(correct, str):
        lowered = correct.strip().lower()
        if lowered in {"true", "yes"}:
            correct = True
        elif lowered in {"false", "no"}:
            correct = False
        else:
            correct = None
    normalized["correct"] = bool(correct) if correct is not None else None
    if normalized["correct"] is None:
        normalized["grading_status"] = "ungraded"
        normalized["score"] = None
        return normalized

    normalized["score"] = 1.0 if normalized["correct"] else 0.0
    if normalized.get("expected") is None:
        normalized["expected"] = authoritative_reference.get("expected")
    return normalized


def _ungraded_fallback(
    *,
    question_case: QuestionCase,
    result_text: str,
    authoritative_reference: dict[str, Any],
    note: str,
) -> dict[str, Any]:
    return {
        "grading_status": "ungraded",
        "correct": None,
        "score": None,
        "expected": authoritative_reference.get("expected"),
        "extracted_answer": _extract_first_answer_line(result_text),
        "normalized_answer": None,
        "grading_notes": note,
        "confidence": "low",
        "grading_method": "agent_v1",
    }


def _extract_first_answer_line(result_text: str) -> str:
    for line in result_text.splitlines():
        stripped = line.strip()
        if stripped.upper().startswith("FINAL_ANSWER:"):
            return stripped.split(":", 1)[1].strip()
    return next((line.strip() for line in result_text.splitlines() if line.strip()), "")


def _parse_json_or_repair(content: str) -> dict[str, Any]:
    text = content.strip()
    if not text:
        raise AgentGradeError("Agent grader response was empty.")
    for candidate in _json_parse_candidates(text):
        try:
            parsed = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            return parsed
    raise AgentGradeError("Agent grader response could not be parsed as JSON.")


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


def _repair_grading_json(
    *,
    client: OpenRouterChatClient,
    grading_model: str,
    expected_shape: dict[str, Any],
    original_content: str,
) -> dict[str, Any]:
    return client.create_chat_completion(
        model=grading_model,
        messages=[
            {
                "role": "system",
                "content": "You repair invalid grading-agent output into strict JSON. Return only valid JSON.",
            },
            {
                "role": "user",
                "content": (
                    "Rewrite the following content as valid JSON only. "
                    f"It must match this shape exactly:\n{json.dumps(expected_shape, indent=2)}\n\n"
                    "Return one JSON object only. Do not use markdown fences.\n\n"
                    f"Original content:\n{original_content}"
                ),
            },
        ],
        max_tokens=1200,
        temperature=0.1,
    )

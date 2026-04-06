"""Post-run reviewer for grading-bank runs."""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any, Dict, Iterable, List


THIS_DIR = Path(__file__).resolve().parent
RUNTIME_DIR = THIS_DIR.parents[1] / "eywa-system" / "runtime"
if str(RUNTIME_DIR) not in sys.path:
    sys.path.insert(0, str(RUNTIME_DIR))

from eywa_runtime.openrouter_client import OpenRouterChatClient, OpenRouterClientConfig, OpenRouterClientError  # noqa: E402
from eywa_runtime.secrets import load_openrouter_api_key  # noqa: E402


REVIEW_SCHEMA_NAME = "eywa_run_review"
REVIEW_SCHEMA_VERSION = "v1"
ALLOWED_ASSESSMENTS = {"correct", "incorrect", "ungraded"}
ALLOWED_ACTIONS = {"keep", "adjust", "investigate"}
ALLOWED_CONFIDENCE = {"low", "medium", "high"}


class ReviewError(ValueError):
    """Raised when a reviewer response is missing or invalid."""


def review_grading_record(
    *,
    question_id: str,
    title: str,
    question_file: str,
    label: str,
    run_id: str,
    run_dir: str,
    runtime_provider: str,
    model: str,
    task_text: str,
    root_result_excerpt: str,
    grading: Dict[str, Any],
    root_variables: Dict[str, Any],
    root_orchestration: Dict[str, Any],
    reviews_root: Path,
    reviewer_provider: str,
    reviewer_model: str,
) -> Dict[str, Any]:
    reviewer_provider = str(reviewer_provider or runtime_provider or "deterministic").strip()
    reviewer_model = str(reviewer_model or model or "deterministic-reviewer-v1").strip()

    if reviewer_provider == "deterministic":
        review = _build_deterministic_review(
            question_id=question_id,
            grading=grading,
            root_variables=root_variables,
            root_orchestration=root_orchestration,
        )
        provider_payload = {
            "provider": "deterministic",
            "request": None,
            "response": {"content": json.dumps(review, indent=2)},
            "parse_error": None,
        }
    elif reviewer_provider == "openrouter":
        review, provider_payload = _build_openrouter_review(
            question_id=question_id,
            title=title,
            question_file=question_file,
            label=label,
            run_id=run_id,
            task_text=task_text,
            root_result_excerpt=root_result_excerpt,
            grading=grading,
            root_variables=root_variables,
            root_orchestration=root_orchestration,
            reviewer_model=reviewer_model,
        )
    else:
        raise ReviewError(f"Unsupported reviewer_provider: {reviewer_provider}")

    review_record = {
        "schema_name": REVIEW_SCHEMA_NAME,
        "schema_version": REVIEW_SCHEMA_VERSION,
        "question_id": question_id,
        "title": title,
        "question_file": question_file,
        "label": label,
        "run_id": run_id,
        "run_dir": run_dir,
        "runtime_provider": runtime_provider,
        "model": model,
        "reviewer_provider": reviewer_provider,
        "reviewer_model": reviewer_model,
        "authoritative_grading": grading,
        "root_variables": root_variables,
        "root_orchestration": root_orchestration,
        "review": review,
        "provider_payload": provider_payload,
    }

    question_review_dir = reviews_root / question_id
    question_review_dir.mkdir(parents=True, exist_ok=True)
    review_record_path = question_review_dir / f"{label}__{run_id}.json"
    review_record["review_record_path"] = str(review_record_path)
    review_record_path.write_text(json.dumps(review_record, indent=2), encoding="utf-8")
    return review_record


def _build_deterministic_review(
    *,
    question_id: str,
    grading: Dict[str, Any],
    root_variables: Dict[str, Any],
    root_orchestration: Dict[str, Any],
) -> Dict[str, Any]:
    grading_status = str(grading.get("grading_status") or "ungraded")
    correct = grading.get("correct")
    expected = grading.get("expected")
    extracted = str(grading.get("extracted_answer") or "")
    prompt_family = str(root_variables.get("prompt_family") or "")
    review_prompt_family = str(root_variables.get("review_prompt_family") or "")

    if grading_status != "graded" or correct is None:
        assessment = "ungraded"
        summary = "The run completed, but the current grading system could not score this benchmark automatically."
        what_worked = [
            f"The run preserved enough metadata to analyze variables and orchestration for {question_id}.",
        ]
        what_failed = [
            "Correctness is not machine-verified here because this benchmark does not yet have an implemented scorer.",
        ]
        recommendations = [
            {
                "target": "grading_harness",
                "action": "investigate",
                "suggested_change": "Add an executable scorer or rubric-backed harness for this benchmark.",
                "reason": "Without an implemented grader, prompt iteration cannot be measured reliably.",
            }
        ]
        confidence = "medium"
    elif correct is True:
        assessment = "correct"
        summary = "The run got the benchmark answer right under the current grader."
        what_worked = [
            f"The extracted answer matched the grader expectation ({expected}).",
            f"The selected orchestration path ended with {root_orchestration.get('final_decision')}, which was sufficient here.",
        ]
        what_failed = []
        recommendations = [
            {
                "target": prompt_family or "prompt_family",
                "action": "keep",
                "suggested_change": prompt_family or "current setup",
                "reason": "This configuration produced a correct graded result.",
            }
        ]
        confidence = "high"
    else:
        assessment = "incorrect"
        summary = "The run was scored incorrect under the current grader."
        what_worked = [
            f"The runtime completed and exposed the full variable/orchestration trace for {question_id}.",
        ]
        what_failed = [
            f"The extracted answer was {extracted or '(empty)'} but the grader expected {expected}.",
        ]
        recommendations = [
            {
                "target": "selected_prompt_text",
                "action": "adjust",
                "suggested_change": "Tighten the task framing so the answering node is guided toward the benchmark's exact output requirement.",
                "reason": "The current prompt setup did not produce the expected graded answer.",
            }
        ]
        if prompt_family == "transmute":
            recommendations.append(
                {
                    "target": "review_selected_prompt_text" if review_prompt_family else "review_prompt_family",
                    "action": "adjust",
                    "suggested_change": "Make the review-turn execute prompt explicitly verify the child answer against the task requirements.",
                    "reason": "The transmute flow completed structurally but still missed the final graded answer.",
                }
            )
        else:
            recommendations.append(
                {
                    "target": "verification_policy",
                    "action": "adjust",
                    "suggested_change": "Use a stricter verification step for exact-answer tasks.",
                    "reason": "The current local execution path produced a wrong final answer.",
                }
            )
        confidence = "high"

    variable_observations = [
        f"prompt_family={prompt_family or 'n/a'}",
        f"review_prompt_family={review_prompt_family or 'n/a'}",
        f"workflow_structure={root_variables.get('workflow_structure') or 'n/a'}",
        f"verification_policy={root_variables.get('verification_policy') or 'n/a'}",
        f"initial_decision={root_orchestration.get('initial_decision') or 'n/a'}",
        f"final_decision={root_orchestration.get('final_decision') or 'n/a'}",
    ]

    return {
        "correctness_assessment": assessment,
        "overall_summary": summary,
        "what_worked": what_worked,
        "where_it_failed": what_failed,
        "variable_observations": variable_observations,
        "recommendations": recommendations,
        "confidence": confidence,
    }


def _build_openrouter_review(
    *,
    question_id: str,
    title: str,
    question_file: str,
    label: str,
    run_id: str,
    task_text: str,
    root_result_excerpt: str,
    grading: Dict[str, Any],
    root_variables: Dict[str, Any],
    root_orchestration: Dict[str, Any],
    reviewer_model: str,
) -> tuple[Dict[str, Any], Dict[str, Any]]:
    api_key = load_openrouter_api_key()
    if not api_key:
        raise ReviewError("OPENROUTER_API_KEY was not found for reviewer.")

    client = OpenRouterChatClient(OpenRouterClientConfig(api_key=api_key, title="Super-Eywa Reviewer v1"))
    review_prompt = _build_review_prompt(
        question_id=question_id,
        title=title,
        question_file=question_file,
        label=label,
        run_id=run_id,
        task_text=task_text,
        root_result_excerpt=root_result_excerpt,
        grading=grading,
        root_variables=root_variables,
        root_orchestration=root_orchestration,
    )
    request_messages = [
        {
            "role": "system",
            "content": (
                "You review benchmark runs for Super-Eywa. "
                "Return only valid JSON. Do not use markdown fences."
            ),
        },
        {
            "role": "user",
            "content": review_prompt,
        },
    ]

    attempts: List[Dict[str, Any]] = []
    try:
        response = client.create_chat_completion(
            model=reviewer_model,
            messages=request_messages,
            max_tokens=900,
            temperature=0.2,
        )
    except OpenRouterClientError as exc:
        raise ReviewError(f"Reviewer request failed: {exc}") from exc

    content = _normalize_openrouter_content(response)
    attempts.append(
        {
            "phase": "initial_generation",
            "request": {"model": reviewer_model, "messages": request_messages},
            "response": response,
            "raw_content": content,
            "parse_error": None,
            "parsed_response": None,
        }
    )

    parsed_review, parse_error = _try_parse_review(content)
    attempts[-1]["parse_error"] = parse_error
    attempts[-1]["parsed_response"] = parsed_review

    if parsed_review is None:
        repair_messages = [
            {
                "role": "system",
                "content": "You repair invalid reviewer output into strict JSON only.",
            },
            {
                "role": "user",
                "content": (
                    "Rewrite the following content as valid JSON for the eywa_run_review review schema. "
                    "Return only JSON.\n\n"
                    f"Original content:\n{content}"
                ),
            },
        ]
        try:
            repaired = client.create_chat_completion(
                model=reviewer_model,
                messages=repair_messages,
                max_tokens=900,
                temperature=0.0,
            )
        except OpenRouterClientError as exc:
            raise ReviewError(f"Reviewer JSON repair failed: {exc}") from exc
        repaired_content = _normalize_openrouter_content(repaired)
        parsed_review, parse_error = _try_parse_review(repaired_content)
        attempts.append(
            {
                "phase": "json_repair",
                "request": {"model": reviewer_model, "messages": repair_messages},
                "response": repaired,
                "raw_content": repaired_content,
                "parse_error": parse_error,
                "parsed_response": parsed_review,
            }
        )

    if parsed_review is None:
        raise ReviewError(f"Reviewer returned invalid JSON: {parse_error}")

    return parsed_review, {
        "provider": "openrouter",
        "attempts": attempts,
    }


def _build_review_prompt(
    *,
    question_id: str,
    title: str,
    question_file: str,
    label: str,
    run_id: str,
    task_text: str,
    root_result_excerpt: str,
    grading: Dict[str, Any],
    root_variables: Dict[str, Any],
    root_orchestration: Dict[str, Any],
) -> str:
    expected_shape = {
        "correctness_assessment": "correct | incorrect | ungraded",
        "overall_summary": "string",
        "what_worked": ["string"],
        "where_it_failed": ["string"],
        "variable_observations": ["string"],
        "recommendations": [
            {
                "target": "string",
                "action": "keep | adjust | investigate",
                "suggested_change": "string",
                "reason": "string",
            }
        ],
        "confidence": "low | medium | high",
    }
    return (
        "Review this Super-Eywa benchmark run.\n"
        "The authoritative grading result below determines whether the run was correct, incorrect, or ungraded. "
        "Use that as ground truth when writing the review.\n\n"
        f"Return exactly one JSON object matching this shape:\n{json.dumps(expected_shape, indent=2)}\n\n"
        f"Question ID: {question_id}\n"
        f"Title: {title}\n"
        f"Question file: {question_file}\n"
        f"Run label: {label}\n"
        f"Run ID: {run_id}\n\n"
        f"Task text:\n{task_text}\n\n"
        f"Root result excerpt:\n{root_result_excerpt}\n\n"
        f"Authoritative grading:\n{json.dumps(grading, indent=2)}\n\n"
        f"Root variables:\n{json.dumps(root_variables, indent=2)}\n\n"
        f"Root orchestration:\n{json.dumps(root_orchestration, indent=2)}"
    )


def _normalize_openrouter_content(response: Dict[str, Any]) -> str:
    choices = list(response.get("choices") or [])
    if not choices:
        return ""
    message = dict(choices[0].get("message") or {})
    content = message.get("content")
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts: List[str] = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(str(item.get("text") or "").strip())
        return "\n".join(part for part in parts if part).strip()
    return ""


def _try_parse_review(raw_text: str) -> tuple[Dict[str, Any] | None, str | None]:
    try:
        payload = _parse_review_text(raw_text)
        normalized = _validate_review_payload(payload)
    except ReviewError as exc:
        return None, str(exc)
    return normalized, None


def _parse_review_text(raw_text: str) -> Dict[str, Any]:
    text = raw_text.strip()
    if not text:
        raise ReviewError("reviewer response was empty")

    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()

    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1 or start >= end:
            raise ReviewError("reviewer response was not valid JSON") from None
        try:
            payload = json.loads(text[start : end + 1])
        except json.JSONDecodeError as exc:
            raise ReviewError("reviewer response was not valid JSON") from exc
    if not isinstance(payload, dict):
        raise ReviewError("reviewer response must be a JSON object")
    return payload


def _validate_review_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    normalized = {
        "correctness_assessment": str(payload.get("correctness_assessment") or "").strip().lower(),
        "overall_summary": str(payload.get("overall_summary") or "").strip(),
        "what_worked": _normalize_string_list(payload.get("what_worked")),
        "where_it_failed": _normalize_string_list(payload.get("where_it_failed")),
        "variable_observations": _normalize_string_list(payload.get("variable_observations")),
        "recommendations": _normalize_recommendations(payload.get("recommendations")),
        "confidence": str(payload.get("confidence") or "").strip().lower(),
    }

    if normalized["correctness_assessment"] not in ALLOWED_ASSESSMENTS:
        raise ReviewError("reviewer correctness_assessment must be correct, incorrect, or ungraded")
    if not normalized["overall_summary"]:
        raise ReviewError("reviewer overall_summary must be a non-empty string")
    if normalized["confidence"] not in ALLOWED_CONFIDENCE:
        raise ReviewError("reviewer confidence must be low, medium, or high")
    return normalized


def _normalize_string_list(value: Any) -> List[str]:
    if not isinstance(value, list):
        raise ReviewError("reviewer list fields must be arrays of strings")
    normalized: List[str] = []
    for item in value:
        text = str(item or "").strip()
        if text:
            normalized.append(text)
    return normalized


def _normalize_recommendations(value: Any) -> List[Dict[str, str]]:
    if not isinstance(value, list):
        raise ReviewError("reviewer recommendations must be an array")
    normalized: List[Dict[str, str]] = []
    for item in value:
        if not isinstance(item, dict):
            raise ReviewError("each reviewer recommendation must be an object")
        target = str(item.get("target") or "").strip()
        action = str(item.get("action") or "").strip().lower()
        suggested_change = str(item.get("suggested_change") or "").strip()
        reason = str(item.get("reason") or "").strip()
        if not target:
            raise ReviewError("reviewer recommendation target must be non-empty")
        if action not in ALLOWED_ACTIONS:
            raise ReviewError("reviewer recommendation action must be keep, adjust, or investigate")
        if not suggested_change:
            raise ReviewError("reviewer recommendation suggested_change must be non-empty")
        if not reason:
            raise ReviewError("reviewer recommendation reason must be non-empty")
        normalized.append(
            {
                "target": target,
                "action": action,
                "suggested_change": suggested_change,
                "reason": reason,
            }
        )
    return normalized

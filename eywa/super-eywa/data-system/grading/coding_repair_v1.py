"""Bounded repair loop for coding submissions with invalid contestant output."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from typing import Any


THIS_DIR = Path(__file__).resolve().parent
RUNTIME_DIR = THIS_DIR.parents[1] / "eywa-system" / "runtime"
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))
if str(RUNTIME_DIR) not in sys.path:
    sys.path.insert(0, str(RUNTIME_DIR))

from coding_packets_v1 import load_coding_packet  # noqa: E402
from eywa_runtime.openrouter_client import OpenRouterChatClient, OpenRouterClientConfig, OpenRouterClientError  # noqa: E402
from eywa_runtime.secrets import load_openrouter_api_key  # noqa: E402
from grading_methods.coding_grade_v1 import grade_coding_submission_path  # noqa: E402
from question_bank_v1 import QuestionCase  # noqa: E402


PYTHON_FENCE_RE = re.compile(r"```(?:python|py)?\s*\n(?P<code>[\s\S]*?)```", flags=re.IGNORECASE)


def maybe_repair_invalid_coding_submission(
    *,
    question_case: QuestionCase,
    runtime_provider: str,
    model: str,
    run_dir: Path,
    grading: dict[str, Any],
    grading_trace: dict[str, Any],
    max_attempts: int = 2,
) -> tuple[dict[str, Any], dict[str, Any]] | None:
    if question_case.entry_type != "coding":
        return None
    if str(runtime_provider).strip() != "openrouter":
        return None
    if not _needs_repair(grading, grading_trace):
        return None

    packet = load_coding_packet(question_id=question_case.question_id, strict=False)
    if packet is None:
        return None
    current_code = _load_current_submission_code(grading_trace)
    seed_excerpt = ""
    has_recovered_code = bool(current_code)
    if not current_code:
        seed_excerpt = _load_raw_model_output_excerpt(run_dir)

    api_key = load_openrouter_api_key()
    if not api_key:
        raise OpenRouterClientError("OPENROUTER_API_KEY was not found for coding repair.")
    client = OpenRouterChatClient(OpenRouterClientConfig(api_key=api_key, title="Super-Eywa Coding Repair"))

    current_grading = grading
    current_trace = grading_trace
    attempts: list[dict[str, Any]] = []
    problem_text = packet.problem_statement_path.read_text(encoding="utf-8").strip()

    for attempt_index in range(1, max_attempts + 1):
        feedback = _build_repair_feedback(current_trace)
        request_messages = _build_repair_messages(
            question_case=question_case,
            problem_text=problem_text,
            current_code=current_code,
            seed_excerpt=seed_excerpt,
            has_recovered_code=has_recovered_code,
            feedback=feedback,
        )
        response = client.create_chat_completion(
            model=model,
            messages=request_messages,
            max_tokens=2400,
            temperature=0.1,
        )
        raw_content = _extract_response_content(response)
        repaired_code = _extract_python_code(raw_content)
        attempt_payload: dict[str, Any] = {
            "attempt_index": attempt_index,
            "request": request_messages,
            "response": response,
            "raw_content": raw_content,
        }
        if not repaired_code:
            attempt_payload["status"] = "no_repaired_code"
            attempts.append(attempt_payload)
            continue

        repair_dir = run_dir / "grading-artifacts" / question_case.question_id / "repair-attempts" / f"attempt_{attempt_index:02d}"
        repair_dir.mkdir(parents=True, exist_ok=True)
        submission_path = repair_dir / packet.entry_file
        submission_path.write_text(repaired_code.rstrip() + "\n", encoding="utf-8")
        artifact_ref = str(submission_path.relative_to(run_dir))
        repaired_grading, repaired_trace = grade_coding_submission_path(
            question_case,
            submission_path=submission_path,
            run_dir=run_dir,
            submission_source="repair_model",
            submission_compliance="repaired_after_invalid_output",
            recovery_used=True,
            recovery_notes=f"Repair attempt {attempt_index} after invalid contestant output.",
            artifact_refs=[artifact_ref],
        )
        attempt_payload.update(
            {
                "status": "graded",
                "submission_path": str(submission_path),
                "grading": repaired_grading,
                "trace": repaired_trace,
            }
        )
        attempts.append(attempt_payload)
        current_code = repaired_code
        has_recovered_code = True
        current_grading = repaired_grading
        current_trace = repaired_trace
        if not _needs_repair(current_grading, current_trace):
            break

    if not attempts:
        return None
    current_trace = dict(current_trace)
    current_trace["repair_attempts"] = attempts
    return current_grading, current_trace


def _build_repair_messages(
    *,
    question_case: QuestionCase,
    problem_text: str,
    current_code: str,
    seed_excerpt: str,
    has_recovered_code: bool,
    feedback: str,
) -> list[dict[str, str]]:
    current_submission_block = (
        "Current main.py:\n"
        f"```python\n{current_code}\n```"
        if has_recovered_code
        else (
            "No runnable main.py was recovered from the previous attempt.\n"
            "Previous model output excerpt:\n"
            f"{seed_excerpt or '(empty)'}"
        )
    )
    return [
        {
            "role": "system",
            "content": (
                "You repair Python competitive-programming submissions. "
                "Return only the full contents of main.py and nothing else. "
                "Highest priority: produce strictly valid contestant output that matches the required output format exactly. "
                "Never print explanations, debug text, labels, or computed scores unless the problem explicitly requires them. "
                "If unsure, prefer the simplest strictly valid solution over an invalid ambitious one."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Question ID: {question_case.question_id}\n"
                f"Title: {question_case.title}\n\n"
                f"Problem statement:\n{problem_text}\n\n"
                f"{current_submission_block}\n\n"
                "Observed validation/scoring feedback from the official public tool:\n"
                f"{feedback}\n\n"
                "Write or repair the Python program so it reads stdin and prints only valid contestant output. "
                "If the output format starts with a count/header line, print that first line exactly. "
                "Do not print the objective value unless the Output section explicitly asks for it. "
                "Return only main.py."
            ),
        },
    ]


def _needs_repair(grading: dict[str, Any], grading_trace: dict[str, Any]) -> bool:
    compliance = str(grading.get("submission_compliance") or "")
    if compliance in {"missing_submission", "ambiguous_submission"}:
        return True
    execution = dict((grading_trace or {}).get("execution") or {})
    for item in list(execution.get("instance_results") or []):
        scorer = dict(item.get("scorer_payload") or {})
        status = str(scorer.get("status") or item.get("status") or "")
        if status == "candidate_output_invalid":
            return True
        notes = "\n".join(
            str(value or "")
            for value in (
                scorer.get("notes"),
                scorer.get("stdout"),
                scorer.get("stderr"),
                item.get("scorer_notes"),
            )
        ).lower()
        if any(marker in notes for marker in ("out of range", "too many outputs", "too few outputs", "parse", "invalid")):
            return True
    return False


def _build_repair_feedback(grading_trace: dict[str, Any]) -> str:
    lines: list[str] = []
    execution = dict((grading_trace or {}).get("execution") or {})
    for item in list(execution.get("instance_results") or [])[:3]:
        scorer = dict(item.get("scorer_payload") or {})
        lines.append(f"Instance: {item.get('name')}")
        if scorer.get("status"):
            lines.append(f"- scorer status: {scorer.get('status')}")
        for field in ("notes", "stdout", "stderr"):
            value = str(scorer.get(field) or "").strip()
            if value:
                lines.append(f"- scorer {field}: {value[:500]}")
        stdout = str(item.get("stdout") or "").strip()
        if stdout:
            lines.append(f"- candidate stdout head: {stdout[:300]}")
        stderr = str(item.get("stderr") or "").strip()
        if stderr:
            lines.append(f"- candidate stderr head: {stderr[:300]}")
    return "\n".join(lines).strip() or "The previous submission did not produce valid contestant output."


def _load_current_submission_code(grading_trace: dict[str, Any]) -> str:
    submission = dict((grading_trace or {}).get("submission") or {})
    submission_path = submission.get("submission_path")
    if not submission_path:
        return ""
    path = Path(str(submission_path))
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _load_raw_model_output_excerpt(run_dir: Path) -> str:
    replay_path = run_dir / "replay" / "node_root" / "raw-model.json"
    if not replay_path.exists():
        return ""
    try:
        payload = json.loads(replay_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return ""
    steps = list(payload.get("steps") or [])
    for step in reversed(steps):
        provider_payload = dict(step.get("provider_payload") or {})
        for attempt in reversed(list(provider_payload.get("attempts") or [])):
            raw_content = str(attempt.get("raw_content") or "").strip()
            if raw_content:
                return raw_content[:4000]
    return ""


def _extract_response_content(response: dict[str, Any]) -> str:
    choice = dict(response.get("choices", [{}])[0])
    message = dict(choice.get("message") or {})
    content = message.get("content")
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(str(item.get("text") or ""))
        return "\n".join(part.strip() for part in parts if part.strip()).strip()
    return ""


def _extract_python_code(raw_text: str) -> str:
    text = str(raw_text or "").strip()
    if not text:
        return ""
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        parsed = None
    if isinstance(parsed, dict):
        candidate = str(parsed.get("main_py") or parsed.get("main.py") or "").strip()
        if candidate:
            text = candidate
    match = PYTHON_FENCE_RE.search(text)
    if match:
        return str(match.group("code") or "").strip()
    lowered = text.lower()
    if lowered.startswith("```python"):
        stripped = text.split("\n", 1)[1] if "\n" in text else ""
        if stripped.rstrip().endswith("```"):
            stripped = stripped.rstrip()[:-3].rstrip()
        return stripped.strip()
    if lowered.startswith("```py"):
        stripped = text.split("\n", 1)[1] if "\n" in text else ""
        if stripped.rstrip().endswith("```"):
            stripped = stripped.rstrip()[:-3].rstrip()
        return stripped.strip()
    if text.startswith("```") and text.endswith("```"):
        stripped = text.strip("`").strip()
        if stripped.lower().startswith("python"):
            return stripped[6:].strip()
    return text

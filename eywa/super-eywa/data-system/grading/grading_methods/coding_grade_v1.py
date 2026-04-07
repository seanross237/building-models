"""Execution-backed grading for packetized coding benchmarks."""

from __future__ import annotations

import ast
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from typing import Any

from atcoder_official_tools_v1 import run_atcoder_tester_and_vis, run_atcoder_vis
from coding_packets_v1 import CodingPacket, load_coding_packet
from question_bank_v1 import QuestionCase


class CodingGradeError(ValueError):
    """Raised when a coding benchmark cannot be evaluated cleanly."""


PYTHON_FENCE_RE = re.compile(r"```(?:python|py)?\s*\n(?P<code>[\s\S]*?)```", flags=re.IGNORECASE)
ATTACHED_COMPLIANCE = "clean"
MISSING_SUBMISSION = "missing_submission"
AMBIGUOUS_SUBMISSION = "ambiguous_submission"


def maybe_grade_coding_submission(
    question_case: QuestionCase,
    *,
    run_dir: Path | None,
    final_output: dict[str, Any] | None,
    result_text: str = "",
) -> tuple[dict[str, Any], dict[str, Any]] | None:
    if question_case.entry_type != "coding":
        return None

    packet = load_coding_packet(question_id=question_case.question_id, strict=False)
    if packet is None:
        grading = _ungraded_payload(
            question_case=question_case,
            note="Coding benchmark has no runnable packet bundle yet.",
        )
        return grading, {
            "provider": "coding-harness-v1",
            "model": "none",
            "packet": None,
            "submission": None,
            "execution": None,
        }

    if packet.language != "python":
        grading = _ungraded_payload(
            question_case=question_case,
            note=f"Unsupported coding packet language for v1: {packet.language}",
        )
        return grading, {
            "provider": "coding-harness-v1",
            "model": "none",
            "packet": _packet_trace(packet),
            "submission": None,
            "execution": None,
        }

    submission = _resolve_submission(
        packet=packet,
        run_dir=run_dir,
        final_output=final_output,
        result_text=result_text,
    )
    return _grade_packet_submission(
        question_case=question_case,
        packet=packet,
        submission=submission,
        run_dir=run_dir,
    )


def grade_coding_submission_path(
    question_case: QuestionCase,
    *,
    submission_path: Path,
    run_dir: Path | None,
    submission_source: str,
    submission_compliance: str,
    recovery_used: bool,
    recovery_notes: str,
    artifact_refs: list[str] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    packet = load_coding_packet(question_id=question_case.question_id, strict=False)
    if packet is None:
        grading = _ungraded_payload(
            question_case=question_case,
            note="Coding benchmark has no runnable packet bundle yet.",
        )
        return grading, {
            "provider": "coding-harness-v1",
            "model": "none",
            "packet": None,
            "submission": None,
            "execution": None,
        }
    submission = {
        "ok": True,
        "artifact_ref": (artifact_refs or [None])[0],
        "artifact_refs": list(artifact_refs or []),
        "submission_path": submission_path,
        "entry_file": packet.entry_file,
        "submission_source": submission_source,
        "submission_compliance": submission_compliance,
        "recovery_used": recovery_used,
        "recovery_notes": recovery_notes,
    }
    return _grade_packet_submission(
        question_case=question_case,
        packet=packet,
        submission=submission,
        run_dir=run_dir,
    )


def _grade_packet_submission(
    *,
    question_case: QuestionCase,
    packet: CodingPacket,
    submission: dict[str, Any],
    run_dir: Path | None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    if not submission["ok"]:
        grading = _contract_failure_grading(packet=packet, submission=submission)
        return grading, {
            "provider": "coding-harness-v1",
            "model": "none",
            "packet": _packet_trace(packet),
            "submission": _submission_trace(submission),
            "execution": None,
        }

    if packet.checker_type == "binary_public_tests":
        grading, execution = _grade_binary_public_tests(packet, submission["submission_path"])
    elif packet.checker_type == "binary_public_checker":
        grading, execution = _grade_binary_public_checker(packet, submission["submission_path"])
    elif packet.checker_type == "continuous_public_simulator":
        grading, execution = _grade_continuous_public_simulator(
            packet,
            submission["submission_path"],
            run_dir=run_dir,
        )
    else:
        raise CodingGradeError(f"Unsupported checker_type: {packet.checker_type}")

    grading.update(_submission_outcome_fields(submission))
    return grading, {
        "provider": "coding-harness-v1",
        "model": "none",
        "packet": _packet_trace(packet),
        "submission": _submission_trace(submission),
        "execution": execution,
    }


def recover_submission_from_response_text(
    *,
    packet: CodingPacket,
    run_dir: Path,
    response_text: str,
    artifact_subdir: str,
    compliance: str,
    notes: str,
) -> dict[str, Any] | None:
    return _recover_submission_from_response(
        packet=packet,
        run_dir=run_dir,
        response_text=response_text,
        attachment_refs=[],
        artifact_subdir=artifact_subdir,
        artifact_ref=f"{artifact_subdir}/{packet.entry_file}",
        fenced_compliance=compliance,
        plain_text_compliance=compliance,
        fenced_notes=notes,
        plain_text_notes=notes,
    )


def _resolve_submission(
    *,
    packet: CodingPacket,
    run_dir: Path | None,
    final_output: dict[str, Any] | None,
    result_text: str,
) -> dict[str, Any]:
    result = dict((final_output or {}).get("result") or {})
    attachment_refs = list(result.get("attachment_refs") or [])
    if run_dir is None:
        return _submission_failure(
            compliance=MISSING_SUBMISSION,
            source="none",
            message="Run directory is missing for coding grading.",
        )

    attached = _attached_submission_candidates(packet=packet, run_dir=run_dir, attachment_refs=attachment_refs)
    if len(attached) > 1:
        return _submission_failure(
            compliance=AMBIGUOUS_SUBMISSION,
            source="attachment",
            message=f"Multiple {packet.entry_file} attachments were present; recovery is ambiguous.",
            attachment_refs=attachment_refs,
        )
    if len(attached) == 1:
        candidate = attached[0]
        return {
            "ok": True,
            "artifact_ref": candidate["artifact_ref"],
            "artifact_refs": [candidate["artifact_ref"]],
            "submission_path": candidate["submission_path"],
            "entry_file": packet.entry_file,
            "submission_source": "attachment",
            "submission_compliance": ATTACHED_COMPLIANCE,
            "recovery_used": False,
            "recovery_notes": "",
        }

    recovered = _recover_submission_from_response(
        packet=packet,
        run_dir=run_dir,
        response_text=str(result.get("content") or result_text or ""),
        attachment_refs=attachment_refs,
    )
    if recovered is not None:
        return recovered

    return _submission_failure(
        compliance=MISSING_SUBMISSION,
        source="none",
        message=f"No safe runnable {packet.entry_file} submission could be recovered.",
        attachment_refs=attachment_refs,
    )


def _attached_submission_candidates(
    *,
    packet: CodingPacket,
    run_dir: Path,
    attachment_refs: list[str],
) -> list[dict[str, Any]]:
    matches: list[dict[str, Any]] = []
    for ref in attachment_refs:
        path = (run_dir / str(ref)).resolve()
        if path.name != packet.entry_file or not path.exists():
            continue
        matches.append({"artifact_ref": str(ref), "submission_path": path})
    return matches


def _recover_submission_from_response(
    *,
    packet: CodingPacket,
    run_dir: Path,
    response_text: str,
    attachment_refs: list[str],
    artifact_subdir: str | None = None,
    artifact_ref: str | None = None,
    fenced_compliance: str = "recovered_from_fenced_code",
    plain_text_compliance: str = "recovered_from_plain_text",
    fenced_notes: str = "Recovered main.py from a fenced code block in the final response.",
    plain_text_notes: str = "Recovered main.py from a plain-text code response.",
) -> dict[str, Any] | None:
    text = str(response_text or "")
    if not text.strip():
        return None

    fenced_candidates = _extract_fenced_code_candidates(text)
    if len(fenced_candidates) > 1:
        return _submission_failure(
            compliance=AMBIGUOUS_SUBMISSION,
            source="fenced_code",
            message="Multiple fenced code submissions were present; recovery is ambiguous.",
            attachment_refs=attachment_refs,
        )
    if len(fenced_candidates) == 1:
        return _persist_recovered_submission(
            packet=packet,
            run_dir=run_dir,
            code_text=fenced_candidates[0],
            source="fenced_code",
            compliance=fenced_compliance,
            notes=fenced_notes,
            attachment_refs=attachment_refs,
            artifact_subdir=artifact_subdir,
            artifact_ref=artifact_ref,
        )

    plain_code = _extract_plain_code_candidate(text)
    if plain_code is not None:
        return _persist_recovered_submission(
            packet=packet,
            run_dir=run_dir,
            code_text=plain_code,
            source="plain_text",
            compliance=plain_text_compliance,
            notes=plain_text_notes,
            attachment_refs=attachment_refs,
            artifact_subdir=artifact_subdir,
            artifact_ref=artifact_ref,
        )
    return None


def _extract_fenced_code_candidates(text: str) -> list[str]:
    candidates: list[str] = []
    for match in PYTHON_FENCE_RE.finditer(text):
        code = str(match.group("code") or "").strip()
        if code and _looks_like_python_submission(code):
            candidates.append(code)
    return candidates


def _extract_plain_code_candidate(text: str) -> str | None:
    stripped = str(text or "").strip()
    if "```" in stripped:
        return None
    if _looks_like_python_submission(stripped):
        return stripped
    return None


def _looks_like_python_submission(code_text: str) -> bool:
    code = str(code_text or "").strip()
    if not code:
        return False
    try:
        ast.parse(code)
    except SyntaxError:
        return False
    lines = [line for line in code.splitlines() if line.strip()]
    if len(lines) < 2:
        return False
    signal_patterns = (
        "import ",
        "from ",
        "def ",
        "class ",
        "if __name__",
        "print(",
        "sys.stdin",
        "input(",
        "map(",
        "for ",
        "while ",
    )
    return any(pattern in code for pattern in signal_patterns)


def _persist_recovered_submission(
    *,
    packet: CodingPacket,
    run_dir: Path,
    code_text: str,
    source: str,
    compliance: str,
    notes: str,
    attachment_refs: list[str],
    artifact_subdir: str | None = None,
    artifact_ref: str | None = None,
) -> dict[str, Any]:
    artifact_subdir = artifact_subdir or f"grading-artifacts/{packet.question_id}/recovered-submissions"
    artifact_ref = artifact_ref or f"{artifact_subdir}/{packet.entry_file}"
    recovered_dir = run_dir / artifact_subdir
    recovered_dir.mkdir(parents=True, exist_ok=True)
    submission_path = recovered_dir / packet.entry_file
    submission_path.write_text(code_text.rstrip() + "\n", encoding="utf-8")
    return {
        "ok": True,
        "artifact_ref": artifact_ref,
        "artifact_refs": [artifact_ref],
        "submission_path": submission_path,
        "entry_file": packet.entry_file,
        "submission_source": source,
        "submission_compliance": compliance,
        "recovery_used": True,
        "recovery_notes": notes,
    }


def _submission_failure(
    *,
    compliance: str,
    source: str,
    message: str,
    attachment_refs: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "ok": False,
        "message": message,
        "attachment_refs": list(attachment_refs or []),
        "submission_compliance": compliance,
        "submission_source": source,
        "recovery_used": False,
        "recovery_notes": message,
    }


def _grade_binary_public_tests(packet: CodingPacket, submission_path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    case_results = []
    for case in packet.public_tests:
        execution = _run_python_submission(
            submission_path=submission_path,
            stdin_text=case.stdin_path.read_text(encoding="utf-8"),
            time_limit_seconds=packet.time_limit_seconds,
        )
        expected_text = case.expected_stdout_path.read_text(encoding="utf-8")
        matched = execution["ok"] and _normalize_stdout(execution["stdout"]) == _normalize_stdout(expected_text)
        case_results.append(
            {
                "name": case.name,
                "stdin_path": str(case.stdin_path),
                "expected_stdout_path": str(case.expected_stdout_path),
                "expected_stdout": expected_text,
                **execution,
                "matched": matched,
            }
        )
        if not matched:
            break

    correct = all(item["matched"] for item in case_results) and len(case_results) == len(packet.public_tests)
    failed_case = next((item for item in case_results if not item["matched"]), None)
    grading = {
        "grading_status": "graded",
        "correct": correct,
        "score": 1.0 if correct else 0.0,
        "task_correct": correct,
        "task_score": 1.0 if correct else 0.0,
        "expected": f"accepted on {len(packet.public_tests)} bundled public test(s)",
        "extracted_answer": "accepted" if correct else (failed_case or {}).get("name") or "failed",
        "normalized_answer": None,
        "grading_notes": (
            "Submission passed all bundled public tests."
            if correct
            else _binary_failure_note(failed_case)
        ),
        "confidence": "high",
        "grading_method": "coding_binary_public_tests_v1",
    }
    return grading, {
        "checker_type": packet.checker_type,
        "case_results": case_results,
    }


def _grade_continuous_public_simulator(
    packet: CodingPacket,
    submission_path: Path,
    *,
    run_dir: Path | None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    if packet.scorer_path is None and packet.official_tool_mode is None:
        raise CodingGradeError(f"continuous packet {packet.question_id} is missing a scorer")

    instance_results = []
    artifact_root = None
    if run_dir is not None:
        artifact_root = run_dir / "grading-artifacts" / packet.question_id
    for instance in packet.instances:
        instance_artifact_dir = artifact_root / instance.name if artifact_root is not None else None
        if packet.official_tool_mode == "atcoder_tester_then_vis":
            if packet.official_tool_path is None:
                raise CodingGradeError(f"interactive packet {packet.question_id} is missing an official tool path")
            scorer = run_atcoder_tester_and_vis(
                tool_dir=packet.official_tool_path,
                input_path=instance.stdin_path,
                submission_path=submission_path,
                artifact_dir=instance_artifact_dir or Path(tempfile.mkdtemp(prefix="super_eywa_coding_tester_")),
                timeout_seconds=packet.official_tool_timeout_seconds,
            )
            instance_results.append(
                {
                    "name": instance.name,
                    "stdin_path": str(instance.stdin_path),
                    "ok": bool(scorer.get("ok")),
                    "status": scorer.get("status"),
                    "exit_code": None,
                    "stdout": scorer.get("stdout", ""),
                    "stderr": scorer.get("stderr", ""),
                    "wall_time_ms": None,
                    "score": float(scorer.get("score") or 0.0),
                    "scorer_notes": str(scorer.get("notes") or ""),
                    "scorer_payload": scorer,
                    "artifact_paths": list(scorer.get("artifact_paths") or []),
                }
            )
            continue

        execution = _run_python_submission(
            submission_path=submission_path,
            stdin_text=instance.stdin_path.read_text(encoding="utf-8"),
            time_limit_seconds=packet.time_limit_seconds,
        )
        candidate_output_path: Path | None = None
        if instance_artifact_dir is not None:
            instance_artifact_dir.mkdir(parents=True, exist_ok=True)
            candidate_output_path = instance_artifact_dir / "candidate.out"
            candidate_output_path.write_text(str(execution.get("stdout") or ""), encoding="utf-8")
        if not execution["ok"]:
            instance_results.append(
                {
                    "name": instance.name,
                    "stdin_path": str(instance.stdin_path),
                    **execution,
                    "score": 0.0,
                    "scorer_notes": "Submission failed before scoring.",
                    "artifact_paths": [str(candidate_output_path)] if candidate_output_path is not None else [],
                }
            )
            continue
        if packet.official_tool_mode == "atcoder_vis":
            if packet.official_tool_path is None or candidate_output_path is None:
                raise CodingGradeError(f"official vis packet {packet.question_id} is missing grading artifacts setup")
            scorer = run_atcoder_vis(
                tool_dir=packet.official_tool_path,
                input_path=instance.stdin_path,
                output_path=candidate_output_path,
                artifact_dir=instance_artifact_dir,
                timeout_seconds=packet.official_tool_timeout_seconds,
            )
        else:
            scorer = _run_scorer(
                scorer_path=packet.scorer_path,
                stdin_path=instance.stdin_path,
                candidate_stdout=execution["stdout"],
            )
        instance_results.append(
            {
                "name": instance.name,
                "stdin_path": str(instance.stdin_path),
                **execution,
                "score": float(scorer.get("score") or 0.0),
                "scorer_notes": str(scorer.get("notes") or ""),
                "scorer_payload": scorer,
                "artifact_paths": list(scorer.get("artifact_paths") or []),
            }
        )

    score = _aggregate_scores(packet.aggregate_method, [item["score"] for item in instance_results])
    grading = {
        "grading_status": "graded",
        "correct": None,
        "score": score,
        "task_correct": None,
        "task_score": score,
        "expected": f"continuous score on {len(instance_results)} bundled public instance(s)",
        "extracted_answer": f"{score}",
        "normalized_answer": score,
        "grading_notes": f"Continuous public-simulator score using aggregate={packet.aggregate_method}.",
        "confidence": "high",
        "grading_method": "coding_continuous_public_simulator_v1",
    }
    return grading, {
        "checker_type": packet.checker_type,
        "instance_results": instance_results,
        "aggregate_method": packet.aggregate_method,
    }


def _grade_binary_public_checker(
    packet: CodingPacket,
    submission_path: Path,
) -> tuple[dict[str, Any], dict[str, Any]]:
    if packet.checker_path is None:
        raise CodingGradeError(f"binary checker packet {packet.question_id} is missing a checker")
    case_results = []
    for case in packet.public_tests:
        execution = _run_python_submission(
            submission_path=submission_path,
            stdin_text=case.stdin_path.read_text(encoding="utf-8"),
            time_limit_seconds=packet.time_limit_seconds,
        )
        if not execution["ok"]:
            case_results.append(
                {
                    "name": case.name,
                    "stdin_path": str(case.stdin_path),
                    **execution,
                    "matched": False,
                    "checker_payload": None,
                }
            )
            break
        checker_payload = _run_binary_checker(
            checker_path=packet.checker_path,
            stdin_path=case.stdin_path,
            candidate_stdout=execution["stdout"],
        )
        matched = bool(checker_payload.get("ok"))
        case_results.append(
            {
                "name": case.name,
                "stdin_path": str(case.stdin_path),
                **execution,
                "matched": matched,
                "checker_payload": checker_payload,
            }
        )
        if not matched:
            break

    correct = all(item["matched"] for item in case_results) and len(case_results) == len(packet.public_tests)
    failed_case = next((item for item in case_results if not item["matched"]), None)
    grading = {
        "grading_status": "graded",
        "correct": correct,
        "score": 1.0 if correct else 0.0,
        "task_correct": correct,
        "task_score": 1.0 if correct else 0.0,
        "expected": f"accepted by checker on {len(packet.public_tests)} bundled public test(s)",
        "extracted_answer": "accepted" if correct else (failed_case or {}).get("name") or "failed",
        "normalized_answer": None,
        "grading_notes": (
            "Submission passed all bundled public checker runs."
            if correct
            else _checker_failure_note(failed_case)
        ),
        "confidence": "high",
        "grading_method": "coding_binary_public_checker_v1",
    }
    return grading, {
        "checker_type": packet.checker_type,
        "case_results": case_results,
    }


def _run_python_submission(*, submission_path: Path, stdin_text: str, time_limit_seconds: float) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="super_eywa_coding_run_") as tmpdir:
        tempdir = Path(tmpdir)
        candidate_path = tempdir / submission_path.name
        shutil.copy2(submission_path, candidate_path)
        try:
            completed = subprocess.run(
                [sys.executable, str(candidate_path)],
                input=stdin_text,
                text=True,
                capture_output=True,
                cwd=tempdir,
                timeout=time_limit_seconds,
                env={"PYTHONUNBUFFERED": "1"},
            )
        except subprocess.TimeoutExpired as exc:
            return {
                "ok": False,
                "status": "timeout",
                "exit_code": None,
                "stdout": str(exc.stdout or ""),
                "stderr": str(exc.stderr or ""),
                "wall_time_ms": int(time_limit_seconds * 1000),
            }

    return {
        "ok": completed.returncode == 0,
        "status": "ok" if completed.returncode == 0 else "runtime_error",
        "exit_code": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "wall_time_ms": None,
    }


def _run_scorer(*, scorer_path: Path, stdin_path: Path, candidate_stdout: str) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="super_eywa_coding_score_") as tmpdir:
        tempdir = Path(tmpdir)
        output_path = tempdir / "candidate.out"
        output_path.write_text(candidate_stdout, encoding="utf-8")
        completed = subprocess.run(
            [sys.executable, str(scorer_path), "--input", str(stdin_path), "--output", str(output_path)],
            text=True,
            capture_output=True,
            cwd=scorer_path.parent,
            timeout=10.0,
            env={"PYTHONUNBUFFERED": "1"},
        )
        if completed.returncode != 0:
            raise CodingGradeError(
                f"scorer failed for {scorer_path.name}: {completed.stderr.strip() or completed.stdout.strip()}"
            )
        try:
            payload = json.loads(completed.stdout)
        except json.JSONDecodeError as exc:
            raise CodingGradeError(f"scorer returned invalid JSON for {scorer_path.name}") from exc
        return payload


def _run_binary_checker(*, checker_path: Path, stdin_path: Path, candidate_stdout: str) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="super_eywa_coding_check_") as tmpdir:
        tempdir = Path(tmpdir)
        output_path = tempdir / "candidate.out"
        output_path.write_text(candidate_stdout, encoding="utf-8")
        completed = subprocess.run(
            [sys.executable, str(checker_path), "--input", str(stdin_path), "--output", str(output_path)],
            text=True,
            capture_output=True,
            cwd=checker_path.parent,
            timeout=10.0,
            env={"PYTHONUNBUFFERED": "1"},
        )
        if completed.returncode != 0:
            raise CodingGradeError(
                f"checker failed for {checker_path.name}: {completed.stderr.strip() or completed.stdout.strip()}"
            )
        try:
            payload = json.loads(completed.stdout)
        except json.JSONDecodeError as exc:
            raise CodingGradeError(f"checker returned invalid JSON for {checker_path.name}") from exc
        return payload


def _aggregate_scores(aggregate_method: str, scores: list[float]) -> float:
    if not scores:
        return 0.0
    if aggregate_method == "sum":
        return float(sum(scores))
    if aggregate_method == "max":
        return float(max(scores))
    return float(sum(scores) / len(scores))


def _normalize_stdout(text: str) -> str:
    normalized_lines = [" ".join(line.rstrip().split()) for line in str(text).strip().splitlines()]
    return "\n".join(normalized_lines).strip()


def _binary_failure_note(failed_case: dict[str, Any] | None) -> str:
    if not failed_case:
        return "Submission failed one of the bundled public tests."
    if failed_case.get("status") == "timeout":
        return f"Submission timed out on public test {failed_case['name']}."
    if failed_case.get("status") == "runtime_error":
        stderr = str(failed_case.get("stderr") or "").strip()
        return f"Submission crashed on public test {failed_case['name']}: {stderr or 'runtime error'}"
    return (
        f"Wrong output on public test {failed_case['name']}. "
        f"Expected {_normalize_stdout(failed_case.get('expected_stdout') or '')!r}, "
        f"got {_normalize_stdout(failed_case.get('stdout') or '')!r}."
    )


def _packet_trace(packet: CodingPacket) -> dict[str, Any]:
    return {
        "question_id": packet.question_id,
        "manifest_path": str(packet.manifest_path),
        "problem_statement_path": str(packet.problem_statement_path),
        "language": packet.language,
        "entry_file": packet.entry_file,
        "checker_type": packet.checker_type,
        "checker_path": str(packet.checker_path) if packet.checker_path else None,
        "official_tool_mode": packet.official_tool_mode,
        "official_tool_path": str(packet.official_tool_path) if packet.official_tool_path else None,
        "official_tool_timeout_seconds": packet.official_tool_timeout_seconds,
        "time_limit_seconds": packet.time_limit_seconds,
        "aggregate_method": packet.aggregate_method,
        "notes": packet.notes,
    }


def _submission_trace(submission: dict[str, Any]) -> dict[str, Any]:
    payload = dict(submission)
    submission_path = payload.get("submission_path")
    if isinstance(submission_path, Path):
        payload["submission_path"] = str(submission_path)
    return payload


def _ungraded_payload(*, question_case: QuestionCase, note: str) -> dict[str, Any]:
    return {
        "grading_status": "ungraded",
        "correct": None,
        "score": None,
        "task_correct": None,
        "task_score": None,
        "submission_compliance": None,
        "recovery_used": False,
        "submission_source": None,
        "recovery_notes": "",
        "expected": question_case.sections.get("grading", ""),
        "extracted_answer": None,
        "normalized_answer": None,
        "grading_notes": note,
        "confidence": "high",
        "grading_method": "coding_harness_missing_v1",
    }


def _checker_failure_note(failed_case: dict[str, Any] | None) -> str:
    if not failed_case:
        return "Submission failed one of the bundled public checker runs."
    if failed_case.get("status") == "timeout":
        return f"Submission timed out on public test {failed_case['name']}."
    if failed_case.get("status") == "runtime_error":
        stderr = str(failed_case.get("stderr") or "").strip()
        return f"Submission crashed on public test {failed_case['name']}: {stderr or 'runtime error'}"
    checker_payload = failed_case.get("checker_payload") or {}
    return str(checker_payload.get("notes") or f"Submission failed public checker {failed_case['name']}.")


def _submission_outcome_fields(submission: dict[str, Any]) -> dict[str, Any]:
    return {
        "submission_compliance": submission.get("submission_compliance"),
        "recovery_used": bool(submission.get("recovery_used")),
        "submission_source": submission.get("submission_source"),
        "recovery_notes": str(submission.get("recovery_notes") or ""),
    }


def _contract_failure_grading(*, packet: CodingPacket, submission: dict[str, Any]) -> dict[str, Any]:
    task_correct = False if packet.checker_type.startswith("binary_") else None
    message = str(submission.get("message") or "No safe runnable submission could be recovered.")
    return {
        "grading_status": "graded",
        "correct": task_correct,
        "score": 0.0,
        "task_correct": task_correct,
        "task_score": 0.0,
        "submission_compliance": submission.get("submission_compliance") or MISSING_SUBMISSION,
        "recovery_used": bool(submission.get("recovery_used")),
        "submission_source": submission.get("submission_source"),
        "recovery_notes": str(submission.get("recovery_notes") or message),
        "expected": "accepted submission on bundled public checks",
        "extracted_answer": message,
        "normalized_answer": None,
        "grading_notes": message,
        "confidence": "high",
        "grading_method": "coding_submission_contract_v2",
    }

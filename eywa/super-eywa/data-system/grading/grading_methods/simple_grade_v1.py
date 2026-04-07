"""Simple grading-bank helpers for Super-Eywa v1 live runs."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict

from coding_packets_v1 import load_coding_packet
from question_bank_v1 import QuestionCase, load_question_case


def parse_question_file(path: Path) -> QuestionCase:
    return load_question_case(source_path=path)


def build_task_prompt(question_case: QuestionCase) -> str:
    if question_case.entry_type == "coding":
        return _build_coding_task_prompt(question_case)

    question_body = question_case.sections.get("problem") or ""
    grading_body = question_case.sections.get("grading", "")

    parts = [
        "Solve this Super-Eywa grading-bank question.",
        f"Question ID: {question_case.question_id}",
        f"Title: {question_case.title}",
        "",
        "Problem:",
        question_body.strip(),
    ]

    if grading_body.strip():
        parts.extend(
            [
                "",
                "Grading target:",
                grading_body.strip(),
            ]
        )

    parts.extend(
        [
            "",
            "Return format:",
            "FINAL_ANSWER: <your answer>",
            "JUSTIFICATION: <brief justification>",
        ]
    )
    return "\n".join(parts).strip()


def _build_coding_task_prompt(question_case: QuestionCase) -> str:
    packet = load_coding_packet(question_id=question_case.question_id, strict=False)
    problem_body = (
        packet.problem_statement_path.read_text(encoding="utf-8").strip()
        if packet is not None
        else (question_case.sections.get("problem") or "").strip()
    )
    grading_body = question_case.sections.get("grading", "")
    parts = [
        "Solve this Super-Eywa coding benchmark.",
        f"Question ID: {question_case.question_id}",
        f"Title: {question_case.title}",
        "",
        "Problem:",
        problem_body,
        "",
        "Submission contract:",
        "- Return a single Python submission file named main.py.",
        "- Read from stdin and write to stdout.",
        "- Put the full file content in the artifacts list of your execute_locally JSON response.",
        "- Use the response field only for a brief submission summary.",
        "- Do not wrap the code in markdown fences inside artifacts.",
        "",
        "Critical validity rules:",
        "- Your program is judged by the stdout it prints when run, not by the summary in your JSON response.",
        "- Print exactly the contestant output described in the Output section, and nothing else.",
        "- Do not print the objective score, estimated score, labels, explanations, or debug text unless the Output section explicitly requires them.",
        "- If the Output section requires a count/header on the first line, print that first line exactly.",
        "- Every printed index, count, and coordinate must stay within the allowed ranges.",
        "- Prefer a simple valid baseline solution over an ambitious but invalid one.",
        "- If the problem permits an empty or minimal valid plan, that is better than malformed output.",
    ]
    if grading_body.strip():
        parts.extend(
            [
                "",
                "Grading target:",
                grading_body.strip(),
            ]
        )
    if packet is not None and packet.valid_baseline_hint:
        parts.extend(
            [
                "",
                "Packet baseline hint:",
                packet.valid_baseline_hint,
            ]
        )
    return "\n".join(parts).strip()


def grade_result(question_case: QuestionCase, result_text: str) -> Dict[str, Any]:
    extracted_answer = extract_final_answer(result_text)
    grader_type = question_case.grader_type
    grader_config = dict(question_case.grader_config or {})

    if grader_type == "exact_numeric_hensel_target":
        return _grade_hensel_lifting(question_case, extracted_answer, int(grader_config["expected"]))
    if grader_type == "exact_numeric":
        return _grade_exact_numeric(question_case, extracted_answer, float(grader_config["expected"]))
    if grader_type == "numeric_tolerance":
        return _grade_numeric_tolerance(
            question_case,
            extracted_answer,
            float(grader_config["expected"]),
            float(grader_config["tolerance"]),
        )
    if grader_type == "exact_normalized_string":
        return _grade_exact_string(question_case, extracted_answer, str(grader_config["expected"]))

    return {
        "grading_status": "ungraded",
        "correct": None,
        "score": None,
        "expected": question_case.sections.get("correct_answer", ""),
        "extracted_answer": extracted_answer,
        "grading_notes": "No simple v1 grader is defined for this question yet.",
    }


def extract_final_answer(result_text: str) -> str:
    for line in result_text.splitlines():
        stripped = line.strip()
        if stripped.upper().startswith("FINAL_ANSWER:"):
            return stripped.split(":", 1)[1].strip()
    first_nonempty_line = next((line.strip() for line in result_text.splitlines() if line.strip()), "")
    return first_nonempty_line


def _grade_exact_numeric(question_case: QuestionCase, extracted_answer: str, expected_value: float) -> Dict[str, Any]:
    number = _extract_number(extracted_answer)
    correct = number is not None and abs(number - expected_value) < 1e-9
    return {
        "grading_status": "graded",
        "correct": correct,
        "score": 1.0 if correct else 0.0,
        "expected": expected_value,
        "extracted_answer": extracted_answer,
        "normalized_answer": number,
        "grading_notes": question_case.sections.get("grading", ""),
    }


def _grade_hensel_lifting(question_case: QuestionCase, extracted_answer: str, expected_value: int) -> Dict[str, Any]:
    number = _extract_hensel_target_number(extracted_answer)
    correct = number is not None and abs(number - expected_value) < 1e-9
    return {
        "grading_status": "graded",
        "correct": correct,
        "score": 1.0 if correct else 0.0,
        "expected": expected_value,
        "extracted_answer": extracted_answer,
        "normalized_answer": number,
        "grading_notes": question_case.sections.get("grading", ""),
    }


def _grade_numeric_tolerance(
    question_case: QuestionCase,
    extracted_answer: str,
    expected_value: float,
    tolerance: float,
) -> Dict[str, Any]:
    number = _extract_number(extracted_answer)
    correct = number is not None and abs(number - expected_value) <= tolerance
    return {
        "grading_status": "graded",
        "correct": correct,
        "score": 1.0 if correct else 0.0,
        "expected": expected_value,
        "tolerance": tolerance,
        "extracted_answer": extracted_answer,
        "normalized_answer": number,
        "grading_notes": question_case.sections.get("grading", ""),
    }


def _grade_exact_string(question_case: QuestionCase, extracted_answer: str, expected_value: str) -> Dict[str, Any]:
    normalized = _normalize_text(extracted_answer)
    correct = normalized == _normalize_text(expected_value)
    return {
        "grading_status": "graded",
        "correct": correct,
        "score": 1.0 if correct else 0.0,
        "expected": expected_value,
        "extracted_answer": extracted_answer,
        "normalized_answer": normalized,
        "grading_notes": question_case.sections.get("grading", ""),
    }


def _extract_number(text: str) -> float | None:
    match = re.search(r"-?\d+(?:\.\d+)?", text.replace(",", ""))
    if not match:
        return None
    try:
        return float(match.group(0))
    except ValueError:
        return None


def _extract_hensel_target_number(text: str) -> float | None:
    normalized = text.replace(",", "")
    m_match = re.search(r"\bm\s*=\s*(-?\d+(?:\.\d+)?)", normalized, flags=re.IGNORECASE)
    if m_match:
        try:
            return float(m_match.group(1))
        except ValueError:
            return None

    numbers = re.findall(r"-?\d+(?:\.\d+)?", normalized)
    if not numbers:
        return None
    try:
        return float(numbers[-1])
    except ValueError:
        return None


def _normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower().rstrip(".")

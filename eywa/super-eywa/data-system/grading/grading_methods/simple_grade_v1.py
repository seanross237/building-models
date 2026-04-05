"""Simple grading-bank helpers for Super-Eywa v1 live runs."""

from __future__ import annotations

from dataclasses import dataclass
import re
from pathlib import Path
from typing import Any, Dict


@dataclass(frozen=True)
class QuestionCase:
    question_id: str
    title: str
    source_path: Path
    sections: Dict[str, str]


def parse_question_file(path: Path) -> QuestionCase:
    raw_text = path.read_text(encoding="utf-8")
    lines = raw_text.splitlines()
    title = path.stem
    if lines and lines[0].startswith("# "):
        title = lines[0][2:].strip()

    sections: Dict[str, str] = {}
    current_section: str | None = None
    buffer: list[str] = []

    def flush() -> None:
        nonlocal buffer, current_section
        if current_section is not None:
            sections[current_section] = "\n".join(buffer).strip()
        buffer = []

    for line in lines[1:]:
        if line.startswith("## "):
            flush()
            current_section = line[3:].strip().lower().replace(" ", "_")
            continue
        if current_section is None:
            continue
        buffer.append(line)
    flush()

    return QuestionCase(
        question_id=path.stem,
        title=title,
        source_path=path.resolve(),
        sections=sections,
    )


def build_task_prompt(question_case: QuestionCase) -> str:
    question_body = question_case.sections.get("question") or question_case.sections.get("task") or ""
    grading_body = question_case.sections.get("grading", "")

    parts = [
        "Solve this Super-Eywa grading-bank question.",
        f"Question ID: {question_case.question_id}",
        f"Title: {question_case.title}",
        "",
        "Question:",
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


def grade_result(question_case: QuestionCase, result_text: str) -> Dict[str, Any]:
    question_id = question_case.question_id
    extracted_answer = extract_final_answer(result_text)

    if question_id == "architecture-derived-B4-hensel-lifting-verification":
        return _grade_exact_numeric(question_case, extracted_answer, 110)
    if question_id == "architecture-derived-B5-combinatorial-probability-random-chords":
        return _grade_exact_numeric(question_case, extracted_answer, 204)
    if question_id == "architecture-derived-B6-binary-representation-minimization":
        return _grade_exact_numeric(question_case, extracted_answer, 3)
    if question_id == "architecture-derived-B10-mean-field-lattice-gas-occupancy":
        return _grade_numeric_tolerance(question_case, extracted_answer, 0.424, 0.01)
    if question_id == "architecture-derived-B11-board-game-rule-chaining":
        return _grade_exact_string(question_case, extracted_answer, "unknown")

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


def _grade_exact_numeric(question_case: QuestionCase, extracted_answer: str, expected_value: int) -> Dict[str, Any]:
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


def _normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower().rstrip(".")

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys


THIS_DIR = Path(__file__).resolve().parent
GRADING_DIR = THIS_DIR.parent
if str(GRADING_DIR) not in sys.path:
    sys.path.insert(0, str(GRADING_DIR))

from grading_methods.simple_grade_v1 import (
    build_task_prompt,
    extract_final_answer,
    grade_result,
    parse_question_file,
)


class SimpleGradeV1Tests(unittest.TestCase):
    def test_parse_and_build_prompt(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            question_file = Path(tmpdir) / "architecture-derived-B6-binary-representation-minimization.md"
            question_file.write_text(
                "\n".join(
                    [
                        "# B6. Binary Representation Minimization",
                        "",
                        "## Question",
                        "",
                        "Find the minimum k(n).",
                        "",
                        "## Correct Answer",
                        "",
                        "3",
                        "",
                        "## Grading",
                        "",
                        "Exact numerical match.",
                    ]
                ),
                encoding="utf-8",
            )
            question_case = parse_question_file(question_file)
            prompt = build_task_prompt(question_case)
            self.assertEqual(question_case.question_id, question_file.stem)
            self.assertIn("Question ID: architecture-derived-B6-binary-representation-minimization", prompt)
            self.assertIn("FINAL_ANSWER:", prompt)

    def test_exact_numeric_grading(self) -> None:
        question_case = parse_question_file(
            Path("data-system/grading/test-questions/architecture-derived-B6-binary-representation-minimization.md")
        )
        result = grade_result(question_case, "FINAL_ANSWER: 3\nJUSTIFICATION: short")
        self.assertTrue(result["correct"])
        self.assertEqual(result["score"], 1.0)

    def test_extract_final_answer_falls_back_to_first_line(self) -> None:
        self.assertEqual(extract_final_answer("unknown\nbecause missing rules"), "unknown")


if __name__ == "__main__":
    unittest.main()

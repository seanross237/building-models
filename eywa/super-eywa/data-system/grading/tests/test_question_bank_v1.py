from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[3]
GRADING_DIR = REPO_ROOT / "data-system" / "grading"
if str(GRADING_DIR) not in sys.path:
    sys.path.insert(0, str(GRADING_DIR))


class QuestionBankV1Tests(unittest.TestCase):
    def test_catalog_builds_and_contains_normalized_problem_entries(self) -> None:
        from question_bank_v1 import build_question_bank_catalog

        catalog = build_question_bank_catalog()
        self.assertEqual(catalog["schema_name"], "eywa_question_bank")
        self.assertEqual(catalog["schema_version"], "v1")
        self.assertEqual(catalog["question_count"], 31)

        by_id = {item["question_id"]: item for item in catalog["questions"]}
        b6 = by_id["architecture-derived-B6-binary-representation-minimization"]
        self.assertEqual(b6["family"], "architecture-derived")
        self.assertEqual(b6["entry_type"], "reasoning")
        self.assertEqual(b6["grader_type"], "exact_numeric")
        self.assertIn("Find the minimum", b6["problem_text"])

        coding_b1 = by_id["coding-B1-usaco-2024-us-open-platinum-identity-theft"]
        self.assertEqual(coding_b1["entry_type"], "coding")
        self.assertEqual(coding_b1["grader_type"], "binary_hidden_tests")
        self.assertTrue(coding_b1["coding_packet_exists"])
        self.assertEqual(coding_b1["coding_checker_type"], "binary_public_tests")

        for suffix in range(1, 7):
            packetized = by_id[f"coding-S{suffix}-" + {
                1: "ahc001-atcoder-ad",
                2: "ahc012-atcoder-10th-anniversary",
                3: "ahc024-topological-map",
                4: "ahc030-polyomino-mining",
                5: "ahc032-mod-stamp",
                6: "ahc037-soda",
            }[suffix]]
            self.assertTrue(packetized["coding_packet_exists"])
            self.assertEqual(packetized["coding_checker_type"], "continuous_public_simulator")

    def test_parse_question_file_uses_catalog_and_problem_section(self) -> None:
        from grading_methods.simple_grade_v1 import build_task_prompt, parse_question_file

        question_case = parse_question_file(
            REPO_ROOT
            / "data-system"
            / "grading"
            / "test-questions"
            / "architecture-derived-B6-binary-representation-minimization.md"
        )
        self.assertEqual(question_case.grader_type, "exact_numeric")
        self.assertIn("Find the minimum", question_case.sections["problem"])

        prompt = build_task_prompt(question_case)
        self.assertIn("Problem:", prompt)
        self.assertNotIn("Question:\n", prompt)

    def test_write_and_reload_catalog(self) -> None:
        from question_bank_v1 import load_question_bank_catalog, write_question_bank_catalog

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "question-bank-v1.json"
            write_question_bank_catalog(output_path=output)
            self.assertTrue(output.exists())
            loaded = load_question_bank_catalog(output_path=output)
            self.assertEqual(loaded["question_count"], 31)


if __name__ == "__main__":
    unittest.main()

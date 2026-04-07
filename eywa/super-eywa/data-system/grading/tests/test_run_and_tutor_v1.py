from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
RUN_QUESTION = REPO_ROOT / "data-system" / "grading" / "run_test_question_v1.py"
RUN_TUTOR = REPO_ROOT / "data-system" / "grading" / "run_tutor_v1.py"
QUESTION_FILE = (
    REPO_ROOT
    / "data-system"
    / "grading"
    / "test-questions"
    / "architecture-derived-B6-binary-representation-minimization.md"
)


def parse_stdout(stdout: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for line in stdout.splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        parsed[key.strip()] = value.strip()
    return parsed


class RunAndTutorV1Tests(unittest.TestCase):
    def test_run_question_grades_without_auto_tutor(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            run_root = Path(tmpdir)
            completed = subprocess.run(
                [
                    "python3",
                    str(RUN_QUESTION),
                    "--question-file",
                    str(QUESTION_FILE),
                    "--label",
                    "baseline",
                    "--runtime-provider",
                    "deterministic",
                    "--model",
                    "deterministic-local-v1",
                    "--run-history-root",
                    str(run_root / "run-history"),
                    "--grading-runs-root",
                    str(run_root / "grading-runs"),
                    "--max-depth",
                    "0",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            parsed = parse_stdout(completed.stdout)
            self.assertNotIn("review_record", parsed)
            self.assertIn("total_tokens", parsed)
            self.assertIn("total_wall_time_ms", parsed)
            self.assertIn("total_cost_usd", parsed)
            self.assertEqual(parsed["grader_provider"], "deterministic")
            self.assertEqual(parsed["grading_method"], "deterministic_reference_v1")

            grading_record_path = Path(parsed["grading_record"])
            grading_record = json.loads(grading_record_path.read_text(encoding="utf-8"))
            self.assertEqual(grading_record["question_id"], "architecture-derived-B6-binary-representation-minimization")
            self.assertIsNone(grading_record["tutor_record_path"])
            self.assertIsNone(grading_record["review_record_path"])
            self.assertNotIn("review", grading_record)
            self.assertIn("total_tokens", grading_record)
            self.assertIn("total_wall_time_ms", grading_record)
            self.assertIn("total_cost_usd", grading_record)
            self.assertEqual(grading_record["grader_provider"], "deterministic")
            self.assertEqual(grading_record["grading_method"], "deterministic_reference_v1")
            self.assertTrue(Path(grading_record["grading_trace_path"]).exists())

    def test_manual_tutor_writes_sidecar_and_links_grading_record(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            run_root = Path(tmpdir)
            completed = subprocess.run(
                [
                    "python3",
                    str(RUN_QUESTION),
                    "--question-file",
                    str(QUESTION_FILE),
                    "--label",
                    "baseline",
                    "--runtime-provider",
                    "deterministic",
                    "--model",
                    "deterministic-local-v1",
                    "--run-history-root",
                    str(run_root / "run-history"),
                    "--grading-runs-root",
                    str(run_root / "grading-runs"),
                    "--max-depth",
                    "0",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            grading_record_path = Path(parse_stdout(completed.stdout)["grading_record"])

            tutor_completed = subprocess.run(
                [
                    "python3",
                    str(RUN_TUTOR),
                    "--grading-record",
                    str(grading_record_path),
                    "--tutoring-root",
                    str(run_root / "tutoring"),
                    "--tutor-provider",
                    "deterministic",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            tutor_parsed = parse_stdout(tutor_completed.stdout)
            tutor_record_path = Path(tutor_parsed["tutor_record"])
            self.assertTrue(tutor_record_path.exists())

            grading_record = json.loads(grading_record_path.read_text(encoding="utf-8"))
            self.assertEqual(grading_record["tutor_record_path"], str(tutor_record_path))

            tutor_record = json.loads(tutor_record_path.read_text(encoding="utf-8"))
            self.assertEqual(tutor_record["question_id"], grading_record["question_id"])
            self.assertEqual(tutor_record["run_id"], grading_record["run_id"])
            self.assertIn("review", tutor_record)


if __name__ == "__main__":
    unittest.main()

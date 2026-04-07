from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[3]
GRADING_DIR = REPO_ROOT / "data-system" / "grading"
if str(GRADING_DIR) not in sys.path:
    sys.path.insert(0, str(GRADING_DIR))


QUESTION_FILE = (
    REPO_ROOT
    / "data-system"
    / "grading"
    / "test-questions"
    / "coding-B1-usaco-2024-us-open-platinum-identity-theft.md"
)


class RunTestQuestionCodingV1Tests(unittest.TestCase):
    def test_coding_question_runs_with_harness_backed_grade(self) -> None:
        from run_test_question_v1 import run_question_case

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = Path(tmpdir)
            record = run_question_case(
                question_path=QUESTION_FILE,
                label="coding_harness_smoke",
                runtime_provider="deterministic",
                model="deterministic-local-v1",
                run_history_root=tmp_root / "run-history",
                grading_runs_root=tmp_root / "grading-runs",
                max_depth=0,
                max_helpers=0,
                run_id="coding_harness_smoke_run",
                grading_provider="deterministic",
                grading_model="deterministic-agent-grader-v1",
                sync_supabase=False,
            )

            self.assertEqual(record["grading"]["grading_status"], "graded")
            self.assertFalse(record["grading"]["correct"])
            self.assertEqual(record["grading"]["score"], 0.0)
            self.assertTrue(record["submission_artifact_refs"])
            self.assertIsInstance(record["coding_execution"], dict)


if __name__ == "__main__":
    unittest.main()

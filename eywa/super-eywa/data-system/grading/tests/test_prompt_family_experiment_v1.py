from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
RUNNER = REPO_ROOT / "data-system" / "grading" / "run_prompt_family_experiment_v1.py"


class PromptFamilyExperimentV1Tests(unittest.TestCase):
    def test_deterministic_experiment_writes_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            run_root = Path(tmpdir)
            completed = subprocess.run(
                [
                    "python3",
                    str(RUNNER),
                    "--runtime-provider",
                    "deterministic",
                    "--model",
                    "deterministic-local-v1",
                    "--run-history-root",
                    str(run_root / "run-history"),
                    "--grading-runs-root",
                    str(run_root / "grading-runs"),
                    "--experiment-runs-root",
                    str(run_root / "experiment-runs"),
                    "--experiment-label",
                    "test",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            parsed = {}
            for line in completed.stdout.splitlines():
                if "=" not in line:
                    continue
                key, value = line.split("=", 1)
                parsed[key] = value

            summary_path = Path(parsed["summary_path"])
            self.assertTrue(summary_path.exists())

            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            self.assertEqual(summary["benchmark"]["benchmark_id"], "transmute-three-failures-v1")
            self.assertEqual(len(summary["question_results"]), 3)
            self.assertEqual(summary["variants"]["baseline_execute"]["prompt_family"], "execute")
            self.assertEqual(summary["variants"]["transmute_candidate"]["prompt_family"], "transmute")
            for question_result in summary["question_results"]:
                self.assertEqual(question_result["baseline_execute"]["root_variables"]["prompt_family"], "execute")
                self.assertEqual(question_result["transmute_candidate"]["root_variables"]["prompt_family"], "transmute")
                self.assertIsNone(question_result["baseline_execute"]["tutor_record_path"])
                self.assertIsNone(question_result["transmute_candidate"]["tutor_record_path"])
                self.assertEqual(
                    question_result["transmute_candidate"]["root_orchestration"]["final_decision"],
                    "transmute",
                )


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
RUN_SWEEP = REPO_ROOT / "data-system" / "grading" / "run_mx1_sweep_v1.py"
QUESTION_ID = "architecture-derived-B6-binary-representation-minimization"


class MX1SweepV1Tests(unittest.TestCase):
    def test_review_family_sweep_runs_two_iterations_deterministically(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            benchmark_path = root / "benchmark.json"
            benchmark_path.write_text(
                json.dumps(
                    {
                        "benchmark_id": "test-sweep",
                        "schema_name": "mx1_benchmark_manifest",
                        "schema_version": "v1",
                        "questions": [{"question_id": QUESTION_ID}],
                        "families": ["review"],
                        "iterations_target": 2,
                        "exploration_iterations": 1,
                        "runtime_provider": "deterministic",
                        "model": "deterministic-local-v1"
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )

            completed = subprocess.run(
                [
                    "python3",
                    str(RUN_SWEEP),
                    "--benchmark-file",
                    str(benchmark_path),
                    "--loop-label",
                    "test",
                    "--question-id",
                    QUESTION_ID,
                    "--family",
                    "review",
                    "--loops-root",
                    str(root / "mx1-loops"),
                    "--run-history-root",
                    str(root / "run-history"),
                    "--grading-runs-root",
                    str(root / "grading-runs"),
                    "--tutoring-root",
                    str(root / "mx1-tutoring"),
                    "--runtime-provider",
                    "deterministic",
                    "--model",
                    "deterministic-local-v1",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            summary = json.loads(completed.stdout)
            self.assertEqual(len(summary["completed_loops"]), 1)
            loop = summary["completed_loops"][0]
            self.assertEqual(loop["family"], "review")
            self.assertEqual(loop["iterations_completed"], 2)
            manifest = json.loads(Path(loop["manifest_path"]).read_text(encoding="utf-8"))
            self.assertEqual(manifest["family"], "review")
            self.assertEqual(manifest["history_summary"]["iterations_completed"], 2)


if __name__ == "__main__":
    unittest.main()

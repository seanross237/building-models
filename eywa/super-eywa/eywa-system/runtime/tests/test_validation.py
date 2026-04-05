from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
RUNNER = REPO_ROOT / "eywa-system" / "runtime" / "run_v1.py"
VALIDATOR = REPO_ROOT / "data-system" / "correctness-suite" / "validate_run_v1.py"


class ValidationTests(unittest.TestCase):
    def test_validator_accepts_generated_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            run_root = Path(tmpdir)
            subprocess.run(
                [
                    "python3",
                    str(RUNNER),
                    "--task",
                    "Plan the backend and implement the frontend.",
                    "--run-id",
                    "run_validation_test",
                    "--run-history-root",
                    str(run_root),
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            completed = subprocess.run(
                [
                    "python3",
                    str(VALIDATOR),
                    str(run_root / "run_validation_test"),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertIn("valid run: run_validation_test", completed.stdout)


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path
import json


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
                    "--runtime-provider",
                    "deterministic",
                    "--model",
                    "deterministic-local-v1",
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

    def test_validator_rejects_invalid_authored_response_in_replay(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            run_root = Path(tmpdir)
            subprocess.run(
                [
                    "python3",
                    str(RUNNER),
                    "--task",
                    "Plan the backend and implement the frontend.",
                    "--run-id",
                    "run_validation_bad_replay",
                    "--run-history-root",
                    str(run_root),
                    "--runtime-provider",
                    "deterministic",
                    "--model",
                    "deterministic-local-v1",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            raw_model_path = (
                run_root
                / "run_validation_bad_replay"
                / "replay"
                / "node_root"
                / "raw-model.json"
            )
            raw_model = json.loads(raw_model_path.read_text(encoding="utf-8"))
            raw_model["steps"][0]["authored_response"].pop("orchestration_decision", None)
            raw_model_path.write_text(json.dumps(raw_model, indent=2), encoding="utf-8")

            completed = subprocess.run(
                [
                    "python3",
                    str(VALIDATOR),
                    str(run_root / "run_validation_bad_replay"),
                ],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("node_authored_response missing required keys", completed.stdout)


if __name__ == "__main__":
    unittest.main()

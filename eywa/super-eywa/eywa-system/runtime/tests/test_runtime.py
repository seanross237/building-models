from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
RUNNER = REPO_ROOT / "eywa-system" / "runtime" / "run_v1.py"


class RuntimeTests(unittest.TestCase):
    def test_single_node_run_writes_expected_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            cmd = [
                "python3",
                str(RUNNER),
                "--task",
                "Write a short summary about feature X.",
                "--run-id",
                "run_test_single",
                "--run-history-root",
                tmpdir,
            ]
            completed = subprocess.run(cmd, check=True, capture_output=True, text=True)
            self.assertIn("run_id=run_test_single", completed.stdout)

            run_dir = Path(tmpdir) / "run_test_single"
            self.assertTrue((run_dir / "run_packet.json").exists())
            self.assertTrue((run_dir / "run_summary.json").exists())
            self.assertTrue((run_dir / "nodes" / "node_root" / "node_packet.json").exists())
            self.assertTrue((run_dir / "nodes" / "node_root" / "node_record.json").exists())
            self.assertTrue((run_dir / "derived" / "timeline.md").exists())

            summary = json.loads((run_dir / "run_summary.json").read_text(encoding="utf-8"))
            self.assertEqual(summary["node_count"], 1)

    def test_decomposition_creates_helpers(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            cmd = [
                "python3",
                str(RUNNER),
                "--task",
                "Design the backend and build the frontend and validate the feature.",
                "--run-id",
                "run_test_helpers",
                "--run-history-root",
                tmpdir,
            ]
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            run_dir = Path(tmpdir) / "run_test_helpers"
            summary = json.loads((run_dir / "run_summary.json").read_text(encoding="utf-8"))
            self.assertGreater(summary["node_count"], 1)
            self.assertTrue((run_dir / "nodes" / "node_root_helper_01" / "node_record.json").exists())
            self.assertTrue((run_dir / "nodes" / "node_root_helper_02" / "node_record.json").exists())


if __name__ == "__main__":
    unittest.main()

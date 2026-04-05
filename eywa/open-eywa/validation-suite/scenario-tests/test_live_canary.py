from __future__ import annotations

import json
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from system.orchestrator import (
    LiveCanaryConfig,
    NodeProgressionEngine,
    build_default_live_canary_mission_path,
    run_live_canary,
)
from system.runtime import SimulatedRuntime, load_scenario

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


class LiveCanaryScenarioTests(unittest.TestCase):
    def test_build_default_live_canary_mission_path_is_stable_and_readable(self) -> None:
        mission_path = build_default_live_canary_mission_path(
            PROJECT_ROOT,
            label="My Tiny Canary",
            now=datetime(2026, 4, 1, 15, 4, 5),
        )
        self.assertEqual(
            mission_path,
            PROJECT_ROOT / "missions" / "live-canaries" / "20260401-150405-my-tiny-canary",
        )

    def test_build_default_live_canary_mission_path_avoids_existing_path_collisions(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir).resolve()
            existing = (
                project_root
                / "missions"
                / "live-canaries"
                / "20260401-150405-my-tiny-canary"
            )
            existing.mkdir(parents=True)

            mission_path = build_default_live_canary_mission_path(
                project_root,
                label="My Tiny Canary",
                now=datetime(2026, 4, 1, 15, 4, 5),
            )

            self.assertEqual(
                mission_path,
                project_root
                / "missions"
                / "live-canaries"
                / "20260401-150405-my-tiny-canary-001",
            )

    def test_run_live_canary_with_worker_root_completes_cleanly(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            mission_path = Path(temp_dir) / "canary"
            runtime = SimulatedRuntime(
                {"worker_success": load_scenario(FIXTURES_DIR / "worker_success.json")}
            )

            def resolver(mission_id: str, node_id: str, role: str, node_root: Path) -> dict[str, str]:
                del mission_id, node_id, node_root
                if role == "worker":
                    return {"scenario_name": "worker_success"}
                raise AssertionError(f"Unexpected role: {role}")

            result = run_live_canary(
                NodeProgressionEngine(runtime, runtime_metadata_resolver=resolver),
                LiveCanaryConfig(
                    mission_path=str(mission_path),
                    goal_text="Write a tiny operator note.",
                    root_agent_mode="worker",
                    mission_id="live-canary-001",
                ),
            )

            self.assertEqual(result.final_status, "finished")
            self.assertEqual(result.terminal_outcome, "completed")
            summary = json.loads((mission_path / "system" / "mission-summary.json").read_text(encoding="utf-8"))
            self.assertEqual(summary["final_status"], "finished")
            self.assertEqual(summary["terminal_outcome"], "completed")
            self.assertEqual(summary["run_count"], 1)
            self.assertTrue((mission_path / "tree" / "root" / "output" / "final-output.md").exists())


if __name__ == "__main__":
    unittest.main()

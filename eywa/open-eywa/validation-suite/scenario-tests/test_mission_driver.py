from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from system.orchestrator import MissionDriver, NodeProgressionEngine, cancel_node, create_mission
from system.runtime import SimulatedRuntime, load_scenario

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


class MissionDriverScenarioTests(unittest.TestCase):
    def test_mission_driver_runs_root_tree_and_writes_summary(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            mission_path = Path(temp_dir) / "mission-001"
            create_mission(mission_path, goal_text="Complete the mission.")

            runtime = SimulatedRuntime(
                {
                    "planner_success": load_scenario(FIXTURES_DIR / "planner_success.json"),
                    "worker_success": load_scenario(FIXTURES_DIR / "worker_success.json"),
                    "evaluator_continue": load_scenario(FIXTURES_DIR / "evaluator_continue.json"),
                    "synthesizer_success": load_scenario(FIXTURES_DIR / "synthesizer_success.json"),
                }
            )

            def resolver(mission_id: str, node_id: str, role: str, node_root: Path) -> dict[str, str]:
                del mission_id, node_id, node_root
                if role == "planner":
                    return {"scenario_name": "planner_success"}
                if role == "worker":
                    return {"scenario_name": "worker_success"}
                if role == "mid-plan-evaluator":
                    return {"scenario_name": "evaluator_continue"}
                if role == "synthesizer":
                    return {"scenario_name": "synthesizer_success"}
                raise AssertionError(f"Unexpected role: {role}")

            result = MissionDriver(
                NodeProgressionEngine(runtime, runtime_metadata_resolver=resolver)
            ).drive_until_stable(mission_path, mission_id="mission-001")

            self.assertEqual(result.final_status, "finished")
            self.assertEqual(result.terminal_outcome, "completed")

            summary = json.loads(
                (mission_path / "system" / "mission-summary.json").read_text(encoding="utf-8")
            )
            self.assertEqual(summary["final_status"], "finished")
            self.assertEqual(summary["terminal_outcome"], "completed")
            self.assertEqual(summary["node_count"], 3)
            self.assertEqual(summary["cancelled_node_count"], 0)
            self.assertGreater(summary["run_count"], 0)

            events = [
                json.loads(line)
                for line in (mission_path / "system" / "mission-events.jsonl")
                .read_text(encoding="utf-8")
                .splitlines()
                if line.strip()
            ]
            event_types = [event["event_type"] for event in events]
            self.assertEqual(event_types[0], "mission_drive_started")
            self.assertEqual(event_types[-1], "mission_drive_completed")

    def test_mission_driver_summarizes_cancelled_root_node(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            mission_path = Path(temp_dir) / "mission-002"
            mission_layout = create_mission(mission_path, goal_text="Cancelled mission.")
            cancel_node(
                mission_layout.root_node_dir,
                cancellation_reason="Mission superseded by a newer variant.",
            )

            result = MissionDriver(NodeProgressionEngine(SimulatedRuntime({}))).drive_until_stable(
                mission_path,
                mission_id="mission-002",
            )

            self.assertEqual(result.final_status, "finished")
            self.assertEqual(result.terminal_outcome, "cancelled")
            summary = json.loads(
                (mission_path / "system" / "mission-summary.json").read_text(encoding="utf-8")
            )
            self.assertEqual(summary["cancelled_node_count"], 1)
            self.assertEqual(summary["terminal_outcome"], "cancelled")


if __name__ == "__main__":
    unittest.main()

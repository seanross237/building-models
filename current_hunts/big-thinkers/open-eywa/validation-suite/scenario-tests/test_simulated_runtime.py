from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from system.orchestrator.node_contract import create_node
from system.runtime import RuntimeRequest, SimulatedRuntime, SimulatedRuntimeError, load_scenario

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


class SimulatedRuntimeScenarioTests(unittest.TestCase):
    def test_scenario_loader_reads_json_fixture(self) -> None:
        scenario = load_scenario(FIXTURES_DIR / "planner_success.json")

        self.assertEqual(scenario.name, "planner_success")
        self.assertEqual(len(scenario.actions), 2)
        self.assertEqual(scenario.exit_reason, "completed")

    def test_simulated_runtime_executes_success_scenario(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            node_path = Path(temp_dir) / "root"
            create_node(node_path, task_source_name="goal", task_text="Make a plan.")

            runtime = SimulatedRuntime(
                {"planner_success": load_scenario(FIXTURES_DIR / "planner_success.json")}
            )
            result = runtime.run(
                RuntimeRequest(
                    mission_id="mission-001",
                    node_id="root",
                    node_path=str(node_path),
                    run_id="run-001",
                    role="planner",
                    model="simulated-model",
                    metadata={"scenario_name": "planner_success"},
                )
            )

            self.assertEqual(result.exit_reason, "completed")
            self.assertIn("output/plan.md", result.artifacts_produced)
            self.assertTrue((node_path / "output" / "plan.md").exists())
            self.assertEqual(result.to_run_summary().usage.total_tokens, 30)
            self.assertEqual(result.details["prepared_inputs"], [])

    def test_simulated_runtime_can_represent_missing_artifact_behavior(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            node_path = Path(temp_dir) / "root"
            create_node(node_path, task_source_name="goal", task_text="Write the output.")

            runtime = SimulatedRuntime(
                {"missing_artifact": load_scenario(FIXTURES_DIR / "missing_artifact.json")}
            )
            result = runtime.run(
                RuntimeRequest(
                    mission_id="mission-001",
                    node_id="root",
                    node_path=str(node_path),
                    run_id="run-002",
                    role="worker",
                    metadata={"scenario_name": "missing_artifact"},
                )
            )

            self.assertEqual(result.exit_reason, "completed")
            self.assertNotIn("output/final-output.md", result.artifacts_produced)
            self.assertFalse((node_path / "output" / "final-output.md").exists())
            self.assertTrue((node_path / "output" / "state.md").exists())

    def test_simulated_runtime_rejects_writes_outside_node_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            node_path = Path(temp_dir) / "root"
            create_node(node_path, task_source_name="goal", task_text="Stay in bounds.")

            runtime = SimulatedRuntime(
                {
                    "invalid_write_outside_node": load_scenario(
                        FIXTURES_DIR / "invalid_write_outside_node.json"
                    )
                }
            )

            with self.assertRaises(SimulatedRuntimeError):
                runtime.run(
                    RuntimeRequest(
                        mission_id="mission-001",
                        node_id="root",
                        node_path=str(node_path),
                        run_id="run-003",
                        role="worker",
                        metadata={"scenario_name": "invalid_write_outside_node"},
                    )
                )

    def test_simulated_runtime_can_execute_real_file_tools(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            node_path = Path(temp_dir) / "root"
            create_node(node_path, task_source_name="goal", task_text="Use file tools.")

            runtime = SimulatedRuntime(
                {"tool_write_final_output": load_scenario(FIXTURES_DIR / "tool_write_final_output.json")}
            )

            result = runtime.run(
                RuntimeRequest(
                    mission_id="mission-001",
                    node_id="root",
                    node_path=str(node_path),
                    run_id="run-004",
                    role="worker",
                    metadata={"scenario_name": "tool_write_final_output"},
                )
            )

            self.assertEqual(result.exit_reason, "completed")
            self.assertEqual(result.tool_call_count, 2)
            self.assertTrue((node_path / "output" / "final-output.md").exists())
            self.assertIn("output/final-output.md", result.artifacts_produced)
            self.assertEqual(result.details["tool_results"][1]["output"]["content"], "# Tool Output\n\nCreated through the file tool layer.\n")


if __name__ == "__main__":
    unittest.main()

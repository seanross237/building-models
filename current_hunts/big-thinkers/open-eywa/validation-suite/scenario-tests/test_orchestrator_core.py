from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from system.orchestrator import NodeOrchestratorCore, create_node, validate_node
from system.orchestrator.node_contract import read_trimmed_text
from system.runtime import SimulatedRuntime, load_scenario

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


class OrchestratorCoreScenarioTests(unittest.TestCase):
    def test_planner_success_keeps_node_active_and_records_run(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            node_path = Path(temp_dir) / "root"
            create_node(
                node_path,
                task_source_name="goal",
                task_text="Make a plan.",
                agent_mode="planner",
            )
            runtime = SimulatedRuntime(
                {"planner_success": load_scenario(FIXTURES_DIR / "planner_success.json")}
            )

            result = NodeOrchestratorCore(runtime).run_once(
                node_path,
                mission_id="mission-001",
                node_id="root",
                runtime_metadata={"scenario_name": "planner_success"},
            )

            self.assertEqual(result.status_after, "active")
            self.assertTrue((node_path / "output" / "plan.md").exists())
            self.assertTrue((node_path / "system" / "runs" / "run-001" / "summary.json").exists())
            request_json = json.loads(
                (node_path / "system" / "runs" / "run-001" / "request.json").read_text(
                    encoding="utf-8"
                )
            )
            prepared_inputs = request_json["prepared_inputs"]
            self.assertEqual(len(prepared_inputs), 1)
            self.assertTrue(Path(prepared_inputs[0]).exists())
            self.assertTrue((node_path / "system" / "events.jsonl").exists())
            self.assertTrue(validate_node(node_path).is_valid)

    def test_worker_success_completes_the_node(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            node_path = Path(temp_dir) / "root"
            create_node(
                node_path,
                task_source_name="goal",
                task_text="Finish the work.",
                agent_mode="worker",
            )
            runtime = SimulatedRuntime(
                {"worker_success": load_scenario(FIXTURES_DIR / "worker_success.json")}
            )

            result = NodeOrchestratorCore(runtime).run_once(
                node_path,
                mission_id="mission-001",
                node_id="root",
                runtime_metadata={"scenario_name": "worker_success"},
            )

            self.assertEqual(result.status_after, "finished")
            self.assertEqual(result.terminal_outcome, "completed")
            self.assertEqual(
                read_trimmed_text(node_path / "for-orchestrator" / "terminal-outcome"),
                "completed",
            )
            usage_summary = json.loads(
                (node_path / "system" / "usage-summary.json").read_text(encoding="utf-8")
            )
            self.assertEqual(usage_summary["total_tokens"], 35)
            self.assertTrue(validate_node(node_path).is_valid)

    def test_missing_required_artifact_fails_the_node(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            node_path = Path(temp_dir) / "root"
            create_node(
                node_path,
                task_source_name="goal",
                task_text="Write the output.",
                agent_mode="worker",
            )
            runtime = SimulatedRuntime(
                {"missing_artifact": load_scenario(FIXTURES_DIR / "missing_artifact.json")}
            )

            result = NodeOrchestratorCore(runtime).run_once(
                node_path,
                mission_id="mission-001",
                node_id="root",
                runtime_metadata={"scenario_name": "missing_artifact"},
            )

            self.assertEqual(result.status_after, "failed")
            self.assertEqual(result.failure_reason, "missing_required_artifact")
            self.assertEqual(
                read_trimmed_text(node_path / "for-orchestrator" / "failure-reason"),
                "missing_required_artifact",
            )
            self.assertTrue(validate_node(node_path).is_valid)

    def test_worker_can_move_node_into_waiting_on_computation(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            node_path = Path(temp_dir) / "root"
            create_node(
                node_path,
                task_source_name="goal",
                task_text="Do a long job.",
                agent_mode="worker",
            )
            runtime = SimulatedRuntime(
                {
                    "waiting_for_computation": load_scenario(
                        FIXTURES_DIR / "waiting_for_computation.json"
                    )
                }
            )

            result = NodeOrchestratorCore(runtime).run_once(
                node_path,
                mission_id="mission-001",
                node_id="root",
                runtime_metadata={"scenario_name": "waiting_for_computation"},
            )

            self.assertEqual(result.status_after, "waiting_on_computation")
            self.assertTrue(
                (node_path / "for-orchestrator" / "WAITING_FOR_COMPUTATION").exists()
            )
            self.assertTrue(validate_node(node_path).is_valid)

    def test_worker_escalation_marks_terminal_escalated_state(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            node_path = Path(temp_dir) / "root"
            create_node(
                node_path,
                task_source_name="goal",
                task_text="Try but escalate if blocked.",
                agent_mode="worker",
            )
            runtime = SimulatedRuntime(
                {"escalation": load_scenario(FIXTURES_DIR / "escalation.json")}
            )

            result = NodeOrchestratorCore(runtime).run_once(
                node_path,
                mission_id="mission-001",
                node_id="root",
                runtime_metadata={"scenario_name": "escalation"},
            )

            self.assertEqual(result.status_after, "finished")
            self.assertEqual(result.terminal_outcome, "escalated")
            self.assertEqual(
                read_trimmed_text(node_path / "for-orchestrator" / "terminal-outcome"),
                "escalated",
            )
            self.assertTrue(validate_node(node_path).is_valid)

    def test_worker_can_complete_via_real_file_tool_calls(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            node_path = Path(temp_dir) / "root"
            create_node(
                node_path,
                task_source_name="goal",
                task_text="Finish via file tools.",
                agent_mode="worker",
            )
            runtime = SimulatedRuntime(
                {
                    "tool_write_final_output": load_scenario(
                        FIXTURES_DIR / "tool_write_final_output.json"
                    )
                }
            )

            result = NodeOrchestratorCore(runtime).run_once(
                node_path,
                mission_id="mission-001",
                node_id="root",
                runtime_metadata={"scenario_name": "tool_write_final_output"},
            )

            self.assertEqual(result.status_after, "finished")
            self.assertEqual(result.terminal_outcome, "completed")
            self.assertEqual(result.run_summary.tool_call_count, 2)
            events = [
                json.loads(line)
                for line in (node_path / "system" / "events.jsonl").read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            event_types = {event["event_type"] for event in events}
            self.assertIn("tool_called", event_types)
            self.assertIn("tool_finished", event_types)
            self.assertTrue(validate_node(node_path).is_valid)


if __name__ == "__main__":
    unittest.main()

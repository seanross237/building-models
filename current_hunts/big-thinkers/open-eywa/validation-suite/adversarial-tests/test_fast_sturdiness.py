from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from system.orchestrator import (
    MissionDriver,
    MissionDriverError,
    NodeOrchestratorCore,
    NodeProgressionEngine,
    OrchestratorProgressionError,
    create_mission,
    create_node,
)
from system.orchestrator.node_contract import read_trimmed_text
from system.runtime import SimulatedRuntime, load_scenario

FIXTURES_DIR = PROJECT_ROOT / "validation-suite" / "scenario-tests" / "fixtures"


def _event_types(path: Path) -> list[str]:
    return [
        json.loads(line)["event_type"]
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


class FastAdversarialSturdinessTests(unittest.TestCase):
    def test_runtime_failure_is_explicit_and_records_run_failed_event(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            node_path = Path(temp_dir) / "root"
            create_node(
                node_path,
                task_source_name="goal",
                task_text="Fail explicitly when the runtime fails.",
                agent_mode="worker",
            )
            runtime = SimulatedRuntime(
                {"runtime_failed": load_scenario(FIXTURES_DIR / "runtime_failed.json")}
            )

            result = NodeOrchestratorCore(runtime).run_once(
                node_path,
                mission_id="mission-adv-001",
                node_id="root",
                runtime_metadata={"scenario_name": "runtime_failed"},
            )

            self.assertEqual(result.status_after, "failed")
            self.assertEqual(result.failure_reason, "runtime_failed")
            self.assertEqual(
                read_trimmed_text(node_path / "for-orchestrator" / "failure-reason"),
                "runtime_failed",
            )
            self.assertIn("run_failed", _event_types(node_path / "system" / "events.jsonl"))

    def test_invalid_evaluator_decision_value_fails_cleanly(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            node_path = Path(temp_dir) / "root"
            create_node(
                node_path,
                task_source_name="goal",
                task_text="Reject invalid evaluator control values.",
                agent_mode="mid-plan-evaluator",
            )
            runtime = SimulatedRuntime(
                {
                    "invalid_evaluator_decision": load_scenario(
                        FIXTURES_DIR / "invalid_evaluator_decision.json"
                    )
                }
            )

            result = NodeOrchestratorCore(runtime).run_once(
                node_path,
                mission_id="mission-adv-002",
                node_id="root",
                runtime_metadata={"scenario_name": "invalid_evaluator_decision"},
            )

            self.assertEqual(result.status_after, "failed")
            self.assertEqual(result.failure_reason, "invalid_decision_value")
            self.assertEqual(
                read_trimmed_text(node_path / "for-orchestrator" / "failure-reason"),
                "invalid_decision_value",
            )
            self.assertIn("node_failed", _event_types(node_path / "system" / "events.jsonl"))

    def test_tool_boundary_violation_stays_inside_runtime_failure_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            node_path = temp_root / "root"
            escaped_target = temp_root / "escape.txt"
            create_node(
                node_path,
                task_source_name="goal",
                task_text="Do not let tools escape node boundaries.",
                agent_mode="worker",
            )
            runtime = SimulatedRuntime(
                {
                    "tool_write_outside_node": load_scenario(
                        FIXTURES_DIR / "tool_write_outside_node.json"
                    )
                }
            )

            result = NodeOrchestratorCore(runtime).run_once(
                node_path,
                mission_id="mission-adv-003",
                node_id="root",
                runtime_metadata={"scenario_name": "tool_write_outside_node"},
            )

            self.assertEqual(result.status_after, "failed")
            self.assertEqual(result.failure_reason, "runtime_failed")
            self.assertFalse(escaped_target.exists())
            event_types = _event_types(node_path / "system" / "events.jsonl")
            self.assertIn("tool_called", event_types)
            self.assertIn("tool_failed", event_types)

    def test_missing_next_action_after_child_report_raises_explicit_progression_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            node_path = Path(temp_dir) / "root"
            create_node(
                node_path,
                task_source_name="goal",
                task_text="Require explicit evaluator next action.",
            )
            runtime = SimulatedRuntime(
                {
                    "planner_success": load_scenario(FIXTURES_DIR / "planner_success.json"),
                    "worker_success": load_scenario(FIXTURES_DIR / "worker_success.json"),
                    "evaluator_missing_next_action": load_scenario(
                        FIXTURES_DIR / "evaluator_missing_next_action.json"
                    ),
                }
            )

            def resolver(
                mission_id: str, node_id: str, role: str, node_root: Path
            ) -> dict[str, str]:
                del mission_id, node_id, node_root
                if role == "planner":
                    return {"scenario_name": "planner_success"}
                if role == "worker":
                    return {"scenario_name": "worker_success"}
                if role == "mid-plan-evaluator":
                    return {"scenario_name": "evaluator_missing_next_action"}
                raise AssertionError(f"Unexpected role: {role}")

            engine = NodeProgressionEngine(runtime, runtime_metadata_resolver=resolver)

            with self.assertRaisesRegex(
                OrchestratorProgressionError,
                "Evaluator completed without next-action-after-child-report",
            ):
                engine.drive_until_stable(
                    node_path,
                    mission_id="mission-adv-004",
                    node_id="root",
                )

    def test_mission_driver_records_failed_drive_for_malformed_plan(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            mission_path = Path(temp_dir) / "mission"
            create_mission(
                mission_path,
                goal_text="Mission should fail explicitly on malformed plan output.",
            )
            runtime = SimulatedRuntime(
                {
                    "malformed_plan_no_steps": load_scenario(
                        FIXTURES_DIR / "malformed_plan_no_steps.json"
                    )
                }
            )

            def resolver(
                mission_id: str, node_id: str, role: str, node_root: Path
            ) -> dict[str, str]:
                del mission_id, node_id, node_root
                if role == "planner":
                    return {"scenario_name": "malformed_plan_no_steps"}
                raise AssertionError(f"Unexpected role: {role}")

            driver = MissionDriver(
                NodeProgressionEngine(runtime, runtime_metadata_resolver=resolver)
            )

            with self.assertRaises(MissionDriverError):
                driver.drive_until_stable(
                    mission_path,
                    mission_id="mission-adv-005",
                )

            event_types = _event_types(mission_path / "system" / "mission-events.jsonl")
            self.assertIn("mission_drive_started", event_types)
            self.assertIn("mission_drive_failed", event_types)
            self.assertNotIn("mission_drive_completed", event_types)


if __name__ == "__main__":
    unittest.main()

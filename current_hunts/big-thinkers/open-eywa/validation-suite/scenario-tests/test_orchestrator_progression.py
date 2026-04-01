from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from system.orchestrator import NodeProgressionEngine, create_node
from system.orchestrator import prepare_node_for_fresh_attempt, record_computation_result
from system.orchestrator.node_contract import node_layout, read_trimmed_text
from system.runtime import SimulatedRuntime, load_scenario

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


class OrchestratorProgressionScenarioTests(unittest.TestCase):
    def test_parent_node_progresses_through_plan_children_evaluation_and_synthesis(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            node_path = Path(temp_dir) / "root"
            create_node(node_path, task_source_name="goal", task_text="Solve the whole task.")

            runtime = SimulatedRuntime(
                {
                    "planner_success": load_scenario(FIXTURES_DIR / "planner_success.json"),
                    "worker_success": load_scenario(FIXTURES_DIR / "worker_success.json"),
                    "evaluator_continue": load_scenario(FIXTURES_DIR / "evaluator_continue.json"),
                    "synthesizer_success": load_scenario(FIXTURES_DIR / "synthesizer_success.json"),
                }
            )

            def resolver(mission_id: str, node_id: str, role: str, node_root: Path) -> dict[str, str]:
                if role == "planner":
                    return {"scenario_name": "planner_success"}
                if role == "worker":
                    return {"scenario_name": "worker_success"}
                if role == "mid-plan-evaluator":
                    return {"scenario_name": "evaluator_continue"}
                if role == "synthesizer":
                    return {"scenario_name": "synthesizer_success"}
                raise AssertionError(f"Unexpected role: {role}")

            result = NodeProgressionEngine(
                runtime,
                runtime_metadata_resolver=resolver,
            ).drive_until_stable(
                node_path,
                mission_id="mission-001",
                node_id="root",
            )

            self.assertEqual(result.final_status, "finished")
            self.assertEqual(result.terminal_outcome, "completed")
            self.assertTrue((node_path / "output" / "final-output.md").exists())

            child_dirs = sorted((node_path / "children").iterdir())
            self.assertEqual(len(child_dirs), 2)
            for child_dir in child_dirs:
                self.assertEqual(
                    read_trimmed_text(child_dir / "for-orchestrator" / "this-nodes-current-status"),
                    "finished",
                )
                self.assertEqual(
                    read_trimmed_text(child_dir / "for-orchestrator" / "terminal-outcome"),
                    "completed",
                )

            progress_state = json.loads(
                (node_path / "system" / "progression-state.json").read_text(encoding="utf-8")
            )
            self.assertEqual(progress_state["current_step_index"], 2)

    def test_replan_decision_resets_parent_plan_state(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            node_path = Path(temp_dir) / "root"
            create_node(node_path, task_source_name="goal", task_text="Need another plan.")

            runtime = SimulatedRuntime(
                {
                    "planner_success": load_scenario(FIXTURES_DIR / "planner_success.json"),
                    "worker_success": load_scenario(FIXTURES_DIR / "worker_success.json"),
                    "replan": load_scenario(FIXTURES_DIR / "replan.json"),
                }
            )

            def resolver(mission_id: str, node_id: str, role: str, node_root: Path) -> dict[str, str]:
                if role == "planner":
                    return {"scenario_name": "planner_success"}
                if role == "worker":
                    return {"scenario_name": "worker_success"}
                if role == "mid-plan-evaluator":
                    return {"scenario_name": "replan"}
                raise AssertionError(f"Unexpected role: {role}")

            engine = NodeProgressionEngine(runtime, runtime_metadata_resolver=resolver)

            layout = node_layout(node_path)
            for _ in range(5):
                engine._advance_once(layout, mission_id="mission-001", node_id="root")

            self.assertFalse((node_path / "system" / "progression-state.json").exists())
            self.assertFalse((node_path / "output" / "plan.md").exists())
            self.assertEqual(
                read_trimmed_text(node_path / "for-orchestrator" / "agent-mode"),
                "planner",
            )
            self.assertTrue((node_path / "system" / "recoveries" / "recovery-001").exists())
            self.assertTrue(
                (
                    node_path
                    / "system"
                    / "recoveries"
                    / "recovery-001"
                    / "output"
                    / "plan.md"
                ).exists()
            )

    def test_child_failure_can_trigger_parent_escalation(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            node_path = Path(temp_dir) / "root"
            create_node(node_path, task_source_name="goal", task_text="Escalate on child failure.")

            runtime = SimulatedRuntime(
                {
                    "planner_success": load_scenario(FIXTURES_DIR / "planner_success.json"),
                    "missing_artifact": load_scenario(FIXTURES_DIR / "missing_artifact.json"),
                    "evaluator_escalate": load_scenario(FIXTURES_DIR / "evaluator_escalate.json"),
                }
            )

            def resolver(mission_id: str, node_id: str, role: str, node_root: Path) -> dict[str, str]:
                del mission_id, node_id, node_root
                if role == "planner":
                    return {"scenario_name": "planner_success"}
                if role == "worker":
                    return {"scenario_name": "missing_artifact"}
                if role == "mid-plan-evaluator":
                    return {"scenario_name": "evaluator_escalate"}
                raise AssertionError(f"Unexpected role: {role}")

            result = NodeProgressionEngine(
                runtime,
                runtime_metadata_resolver=resolver,
            ).drive_until_stable(
                node_path,
                mission_id="mission-001",
                node_id="root",
            )

            self.assertEqual(result.final_status, "finished")
            self.assertEqual(result.terminal_outcome, "escalated")
            self.assertTrue((node_path / "output" / "escalation.md").exists())

    def test_child_waiting_moves_parent_into_waiting_on_computation(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            node_path = Path(temp_dir) / "root"
            create_node(node_path, task_source_name="goal", task_text="Wait on child computation.")

            runtime = SimulatedRuntime(
                {
                    "planner_success": load_scenario(FIXTURES_DIR / "planner_success.json"),
                    "waiting_for_computation": load_scenario(
                        FIXTURES_DIR / "waiting_for_computation.json"
                    ),
                }
            )

            def resolver(mission_id: str, node_id: str, role: str, node_root: Path) -> dict[str, str]:
                del mission_id, node_id, node_root
                if role == "planner":
                    return {"scenario_name": "planner_success"}
                if role == "worker":
                    return {"scenario_name": "waiting_for_computation"}
                raise AssertionError(f"Unexpected role: {role}")

            result = NodeProgressionEngine(
                runtime,
                runtime_metadata_resolver=resolver,
            ).drive_until_stable(
                node_path,
                mission_id="mission-001",
                node_id="root",
            )

            self.assertEqual(result.final_status, "waiting_on_computation")
            self.assertEqual(
                read_trimmed_text(node_path / "for-orchestrator" / "this-nodes-current-status"),
                "waiting_on_computation",
            )

    def test_progression_emits_child_and_parent_decision_events(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            node_path = Path(temp_dir) / "root"
            create_node(node_path, task_source_name="goal", task_text="Track progression events.")

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

            NodeProgressionEngine(
                runtime,
                runtime_metadata_resolver=resolver,
            ).drive_until_stable(
                node_path,
                mission_id="mission-001",
                node_id="root",
            )

            events = [
                json.loads(line)
                for line in (node_path / "system" / "events.jsonl").read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            event_types = {event["event_type"] for event in events}
            self.assertIn("plan_parsed", event_types)
            self.assertIn("plan_step_registered", event_types)
            self.assertIn("child_node_created", event_types)
            self.assertIn("child_node_report_received", event_types)
            self.assertIn("parent_next_action_chosen", event_types)
            self.assertIn("plan_step_completed", event_types)

    def test_waiting_child_can_resume_and_parent_then_complete(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            node_path = Path(temp_dir) / "root"
            create_node(node_path, task_source_name="goal", task_text="Resume after waiting.")

            worker_call_count = {"count": 0}
            runtime = SimulatedRuntime(
                {
                    "planner_success": load_scenario(FIXTURES_DIR / "planner_success.json"),
                    "waiting_for_computation": load_scenario(
                        FIXTURES_DIR / "waiting_for_computation.json"
                    ),
                    "worker_success": load_scenario(FIXTURES_DIR / "worker_success.json"),
                    "evaluator_continue": load_scenario(FIXTURES_DIR / "evaluator_continue.json"),
                    "synthesizer_success": load_scenario(FIXTURES_DIR / "synthesizer_success.json"),
                }
            )

            def resolver(mission_id: str, node_id: str, role: str, node_root: Path) -> dict[str, str]:
                del mission_id, node_root
                if role == "planner":
                    return {"scenario_name": "planner_success"}
                if role == "worker":
                    worker_call_count["count"] += 1
                    if node_id.endswith("step-01-gather-the-facts") and worker_call_count["count"] == 1:
                        return {"scenario_name": "waiting_for_computation"}
                    return {"scenario_name": "worker_success"}
                if role == "mid-plan-evaluator":
                    return {"scenario_name": "evaluator_continue"}
                if role == "synthesizer":
                    return {"scenario_name": "synthesizer_success"}
                raise AssertionError(f"Unexpected role: {role}")

            engine = NodeProgressionEngine(runtime, runtime_metadata_resolver=resolver)
            first_result = engine.drive_until_stable(
                node_path,
                mission_id="mission-001",
                node_id="root",
            )
            self.assertEqual(first_result.final_status, "waiting_on_computation")

            child_path = node_path / "children" / "step-01-gather-the-facts"
            record_computation_result(child_path, result_text="Computation finished successfully.")

            final_result = engine.drive_until_stable(
                node_path,
                mission_id="mission-001",
                node_id="root",
            )
            self.assertEqual(final_result.final_status, "finished")
            self.assertEqual(final_result.terminal_outcome, "completed")

    def test_failed_leaf_node_can_be_prepared_for_retry_and_then_complete(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            node_path = Path(temp_dir) / "leaf"
            create_node(
                node_path,
                task_source_name="goal",
                task_text="Retry the worker node.",
                agent_mode="worker",
            )

            runtime = SimulatedRuntime(
                {
                    "missing_artifact": load_scenario(FIXTURES_DIR / "missing_artifact.json"),
                    "worker_success": load_scenario(FIXTURES_DIR / "worker_success.json"),
                }
            )
            core_engine = NodeProgressionEngine(
                runtime,
                runtime_metadata_resolver=lambda mission_id, node_id, role, node_root: {
                    "scenario_name": "missing_artifact"
                },
            )

            first_result = core_engine.drive_until_stable(
                node_path,
                mission_id="mission-001",
                node_id="leaf",
            )
            self.assertEqual(first_result.final_status, "failed")

            prepare_node_for_fresh_attempt(
                node_path,
                recovery_reason="Retry with better worker inputs.",
                next_role="worker",
                mission_id="mission-001",
                node_id="leaf",
            )

            success_engine = NodeProgressionEngine(
                runtime,
                runtime_metadata_resolver=lambda mission_id, node_id, role, node_root: {
                    "scenario_name": "worker_success"
                },
            )
            second_result = success_engine.drive_until_stable(
                node_path,
                mission_id="mission-001",
                node_id="leaf",
            )
            self.assertEqual(second_result.final_status, "finished")
            self.assertEqual(second_result.terminal_outcome, "completed")
            self.assertTrue((node_path / "system" / "recoveries" / "recovery-001").exists())


if __name__ == "__main__":
    unittest.main()

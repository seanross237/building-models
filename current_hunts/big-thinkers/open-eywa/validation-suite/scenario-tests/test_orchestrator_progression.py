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
from system.orchestrator.node_contract import node_layout
from system.orchestrator.node_record import read_node_record
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
                child_record = read_node_record(child_dir)
                self.assertEqual(
                    child_record["lifecycle"]["status"],
                    "finished",
                )
                self.assertEqual(
                    child_record["lifecycle"]["terminal_outcome"],
                    "completed",
                )

            progress_state = read_node_record(node_path)["progression"]
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

            self.assertFalse((node_path / "output" / "plan.md").exists())
            self.assertEqual(read_node_record(node_path)["control"]["next_role"], "planner")
            self.assertEqual(read_node_record(node_path)["progression"]["steps"], [])
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
                read_node_record(node_path)["lifecycle"]["status"],
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

    def test_structured_planner_format_creates_children_from_goal_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            node_path = Path(temp_dir) / "root"
            create_node(node_path, task_source_name="goal", task_text="Use strict planner format.")

            runtime = SimulatedRuntime(
                {
                    "planner_strict_format": load_scenario(
                        FIXTURES_DIR / "planner_strict_format.json"
                    ),
                    "worker_success": load_scenario(FIXTURES_DIR / "worker_success.json"),
                    "evaluator_continue": load_scenario(FIXTURES_DIR / "evaluator_continue.json"),
                    "synthesizer_success": load_scenario(FIXTURES_DIR / "synthesizer_success.json"),
                }
            )

            def resolver(mission_id: str, node_id: str, role: str, node_root: Path) -> dict[str, str]:
                del mission_id, node_id, node_root
                if role == "planner":
                    return {"scenario_name": "planner_strict_format"}
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
            first_child = node_path / "children" / "step-01-gather-background"
            second_child = node_path / "children" / "step-02-explain-inspection-priorities"
            self.assertTrue(first_child.exists())
            self.assertTrue(second_child.exists())
            self.assertEqual(
                (first_child / "input" / "parent-instructions.md").read_text(encoding="utf-8").strip(),
                "Research what Open-Eywa is and produce a concise summary suitable for an operator note.",
            )
            self.assertEqual(
                (second_child / "input" / "parent-instructions.md").read_text(encoding="utf-8").strip(),
                "Identify which mission files a human should inspect first and explain why they matter.",
            )
            second_context = (second_child / "input" / "context.md").read_text(encoding="utf-8")
            self.assertIn("## Parent Task", second_context)
            self.assertIn("Use strict planner format.", second_context)
            self.assertIn("## Prior Completed Step Results", second_context)
            self.assertIn("The work is complete.", second_context)

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

    def test_live_tree_like_plan_passes_prior_child_results_into_later_child_contexts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            node_path = Path(temp_dir) / "root"
            create_node(
                node_path,
                task_source_name="goal",
                task_text=(
                    "Using only these facts, create a short operator note: "
                    "(1) nodes are durable units of work, "
                    "(2) mission runs live in mission folders, "
                    "(3) testing improves reliability."
                ),
            )

            runtime = SimulatedRuntime(
                {
                    "planner_live_tree_shape": load_scenario(
                        FIXTURES_DIR / "planner_live_tree_shape.json"
                    ),
                    "worker_success": load_scenario(FIXTURES_DIR / "worker_success.json"),
                    "evaluator_continue": load_scenario(FIXTURES_DIR / "evaluator_continue.json"),
                    "synthesizer_success": load_scenario(FIXTURES_DIR / "synthesizer_success.json"),
                }
            )

            def resolver(mission_id: str, node_id: str, role: str, node_root: Path) -> dict[str, str]:
                del mission_id, node_id, node_root
                if role == "planner":
                    return {"scenario_name": "planner_live_tree_shape"}
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

            synth_child = node_path / "children" / "step-03-synthesize-final-note"
            review_child = node_path / "children" / "step-04-review-and-refine-note"
            self.assertTrue(synth_child.exists())
            self.assertTrue(review_child.exists())

            synth_context = (synth_child / "input" / "context.md").read_text(encoding="utf-8")
            self.assertIn("## Prior Completed Step Results", synth_context)
            self.assertIn("### Gather Facts", synth_context)
            self.assertIn("### Draft Operator Note", synth_context)
            self.assertIn("The work is complete.", synth_context)

            review_context = (review_child / "input" / "context.md").read_text(encoding="utf-8")
            self.assertIn("## Prior Completed Step Results", review_context)
            self.assertIn("### Synthesize Final Note", review_context)
            self.assertIn("## Parent Plan", review_context)
            self.assertIn("## Parent Task", review_context)

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

    def test_missing_required_artifact_is_retried_once_and_then_completes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            node_path = Path(temp_dir) / "leaf"
            create_node(
                node_path,
                task_source_name="goal",
                task_text="Retry automatically after missing output.",
                agent_mode="worker",
            )

            runtime = SimulatedRuntime(
                {
                    "missing_artifact": load_scenario(FIXTURES_DIR / "missing_artifact.json"),
                    "worker_success": load_scenario(FIXTURES_DIR / "worker_success.json"),
                }
            )

            def resolver(mission_id: str, node_id: str, role: str, node_root: Path) -> dict[str, str]:
                del mission_id, node_id, role
                retry_count = read_node_record(node_root)["lifecycle"].get("retry_count", 0)
                scenario_name = "worker_success" if retry_count >= 1 else "missing_artifact"
                return {"scenario_name": scenario_name}

            result = NodeProgressionEngine(
                runtime,
                runtime_metadata_resolver=resolver,
            ).drive_until_stable(
                node_path,
                mission_id="mission-001",
                node_id="leaf",
            )

            self.assertEqual(result.final_status, "finished")
            self.assertEqual(result.terminal_outcome, "completed")
            record = read_node_record(node_path)
            self.assertEqual(record["lifecycle"]["retry_count"], 1)
            self.assertTrue((node_path / "system" / "runs" / "run-001").exists())
            self.assertTrue((node_path / "system" / "runs" / "run-002").exists())
            events = [
                json.loads(line)
                for line in (node_path / "system" / "events.jsonl").read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            retry_events = [
                event
                for event in events
                if event["event_type"] == "node_recovery_prepared"
            ]
            self.assertEqual(len(retry_events), 1)
            self.assertEqual(retry_events[0]["payload"]["retry_count"], 1)
            self.assertEqual(retry_events[0]["payload"]["recovery_mode"], "retry")

    def test_missing_required_artifact_stops_after_three_retries(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            node_path = Path(temp_dir) / "leaf"
            create_node(
                node_path,
                task_source_name="goal",
                task_text="Stop after bounded automatic retries.",
                agent_mode="worker",
            )

            runtime = SimulatedRuntime(
                {"missing_artifact": load_scenario(FIXTURES_DIR / "missing_artifact.json")}
            )

            result = NodeProgressionEngine(
                runtime,
                runtime_metadata_resolver=lambda mission_id, node_id, role, node_root: {
                    "scenario_name": "missing_artifact"
                },
            ).drive_until_stable(
                node_path,
                mission_id="mission-001",
                node_id="leaf",
            )

            self.assertEqual(result.final_status, "failed")
            self.assertEqual(result.failure_reason, "missing_required_artifact")
            record = read_node_record(node_path)
            self.assertEqual(record["lifecycle"]["retry_count"], 3)
            self.assertTrue((node_path / "system" / "recoveries" / "recovery-003").exists())
            self.assertTrue((node_path / "system" / "runs" / "run-004").exists())


if __name__ == "__main__":
    unittest.main()

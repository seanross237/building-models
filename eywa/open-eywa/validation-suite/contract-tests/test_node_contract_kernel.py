from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from system.orchestrator.node_contract import create_node, write_text
from system.orchestrator.node_controls import (
    cancel_node,
    record_computation_result,
    resume_waiting_node_if_ready,
)
from system.orchestrator.node_lifecycle import NodeTransitionError, transition_node
from system.orchestrator.node_recovery import (
    NodeRecoveryError,
    prepare_node_for_fresh_attempt,
    prepare_node_for_retry,
)
from system.orchestrator.node_record import read_node_record, write_node_record
from system.orchestrator.node_validator import validate_node


class NodeContractKernelTests(unittest.TestCase):
    def test_create_node_builds_a_valid_pending_root_node(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            node_path = Path(temp_dir) / "root"
            create_node(node_path, task_source_name="goal", task_text="Do the work.")

            report = validate_node(node_path)

            self.assertTrue(report.is_valid, report.issues)
            record = read_node_record(node_path)
            self.assertEqual(record["lifecycle"]["status"], "pending")
            self.assertEqual(record["lifecycle"]["retry_count"], 0)
            self.assertEqual(record["task"]["source_name"], "goal")
            self.assertFalse((node_path / "for-orchestrator").exists())

    def test_create_child_node_records_identity_and_task_in_node_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            child_path = Path(temp_dir) / "children" / "step-01"
            create_node(
                child_path,
                task_source_name="parent-instructions",
                task_text="Do the child work.",
                node_id="root.step-01",
                parent_node_id="root",
                next_role="worker",
            )

            record = read_node_record(child_path)

            self.assertEqual(record["identity"]["node_id"], "root.step-01")
            self.assertEqual(record["identity"]["parent_node_id"], "root")
            self.assertEqual(record["task"]["source_name"], "parent-instructions")
            self.assertEqual(record["task"]["source_path"], "input/parent-instructions.md")

    def test_validator_rejects_multiple_task_sources(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            node_path = Path(temp_dir) / "root"
            layout = create_node(node_path, task_source_name="goal", task_text="Do the work.")
            write_text(layout.parent_instructions_file, "Also do this.\n")

            report = validate_node(node_path)

            self.assertFalse(report.is_valid)
            self.assertIn("task_source_count", {issue.code for issue in report.issues})

    def test_finished_nodes_require_terminal_outcome(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            node_path = Path(temp_dir) / "root"
            create_node(node_path, task_source_name="goal", task_text="Do the work.")

            record = read_node_record(node_path)
            record["lifecycle"]["status"] = "finished"
            record["lifecycle"]["terminal_outcome"] = None
            write_node_record(node_path, record)

            report = validate_node(node_path)

            self.assertFalse(report.is_valid)
            self.assertIn("terminal_outcome_missing", {issue.code for issue in report.issues})

    def test_validator_rejects_missing_node_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            node_path = Path(temp_dir) / "root"
            create_node(node_path, task_source_name="goal", task_text="Do the work.")
            (node_path / "system" / "node.json").unlink()

            report = validate_node(node_path)

            self.assertFalse(report.is_valid)
            self.assertIn("node_record_missing", {issue.code for issue in report.issues})

    def test_completed_transition_requires_final_output(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            node_path = Path(temp_dir) / "root"
            create_node(node_path, task_source_name="goal", task_text="Do the work.")
            transition_node(node_path, next_status="active", expected_current_status="pending")

            with self.assertRaises(NodeTransitionError):
                transition_node(
                    node_path,
                    next_status="finished",
                    expected_current_status="active",
                    terminal_outcome="completed",
                )

    def test_successful_completed_transition_validates_cleanly(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            node_path = Path(temp_dir) / "root"
            layout = create_node(node_path, task_source_name="goal", task_text="Do the work.")
            transition_node(node_path, next_status="active", expected_current_status="pending")
            write_text(layout.final_output_file, "All done.\n")
            transition_node(
                node_path,
                next_status="finished",
                expected_current_status="active",
                terminal_outcome="completed",
            )

            report = validate_node(node_path)

            self.assertTrue(report.is_valid, report.issues)
            self.assertEqual(read_node_record(node_path)["lifecycle"]["terminal_outcome"], "completed")

    def test_waiting_transition_creates_required_note(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            node_path = Path(temp_dir) / "root"
            create_node(node_path, task_source_name="goal", task_text="Do the work.")
            transition_node(node_path, next_status="active", expected_current_status="pending")
            transition_node(
                node_path,
                next_status="waiting_on_computation",
                expected_current_status="active",
                waiting_note="Long computation running.",
            )

            record = read_node_record(node_path)
            self.assertEqual(
                record["lifecycle"]["waiting_on_computation_note"],
                "Long computation running.",
            )
            report = validate_node(node_path)
            self.assertTrue(report.is_valid, report.issues)

    def test_cancelled_transition_requires_cancellation_reason(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            node_path = Path(temp_dir) / "root"
            create_node(node_path, task_source_name="goal", task_text="Cancel the work.")
            transition_node(node_path, next_status="active", expected_current_status="pending")

            with self.assertRaises(NodeTransitionError):
                transition_node(
                    node_path,
                    next_status="finished",
                    expected_current_status="active",
                    terminal_outcome="cancelled",
                )

    def test_cancel_node_writes_cancelled_state_validly(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            node_path = Path(temp_dir) / "root"
            create_node(node_path, task_source_name="goal", task_text="Cancel the work.")

            cancel_node(node_path, cancellation_reason="Parent replanned this node away.")

            report = validate_node(node_path)
            self.assertTrue(report.is_valid, report.issues)
            record = read_node_record(node_path)
            self.assertEqual(record["lifecycle"]["terminal_outcome"], "cancelled")
            self.assertEqual(
                record["lifecycle"]["cancellation_reason"],
                "Parent replanned this node away.",
            )

    def test_resume_waiting_node_requires_computation_result_note(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            node_path = Path(temp_dir) / "root"
            create_node(node_path, task_source_name="goal", task_text="Resume the work.")
            transition_node(node_path, next_status="active", expected_current_status="pending")
            transition_node(
                node_path,
                next_status="waiting_on_computation",
                expected_current_status="active",
                waiting_note="Long computation running.",
            )

            no_result = resume_waiting_node_if_ready(node_path)
            self.assertFalse(no_result.resumed)

            record_computation_result(node_path, result_text="Computation finished.")
            did_resume = resume_waiting_node_if_ready(node_path)

            self.assertTrue(did_resume.resumed)
            self.assertEqual(did_resume.current_status, "active")
            self.assertIsNone(read_node_record(node_path)["lifecycle"]["computation_result_note"])
            report = validate_node(node_path)
            self.assertTrue(report.is_valid, report.issues)

    def test_prepare_node_for_fresh_attempt_archives_failed_state(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            node_path = Path(temp_dir) / "root"
            layout = create_node(
                node_path,
                task_source_name="goal",
                task_text="Retry the work.",
                initial_status="failed",
                next_role="worker",
                failure_reason="missing_required_artifact",
            )
            write_text(layout.final_output_file, "old output\n")

            result = prepare_node_for_fresh_attempt(
                node_path,
                recovery_reason="retry after missing artifact",
                next_role="worker",
                mission_id="mission-001",
                node_id="root",
            )

            self.assertEqual(result.current_status, "pending")
            self.assertEqual(result.next_role, "worker")
            self.assertTrue((layout.recoveries_dir / "recovery-001" / "output" / "final-output.md").exists())
            self.assertTrue((layout.recoveries_dir / "recovery-001" / "node.json").exists())
            record = read_node_record(node_path)
            self.assertEqual(record["lifecycle"]["status"], "pending")
            self.assertEqual(record["lifecycle"]["retry_count"], 1)
            self.assertEqual(record["control"]["next_role"], "worker")
            self.assertEqual(result.retry_count, 1)
            report = validate_node(node_path)
            self.assertTrue(report.is_valid, report.issues)

    def test_prepare_node_for_retry_preserves_progression_and_increments_retry_count(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            node_path = Path(temp_dir) / "root"
            layout = create_node(
                node_path,
                task_source_name="goal",
                task_text="Retry without wiping the plan state.",
                initial_status="failed",
                next_role="synthesizer",
                failure_reason="missing_required_artifact",
            )
            write_text(layout.plan_file, "# Existing plan\n")
            write_text(layout.state_file, "partial state\n")
            record = read_node_record(node_path)
            record["progression"]["current_step_index"] = 2
            record["progression"]["steps"] = [{"index": 0, "title": "Step", "goal": "Goal"}]
            write_node_record(node_path, record)

            result = prepare_node_for_retry(
                node_path,
                recovery_reason="automatic_retry_after_missing_required_artifact",
                next_role="synthesizer",
                mission_id="mission-001",
                node_id="root",
            )

            record = read_node_record(node_path)
            self.assertEqual(result.retry_count, 1)
            self.assertEqual(record["lifecycle"]["status"], "pending")
            self.assertEqual(record["lifecycle"]["retry_count"], 1)
            self.assertEqual(record["progression"]["current_step_index"], 2)
            self.assertEqual(record["control"]["next_role"], "synthesizer")
            self.assertTrue(layout.plan_file.exists())
            self.assertTrue((layout.recoveries_dir / "recovery-001" / "output" / "plan.md").exists())
            report = validate_node(node_path)
            self.assertTrue(report.is_valid, report.issues)

    def test_prepare_node_for_fresh_attempt_rejects_completed_nodes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            node_path = Path(temp_dir) / "root"
            layout = create_node(node_path, task_source_name="goal", task_text="Do the work.")
            transition_node(node_path, next_status="active", expected_current_status="pending")
            write_text(layout.final_output_file, "done\n")
            transition_node(
                node_path,
                next_status="finished",
                expected_current_status="active",
                terminal_outcome="completed",
            )

            with self.assertRaises(NodeRecoveryError):
                prepare_node_for_fresh_attempt(
                    node_path,
                    recovery_reason="should fail for completed node",
                )


if __name__ == "__main__":
    unittest.main()

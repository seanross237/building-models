from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from system.orchestrator.node_contract import create_node, write_text
from system.orchestrator.node_controls import cancel_node, record_computation_result, resume_waiting_node_if_ready
from system.orchestrator.node_lifecycle import NodeTransitionError, transition_node
from system.orchestrator.node_recovery import NodeRecoveryError, prepare_node_for_fresh_attempt
from system.orchestrator.node_validator import validate_node


class NodeContractKernelTests(unittest.TestCase):
    def test_create_node_builds_a_valid_pending_root_node(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            node_path = Path(temp_dir) / "root"
            create_node(node_path, task_source_name="goal", task_text="Do the work.")

            report = validate_node(node_path)

            self.assertTrue(report.is_valid, report.issues)

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
            layout = create_node(node_path, task_source_name="goal", task_text="Do the work.")
            write_text(layout.status_file, "finished\n")

            report = validate_node(node_path)

            self.assertFalse(report.is_valid)
            self.assertIn("terminal_outcome_missing", {issue.code for issue in report.issues})

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

    def test_waiting_transition_creates_required_marker(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            node_path = Path(temp_dir) / "root"
            layout = create_node(node_path, task_source_name="goal", task_text="Do the work.")
            transition_node(node_path, next_status="active", expected_current_status="pending")
            transition_node(
                node_path,
                next_status="waiting_on_computation",
                expected_current_status="active",
                waiting_note="Long computation running.",
            )

            self.assertTrue(layout.waiting_marker_file.exists())
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
            layout = create_node(node_path, task_source_name="goal", task_text="Cancel the work.")

            cancel_node(node_path, cancellation_reason="Parent replanned this node away.")

            report = validate_node(node_path)
            self.assertTrue(report.is_valid, report.issues)
            self.assertEqual(layout.terminal_outcome_file.read_text(encoding="utf-8").strip(), "cancelled")
            self.assertEqual(layout.cancellation_reason_file.read_text(encoding="utf-8").strip(), "Parent replanned this node away.")

    def test_resume_waiting_node_requires_computation_result_marker(self) -> None:
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
            self.assertFalse((node_path / "for-orchestrator" / "computation_result").exists())
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
                agent_mode="worker",
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
            self.assertTrue((layout.recoveries_dir / "recovery-001" / "for-orchestrator" / "failure-reason").exists())
            self.assertEqual(layout.status_file.read_text(encoding="utf-8").strip(), "pending")
            self.assertEqual(layout.agent_mode_file.read_text(encoding="utf-8").strip(), "worker")
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

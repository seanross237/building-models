from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from system.orchestrator import create_node, prepare_node_context_packet
from system.orchestrator.node_contract import node_layout, write_text


class NodePreparationTests(unittest.TestCase):
    def test_prepared_context_packet_includes_role_relevant_sections(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            node_path = Path(temp_dir) / "root"
            layout = create_node(node_path, task_source_name="goal", task_text="Evaluate the child.")
            layout.run_dir("run-001").mkdir(parents=True, exist_ok=True)

            write_text(layout.context_file, "shared context\n")
            write_text(layout.plan_file, "# Plan\n\n1. Do the work.\n")
            write_text(layout.state_file, "parent notes\n")
            write_text(
                layout.latest_child_node_report_file,
                json.dumps(
                    {
                        "child_node_id": "root.step-01-do-the-work",
                        "child_status": "failed",
                    },
                    indent=2,
                )
                + "\n",
            )
            child_layout = create_node(
                layout.children_dir / "step-01-do-the-work",
                task_source_name="parent-instructions",
                task_text="Do the work.",
                initial_status="finished",
                terminal_outcome="completed",
                cancellation_reason=None,
            )
            write_text(child_layout.final_output_file, "child final output\n")

            result = prepare_node_context_packet(layout, run_id="run-001", role="mid-plan-evaluator")
            packet = json.loads(Path(result.packet_path).read_text(encoding="utf-8"))

            self.assertIn("latest_child_report", packet["available_sections"])
            self.assertIn("context", packet["available_sections"])
            self.assertIn("progression", packet)
            self.assertEqual(packet["role"], "mid-plan-evaluator")
            self.assertIn("latest_child_report", packet["focus_sections"])
            self.assertEqual(len(packet["children"]), 1)
            self.assertEqual(packet["children"][0]["status"], "finished")

    def test_worker_packet_surfaces_context_when_present(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            node_path = Path(temp_dir) / "child"
            layout = create_node(
                node_path,
                task_source_name="parent-instructions",
                task_text="Write the next step.",
            )
            layout.run_dir("run-001").mkdir(parents=True, exist_ok=True)
            write_text(layout.context_file, "Parent facts and prior outputs.\n")

            result = prepare_node_context_packet(layout, run_id="run-001", role="worker")
            packet = json.loads(Path(result.packet_path).read_text(encoding="utf-8"))

            self.assertIn("context", packet["available_sections"])
            self.assertIn("context", packet["focus_sections"])
            self.assertEqual(
                packet["available_sections"]["context"]["text"],
                "Parent facts and prior outputs.\n",
            )


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[3]
RUNNER = REPO_ROOT / "eywa-system" / "runtime" / "run_v1.py"
RUNTIME_DIR = REPO_ROOT / "eywa-system" / "runtime"

import sys

if str(RUNTIME_DIR) not in sys.path:
    sys.path.insert(0, str(RUNTIME_DIR))

from eywa_runtime.engine import EywaEngine  # noqa: E402
from eywa_runtime.executor import ExecutionStep  # noqa: E402


class RuntimeTests(unittest.TestCase):
    def test_single_node_run_writes_expected_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            cmd = [
                "python3",
                str(RUNNER),
                "--task",
                "Write a short summary about feature X.",
                "--run-id",
                "run_test_single",
                "--run-history-root",
                tmpdir,
            ]
            completed = subprocess.run(cmd, check=True, capture_output=True, text=True)
            self.assertIn("run_id=run_test_single", completed.stdout)

            run_dir = Path(tmpdir) / "run_test_single"
            self.assertTrue((run_dir / "run_packet.json").exists())
            self.assertTrue((run_dir / "run_summary.json").exists())
            self.assertTrue((run_dir / "nodes" / "node_root" / "node_packet.json").exists())
            self.assertTrue((run_dir / "nodes" / "node_root" / "node_record.json").exists())
            self.assertTrue((run_dir / "derived" / "timeline.md").exists())

            summary = json.loads((run_dir / "run_summary.json").read_text(encoding="utf-8"))
            self.assertEqual(summary["node_count"], 1)

            node_record = json.loads(
                (run_dir / "nodes" / "node_root" / "node_record.json").read_text(encoding="utf-8")
            )
            self.assertEqual(node_record["orchestration"]["initial_decision"], "execute_locally")
            self.assertEqual(node_record["orchestration"]["final_decision"], "execute_locally")
            self.assertIsInstance(node_record["results"][0]["content"], str)
            self.assertFalse(node_record["results"][0]["content"].lstrip().startswith("{"))

            replay = json.loads(
                (run_dir / "replay" / "node_root" / "raw-model.json").read_text(encoding="utf-8")
            )
            self.assertEqual(
                replay["steps"][0]["authored_response"]["orchestration_decision"],
                "execute_locally",
            )

    def test_decomposition_creates_helpers(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            cmd = [
                "python3",
                str(RUNNER),
                "--task",
                "Design the backend and build the frontend and validate the feature.",
                "--run-id",
                "run_test_helpers",
                "--run-history-root",
                tmpdir,
            ]
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            run_dir = Path(tmpdir) / "run_test_helpers"
            summary = json.loads((run_dir / "run_summary.json").read_text(encoding="utf-8"))
            self.assertGreater(summary["node_count"], 1)
            self.assertTrue((run_dir / "nodes" / "node_root_helper_01" / "node_record.json").exists())
            self.assertTrue((run_dir / "nodes" / "node_root_helper_02" / "node_record.json").exists())

            root_record = json.loads(
                (run_dir / "nodes" / "node_root" / "node_record.json").read_text(encoding="utf-8")
            )
            self.assertEqual(root_record["orchestration"]["initial_decision"], "delegate")
            self.assertEqual(root_record["orchestration"]["final_decision"], "execute_locally")

            helper_record = json.loads(
                (run_dir / "nodes" / "node_root_helper_01" / "node_record.json").read_text(encoding="utf-8")
            )
            self.assertEqual(helper_record["orchestration"]["initial_decision"], "execute_locally")

            replay = json.loads(
                (run_dir / "replay" / "node_root" / "raw-model.json").read_text(encoding="utf-8")
            )
            self.assertEqual(replay["steps"][0]["output"]["action_type"], "recruit_help")
            self.assertEqual(
                replay["steps"][-1]["authored_response"]["orchestration_decision"],
                "execute_locally",
            )

    def test_parent_can_delegate_again_after_child_review(self) -> None:
        class ScriptedExecutor:
            provider_name = "scripted-test"

            def author_node_response(
                self,
                *,
                node_packet,
                depth,
                turn_index,
                allowed_decisions,
                child_summaries=None,
                synthesis_brief=None,
            ) -> ExecutionStep:
                node_id = node_packet["node_id"]
                authored_response = scripted_response(node_id=node_id, turn_index=turn_index)
                return ExecutionStep(
                    authored_response=authored_response,
                    note=f"scripted response for {node_id} turn {turn_index}",
                    prompt_snapshot=f"scripted prompt for {node_id} turn {turn_index}",
                    provider_payload={
                        "provider": self.provider_name,
                        "parsed_response": authored_response,
                    },
                    usage=self._zero_usage(),
                )

            def _zero_usage(self):
                return {
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "reasoning_tokens": 0,
                    "cached_prompt_tokens": 0,
                    "total_tokens": 0,
                    "cost_usd": 0.0,
                    "provider_details": {"responses": [{"provider": self.provider_name}]},
                }

        def scripted_response(*, node_id: str, turn_index: int) -> dict:
            key = (node_id, turn_index)
            responses = {
                ("node_root", 1): {
                    "schema_name": "eywa_node_response",
                    "schema_version": "v1",
                    "orchestration_decision": "delegate",
                    "decision_notes": "First round splits the task in two.",
                    "helpers": [
                        {
                            "label": "phase_one",
                            "instructions": "Handle phase one.",
                            "variable_overrides": {},
                        },
                        {
                            "label": "phase_two",
                            "instructions": "Handle phase two.",
                            "variable_overrides": {},
                        },
                    ],
                    "synthesis_brief": "Review the first helper round before deciding what remains.",
                },
                ("node_root", 2): {
                    "schema_name": "eywa_node_response",
                    "schema_version": "v1",
                    "orchestration_decision": "delegate",
                    "decision_notes": "One more helper is needed after the first review.",
                    "helpers": [
                        {
                            "label": "phase_three",
                            "instructions": "Handle phase three.",
                            "variable_overrides": {},
                        }
                    ],
                    "synthesis_brief": "Combine every helper result into the final answer.",
                },
                ("node_root", 3): {
                    "schema_name": "eywa_node_response",
                    "schema_version": "v1",
                    "orchestration_decision": "execute_locally",
                    "decision_notes": "The parent now has enough information to finish locally.",
                    "response": "FINAL_ANSWER: scripted-finish\nJUSTIFICATION: all helper outputs are now available.",
                    "result_type": "summary",
                },
                ("node_root_helper_01", 1): {
                    "schema_name": "eywa_node_response",
                    "schema_version": "v1",
                    "orchestration_decision": "execute_locally",
                    "decision_notes": "Handled locally.",
                    "response": "phase one complete",
                    "result_type": "summary",
                },
                ("node_root_helper_02", 1): {
                    "schema_name": "eywa_node_response",
                    "schema_version": "v1",
                    "orchestration_decision": "execute_locally",
                    "decision_notes": "Handled locally.",
                    "response": "phase two complete",
                    "result_type": "summary",
                },
                ("node_root_helper_03", 1): {
                    "schema_name": "eywa_node_response",
                    "schema_version": "v1",
                    "orchestration_decision": "execute_locally",
                    "decision_notes": "Handled locally.",
                    "response": "phase three complete",
                    "result_type": "summary",
                },
            }
            return responses[key]

        with tempfile.TemporaryDirectory() as tmpdir:
            engine = EywaEngine(Path(tmpdir))
            with patch("eywa_runtime.engine.build_executor", side_effect=lambda resolved_variables: ScriptedExecutor()):
                result = engine.run(
                    task_text="Do the three-phase task.",
                    run_id="run_test_redelegate",
                )

            run_dir = result.run_dir
            root_record = json.loads(
                (run_dir / "nodes" / "node_root" / "node_record.json").read_text(encoding="utf-8")
            )
            self.assertEqual(root_record["orchestration"]["initial_decision"], "delegate")
            self.assertEqual(root_record["orchestration"]["final_decision"], "execute_locally")
            self.assertEqual(root_record["orchestration"]["turn_count"], 3)
            self.assertEqual(root_record["orchestration"]["helper_count"], 3)
            self.assertTrue((run_dir / "nodes" / "node_root_helper_03" / "node_record.json").exists())

            replay = json.loads(
                (run_dir / "replay" / "node_root" / "raw-model.json").read_text(encoding="utf-8")
            )
            self.assertEqual(
                [step["authored_response"]["orchestration_decision"] for step in replay["steps"]],
                ["delegate", "delegate", "execute_locally"],
            )


if __name__ == "__main__":
    unittest.main()

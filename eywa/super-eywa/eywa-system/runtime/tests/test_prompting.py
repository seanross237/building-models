from __future__ import annotations

import unittest
from pathlib import Path
import sys


THIS_DIR = Path(__file__).resolve().parent
RUNTIME_DIR = THIS_DIR.parent
if str(RUNTIME_DIR) not in sys.path:
    sys.path.insert(0, str(RUNTIME_DIR))

from eywa_runtime.prompting import build_turn_prompt  # noqa: E402


class PromptingTests(unittest.TestCase):
    def test_custom_prompt_text_and_blank_header_are_used_verbatim(self) -> None:
        node_packet = {
            "run_id": "run_prompting_test",
            "node_id": "node_root",
            "input": {
                "instructions": "Original question text.",
                "provided_context_refs": [],
                "attachment_refs": [],
            },
            "variable_resolution": {
                "resolved_variables": {
                    "prompt_family": "transmute",
                    "selected_prompt_text": "You are going to transmute this question.",
                    "base_header_prompt": "",
                    "additional_instruction_prompt_profiles": [],
                    "budget_policy": {
                        "max_depth": 3,
                        "max_helpers_per_node": 3,
                        "max_turns_per_node": 4,
                    },
                }
            },
        }

        prompt_bundle = build_turn_prompt(
            node_packet,
            allowed_decisions=["transmute"],
            turn_index=1,
            depth=0,
        )

        self.assertEqual(prompt_bundle["system_prompt"], "")
        self.assertTrue(prompt_bundle["user_prompt"].startswith("You are going to transmute this question."))
        self.assertTrue(prompt_bundle["user_prompt"].endswith("Question:\nOriginal question text."))

    def test_child_review_can_switch_to_review_prompt(self) -> None:
        node_packet = {
            "run_id": "run_prompting_review_test",
            "node_id": "node_root",
            "input": {
                "instructions": "Original question text.",
                "provided_context_refs": [],
                "attachment_refs": [],
            },
            "variable_resolution": {
                "resolved_variables": {
                    "prompt_family": "transmute",
                    "selected_prompt_text": "First-turn transmute prompt.",
                    "review_prompt_family": "execute",
                    "review_selected_prompt_text": "Now use the child result and solve it.",
                    "base_header_prompt": "",
                    "additional_instruction_prompt_profiles": [],
                    "budget_policy": {
                        "max_depth": 3,
                        "max_helpers_per_node": 3,
                        "max_turns_per_node": 4,
                    },
                }
            },
        }

        prompt_bundle = build_turn_prompt(
            node_packet,
            allowed_decisions=["execute_locally"],
            turn_index=2,
            depth=0,
            child_results=[
                {
                    "node_id": "node_root_helper_01",
                    "summary": "Child answer text.",
                }
            ],
        )

        self.assertEqual(prompt_bundle["prompt_family"], "execute")
        self.assertTrue(prompt_bundle["user_prompt"].startswith("Now use the child result and solve it."))
        self.assertIn("Child results already returned to you", prompt_bundle["user_prompt"])

    def test_review_family_uses_one_child_review_prompt_then_executes(self) -> None:
        node_packet = {
            "run_id": "run_prompting_review_family_test",
            "node_id": "node_root",
            "input": {
                "instructions": "Original question text.",
                "provided_context_refs": [],
                "attachment_refs": [],
            },
            "variable_resolution": {
                "resolved_variables": {
                    "prompt_family": "review",
                    "selected_prompt_text": "",
                    "base_header_prompt": "",
                    "additional_instruction_prompt_profiles": [],
                    "budget_policy": {
                        "max_depth": 3,
                        "max_helpers_per_node": 3,
                        "max_turns_per_node": 4,
                    },
                }
            },
        }

        first_turn = build_turn_prompt(
            node_packet,
            allowed_decisions=["review"],
            turn_index=1,
            depth=0,
        )
        self.assertEqual(first_turn["prompt_family"], "review")
        self.assertIn('"orchestration_decision": "review"', first_turn["user_prompt"])

        second_turn = build_turn_prompt(
            node_packet,
            allowed_decisions=["execute_locally"],
            turn_index=2,
            depth=0,
            child_results=[{"node_id": "node_root_helper_01", "summary": "critique"}],
        )
        self.assertEqual(second_turn["prompt_family"], "review")
        self.assertIn('"orchestration_decision": "execute_locally"', second_turn["user_prompt"])

if __name__ == "__main__":
    unittest.main()

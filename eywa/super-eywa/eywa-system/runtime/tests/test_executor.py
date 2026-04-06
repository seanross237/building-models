from __future__ import annotations

import unittest
from pathlib import Path
import sys


THIS_DIR = Path(__file__).resolve().parent
RUNTIME_DIR = THIS_DIR.parent
if str(RUNTIME_DIR) not in sys.path:
    sys.path.insert(0, str(RUNTIME_DIR))

from eywa_runtime.executor import OpenRouterClientError, OpenRouterLiveExecutor  # noqa: E402


class ExecutorTests(unittest.TestCase):
    def test_live_executor_turn_becomes_problem_report_when_repair_fails(self) -> None:
        executor = OpenRouterLiveExecutor.__new__(OpenRouterLiveExecutor)
        executor.model = "openai/gpt-4.1-mini"
        executor.provider_name = "openrouter"

        def fake_generate_text(*, system_prompt: str, user_prompt: str, max_tokens: int, temperature: float):
            return {
                "content": "This is not valid JSON.",
                "provider_payload": {
                    "provider": "openrouter",
                    "request": {
                        "system_prompt": system_prompt,
                        "user_prompt": user_prompt,
                    },
                    "response": {"id": "fake-response"},
                },
                "usage": {
                    "prompt_tokens": 10,
                    "completion_tokens": 5,
                    "reasoning_tokens": 0,
                    "cached_prompt_tokens": 0,
                    "total_tokens": 15,
                    "cost_usd": 0.0,
                    "provider_details": {"responses": [{"provider": "openrouter"}]},
                },
            }

        def fake_repair_response(*, raw_text: str, allowed_decisions, max_tokens: int, temperature: float):
            raise OpenRouterClientError("OpenRouter request timed out.")

        executor._generate_text = fake_generate_text
        executor._repair_response = fake_repair_response

        node_packet = {
            "run_id": "run_test_executor",
            "node_id": "node_root",
            "input": {
                "instructions": "Delegate if needed.",
                "provided_context_refs": [],
                "attachment_refs": [],
            },
            "variable_resolution": {
                "resolved_variables": {
                    "injected_prompt_profile": "agent_orchestration_basic_instruction_prompt",
                    "additional_instruction_prompt_profiles": [],
                    "budget_policy": {
                        "max_helpers_per_node": 3,
                    },
                    "routing_policy": "return_to_creator",
                    "recovery_policy": "report_problem",
                    "workflow_structure": "sequential_parent_review",
                    "verification_policy": "light",
                }
            },
        }

        step = executor.author_node_response(
            node_packet=node_packet,
            depth=0,
            turn_index=1,
            allowed_decisions=["execute_locally", "delegate", "report_problem"],
        )

        self.assertEqual(step.authored_response["orchestration_decision"], "report_problem")
        self.assertIn("json repair failed", step.authored_response["response"])
        self.assertEqual(step.provider_payload["attempts"][-1]["phase"], "json_repair")
        self.assertEqual(step.provider_payload["attempts"][-1]["parse_error"], "OpenRouter request timed out.")

    def test_live_executor_resolves_generation_settings_from_variables(self) -> None:
        executor = OpenRouterLiveExecutor.__new__(OpenRouterLiveExecutor)

        self.assertEqual(
            executor._resolved_max_tokens({"provider_max_tokens": "1600"}),
            1600,
        )
        self.assertEqual(
            executor._resolved_max_tokens({"provider_max_tokens": "999999"}),
            4000,
        )
        self.assertAlmostEqual(
            executor._resolved_temperature({"provider_temperature": "0.35"}),
            0.35,
        )
        self.assertAlmostEqual(
            executor._resolved_temperature({"provider_temperature": "-1"}),
            0.0,
        )


if __name__ == "__main__":
    unittest.main()

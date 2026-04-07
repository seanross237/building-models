from __future__ import annotations

import unittest
from pathlib import Path
import sys
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[3]
GRADING_DIR = REPO_ROOT / "data-system" / "grading"
if str(GRADING_DIR) not in sys.path:
    sys.path.insert(0, str(GRADING_DIR))


class MX1TutorPromptTests(unittest.TestCase):
    def test_build_tutor_prompt_includes_run_context_and_prior_outputs(self) -> None:
        from mx1_tutor_v1 import build_tutor_prompt

        manifest = {
            "family": "transmute",
            "loop_id": "loop-1",
            "exploration_iterations": 3,
            "starter_prompt_text": "starter prompt",
            "history_summary": {
                "best_iteration_index": 1,
                "best_score": 0.0,
                "plateau_streak": 1,
                "needs_new_direction": False,
            },
        }
        grading_record = {
            "task_text": "Question text",
            "validation_status": "valid",
            "node_count": 2,
            "root_orchestration": {
                "initial_decision": "transmute",
                "final_decision": "transmute",
            },
            "root_result_excerpt": "root excerpt",
            "final_result_excerpt": "final excerpt",
        }
        current_attempt = {
            "iteration_index": 2,
            "prompt_text": "current prompt",
            "score": 0.0,
            "correct": False,
            "total_tokens": 100,
            "total_wall_time_ms": 200,
            "total_cost_usd": 0.1,
        }
        prior_attempts = [
            {
                "iteration_index": 1,
                "kind": "transmute",
                "run_id": "run-1",
                "score": 0.0,
                "correct": False,
                "total_tokens": 110,
                "total_wall_time_ms": 210,
                "total_cost_usd": 0.2,
                "prompt_text": "prior prompt",
                "prompt_file": None,
                "root_orchestration": {"final_decision": "transmute"},
                "root_result_excerpt": "prior root excerpt",
                "final_result_excerpt": "prior final excerpt",
            }
        ]

        prompt = build_tutor_prompt(
            manifest=manifest,
            grading_record=grading_record,
            current_attempt=current_attempt,
            prior_attempts=prior_attempts,
        )

        self.assertIn("Current run context", prompt)
        self.assertIn("root excerpt", prompt)
        self.assertIn("final excerpt", prompt)
        self.assertIn("prior root excerpt", prompt)
        self.assertIn("prior final excerpt", prompt)
        self.assertIn("reusable family-level prompt", prompt)
        self.assertIn("Do not bake in problem details", prompt)

    def test_question_specific_detector_flags_problem_framing_and_fixed_split_counts(self) -> None:
        from mx1_tutor_v1 import looks_question_specific

        self.assertTrue(looks_question_specific("Problem: check whether 2023 divides 2^a + 2^b"))
        self.assertTrue(looks_question_specific("Split this into 2 helper tasks."))
        self.assertFalse(looks_question_specific("Use 2023 as given in the original question and preserve all constants."))
        self.assertFalse(
            looks_question_specific(
                "Decompose the problem into a small number of useful subproblems and keep each helper focused."
            )
        )

    def test_parse_json_or_repair_handles_raw_backslashes(self) -> None:
        from mx1_tutor_v1 import _parse_json_or_repair

        content = r'''
        {
          "correctness_assessment": "incorrect",
          "assessment": {
            "score_direction": "same",
            "token_direction": "same",
            "time_direction": "same",
            "summary": "Needs a new direction."
          },
          "what_helped": ["History was preserved."],
          "what_hurt": ["Prompt used \equiv and \pmod in plain text."],
          "recommendation": {
            "action": "adjust",
            "reason": "Avoid malformed escapes.",
            "new_prompt_text": "Keep constants like 2023, and say \equiv only in plain text."
          },
          "history_observations": ["plateaued"],
          "confidence": "medium"
        }
        '''

        parsed = _parse_json_or_repair(content)

        self.assertEqual(parsed["recommendation"]["action"], "adjust")
        self.assertIn(r"\equiv", parsed["recommendation"]["new_prompt_text"])

    def test_openrouter_tutor_falls_back_to_deterministic_if_repair_still_invalid(self) -> None:
        import mx1_tutor_v1

        manifest = {
            "family": "transmute",
            "question_id": "q1",
            "question_title": "Q1",
            "question_file": "q1.md",
            "loop_id": "loop-1",
            "starter_prompt_text": "starter",
            "exploration_iterations": 3,
            "history_summary": {},
        }
        grading_record = {
            "runtime_provider": "openrouter",
            "model": "google/gemma-4-26b-a4b-it",
            "grading": {"correct": False, "score": 0.0},
        }
        current_attempt = {
            "iteration_index": 2,
            "score": 0.0,
            "correct": False,
            "total_tokens": 100,
            "total_wall_time_ms": 200,
            "total_cost_usd": 0.1,
            "prompt_text": "current prompt",
        }
        prior_attempts = []

        class FakeClient:
            def __init__(self, config):
                self.calls = 0

            def create_chat_completion(self, **kwargs):
                self.calls += 1
                return {
                    "choices": [
                        {
                            "message": {
                                "content": "not json at all"
                            }
                        }
                    ]
                }

        with mock.patch.object(mx1_tutor_v1, "load_openrouter_api_key", return_value="test-key"), mock.patch.object(
            mx1_tutor_v1, "OpenRouterChatClient", FakeClient
        ):
            tutor, provider_payload = mx1_tutor_v1._build_openrouter_tutor(
                manifest=manifest,
                grading_record=grading_record,
                current_attempt=current_attempt,
                prior_attempts=prior_attempts,
                tutor_model="google/gemma-4-26b-a4b-it",
            )

        self.assertEqual(provider_payload["fallback_reason"], "repair_response_could_not_be_parsed")
        self.assertEqual(provider_payload["fallback_provider_payload"]["provider"], "deterministic")
        self.assertIn("recommendation", tutor)

    def test_openrouter_tutor_falls_back_to_deterministic_if_request_errors(self) -> None:
        import mx1_tutor_v1

        manifest = {
            "family": "delegate",
            "question_id": "q1",
            "question_title": "Q1",
            "question_file": "q1.md",
            "loop_id": "loop-1",
            "starter_prompt_text": "starter",
            "exploration_iterations": 3,
            "history_summary": {},
        }
        grading_record = {
            "runtime_provider": "openrouter",
            "model": "google/gemma-4-26b-a4b-it",
            "grading": {"correct": False, "score": 0.0},
        }
        current_attempt = {
            "iteration_index": 2,
            "score": 0.0,
            "correct": False,
            "total_tokens": 100,
            "total_wall_time_ms": 200,
            "total_cost_usd": 0.1,
            "prompt_text": "current prompt",
        }

        class ErroringClient:
            def __init__(self, config):
                pass

            def create_chat_completion(self, **kwargs):
                raise mx1_tutor_v1.OpenRouterClientError("missing choices")

        with mock.patch.object(mx1_tutor_v1, "load_openrouter_api_key", return_value="test-key"), mock.patch.object(
            mx1_tutor_v1, "OpenRouterChatClient", ErroringClient
        ):
            tutor, provider_payload = mx1_tutor_v1._build_openrouter_tutor(
                manifest=manifest,
                grading_record=grading_record,
                current_attempt=current_attempt,
                prior_attempts=[],
                tutor_model="google/gemma-4-26b-a4b-it",
            )

        self.assertEqual(provider_payload["fallback_reason"], "openrouter_request_failed")
        self.assertEqual(provider_payload["fallback_provider_payload"]["provider"], "deterministic")
        self.assertIn("recommendation", tutor)


if __name__ == "__main__":
    unittest.main()

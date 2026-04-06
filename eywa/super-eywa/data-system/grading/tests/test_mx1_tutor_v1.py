from __future__ import annotations

import unittest


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


if __name__ == "__main__":
    unittest.main()

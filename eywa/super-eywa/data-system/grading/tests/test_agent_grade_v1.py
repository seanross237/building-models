from __future__ import annotations

import unittest
from pathlib import Path
import sys
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[3]
GRADING_DIR = REPO_ROOT / "data-system" / "grading"
if str(GRADING_DIR) not in sys.path:
    sys.path.insert(0, str(GRADING_DIR))


QUESTION_FILE = (
    REPO_ROOT
    / "data-system"
    / "grading"
    / "test-questions"
    / "architecture-derived-B6-binary-representation-minimization.md"
)


class AgentGradeV1Tests(unittest.TestCase):
    def test_deterministic_agent_grade_uses_reference_logic(self) -> None:
        from grading_methods.agent_grade_v1 import grade_result
        from question_bank_v1 import load_question_case

        question_case = load_question_case(source_path=QUESTION_FILE)
        grading, trace = grade_result(
            question_case,
            "FINAL_ANSWER: 3\nJUSTIFICATION: short",
            grading_provider="deterministic",
            grading_model="deterministic-agent-grader-v1",
        )

        self.assertEqual(grading["grading_status"], "graded")
        self.assertTrue(grading["correct"])
        self.assertEqual(grading["score"], 1.0)
        self.assertEqual(grading["grading_method"], "deterministic_reference_v1")
        self.assertEqual(trace["provider"], "deterministic")

    def test_agent_grader_parser_handles_raw_backslashes(self) -> None:
        from grading_methods.agent_grade_v1 import _parse_json_or_repair

        content = r'''
        {
          "grading_status": "graded",
          "correct": false,
          "score": 0.0,
          "expected": 3,
          "extracted_answer": "4",
          "normalized_answer": "4",
          "grading_notes": "Submission used \equiv incorrectly.",
          "confidence": "medium"
        }
        '''

        parsed = _parse_json_or_repair(content)

        self.assertEqual(parsed["grading_status"], "graded")
        self.assertIn(r"\equiv", parsed["grading_notes"])

    def test_agent_grader_falls_back_to_ungraded_if_repair_still_invalid(self) -> None:
        import grading_methods.agent_grade_v1 as agent_grade_v1
        from question_bank_v1 import load_question_case

        question_case = load_question_case(source_path=QUESTION_FILE)

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

        with mock.patch.object(agent_grade_v1, "load_openrouter_api_key", return_value="test-key"), mock.patch.object(
            agent_grade_v1, "OpenRouterChatClient", FakeClient
        ):
            grading, trace = agent_grade_v1.grade_result(
                question_case,
                "FINAL_ANSWER: 4\nJUSTIFICATION: short",
                grading_provider="openrouter",
                grading_model="google/gemma-4-26b-a4b-it",
            )

        self.assertEqual(grading["grading_status"], "ungraded")
        self.assertIsNone(grading["score"])
        self.assertEqual(trace["fallback_reason"], "repair_response_could_not_be_parsed")

    def test_detects_repairable_coding_output_failure(self) -> None:
        from grading_methods.agent_grade_v1 import _should_attempt_coding_repair

        grading = {"grading_status": "graded", "task_score": 0.0}
        trace = {
            "execution": {
                "instance_results": [
                    {
                        "scorer_payload": {
                            "stdout": "Out of range: 18\nScore = 0\n",
                            "stderr": "",
                            "notes": "",
                        }
                    }
                ]
            }
        }

        self.assertTrue(_should_attempt_coding_repair(grading=grading, trace=trace))

    def test_extract_python_repair_candidate_from_json_payload(self) -> None:
        from grading_methods.agent_grade_v1 import _extract_python_repair_candidate

        content = '{"main_py":"import sys\\nprint(0)\\n","notes":"simple valid baseline"}'

        extracted = _extract_python_repair_candidate(content)

        self.assertEqual(extracted, "import sys\nprint(0)")


if __name__ == "__main__":
    unittest.main()

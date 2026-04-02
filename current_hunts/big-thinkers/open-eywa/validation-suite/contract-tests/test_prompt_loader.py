from __future__ import annotations

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from system.runtime import PromptLoader, PromptLoaderError


class PromptLoaderTests(unittest.TestCase):
    def test_planner_prompt_bundle_loads_support_docs(self) -> None:
        bundle = PromptLoader().load("planner")

        self.assertEqual(bundle.role, "planner")
        self.assertIn("You are the `planner` role", bundle.system_prompt)
        self.assertGreaterEqual(len(bundle.support_documents), 2)
        self.assertIn("stuff-for-agents/planning/planner/system-prompt.md", bundle.source_paths)

    def test_unknown_role_raises(self) -> None:
        with self.assertRaises(PromptLoaderError):
            PromptLoader().load("not-a-real-role")

    def test_prompt_bundles_use_node_json_control_language(self) -> None:
        loader = PromptLoader()
        evaluator_bundle = loader.load("mid-plan-evaluator")
        synthesizer_bundle = loader.load("synthesizer")

        evaluator_text = "\n".join(
            [evaluator_bundle.system_prompt, *(text for _, text in evaluator_bundle.support_documents)]
        )
        synthesizer_text = "\n".join(
            [synthesizer_bundle.system_prompt, *(text for _, text in synthesizer_bundle.support_documents)]
        )

        self.assertNotIn("for-orchestrator/eval-decision", evaluator_text)
        self.assertNotIn("for-orchestrator/next-action-after-child-report", evaluator_text)
        self.assertIn("NEXT_ACTION_AFTER_CHILD_REPORT", evaluator_text)
        self.assertNotIn("for-orchestrator/eval-decision", synthesizer_text)

    def test_worker_prompt_mentions_input_context_handoff(self) -> None:
        worker_bundle = PromptLoader().load("worker")

        self.assertIn("input/context.md", worker_bundle.system_prompt)


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import os
import sys
import unittest
from unittest.mock import patch
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from system.runtime import (
    LIVE_CANARY_DEFAULT_MODEL,
    LiveCanaryRuntimeSettings,
    build_openrouter_runtime_for_live_canary,
    default_live_canary_role_models,
)


class RuntimeFactoryTests(unittest.TestCase):
    def test_default_live_canary_role_models_cover_all_current_roles(self) -> None:
        mapping = default_live_canary_role_models()
        self.assertEqual(set(mapping.values()), {LIVE_CANARY_DEFAULT_MODEL})
        self.assertEqual(
            set(mapping.keys()),
            {
                "librarian",
                "planner",
                "plan-reviewer",
                "plan-decider",
                "worker",
                "mid-plan-evaluator",
                "synthesizer",
            },
        )

    def test_build_openrouter_runtime_uses_environment_key(self) -> None:
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}, clear=False):
            runtime = build_openrouter_runtime_for_live_canary(
                LiveCanaryRuntimeSettings(model_name="google/gemini-2.5-flash-lite")
            )
        self.assertEqual(
            runtime.config.default_models["worker"],
            "google/gemini-2.5-flash-lite",
        )
        self.assertEqual(runtime.config.api_key, "test-key")


if __name__ == "__main__":
    unittest.main()

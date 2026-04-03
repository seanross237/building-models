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
    LiveRuntimeSettings,
    build_live_runtime,
    build_openrouter_runtime_for_live_canary,
    default_live_canary_role_models,
)
from system.runtime.claude_cli_runtime import ClaudeCliRuntime
from system.runtime.codex_cli_runtime import CodexCliRuntime
from system.runtime.openrouter_runtime import OpenRouterRuntime


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


class BuildLiveRuntimeTests(unittest.TestCase):
    def test_openrouter_provider_returns_openrouter_runtime(self) -> None:
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}, clear=False):
            runtime = build_live_runtime(
                LiveRuntimeSettings(runtime_provider="openrouter")
            )
        self.assertIsInstance(runtime, OpenRouterRuntime)

    def test_claude_provider_returns_claude_runtime(self) -> None:
        runtime = build_live_runtime(
            LiveRuntimeSettings(
                runtime_provider="claude",
                model_name="claude-sonnet-4-6",
            )
        )
        self.assertIsInstance(runtime, ClaudeCliRuntime)
        self.assertEqual(runtime.config.default_models["worker"], "claude-sonnet-4-6")

    def test_codex_provider_returns_codex_runtime(self) -> None:
        runtime = build_live_runtime(
            LiveRuntimeSettings(
                runtime_provider="codex",
                model_name="gpt-5.4-mini",
            )
        )
        self.assertIsInstance(runtime, CodexCliRuntime)
        self.assertEqual(runtime.config.default_models["worker"], "gpt-5.4-mini")

    def test_cli_runtime_inherits_max_turns(self) -> None:
        runtime = build_live_runtime(
            LiveRuntimeSettings(
                runtime_provider="claude",
                max_turns=10,
            )
        )
        self.assertEqual(runtime.config.max_turns, 10)

    def test_cli_runtime_inherits_timeout(self) -> None:
        runtime = build_live_runtime(
            LiveRuntimeSettings(
                runtime_provider="codex",
                timeout_seconds=600,
            )
        )
        self.assertEqual(runtime.config.timeout_seconds, 600)

    def test_default_settings_use_openrouter(self) -> None:
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}, clear=False):
            runtime = build_live_runtime()
        self.assertIsInstance(runtime, OpenRouterRuntime)


if __name__ == "__main__":
    unittest.main()

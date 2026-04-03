from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
import subprocess

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from system.runtime.cli_runtime_base import CliRuntimeConfig
from system.runtime.claude_cli_runtime import ClaudeCliRuntime
from system.runtime.runtime_interface import RuntimeRequest


def _make_config(**overrides: object) -> CliRuntimeConfig:
    defaults = {
        "default_models": {"worker": "claude-sonnet-4-6"},
        "max_turns": 6,
        "timeout_seconds": 60,
    }
    defaults.update(overrides)
    return CliRuntimeConfig(**defaults)


def _make_request(tmp_path: Path, **overrides: object) -> RuntimeRequest:
    defaults = {
        "mission_id": "m-001",
        "node_id": "n-001",
        "node_path": str(tmp_path),
        "run_id": "r-001",
        "role": "worker",
    }
    defaults.update(overrides)
    return RuntimeRequest(**defaults)


class TestClaudeCliRuntimeCommand(unittest.TestCase):
    def test_build_command_shape(self) -> None:
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            runtime = ClaudeCliRuntime(_make_config())
            task_file = tmp_path / "runtime-task.md"
            task_file.touch()
            cmd = runtime._build_command(
                _make_request(tmp_path),
                task_file,
                "claude-sonnet-4-6",
            )
        self.assertEqual(cmd[0], "claude")
        self.assertEqual(cmd[1], "-p")
        self.assertIn("--model", cmd)
        model_idx = cmd.index("--model")
        self.assertEqual(cmd[model_idx + 1], "claude-sonnet-4-6")
        self.assertNotIn("--max-turns", cmd)
        self.assertIn("--allowedTools", cmd)
        self.assertIn("--output-format", cmd)
        self.assertIn("--permission-mode", cmd)
        perm_idx = cmd.index("--permission-mode")
        self.assertEqual(cmd[perm_idx + 1], "bypassPermissions")

    def test_provider_name(self) -> None:
        runtime = ClaudeCliRuntime(_make_config())
        self.assertEqual(runtime.provider_name, "claude")


class TestClaudeCliRuntimeRun(unittest.TestCase):
    def test_successful_run_produces_valid_result(self) -> None:
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            output_dir = tmp_path / "output"
            output_dir.mkdir()
            (output_dir / "final-output.md").write_text("result", encoding="utf-8")

            runtime = ClaudeCliRuntime(_make_config())
            # Mock the prompt loader
            mock_bundle = MagicMock()
            mock_bundle.system_prompt = "Test prompt"
            mock_bundle.support_documents = ()
            mock_bundle.source_paths = ("test.md",)
            runtime.prompt_loader = MagicMock()
            runtime.prompt_loader.load.return_value = mock_bundle

            request = _make_request(tmp_path)
            mock_proc = subprocess.CompletedProcess(
                args=["claude", "-p", "..."],
                returncode=0,
                stdout="Done.",
                stderr="",
            )
            with patch("system.runtime.cli_runtime_base.subprocess.run", return_value=mock_proc):
                result = runtime.run(request)

        self.assertEqual(result.exit_reason, "completed")
        self.assertEqual(result.model, "claude-sonnet-4-6")
        self.assertIn("output/final-output.md", result.artifacts_produced)
        self.assertEqual(result.usage.total_cost_usd, 0.0)
        self.assertEqual(
            result.usage.provider_details["provider_kind"],
            "cli_subscription",
        )

    def test_cli_not_found_returns_crashed(self) -> None:
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            runtime = ClaudeCliRuntime(_make_config())
            mock_bundle = MagicMock()
            mock_bundle.system_prompt = "Test"
            mock_bundle.support_documents = ()
            mock_bundle.source_paths = ("test.md",)
            runtime.prompt_loader = MagicMock()
            runtime.prompt_loader.load.return_value = mock_bundle

            request = _make_request(tmp_path)
            with patch(
                "system.runtime.cli_runtime_base.subprocess.run",
                side_effect=FileNotFoundError("claude not found"),
            ):
                result = runtime.run(request)

        self.assertEqual(result.exit_reason, "crashed")
        self.assertIn("CLI not found", result.details["error"])

    def test_timeout_returns_timed_out(self) -> None:
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            runtime = ClaudeCliRuntime(_make_config(timeout_seconds=1))
            mock_bundle = MagicMock()
            mock_bundle.system_prompt = "Test"
            mock_bundle.support_documents = ()
            mock_bundle.source_paths = ("test.md",)
            runtime.prompt_loader = MagicMock()
            runtime.prompt_loader.load.return_value = mock_bundle

            request = _make_request(tmp_path)
            with patch(
                "system.runtime.cli_runtime_base.subprocess.run",
                side_effect=subprocess.TimeoutExpired(cmd="claude", timeout=1),
            ):
                result = runtime.run(request)

        self.assertEqual(result.exit_reason, "timed_out")


if __name__ == "__main__":
    unittest.main()

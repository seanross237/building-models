"""Claude CLI runtime adapter.

Runs Open-Eywa nodes via `claude -p` in non-interactive mode.
"""

from __future__ import annotations

from pathlib import Path

from .cli_runtime_base import CliRuntimeBase
from .runtime_interface import RuntimeRequest


class ClaudeCliRuntime(CliRuntimeBase):
    """Runtime adapter that executes nodes via the Claude CLI."""

    provider_name = "claude"

    def _build_command(
        self,
        request: RuntimeRequest,
        task_file: Path,
        model: str,
    ) -> list[str]:
        return [
            "claude",
            "-p",
            (
                f"Read the file `{task_file.name}` in the current directory "
                f"and follow its instructions exactly. "
                f"Write all required output artifacts under `output/`."
            ),
            "--model",
            model,
            "--output-format",
            "text",
            "--permission-mode",
            "bypassPermissions",
            "--allowedTools",
            "Read,Write,Edit,Glob,Grep",
        ]

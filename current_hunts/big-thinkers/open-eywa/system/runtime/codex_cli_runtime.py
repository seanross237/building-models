"""Codex CLI runtime adapter.

Runs Open-Eywa nodes via `codex exec` in non-interactive mode.
"""

from __future__ import annotations

from pathlib import Path

from .cli_runtime_base import CliRuntimeBase
from .runtime_interface import RuntimeRequest


class CodexCliRuntime(CliRuntimeBase):
    """Runtime adapter that executes nodes via the Codex CLI."""

    provider_name = "codex"

    def _build_command(
        self,
        request: RuntimeRequest,
        task_file: Path,
        model: str,
    ) -> list[str]:
        return [
            "codex",
            "exec",
            (
                f"Read the file `{task_file.name}` in the current directory "
                f"and follow its instructions exactly. "
                f"Write all required output artifacts under `output/`."
            ),
            "--model",
            model,
            "--sandbox",
            "workspace-write",
        ]

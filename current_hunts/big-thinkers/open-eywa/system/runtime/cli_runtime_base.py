"""Shared base for CLI-backed runtime adapters (Claude CLI, Codex CLI).

Handles prompt loading, task file assembly, subprocess execution,
stdout/stderr capture, artifact scanning, and RuntimeResult construction.
Provider-specific adapters subclass this and override _build_command().
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from time import perf_counter
from typing import Any

from system.orchestrator.event_schema import utc_now_iso
from system.orchestrator.usage_schema import UsageRecord

from .prompt_loader import PromptLoader, PromptLoaderError
from .runtime_interface import RuntimeRequest, RuntimeResult
from .runtime_task_builder import (
    RuntimeTaskBuildError,
    build_runtime_task_content,
    load_prepared_packet,
)


class CliRuntimeError(RuntimeError):
    """Raised when a CLI-backed runtime cannot safely complete a run."""


@dataclass(frozen=True)
class CliRuntimeConfig:
    """Configuration shared by all CLI runtime adapters."""

    default_models: dict[str, str]
    max_turns: int = 6
    timeout_seconds: int = 300


class CliRuntimeBase:
    """Base class for CLI-backed runtimes.

    Subclasses must set `provider_name` and implement `_build_command()`.
    """

    provider_name: str = ""

    def __init__(
        self,
        config: CliRuntimeConfig,
        *,
        prompt_loader: PromptLoader | None = None,
    ) -> None:
        self.config = config
        self.prompt_loader = prompt_loader or PromptLoader()

    def run(self, request: RuntimeRequest) -> RuntimeResult:
        model = request.model or self.config.default_models.get(request.role)
        if not model:
            raise CliRuntimeError(
                f"No model provided and no default for role {request.role!r}."
            )

        try:
            prompt_bundle = self.prompt_loader.load(request.role)
        except PromptLoaderError as exc:
            raise CliRuntimeError(str(exc)) from exc

        prepared_packets = []
        for path in request.prepared_inputs:
            try:
                prepared_packets.append(load_prepared_packet(path))
            except RuntimeTaskBuildError as exc:
                raise CliRuntimeError(str(exc)) from exc

        task_content = build_runtime_task_content(
            request,
            prompt_bundle,
            prepared_packets,
            provider_name=self.provider_name,
        )

        node_root = request.node_root
        task_file = node_root / "runtime-task.md"
        node_root.mkdir(parents=True, exist_ok=True)
        task_file.write_text(task_content, encoding="utf-8")

        command = self._build_command(request, task_file, model)

        started_at = utc_now_iso()
        start_clock = perf_counter()

        try:
            proc = subprocess.run(
                command,
                cwd=str(node_root),
                stdin=subprocess.DEVNULL,
                capture_output=True,
                text=True,
                timeout=self.config.timeout_seconds,
            )
        except subprocess.TimeoutExpired as exc:
            self._save_cli_output(node_root, exc.stdout or "", exc.stderr or "")
            return self._build_result(
                request,
                model=model,
                exit_reason="timed_out",
                started_at=started_at,
                start_clock=start_clock,
                node_root=node_root,
                returncode=-1,
                command=command,
                task_file=task_file,
                prompt_bundle_paths=list(prompt_bundle.source_paths),
                extra_details={"timeout_seconds": self.config.timeout_seconds},
            )
        except FileNotFoundError:
            return self._build_result(
                request,
                model=model,
                exit_reason="crashed",
                started_at=started_at,
                start_clock=start_clock,
                node_root=node_root,
                returncode=-1,
                command=command,
                task_file=task_file,
                prompt_bundle_paths=list(prompt_bundle.source_paths),
                extra_details={
                    "error": f"CLI not found: {command[0]!r}. Is it installed and on PATH?"
                },
            )
        except OSError as exc:
            return self._build_result(
                request,
                model=model,
                exit_reason="crashed",
                started_at=started_at,
                start_clock=start_clock,
                node_root=node_root,
                returncode=-1,
                command=command,
                task_file=task_file,
                prompt_bundle_paths=list(prompt_bundle.source_paths),
                extra_details={"error": str(exc)},
            )

        self._save_cli_output(node_root, proc.stdout, proc.stderr)

        exit_reason = "completed" if proc.returncode == 0 else "failed"

        return self._build_result(
            request,
            model=model,
            exit_reason=exit_reason,
            started_at=started_at,
            start_clock=start_clock,
            node_root=node_root,
            returncode=proc.returncode,
            command=command,
            task_file=task_file,
            prompt_bundle_paths=list(prompt_bundle.source_paths),
        )

    def _build_command(
        self,
        request: RuntimeRequest,
        task_file: Path,
        model: str,
    ) -> list[str]:
        """Return the CLI command to execute. Subclasses must override."""
        raise NotImplementedError

    def _scan_artifacts(self, node_root: Path) -> tuple[str, ...]:
        """Scan node output/ directory for produced artifacts."""
        output_dir = node_root / "output"
        if not output_dir.is_dir():
            return ()
        artifacts = []
        for path in sorted(output_dir.rglob("*")):
            if path.is_file():
                artifacts.append(str(path.relative_to(node_root)))
        return tuple(artifacts)

    def _save_cli_output(
        self, node_root: Path, stdout: str, stderr: str
    ) -> None:
        """Write CLI stdout/stderr to disk for inspectability."""
        if stdout:
            (node_root / "cli-stdout.txt").write_text(stdout, encoding="utf-8")
        if stderr:
            (node_root / "cli-stderr.txt").write_text(stderr, encoding="utf-8")

    def _build_result(
        self,
        request: RuntimeRequest,
        *,
        model: str,
        exit_reason: str,
        started_at: str,
        start_clock: float,
        node_root: Path,
        returncode: int,
        command: list[str],
        task_file: Path,
        prompt_bundle_paths: list[str],
        extra_details: dict[str, Any] | None = None,
    ) -> RuntimeResult:
        artifacts = self._scan_artifacts(node_root)
        details: dict[str, Any] = {
            "provider_name": self.provider_name,
            "command": [str(c) for c in command],
            "returncode": returncode,
            "task_file_path": str(task_file),
            "prompt_bundle_paths": prompt_bundle_paths,
            "prepared_inputs": list(request.prepared_inputs),
        }
        stdout_path = node_root / "cli-stdout.txt"
        stderr_path = node_root / "cli-stderr.txt"
        if stdout_path.exists():
            details["stdout_path"] = str(stdout_path)
        if stderr_path.exists():
            details["stderr_path"] = str(stderr_path)
        if extra_details:
            details.update(extra_details)

        return RuntimeResult(
            mission_id=request.mission_id,
            node_id=request.node_id,
            node_path=request.node_path,
            run_id=request.run_id,
            role=request.role,
            model=model,
            variant=request.variant,
            exit_reason=exit_reason,
            started_at_utc=started_at,
            finished_at_utc=utc_now_iso(),
            duration_seconds=perf_counter() - start_clock,
            artifacts_produced=artifacts,
            tool_call_count=0,
            usage=UsageRecord(
                total_cost_usd=0.0,
                provider_details={
                    "provider_name": self.provider_name,
                    "provider_kind": "cli_subscription",
                    "accounting_mode": "subscription_or_external",
                    "usage_unavailable": True,
                },
            ),
            details=details,
        )

"""Claude CLI adapter — spawns `claude -p --output-format json` as a subprocess.

Mirrors the pattern in `research_hub/research-radar/runner/agent-runner/lib/claude.js`:
the CLI returns a JSON envelope where `result` holds the assistant's text,
and inside that text we expect a JSON object with a `premises` array.
"""
from __future__ import annotations

import json
import logging
import shutil
import subprocess
import time
from typing import Any, Dict, List, Optional

from idea_factory.adapter import ModelAdapter, Premise, PremiseResult
from idea_factory.adapters._json_parsing import extract_first_json_object, find_premise_list


LOG = logging.getLogger("idea_factory.adapters.claude_cli")

SYSTEM_PROMPT = "\n".join(
    [
        "You are running an automated scheduled task.",
        "Work autonomously and output only the requested JSON object.",
        "Do not wrap the JSON in markdown fences.",
    ]
)


class ClaudeCLIAdapter(ModelAdapter):
    """Real Claude adapter via the locally-installed `claude` CLI."""

    model_id = "claude-opus"

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        # Allow `id` from models.yaml to override the default model_id label.
        if "id" in self.config:
            self.model_id = str(self.config["id"])
        self.cli_model: str = str(self.config.get("cli_model", "claude-opus-4-6"))
        self.timeout_sec: int = int(self.config.get("timeout_sec", 120))
        self.max_turns: int = int(self.config.get("max_turns", 1))

    # ----------------------------------------------------------------- helpers

    def _binary(self) -> Optional[str]:
        return shutil.which("claude")

    def is_available(self) -> bool:
        return self._binary() is not None

    def _build_command(self, prompt: str) -> List[str]:
        return [
            self._binary() or "claude",
            "-p",
            prompt,
            "--output-format",
            "json",
            "--model",
            self.cli_model,
            "--dangerously-skip-permissions",
            "--append-system-prompt",
            SYSTEM_PROMPT,
            "--max-turns",
            str(self.max_turns),
        ]

    # ----------------------------------------------------------------- generate

    def generate(
        self,
        signal: Dict[str, Any],
        prompt: str,
        n_premises: int = 3,
    ) -> PremiseResult:
        signal_id = str(signal.get("signal_id") or signal.get("id") or "unknown")
        result = PremiseResult(model_id=self.model_id, signal_id=signal_id)
        if not self.is_available():
            result.error = "claude CLI not on PATH"
            return result

        cmd = self._build_command(prompt)
        started = time.time()
        try:
            completed = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False,
                timeout=self.timeout_sec,
            )
        except subprocess.TimeoutExpired as exc:
            result.error = f"claude CLI timed out after {self.timeout_sec}s"
            result.duration_ms = int((time.time() - started) * 1000)
            return result
        except Exception as exc:  # pragma: no cover - defensive
            result.error = f"claude CLI invocation failed: {exc}"
            result.duration_ms = int((time.time() - started) * 1000)
            return result

        result.duration_ms = int((time.time() - started) * 1000)
        stdout = (completed.stdout or "").strip()
        stderr = (completed.stderr or "").strip()

        if completed.returncode != 0 and not stdout:
            result.error = f"claude exit {completed.returncode}: {stderr[:300]}"
            return result

        # Step 1: parse the CLI envelope.
        envelope: Optional[Dict[str, Any]] = None
        try:
            envelope = json.loads(stdout)
        except json.JSONDecodeError:
            envelope = None

        inner_text = ""
        if isinstance(envelope, dict):
            # The CLI puts the assistant text in `result`. Older builds use
            # `response`. Fall back to the raw stdout if neither is set.
            inner_text = str(envelope.get("result") or envelope.get("response") or "").strip()
            cost_usd = envelope.get("total_cost_usd")
            if isinstance(cost_usd, (int, float)):
                result.cost_cents = int(round(float(cost_usd) * 100))
        if not inner_text:
            inner_text = stdout

        result.raw_response = inner_text

        # Step 2: parse the inner JSON for premises.
        parsed = extract_first_json_object(inner_text)
        if parsed is None:
            result.error = "claude response did not contain a JSON object"
            return result

        premise_dicts = find_premise_list(parsed)
        if not premise_dicts:
            result.error = "claude response had no premises"
            return result

        result.premises = [Premise.from_dict(p) for p in premise_dicts[:n_premises]]
        if not result.premises:
            result.error = "claude premises were empty after parsing"
        return result


__all__ = ["ClaudeCLIAdapter"]

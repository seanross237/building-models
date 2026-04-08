"""Claude frame critic adapter.

Reuses the Phase 3 ClaudeCLIAdapter subprocess pattern (`claude -p
--output-format json`) to score clips. The Claude CLI is a text-only
seam — it does not accept image attachments — so this adapter:

    1. Samples N frames from the clip with `frame_sampler.sample_frames`
       (purely so we know how many frames exist + can write a manifest
       on disk for later inspection / regression debugging).
    2. Optionally extracts a 16kHz mono WAV via ffmpeg and runs whisper
       on it if whisper happens to be installed (it isn't a project
       dependency — the import is lazy).
    3. Builds a text prompt describing the beat, the storyboard
       expectations, the number of sampled frames, and any transcript.
    4. Spawns `claude -p` and parses the inner JSON response, the same
       way the Phase 3 ClaudeCLIAdapter does.

This is intentionally weaker than the Gemini video critic — Claude
doesn't see the pixels — but it's a useful second opinion for the cases
where `GEMINI_API_KEY` isn't set and the user does have Claude CLI
authenticated. It's also a clean place to hang the Whisper transcript
hook for the audio side of "is this funny" judgments.
"""
from __future__ import annotations

import json
import logging
import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from critic.adapter import CriticAdapter, ShotReport, SketchCritique
from critic.frame_sampler import (
    extract_audio_wav,
    sample_frames,
    transcribe_with_whisper,
)
from idea_factory.adapters._json_parsing import extract_first_json_object


LOG = logging.getLogger("critic.adapters.claude_frame")
SYSTEM_PROMPT = "\n".join(
    [
        "You are running an automated scheduled task.",
        "Work autonomously and output only the requested JSON object.",
        "Do not wrap the JSON in markdown fences.",
    ]
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class ClaudeFrameCritic(CriticAdapter):
    adapter_id = "claude-frame-critic"

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self.cli_model: str = str(self.config.get("cli_model", "claude-opus-4-6"))
        self.timeout_sec: int = int(self.config.get("timeout_sec", 120))
        self.n_frames_per_clip: int = int(self.config.get("n_frames_per_clip", 4))
        self.max_turns: int = int(self.config.get("max_turns", 1))

    # ----------------------------------------------------------------- helpers

    def _binary(self) -> Optional[str]:
        return shutil.which("claude")

    def is_available(self) -> bool:
        return self._binary() is not None

    def _run_claude(self, prompt: str) -> str:
        """Spawn `claude -p`, return the assistant's text. Raises on hard failure."""
        binary = self._binary()
        if not binary:
            raise RuntimeError("claude CLI not on PATH")
        cmd = [
            binary,
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
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False,
                timeout=self.timeout_sec,
            )
        except subprocess.TimeoutExpired:
            raise RuntimeError(f"claude CLI timed out after {self.timeout_sec}s")
        if result.returncode != 0 and not (result.stdout or "").strip():
            raise RuntimeError(f"claude exit {result.returncode}: {(result.stderr or '')[:300]}")

        stdout = (result.stdout or "").strip()
        try:
            envelope = json.loads(stdout)
        except json.JSONDecodeError:
            envelope = None
        if isinstance(envelope, dict):
            inner = str(envelope.get("result") or envelope.get("response") or "").strip()
            if inner:
                return inner
        return stdout

    def _maybe_transcript(self, clip_path: Path) -> Optional[str]:
        """Pull a transcript via ffmpeg + whisper if both happen to be available."""
        with tempfile.TemporaryDirectory() as tmpdir:
            wav_path = Path(tmpdir) / "audio.wav"
            extracted = extract_audio_wav(clip_path, wav_path)
            if extracted is None:
                return None
            return transcribe_with_whisper(extracted)

    def _sample_to_temp(self, clip_path: Path, n: int) -> List[Path]:
        if n <= 0:
            return []
        out_dir = Path(tempfile.mkdtemp(prefix="claude_frame_"))
        return sample_frames(clip_path, n, out_dir)

    # ----------------------------------------------------------------- shot check

    def check_shot(
        self,
        clip_path: Path,
        expected_frame: Path,
        character_refs: List[Path],
        beat_metadata: Dict[str, Any],
    ) -> ShotReport:
        beat_n = int(beat_metadata.get("n", 1) or 1)
        report = ShotReport(
            beat_n=beat_n,
            passed=True,
            score=0,
            adapter_id=self.adapter_id,
        )

        if not self.is_available():
            report.error = "claude CLI not on PATH"
            return report

        if not Path(clip_path).exists() or Path(clip_path).stat().st_size == 0:
            report.error = f"clip missing or empty: {clip_path}"
            return report

        sampled = self._sample_to_temp(clip_path, self.n_frames_per_clip)
        characters = beat_metadata.get("characters") or []
        char_names = ", ".join(
            c.get("name", "") if isinstance(c, dict) else str(c) for c in characters
        )

        prompt = "\n".join(
            [
                "You are an automated quality control reviewer for an AI-generated comedy clip.",
                "You will not see the pixels — you must reason from the metadata I provide.",
                "Your job is to flag obvious technical / continuity problems in the rendered beat.",
                "",
                f"Beat number: {beat_n}",
                f"Action: {beat_metadata.get('action', '')}",
                f"Camera: {beat_metadata.get('camera', '')}",
                f"Location: {beat_metadata.get('location', '')}",
                f"Visual note: {beat_metadata.get('visual_note', '')}",
                f"Characters expected: {char_names or '(none)'}",
                f"Storyboard reference frame on disk: {expected_frame}",
                f"Character ref images on disk: {[str(p) for p in character_refs]}",
                f"Sampled frame count from the rendered clip: {len(sampled)}",
                f"Clip path: {clip_path}",
                "",
                "Default to passed=true unless something in the metadata is obviously broken",
                "(e.g. no frames could be sampled, the clip path is missing, etc.).",
                "",
                "Output ONLY this JSON, no markdown fences:",
                '{"passed": true, "score": 7, "issues": [], "suggestions": []}',
            ]
        )

        started = time.time()
        try:
            text = self._run_claude(prompt)
        except Exception as exc:
            report.error = f"claude shot check failed: {exc}"
            report.duration_ms = int((time.time() - started) * 1000)
            return report
        report.duration_ms = int((time.time() - started) * 1000)
        report.raw_response = text

        parsed = extract_first_json_object(text)
        if not isinstance(parsed, dict):
            report.error = "claude shot response was not a JSON object"
            return report
        try:
            report.passed = bool(parsed.get("passed", True))
            report.score = int(parsed.get("score", 0) or 0)
            report.issues = [str(x) for x in (parsed.get("issues") or [])]
            report.suggestions = [str(x) for x in (parsed.get("suggestions") or [])]
        except Exception as exc:
            report.error = f"claude shot response coerce failed: {exc}"
            report.passed = True
        return report

    # ----------------------------------------------------------------- full critique

    def critique_sketch(
        self,
        final_cut_path: Path,
        sketch_metadata: Dict[str, Any],
    ) -> SketchCritique:
        critique = SketchCritique(
            sketch_id=str(sketch_metadata.get("sketch_id", "unknown")),
            overall_score=0,
            adapter_id=self.adapter_id,
        )

        if not self.is_available():
            critique.error = "claude CLI not on PATH"
            return critique

        if not Path(final_cut_path).exists() or Path(final_cut_path).stat().st_size == 0:
            critique.error = f"final cut missing or empty: {final_cut_path}"
            return critique

        # Sample more frames across the full cut for the headline critique.
        sampled = self._sample_to_temp(final_cut_path, max(self.n_frames_per_clip * 2, 8))
        transcript = self._maybe_transcript(final_cut_path) or ""

        prompt = "\n".join(
            [
                "You are an automated comedy critic reviewing a 30-second AI-generated sketch.",
                "You cannot see the pixels — reason from the metadata and any transcript I provide.",
                "Be specific. Avoid generic praise.",
                "",
                f"Logline: {sketch_metadata.get('logline', '')}",
                f"Tone: {sketch_metadata.get('tone', '')}",
                f"Twist: {sketch_metadata.get('twist', '')}",
                f"Beat count: {sketch_metadata.get('beat_count', 0)}",
                f"Target length sec: {sketch_metadata.get('target_length_sec', 30)}",
                f"Frames sampled across the full cut: {len(sampled)}",
                f"Audio transcript (may be empty): {transcript or '(no transcript available)'}",
                "",
                "Output ONLY this JSON shape, no markdown fences:",
                '{"overall_score": 7, "is_funny": true, "axes": {"comedic_timing":7,"pacing":6,"punchline_landing":7,"audio_clarity":5,"character_consistency":7}, "issues": ["..."], "fix_suggestions": ["..."], "verdict": "one short sentence"}',
            ]
        )

        started = time.time()
        try:
            text = self._run_claude(prompt)
        except Exception as exc:
            critique.error = f"claude critique failed: {exc}"
            critique.duration_ms = int((time.time() - started) * 1000)
            return critique
        critique.duration_ms = int((time.time() - started) * 1000)
        critique.raw_response = text

        parsed = extract_first_json_object(text)
        if not isinstance(parsed, dict):
            critique.error = "claude sketch response was not a JSON object"
            return critique
        try:
            critique.overall_score = int(parsed.get("overall_score", 0) or 0)
            critique.is_funny = bool(parsed.get("is_funny", False))
            axes = parsed.get("axes") or {}
            critique.axes = {str(k): int(v or 0) for k, v in axes.items()}
            critique.issues = [str(x) for x in (parsed.get("issues") or [])]
            critique.fix_suggestions = [str(x) for x in (parsed.get("fix_suggestions") or [])]
            critique.verdict = str(parsed.get("verdict", "")).strip()
        except Exception as exc:
            critique.error = f"claude sketch response coerce failed: {exc}"
        return critique


__all__ = ["ClaudeFrameCritic"]

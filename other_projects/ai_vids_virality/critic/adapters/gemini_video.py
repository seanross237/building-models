"""Gemini 2.5 Pro video critic adapter.

Uses the same Google AI Studio REST endpoint pattern as the Phase 4
storyboard adapter, but with `gemini-2.5-pro` and the clip MP4 sent
inline as `inline_data` with `mime_type: video/mp4`. The model's
response is expected to be a JSON object matching either the
`ShotReport` or the `SketchCritique` schema (the prompt asks for it
explicitly).

Critical contract:
    - On any failure path the adapter MUST return the dataclass with
      `error` set and never raise.
    - For shot checks specifically, infrastructure failures return
      `passed=True` so the video pipeline doesn't loop forever
      regenerating clips because of our network problems.
"""
from __future__ import annotations

import base64
import logging
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from critic.adapter import CriticAdapter, ShotReport, SketchCritique
from idea_factory.adapters._json_parsing import extract_first_json_object


LOG = logging.getLogger("critic.adapters.gemini_video")
URL_TEMPLATE = (
    "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
)
ENV_KEY = "GEMINI_API_KEY"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SHOT_PROMPT_PATH = PROJECT_ROOT / "critic" / "prompts" / "shot_check.md"
FULL_PROMPT_PATH = PROJECT_ROOT / "critic" / "prompts" / "full_sketch.md"


def _load_prompt(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def _format_shot_prompt(beat: Dict[str, Any]) -> str:
    template = _load_prompt(SHOT_PROMPT_PATH)
    if not template:
        return "Inspect this clip and return JSON with passed/score/issues/suggestions."
    characters = beat.get("characters") or []
    char_names = ", ".join(
        c.get("name", "") if isinstance(c, dict) else str(c) for c in characters
    ).strip(", ")
    return template.format(
        beat_n=beat.get("n", 1),
        action=str(beat.get("action", "")).strip(),
        camera=str(beat.get("camera", "medium")).strip(),
        location=str(beat.get("location", "")).strip(),
        visual_note=str(beat.get("visual_note", "")).strip(),
        character_names=char_names or "(none)",
    )


def _format_full_prompt(meta: Dict[str, Any]) -> str:
    template = _load_prompt(FULL_PROMPT_PATH)
    if not template:
        return "Critique this sketch and return JSON with overall_score/axes/issues/fix_suggestions/verdict."
    return template.format(
        logline=str(meta.get("logline", "")),
        tone=str(meta.get("tone", "")),
        twist=str(meta.get("twist", "")),
        target_length_sec=meta.get("target_length_sec", 30),
        beat_count=meta.get("beat_count", 0),
        audio_transcript=str(meta.get("audio_transcript", "") or "(no transcript available)"),
    )


class GeminiVideoCritic(CriticAdapter):
    adapter_id = "gemini-2.5-pro"

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self.model: str = str(self.config.get("model", "gemini-2.5-pro"))
        self.timeout_sec: int = int(self.config.get("timeout_sec", 120))

    def is_available(self) -> bool:
        return bool(os.environ.get(ENV_KEY))

    # ----------------------------------------------------------------- HTTP

    def _post(self, parts: List[Dict[str, Any]]) -> Dict[str, Any]:
        try:
            import httpx
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError("httpx unavailable") from exc

        url = URL_TEMPLATE.format(model=self.model)
        body = {
            "contents": [{"role": "user", "parts": parts}],
            "generationConfig": {
                "responseMimeType": "application/json",
            },
        }
        response = httpx.post(
            url,
            params={"key": os.environ.get(ENV_KEY)},
            headers={"Content-Type": "application/json"},
            json=body,
            timeout=self.timeout_sec,
        )
        if response.status_code != 200:
            raise RuntimeError(f"gemini-video status {response.status_code}: {response.text[:300]}")
        try:
            return response.json()
        except Exception as exc:
            raise RuntimeError(f"gemini-video json decode failed: {exc}")

    def _extract_text(self, payload: Dict[str, Any]) -> str:
        try:
            return str(payload["candidates"][0]["content"]["parts"][0]["text"])
        except (KeyError, IndexError, TypeError):
            return ""

    def _video_part(self, clip_path: Path) -> Dict[str, Any]:
        raw = Path(clip_path).read_bytes()
        return {
            "inline_data": {
                "mime_type": "video/mp4",
                "data": base64.b64encode(raw).decode("ascii"),
            }
        }

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
            passed=True,  # default to True so failures don't loop
            score=0,
            adapter_id=self.adapter_id,
        )

        if not self.is_available():
            report.error = f"{ENV_KEY} not set"
            return report

        if not Path(clip_path).exists() or Path(clip_path).stat().st_size == 0:
            report.error = f"clip missing or empty: {clip_path}"
            return report

        prompt = _format_shot_prompt(beat_metadata)
        parts: List[Dict[str, Any]] = [{"text": prompt}]
        try:
            parts.append(self._video_part(clip_path))
        except Exception as exc:
            report.error = f"could not read clip bytes: {exc}"
            return report
        # Optionally include the storyboard reference frame.
        try:
            if Path(expected_frame).exists():
                ref_bytes = Path(expected_frame).read_bytes()
                parts.append(
                    {
                        "inline_data": {
                            "mime_type": "image/png",
                            "data": base64.b64encode(ref_bytes).decode("ascii"),
                        }
                    }
                )
        except Exception:
            pass

        started = time.time()
        try:
            payload = self._post(parts)
        except Exception as exc:
            report.error = f"gemini-video request failed: {exc}"
            report.duration_ms = int((time.time() - started) * 1000)
            return report
        report.duration_ms = int((time.time() - started) * 1000)
        text = self._extract_text(payload)
        report.raw_response = text
        parsed = extract_first_json_object(text)
        if not isinstance(parsed, dict):
            report.error = "gemini-video shot response was not a JSON object"
            return report
        try:
            report.passed = bool(parsed.get("passed", True))
            report.score = int(parsed.get("score", 0) or 0)
            report.issues = [str(x) for x in (parsed.get("issues") or [])]
            report.suggestions = [str(x) for x in (parsed.get("suggestions") or [])]
        except Exception as exc:
            report.error = f"gemini-video shot response coerce failed: {exc}"
            report.passed = True  # don't loop on parse errors
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
            critique.error = f"{ENV_KEY} not set"
            return critique

        if not Path(final_cut_path).exists() or Path(final_cut_path).stat().st_size == 0:
            critique.error = f"final cut missing or empty: {final_cut_path}"
            return critique

        prompt = _format_full_prompt(sketch_metadata)
        parts: List[Dict[str, Any]] = [{"text": prompt}]
        try:
            parts.append(self._video_part(final_cut_path))
        except Exception as exc:
            critique.error = f"could not read final cut bytes: {exc}"
            return critique

        started = time.time()
        try:
            payload = self._post(parts)
        except Exception as exc:
            critique.error = f"gemini-video request failed: {exc}"
            critique.duration_ms = int((time.time() - started) * 1000)
            return critique
        critique.duration_ms = int((time.time() - started) * 1000)
        text = self._extract_text(payload)
        critique.raw_response = text
        parsed = extract_first_json_object(text)
        if not isinstance(parsed, dict):
            critique.error = "gemini-video sketch response was not a JSON object"
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
            critique.error = f"gemini-video sketch response coerce failed: {exc}"
        return critique


__all__ = ["GeminiVideoCritic"]

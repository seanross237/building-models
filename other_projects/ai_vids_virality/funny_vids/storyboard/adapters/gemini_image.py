"""Gemini image adapter — calls `gemini-2.5-flash-image` (nano banana 2).

Uses `httpx` directly — no `google-generativeai` SDK dependency. On any
failure the adapter copies the Phase 1 placeholder PNG to `out_path` and
returns a dataclass with `error` set, so downstream stages always have a
valid file to work with.
"""
from __future__ import annotations

import base64
import logging
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from storyboard._common import copy_placeholder, slugify
from storyboard.adapter import CharacterRef, Frame, StoryboardAdapter


LOG = logging.getLogger("storyboard.adapters.gemini_image")
ENV_KEY = "GEMINI_API_KEY"
URL_TEMPLATE = (
    "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
)


def _build_character_prompt(character: Dict[str, Any], style_guide: str) -> str:
    name = character.get("name") or "unnamed character"
    description = character.get("description") or ""
    return "\n".join(
        [
            "Generate a character reference sheet image for a sketch-comedy short.",
            "Front view, centered, neutral expression, plain background.",
            f"Character name: {name}",
            f"Description: {description}",
            "",
            "Style guide:",
            style_guide.strip() or "(no style guide)",
            "",
            "Return only the image.",
        ]
    )


def _build_frame_prompt(
    beat: Dict[str, Any],
    style_guide: str,
    char_names: List[str],
) -> str:
    location = beat.get("location") or "interior"
    action = beat.get("action") or ""
    visual_note = beat.get("visual_note") or ""
    camera = beat.get("camera") or "medium"
    dialogue = beat.get("dialogue") or ""
    characters_line = ", ".join(char_names) if char_names else "(no characters)"
    pieces = [
        f"Beat {beat.get('n', 1)} — start frame.",
        f"Location: {location}",
        f"Camera: {camera} shot",
        f"Characters on screen: {characters_line}",
        f"Action: {action}",
    ]
    if dialogue:
        pieces.append(f"Dialogue snippet: {dialogue}")
    if visual_note:
        pieces.append(f"Visual note: {visual_note}")
    pieces.append("")
    pieces.append("Style guide:")
    pieces.append(style_guide.strip() or "(no style guide)")
    pieces.append("")
    pieces.append(
        "Use the provided reference images as authoritative anchors for character "
        "faces and outfits. Return only the generated image."
    )
    return "\n".join(pieces)


def _extract_image_bytes(payload: Dict[str, Any]) -> Optional[bytes]:
    """Walk a Gemini generateContent response and return the first image bytes."""
    candidates = payload.get("candidates") if isinstance(payload, dict) else None
    if not isinstance(candidates, list):
        return None
    for candidate in candidates:
        if not isinstance(candidate, dict):
            continue
        content = candidate.get("content")
        if not isinstance(content, dict):
            continue
        parts = content.get("parts")
        if not isinstance(parts, list):
            continue
        for part in parts:
            if not isinstance(part, dict):
                continue
            inline = part.get("inline_data") or part.get("inlineData")
            if not isinstance(inline, dict):
                continue
            data = inline.get("data")
            if not isinstance(data, str):
                continue
            try:
                return base64.b64decode(data)
            except Exception:
                continue
    return None


class GeminiImageAdapter(StoryboardAdapter):
    """Real nano-banana-2 caller via Google AI Studio REST."""

    adapter_id = "gemini-2.5-flash-image"

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self.model: str = str(self.config.get("model", "gemini-2.5-flash-image"))
        self.timeout_sec: int = int(self.config.get("timeout_sec", 60))

    def is_available(self) -> bool:
        return bool(os.environ.get(ENV_KEY))

    # ----------------------------------------------------------------- core HTTP

    def _post(self, parts: List[Dict[str, Any]]) -> Dict[str, Any]:
        try:
            import httpx
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError("httpx is required for the Gemini adapter") from exc

        body = {
            "contents": [{"role": "user", "parts": parts}],
            "generationConfig": {
                "responseModalities": ["IMAGE"],
            },
        }
        url = URL_TEMPLATE.format(model=self.model)
        response = httpx.post(
            url,
            params={"key": os.environ.get(ENV_KEY)},
            headers={"Content-Type": "application/json"},
            json=body,
            timeout=self.timeout_sec,
        )
        if response.status_code != 200:
            raise RuntimeError(
                f"gemini-image status {response.status_code}: {response.text[:300]}"
            )
        try:
            return response.json()
        except Exception as exc:
            raise RuntimeError(f"gemini-image json decode failed: {exc}")

    def _write_bytes(self, out_path: Path, raw: bytes) -> None:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("wb") as handle:
            handle.write(raw)

    # ----------------------------------------------------------------- public API

    def generate_character_ref(
        self,
        character: Dict[str, Any],
        style_guide: str,
        out_path: Path,
    ) -> CharacterRef:
        name = str(character.get("name") or "unnamed")
        ref = CharacterRef(
            name=name,
            slug=slugify(name),
            path=out_path,
            prompt="",
            adapter_id=self.adapter_id,
        )

        if not self.is_available():
            ref.error = "GEMINI_API_KEY not set"
            copy_placeholder(out_path)
            return ref

        prompt = _build_character_prompt(character, style_guide)
        ref.prompt = prompt
        started = time.time()
        try:
            payload = self._post([{"text": prompt}])
        except Exception as exc:
            ref.error = f"gemini-image request failed: {exc}"
            ref.duration_ms = int((time.time() - started) * 1000)
            copy_placeholder(out_path)
            return ref

        ref.duration_ms = int((time.time() - started) * 1000)
        raw = _extract_image_bytes(payload)
        if not raw:
            ref.error = "gemini-image response contained no image bytes"
            copy_placeholder(out_path)
            return ref

        try:
            self._write_bytes(out_path, raw)
        except Exception as exc:
            ref.error = f"gemini-image disk write failed: {exc}"
            copy_placeholder(out_path)
        return ref

    def generate_frame(
        self,
        beat: Dict[str, Any],
        character_refs: List[CharacterRef],
        style_guide: str,
        out_path: Path,
    ) -> Frame:
        beat_n = int(beat.get("n", 1) or 1)
        frame = Frame(
            beat_n=beat_n,
            path=out_path,
            prompt="",
            adapter_id=self.adapter_id,
        )

        if not self.is_available():
            frame.error = "GEMINI_API_KEY not set"
            copy_placeholder(out_path)
            return frame

        # Build the prompt mentioning the characters that appear in this beat.
        beat_characters = beat.get("characters") or []
        beat_names = [c.get("name") if isinstance(c, dict) else str(c) for c in beat_characters]
        beat_names = [n for n in beat_names if n]

        prompt = _build_frame_prompt(beat, style_guide, beat_names)
        frame.prompt = prompt

        parts: List[Dict[str, Any]] = [{"text": prompt}]

        # Include character ref images as inline_data parts so the model
        # conditions on them.
        for ref in character_refs:
            # Only include refs whose names are referenced in this beat.
            if beat_names and ref.name not in beat_names:
                continue
            try:
                raw_bytes = Path(ref.path).read_bytes()
                encoded = base64.b64encode(raw_bytes).decode("ascii")
            except Exception as exc:
                LOG.warning("could not load character ref %s: %s", ref.path, exc)
                continue
            parts.append(
                {
                    "inline_data": {
                        "mime_type": "image/png",
                        "data": encoded,
                    }
                }
            )

        started = time.time()
        try:
            payload = self._post(parts)
        except Exception as exc:
            frame.error = f"gemini-image request failed: {exc}"
            frame.duration_ms = int((time.time() - started) * 1000)
            copy_placeholder(out_path)
            return frame

        frame.duration_ms = int((time.time() - started) * 1000)
        raw = _extract_image_bytes(payload)
        if not raw:
            frame.error = "gemini-image response contained no image bytes"
            copy_placeholder(out_path)
            return frame

        try:
            self._write_bytes(out_path, raw)
        except Exception as exc:
            frame.error = f"gemini-image disk write failed: {exc}"
            copy_placeholder(out_path)
        return frame


__all__ = ["GeminiImageAdapter"]

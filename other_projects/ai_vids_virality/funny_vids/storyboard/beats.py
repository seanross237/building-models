"""Beat sheet generation via a Phase 3 ModelAdapter.

`generate_beats(sketch, model_adapter)` reuses the LLM abstraction we
built in Phase 3 to expand an approved premise into a 4–8 beat shot
list. Malformed responses fall back to a single-beat skeleton so the
downstream storyboard pipeline always has something to work with.
"""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from idea_factory.adapter import ModelAdapter
from idea_factory.adapters._json_parsing import extract_first_json_object
from state.store import Sketch


LOG = logging.getLogger("storyboard.beats")

PROMPT_PATH = Path(__file__).resolve().parent / "prompts" / "beat_sheet.md"


def _load_prompt_template() -> str:
    if PROMPT_PATH.exists():
        return PROMPT_PATH.read_text(encoding="utf-8")
    return ""


def _format_prompt(premise: Dict[str, Any], target_length_sec: int) -> str:
    template = _load_prompt_template()
    if not template:
        return (
            "Break this premise into 4-8 sketch beats as a JSON object "
            f"{{\"beats\": [...]}}: {json.dumps(premise)}"
        )
    characters = premise.get("characters") or []
    try:
        characters_json = json.dumps(characters)
    except Exception:
        characters_json = "[]"
    return template.format(
        premise_logline=str(premise.get("logline", "")),
        premise_synopsis=str(premise.get("synopsis", "")),
        premise_tone=str(premise.get("tone", "")),
        premise_twist=str(premise.get("twist", "")),
        premise_characters=characters_json,
        target_length_sec=target_length_sec,
    )


def _coerce_beat(raw: Any, index: int, characters: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not isinstance(raw, dict):
        return _fallback_beat(index, characters)
    try:
        n = int(raw.get("n", index) or index)
    except (TypeError, ValueError):
        n = index
    try:
        duration = int(raw.get("duration_sec", 5) or 5)
    except (TypeError, ValueError):
        duration = 5
    duration = max(1, min(12, duration))
    beat = {
        "n": n,
        "duration_sec": duration,
        "location": str(raw.get("location", "") or "").strip() or "interior",
        "characters": raw.get("characters") or characters,
        "action": str(raw.get("action", "") or "").strip() or f"beat {n} action",
        "dialogue": raw.get("dialogue") if raw.get("dialogue") is not None else None,
        "camera": str(raw.get("camera", "") or "").strip() or "medium",
        "visual_note": str(raw.get("visual_note", "") or "").strip(),
    }
    return beat


def _fallback_beat(index: int, characters: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "n": index,
        "duration_sec": 6,
        "location": "interior",
        "characters": characters,
        "action": "fallback beat — LLM response was empty or unparseable",
        "dialogue": None,
        "camera": "medium",
        "visual_note": "",
    }


def _extract_beats(raw_text: str) -> List[Dict[str, Any]]:
    payload = extract_first_json_object(raw_text or "")
    if not isinstance(payload, dict):
        return []
    beats = payload.get("beats")
    if isinstance(beats, list):
        return [b for b in beats if isinstance(b, dict)]
    # Some models emit the bare list.
    if isinstance(payload, list):
        return [b for b in payload if isinstance(b, dict)]
    return []


def generate_beats(
    sketch: Sketch,
    model_adapter: ModelAdapter,
    *,
    n_beats_max: int = 8,
    n_beats_min: int = 4,
) -> List[Dict[str, Any]]:
    """Expand the sketch's approved premise into a list of beat dicts.

    Uses the provided `model_adapter` to make a single LLM call with the
    beat-sheet prompt. On any failure path the function returns a small
    fallback beat list so the storyboard pipeline never gets stuck.
    """
    premise: Dict[str, Any] = sketch.premise or {}
    characters = premise.get("characters") or []
    target_length = int(premise.get("target_length_sec", 30) or 30)

    prompt = _format_prompt(premise, target_length)
    signal = {
        "signal_id": sketch.signal_id or sketch.id,
        "id": sketch.id,
        "title": premise.get("logline", ""),
        "summary": premise.get("synopsis", ""),
    }

    try:
        result = model_adapter.generate(signal, prompt, n_premises=1)
    except Exception as exc:
        LOG.warning("beat sheet LLM call raised: %s", exc)
        return [_fallback_beat(i + 1, characters) for i in range(max(n_beats_min, 1))]

    if getattr(result, "error", None):
        LOG.warning("beat sheet LLM returned error: %s", result.error)

    raw_text = getattr(result, "raw_response", "") or ""
    parsed = _extract_beats(raw_text)

    if not parsed:
        LOG.warning("beat sheet JSON was empty or unparseable; using fallback")
        return [_fallback_beat(1, characters)]

    # Clip to the allowed range and renumber contiguously.
    parsed = parsed[:n_beats_max]
    beats = [_coerce_beat(b, i + 1, characters) for i, b in enumerate(parsed)]
    for i, beat in enumerate(beats, start=1):
        beat["n"] = i
    return beats


__all__ = ["generate_beats"]

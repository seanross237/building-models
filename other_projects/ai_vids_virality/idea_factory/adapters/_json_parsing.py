"""Shared helpers for extracting an inner JSON object from an LLM response.

The prompt asks every model to emit strict JSON, but in practice models
sometimes wrap their output in ```json fences, prepend a sentence, or
emit a single JSON object that contains the `premises` array nested
inside another field. These helpers handle all three cases.
"""
from __future__ import annotations

import json
import re
from typing import Any, Dict, List, Optional


_FENCE_RE = re.compile(r"^```(?:json)?\s*\n?", re.IGNORECASE)


def strip_code_fences(text: str) -> str:
    """Remove leading/trailing ``` fences if present."""
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = _FENCE_RE.sub("", stripped, count=1)
        if stripped.endswith("```"):
            stripped = stripped[: -3].rstrip()
    return stripped


def extract_first_json_object(text: str) -> Optional[Dict[str, Any]]:
    """Find the first balanced `{...}` block in `text` and json.loads it."""
    cleaned = strip_code_fences(text)
    start = cleaned.find("{")
    if start == -1:
        return None
    depth = 0
    for i in range(start, len(cleaned)):
        ch = cleaned[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                blob = cleaned[start : i + 1]
                try:
                    parsed = json.loads(blob)
                    if isinstance(parsed, dict):
                        return parsed
                except json.JSONDecodeError:
                    return None
    return None


def find_premise_list(payload: Any) -> List[Dict[str, Any]]:
    """Walk a parsed JSON tree and return the first list of premise-shaped dicts.

    A premise-shaped dict is any dict that contains both `logline` and
    `synopsis` keys. This is more robust than insisting the model used the
    exact `{"premises": [...]}` envelope.
    """
    if isinstance(payload, dict):
        if "premises" in payload and isinstance(payload["premises"], list):
            return [p for p in payload["premises"] if isinstance(p, dict)]
        if "logline" in payload and "synopsis" in payload:
            return [payload]
        for value in payload.values():
            found = find_premise_list(value)
            if found:
                return found
    elif isinstance(payload, list):
        if all(isinstance(p, dict) and "logline" in p and "synopsis" in p for p in payload):
            return payload
        for item in payload:
            found = find_premise_list(item)
            if found:
                return found
    return []


__all__ = ["extract_first_json_object", "find_premise_list", "strip_code_fences"]

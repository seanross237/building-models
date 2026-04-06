"""Stub critic.

Returns a hardcoded scoring report and writes it onto the sketch.
Phase 6 will replace this with multimodal model calls.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict

from state.store import Sketch, Store


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run(store: Store, sketch_id: str) -> Dict[str, Any]:
    """Score the sketch and persist the report. Mutates the sketch."""
    sketch: Sketch = store.get_sketch(sketch_id)
    report: Dict[str, Any] = {
        "model": "stub-critic-v1",
        "scored_at": _now(),
        "scores": {
            "comedic_timing": 7,
            "pacing": 6,
            "punchline_landing": 7,
            "audio_clarity": 8,
            "is_actually_funny": 6,
        },
        "overall_score": 7,
        "verdict": "passes the stub bar",
        "fix_suggestions": [
            "tighten the second beat by half a second",
            "raise the music bed in the final shot",
        ],
    }
    sketch.critic_report = report
    store.save_sketch(sketch)
    return report

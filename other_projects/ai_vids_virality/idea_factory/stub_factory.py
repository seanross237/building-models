"""Stub idea factory.

Reads the idea-factory queue, and for each unconsumed signal creates a
new sketch with three hardcoded premises that vary based on the signal
title. The sketch lands in PREMISE_REVIEW with a marker in the
premise-review queue.

The seam (`run_factory(store)`) is what Phase 3's multi-model controller
will call instead of the stub.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from state.machine import Status
from state.store import Sketch, Store


MODEL_NAME = "stub-factory-v1"


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _make_sketch_id(signal_id: str) -> str:
    """Deterministic ID derived from the signal so the factory is idempotent."""
    digest = hashlib.sha1(signal_id.encode("utf-8")).hexdigest()[:6]
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return f"sk-{today}-{digest}"


def _generate_premises(signal_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    title = signal_payload.get("title", "an unnamed event")
    summary = signal_payload.get("summary", "")
    return [
        {
            "logline": f"A small office reckons with the news that {title.lower()}",
            "synopsis": (
                "Three coworkers at a totally unrelated company spend the day "
                "passive-aggressively litigating the implications. " + summary
            ),
            "tone": "dry workplace",
            "target_length_sec": 30,
            "characters": ["middle-manager", "intern", "the-guy-who-knew"],
            "twist": "the intern was right the whole time",
        },
        {
            "logline": f"A reporter tries to get a normal quote about: {title}",
            "synopsis": (
                "A local TV reporter pushes a microphone into the face of "
                "every passerby and gets increasingly unhinged answers."
            ),
            "tone": "mockumentary",
            "target_length_sec": 30,
            "characters": ["reporter", "passerby-1", "passerby-2", "passerby-3"],
            "twist": "the third passerby is the original subject in disguise",
        },
        {
            "logline": f"Two AI assistants debate whether {title.lower()} is real",
            "synopsis": (
                "Two voice assistants on the same desk argue the merits of the "
                "story until their owner unplugs them both."
            ),
            "tone": "absurdist",
            "target_length_sec": 30,
            "characters": ["assistant-A", "assistant-B", "owner"],
            "twist": "the owner is also an AI",
        },
    ]


def _signal_already_consumed(store: Store, signal_id: str) -> bool:
    for sketch in store.list_sketches():
        if sketch.signal_id == signal_id:
            return True
    return False


def run_factory(store: Store) -> List[str]:
    """Walk the idea-factory queue and create sketches in PREMISE_REVIEW.

    Returns the list of new sketch IDs created during this run.
    """
    new_sketch_ids: List[str] = []
    for marker_path in store.list_queue("idea-factory"):
        payload = store.read_queue_marker(marker_path)
        signal_id = payload.get("signal_id")
        if not signal_id or _signal_already_consumed(store, signal_id):
            continue

        sketch_id = _make_sketch_id(signal_id)
        if (store.sketch_json_path(sketch_id)).exists():
            continue

        premises = _generate_premises(payload)
        sketch = Sketch(
            id=sketch_id,
            status=Status.PREMISE_REVIEW,
            signal_id=signal_id,
            premise=premises[0],
            premises=premises,
        )
        sketch.history.append(
            {
                "from": Status.IDEA_PENDING.value,
                "to": Status.PREMISE_REVIEW.value,
                "at": _now(),
                "payload": {"model": MODEL_NAME, "premise_count": len(premises)},
            }
        )
        store.save_sketch(sketch)
        store.write_queue_marker(
            "premise-review",
            sketch_id,
            {
                "sketch_id": sketch_id,
                "signal_id": signal_id,
                "model": MODEL_NAME,
                "queued_at": _now(),
            },
        )
        new_sketch_ids.append(sketch_id)
    return new_sketch_ids

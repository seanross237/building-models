"""Stub storyboard generator.

For each beat in a sketch, copy the placeholder PNG into
`data/sketches/{sketch_id}/storyboard/beat-{n}-start.png` and append a
storyboard frame entry to the sketch.

Phase 4 will replace this with real nano-banana-2 calls. The seam is
`generate(store, sketch_id)`.
"""
from __future__ import annotations

import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from state.store import Sketch, Store


PLACEHOLDER_PATH = Path(__file__).resolve().parent / "placeholder.png"


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def ensure_placeholder() -> Path:
    """Make sure the placeholder PNG exists. Generate it with PIL if not."""
    if PLACEHOLDER_PATH.exists():
        return PLACEHOLDER_PATH
    try:
        from PIL import Image  # type: ignore
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError(
            "Pillow is required to generate the storyboard placeholder. "
            "Install it via requirements.txt."
        ) from exc
    PLACEHOLDER_PATH.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", (512, 512), "#444").save(PLACEHOLDER_PATH)
    return PLACEHOLDER_PATH


def generate(store: Store, sketch_id: str) -> List[Dict[str, Any]]:
    """Generate storyboard frames for every beat on the sketch.

    Returns the list of frame metadata appended. Mutates the sketch on disk.
    """
    placeholder = ensure_placeholder()
    sketch: Sketch = store.get_sketch(sketch_id)

    storyboard_dir = store.sketch_storyboard_dir(sketch_id)
    storyboard_dir.mkdir(parents=True, exist_ok=True)

    frames: List[Dict[str, Any]] = []
    beats = sketch.beats or []
    if not beats:
        beats = [
            {"n": 1, "duration_sec": 5, "action": "stub beat 1"},
            {"n": 2, "duration_sec": 5, "action": "stub beat 2"},
        ]
        sketch.beats = beats

    for beat in beats:
        n = beat.get("n", 1)
        out_path = storyboard_dir / f"beat-{n}-start.png"
        shutil.copyfile(placeholder, out_path)
        frame = {
            "beat_n": n,
            "kind": "start",
            "path": str(out_path),
            "model": "stub-storyboard-v1",
            "generated_at": _now(),
            "cost_cents": 0,
        }
        frames.append(frame)

    sketch.storyboard_frames = frames
    store.save_sketch(sketch)
    return frames

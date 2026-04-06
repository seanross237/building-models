"""Stub video provider.

For each storyboard frame, copies the placeholder MP4 into
`data/sketches/{sketch_id}/clips/beat-{n}.mp4` and then copies the first
clip to `final.mp4` as the stitched output.

If the placeholder MP4 doesn't exist, generates it via ffmpeg. If ffmpeg
isn't available either, falls back to writing a tiny static MP4 byte
sequence so tests still pass on machines without ffmpeg.
"""
from __future__ import annotations

import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from state.store import Sketch, Store


PLACEHOLDER_PATH = Path(__file__).resolve().parent / "placeholder.mp4"

# Smallest possible "valid-looking" MP4 byte sequence used as a fallback
# when ffmpeg is not available. This is not a real playable file but it
# satisfies the "file exists with non-zero bytes" assertion in tests.
FALLBACK_MP4_BYTES = (
    b"\x00\x00\x00\x18ftypisom\x00\x00\x02\x00isomiso2mp41"
    b"\x00\x00\x00\x08free"
    b"\x00\x00\x00\x08mdat"
)


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _have_ffmpeg() -> bool:
    return shutil.which("ffmpeg") is not None


def ensure_placeholder() -> Path:
    """Ensure the placeholder MP4 exists. Try ffmpeg, fall back to bytes."""
    if PLACEHOLDER_PATH.exists() and PLACEHOLDER_PATH.stat().st_size > 0:
        return PLACEHOLDER_PATH
    PLACEHOLDER_PATH.parent.mkdir(parents=True, exist_ok=True)
    if _have_ffmpeg():
        try:
            subprocess.run(
                [
                    "ffmpeg",
                    "-loglevel",
                    "error",
                    "-f",
                    "lavfi",
                    "-i",
                    "color=c=black:s=320x240:d=2",
                    "-y",
                    str(PLACEHOLDER_PATH),
                ],
                check=True,
            )
            return PLACEHOLDER_PATH
        except subprocess.CalledProcessError:
            pass
    PLACEHOLDER_PATH.write_bytes(FALLBACK_MP4_BYTES)
    return PLACEHOLDER_PATH


def generate(store: Store, sketch_id: str) -> Dict[str, Any]:
    """Render stub clips for every storyboard frame and stitch a final.mp4.

    Returns a dict with `clips` and `final_cut_path`. Mutates the sketch.
    """
    placeholder = ensure_placeholder()
    sketch: Sketch = store.get_sketch(sketch_id)

    clips_dir = store.sketch_clips_dir(sketch_id)
    clips_dir.mkdir(parents=True, exist_ok=True)

    clips: List[Dict[str, Any]] = []
    frames = sketch.storyboard_frames or [{"beat_n": 1}]
    for frame in frames:
        n = frame.get("beat_n", 1)
        out_path = clips_dir / f"beat-{n}.mp4"
        shutil.copyfile(placeholder, out_path)
        clips.append(
            {
                "beat_n": n,
                "path": str(out_path),
                "model": "stub-video-v1",
                "duration_sec": 2,
                "cost_cents": 0,
                "generated_at": _now(),
            }
        )

    final_path = store.sketch_final_path(sketch_id)
    final_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(placeholder, final_path)

    sketch.video_clips = clips
    sketch.final_cut_path = str(final_path)
    store.save_sketch(sketch)
    return {"clips": clips, "final_cut_path": str(final_path)}

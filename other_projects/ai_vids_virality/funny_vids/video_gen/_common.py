"""Shared helpers for the video_gen layer."""
from __future__ import annotations

import base64
import logging
import shutil
import subprocess
from pathlib import Path
from typing import Optional


LOG = logging.getLogger("video_gen._common")
PLACEHOLDER_PATH = Path(__file__).resolve().parent / "placeholder.mp4"

# Minimum-valid MP4 byte sequence used when ffmpeg is unavailable. Not
# a playable file but enough for tests that only check existence + size.
FALLBACK_MP4_BYTES = (
    b"\x00\x00\x00\x18ftypisom\x00\x00\x02\x00isomiso2mp41"
    b"\x00\x00\x00\x08free"
    b"\x00\x00\x00\x08mdat"
)


def ensure_placeholder() -> Path:
    """Ensure the placeholder MP4 exists on disk; create it via ffmpeg or fall back."""
    if PLACEHOLDER_PATH.exists() and PLACEHOLDER_PATH.stat().st_size > 0:
        return PLACEHOLDER_PATH
    PLACEHOLDER_PATH.parent.mkdir(parents=True, exist_ok=True)
    if shutil.which("ffmpeg"):
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


def copy_placeholder(out_path: Path) -> None:
    """Copy the placeholder MP4 into `out_path` (creating parent dirs)."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ensure_placeholder(), out_path)


def base64_file(path: Path) -> str:
    """Read a file and return its base64-encoded string (no prefix)."""
    return base64.b64encode(Path(path).read_bytes()).decode("ascii")


def write_bytes(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as handle:
        handle.write(raw)


__all__ = [
    "FALLBACK_MP4_BYTES",
    "PLACEHOLDER_PATH",
    "base64_file",
    "copy_placeholder",
    "ensure_placeholder",
    "write_bytes",
]

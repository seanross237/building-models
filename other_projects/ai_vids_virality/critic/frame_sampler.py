"""ffmpeg-based frame sampler.

`sample_frames(clip_path, n, out_dir)` extracts `n` evenly-spaced frames
from a clip and writes them as PNGs to `out_dir`. Returns the list of
output paths.

The Claude critic adapter uses this to send a small set of frames to
the LLM as image inputs. We don't need every frame — 4 evenly-spaced
samples per clip is enough to spot continuity issues, character
morphing, and obvious artifacts.

If `ffmpeg` isn't on PATH the function returns an empty list and logs
a warning, so the calling adapter can fall back gracefully.

Audio extraction (`extract_audio_wav`) is provided as a sibling helper
for the optional Whisper transcription path. Whisper is NOT a project
dependency — the helper returns None if Whisper or ffmpeg is missing.
"""
from __future__ import annotations

import logging
import shutil
import subprocess
from pathlib import Path
from typing import List, Optional


LOG = logging.getLogger("critic.frame_sampler")


def have_ffmpeg() -> bool:
    return shutil.which("ffmpeg") is not None


def have_ffprobe() -> bool:
    return shutil.which("ffprobe") is not None


def probe_duration_sec(path: Path) -> Optional[float]:
    if not have_ffprobe():
        return None
    cmd = [
        "ffprobe",
        "-loglevel",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        return None
    raw = (result.stdout or "").strip()
    try:
        return float(raw)
    except (TypeError, ValueError):
        return None


def sample_frames(clip_path: Path, n: int, out_dir: Path) -> List[Path]:
    """Sample `n` evenly-spaced frames from a clip and write them as PNGs."""
    if n <= 0:
        return []
    if not Path(clip_path).exists() or Path(clip_path).stat().st_size == 0:
        LOG.warning("frame sampler: clip %s missing or empty", clip_path)
        return []
    if not have_ffmpeg():
        LOG.warning("frame sampler: ffmpeg not on PATH; returning no frames")
        return []

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    duration = probe_duration_sec(Path(clip_path))
    if duration is None or duration <= 0:
        # Fall back to a single keyframe extraction.
        out_path = out_dir / "frame_01.png"
        cmd = [
            "ffmpeg",
            "-loglevel",
            "error",
            "-i",
            str(clip_path),
            "-frames:v",
            "1",
            "-y",
            str(out_path),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if result.returncode == 0 and out_path.exists() and out_path.stat().st_size > 0:
            return [out_path]
        return []

    out_paths: List[Path] = []
    for i in range(n):
        # Pick a timestamp at the midpoint of each evenly-divided slice.
        t = ((i + 0.5) / n) * duration
        out_path = out_dir / f"frame_{i + 1:02d}.png"
        cmd = [
            "ffmpeg",
            "-loglevel",
            "error",
            "-ss",
            f"{t:.3f}",
            "-i",
            str(clip_path),
            "-frames:v",
            "1",
            "-y",
            str(out_path),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if result.returncode == 0 and out_path.exists() and out_path.stat().st_size > 0:
            out_paths.append(out_path)
    return out_paths


def extract_audio_wav(clip_path: Path, out_path: Path) -> Optional[Path]:
    """Pull a 16kHz mono WAV from a clip via ffmpeg. Returns None on failure."""
    if not Path(clip_path).exists() or not have_ffmpeg():
        return None
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg",
        "-loglevel",
        "error",
        "-i",
        str(clip_path),
        "-vn",
        "-ac",
        "1",
        "-ar",
        "16000",
        "-y",
        str(out_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode == 0 and out_path.exists() and out_path.stat().st_size > 0:
        return out_path
    return None


def transcribe_with_whisper(audio_path: Path) -> Optional[str]:
    """Transcribe a WAV with whisper-the-python-package if it's installed.

    Whisper is NOT a project dependency. This function attempts the
    import lazily and returns None on any failure — the caller should
    treat the absence of a transcript as "no audio info available".
    """
    try:
        import whisper  # type: ignore
    except ImportError:
        LOG.info("whisper not installed; skipping transcription")
        return None
    try:
        model = whisper.load_model("base")
        result = model.transcribe(str(audio_path))
    except Exception as exc:  # pragma: no cover
        LOG.warning("whisper transcription failed: %s", exc)
        return None
    return str(result.get("text", "")).strip() or None


__all__ = [
    "extract_audio_wav",
    "have_ffmpeg",
    "have_ffprobe",
    "probe_duration_sec",
    "sample_frames",
    "transcribe_with_whisper",
]

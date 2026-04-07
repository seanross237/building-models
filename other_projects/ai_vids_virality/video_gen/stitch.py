"""ffmpeg-based clip stitching.

`stitch_clips(clips, out_path)` concatenates a list of video files into a
single MP4 using ffmpeg's concat demuxer with stream-copy mode. If the
input clips have mismatched codecs (which makes concat-copy fail with
"Unsafe file name" or "non-monotonic DTS"), it falls back to a full
re-encode (`-c:v libx264 -c:a aac`).

If `ffmpeg` is not on PATH, falls back to copying the first clip to
`out_path` so the rest of the pipeline always has a final.mp4 to point
at.
"""
from __future__ import annotations

import logging
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import List, Optional


LOG = logging.getLogger("video_gen.stitch")


class StitchError(RuntimeError):
    pass


def _have_ffmpeg() -> bool:
    return shutil.which("ffmpeg") is not None


def _write_concat_list(clips: List[Path], list_path: Path) -> None:
    lines = []
    for clip in clips:
        # Escape single quotes per ffmpeg concat-demuxer rules.
        escaped = str(Path(clip).resolve()).replace("'", "'\\''")
        lines.append(f"file '{escaped}'")
    list_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _try_concat_copy(clips: List[Path], out_path: Path) -> bool:
    """Attempt the cheap stream-copy concat. Returns True on success."""
    with tempfile.TemporaryDirectory() as tmpdir:
        list_path = Path(tmpdir) / "concat.txt"
        _write_concat_list(clips, list_path)
        cmd = [
            "ffmpeg",
            "-loglevel",
            "error",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(list_path),
            "-c",
            "copy",
            "-y",
            str(out_path),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if result.returncode == 0 and out_path.exists() and out_path.stat().st_size > 0:
            return True
        LOG.warning(
            "concat-copy failed (rc=%s): %s",
            result.returncode,
            (result.stderr or "").strip()[:300],
        )
        return False


def _try_concat_reencode(clips: List[Path], out_path: Path) -> bool:
    """Fall-back: re-encode every input to a common codec via concat demuxer."""
    with tempfile.TemporaryDirectory() as tmpdir:
        list_path = Path(tmpdir) / "concat.txt"
        _write_concat_list(clips, list_path)
        cmd = [
            "ffmpeg",
            "-loglevel",
            "error",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(list_path),
            "-c:v",
            "libx264",
            "-preset",
            "ultrafast",
            "-c:a",
            "aac",
            "-y",
            str(out_path),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if result.returncode == 0 and out_path.exists() and out_path.stat().st_size > 0:
            return True
        LOG.warning(
            "concat-reencode failed (rc=%s): %s",
            result.returncode,
            (result.stderr or "").strip()[:300],
        )
        return False


def stitch_clips(clips: List[Path], out_path: Path) -> Path:
    """Concatenate `clips` into `out_path`. Returns `out_path` on success."""
    valid_clips = [Path(c) for c in clips if Path(c).exists() and Path(c).stat().st_size > 0]
    if not valid_clips:
        raise StitchError("no valid input clips to stitch")

    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Single-clip case: nothing to concat, just copy.
    if len(valid_clips) == 1:
        shutil.copyfile(valid_clips[0], out_path)
        return out_path

    if not _have_ffmpeg():
        LOG.warning("ffmpeg not on PATH; falling back to copying the first clip")
        shutil.copyfile(valid_clips[0], out_path)
        return out_path

    if _try_concat_copy(valid_clips, out_path):
        return out_path
    if _try_concat_reencode(valid_clips, out_path):
        return out_path

    # Both modes failed — last-resort copy of the first clip so we have a file.
    LOG.warning("both ffmpeg concat modes failed; copying the first clip as final.mp4")
    shutil.copyfile(valid_clips[0], out_path)
    return out_path


def probe_duration_sec(path: Path) -> Optional[float]:
    """Return the duration of `path` in seconds via ffprobe, or None on failure."""
    if not shutil.which("ffprobe"):
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


__all__ = ["StitchError", "probe_duration_sec", "stitch_clips"]

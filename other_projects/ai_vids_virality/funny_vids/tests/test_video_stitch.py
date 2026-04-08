"""Tests for the ffmpeg stitching helper."""
from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from video_gen.stitch import StitchError, probe_duration_sec, stitch_clips


FIXTURES = Path(__file__).resolve().parent / "fixtures" / "sample_clips"


def _ffmpeg_available() -> bool:
    return shutil.which("ffmpeg") is not None


@pytest.fixture()
def sample_clip_paths() -> list:
    files = sorted(FIXTURES.glob("clip-*.mp4"))
    assert len(files) == 3, "expected 3 fixture clips in tests/fixtures/sample_clips"
    return files


def test_stitch_three_fixture_clips_into_one(
    tmp_path: Path,
    sample_clip_paths: list,
) -> None:
    out = tmp_path / "joined.mp4"
    result = stitch_clips(sample_clip_paths, out)
    assert result == out
    assert out.exists()
    assert out.stat().st_size > 0
    if shutil.which("ffprobe"):
        duration = probe_duration_sec(out)
        # Each fixture clip is 1 second; allow generous tolerance for muxing.
        assert duration is not None
        assert 2.5 < duration < 4.0


def test_stitch_single_clip_just_copies(
    tmp_path: Path,
    sample_clip_paths: list,
) -> None:
    out = tmp_path / "single.mp4"
    result = stitch_clips([sample_clip_paths[0]], out)
    assert result == out
    assert out.exists()
    assert out.stat().st_size == sample_clip_paths[0].stat().st_size


def test_stitch_empty_list_raises(tmp_path: Path) -> None:
    with pytest.raises(StitchError):
        stitch_clips([], tmp_path / "x.mp4")


def test_stitch_skips_zero_byte_inputs(tmp_path: Path, sample_clip_paths: list) -> None:
    bad = tmp_path / "empty.mp4"
    bad.touch()
    out = tmp_path / "joined.mp4"
    result = stitch_clips([bad, sample_clip_paths[0], sample_clip_paths[1]], out)
    assert result == out
    assert out.exists()


def test_stitch_falls_back_when_ffmpeg_missing(
    tmp_path: Path,
    sample_clip_paths: list,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """When ffmpeg isn't on PATH the stitcher copies the first clip."""
    monkeypatch.setattr("video_gen.stitch.shutil.which", lambda name: None)
    out = tmp_path / "fallback.mp4"
    result = stitch_clips(sample_clip_paths, out)
    assert result == out
    assert out.exists()
    # Should match the first clip's bytes (copy fallback).
    assert out.stat().st_size == sample_clip_paths[0].stat().st_size


def test_stitch_concat_copy_failure_falls_back_to_reencode(
    tmp_path: Path,
    sample_clip_paths: list,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """If concat-copy fails, the stitcher should call concat-reencode."""
    calls = []

    def fake_copy(clips, out_path):
        calls.append("copy")
        return False

    def fake_reencode(clips, out_path):
        calls.append("reencode")
        # Pretend we wrote a file.
        out_path.write_bytes(b"fake-mp4")
        return True

    monkeypatch.setattr("video_gen.stitch._try_concat_copy", fake_copy)
    monkeypatch.setattr("video_gen.stitch._try_concat_reencode", fake_reencode)

    out = tmp_path / "out.mp4"
    stitch_clips(sample_clip_paths, out)
    assert calls == ["copy", "reencode"]
    assert out.exists()

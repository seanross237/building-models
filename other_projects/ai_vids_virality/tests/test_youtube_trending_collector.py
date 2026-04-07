"""YouTube trending collector unit tests using a mocked subprocess runner."""
from __future__ import annotations

from pathlib import Path
from typing import Any, List
from types import SimpleNamespace

import pytest

from collectors.youtube_trending import fetch as yt_trending
from state.store import Store


FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _make_runner(stdout: str, returncode: int = 0):
    captured: List[List[str]] = []

    def runner(cmd: List[str], **kwargs: Any) -> Any:
        captured.append(cmd)
        return SimpleNamespace(stdout=stdout, stderr="", returncode=returncode)

    runner.calls = captured  # type: ignore[attr-defined]
    return runner


@pytest.fixture()
def sample_stdout() -> str:
    return (FIXTURES / "yt_dlp_sample.json").read_text(encoding="utf-8")


@pytest.fixture()
def force_yt_dlp_present(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(yt_trending, "_yt_dlp_path", lambda: "/fake/yt-dlp")


def test_first_run_creates_signals(
    tmp_path: Path,
    sample_stdout: str,
    force_yt_dlp_present: None,
) -> None:
    store = Store(root=tmp_path)
    runner = _make_runner(sample_stdout)
    new_ids = yt_trending.fetch(store, config={"limit": 5}, runner=runner)
    assert len(new_ids) == 3
    assert all(sid.startswith("yt-") for sid in new_ids)

    items_dir = tmp_path / "signals" / "youtube_trending" / "items"
    files = sorted(items_dir.glob("*.md"))
    assert len(files) == 3
    text = files[0].read_text(encoding="utf-8")
    assert "source: youtube_trending" in text


def test_dedupe(
    tmp_path: Path,
    sample_stdout: str,
    force_yt_dlp_present: None,
) -> None:
    store = Store(root=tmp_path)
    runner = _make_runner(sample_stdout)
    first = yt_trending.fetch(store, config={"limit": 5}, runner=runner)
    second = yt_trending.fetch(store, config={"limit": 5}, runner=runner)
    assert len(first) == 3
    assert second == []


def test_yt_dlp_missing_returns_zero(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(yt_trending, "_yt_dlp_path", lambda: None)
    store = Store(root=tmp_path)
    new_ids = yt_trending.fetch(store, config={"limit": 5})
    assert new_ids == []


def test_yt_dlp_failure_returns_zero(
    tmp_path: Path,
    sample_stdout: str,
    force_yt_dlp_present: None,
) -> None:
    store = Store(root=tmp_path)
    runner = _make_runner("", returncode=2)
    new_ids = yt_trending.fetch(store, config={"limit": 5}, runner=runner)
    assert new_ids == []


def test_unparseable_lines_skipped(
    tmp_path: Path,
    force_yt_dlp_present: None,
) -> None:
    bad = '{"id":"goodvid","title":"good"}\nnot json line\n{"id":"goodvid2","title":"also good"}\n'
    store = Store(root=tmp_path)
    runner = _make_runner(bad)
    new_ids = yt_trending.fetch(store, config={"limit": 5}, runner=runner)
    assert len(new_ids) == 2

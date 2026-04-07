"""Google News RSS collector unit tests using a fixture XML and feedparser."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pytest
import feedparser

from collectors.google_news import fetch as google_news
from state.store import Store


FIXTURES = Path(__file__).resolve().parent / "fixtures"


class FakeFeedparser:
    """Pretends to be the `feedparser` module by parsing a local file."""

    def __init__(self, sample_xml: str) -> None:
        self.sample_xml = sample_xml
        self.calls: list = []

    def parse(self, url: str) -> Any:
        self.calls.append(url)
        return feedparser.parse(self.sample_xml)


@pytest.fixture()
def sample_xml() -> str:
    return (FIXTURES / "google_news_sample.xml").read_text(encoding="utf-8")


@pytest.fixture()
def freeze_now(monkeypatch: pytest.MonkeyPatch) -> None:
    fixed = datetime(2026, 4, 6, 12, 0, 0, tzinfo=timezone.utc)

    class _FixedDateTime(datetime):
        @classmethod
        def now(cls, tz=None):  # type: ignore[override]
            return fixed if tz is None else fixed.astimezone(tz)

    import collectors._common as common
    monkeypatch.setattr(common, "datetime", _FixedDateTime)


def test_first_run_creates_signals(
    tmp_path: Path,
    sample_xml: str,
    freeze_now: None,
) -> None:
    store = Store(root=tmp_path)
    rss = FakeFeedparser(sample_xml)
    new_ids = google_news.fetch(
        store,
        config={"feeds": ["http://fake/feed"], "limit_per_feed": 50, "max_age_hours": 100000},
        parser=rss,
    )
    assert len(new_ids) == 3
    assert all(sid.startswith("gn-") for sid in new_ids)

    items_dir = tmp_path / "signals" / "google_news" / "items"
    files = sorted(items_dir.glob("*.md"))
    assert len(files) == 3
    text = files[0].read_text(encoding="utf-8")
    assert "source: google_news" in text


def test_dedupe(tmp_path: Path, sample_xml: str, freeze_now: None) -> None:
    store = Store(root=tmp_path)
    rss = FakeFeedparser(sample_xml)
    first = google_news.fetch(
        store,
        config={"feeds": ["http://fake/feed"], "max_age_hours": 100000},
        parser=rss,
    )
    second = google_news.fetch(
        store,
        config={"feeds": ["http://fake/feed"], "max_age_hours": 100000},
        parser=rss,
    )
    assert len(first) == 3
    assert second == []


def test_max_age_filter(tmp_path: Path, sample_xml: str) -> None:
    store = Store(root=tmp_path)
    rss = FakeFeedparser(sample_xml)
    new_ids = google_news.fetch(
        store,
        config={"feeds": ["http://fake/feed"], "max_age_hours": 0.001},
        parser=rss,
    )
    assert new_ids == []


def test_limit_per_feed(tmp_path: Path, sample_xml: str, freeze_now: None) -> None:
    store = Store(root=tmp_path)
    rss = FakeFeedparser(sample_xml)
    new_ids = google_news.fetch(
        store,
        config={"feeds": ["http://fake/feed"], "limit_per_feed": 1, "max_age_hours": 100000},
        parser=rss,
    )
    assert len(new_ids) == 1

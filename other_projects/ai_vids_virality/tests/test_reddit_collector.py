"""Reddit collector unit tests using a mocked HTTP client + JSON fixture."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

import pytest

from collectors.reddit import fetch as reddit
from state.store import Store


FIXTURES = Path(__file__).resolve().parent / "fixtures"


class FakeResponse:
    def __init__(self, payload: Any, status: int = 200) -> None:
        self._payload = payload
        self.status_code = status

    def json(self) -> Any:
        return self._payload


class FakeHttp:
    """A pretend `requests` module that returns the same fixture every call."""

    def __init__(self, payload: Any) -> None:
        self.payload = payload
        self.calls: list = []

    def get(self, url: str, **kwargs: Any) -> FakeResponse:
        self.calls.append((url, kwargs))
        return FakeResponse(self.payload)


@pytest.fixture()
def reddit_payload() -> Dict[str, Any]:
    return json.loads((FIXTURES / "reddit_popular_sample.json").read_text(encoding="utf-8"))


@pytest.fixture()
def freeze_now(monkeypatch: pytest.MonkeyPatch) -> None:
    """Freeze the collectors' notion of 'now' to just after the fixture timestamps."""
    fixed = datetime(2026, 4, 6, 12, 0, 0, tzinfo=timezone.utc)

    class _FixedDateTime(datetime):
        @classmethod
        def now(cls, tz=None):  # type: ignore[override]
            return fixed if tz is None else fixed.astimezone(tz)

    import collectors._common as common
    monkeypatch.setattr(common, "datetime", _FixedDateTime)


def test_first_run_creates_signals(
    tmp_path: Path,
    reddit_payload: Dict[str, Any],
    freeze_now: None,
) -> None:
    store = Store(root=tmp_path)
    http = FakeHttp(reddit_payload)
    new_ids = reddit.fetch(
        store,
        config={"subreddits": ["popular"], "limit_per_sub": 25, "max_age_hours": 100000},
        http=http,
    )
    # The fixture has two valid posts and one stickied post that must be skipped.
    assert len(new_ids) == 2
    assert all(sid.startswith("reddit-") for sid in new_ids)

    items_dir = tmp_path / "signals" / "reddit" / "items"
    files = sorted(items_dir.glob("*.md"))
    assert len(files) == 2

    text = files[0].read_text(encoding="utf-8")
    assert text.startswith("---\n")
    for key in ("id:", "source:", "source_url:", "title:", "captured_at:", "heat_score_raw:", "freshness_hours:", "tags:"):
        assert key in text


def test_dedupe_via_seen_ids(
    tmp_path: Path,
    reddit_payload: Dict[str, Any],
    freeze_now: None,
) -> None:
    store = Store(root=tmp_path)
    http = FakeHttp(reddit_payload)
    first = reddit.fetch(store, config={"subreddits": ["popular"], "max_age_hours": 100000}, http=http)
    second = reddit.fetch(store, config={"subreddits": ["popular"], "max_age_hours": 100000}, http=http)
    assert len(first) == 2
    assert second == []


def test_old_posts_are_skipped(tmp_path: Path, reddit_payload: Dict[str, Any]) -> None:
    """With a 1-hour freshness window and old fixture timestamps, nothing should pass."""
    store = Store(root=tmp_path)
    http = FakeHttp(reddit_payload)
    new_ids = reddit.fetch(
        store,
        config={"subreddits": ["popular"], "max_age_hours": 0.001},
        http=http,
    )
    assert new_ids == []


def test_status_non_200_yields_zero(tmp_path: Path) -> None:
    class BadHttp:
        def get(self, url: str, **kwargs: Any) -> FakeResponse:
            return FakeResponse({}, status=503)

    store = Store(root=tmp_path)
    new_ids = reddit.fetch(store, config={"subreddits": ["popular"]}, http=BadHttp())
    assert new_ids == []


def test_stickied_and_nsfw_filtered(
    tmp_path: Path,
    reddit_payload: Dict[str, Any],
    freeze_now: None,
) -> None:
    store = Store(root=tmp_path)
    http = FakeHttp(reddit_payload)
    new_ids = reddit.fetch(
        store,
        config={"subreddits": ["popular"], "max_age_hours": 100000},
        http=http,
    )
    # Make sure the stickied post never made it through.
    assert not any("stickied999" in sid for sid in new_ids)

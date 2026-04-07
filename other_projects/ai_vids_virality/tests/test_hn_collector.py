"""Hacker News collector unit tests using a mocked Firebase HTTP layer."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

import pytest

from collectors.hacker_news import fetch as hn
from state.store import Store


FIXTURES = Path(__file__).resolve().parent / "fixtures"


class FakeResponse:
    def __init__(self, payload: Any, status: int = 200) -> None:
        self._payload = payload
        self.status_code = status

    def json(self) -> Any:
        return self._payload


class FakeHttp:
    """Pretends to be `requests` for HN's two endpoints."""

    def __init__(self, fixture: Dict[str, Any]) -> None:
        self.fixture = fixture
        self.calls: list = []

    def get(self, url: str, **kwargs: Any) -> FakeResponse:
        self.calls.append(url)
        if url.endswith("/topstories.json"):
            return FakeResponse(self.fixture["topstories"])
        for key, value in self.fixture["items"].items():
            if f"/item/{key}.json" in url:
                return FakeResponse(value)
        return FakeResponse(None, status=404)


@pytest.fixture()
def hn_payload() -> Dict[str, Any]:
    return json.loads((FIXTURES / "hn_topstories_sample.json").read_text(encoding="utf-8"))


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
    hn_payload: Dict[str, Any],
    freeze_now: None,
) -> None:
    store = Store(root=tmp_path)
    http = FakeHttp(hn_payload)
    new_ids = hn.fetch(store, config={"limit": 5, "max_age_hours": 100000}, http=http)
    # The fixture has two valid stories and one deleted item that must be skipped.
    assert len(new_ids) == 2
    assert all(sid.startswith("hn-") for sid in new_ids)

    items_dir = tmp_path / "signals" / "hacker_news" / "items"
    files = sorted(items_dir.glob("*.md"))
    assert len(files) == 2

    text = files[0].read_text(encoding="utf-8")
    for key in ("id:", "source: hacker_news", "source_url:", "title:", "heat_score_raw:"):
        assert key in text


def test_dedupe_second_run(
    tmp_path: Path,
    hn_payload: Dict[str, Any],
    freeze_now: None,
) -> None:
    store = Store(root=tmp_path)
    http = FakeHttp(hn_payload)
    first = hn.fetch(store, config={"limit": 5, "max_age_hours": 100000}, http=http)
    second = hn.fetch(store, config={"limit": 5, "max_age_hours": 100000}, http=http)
    assert len(first) == 2
    assert second == []


def test_max_age_filter(tmp_path: Path, hn_payload: Dict[str, Any]) -> None:
    store = Store(root=tmp_path)
    http = FakeHttp(hn_payload)
    new_ids = hn.fetch(store, config={"limit": 5, "max_age_hours": 0.001}, http=http)
    assert new_ids == []


def test_topstories_failure_returns_zero(tmp_path: Path) -> None:
    class BadHttp:
        def get(self, url: str, **kwargs: Any) -> FakeResponse:
            return FakeResponse(None, status=500)

    store = Store(root=tmp_path)
    assert hn.fetch(store, config={"limit": 5}, http=BadHttp()) == []

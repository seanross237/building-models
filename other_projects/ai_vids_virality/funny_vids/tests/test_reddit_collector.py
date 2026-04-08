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


class OAuthFakeHttp(FakeHttp):
    def __init__(
        self,
        payload: Any,
        token_payload: Any | None = None,
        token_status: int = 200,
        post_exc: Exception | None = None,
    ) -> None:
        super().__init__(payload)
        self.token_payload = token_payload or {}
        self.token_status = token_status
        self.post_exc = post_exc
        self.get_calls: list = []
        self.post_calls: list = []

    def get(self, url: str, **kwargs: Any) -> FakeResponse:
        self.get_calls.append((url, kwargs))
        return super().get(url, **kwargs)

    def post(self, url: str, **kwargs: Any) -> FakeResponse:
        self.post_calls.append((url, kwargs))
        if self.post_exc is not None:
            raise self.post_exc
        return FakeResponse(self.token_payload, status=self.token_status)


@pytest.fixture()
def reddit_payload() -> Dict[str, Any]:
    return json.loads((FIXTURES / "reddit_popular_sample.json").read_text(encoding="utf-8"))


@pytest.fixture(autouse=True)
def reset_reddit_oauth(monkeypatch: pytest.MonkeyPatch) -> None:
    reddit._TOKEN_CACHE = {"token": None, "expires_at": 0.0}
    for env_name in (reddit.REDDIT_CLIENT_ID, reddit.REDDIT_CLIENT_SECRET, reddit.REDDIT_USER_AGENT):
        monkeypatch.delenv(env_name, raising=False)


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


def test_oauth_path_uses_bearer_token(
    tmp_path: Path,
    reddit_payload: Dict[str, Any],
    freeze_now: None,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("REDDIT_CLIENT_ID", "fake_id")
    monkeypatch.setenv("REDDIT_CLIENT_SECRET", "fake_secret")
    http = OAuthFakeHttp(
        reddit_payload,
        token_payload={"access_token": "fake_bearer_xyz", "expires_in": 3600},
    )

    new_ids = reddit.fetch(
        store=Store(root=tmp_path),
        config={"subreddits": ["popular"], "limit_per_sub": 25, "max_age_hours": 100000},
        http=http,
    )

    assert len(new_ids) == 2
    assert len(http.post_calls) == 1
    token_url, token_kwargs = http.post_calls[0]
    assert token_url == reddit.OAUTH_TOKEN_URL
    assert token_kwargs["auth"] == ("fake_id", "fake_secret")
    assert token_kwargs["data"] == {"grant_type": "client_credentials"}
    assert all(url.startswith(f"{reddit.OAUTH_API_BASE}/r/") for url, _ in http.get_calls)
    assert all("www.reddit.com" not in url for url, _ in http.get_calls)
    assert all(
        kwargs["headers"]["Authorization"] == "Bearer fake_bearer_xyz" for _, kwargs in http.get_calls
    )


def test_oauth_token_cached_across_subreddits(
    tmp_path: Path,
    reddit_payload: Dict[str, Any],
    freeze_now: None,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("REDDIT_CLIENT_ID", "fake_id")
    monkeypatch.setenv("REDDIT_CLIENT_SECRET", "fake_secret")
    http = OAuthFakeHttp(
        reddit_payload,
        token_payload={"access_token": "fake_bearer_xyz", "expires_in": 3600},
    )

    reddit.fetch(
        store=Store(root=tmp_path),
        config={"subreddits": ["popular", "news"], "limit_per_sub": 25, "max_age_hours": 100000},
        http=http,
    )

    assert len(http.post_calls) == 1
    assert len(http.get_calls) == 2


def test_oauth_non_200_falls_back_to_anonymous(
    tmp_path: Path,
    reddit_payload: Dict[str, Any],
    freeze_now: None,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("REDDIT_CLIENT_ID", "fake_id")
    monkeypatch.setenv("REDDIT_CLIENT_SECRET", "fake_secret")
    http = OAuthFakeHttp(reddit_payload, token_payload={"error": "unauthorized"}, token_status=401)

    new_ids = reddit.fetch(
        store=Store(root=tmp_path),
        config={"subreddits": ["popular"], "limit_per_sub": 25, "max_age_hours": 100000},
        http=http,
    )

    assert len(new_ids) == 2
    assert len(http.post_calls) == 1
    assert len(http.get_calls) == 1
    get_url, get_kwargs = http.get_calls[0]
    assert get_url == "https://www.reddit.com/r/popular.json?limit=25"
    assert "Authorization" not in get_kwargs["headers"]


def test_oauth_exception_falls_back_to_anonymous(
    tmp_path: Path,
    reddit_payload: Dict[str, Any],
    freeze_now: None,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("REDDIT_CLIENT_ID", "fake_id")
    monkeypatch.setenv("REDDIT_CLIENT_SECRET", "fake_secret")
    http = OAuthFakeHttp(reddit_payload, post_exc=RuntimeError("boom"))

    new_ids = reddit.fetch(
        store=Store(root=tmp_path),
        config={"subreddits": ["popular"], "limit_per_sub": 25, "max_age_hours": 100000},
        http=http,
    )

    assert len(new_ids) == 2
    assert len(http.post_calls) == 1
    assert len(http.get_calls) == 1
    get_url, get_kwargs = http.get_calls[0]
    assert get_url == "https://www.reddit.com/r/popular.json?limit=25"
    assert "Authorization" not in get_kwargs["headers"]

"""Tests for the Phase 7 Publisher implementations."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Dict, List, Optional

import pytest

from publishing.adapter import Publisher, PublishResult
from publishing.adapters.local_archive import LocalArchivePublisher
from publishing.adapters.stub_publisher import StubPublisher
from publishing.adapters.youtube_shorts import YouTubeShortsPublisher
from publishing.pipeline import (
    load_publishers,
    load_publishing_config,
    run_publishers,
)
from state.machine import Status
from state.store import Sketch, Store


# ----------------------------------------------------------------- fixtures


def _seed_finished_sketch(store: Store, sketch_id: str = "sk-test-publish-001") -> Sketch:
    sketch = Sketch(
        id=sketch_id,
        status=Status.PREMISE_REVIEW,
        signal_id="test-sig",
        premise={
            "logline": "A communications intern is tasked with logging posture every 15 minutes",
            "synopsis": "Dry office beat. Intern gets a clipboard.",
            "tone": "dry workplace",
            "target_length_sec": 30,
            "characters": [],
            "twist": "the boss freezes mid-sentence",
        },
        beats=[{"n": 1, "duration_sec": 5}],
    )
    store.save_sketch(sketch)
    # Walk the sketch through the state machine to CRITIC_REVIEW so publish
    # can run from a valid source state.
    store.transition(sketch_id, Status.SCRIPTED, {})
    store.transition(sketch_id, Status.STORYBOARD_REVIEW, {})
    store.transition(sketch_id, Status.VIDEO_PENDING, {})
    store.transition(sketch_id, Status.CRITIC_REVIEW, {})
    # Drop a final.mp4 + sketch.json + critic.json on disk so the archive
    # publisher has something to copy.
    final_path = store.sketch_final_path(sketch_id)
    final_path.parent.mkdir(parents=True, exist_ok=True)
    final_path.write_bytes(b"FAKE_MP4_BYTES")
    (store.sketch_dir(sketch_id) / "critic.json").write_text(
        json.dumps({"sketch_id": sketch_id, "overall_score": 7}) + "\n",
        encoding="utf-8",
    )
    return store.get_sketch(sketch_id)


# ----------------------------------------------------------------- local_archive


def test_local_archive_always_available() -> None:
    publisher = LocalArchivePublisher()
    assert publisher.is_available() is True


def test_local_archive_copies_files(tmp_path: Path) -> None:
    store = Store(root=tmp_path)
    sketch = _seed_finished_sketch(store)
    publisher = LocalArchivePublisher(config={"id": "local_archive"})
    result = publisher.publish(sketch, store)

    assert result.success is True
    assert result.destination_id == "local_archive"
    assert result.url.startswith("file://")

    archive_dir = tmp_path / "published" / sketch.id
    assert archive_dir.is_dir()
    assert (archive_dir / "final.mp4").exists()
    assert (archive_dir / "final.mp4").read_bytes() == b"FAKE_MP4_BYTES"
    assert (archive_dir / "sketch.json").exists()
    assert (archive_dir / "critic.json").exists()
    assert (archive_dir / "published_at.txt").exists()
    assert result.extra["final_mp4_present"] is True


def test_local_archive_handles_missing_final_mp4(tmp_path: Path) -> None:
    """Missing final.mp4 is logged but shouldn't fail the archive publish."""
    store = Store(root=tmp_path)
    sketch = _seed_finished_sketch(store)
    final_path = store.sketch_final_path(sketch.id)
    final_path.unlink()

    publisher = LocalArchivePublisher(config={"id": "local_archive"})
    result = publisher.publish(sketch, store)
    assert result.success is True
    assert result.extra["final_mp4_present"] is False
    # Other files still got archived.
    assert (tmp_path / "published" / sketch.id / "sketch.json").exists()


# ----------------------------------------------------------------- stub publisher


def test_stub_publisher_always_succeeds(tmp_path: Path) -> None:
    store = Store(root=tmp_path)
    sketch = _seed_finished_sketch(store)
    publisher = StubPublisher(config={"id": "tiktok"})
    result = publisher.publish(sketch, store)
    assert result.success is True
    assert result.destination_id == "tiktok"
    assert result.url == f"stub://tiktok/{sketch.id}"
    assert result.extra.get("stub") is True


# ----------------------------------------------------------------- youtube_shorts


def test_youtube_unavailable_without_env(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    for var in ("YT_REFRESH_TOKEN", "YT_CLIENT_ID", "YT_CLIENT_SECRET"):
        monkeypatch.delenv(var, raising=False)
    publisher = YouTubeShortsPublisher()
    assert publisher.is_available() is False

    store = Store(root=tmp_path)
    sketch = _seed_finished_sketch(store)
    result = publisher.publish(sketch, store)
    assert result.success is False
    assert "YT_REFRESH_TOKEN" in (result.error or "")


def test_youtube_missing_final_mp4(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("YT_REFRESH_TOKEN", "fake-rt")
    monkeypatch.setenv("YT_CLIENT_ID", "fake-id")
    monkeypatch.setenv("YT_CLIENT_SECRET", "fake-secret")

    store = Store(root=tmp_path)
    sketch = _seed_finished_sketch(store)
    store.sketch_final_path(sketch.id).unlink()

    publisher = YouTubeShortsPublisher()
    result = publisher.publish(sketch, store)
    assert result.success is False
    assert "final.mp4 missing" in (result.error or "")


# ----------------------------------------------------------------- youtube happy path (mocked httpx)


class _FakeResponse:
    def __init__(
        self,
        payload: Any = None,
        status_code: int = 200,
        text: str = "",
        headers: Optional[Dict[str, str]] = None,
    ) -> None:
        self._payload = payload
        self.status_code = status_code
        self.text = text or (json.dumps(payload) if payload is not None else "")
        self.headers = headers or {}

    def json(self) -> Any:
        if self._payload is None:
            raise ValueError("no json payload")
        return self._payload


class _FakeHttpx:
    def __init__(self, routes: Dict[str, List[_FakeResponse]]) -> None:
        self.routes = routes
        self.calls: List[Dict[str, Any]] = []

    def _resolve(self, url: str) -> _FakeResponse:
        for prefix, responses in self.routes.items():
            if prefix in url:
                if not responses:
                    return _FakeResponse(status_code=500, text="no more responses")
                return responses.pop(0)
        return _FakeResponse(status_code=404, text="no route")

    def post(self, url: str, **kwargs: Any) -> _FakeResponse:
        self.calls.append({"method": "POST", "url": url, "kwargs": kwargs})
        return self._resolve(url)

    def put(self, url: str, **kwargs: Any) -> _FakeResponse:
        self.calls.append({"method": "PUT", "url": url, "kwargs": kwargs})
        return self._resolve(url)


def _install_fake_httpx(monkeypatch: pytest.MonkeyPatch, fake: _FakeHttpx) -> None:
    fake_module = SimpleNamespace(post=fake.post, put=fake.put)
    monkeypatch.setitem(sys.modules, "httpx", fake_module)


def test_youtube_happy_path_mocked(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("YT_REFRESH_TOKEN", "fake-rt")
    monkeypatch.setenv("YT_CLIENT_ID", "fake-id")
    monkeypatch.setenv("YT_CLIENT_SECRET", "fake-secret")

    token_response = _FakeResponse(
        payload={"access_token": "fake-at", "expires_in": 3600, "token_type": "Bearer"},
    )
    init_response = _FakeResponse(
        status_code=200,
        payload=None,
        text="",
        headers={"location": "https://upload.googleapis.com/upload/session/fake"},
    )
    upload_response = _FakeResponse(
        payload={
            "kind": "youtube#video",
            "id": "abc123XYZ",
            "snippet": {"title": "x"},
        }
    )
    fake = _FakeHttpx(
        {
            "oauth2.googleapis.com/token": [token_response],
            "googleapis.com/upload/youtube/v3/videos": [init_response],
            "upload.googleapis.com/upload/session": [upload_response],
        }
    )
    _install_fake_httpx(monkeypatch, fake)

    store = Store(root=tmp_path)
    sketch = _seed_finished_sketch(store)

    publisher = YouTubeShortsPublisher(
        config={"id": "youtube_shorts", "default_privacy": "private", "category_id": "23"}
    )
    result = publisher.publish(sketch, store)

    assert result.success is True, f"expected success, got {result.error}"
    assert result.url == "https://www.youtube.com/watch?v=abc123XYZ"
    assert result.extra["video_id"] == "abc123XYZ"
    assert result.extra["category_id"] == "23"
    assert result.extra["privacy_status"] == "private"

    # Verify the init POST carried the metadata body with our snippet fields.
    init_call = next(
        c for c in fake.calls if c["method"] == "POST" and "/upload/youtube/v3/videos" in c["url"]
    )
    body = init_call["kwargs"]["json"]
    assert body["snippet"]["title"].startswith("A communications intern")
    assert body["snippet"]["categoryId"] == "23"
    assert "#shorts" in body["snippet"]["description"]
    assert body["status"]["privacyStatus"] == "private"
    # And the init request carried the resumable header.
    assert init_call["kwargs"]["headers"]["Authorization"] == "Bearer fake-at"
    assert init_call["kwargs"]["headers"]["X-Upload-Content-Type"] == "video/mp4"

    # Verify the video bytes were PUT to the session URI.
    put_call = next(c for c in fake.calls if c["method"] == "PUT")
    assert put_call["url"] == "https://upload.googleapis.com/upload/session/fake"
    assert put_call["kwargs"]["content"] == b"FAKE_MP4_BYTES"


def test_youtube_token_exchange_failure(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("YT_REFRESH_TOKEN", "fake-rt")
    monkeypatch.setenv("YT_CLIENT_ID", "fake-id")
    monkeypatch.setenv("YT_CLIENT_SECRET", "fake-secret")

    fake = _FakeHttpx(
        {
            "oauth2.googleapis.com/token": [
                _FakeResponse(status_code=400, text="invalid_grant", payload={"error": "invalid_grant"}),
            ],
        }
    )
    _install_fake_httpx(monkeypatch, fake)

    store = Store(root=tmp_path)
    sketch = _seed_finished_sketch(store)
    publisher = YouTubeShortsPublisher()
    result = publisher.publish(sketch, store)
    assert result.success is False
    assert "token refresh failed" in (result.error or "")


def test_youtube_init_missing_location_header(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("YT_REFRESH_TOKEN", "fake-rt")
    monkeypatch.setenv("YT_CLIENT_ID", "fake-id")
    monkeypatch.setenv("YT_CLIENT_SECRET", "fake-secret")
    fake = _FakeHttpx(
        {
            "oauth2.googleapis.com/token": [
                _FakeResponse(payload={"access_token": "fake-at"}),
            ],
            "googleapis.com/upload/youtube/v3/videos": [
                _FakeResponse(status_code=200, payload={}, headers={}),
            ],
        }
    )
    _install_fake_httpx(monkeypatch, fake)

    store = Store(root=tmp_path)
    sketch = _seed_finished_sketch(store)
    publisher = YouTubeShortsPublisher()
    result = publisher.publish(sketch, store)
    assert result.success is False
    assert "missing Location" in (result.error or "")


# ----------------------------------------------------------------- pipeline orchestrator


def test_run_publishers_happy_path(tmp_path: Path) -> None:
    store = Store(root=tmp_path)
    sketch = _seed_finished_sketch(store)
    publishers = [
        LocalArchivePublisher(config={"id": "local_archive"}),
        StubPublisher(config={"id": "tiktok"}),
    ]
    results = run_publishers(sketch, store, publishers=publishers)
    assert len(results) == 2
    assert all(r.success for r in results)
    assert {r.destination_id for r in results} == {"local_archive", "tiktok"}


class _RaisingPublisher(Publisher):
    destination_id = "raiser"

    def is_available(self) -> bool:
        return True

    def publish(self, sketch: Sketch, store: Store) -> PublishResult:
        raise RuntimeError("kaboom")


def test_run_publishers_catches_raised_exceptions(tmp_path: Path) -> None:
    store = Store(root=tmp_path)
    sketch = _seed_finished_sketch(store)
    publishers = [LocalArchivePublisher(config={"id": "local_archive"}), _RaisingPublisher()]
    results = run_publishers(sketch, store, publishers=publishers)
    assert len(results) == 2
    assert results[0].success is True
    assert results[1].success is False
    assert "kaboom" in (results[1].error or "")


def test_load_publishers_from_production_config() -> None:
    """The production config/publishing.yaml must be importable."""
    publishers = load_publishers()
    ids = {p.destination_id for p in publishers}
    assert "local_archive" in ids
    assert "youtube_shorts" in ids


def test_load_publishing_config_returns_defaults_when_missing(tmp_path: Path) -> None:
    cfg = load_publishing_config(tmp_path / "nonexistent.yaml")
    assert cfg == {"destinations": []}


# ----------------------------------------------------------------- publish integration


@pytest.mark.publish
def test_real_youtube_upload(tmp_path: Path) -> None:
    """Opt-in integration test. Burns real quota. Skipped unless env is set."""
    import os as _os

    required = ("YT_REFRESH_TOKEN", "YT_CLIENT_ID", "YT_CLIENT_SECRET")
    if not all(_os.environ.get(k) for k in required):
        pytest.skip(f"one of {required} not set")

    store = Store(root=tmp_path)
    sketch = _seed_finished_sketch(store)
    publisher = YouTubeShortsPublisher(
        config={"id": "youtube_shorts", "default_privacy": "private"}
    )
    result = publisher.publish(sketch, store)
    assert result.success is True, result.error
    assert result.url.startswith("https://www.youtube.com/watch?v=")

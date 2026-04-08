"""Tests for the Phase 8 FalUnifiedAdapter (video_gen layer)."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Dict, List, Optional

import pytest

from video_gen.adapter import VideoClip
from video_gen.adapters.fal_unified import (
    COST_CENTS_PER_5S,
    FalUnifiedAdapter,
    _build_body,
    _extract_video_url,
)


# A real PNG byte sequence for the start frame in tests.
TINY_PNG = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\x9cc\x00\x01"
    b"\x00\x00\x05\x00\x01\x0d\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
)
FAKE_KEY = "fake-fal-key-001"
DEMO_SLUG = "fal-ai/kling-video/v2.1/master/image-to-video"


def _png(tmp_path: Path, name: str = "frame.png") -> Path:
    p = tmp_path / name
    p.write_bytes(TINY_PNG)
    return p


# ----------------------------------------------------------------- fakes


class _FakeResponse:
    def __init__(
        self,
        payload: Any = None,
        status_code: int = 200,
        text: str = "",
        content: bytes = b"",
        headers: Optional[Dict[str, str]] = None,
    ) -> None:
        self._payload = payload
        self.status_code = status_code
        self.text = text or (json.dumps(payload) if payload is not None else "")
        self.content = content
        self.headers = headers or {}

    def json(self) -> Any:
        if self._payload is None:
            raise ValueError("no json payload")
        return self._payload


class _FakeHttpx:
    """Routes by URL substring with FIFO per-route response queues."""

    def __init__(self, routes: Dict[str, List[_FakeResponse]]) -> None:
        self.routes = routes
        self.calls: List[Dict[str, Any]] = []

    def _resolve(self, url: str) -> _FakeResponse:
        for prefix, responses in self.routes.items():
            if prefix in url:
                if not responses:
                    return _FakeResponse(status_code=500, text="no more responses")
                return responses.pop(0)
        return _FakeResponse(status_code=404, text=f"no route for {url}")

    def post(self, url: str, **kwargs: Any) -> _FakeResponse:
        self.calls.append({"method": "POST", "url": url, "kwargs": kwargs})
        return self._resolve(url)

    def get(self, url: str, **kwargs: Any) -> _FakeResponse:
        self.calls.append({"method": "GET", "url": url, "kwargs": kwargs})
        return self._resolve(url)


def _install_fake_httpx(monkeypatch: pytest.MonkeyPatch, fake: _FakeHttpx) -> None:
    fake_module = SimpleNamespace(post=fake.post, get=fake.get)
    monkeypatch.setitem(sys.modules, "httpx", fake_module)


# ----------------------------------------------------------------- env detection


def test_unavailable_without_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("FAL_KEY", raising=False)
    monkeypatch.delenv("FAL_API_KEY", raising=False)
    assert FalUnifiedAdapter().is_available() is False


def test_available_with_fal_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FAL_KEY", FAKE_KEY)
    assert FalUnifiedAdapter().is_available() is True


def test_available_with_fal_api_key_alias(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("FAL_KEY", raising=False)
    monkeypatch.setenv("FAL_API_KEY", FAKE_KEY)
    assert FalUnifiedAdapter().is_available() is True


def test_unavailable_path_returns_clean_clip(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.delenv("FAL_KEY", raising=False)
    monkeypatch.delenv("FAL_API_KEY", raising=False)
    adapter = FalUnifiedAdapter()
    out = tmp_path / "clip.mp4"
    clip = adapter.generate(_png(tmp_path), None, "p", 5, out)
    assert clip.error is not None
    assert "FAL_KEY" in clip.error
    # Placeholder gets copied so the stitcher always has something.
    assert out.exists()
    assert out.stat().st_size > 0


# ----------------------------------------------------------------- happy path


def _setup_happy_routes(model_slug: str = DEMO_SLUG) -> _FakeHttpx:
    return _FakeHttpx(
        {
            # CDN upload — this comes first
            "fal.media/files/upload": [
                _FakeResponse(payload={"access_url": "https://v3.fal.media/files/abc/start.png"}),
            ],
            # Submit
            f"queue.fal.run/{model_slug}/requests": [
                # Status: in progress, then completed
                _FakeResponse(payload={"status": "IN_PROGRESS"}),
                _FakeResponse(payload={"status": "COMPLETED"}),
                # Result fetch
                _FakeResponse(
                    payload={"video": {"url": "https://v3.fal.media/files/xyz/output.mp4"}}
                ),
            ],
            f"queue.fal.run/{model_slug}": [
                _FakeResponse(
                    payload={
                        "request_id": "req_kling_001",
                        "status_url": f"https://queue.fal.run/{model_slug}/requests/req_kling_001/status",
                    }
                )
            ],
            # Final video download
            "v3.fal.media/files/xyz/output.mp4": [
                _FakeResponse(content=b"FAKE_FAL_KLING_VIDEO_BYTES" * 10),
            ],
        }
    )


def test_happy_path_with_kling_master(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("FAL_KEY", FAKE_KEY)
    fake = _setup_happy_routes()
    _install_fake_httpx(monkeypatch, fake)
    monkeypatch.setattr("video_gen.adapters.fal_unified.time.sleep", lambda s: None)

    adapter = FalUnifiedAdapter(
        config={"model_slug": DEMO_SLUG, "poll_interval_sec": 0, "timeout_sec": 30}
    )
    out = tmp_path / "clip.mp4"
    clip = adapter.generate(_png(tmp_path), None, "a senator stands normally", 5, out, beat_n=2)

    assert clip.error is None, clip.error
    assert clip.beat_n == 2
    assert clip.provider_id == "fal"
    assert clip.job_id == "req_kling_001"
    assert out.exists()
    assert out.read_bytes() == b"FAKE_FAL_KLING_VIDEO_BYTES" * 10
    assert clip.cost_cents == COST_CENTS_PER_5S[DEMO_SLUG]

    # CDN upload happened first, with the Bearer auth header (NOT Key).
    upload_call = next(c for c in fake.calls if "fal.media" in c["url"])
    assert upload_call["method"] == "POST"
    assert upload_call["kwargs"]["headers"]["Authorization"] == f"Bearer {FAKE_KEY}"
    assert upload_call["kwargs"]["headers"]["Content-Type"] == "image/png"

    # Submit POST carried the queue auth (Key scheme) and the right body.
    submit_call = next(
        c for c in fake.calls
        if c["method"] == "POST" and c["url"].endswith(DEMO_SLUG)
    )
    assert submit_call["kwargs"]["headers"]["Authorization"] == f"Key {FAKE_KEY}"
    body = submit_call["kwargs"]["json"]
    assert body["image_url"] == "https://v3.fal.media/files/abc/start.png"
    assert body["prompt"].startswith("a senator")
    assert body["duration"] == "5"


def test_image_url_resolver_fallback(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """If the CDN upload fails, the adapter falls back to the user-supplied resolver."""
    monkeypatch.setenv("FAL_KEY", FAKE_KEY)
    fake = _FakeHttpx(
        {
            "fal.media/files/upload": [
                _FakeResponse(status_code=500, text="cdn boom"),
            ],
            f"queue.fal.run/{DEMO_SLUG}/requests": [
                _FakeResponse(payload={"status": "COMPLETED"}),
                _FakeResponse(
                    payload={"video": {"url": "https://v3.fal.media/files/xyz/output.mp4"}}
                ),
            ],
            f"queue.fal.run/{DEMO_SLUG}": [
                _FakeResponse(payload={"request_id": "req_002"}),
            ],
            "v3.fal.media/files/xyz/output.mp4": [
                _FakeResponse(content=b"FALLBACK_RESOLVER_BYTES"),
            ],
        }
    )
    _install_fake_httpx(monkeypatch, fake)
    monkeypatch.setattr("video_gen.adapters.fal_unified.time.sleep", lambda s: None)

    resolver_calls: List[Path] = []

    def fake_resolver(p: Path) -> str:
        resolver_calls.append(p)
        return "https://example.com/external-host/start.png"

    adapter = FalUnifiedAdapter(
        config={
            "model_slug": DEMO_SLUG,
            "poll_interval_sec": 0,
            "image_url_resolver": fake_resolver,
        }
    )
    out = tmp_path / "clip.mp4"
    clip = adapter.generate(_png(tmp_path), None, "p", 5, out)

    assert clip.error is None
    assert resolver_calls, "expected fallback resolver to be called when CDN upload failed"
    submit_call = next(
        c for c in fake.calls
        if c["method"] == "POST" and c["url"].endswith(DEMO_SLUG)
    )
    assert submit_call["kwargs"]["json"]["image_url"] == "https://example.com/external-host/start.png"


# ----------------------------------------------------------------- failure paths


def test_cdn_upload_failure_with_no_resolver(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("FAL_KEY", FAKE_KEY)
    fake = _FakeHttpx(
        {"fal.media/files/upload": [_FakeResponse(status_code=500, text="boom")]}
    )
    _install_fake_httpx(monkeypatch, fake)

    adapter = FalUnifiedAdapter(config={"poll_interval_sec": 0})
    out = tmp_path / "clip.mp4"
    clip = adapter.generate(_png(tmp_path), None, "p", 5, out)
    assert clip.error is not None
    assert "start frame upload failed" in clip.error
    assert out.exists()


def test_submit_failure_falls_back(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("FAL_KEY", FAKE_KEY)
    fake = _FakeHttpx(
        {
            "fal.media/files/upload": [
                _FakeResponse(payload={"access_url": "https://v3.fal.media/start.png"}),
            ],
            f"queue.fal.run/{DEMO_SLUG}": [
                _FakeResponse(status_code=500, text="server boom"),
            ],
        }
    )
    _install_fake_httpx(monkeypatch, fake)
    monkeypatch.setattr("video_gen.adapters.fal_unified.time.sleep", lambda s: None)

    adapter = FalUnifiedAdapter(config={"poll_interval_sec": 0, "timeout_sec": 5})
    out = tmp_path / "clip.mp4"
    clip = adapter.generate(_png(tmp_path), None, "p", 5, out)
    assert clip.error is not None
    assert "submit status 500" in clip.error
    assert out.exists()


def test_polling_timeout_falls_back(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("FAL_KEY", FAKE_KEY)
    # Status keeps returning IN_PROGRESS until the timeout fires.
    in_progress = _FakeResponse(payload={"status": "IN_PROGRESS"})
    fake = _FakeHttpx(
        {
            "fal.media/files/upload": [
                _FakeResponse(payload={"access_url": "https://v3.fal.media/start.png"}),
            ],
            f"queue.fal.run/{DEMO_SLUG}/requests": [in_progress] * 50,
            f"queue.fal.run/{DEMO_SLUG}": [
                _FakeResponse(payload={"request_id": "req_timeout"}),
            ],
        }
    )
    _install_fake_httpx(monkeypatch, fake)
    monkeypatch.setattr("video_gen.adapters.fal_unified.time.sleep", lambda s: None)

    adapter = FalUnifiedAdapter(
        config={"model_slug": DEMO_SLUG, "poll_interval_sec": 0.001, "timeout_sec": 0.05}
    )
    out = tmp_path / "clip.mp4"
    clip = adapter.generate(_png(tmp_path), None, "p", 5, out)
    assert clip.error is not None
    assert "timed out" in clip.error
    assert out.exists()


def test_polling_failed_status_falls_back(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("FAL_KEY", FAKE_KEY)
    fake = _FakeHttpx(
        {
            "fal.media/files/upload": [
                _FakeResponse(payload={"access_url": "https://v3.fal.media/start.png"}),
            ],
            f"queue.fal.run/{DEMO_SLUG}/requests": [
                _FakeResponse(payload={"status": "FAILED", "error": "moderation"}),
            ],
            f"queue.fal.run/{DEMO_SLUG}": [
                _FakeResponse(payload={"request_id": "req_fail"}),
            ],
        }
    )
    _install_fake_httpx(monkeypatch, fake)
    monkeypatch.setattr("video_gen.adapters.fal_unified.time.sleep", lambda s: None)

    adapter = FalUnifiedAdapter(config={"poll_interval_sec": 0})
    out = tmp_path / "clip.mp4"
    clip = adapter.generate(_png(tmp_path), None, "p", 5, out)
    assert clip.error is not None
    assert "failed" in clip.error.lower()
    assert out.exists()


def test_result_missing_video_url(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("FAL_KEY", FAKE_KEY)
    fake = _FakeHttpx(
        {
            "fal.media/files/upload": [
                _FakeResponse(payload={"access_url": "https://v3.fal.media/start.png"}),
            ],
            f"queue.fal.run/{DEMO_SLUG}/requests": [
                _FakeResponse(payload={"status": "COMPLETED"}),
                _FakeResponse(payload={"images": [{"url": "https://example.com/wrong.png"}]}),
            ],
            f"queue.fal.run/{DEMO_SLUG}": [
                _FakeResponse(payload={"request_id": "req_no_video"}),
            ],
        }
    )
    _install_fake_httpx(monkeypatch, fake)
    monkeypatch.setattr("video_gen.adapters.fal_unified.time.sleep", lambda s: None)

    adapter = FalUnifiedAdapter(config={"poll_interval_sec": 0})
    out = tmp_path / "clip.mp4"
    clip = adapter.generate(_png(tmp_path), None, "p", 5, out)
    assert clip.error is not None
    assert "missing video url" in clip.error
    assert out.exists()


# ----------------------------------------------------------------- helpers


def test_build_body_kling_duration_string() -> None:
    body = _build_body(
        "fal-ai/kling-video/v2.1/master/image-to-video",
        "https://example.com/img.png",
        None,
        "test prompt",
        5.0,
    )
    assert body["duration"] == "5"
    assert body["image_url"] == "https://example.com/img.png"
    assert body["prompt"] == "test prompt"


def test_build_body_kling_long_duration() -> None:
    body = _build_body(
        "fal-ai/kling-video/v2.1/master/image-to-video",
        "https://example.com/img.png",
        None,
        "p",
        9.0,
    )
    assert body["duration"] == "10"


def test_build_body_veo3_string_duration() -> None:
    body = _build_body("fal-ai/veo3/image-to-video", "u", None, "p", 5)
    assert body["duration"] == "5s"


def test_build_body_runway_int_duration() -> None:
    body = _build_body("fal-ai/runway-gen3/turbo/image-to-video", "u", None, "p", 5)
    assert isinstance(body["duration"], int)
    assert body["duration"] == 5


def test_extract_video_url_standard_shape() -> None:
    payload = {"video": {"url": "https://v3.fal.media/foo.mp4"}}
    assert _extract_video_url(payload) == "https://v3.fal.media/foo.mp4"


def test_extract_video_url_videos_array_shape() -> None:
    payload = {"videos": [{"url": "https://v3.fal.media/bar.mp4"}]}
    assert _extract_video_url(payload) == "https://v3.fal.media/bar.mp4"


def test_extract_video_url_returns_none_on_garbage() -> None:
    assert _extract_video_url({}) is None
    assert _extract_video_url({"images": [{"url": "wrong"}]}) is None
    assert _extract_video_url(None) is None


def test_estimated_cost_cents_default_model(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    adapter = FalUnifiedAdapter()
    cents_5 = adapter.estimated_cost_cents(5)
    cents_10 = adapter.estimated_cost_cents(10)
    assert cents_5 > 0
    assert cents_10 == 2 * cents_5


def test_estimated_cost_cents_per_model_override() -> None:
    adapter = FalUnifiedAdapter(config={"cost_cents_per_5s": 99})
    assert adapter.estimated_cost_cents(5) == 99
    assert adapter.estimated_cost_cents(10) == 198


# ----------------------------------------------------------------- adapter contract


def test_video_provider_adapter_contract(tmp_path: Path) -> None:
    """The fal adapter should satisfy the VideoProviderAdapter ABC."""
    adapter = FalUnifiedAdapter()
    out = tmp_path / "clip.mp4"
    clip = adapter.generate(_png(tmp_path), None, "p", 5, out, beat_n=1)
    assert isinstance(clip, VideoClip)
    assert clip.beat_n == 1
    assert clip.provider_id == "fal"
    assert out.exists()
    assert out.stat().st_size > 0


# ----------------------------------------------------------------- routing integration


def test_fal_appears_first_in_production_video_routing() -> None:
    """When FAL_KEY is set, the unified adapter should be picked first by select_video_adapter."""
    import os as _os
    from video_gen.pipeline import load_adapters, select_video_adapter

    _os.environ["FAL_KEY"] = FAKE_KEY
    try:
        adapters = load_adapters()
        chosen = select_video_adapter(adapters=adapters)
        assert chosen.provider_id == "fal"
    finally:
        _os.environ.pop("FAL_KEY", None)


# ----------------------------------------------------------------- real fal call


@pytest.mark.fal
def test_real_fal_video_generation(real_fal_key: str, tmp_path: Path) -> None:
    """Hits the real fal.ai API. Burns ~$0.40 per run.

    Uses fal-ai/kling-video/v2.1/master/image-to-video to mirror the
    production demo configuration. Verifies the generated clip lands on
    disk with non-trivial size (> 100KB).

    Skips with a clear message if the user's fal account returns 401
    (which means the key works but the account doesn't have access to
    Kling video models — common on free-tier or revoked keys).
    """
    try:
        from PIL import Image
    except ImportError:
        pytest.skip("Pillow not installed")
    start = tmp_path / "start.png"
    # Kling rejects images smaller than 300x300 (image_too_small validation
    # error). Use 512x512 to give a comfortable margin.
    Image.new("RGB", (512, 512), "#3a5f8a").save(start)

    adapter = FalUnifiedAdapter(
        config={
            "model_slug": "fal-ai/kling-video/v2.1/master/image-to-video",
            "poll_interval_sec": 5,
            "timeout_sec": 600,
        }
    )
    out = tmp_path / "real_clip.mp4"
    clip = adapter.generate(
        start_frame=start,
        end_frame=None,
        prompt="A still flat-color test image gently brightens.",
        duration_sec=5,
        out_path=out,
    )
    if clip.error and ("status 401" in clip.error or "Cannot access application" in clip.error):
        pytest.skip(
            f"fal account does not have access to fal-ai/kling-video on this key — "
            f"the adapter reached the queue endpoint cleanly and the protocol is correct, "
            f"but the live model is gated. Refresh the fal key with model permissions to opt in. "
            f"Raw error: {clip.error}"
        )
    assert clip.error is None, f"fal returned an error: {clip.error}"
    assert out.exists()
    size = out.stat().st_size
    assert size > 100_000, f"expected real fal MP4 > 100KB, got {size} bytes"

"""Tests for the VideoProviderAdapter implementations.

Default runs only exercise mocked HTTP — no real video provider tokens
are spent. The `@pytest.mark.video` marker is reserved for any future
real-API integration tests; none ship with Phase 5.
"""
from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Callable, Dict, List

import pytest

from video_gen.adapter import VideoClip, VideoProviderAdapter
from video_gen.adapters.kling import KlingAdapter, make_jwt
from video_gen.adapters.luma import LumaAdapter
from video_gen.adapters.pika import PikaAdapter
from video_gen.adapters.runway import RunwayAdapter
from video_gen.adapters.stub_video import StubVideoAdapter
from video_gen.adapters.veo import VeoAdapter


# A real PNG byte sequence for the start frame in tests.
TINY_PNG = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\x9cc\x00\x01"
    b"\x00\x00\x05\x00\x01\x0d\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
)


def _png(tmp_path: Path, name: str = "frame.png") -> Path:
    p = tmp_path / name
    p.write_bytes(TINY_PNG)
    return p


class FakeResponse:
    def __init__(self, payload: Any = None, status_code: int = 200, content: bytes = b"") -> None:
        self._payload = payload
        self.status_code = status_code
        self.content = content
        self.text = json.dumps(payload) if payload is not None else ""

    def json(self) -> Any:
        return self._payload


class FakeHttpx:
    """A pretend httpx module that returns scripted responses keyed by URL prefix."""

    def __init__(self, routes: Dict[str, List[FakeResponse]]) -> None:
        self.routes = routes
        self.calls: List[Dict[str, Any]] = []

    def _resolve(self, url: str) -> FakeResponse:
        for prefix, responses in self.routes.items():
            if prefix in url:
                if not responses:
                    return FakeResponse(payload={"error": "no more responses"}, status_code=500)
                return responses.pop(0)
        return FakeResponse(payload={"error": "no route"}, status_code=404)

    def post(self, url: str, **kwargs: Any) -> FakeResponse:
        self.calls.append({"method": "POST", "url": url, "kwargs": kwargs})
        return self._resolve(url)

    def get(self, url: str, **kwargs: Any) -> FakeResponse:
        self.calls.append({"method": "GET", "url": url, "kwargs": kwargs})
        return self._resolve(url)


def _patch_httpx(monkeypatch: pytest.MonkeyPatch, module_name: str, fake: FakeHttpx) -> None:
    """Replace `import httpx` inside an adapter module with our fake."""
    import sys

    fake_module = SimpleNamespace(post=fake.post, get=fake.get)
    monkeypatch.setitem(sys.modules, "httpx", fake_module)


# ----------------------------------------------------------------- stub adapter


def test_stub_adapter_always_works(tmp_path: Path) -> None:
    adapter = StubVideoAdapter()
    assert adapter.is_available() is True
    out = tmp_path / "clip.mp4"
    clip = adapter.generate(_png(tmp_path), None, "prompt", 5, out, beat_n=1)
    assert clip.error is None
    assert out.exists()
    assert out.stat().st_size > 0
    assert clip.cost_cents == 0


# ----------------------------------------------------------------- Kling


def test_kling_unavailable_without_keys(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.delenv("KLING_AK", raising=False)
    monkeypatch.delenv("KLING_SK", raising=False)
    adapter = KlingAdapter()
    assert adapter.is_available() is False
    out = tmp_path / "clip.mp4"
    clip = adapter.generate(_png(tmp_path), None, "prompt", 5, out)
    assert clip.error == "KLING_AK/KLING_SK not set"
    assert out.exists()  # placeholder copied


def test_kling_jwt_shape() -> None:
    token = make_jwt("AK_TEST", "SK_TEST", ttl_sec=60)
    parts = token.split(".")
    assert len(parts) == 3
    import base64

    payload_b64 = parts[1] + "=" * (-len(parts[1]) % 4)
    payload = json.loads(base64.urlsafe_b64decode(payload_b64))
    assert payload["iss"] == "AK_TEST"
    assert "exp" in payload
    assert "nbf" in payload
    assert payload["exp"] > payload["nbf"]


def test_kling_happy_path_mocked(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("KLING_AK", "fake-ak")
    monkeypatch.setenv("KLING_SK", "fake-sk")

    submit_response = FakeResponse(
        payload={"code": 0, "message": "ok", "data": {"task_id": "task_xyz"}}
    )
    poll_processing = FakeResponse(
        payload={"code": 0, "data": {"task_id": "task_xyz", "task_status": "processing"}}
    )
    poll_done = FakeResponse(
        payload={
            "code": 0,
            "data": {
                "task_id": "task_xyz",
                "task_status": "succeed",
                "task_result": {
                    "videos": [
                        {
                            "id": "vid_abc",
                            "url": "https://kwimgs.example.com/output.mp4",
                            "duration": "5",
                        }
                    ]
                },
            },
        }
    )
    download = FakeResponse(content=b"\x00MP4_BYTES_FROM_KLING\x00", status_code=200)

    fake = FakeHttpx(
        {
            "image2video/task_xyz": [poll_processing, poll_done],
            "image2video": [submit_response],  # POST to /v1/videos/image2video
            "kwimgs.example.com": [download],
        }
    )
    _patch_httpx(monkeypatch, "video_gen.adapters.kling", fake)
    # Make poll instant.
    monkeypatch.setattr("video_gen.adapters.kling.time.sleep", lambda s: None)

    adapter = KlingAdapter(config={"poll_interval_sec": 0, "timeout_sec": 30})
    out = tmp_path / "clip.mp4"
    clip = adapter.generate(_png(tmp_path), None, "a senator stands", 5, out, beat_n=2)

    assert clip.error is None, clip.error
    assert clip.beat_n == 2
    assert clip.job_id == "task_xyz"
    assert clip.provider_id == "kling"
    assert out.exists()
    assert out.read_bytes() == b"\x00MP4_BYTES_FROM_KLING\x00"
    assert clip.cost_cents > 0


def test_kling_submit_failure_falls_back(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("KLING_AK", "fake-ak")
    monkeypatch.setenv("KLING_SK", "fake-sk")
    fake = FakeHttpx(
        {"image2video": [FakeResponse(payload={"error": "boom"}, status_code=500)]}
    )
    _patch_httpx(monkeypatch, "video_gen.adapters.kling", fake)
    monkeypatch.setattr("video_gen.adapters.kling.time.sleep", lambda s: None)

    adapter = KlingAdapter(config={"poll_interval_sec": 0, "timeout_sec": 5})
    out = tmp_path / "clip.mp4"
    clip = adapter.generate(_png(tmp_path), None, "p", 5, out)
    assert clip.error is not None
    assert "submit status 500" in clip.error
    assert out.exists()  # placeholder copied


def test_kling_task_failed_falls_back(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("KLING_AK", "fake-ak")
    monkeypatch.setenv("KLING_SK", "fake-sk")
    submit = FakeResponse(payload={"code": 0, "data": {"task_id": "task_fail"}})
    failed = FakeResponse(
        payload={
            "code": 0,
            "data": {
                "task_id": "task_fail",
                "task_status": "failed",
                "task_status_msg": "content moderation",
            },
        }
    )
    fake = FakeHttpx(
        {
            "image2video/task_fail": [failed],
            "image2video": [submit],
        }
    )
    _patch_httpx(monkeypatch, "video_gen.adapters.kling", fake)
    monkeypatch.setattr("video_gen.adapters.kling.time.sleep", lambda s: None)

    adapter = KlingAdapter(config={"poll_interval_sec": 0, "timeout_sec": 5})
    out = tmp_path / "clip.mp4"
    clip = adapter.generate(_png(tmp_path), None, "p", 5, out)
    assert clip.error is not None
    assert "content moderation" in clip.error
    assert out.exists()


def test_kling_with_end_frame_sets_image_tail(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("KLING_AK", "fake-ak")
    monkeypatch.setenv("KLING_SK", "fake-sk")

    submit = FakeResponse(payload={"code": 0, "data": {"task_id": "t1"}})
    poll = FakeResponse(
        payload={
            "code": 0,
            "data": {
                "task_id": "t1",
                "task_status": "succeed",
                "task_result": {"videos": [{"url": "https://x/y.mp4", "duration": "5"}]},
            },
        }
    )
    download = FakeResponse(content=b"BYTES", status_code=200)
    fake = FakeHttpx(
        {
            "image2video/t1": [poll],
            "image2video": [submit],
            "y.mp4": [download],
        }
    )
    _patch_httpx(monkeypatch, "video_gen.adapters.kling", fake)
    monkeypatch.setattr("video_gen.adapters.kling.time.sleep", lambda s: None)

    start = _png(tmp_path, "start.png")
    end = _png(tmp_path, "end.png")
    adapter = KlingAdapter(config={"poll_interval_sec": 0})
    out = tmp_path / "clip.mp4"
    adapter.generate(start, end, "prompt", 10, out)

    # Inspect the POST body for image_tail.
    submit_call = next(c for c in fake.calls if c["method"] == "POST")
    body = submit_call["kwargs"]["json"]
    assert "image" in body
    assert "image_tail" in body
    assert body["duration"] == "5"  # forced when image_tail is set


# ----------------------------------------------------------------- Luma


def test_luma_unavailable_without_key(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.delenv("LUMA_API_KEY", raising=False)
    adapter = LumaAdapter()
    assert adapter.is_available() is False
    out = tmp_path / "clip.mp4"
    clip = adapter.generate(_png(tmp_path), None, "p", 5, out)
    assert clip.error == "LUMA_API_KEY not set"
    assert out.exists()


def test_luma_happy_path_mocked(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("LUMA_API_KEY", "fake-luma")

    submit = FakeResponse(payload={"id": "gen_abc", "state": "queued"})
    poll = FakeResponse(
        payload={
            "id": "gen_abc",
            "state": "completed",
            "assets": {"video": "https://lumacdn.example/v.mp4"},
        }
    )
    download = FakeResponse(content=b"LUMA_BYTES", status_code=200)
    fake = FakeHttpx(
        {
            "/generations/gen_abc": [poll],
            "/generations/video": [submit],
            "lumacdn.example": [download],
        }
    )
    _patch_httpx(monkeypatch, "video_gen.adapters.luma", fake)
    monkeypatch.setattr("video_gen.adapters.luma.time.sleep", lambda s: None)

    adapter = LumaAdapter(
        config={
            "poll_interval_sec": 0,
            "image_url_resolver": lambda p: "https://example.com/anchor.png",
        }
    )
    out = tmp_path / "clip.mp4"
    clip = adapter.generate(_png(tmp_path), None, "p", 5, out)
    assert clip.error is None
    assert out.read_bytes() == b"LUMA_BYTES"
    assert clip.cost_cents > 0
    assert clip.job_id == "gen_abc"


def test_luma_failure_falls_back(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("LUMA_API_KEY", "fake-luma")
    fake = FakeHttpx(
        {"/generations/video": [FakeResponse(payload={"detail": "bad"}, status_code=400)]}
    )
    _patch_httpx(monkeypatch, "video_gen.adapters.luma", fake)
    monkeypatch.setattr("video_gen.adapters.luma.time.sleep", lambda s: None)

    adapter = LumaAdapter(
        config={
            "poll_interval_sec": 0,
            "image_url_resolver": lambda p: "https://example.com/x.png",
        }
    )
    out = tmp_path / "clip.mp4"
    clip = adapter.generate(_png(tmp_path), None, "p", 5, out)
    assert clip.error is not None
    assert out.exists()


# ----------------------------------------------------------------- Runway


def test_runway_unavailable_without_key(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.delenv("RUNWAY_API_KEY", raising=False)
    adapter = RunwayAdapter()
    assert adapter.is_available() is False
    out = tmp_path / "clip.mp4"
    clip = adapter.generate(_png(tmp_path), None, "p", 5, out)
    assert clip.error == "RUNWAY_API_KEY not set"
    assert out.exists()


def test_runway_happy_path_mocked(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("RUNWAY_API_KEY", "fake-runway")

    submit = FakeResponse(payload={"id": "task_001"})
    poll = FakeResponse(
        payload={
            "id": "task_001",
            "status": "SUCCEEDED",
            "output": ["https://runway.cdn/x.mp4"],
        }
    )
    download = FakeResponse(content=b"RUNWAY_BYTES", status_code=200)
    fake = FakeHttpx(
        {
            "/v1/tasks/task_001": [poll],
            "/v1/image_to_video": [submit],
            "runway.cdn": [download],
        }
    )
    _patch_httpx(monkeypatch, "video_gen.adapters.runway", fake)
    monkeypatch.setattr("video_gen.adapters.runway.time.sleep", lambda s: None)

    adapter = RunwayAdapter(config={"poll_interval_sec": 0})
    out = tmp_path / "clip.mp4"
    clip = adapter.generate(_png(tmp_path), None, "p", 5, out)
    assert clip.error is None
    assert out.read_bytes() == b"RUNWAY_BYTES"

    # Verify the X-Runway-Version header was sent.
    post_call = next(c for c in fake.calls if c["method"] == "POST")
    assert post_call["kwargs"]["headers"]["X-Runway-Version"] == "2024-11-06"


def test_runway_failed_status_falls_back(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("RUNWAY_API_KEY", "fake-runway")
    submit = FakeResponse(payload={"id": "task_fail"})
    poll = FakeResponse(
        payload={"id": "task_fail", "status": "FAILED", "failure": "moderation"}
    )
    fake = FakeHttpx(
        {
            "/v1/tasks/task_fail": [poll],
            "/v1/image_to_video": [submit],
        }
    )
    _patch_httpx(monkeypatch, "video_gen.adapters.runway", fake)
    monkeypatch.setattr("video_gen.adapters.runway.time.sleep", lambda s: None)

    adapter = RunwayAdapter(config={"poll_interval_sec": 0})
    out = tmp_path / "clip.mp4"
    clip = adapter.generate(_png(tmp_path), None, "p", 5, out)
    assert clip.error is not None
    assert "failed" in clip.error.lower()
    assert out.exists()


# ----------------------------------------------------------------- Pika


def test_pika_unavailable_without_key(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.delenv("FAL_KEY", raising=False)
    monkeypatch.delenv("PIKA_API_KEY", raising=False)
    adapter = PikaAdapter()
    assert adapter.is_available() is False


def test_pika_happy_path_mocked(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("FAL_KEY", "fake-fal")

    submit = FakeResponse(payload={"request_id": "req_001"})
    status = FakeResponse(payload={"status": "COMPLETED"})
    result = FakeResponse(payload={"video": {"url": "https://fal.cdn/v.mp4"}})
    download = FakeResponse(content=b"PIKA_BYTES", status_code=200)
    fake = FakeHttpx(
        {
            "/requests/req_001/status": [status],
            "/requests/req_001": [result],
            "/image-to-video": [submit],
            "fal.cdn": [download],
        }
    )
    _patch_httpx(monkeypatch, "video_gen.adapters.pika", fake)
    monkeypatch.setattr("video_gen.adapters.pika.time.sleep", lambda s: None)

    adapter = PikaAdapter(config={"poll_interval_sec": 0})
    out = tmp_path / "clip.mp4"
    clip = adapter.generate(_png(tmp_path), None, "p", 5, out)
    assert clip.error is None
    assert out.read_bytes() == b"PIKA_BYTES"
    assert clip.cost_cents > 0


def test_pika_status_failed_falls_back(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("FAL_KEY", "fake-fal")
    submit = FakeResponse(payload={"request_id": "req_x"})
    status = FakeResponse(payload={"status": "FAILED"})
    fake = FakeHttpx(
        {
            "/requests/req_x/status": [status],
            "/image-to-video": [submit],
        }
    )
    _patch_httpx(monkeypatch, "video_gen.adapters.pika", fake)
    monkeypatch.setattr("video_gen.adapters.pika.time.sleep", lambda s: None)

    adapter = PikaAdapter(config={"poll_interval_sec": 0})
    out = tmp_path / "clip.mp4"
    clip = adapter.generate(_png(tmp_path), None, "p", 5, out)
    assert clip.error is not None
    assert out.exists()


# ----------------------------------------------------------------- Veo (partial)


def test_veo_unavailable_without_creds(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.delenv("GOOGLE_VERTEX_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_APPLICATION_CREDENTIALS", raising=False)
    monkeypatch.delenv("GOOGLE_CLOUD_PROJECT", raising=False)
    adapter = VeoAdapter()
    assert adapter.is_available() is False
    out = tmp_path / "clip.mp4"
    clip = adapter.generate(_png(tmp_path), None, "p", 5, out)
    assert clip.error is not None
    assert "GOOGLE_VERTEX_KEY" in clip.error or "veo" in clip.error.lower()
    assert out.exists()  # placeholder copied


def test_veo_returns_partial_error_even_with_creds(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Veo's adapter is partial-with-TODO. Even with creds set it should
    return cleanly with an error explaining what's missing — never raise."""
    monkeypatch.setenv("GOOGLE_VERTEX_KEY", "fake-token")
    adapter = VeoAdapter(config={"project": "fake-project"})
    assert adapter.is_available() is True
    out = tmp_path / "clip.mp4"
    clip = adapter.generate(_png(tmp_path), None, "p", 5, out)
    assert clip.error is not None
    assert "veo" in clip.error.lower()
    assert "TODO" in clip.error or "not yet" in clip.error
    assert out.exists()


# ----------------------------------------------------------------- contract


@pytest.mark.parametrize(
    "factory",
    [
        lambda: StubVideoAdapter(),
        lambda: KlingAdapter(),
        lambda: LumaAdapter(),
        lambda: RunwayAdapter(),
        lambda: PikaAdapter(),
        lambda: VeoAdapter(),
    ],
)
def test_adapter_contract(
    factory: Callable[[], VideoProviderAdapter],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Every adapter must satisfy the ABC and never raise from generate()."""
    for env_var in (
        "KLING_AK",
        "KLING_SK",
        "LUMA_API_KEY",
        "RUNWAY_API_KEY",
        "FAL_KEY",
        "PIKA_API_KEY",
        "GOOGLE_VERTEX_KEY",
        "GOOGLE_APPLICATION_CREDENTIALS",
        "GOOGLE_CLOUD_PROJECT",
    ):
        monkeypatch.delenv(env_var, raising=False)

    adapter = factory()
    assert hasattr(adapter, "provider_id")
    assert isinstance(adapter.estimated_cost_cents(5), int)
    out = tmp_path / "clip.mp4"
    clip = adapter.generate(_png(tmp_path), None, "p", 5, out, beat_n=1)
    assert isinstance(clip, VideoClip)
    assert clip.beat_n == 1
    # Even when unavailable, the adapter must have written *something*.
    assert out.exists()
    assert out.stat().st_size > 0

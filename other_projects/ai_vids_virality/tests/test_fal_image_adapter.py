"""Tests for the Phase 8 FalImageAdapter (storyboard layer)."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Dict, List, Optional

import pytest

from storyboard.adapter import CharacterRef, Frame
from storyboard.adapters.fal_image import FalImageAdapter, _extract_image_url


TINY_PNG = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\x9cc\x00\x01"
    b"\x00\x00\x05\x00\x01\x0d\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
)
FAKE_KEY = "fake-fal-key-002"
STYLE_GUIDE = "bright stylized 3d animation"


def _png(tmp_path: Path, name: str = "ref.png") -> Path:
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
    ) -> None:
        self._payload = payload
        self.status_code = status_code
        self.text = text or (json.dumps(payload) if payload is not None else "")
        self.content = content

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


# ----------------------------------------------------------------- env


def test_unavailable_without_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("FAL_KEY", raising=False)
    monkeypatch.delenv("FAL_API_KEY", raising=False)
    assert FalImageAdapter().is_available() is False


def test_available_with_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FAL_KEY", FAKE_KEY)
    assert FalImageAdapter().is_available() is True


def test_character_ref_unavailable_returns_placeholder(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.delenv("FAL_KEY", raising=False)
    monkeypatch.delenv("FAL_API_KEY", raising=False)
    adapter = FalImageAdapter()
    out = tmp_path / "refs" / "brent.png"
    ref = adapter.generate_character_ref(
        {"name": "Brent", "description": "press secretary"}, STYLE_GUIDE, out
    )
    assert ref.error is not None
    assert "FAL_KEY" in ref.error
    assert out.exists()
    assert out.stat().st_size > 0


# ----------------------------------------------------------------- character ref happy


def test_character_ref_happy_path(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("FAL_KEY", FAKE_KEY)
    fake = _FakeHttpx(
        {
            "queue.fal.run/fal-ai/nano-banana-2/requests": [
                _FakeResponse(payload={"status": "COMPLETED"}),
                _FakeResponse(
                    payload={"images": [{"url": "https://v3.fal.media/character.png"}]}
                ),
            ],
            "queue.fal.run/fal-ai/nano-banana-2": [
                _FakeResponse(payload={"request_id": "req_char_001"}),
            ],
            "v3.fal.media/character.png": [_FakeResponse(content=b"FAKE_REF_PNG_BYTES")],
        }
    )
    _install_fake_httpx(monkeypatch, fake)
    monkeypatch.setattr("storyboard.adapters.fal_image.time.sleep", lambda s: None)

    adapter = FalImageAdapter(config={"poll_interval_sec": 0})
    out = tmp_path / "refs" / "brent.png"
    ref = adapter.generate_character_ref(
        {"name": "Brent", "description": "press secretary"}, STYLE_GUIDE, out
    )

    assert ref.error is None
    assert isinstance(ref, CharacterRef)
    assert ref.name == "Brent"
    assert ref.slug == "brent"
    assert ref.cost_cents > 0
    assert out.read_bytes() == b"FAKE_REF_PNG_BYTES"

    submit_call = next(
        c for c in fake.calls
        if c["method"] == "POST" and c["url"].endswith("nano-banana-2")
    )
    assert submit_call["kwargs"]["headers"]["Authorization"] == f"Key {FAKE_KEY}"
    body = submit_call["kwargs"]["json"]
    assert "Brent" in body["prompt"]
    assert "press secretary" in body["prompt"]
    assert body["num_images"] == 1


def test_character_ref_failure_falls_back(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("FAL_KEY", FAKE_KEY)
    fake = _FakeHttpx(
        {
            "queue.fal.run/fal-ai/nano-banana-2": [
                _FakeResponse(status_code=500, text="boom"),
            ],
        }
    )
    _install_fake_httpx(monkeypatch, fake)
    monkeypatch.setattr("storyboard.adapters.fal_image.time.sleep", lambda s: None)

    adapter = FalImageAdapter(config={"poll_interval_sec": 0})
    out = tmp_path / "refs" / "brent.png"
    ref = adapter.generate_character_ref(
        {"name": "Brent", "description": "x"}, STYLE_GUIDE, out
    )
    assert ref.error is not None
    assert out.exists()  # placeholder copied


# ----------------------------------------------------------------- frame happy (with refs)


def test_frame_with_refs_uploads_and_calls_edit(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("FAL_KEY", FAKE_KEY)

    # Pre-create a character ref PNG on disk so the adapter can read + upload it.
    ref_png = tmp_path / "refs" / "brent.png"
    ref_png.parent.mkdir(parents=True, exist_ok=True)
    ref_png.write_bytes(TINY_PNG)
    character_ref = CharacterRef(
        name="Brent",
        slug="brent",
        path=ref_png,
        prompt="",
        adapter_id="fal-image",
    )

    fake = _FakeHttpx(
        {
            "fal.media/files/upload": [
                _FakeResponse(payload={"access_url": "https://v3.fal.media/refs/brent.png"}),
            ],
            "queue.fal.run/fal-ai/nano-banana-2/edit/requests": [
                _FakeResponse(payload={"status": "COMPLETED"}),
                _FakeResponse(
                    payload={"images": [{"url": "https://v3.fal.media/frames/beat-02.png"}]}
                ),
            ],
            "queue.fal.run/fal-ai/nano-banana-2/edit": [
                _FakeResponse(payload={"request_id": "req_edit_001"}),
            ],
            "v3.fal.media/frames/beat-02.png": [_FakeResponse(content=b"FAKE_FRAME_PNG")],
        }
    )
    _install_fake_httpx(monkeypatch, fake)
    monkeypatch.setattr("storyboard.adapters.fal_image.time.sleep", lambda s: None)

    adapter = FalImageAdapter(config={"poll_interval_sec": 0})
    beat = {
        "n": 2,
        "action": "Brent freezes",
        "location": "office",
        "camera": "close-up",
        "characters": [{"name": "Brent", "description": "press secretary"}],
    }
    out = tmp_path / "storyboard" / "beat-02-start.png"
    frame = adapter.generate_frame(beat, [character_ref], STYLE_GUIDE, out)

    assert frame.error is None
    assert isinstance(frame, Frame)
    assert frame.beat_n == 2
    assert frame.cost_cents > 0
    assert out.read_bytes() == b"FAKE_FRAME_PNG"

    # CDN upload happened with Bearer auth (NOT Key).
    upload_call = next(c for c in fake.calls if "fal.media/files/upload" in c["url"])
    assert upload_call["kwargs"]["headers"]["Authorization"] == f"Bearer {FAKE_KEY}"
    assert upload_call["kwargs"]["headers"]["Content-Type"] == "image/png"

    # Edit POST carried image_urls from the upload + the frame prompt.
    edit_call = next(
        c for c in fake.calls
        if c["method"] == "POST" and c["url"].endswith("nano-banana-2/edit")
    )
    body = edit_call["kwargs"]["json"]
    assert body["image_urls"] == ["https://v3.fal.media/refs/brent.png"]
    assert "Brent" in body["prompt"]
    assert "office" in body["prompt"]


def test_frame_falls_back_to_text_only_when_no_refs(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """If we have no character refs (or none match the beat's characters),
    the adapter should fall back to the text-only nano-banana model."""
    monkeypatch.setenv("FAL_KEY", FAKE_KEY)
    fake = _FakeHttpx(
        {
            "queue.fal.run/fal-ai/nano-banana-2/requests": [
                _FakeResponse(payload={"status": "COMPLETED"}),
                _FakeResponse(
                    payload={"images": [{"url": "https://v3.fal.media/textonly.png"}]}
                ),
            ],
            "queue.fal.run/fal-ai/nano-banana-2": [
                _FakeResponse(payload={"request_id": "req_textonly_001"}),
            ],
            "v3.fal.media/textonly.png": [_FakeResponse(content=b"TEXT_ONLY_FRAME")],
        }
    )
    _install_fake_httpx(monkeypatch, fake)
    monkeypatch.setattr("storyboard.adapters.fal_image.time.sleep", lambda s: None)

    adapter = FalImageAdapter(config={"poll_interval_sec": 0})
    beat = {
        "n": 1,
        "action": "establishing shot of a parking lot",
        "characters": [],
        "camera": "wide",
        "location": "parking lot",
    }
    out = tmp_path / "storyboard" / "beat-01-start.png"
    frame = adapter.generate_frame(beat, [], STYLE_GUIDE, out)
    assert frame.error is None
    assert out.read_bytes() == b"TEXT_ONLY_FRAME"


def test_frame_failure_falls_back_to_placeholder(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("FAL_KEY", FAKE_KEY)
    fake = _FakeHttpx(
        {
            "queue.fal.run/fal-ai/nano-banana-2": [
                _FakeResponse(status_code=500, text="boom"),
            ],
        }
    )
    _install_fake_httpx(monkeypatch, fake)
    monkeypatch.setattr("storyboard.adapters.fal_image.time.sleep", lambda s: None)

    adapter = FalImageAdapter(config={"poll_interval_sec": 0})
    out = tmp_path / "storyboard" / "beat-01-start.png"
    frame = adapter.generate_frame(
        {"n": 1, "action": "x", "characters": []},
        [],
        STYLE_GUIDE,
        out,
    )
    assert frame.error is not None
    assert out.exists()
    assert out.stat().st_size > 0


def test_polling_failed_status_falls_back(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("FAL_KEY", FAKE_KEY)
    fake = _FakeHttpx(
        {
            "queue.fal.run/fal-ai/nano-banana-2/requests": [
                _FakeResponse(payload={"status": "FAILED"}),
            ],
            "queue.fal.run/fal-ai/nano-banana-2": [
                _FakeResponse(payload={"request_id": "req_fail_001"}),
            ],
        }
    )
    _install_fake_httpx(monkeypatch, fake)
    monkeypatch.setattr("storyboard.adapters.fal_image.time.sleep", lambda s: None)

    adapter = FalImageAdapter(config={"poll_interval_sec": 0})
    out = tmp_path / "refs" / "x.png"
    ref = adapter.generate_character_ref({"name": "X"}, STYLE_GUIDE, out)
    assert ref.error is not None
    assert "failed" in ref.error.lower()
    assert out.exists()


def test_polling_timeout_falls_back(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("FAL_KEY", FAKE_KEY)
    fake = _FakeHttpx(
        {
            "queue.fal.run/fal-ai/nano-banana-2/requests": [
                _FakeResponse(payload={"status": "IN_PROGRESS"}),
            ] * 50,
            "queue.fal.run/fal-ai/nano-banana-2": [
                _FakeResponse(payload={"request_id": "req_timeout_001"}),
            ],
        }
    )
    _install_fake_httpx(monkeypatch, fake)
    monkeypatch.setattr("storyboard.adapters.fal_image.time.sleep", lambda s: None)

    adapter = FalImageAdapter(
        config={"poll_interval_sec": 0.001, "timeout_sec": 0.05}
    )
    out = tmp_path / "refs" / "x.png"
    ref = adapter.generate_character_ref({"name": "X"}, STYLE_GUIDE, out)
    assert ref.error is not None
    assert "timed out" in ref.error
    assert out.exists()


# ----------------------------------------------------------------- helpers


def test_extract_image_url_standard_shape() -> None:
    payload = {"images": [{"url": "https://v3.fal.media/foo.png"}]}
    assert _extract_image_url(payload) == "https://v3.fal.media/foo.png"


def test_extract_image_url_singular_shape() -> None:
    payload = {"image": {"url": "https://v3.fal.media/bar.png"}}
    assert _extract_image_url(payload) == "https://v3.fal.media/bar.png"


def test_extract_image_url_returns_none_on_garbage() -> None:
    assert _extract_image_url({}) is None
    assert _extract_image_url({"video": {"url": "wrong"}}) is None
    assert _extract_image_url(None) is None


# ----------------------------------------------------------------- routing


def test_fal_image_appears_first_in_storyboard_routing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """When FAL_KEY is set, the storyboard pipeline should pick fal-image first."""
    monkeypatch.setenv("FAL_KEY", FAKE_KEY)
    from storyboard.pipeline import select_storyboard_adapter

    adapter = select_storyboard_adapter()
    assert adapter.adapter_id == "fal-image"


# ----------------------------------------------------------------- real fal call


@pytest.mark.fal
def test_real_fal_character_ref(real_fal_key: str, tmp_path: Path) -> None:
    """Hits the real fal.ai nano-banana-2 endpoint. Burns ~$0.04.

    Verifies the character ref PNG lands on disk with non-trivial size
    (>5KB so it's clearly not the placeholder).

    Skips with a clear message if the user's account doesn't have
    nano-banana-2 access (401 Cannot access application).
    """
    adapter = FalImageAdapter(
        config={
            "text_slug": "fal-ai/nano-banana-2",
            "poll_interval_sec": 3,
            "timeout_sec": 240,
        }
    )
    out = tmp_path / "brent.png"
    ref = adapter.generate_character_ref(
        {"name": "Brent", "description": "Mid-40s communications director, dry"},
        "bright stylized 3d animation, cinematic lighting",
        out,
    )
    if ref.error and ("status 401" in ref.error or "Cannot access application" in ref.error):
        pytest.skip(
            f"fal account does not have access to fal-ai/nano-banana-2 on this key. "
            f"Adapter protocol is correct (verified by mocked tests). "
            f"Raw error: {ref.error}"
        )
    assert ref.error is None, f"fal returned: {ref.error}"
    assert out.exists()
    size = out.stat().st_size
    assert size > 5000, f"expected real PNG > 5KB, got {size} bytes"

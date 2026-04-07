"""Tests for the StoryboardAdapter implementations."""
from __future__ import annotations

import base64
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Dict, List

import pytest

from storyboard.adapter import CharacterRef, Frame, StoryboardAdapter
from storyboard.adapters.gemini_image import (
    GeminiImageAdapter,
    _extract_image_bytes,
)
from storyboard.adapters.stub_storyboard import StubStoryboardAdapter


STYLE_GUIDE = "bright stylized 3d animation, cinematic lighting"


def _tiny_png_bytes() -> bytes:
    """Return a tiny 1x1 valid PNG for fake HTTP responses."""
    return (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00"
        b"\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\x9c"
        b"c\x00\x01\x00\x00\x05\x00\x01\x0d\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
    )


def _gemini_response(image_bytes: bytes) -> Dict[str, Any]:
    return {
        "candidates": [
            {
                "content": {
                    "parts": [
                        {
                            "inline_data": {
                                "mime_type": "image/png",
                                "data": base64.b64encode(image_bytes).decode("ascii"),
                            }
                        }
                    ]
                }
            }
        ]
    }


# ----------------------------------------------------------------- stub adapter


def test_stub_adapter_always_available() -> None:
    adapter = StubStoryboardAdapter()
    assert adapter.is_available() is True


def test_stub_character_ref_copies_placeholder(tmp_path: Path) -> None:
    adapter = StubStoryboardAdapter()
    out = tmp_path / "refs" / "brent.png"
    ref = adapter.generate_character_ref(
        {"name": "Brent", "description": "press secretary"}, STYLE_GUIDE, out
    )
    assert isinstance(ref, CharacterRef)
    assert ref.name == "Brent"
    assert ref.slug == "brent"
    assert out.exists()
    assert out.stat().st_size > 0
    assert ref.error is None


def test_stub_frame_copies_placeholder(tmp_path: Path) -> None:
    adapter = StubStoryboardAdapter()
    out = tmp_path / "storyboard" / "beat-01-start.png"
    frame = adapter.generate_frame(
        {"n": 1, "action": "wide shot of beige office"},
        [],
        STYLE_GUIDE,
        out,
    )
    assert isinstance(frame, Frame)
    assert frame.beat_n == 1
    assert out.exists()
    assert out.stat().st_size > 0
    assert frame.error is None


# ----------------------------------------------------------------- gemini adapter


def test_gemini_not_available_without_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    adapter = GeminiImageAdapter()
    assert adapter.is_available() is False


def test_gemini_character_ref_fallback_without_key(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    adapter = GeminiImageAdapter()
    out = tmp_path / "refs" / "brent.png"
    ref = adapter.generate_character_ref(
        {"name": "Brent", "description": "press secretary"}, STYLE_GUIDE, out
    )
    assert ref.error == "GEMINI_API_KEY not set"
    assert out.exists()  # placeholder copied
    assert out.stat().st_size > 0


def test_gemini_frame_fallback_without_key(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    adapter = GeminiImageAdapter()
    out = tmp_path / "storyboard" / "beat-01-start.png"
    frame = adapter.generate_frame(
        {"n": 1, "action": "interior office", "location": "office"},
        [],
        STYLE_GUIDE,
        out,
    )
    assert frame.error == "GEMINI_API_KEY not set"
    assert out.exists()


def test_gemini_parses_image_from_mocked_response(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")
    adapter = GeminiImageAdapter()
    expected = _tiny_png_bytes() + b"REAL_IMAGE_SENTINEL"

    def fake_post(self, parts: List[Dict[str, Any]]) -> Dict[str, Any]:
        return _gemini_response(expected)

    monkeypatch.setattr(GeminiImageAdapter, "_post", fake_post)

    out = tmp_path / "refs" / "brent.png"
    ref = adapter.generate_character_ref(
        {"name": "Brent", "description": "press secretary"}, STYLE_GUIDE, out
    )
    assert ref.error is None
    assert out.read_bytes() == expected


def test_gemini_frame_passes_inline_character_refs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A character ref whose name appears in the beat should be sent as inline_data."""
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")

    ref_path = tmp_path / "refs" / "brent.png"
    ref_path.parent.mkdir(parents=True, exist_ok=True)
    ref_path.write_bytes(b"FAKE_REF_PNG_BYTES")

    character_ref = CharacterRef(
        name="Brent",
        slug="brent",
        path=ref_path,
        prompt="",
        adapter_id="gemini-2.5-flash-image",
    )

    captured_parts: List[List[Dict[str, Any]]] = []
    expected = _tiny_png_bytes()

    def fake_post(self, parts: List[Dict[str, Any]]) -> Dict[str, Any]:
        captured_parts.append(parts)
        return _gemini_response(expected)

    monkeypatch.setattr(GeminiImageAdapter, "_post", fake_post)

    adapter = GeminiImageAdapter()
    beat = {
        "n": 2,
        "action": "Brent freezes in the rigid pose",
        "location": "office",
        "characters": [{"name": "Brent", "description": "press sec"}],
    }
    out = tmp_path / "storyboard" / "beat-02-start.png"
    frame = adapter.generate_frame(beat, [character_ref], STYLE_GUIDE, out)
    assert frame.error is None

    # The first part is text, the second is inline_data with the ref PNG bytes.
    assert len(captured_parts) == 1
    parts = captured_parts[0]
    assert parts[0].get("text")
    assert any("inline_data" in p for p in parts[1:])
    inline = next(p for p in parts if "inline_data" in p)
    assert inline["inline_data"]["mime_type"] == "image/png"
    decoded = base64.b64decode(inline["inline_data"]["data"])
    assert decoded == b"FAKE_REF_PNG_BYTES"


def test_gemini_frame_excludes_unrelated_character_refs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")
    ref_path = tmp_path / "refs" / "someone-else.png"
    ref_path.parent.mkdir(parents=True, exist_ok=True)
    ref_path.write_bytes(b"UNRELATED")

    unrelated = CharacterRef(
        name="Marlene",
        slug="marlene",
        path=ref_path,
        prompt="",
        adapter_id="gemini-2.5-flash-image",
    )

    captured: List[List[Dict[str, Any]]] = []

    def fake_post(self, parts: List[Dict[str, Any]]) -> Dict[str, Any]:
        captured.append(parts)
        return _gemini_response(_tiny_png_bytes())

    monkeypatch.setattr(GeminiImageAdapter, "_post", fake_post)

    adapter = GeminiImageAdapter()
    beat = {
        "n": 1,
        "action": "Brent enters",
        "location": "office",
        "characters": [{"name": "Brent", "description": "press sec"}],
    }
    out = tmp_path / "storyboard" / "beat-01-start.png"
    adapter.generate_frame(beat, [unrelated], STYLE_GUIDE, out)
    parts = captured[0]
    # Only the text part — Marlene is not referenced in this beat.
    assert all("inline_data" not in p for p in parts[1:]) or len(parts) == 1


def test_gemini_malformed_response_falls_back(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")

    def fake_post(self, parts: List[Dict[str, Any]]) -> Dict[str, Any]:
        return {"candidates": [{"content": {"parts": [{"text": "sorry no image"}]}}]}

    monkeypatch.setattr(GeminiImageAdapter, "_post", fake_post)

    adapter = GeminiImageAdapter()
    out = tmp_path / "refs" / "brent.png"
    ref = adapter.generate_character_ref(
        {"name": "Brent", "description": "press sec"}, STYLE_GUIDE, out
    )
    assert ref.error is not None
    assert "no image bytes" in ref.error
    assert out.exists()  # placeholder copied
    assert out.stat().st_size > 0


def test_gemini_http_failure_falls_back(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")

    def fake_post(self, parts: List[Dict[str, Any]]) -> Dict[str, Any]:
        raise RuntimeError("boom")

    monkeypatch.setattr(GeminiImageAdapter, "_post", fake_post)

    adapter = GeminiImageAdapter()
    out = tmp_path / "refs" / "brent.png"
    ref = adapter.generate_character_ref(
        {"name": "Brent", "description": "press sec"}, STYLE_GUIDE, out
    )
    assert ref.error is not None
    assert "boom" in ref.error
    assert out.exists()


def test_extract_image_bytes_handles_camelCase_key() -> None:
    payload = {
        "candidates": [
            {
                "content": {
                    "parts": [
                        {
                            "inlineData": {
                                "mimeType": "image/png",
                                "data": base64.b64encode(b"CAMEL").decode("ascii"),
                            }
                        }
                    ]
                }
            }
        ]
    }
    assert _extract_image_bytes(payload) == b"CAMEL"


def test_extract_image_bytes_returns_none_on_empty() -> None:
    assert _extract_image_bytes({}) is None
    assert _extract_image_bytes({"candidates": []}) is None


# ----------------------------------------------------------------- integration


@pytest.mark.gemini
def test_real_gemini_image_api(tmp_path: Path) -> None:
    """Hits the real Google AI Studio Gemini image API.

    Requires GEMINI_API_KEY. Skipped by default.
    """
    import os as _os
    if not _os.environ.get("GEMINI_API_KEY"):
        pytest.skip("GEMINI_API_KEY not set")

    adapter = GeminiImageAdapter()
    out = tmp_path / "refs" / "brent.png"
    ref = adapter.generate_character_ref(
        {"name": "Brent", "description": "Mid-40s communications director"},
        STYLE_GUIDE,
        out,
    )
    assert ref.error is None, f"gemini returned an error: {ref.error}"
    assert out.exists()
    assert out.stat().st_size > 50_000, "real PNGs should be >50KB"

"""Tests for the CriticAdapter implementations.

Default runs only exercise the stub + mocked HTTP — no real API tokens
spent. The `@pytest.mark.critic` marker is reserved for future opt-in
real-API tests; none ship with Phase 6.
"""
from __future__ import annotations

import base64
import json
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Dict, List

import pytest

from critic.adapter import CriticAdapter, ShotReport, SketchCritique
from critic.adapters.gemini_video import GeminiVideoCritic
from critic.adapters.stub_critic import StubCritic


# A handful of bytes that pass our "non-empty file" sanity checks.
TINY_MP4 = b"\x00\x00\x00\x18ftypisom\x00\x00\x02\x00isomiso2mp41\x00\x00\x00\x08mdat"
TINY_PNG = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\x9cc\x00\x01"
    b"\x00\x00\x05\x00\x01\x0d\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
)


def _mp4(tmp_path: Path, name: str = "clip.mp4") -> Path:
    p = tmp_path / name
    p.write_bytes(TINY_MP4)
    return p


def _png(tmp_path: Path, name: str = "frame.png") -> Path:
    p = tmp_path / name
    p.write_bytes(TINY_PNG)
    return p


# ----------------------------------------------------------------- stub critic


def test_stub_always_available_and_passes_shot(tmp_path: Path) -> None:
    adapter = StubCritic()
    assert adapter.is_available() is True
    report = adapter.check_shot(
        clip_path=_mp4(tmp_path),
        expected_frame=_png(tmp_path),
        character_refs=[],
        beat_metadata={"n": 2, "action": "x"},
    )
    assert isinstance(report, ShotReport)
    assert report.passed is True
    assert report.beat_n == 2
    assert report.adapter_id == "stub-critic-v1"


def test_stub_critique_returns_full_report(tmp_path: Path) -> None:
    adapter = StubCritic()
    critique = adapter.critique_sketch(
        final_cut_path=_mp4(tmp_path),
        sketch_metadata={"sketch_id": "sk-stub-001", "logline": "x"},
    )
    assert isinstance(critique, SketchCritique)
    assert critique.sketch_id == "sk-stub-001"
    assert critique.is_funny is True
    assert critique.overall_score >= 1
    assert "comedic_timing" in critique.axes
    assert critique.fix_suggestions
    assert critique.adapter_id == "stub-critic-v1"


# ----------------------------------------------------------------- gemini critic


class FakeResponse:
    def __init__(self, payload: Any = None, status_code: int = 200) -> None:
        self._payload = payload
        self.status_code = status_code
        self.text = json.dumps(payload) if payload is not None else ""

    def json(self) -> Any:
        return self._payload


def _patch_httpx(monkeypatch: pytest.MonkeyPatch, response: Any) -> Dict[str, Any]:
    """Replace `import httpx` inside the gemini adapter module with a fake."""
    captured: Dict[str, Any] = {"calls": []}

    def post(url: str, **kwargs: Any) -> Any:
        captured["calls"].append({"url": url, "kwargs": kwargs})
        if isinstance(response, Exception):
            raise response
        return response

    fake_module = SimpleNamespace(post=post)
    monkeypatch.setitem(sys.modules, "httpx", fake_module)
    return captured


def _gemini_text_response(text: str) -> Dict[str, Any]:
    return {
        "candidates": [
            {
                "content": {
                    "parts": [{"text": text}],
                }
            }
        ]
    }


def test_gemini_unavailable_without_key(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    adapter = GeminiVideoCritic()
    assert adapter.is_available() is False
    report = adapter.check_shot(
        clip_path=_mp4(tmp_path),
        expected_frame=_png(tmp_path),
        character_refs=[],
        beat_metadata={"n": 1},
    )
    # Defaults to passed=True so the retry loop doesn't fire on missing creds.
    assert report.passed is True
    assert report.error == "GEMINI_API_KEY not set"


def test_gemini_shot_check_happy_path(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")
    payload = _gemini_text_response(
        json.dumps(
            {
                "passed": False,
                "score": 3,
                "issues": ["face morphs at 1.2s"],
                "suggestions": ["regenerate with stricter character ref"],
            }
        )
    )
    captured = _patch_httpx(monkeypatch, FakeResponse(payload=payload))

    adapter = GeminiVideoCritic()
    report = adapter.check_shot(
        clip_path=_mp4(tmp_path),
        expected_frame=_png(tmp_path),
        character_refs=[],
        beat_metadata={
            "n": 5,
            "action": "Brent freezes",
            "camera": "close-up",
            "characters": [{"name": "Brent", "description": "press sec"}],
        },
    )
    assert report.error is None
    assert report.passed is False
    assert report.score == 3
    assert "face morphs at 1.2s" in report.issues
    assert report.suggestions == ["regenerate with stricter character ref"]
    # Verify the request actually carried both the text prompt and the inline video bytes.
    body = captured["calls"][0]["kwargs"]["json"]
    parts = body["contents"][0]["parts"]
    assert any("text" in p for p in parts)
    assert any("inline_data" in p and p["inline_data"]["mime_type"] == "video/mp4" for p in parts)


def test_gemini_shot_check_request_failure_returns_passed_true(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Infrastructure errors must default to passed=True so we don't loop."""
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")
    _patch_httpx(monkeypatch, FakeResponse(payload={"error": "x"}, status_code=500))

    adapter = GeminiVideoCritic()
    report = adapter.check_shot(
        clip_path=_mp4(tmp_path),
        expected_frame=_png(tmp_path),
        character_refs=[],
        beat_metadata={"n": 1},
    )
    assert report.passed is True
    assert report.error is not None
    assert "status 500" in report.error


def test_gemini_shot_check_malformed_inner_json(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")
    _patch_httpx(monkeypatch, FakeResponse(payload=_gemini_text_response("not json")))
    adapter = GeminiVideoCritic()
    report = adapter.check_shot(
        clip_path=_mp4(tmp_path),
        expected_frame=_png(tmp_path),
        character_refs=[],
        beat_metadata={"n": 1},
    )
    assert report.passed is True
    assert report.error is not None


def test_gemini_critique_sketch_happy_path(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")
    payload = _gemini_text_response(
        json.dumps(
            {
                "overall_score": 8,
                "is_funny": True,
                "axes": {
                    "comedic_timing": 8,
                    "pacing": 7,
                    "punchline_landing": 9,
                    "audio_clarity": 6,
                    "character_consistency": 7,
                },
                "issues": ["audio drops out at 0:18"],
                "fix_suggestions": ["raise the music bed in the final beat"],
                "verdict": "the twist lands but the audio mix is muddy",
            }
        )
    )
    _patch_httpx(monkeypatch, FakeResponse(payload=payload))

    adapter = GeminiVideoCritic()
    critique = adapter.critique_sketch(
        _mp4(tmp_path),
        {
            "sketch_id": "sk-test-critic-001",
            "logline": "intern types statement",
            "tone": "dry workplace",
            "twist": "they all freeze",
            "beat_count": 5,
            "target_length_sec": 30,
        },
    )
    assert critique.error is None
    assert critique.overall_score == 8
    assert critique.is_funny is True
    assert critique.axes["punchline_landing"] == 9
    assert "audio drops out at 0:18" in critique.issues
    assert critique.fix_suggestions == ["raise the music bed in the final beat"]
    assert "twist lands" in critique.verdict


def test_gemini_critique_request_failure_falls_back(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")
    _patch_httpx(monkeypatch, RuntimeError("boom"))

    adapter = GeminiVideoCritic()
    critique = adapter.critique_sketch(
        _mp4(tmp_path),
        {"sketch_id": "sk-test-critic-002"},
    )
    assert critique.error is not None
    assert "boom" in critique.error


def test_gemini_with_missing_clip_returns_error(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")
    adapter = GeminiVideoCritic()
    report = adapter.check_shot(
        clip_path=tmp_path / "doesnotexist.mp4",
        expected_frame=_png(tmp_path),
        character_refs=[],
        beat_metadata={"n": 1},
    )
    assert report.passed is True
    assert report.error is not None
    assert "missing" in report.error


# ----------------------------------------------------------------- claude critic
# (CLI presence is tested by the framework — full real-CLI runs are gated
# behind the `llm` marker. Here we only verify the unavailable / missing-CLI
# fallback path so the suite stays offline.)


def test_claude_frame_unavailable_without_cli(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    from critic.adapters.claude_frame import ClaudeFrameCritic

    monkeypatch.setattr(
        "critic.adapters.claude_frame.shutil.which",
        lambda name: None,
    )
    adapter = ClaudeFrameCritic()
    assert adapter.is_available() is False

    report = adapter.check_shot(
        clip_path=_mp4(tmp_path),
        expected_frame=_png(tmp_path),
        character_refs=[],
        beat_metadata={"n": 1},
    )
    assert report.passed is True
    assert report.error == "claude CLI not on PATH"

    critique = adapter.critique_sketch(
        _mp4(tmp_path),
        {"sketch_id": "sk-test-claude-critic-001"},
    )
    assert critique.error == "claude CLI not on PATH"


def test_claude_frame_handles_missing_clip(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    from critic.adapters.claude_frame import ClaudeFrameCritic

    monkeypatch.setattr(
        "critic.adapters.claude_frame.shutil.which",
        lambda name: "/fake/claude",
    )
    adapter = ClaudeFrameCritic()
    report = adapter.check_shot(
        clip_path=tmp_path / "missing.mp4",
        expected_frame=_png(tmp_path),
        character_refs=[],
        beat_metadata={"n": 1},
    )
    assert report.passed is True
    assert report.error is not None


# ----------------------------------------------------------------- contract


@pytest.mark.parametrize(
    "factory",
    [
        lambda: StubCritic(),
        lambda: GeminiVideoCritic(),
    ],
)
def test_critic_contract_returns_dataclasses(
    factory, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Every critic adapter must satisfy the ABC and never raise."""
    for env_var in ("GEMINI_API_KEY",):
        monkeypatch.delenv(env_var, raising=False)
    adapter = factory()
    assert hasattr(adapter, "adapter_id")
    report = adapter.check_shot(
        clip_path=_mp4(tmp_path),
        expected_frame=_png(tmp_path),
        character_refs=[],
        beat_metadata={"n": 1},
    )
    assert isinstance(report, ShotReport)
    critique = adapter.critique_sketch(
        _mp4(tmp_path),
        {"sketch_id": "sk-contract"},
    )
    assert isinstance(critique, SketchCritique)

"""Tests for the Phase 9 OpenRouterAdapter (idea_factory layer).

Mocked-HTTP suite modeled on Phase 8's `test_fal_unified_adapter.py`:
every test either injects a fake `httpx.post` via `sys.modules["httpx"]`
or manipulates `OPENROUTER_API_KEY` through monkeypatch. The single
opt-in `@pytest.mark.openrouter` test uses the `real_openrouter_key`
fixture from conftest.py and hits the real OpenRouter chat-completions
endpoint.
"""
from __future__ import annotations

import json
import sys
from types import SimpleNamespace
from typing import Any, Dict, List, Optional

import pytest

from idea_factory.adapter import PremiseResult
from idea_factory.adapters.openrouter import (
    ENV_KEY,
    OPENROUTER_URL,
    OpenRouterAdapter,
)


FAKE_KEY = "sk-or-fake-000"


SIGNAL = {
    "signal_id": "test-or-signal-001",
    "id": "test-or-signal-001",
    "title": "A raccoon briefly hosts a morning news show",
    "source": "reddit",
    "source_url": "https://example.com/r/2",
    "summary": "The raccoon read one paragraph before the anchor returned.",
}


def _premise_dict(prefix: str = "fake") -> Dict[str, Any]:
    return {
        "logline": f"{prefix} logline about a raccoon anchor",
        "synopsis": f"{prefix} synopsis with three sentences. " * 2,
        "tone": "deadpan",
        "target_length_sec": 30,
        "characters": [{"name": "Raccoon", "description": "new hire"}],
        "twist": f"{prefix} twist",
    }


def _openrouter_envelope(inner_text: str) -> Dict[str, Any]:
    """Mimic the OpenAI-compatible chat.completions response shape."""
    return {
        "id": "gen-fake-001",
        "object": "chat.completion",
        "created": 1712345678,
        "model": "openai/gpt-5",
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": inner_text},
                "finish_reason": "stop",
            }
        ],
        "usage": {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30},
    }


# ----------------------------------------------------------------- fakes


class _FakeResponse:
    def __init__(
        self,
        payload: Any = None,
        status_code: int = 200,
        text: str = "",
    ) -> None:
        self._payload = payload
        self.status_code = status_code
        self.text = text or (json.dumps(payload) if payload is not None else "")

    def json(self) -> Any:
        if self._payload is None:
            raise ValueError("no json payload")
        return self._payload


class _FakeHttpx:
    """Captures every POST. Returns a queue of responses in FIFO order."""

    ConnectError = type("ConnectError", (Exception,), {})

    def __init__(
        self,
        responses: Optional[List[_FakeResponse]] = None,
        raise_exc: Optional[Exception] = None,
    ) -> None:
        self.responses = list(responses or [])
        self.raise_exc = raise_exc
        self.calls: List[Dict[str, Any]] = []

    def post(self, url: str, **kwargs: Any) -> _FakeResponse:
        self.calls.append({"url": url, "kwargs": kwargs})
        if self.raise_exc is not None:
            raise self.raise_exc
        if not self.responses:
            return _FakeResponse(status_code=500, text="no more responses")
        return self.responses.pop(0)


def _install_fake_httpx(monkeypatch: pytest.MonkeyPatch, fake: _FakeHttpx) -> _FakeHttpx:
    fake_module = SimpleNamespace(post=fake.post, ConnectError=_FakeHttpx.ConnectError)
    monkeypatch.setitem(sys.modules, "httpx", fake_module)
    return fake


# ----------------------------------------------------------------- env detection


def test_is_available_when_env_set(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(ENV_KEY, FAKE_KEY)
    assert OpenRouterAdapter().is_available() is True


def test_is_available_when_env_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(ENV_KEY, raising=False)
    assert OpenRouterAdapter().is_available() is False


# ----------------------------------------------------------------- happy path


def _three_premises_payload() -> Dict[str, Any]:
    return {
        "premises": [
            _premise_dict("one"),
            _premise_dict("two"),
            _premise_dict("three"),
        ]
    }


def test_generate_happy_path_gpt5(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(ENV_KEY, FAKE_KEY)
    fake = _install_fake_httpx(
        monkeypatch,
        _FakeHttpx(
            responses=[
                _FakeResponse(
                    payload=_openrouter_envelope(json.dumps(_three_premises_payload()))
                )
            ]
        ),
    )

    adapter = OpenRouterAdapter(
        config={"id": "gpt-5", "api_model": "openai/gpt-5", "timeout_sec": 30}
    )
    result = adapter.generate(SIGNAL, "PROMPT", n_premises=3)

    assert isinstance(result, PremiseResult)
    assert result.error is None
    assert result.model_id == "gpt-5"
    assert len(result.premises) == 3
    assert result.premises[0].logline.startswith("one")
    assert fake.calls[0]["url"] == OPENROUTER_URL


def test_generate_happy_path_gemini(monkeypatch: pytest.MonkeyPatch) -> None:
    """Per-slug identity: same adapter class, different `id` → model_id sticks."""
    monkeypatch.setenv(ENV_KEY, FAKE_KEY)
    _install_fake_httpx(
        monkeypatch,
        _FakeHttpx(
            responses=[
                _FakeResponse(
                    payload=_openrouter_envelope(json.dumps(_three_premises_payload()))
                )
            ]
        ),
    )

    adapter = OpenRouterAdapter(
        config={
            "id": "gemini-2.5-pro",
            "api_model": "google/gemini-2.5-pro",
            "timeout_sec": 30,
        }
    )
    result = adapter.generate(SIGNAL, "PROMPT", n_premises=3)

    assert result.error is None
    assert result.model_id == "gemini-2.5-pro"
    assert len(result.premises) == 3


# ----------------------------------------------------------------- request shape


def test_generate_uses_bearer_auth(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(ENV_KEY, FAKE_KEY)
    fake = _install_fake_httpx(
        monkeypatch,
        _FakeHttpx(
            responses=[
                _FakeResponse(
                    payload=_openrouter_envelope(json.dumps(_three_premises_payload()))
                )
            ]
        ),
    )

    adapter = OpenRouterAdapter(
        config={"id": "gpt-5", "api_model": "openai/gpt-5"}
    )
    adapter.generate(SIGNAL, "PROMPT", n_premises=3)

    headers = fake.calls[0]["kwargs"]["headers"]
    assert headers["Authorization"] == f"Bearer {FAKE_KEY}"
    assert headers["HTTP-Referer"] == "https://github.com/seanross237/ai_vids_virality"
    assert headers["X-Title"] == "ai_vids_virality"
    assert headers["Content-Type"] == "application/json"


def test_generate_passes_system_and_user_messages(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(ENV_KEY, FAKE_KEY)
    fake = _install_fake_httpx(
        monkeypatch,
        _FakeHttpx(
            responses=[
                _FakeResponse(
                    payload=_openrouter_envelope(json.dumps(_three_premises_payload()))
                )
            ]
        ),
    )

    adapter = OpenRouterAdapter(
        config={"id": "gpt-5", "api_model": "openai/gpt-5"}
    )
    adapter.generate(SIGNAL, "THE-PROMPT-TEXT", n_premises=3)

    body = fake.calls[0]["kwargs"]["json"]
    assert body["messages"][0]["role"] == "system"
    assert body["messages"][1]["role"] == "user"
    assert body["messages"][1]["content"] == "THE-PROMPT-TEXT"
    assert body["temperature"] == 0.7


def test_generate_passes_response_format_json_object(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(ENV_KEY, FAKE_KEY)
    fake = _install_fake_httpx(
        monkeypatch,
        _FakeHttpx(
            responses=[
                _FakeResponse(
                    payload=_openrouter_envelope(json.dumps(_three_premises_payload()))
                )
            ]
        ),
    )

    adapter = OpenRouterAdapter(
        config={"id": "gpt-5", "api_model": "openai/gpt-5"}
    )
    adapter.generate(SIGNAL, "PROMPT", n_premises=3)

    body = fake.calls[0]["kwargs"]["json"]
    assert body["response_format"] == {"type": "json_object"}


def test_generate_passes_api_model(monkeypatch: pytest.MonkeyPatch) -> None:
    """The `model` field in the request body is the OpenRouter slug, NOT the registry id."""
    monkeypatch.setenv(ENV_KEY, FAKE_KEY)
    fake = _install_fake_httpx(
        monkeypatch,
        _FakeHttpx(
            responses=[
                _FakeResponse(
                    payload=_openrouter_envelope(json.dumps(_three_premises_payload()))
                )
            ]
        ),
    )

    adapter = OpenRouterAdapter(
        config={"id": "gpt-5", "api_model": "openai/gpt-5"}
    )
    adapter.generate(SIGNAL, "PROMPT", n_premises=3)

    body = fake.calls[0]["kwargs"]["json"]
    assert body["model"] == "openai/gpt-5"


# ----------------------------------------------------------------- error paths


def test_generate_503_returns_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(ENV_KEY, FAKE_KEY)
    _install_fake_httpx(
        monkeypatch,
        _FakeHttpx(
            responses=[_FakeResponse(status_code=503, text="service unavailable")]
        ),
    )

    adapter = OpenRouterAdapter(config={"id": "gpt-5", "api_model": "openai/gpt-5"})
    result = adapter.generate(SIGNAL, "PROMPT", n_premises=3)

    assert result.error is not None
    assert "openrouter status 503" in result.error
    assert result.premises == []


def test_generate_network_error_returns_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(ENV_KEY, FAKE_KEY)
    _install_fake_httpx(
        monkeypatch,
        _FakeHttpx(raise_exc=_FakeHttpx.ConnectError("connection refused")),
    )

    adapter = OpenRouterAdapter(config={"id": "gpt-5", "api_model": "openai/gpt-5"})
    result = adapter.generate(SIGNAL, "PROMPT", n_premises=3)

    assert result.error is not None
    assert "openrouter request failed" in result.error
    assert result.premises == []


def test_generate_missing_choices_returns_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(ENV_KEY, FAKE_KEY)
    _install_fake_httpx(
        monkeypatch,
        _FakeHttpx(
            responses=[_FakeResponse(payload={"id": "gen-broken-001", "object": "chat.completion"})]
        ),
    )

    adapter = OpenRouterAdapter(config={"id": "gpt-5", "api_model": "openai/gpt-5"})
    result = adapter.generate(SIGNAL, "PROMPT", n_premises=3)

    assert result.error is not None
    assert "missing choices" in result.error


def test_generate_non_json_content_returns_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(ENV_KEY, FAKE_KEY)
    _install_fake_httpx(
        monkeypatch,
        _FakeHttpx(
            responses=[
                _FakeResponse(payload=_openrouter_envelope("sorry, can't help"))
            ]
        ),
    )

    adapter = OpenRouterAdapter(config={"id": "gpt-5", "api_model": "openai/gpt-5"})
    result = adapter.generate(SIGNAL, "PROMPT", n_premises=3)

    assert result.error is not None
    assert "did not contain a JSON object" in result.error


def test_generate_empty_premise_list_returns_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(ENV_KEY, FAKE_KEY)
    _install_fake_httpx(
        monkeypatch,
        _FakeHttpx(
            responses=[
                _FakeResponse(
                    payload=_openrouter_envelope(json.dumps({"premises": []}))
                )
            ]
        ),
    )

    adapter = OpenRouterAdapter(config={"id": "gpt-5", "api_model": "openai/gpt-5"})
    result = adapter.generate(SIGNAL, "PROMPT", n_premises=3)

    assert result.error is not None
    assert "no premises" in result.error


def test_generate_truncates_to_n_premises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(ENV_KEY, FAKE_KEY)
    many = {
        "premises": [
            _premise_dict("one"),
            _premise_dict("two"),
            _premise_dict("three"),
            _premise_dict("four"),
            _premise_dict("five"),
        ]
    }
    _install_fake_httpx(
        monkeypatch,
        _FakeHttpx(
            responses=[_FakeResponse(payload=_openrouter_envelope(json.dumps(many)))]
        ),
    )

    adapter = OpenRouterAdapter(config={"id": "gpt-5", "api_model": "openai/gpt-5"})
    result = adapter.generate(SIGNAL, "PROMPT", n_premises=2)

    assert result.error is None
    assert len(result.premises) == 2


def test_generate_stamps_signal_id_and_duration(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(ENV_KEY, FAKE_KEY)
    _install_fake_httpx(
        monkeypatch,
        _FakeHttpx(
            responses=[
                _FakeResponse(
                    payload=_openrouter_envelope(json.dumps(_three_premises_payload()))
                )
            ]
        ),
    )

    adapter = OpenRouterAdapter(config={"id": "gpt-5", "api_model": "openai/gpt-5"})
    result = adapter.generate(SIGNAL, "PROMPT", n_premises=3)

    assert result.signal_id == "test-or-signal-001"
    assert result.duration_ms >= 0  # the request is mocked so this can legitimately be 0


def test_generate_when_env_missing_returns_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """No env key → hard error, no httpx call, no stub fallback."""
    monkeypatch.delenv(ENV_KEY, raising=False)
    fake = _install_fake_httpx(monkeypatch, _FakeHttpx())

    adapter = OpenRouterAdapter(config={"id": "gpt-5", "api_model": "openai/gpt-5"})
    result = adapter.generate(SIGNAL, "PROMPT", n_premises=3)

    assert result.error is not None
    assert "OPENROUTER_API_KEY not set" in result.error
    assert result.premises == []
    assert fake.calls == []  # adapter short-circuited before touching httpx


# ----------------------------------------------------------------- real API


@pytest.mark.openrouter
def test_real_openrouter_gpt5(real_openrouter_key: str) -> None:
    """Hits the real OpenRouter chat-completions endpoint at `openai/gpt-5`.

    Skips with a clear message if the user's OpenRouter account doesn't
    have access to the slug (401 / 402 / 404), analogous to Phase 8's
    fal opt-in skip path. Any other error fails the test loudly.
    """
    adapter = OpenRouterAdapter(
        config={
            "id": "gpt-5",
            "api_model": "openai/gpt-5",
            "timeout_sec": 120,
        }
    )
    assert adapter.is_available() is True

    tiny_signal = {
        "signal_id": "or-live-test-001",
        "id": "or-live-test-001",
        "title": "A pigeon wins a spelling bee",
        "source": "test",
        "source_url": "https://example.com/t",
        "summary": "The pigeon only knew one word.",
    }
    prompt = (
        "Return strict JSON of the form {\"premises\": [ {\"logline\": str, "
        "\"synopsis\": str, \"tone\": str, \"target_length_sec\": int, "
        "\"characters\": [], \"twist\": str} ]}. Produce exactly 1 premise "
        "for the following news item: 'A pigeon wins a spelling bee.'"
    )

    result = adapter.generate(tiny_signal, prompt, n_premises=1)

    if result.error and any(
        tag in result.error
        for tag in ("status 401", "status 402", "status 403", "status 404")
    ):
        pytest.skip(
            f"openrouter account does not have access to openai/gpt-5 on this key — "
            f"the adapter reached the chat-completions endpoint cleanly and the "
            f"protocol is correct, but the live slug is gated. Refresh the key or "
            f"switch slugs. Raw error: {result.error}"
        )
    assert result.error is None, f"openrouter returned an error: {result.error}"
    assert len(result.premises) >= 1
    assert result.duration_ms > 0
    assert result.raw_response is not None

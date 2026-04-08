"""Tests for the ModelAdapter implementations.

The default test runs are offline. The Claude CLI integration test is
marked `@pytest.mark.llm` so it only runs when the user opts in via
`pytest -m llm`. That test really spawns the `claude` CLI and asserts a
real PremiseResult comes back.
"""
from __future__ import annotations

import json
import shutil
from typing import Any, Dict, List
from types import SimpleNamespace

import pytest

from idea_factory.adapter import ModelAdapter, Premise, PremiseResult
from idea_factory.adapters._json_parsing import (
    extract_first_json_object,
    find_premise_list,
    strip_code_fences,
)
from idea_factory.adapters.claude_cli import ClaudeCLIAdapter
from idea_factory.adapters.gemini_stub import GeminiAdapter
from idea_factory.adapters.openai_stub import OpenAIAdapter


SIGNAL = {
    "signal_id": "test-signal-001",
    "id": "test-signal-001",
    "title": "Senator caught using spoon as wifi antenna in committee hearing",
    "source": "reddit",
    "source_url": "https://example.com/r/1",
    "summary": "An aide rolled tape and handed it back. The senator continued.",
}


def _claude_envelope(inner_text: str) -> str:
    return json.dumps(
        {
            "result": inner_text,
            "session_id": "fake-session",
            "total_cost_usd": 0.04,
            "num_turns": 1,
            "model": "claude-opus-4-6",
        }
    )


def _premise_dict(prefix: str = "fake") -> Dict[str, Any]:
    return {
        "logline": f"{prefix} logline about a senator",
        "synopsis": f"{prefix} synopsis with three sentences. " * 2,
        "tone": "dry workplace",
        "target_length_sec": 30,
        "characters": [{"name": "Riley", "description": "intern"}],
        "twist": f"{prefix} twist",
    }


# ----------------------------------------------------------------- json helpers


def test_strip_code_fences_with_fence() -> None:
    assert strip_code_fences("```json\n{\"a\": 1}\n```") == '{"a": 1}'


def test_strip_code_fences_no_fence() -> None:
    assert strip_code_fences('{"a": 1}') == '{"a": 1}'


def test_extract_first_json_object_with_prose() -> None:
    text = 'Sure thing. Here is the JSON: {"premises": [{"logline": "x", "synopsis": "y"}]} and that is it.'
    parsed = extract_first_json_object(text)
    assert parsed is not None
    assert "premises" in parsed


def test_find_premise_list_handles_envelope() -> None:
    payload = {"premises": [_premise_dict("a"), _premise_dict("b")]}
    found = find_premise_list(payload)
    assert len(found) == 2


def test_find_premise_list_handles_nested() -> None:
    payload = {"data": {"output": {"premises": [_premise_dict("c")]}}}
    found = find_premise_list(payload)
    assert len(found) == 1


def test_find_premise_list_handles_bare_list() -> None:
    payload = [_premise_dict("d"), _premise_dict("e")]
    found = find_premise_list(payload)
    assert len(found) == 2


# ----------------------------------------------------------------- claude_cli


class FakeClaudeRunner:
    """Stand-in for `subprocess.run` used by ClaudeCLIAdapter tests."""

    def __init__(self, stdout: str, returncode: int = 0, raises: Exception = None) -> None:
        self.stdout = stdout
        self.returncode = returncode
        self.raises = raises
        self.calls: List[List[str]] = []

    def __call__(self, cmd: List[str], **kwargs: Any) -> Any:
        self.calls.append(cmd)
        if self.raises:
            raise self.raises
        return SimpleNamespace(stdout=self.stdout, stderr="", returncode=self.returncode)


@pytest.fixture()
def claude_adapter_with_fake_runner(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(
        "idea_factory.adapters.claude_cli.shutil.which",
        lambda name: "/fake/claude",
    )

    def make(stdout: str, returncode: int = 0, raises: Exception = None) -> ClaudeCLIAdapter:
        runner = FakeClaudeRunner(stdout=stdout, returncode=returncode, raises=raises)
        monkeypatch.setattr(
            "idea_factory.adapters.claude_cli.subprocess.run",
            runner,
        )
        adapter = ClaudeCLIAdapter(config={"id": "claude-opus", "cli_model": "claude-opus-4-6"})
        adapter._fake_runner = runner  # type: ignore[attr-defined]
        return adapter

    return make


def test_claude_adapter_parses_envelope(claude_adapter_with_fake_runner) -> None:
    inner = json.dumps({"premises": [_premise_dict("envelope")]})
    adapter = claude_adapter_with_fake_runner(_claude_envelope(inner))
    result = adapter.generate(SIGNAL, "prompt", n_premises=3)
    assert result.error is None
    assert result.model_id == "claude-opus"
    assert len(result.premises) == 1
    assert result.premises[0].logline.startswith("envelope")
    assert result.cost_cents == 4  # 0.04 usd -> 4 cents


def test_claude_adapter_strips_markdown_fences(claude_adapter_with_fake_runner) -> None:
    inner = "```json\n" + json.dumps({"premises": [_premise_dict("fenced")]}) + "\n```"
    adapter = claude_adapter_with_fake_runner(_claude_envelope(inner))
    result = adapter.generate(SIGNAL, "prompt")
    assert result.error is None
    assert result.premises[0].logline.startswith("fenced")


def test_claude_adapter_handles_garbage_inner(claude_adapter_with_fake_runner) -> None:
    adapter = claude_adapter_with_fake_runner(_claude_envelope("not json at all"))
    result = adapter.generate(SIGNAL, "prompt")
    assert result.error is not None
    assert result.premises == []


def test_claude_adapter_handles_non_zero_exit(claude_adapter_with_fake_runner) -> None:
    adapter = claude_adapter_with_fake_runner("", returncode=2)
    result = adapter.generate(SIGNAL, "prompt")
    assert result.error is not None
    assert "exit 2" in result.error


def test_claude_adapter_handles_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    import subprocess as sp

    monkeypatch.setattr(
        "idea_factory.adapters.claude_cli.shutil.which",
        lambda name: "/fake/claude",
    )

    def boom(*args: Any, **kwargs: Any) -> Any:
        raise sp.TimeoutExpired(cmd=["claude"], timeout=1)

    monkeypatch.setattr("idea_factory.adapters.claude_cli.subprocess.run", boom)
    adapter = ClaudeCLIAdapter(config={"id": "claude-opus", "timeout_sec": 1})
    result = adapter.generate(SIGNAL, "prompt")
    assert result.error is not None
    assert "timed out" in result.error
    assert result.premises == []


def test_claude_adapter_unavailable_when_no_cli(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("idea_factory.adapters.claude_cli.shutil.which", lambda name: None)
    adapter = ClaudeCLIAdapter(config={"id": "claude-opus"})
    assert adapter.is_available() is False
    result = adapter.generate(SIGNAL, "prompt")
    assert result.error == "claude CLI not on PATH"
    assert result.premises == []


# ----------------------------------------------------------------- openai stub


def test_openai_stub_returns_three_premises_when_no_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    adapter = OpenAIAdapter(config={"id": "gpt-5"})
    assert adapter.is_available() is False
    result = adapter.generate(SIGNAL, "prompt", n_premises=3)
    assert result.error is None
    assert len(result.premises) == 3
    for p in result.premises:
        assert isinstance(p, Premise)
        assert p.logline


def test_openai_stub_premises_are_deterministic(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    adapter = OpenAIAdapter(config={"id": "gpt-5"})
    first = adapter.generate(SIGNAL, "prompt").premises
    second = adapter.generate(SIGNAL, "prompt").premises
    assert [p.logline for p in first] == [p.logline for p in second]


def test_openai_is_available_when_env_set(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "fake-key")
    adapter = OpenAIAdapter(config={"id": "gpt-5"})
    assert adapter.is_available() is True


# ----------------------------------------------------------------- gemini stub


def test_gemini_stub_returns_three_premises_when_no_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    adapter = GeminiAdapter(config={"id": "gemini-2.5-pro"})
    assert adapter.is_available() is False
    result = adapter.generate(SIGNAL, "prompt", n_premises=3)
    assert result.error is None
    assert len(result.premises) == 3


def test_gemini_and_openai_stubs_diverge(monkeypatch: pytest.MonkeyPatch) -> None:
    """The two stubs should produce visibly different premises so the
    side-by-side UI shows variety."""
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    o = OpenAIAdapter(config={"id": "gpt-5"}).generate(SIGNAL, "prompt").premises
    g = GeminiAdapter(config={"id": "gemini-2.5-pro"}).generate(SIGNAL, "prompt").premises
    assert [p.logline for p in o] != [p.logline for p in g]


# ----------------------------------------------------------------- contract


@pytest.mark.parametrize(
    "factory",
    [
        lambda: OpenAIAdapter(config={"id": "gpt-5"}),
        lambda: GeminiAdapter(config={"id": "gemini-2.5-pro"}),
    ],
)
def test_stub_adapter_contract(factory, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    adapter: ModelAdapter = factory()
    result = adapter.generate(SIGNAL, "prompt", n_premises=2)
    assert isinstance(result, PremiseResult)
    assert result.signal_id == SIGNAL["signal_id"]
    assert result.model_id  # set
    assert result.error is None
    assert len(result.premises) >= 1
    for p in result.premises:
        assert isinstance(p, Premise)
        assert p.target_length_sec == 30


# ----------------------------------------------------------------- LLM integration


@pytest.mark.llm
def test_real_claude_call_returns_premises() -> None:
    """Spawns the real `claude` CLI on a tiny hardcoded signal.

    Runs only with `pytest -m llm`. Requires Claude CLI installed and
    authenticated. Burns real tokens — keep n_premises small.
    """
    if not shutil.which("claude"):
        pytest.skip("claude CLI not on PATH")

    from idea_factory.factory import (
        _format_prompt,
        _load_lens_excerpt,
        _load_prompt_template,
    )

    adapter = ClaudeCLIAdapter(
        config={
            "id": "claude-opus",
            "cli_model": "claude-opus-4-6",
            "timeout_sec": 240,
            "max_turns": 1,
        }
    )
    template = _load_prompt_template()
    lens = _load_lens_excerpt()
    prompt = _format_prompt(template, SIGNAL, n=3, lens=lens)
    result = adapter.generate(SIGNAL, prompt, n_premises=3)
    assert result.error is None, f"claude returned an error: {result.error}"
    assert len(result.premises) >= 1
    # Save the real output so the demo report can quote it.
    out_path = pytest._real_claude_premise_capture = result  # type: ignore[attr-defined]
    for p in result.premises:
        assert p.logline
        assert p.synopsis
        assert p.tone

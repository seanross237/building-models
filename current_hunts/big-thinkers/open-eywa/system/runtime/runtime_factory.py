from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from .cli_runtime_base import CliRuntimeConfig
from .claude_cli_runtime import ClaudeCliRuntime
from .codex_cli_runtime import CodexCliRuntime
from .openrouter_runtime import OpenRouterRuntime, OpenRouterRuntimeConfig
from .runtime_interface import RuntimeAdapter

RuntimeProvider = Literal["openrouter", "claude", "codex"]

LIVE_CANARY_DEFAULT_MODEL = "openai/gpt-4.1-mini"

LIVE_CANARY_ROLE_ORDER: tuple[str, ...] = (
    "librarian",
    "planner",
    "plan-reviewer",
    "plan-decider",
    "worker",
    "mid-plan-evaluator",
    "synthesizer",
)


def default_live_canary_role_models(model_name: str = LIVE_CANARY_DEFAULT_MODEL) -> dict[str, str]:
    if not isinstance(model_name, str) or not model_name.strip():
        raise ValueError("model_name must be a non-empty string.")
    return {role: model_name.strip() for role in LIVE_CANARY_ROLE_ORDER}


# --- Provider-neutral settings and builder ---


@dataclass(frozen=True)
class LiveRuntimeSettings:
    """Provider-neutral settings for live runtime construction."""

    runtime_provider: RuntimeProvider = "openrouter"
    model_name: str = LIVE_CANARY_DEFAULT_MODEL
    max_turns: int = 6
    max_tokens: int = 1600
    temperature: float = 0.0
    timeout_seconds: int = 300
    # OpenRouter-specific
    referer_url: str | None = None
    title: str | None = "Open-Eywa Canary"
    fetch_generation_stats: bool = True


def build_live_runtime(
    settings: LiveRuntimeSettings | None = None,
) -> RuntimeAdapter:
    """Build a runtime adapter for the selected provider."""
    effective = settings or LiveRuntimeSettings()
    role_models = default_live_canary_role_models(effective.model_name)

    if effective.runtime_provider == "openrouter":
        config = OpenRouterRuntimeConfig.from_environment(
            default_models=role_models,
            referer_url=effective.referer_url,
            title=effective.title,
            fetch_generation_stats=effective.fetch_generation_stats,
            max_turns=effective.max_turns,
            max_tokens=effective.max_tokens,
            temperature=effective.temperature,
        )
        return OpenRouterRuntime(config)

    if effective.runtime_provider == "claude":
        config = CliRuntimeConfig(
            default_models=role_models,
            max_turns=effective.max_turns,
            timeout_seconds=effective.timeout_seconds,
        )
        return ClaudeCliRuntime(config)

    if effective.runtime_provider == "codex":
        config = CliRuntimeConfig(
            default_models=role_models,
            max_turns=effective.max_turns,
            timeout_seconds=effective.timeout_seconds,
        )
        return CodexCliRuntime(config)

    raise ValueError(f"Unknown runtime provider: {effective.runtime_provider!r}")


# --- Legacy OpenRouter-only builder (kept for backwards compatibility) ---


@dataclass(frozen=True)
class LiveCanaryRuntimeSettings:
    model_name: str = LIVE_CANARY_DEFAULT_MODEL
    referer_url: str | None = None
    title: str | None = "Open-Eywa Canary"
    fetch_generation_stats: bool = True
    max_turns: int = 6
    max_tokens: int = 1600
    temperature: float = 0.0


def build_openrouter_runtime_for_live_canary(
    settings: LiveCanaryRuntimeSettings | None = None,
) -> OpenRouterRuntime:
    effective = settings or LiveCanaryRuntimeSettings()
    config = OpenRouterRuntimeConfig.from_environment(
        default_models=default_live_canary_role_models(effective.model_name),
        referer_url=effective.referer_url,
        title=effective.title,
        fetch_generation_stats=effective.fetch_generation_stats,
        max_turns=effective.max_turns,
        max_tokens=effective.max_tokens,
        temperature=effective.temperature,
    )
    return OpenRouterRuntime(config)

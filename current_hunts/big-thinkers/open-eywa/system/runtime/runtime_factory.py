from __future__ import annotations

from dataclasses import dataclass

from .openrouter_runtime import OpenRouterRuntime, OpenRouterRuntimeConfig

LIVE_CANARY_DEFAULT_MODEL = "google/gemini-2.5-flash-lite"

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

"""Runtime seam for the Open-Eywa rebuild."""

from .openrouter_client import (
    OpenRouterChatClient,
    OpenRouterClientConfig,
    OpenRouterClientError,
)
from .openrouter_runtime import (
    OpenRouterRuntime,
    OpenRouterRuntimeConfig,
    OpenRouterRuntimeError,
)
from .prompt_loader import PromptBundle, PromptLoader, PromptLoaderError
from .runtime_factory import (
    LIVE_CANARY_DEFAULT_MODEL,
    LIVE_CANARY_ROLE_ORDER,
    LiveCanaryRuntimeSettings,
    build_openrouter_runtime_for_live_canary,
    default_live_canary_role_models,
)
from .runtime_interface import (
    RUN_EXIT_REASONS,
    RuntimeAdapter,
    RuntimeContractError,
    RuntimeRequest,
    RuntimeResult,
)
from .simulated_runtime import SimulatedRuntime, SimulatedRuntimeError
from .simulation_scenarios import (
    SCENARIO_ACTION_TYPES,
    ScenarioAction,
    ScenarioScenarioError,
    SimulatedScenario,
    load_scenario,
)

__all__ = [
    "RUN_EXIT_REASONS",
    "OpenRouterChatClient",
    "OpenRouterClientConfig",
    "OpenRouterClientError",
    "OpenRouterRuntime",
    "OpenRouterRuntimeConfig",
    "OpenRouterRuntimeError",
    "LIVE_CANARY_DEFAULT_MODEL",
    "LIVE_CANARY_ROLE_ORDER",
    "LiveCanaryRuntimeSettings",
    "PromptBundle",
    "PromptLoader",
    "PromptLoaderError",
    "RuntimeAdapter",
    "RuntimeContractError",
    "RuntimeRequest",
    "RuntimeResult",
    "build_openrouter_runtime_for_live_canary",
    "default_live_canary_role_models",
    "SCENARIO_ACTION_TYPES",
    "ScenarioAction",
    "ScenarioScenarioError",
    "SimulatedRuntime",
    "SimulatedRuntimeError",
    "SimulatedScenario",
    "load_scenario",
]

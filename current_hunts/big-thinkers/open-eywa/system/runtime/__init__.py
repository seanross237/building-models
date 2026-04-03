"""Runtime seam for the Open-Eywa rebuild."""

# --- No orchestrator dependency (must load first to break circular import) ---
from .runtime_interface import (
    RUN_EXIT_REASONS,
    RuntimeAdapter,
    RuntimeContractError,
    RuntimeRequest,
    RuntimeResult,
)
from .prompt_loader import PromptBundle, PromptLoader, PromptLoaderError
from .runtime_task_builder import (
    RuntimeTaskBuildError,
    build_runtime_task_content,
    load_prepared_packet,
)
from .openrouter_client import (
    OpenRouterChatClient,
    OpenRouterClientConfig,
    OpenRouterClientError,
)
from .simulation_scenarios import (
    SCENARIO_ACTION_TYPES,
    ScenarioAction,
    ScenarioScenarioError,
    SimulatedScenario,
    load_scenario,
)

# --- These trigger system.orchestrator; RuntimeAdapter is now available ---
from .cli_runtime_base import CliRuntimeBase, CliRuntimeConfig, CliRuntimeError
from .claude_cli_runtime import ClaudeCliRuntime
from .codex_cli_runtime import CodexCliRuntime
from .openrouter_runtime import (
    OpenRouterRuntime,
    OpenRouterRuntimeConfig,
    OpenRouterRuntimeError,
)
from .simulated_runtime import SimulatedRuntime, SimulatedRuntimeError
from .runtime_factory import (
    LIVE_CANARY_DEFAULT_MODEL,
    LIVE_CANARY_ROLE_ORDER,
    LiveCanaryRuntimeSettings,
    LiveRuntimeSettings,
    RuntimeProvider,
    build_live_runtime,
    build_openrouter_runtime_for_live_canary,
    default_live_canary_role_models,
)

__all__ = [
    "RUN_EXIT_REASONS",
    "ClaudeCliRuntime",
    "CliRuntimeBase",
    "CliRuntimeConfig",
    "CliRuntimeError",
    "CodexCliRuntime",
    "LIVE_CANARY_DEFAULT_MODEL",
    "LIVE_CANARY_ROLE_ORDER",
    "LiveCanaryRuntimeSettings",
    "LiveRuntimeSettings",
    "OpenRouterChatClient",
    "OpenRouterClientConfig",
    "OpenRouterClientError",
    "OpenRouterRuntime",
    "OpenRouterRuntimeConfig",
    "OpenRouterRuntimeError",
    "PromptBundle",
    "PromptLoader",
    "PromptLoaderError",
    "RuntimeAdapter",
    "RuntimeContractError",
    "RuntimeProvider",
    "RuntimeRequest",
    "RuntimeResult",
    "RuntimeTaskBuildError",
    "build_live_runtime",
    "build_openrouter_runtime_for_live_canary",
    "build_runtime_task_content",
    "default_live_canary_role_models",
    "load_prepared_packet",
    "SCENARIO_ACTION_TYPES",
    "ScenarioAction",
    "ScenarioScenarioError",
    "SimulatedRuntime",
    "SimulatedRuntimeError",
    "SimulatedScenario",
    "load_scenario",
]

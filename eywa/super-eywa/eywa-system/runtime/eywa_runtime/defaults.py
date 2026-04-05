"""Default variable values for the deterministic v1 runtime."""

DEFAULT_RUN_LEVEL_VARIABLES = {
    "runtime_provider": "deterministic",
    "model": "deterministic-local-v1",
    "injected_prompt_profile": "default-builder",
    "context_policy": "minimal",
    "workflow_structure": "sequential_parent_review",
    "verification_policy": "light",
    "tool_policy": "none",
    "budget_policy": {
        "max_depth": 1,
        "max_helpers_per_node": 3,
    },
    "routing_policy": "return_to_creator",
    "recovery_policy": "report_problem",
}

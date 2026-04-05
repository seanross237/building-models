"""Default variable values for the deterministic v1 runtime."""

DEFAULT_RUN_LEVEL_VARIABLES = {
    "runtime_provider": "deterministic",
    "model": "deterministic-local-v1",
    "injected_prompt_profile": "agent_orchestration_basic_instruction_prompt",
    "additional_instruction_prompt_profiles": [],
    "context_policy": "minimal",
    "workflow_structure": "sequential_parent_review",
    "verification_policy": "light",
    "tool_policy": "none",
    "json_response_policy": "strict_required",
    "orchestration_policy": "agent_decides",
    "budget_policy": {
        "max_depth": 3,
        "max_helpers_per_node": 3,
        "max_turns_per_node": 4,
    },
    "routing_policy": "return_to_creator",
    "recovery_policy": "report_problem",
}

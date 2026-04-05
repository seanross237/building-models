"""Prompt assembly for the JSON orchestration runtime."""

from __future__ import annotations

import json
from typing import Any, Dict, Iterable, List


PROTOCOL_HEADER = """You are one Super-Eywa node.
Return only valid JSON.
Do not use markdown fences.
Your JSON must use schema_name "eywa_node_response" and schema_version "v1".
Your JSON must always include orchestration_decision.
Only choose orchestration decisions that are explicitly allowed for this turn."""


PROMPT_PROFILES: Dict[str, str] = {
    "agent_orchestration_basic_instruction_prompt": (
        "Decide how this node should proceed. "
        "You may execute locally, delegate to helper nodes, or report a problem. "
        "If you execute locally, put the actual node result text in response. "
        "If you delegate, create a helpers array where each helper has focused instructions and optional variable_overrides. "
        "If you report a problem, explain the blockage clearly in response."
    ),
    "double_check_reasoning_prompt": (
        "Before finalizing a decision, briefly sanity-check your reasoning. "
        "Prefer direct execution when the task is already narrow, and prefer delegation only when it materially improves the chance of a correct result."
    ),
    "numerical_self_verify_prompt": (
        "If the task appears numerical, verify the final quantity carefully before deciding that local execution is complete."
    ),
    "be_conservative_about_delegation_prompt": (
        "Delegate only when you can give genuinely useful helper instructions. "
        "Avoid shallow delegation that merely restates the original task."
    ),
}


def build_turn_prompt(
    node_packet: Dict[str, object],
    *,
    allowed_decisions: Iterable[str],
    turn_index: int,
    depth: int,
    child_results: List[Dict[str, object]] | None = None,
    synthesis_brief: str | None = None,
) -> Dict[str, Any]:
    input_payload = node_packet["input"]
    variable_resolution = node_packet["variable_resolution"]
    resolved_variables = variable_resolution["resolved_variables"]
    budget_policy = resolved_variables.get("budget_policy", {})

    base_profile_name = str(
        resolved_variables.get("injected_prompt_profile", "agent_orchestration_basic_instruction_prompt")
    )
    additional_profile_names = _normalize_profile_names(
        resolved_variables.get("additional_instruction_prompt_profiles", [])
    )
    profile_blocks = [build_profile_block(base_profile_name)]
    profile_blocks.extend(build_profile_block(name) for name in additional_profile_names)

    allowed = [str(decision) for decision in allowed_decisions]
    runtime_facts = [
        f"- node_id: {node_packet['node_id']}",
        f"- run_id: {node_packet['run_id']}",
        f"- current_depth: {depth}",
        f"- turn_index_for_this_node: {turn_index}",
        f"- max_depth: {budget_policy.get('max_depth')}",
        f"- max_helpers_per_node: {budget_policy.get('max_helpers_per_node')}",
        f"- max_turns_per_node: {budget_policy.get('max_turns_per_node')}",
        f"- routing_policy: {resolved_variables.get('routing_policy')}",
        f"- recovery_policy: {resolved_variables.get('recovery_policy')}",
        f"- workflow_structure: {resolved_variables.get('workflow_structure')}",
        f"- verification_policy: {resolved_variables.get('verification_policy')}",
        f"- allowed_decisions_this_turn: {', '.join(allowed)}",
    ]

    user_sections = [
        "Runtime facts:",
        "\n".join(runtime_facts),
        "",
        "Node assignment:",
        str(input_payload["instructions"]),
    ]

    context_refs = input_payload.get("provided_context_refs", [])
    if context_refs:
        user_sections.extend(
            [
                "",
                "Provided context refs:",
                json.dumps(context_refs, indent=2),
            ]
        )

    if synthesis_brief:
        user_sections.extend(
            [
                "",
                "Synthesis brief from the earlier delegation decision:",
                synthesis_brief,
            ]
        )

    if child_results:
        rendered_child_results = []
        for item in child_results:
            rendered_child_results.append(
                {
                    "node_id": item["node_id"],
                    "summary": item["summary"],
                }
            )
        user_sections.extend(
            [
                "",
                "Child results available to this node:",
                json.dumps(rendered_child_results, indent=2),
            ]
        )

    user_sections.extend(
        [
            "",
            "Required JSON shape guidance:",
            json.dumps(_response_shape_guidance(), indent=2),
        ]
    )
    user_prompt = "\n".join(user_sections).strip()

    system_sections = [PROTOCOL_HEADER, ""]
    for block in profile_blocks:
        system_sections.extend(
            [
                f"Prompt profile: {block['name']}",
                block["text"],
                "",
            ]
        )
    system_prompt = "\n".join(system_sections).strip()

    snapshot_lines = [
        "Super-Eywa v1 runtime prompt snapshot.",
        f"Turn index: {turn_index}",
        f"Node depth: {depth}",
        f"Allowed decisions: {allowed}",
        f"Injected prompt profile: {base_profile_name}",
        f"Additional instruction prompt profiles: {additional_profile_names}",
        "System prompt:",
        system_prompt,
        "",
        "User prompt:",
        user_prompt,
    ]

    return {
        "system_prompt": system_prompt,
        "user_prompt": user_prompt,
        "snapshot_text": "\n".join(snapshot_lines).strip(),
        "base_profile_name": base_profile_name,
        "additional_profile_names": additional_profile_names,
        "allowed_decisions": allowed,
    }


def build_profile_block(name: str) -> Dict[str, str]:
    text = PROMPT_PROFILES.get(name)
    if text is None:
        text = f"Unknown prompt profile '{name}'. Fall back to the JSON orchestration protocol and do not invent behavior."
    return {
        "name": name,
        "text": text,
    }


def _normalize_profile_names(value: object) -> List[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    return []


def _response_shape_guidance() -> Dict[str, Any]:
    return {
        "schema_name": "eywa_node_response",
        "schema_version": "v1",
        "orchestration_decision": "execute_locally | delegate | report_problem",
        "decision_notes": "optional string",
        "execute_locally_shape": {
            "response": "string",
            "result_type": "optional string",
        },
        "delegate_shape": {
            "helpers": [
                {
                    "label": "string",
                    "instructions": "string",
                    "variable_overrides": {},
                }
            ],
            "synthesis_brief": "optional string",
        },
        "report_problem_shape": {
            "response": "string",
        },
    }

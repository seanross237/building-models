"""Prompt rendering for the v1 runtime."""

from __future__ import annotations

from typing import Dict, List


def render_prompt_text(
    node_packet: Dict[str, object],
    child_results: List[Dict[str, object]] | None = None,
) -> str:
    input_payload = node_packet["input"]
    variable_resolution = node_packet["variable_resolution"]
    resolved_variables = variable_resolution["resolved_variables"]

    lines = [
        "Super-Eywa v1 runtime prompt snapshot.",
        f"Instructions: {input_payload['instructions']}",
        f"Injected prompt profile: {resolved_variables.get('injected_prompt_profile')}",
        f"Context policy: {resolved_variables.get('context_policy')}",
        f"Workflow structure: {resolved_variables.get('workflow_structure')}",
        f"Verification policy: {resolved_variables.get('verification_policy')}",
    ]

    context_refs = input_payload.get("provided_context_refs", [])
    if context_refs:
        lines.append(f"Provided context refs: {context_refs}")
    else:
        lines.append("Provided context refs: []")

    if child_results:
        lines.append("Child results:")
        for result in child_results:
            lines.append(f"- {result['node_id']}: {result['summary']}")

    return "\n".join(lines)

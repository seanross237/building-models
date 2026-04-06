"""Prompt assembly for prompt-family-based JSON orchestration."""

from __future__ import annotations

import json
from typing import Any, Dict, Iterable, List


PROMPT_PROFILES: Dict[str, str] = {
    "agent_orchestration_basic_instruction_prompt": (
        "Decide how this node should proceed on this turn. "
        "You may execute locally, delegate to helper nodes, or report a problem. "
        "Prefer direct execution when the task is narrow and self-contained. "
        "Prefer delegation when the task separates into genuinely useful subproblems. "
        "If child results are already present, use them seriously when deciding whether you can now finish the task."
    ),
    "single_child_transmute_prompt": (
        "Treat this turn as a transmutation step. "
        "Your job is to reframe the assignment into one sharper formulation that gives a single child node a better chance of success. "
        "Do not decompose into multiple parts. "
        "Delegate to exactly one helper with the best transformed version of the task you can produce."
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

PROMPT_FAMILIES = {
    "none",
    "execute",
    "transmute",
    "delegate",
    "agent_chooses",
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
    allowed = [str(decision) for decision in allowed_decisions]
    child_review = bool(child_results)
    prompt_family = _resolved_prompt_family(resolved_variables, child_review=child_review)
    base_header_prompt = _resolved_base_header_prompt(resolved_variables, child_review=child_review)
    selected_prompt_text = _resolved_selected_prompt_text(
        resolved_variables,
        prompt_family=prompt_family,
        allowed_decisions=allowed,
        child_review=child_review,
    )
    if not selected_prompt_text:
        selected_prompt_text = _default_selected_prompt_text(
            prompt_family=prompt_family,
            allowed_decisions=allowed,
            child_review=child_review,
        )

    additional_profile_names = _normalize_profile_names(
        resolved_variables.get("additional_instruction_prompt_profiles", [])
    )
    additional_profile_texts = [
        build_profile_block(name)["text"]
        for name in additional_profile_names
    ]

    user_sections: List[str] = []
    if selected_prompt_text:
        user_sections.append(selected_prompt_text)

    for profile_text in additional_profile_texts:
        if profile_text.strip():
            user_sections.append(profile_text)

    if synthesis_brief:
        user_sections.append(
            "Synthesis brief from the earlier child-creation step:\n"
            f"{synthesis_brief}"
        )

    if child_results:
        rendered_child_results = [
            {
                "node_id": item["node_id"],
                "summary": item["summary"],
            }
            for item in child_results
        ]
        user_sections.append(
            "Child results already returned to you:\n"
            f"{json.dumps(rendered_child_results, indent=2)}"
        )

    context_refs = input_payload.get("provided_context_refs", [])
    if context_refs:
        user_sections.append(
            "Provided context refs:\n"
            f"{json.dumps(context_refs, indent=2)}"
        )

    user_sections.append(f"Question:\n{str(input_payload['instructions'])}")
    user_prompt = "\n\n".join(section for section in user_sections if section.strip()).strip()
    system_prompt = base_header_prompt

    snapshot_lines = [
        "Super-Eywa v1 runtime prompt snapshot.",
        f"Turn index: {turn_index}",
        f"Node depth: {depth}",
        f"Allowed decisions: {allowed}",
        f"Prompt family: {prompt_family}",
        f"Base header prompt: {base_header_prompt!r}",
        "Selected prompt text:",
        selected_prompt_text or "(blank)",
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
        "prompt_family": prompt_family,
        "selected_prompt_text": selected_prompt_text,
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


def _normalize_prompt_family(value: object) -> str:
    family = str(value or "agent_chooses").strip()
    if family not in PROMPT_FAMILIES:
        return "agent_chooses"
    return family


def _resolved_prompt_family(resolved_variables: Dict[str, Any], *, child_review: bool) -> str:
    if child_review:
        review_prompt_family = str(resolved_variables.get("review_prompt_family", "") or "").strip()
        if review_prompt_family:
            return _normalize_prompt_family(review_prompt_family)
    return _normalize_prompt_family(resolved_variables.get("prompt_family", "agent_chooses"))


def _resolved_base_header_prompt(resolved_variables: Dict[str, Any], *, child_review: bool) -> str:
    if child_review:
        review_header = str(resolved_variables.get("review_base_header_prompt", "") or "").strip()
        if review_header:
            return review_header
    return str(resolved_variables.get("base_header_prompt", "") or "").strip()


def _resolved_selected_prompt_text(
    resolved_variables: Dict[str, Any],
    *,
    prompt_family: str,
    allowed_decisions: List[str],
    child_review: bool,
) -> str:
    if child_review:
        review_prompt_text = str(resolved_variables.get("review_selected_prompt_text", "") or "").strip()
        if review_prompt_text:
            return review_prompt_text

        if prompt_family in {"transmute", "delegate"} and allowed_decisions == ["execute_locally"]:
            return ""

    return str(resolved_variables.get("selected_prompt_text", "") or "").strip()


def _default_selected_prompt_text(
    *,
    prompt_family: str,
    allowed_decisions: List[str],
    child_review: bool,
) -> str:
    if prompt_family == "none":
        return ""

    if prompt_family == "execute":
        return (
            "You are going to solve the following question yourself. "
            "Return exactly one JSON object in this format:\n"
            f"{json.dumps(_execute_example(), indent=2)}"
        )

    if prompt_family == "transmute":
        if child_review:
            return (
                "A child result has already come back to you. "
                "Use that returned work to produce the final response yourself. "
                "Return exactly one JSON object in this format:\n"
                f"{json.dumps(_execute_example(), indent=2)}"
            )
        return (
            "You are going to transmute the following question for another agent to solve. "
            "Try to make it clearer, sharper, more executable, or more formal. "
            "Return exactly one JSON object in this format:\n"
            f"{json.dumps(_transmute_example(), indent=2)}"
        )

    if prompt_family == "delegate":
        if child_review:
            return (
                "Child results have already come back to you. "
                "Use them to produce the final response yourself. "
                "Return exactly one JSON object in this format:\n"
                f"{json.dumps(_execute_example(), indent=2)}"
            )
        return (
            "You are going to decompose the following question into useful subproblems for other agents. "
            "Return exactly one JSON object in this format:\n"
            f"{json.dumps(_delegate_example(), indent=2)}"
        )

    choice_examples = _agent_choice_examples(allowed_decisions)
    return (
        "Choose how to proceed on this turn. "
        f"Valid orchestration decisions for this turn are: {', '.join(allowed_decisions)}. "
        "Return exactly one JSON object matching one of these formats:\n"
        f"{json.dumps(choice_examples, indent=2)}"
    )


def _execute_example() -> Dict[str, Any]:
    return {
        "schema_name": "eywa_node_response",
        "schema_version": "v1",
        "orchestration_decision": "execute_locally",
        "decision_notes": "optional string",
        "response": "string",
        "result_type": "optional string",
    }


def _transmute_example() -> Dict[str, Any]:
    return {
        "schema_name": "eywa_node_response",
        "schema_version": "v1",
        "orchestration_decision": "transmute",
        "decision_notes": "optional string",
        "message_for_next_agent": "string",
    }


def _delegate_example() -> Dict[str, Any]:
    return {
        "schema_name": "eywa_node_response",
        "schema_version": "v1",
        "orchestration_decision": "delegate",
        "decision_notes": "optional string",
        "helpers": [
            {
                "label": "string",
                "instructions": "string",
                "variable_overrides": {},
            }
        ],
        "synthesis_brief": "optional string",
    }


def _report_problem_example() -> Dict[str, Any]:
    return {
        "schema_name": "eywa_node_response",
        "schema_version": "v1",
        "orchestration_decision": "report_problem",
        "decision_notes": "optional string",
        "response": "string",
    }


def _agent_choice_examples(allowed_decisions: Iterable[str]) -> Dict[str, Any]:
    examples: Dict[str, Any] = {}
    for decision in allowed_decisions:
        if decision == "execute_locally":
            examples["execute_locally_example"] = _execute_example()
        elif decision == "transmute":
            examples["transmute_example"] = _transmute_example()
        elif decision == "delegate":
            examples["delegate_example"] = _delegate_example()
        elif decision == "report_problem":
            examples["report_problem_example"] = _report_problem_example()
    return examples

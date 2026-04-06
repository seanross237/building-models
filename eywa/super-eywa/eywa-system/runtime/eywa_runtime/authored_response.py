"""Parsing and validation for node-authored JSON responses."""

from __future__ import annotations

import json
from typing import Any, Dict, Iterable

from .contracts import ContractError, validate_node_authored_response


NODE_RESPONSE_SCHEMA_NAME = "eywa_node_response"
NODE_RESPONSE_SCHEMA_VERSION = "v1"


class AuthoredResponseError(ValueError):
    """Raised when a node-authored response is missing or invalid."""


def parse_authored_response_text(raw_text: str) -> Dict[str, Any]:
    text = raw_text.strip()
    if not text:
        raise AuthoredResponseError("node-authored response was empty")

    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()

    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1 or start >= end:
            raise AuthoredResponseError("node-authored response was not valid JSON") from None
        try:
            payload = json.loads(text[start : end + 1])
        except json.JSONDecodeError as exc:
            raise AuthoredResponseError("node-authored response was not valid JSON") from exc

    if not isinstance(payload, dict):
        raise AuthoredResponseError("node-authored response must be a JSON object")
    return payload


def validate_authored_response(
    payload: Dict[str, Any],
    *,
    allowed_decisions: Iterable[str],
    max_helpers: int,
) -> Dict[str, Any]:
    payload = _normalize_wrapper_payload(payload)
    execute_locally_shape = payload.get("execute_locally_shape")
    delegate_shape = payload.get("delegate_shape")
    report_problem_shape = payload.get("report_problem_shape")

    normalized: Dict[str, Any] = {
        "schema_name": payload.get("schema_name", NODE_RESPONSE_SCHEMA_NAME),
        "schema_version": payload.get("schema_version", NODE_RESPONSE_SCHEMA_VERSION),
        "orchestration_decision": payload.get("orchestration_decision"),
        "decision_notes": payload.get("decision_notes", ""),
    }

    decision = normalized.get("orchestration_decision")
    if isinstance(decision, str):
        normalized["orchestration_decision"] = decision.strip()
    if isinstance(normalized.get("decision_notes"), str):
        normalized["decision_notes"] = str(normalized["decision_notes"]).strip()

    if normalized["orchestration_decision"] == "execute_locally":
        response = payload.get("response", "")
        if not isinstance(response, str) or not response.strip():
            response = _coerce_response_text(response)
        if (not isinstance(response, str) or not response.strip()) and isinstance(execute_locally_shape, dict):
            response = execute_locally_shape.get("response", "")
        if not isinstance(response, str) or not response.strip():
            response = _coerce_response_text(response)
        normalized["response"] = response.strip() if isinstance(response, str) else ""
        result_type = payload.get("result_type", "summary")
        if result_type == "summary" and isinstance(execute_locally_shape, dict):
            nested_result_type = execute_locally_shape.get("result_type")
            if nested_result_type is not None:
                result_type = nested_result_type
        if result_type is not None:
            normalized["result_type"] = str(result_type).strip()
    elif normalized["orchestration_decision"] == "report_problem":
        response = payload.get("response", "")
        if not isinstance(response, str) or not response.strip():
            response = _coerce_response_text(response)
        if (not isinstance(response, str) or not response.strip()) and isinstance(report_problem_shape, dict):
            response = report_problem_shape.get("response", "")
        if not isinstance(response, str) or not response.strip():
            response = _coerce_response_text(response)
        normalized["response"] = response.strip() if isinstance(response, str) else ""
    elif normalized["orchestration_decision"] == "transmute":
        message_for_next_agent = payload.get("message_for_next_agent", "")
        if (not isinstance(message_for_next_agent, str) or not message_for_next_agent.strip()) and isinstance(
            payload.get("payload"), dict
        ):
            message_for_next_agent = _render_transmute_payload(payload["payload"])
        normalized["message_for_next_agent"] = (
            message_for_next_agent.strip() if isinstance(message_for_next_agent, str) else ""
        )
        next_node_overrides = payload.get("next_node_overrides") or {}
        normalized["next_node_overrides"] = next_node_overrides if isinstance(next_node_overrides, dict) else next_node_overrides
    elif normalized["orchestration_decision"] == "delegate":
        helpers = payload.get("helpers", [])
        if (not isinstance(helpers, list) or not helpers) and isinstance(delegate_shape, dict):
            helpers = delegate_shape.get("helpers", [])
        if isinstance(helpers, list):
            normalized_helpers = []
            for index, helper in enumerate(helpers, start=1):
                if not isinstance(helper, dict):
                    normalized_helpers.append(helper)
                    continue
                normalized_helpers.append(
                    {
                        "label": str(helper.get("label") or f"helper_{index:02d}").strip(),
                        "instructions": str(helper.get("instructions", "")).strip(),
                        "variable_overrides": helper.get("variable_overrides") or {},
                    }
                )
            normalized["helpers"] = normalized_helpers
        else:
            normalized["helpers"] = helpers
        synthesis_brief = payload.get("synthesis_brief", "")
        if (not synthesis_brief) and isinstance(delegate_shape, dict):
            synthesis_brief = delegate_shape.get("synthesis_brief", "")
        normalized["synthesis_brief"] = str(synthesis_brief).strip() if synthesis_brief is not None else ""

    helper_count = len(normalized.get("helpers", [])) if isinstance(normalized.get("helpers"), list) else 0
    if normalized.get("orchestration_decision") == "delegate" and helper_count > max_helpers:
        raise AuthoredResponseError(
            f"delegate responses requested {helper_count} helpers but max_helpers is {max_helpers}"
        )

    try:
        validate_node_authored_response(
            normalized,
            allowed_decisions=allowed_decisions,
        )
    except ContractError as exc:
        raise AuthoredResponseError(str(exc)) from exc
    return normalized


def _normalize_wrapper_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    wrapped = payload.get("eywa_node_response")
    if not isinstance(wrapped, dict):
        return payload

    normalized = dict(wrapped)
    normalized.setdefault("schema_name", "eywa_node_response")
    if "schema_version" not in normalized and "version" in normalized:
        normalized["schema_version"] = normalized.get("version")
    if "payload" not in normalized and isinstance(normalized.get("content"), dict):
        normalized["payload"] = normalized.get("content")
    return normalized


def _render_transmute_payload(payload: Dict[str, Any]) -> str:
    sections: list[str] = []
    task_description = payload.get("task_description")
    if isinstance(task_description, str) and task_description.strip():
        sections.append(task_description.strip())
    mathematical_formulation = payload.get("mathematical_formulation")
    if isinstance(mathematical_formulation, str) and mathematical_formulation.strip():
        sections.append(f"Mathematical formulation: {mathematical_formulation.strip()}")

    parameters = payload.get("parameters")
    if isinstance(parameters, dict) and parameters:
        lines = ["Parameters:"]
        for key, value in parameters.items():
            lines.append(f"- {key}: {value}")
        sections.append("\n".join(lines))

    expected_output_format = payload.get("expected_output_format")
    if isinstance(expected_output_format, dict) and expected_output_format:
        lines = ["Expected output format:"]
        for key, value in expected_output_format.items():
            lines.append(f"- {key}: {value}")
        sections.append("\n".join(lines))

    if not sections:
        return json.dumps(payload, indent=2)
    return "\n\n".join(sections)


def _coerce_response_text(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()
    if not isinstance(value, dict):
        return ""

    final_answer = value.get("final_answer")
    justification = value.get("justification")
    if final_answer is not None or justification is not None:
        lines: list[str] = []
        if final_answer is not None:
            lines.append(f"FINAL_ANSWER: {str(final_answer).strip()}")
        if justification is not None:
            lines.append(f"JUSTIFICATION: {str(justification).strip()}")
        return "\n".join(line for line in lines if line.strip()).strip()

    for key in ("response", "content", "message"):
        nested = value.get(key)
        if isinstance(nested, str) and nested.strip():
            return nested.strip()

    return ""

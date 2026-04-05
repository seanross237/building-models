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
        normalized["response"] = response.strip() if isinstance(response, str) else ""
        result_type = payload.get("result_type", "summary")
        if result_type is not None:
            normalized["result_type"] = str(result_type).strip()
    elif normalized["orchestration_decision"] == "report_problem":
        response = payload.get("response", "")
        normalized["response"] = response.strip() if isinstance(response, str) else ""
    elif normalized["orchestration_decision"] == "delegate":
        helpers = payload.get("helpers", [])
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

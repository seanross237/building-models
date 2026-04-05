"""Simple contract validators for Super-Eywa v1."""

from __future__ import annotations

from typing import Any, Dict, Iterable


class ContractError(ValueError):
    """Raised when a contract payload is invalid."""


def _require_keys(payload: Dict[str, Any], required: Iterable[str], contract_name: str) -> None:
    missing = [key for key in required if key not in payload]
    if missing:
        raise ContractError(f"{contract_name} missing required keys: {missing}")


def validate_run_packet(payload: Dict[str, Any]) -> None:
    _require_keys(
        payload,
        [
            "contract_name",
            "contract_version",
            "run_id",
            "created_at_utc",
            "root_node_id",
            "task",
            "run_level_variables",
            "top_level_context",
            "root_setup",
        ],
        "run_packet",
    )
    if payload["contract_name"] != "run_packet":
        raise ContractError("run_packet contract_name must be 'run_packet'")


def validate_node_packet(payload: Dict[str, Any]) -> None:
    _require_keys(
        payload,
        [
            "contract_name",
            "contract_version",
            "run_id",
            "node_id",
            "created_at_utc",
            "creation_parent_node_id",
            "input",
            "variable_resolution",
            "node_setup",
        ],
        "node_packet",
    )
    if payload["contract_name"] != "node_packet":
        raise ContractError("node_packet contract_name must be 'node_packet'")


def validate_node_output(payload: Dict[str, Any]) -> None:
    _require_keys(
        payload,
        [
            "contract_name",
            "contract_version",
            "run_id",
            "node_id",
            "action_type",
            "results",
            "outgoing_packets",
        ],
        "node_output",
    )
    if payload["contract_name"] != "node_output":
        raise ContractError("node_output contract_name must be 'node_output'")

    allowed_actions = {
        "local_attempt",
        "local_replan",
        "recruit_help",
        "report_success",
        "report_problem",
    }
    if payload["action_type"] not in allowed_actions:
        raise ContractError(f"invalid action_type: {payload['action_type']}")

    allowed_message_types = {
        "helper_assignment",
        "work_result",
        "replan_message",
        "success_report",
        "problem_report",
    }
    allowed_target_types = {
        "creating_parent",
        "existing_node",
        "new_helper",
    }
    for packet in payload["outgoing_packets"]:
        _require_keys(packet, ["message_type", "target", "message", "attachment_refs"], "outgoing_packet")
        if packet["message_type"] not in allowed_message_types:
            raise ContractError(f"invalid message_type: {packet['message_type']}")
        _require_keys(packet["target"], ["target_type", "target_ref"], "outgoing_packet.target")
        if packet["target"]["target_type"] not in allowed_target_types:
            raise ContractError(f"invalid target_type: {packet['target']['target_type']}")


def validate_node_record(payload: Dict[str, Any]) -> None:
    _require_keys(
        payload,
        [
            "contract_name",
            "contract_version",
            "run_id",
            "node_id",
            "state",
            "final_action_type",
            "input",
            "variables",
            "orchestration",
            "prompt",
            "results",
            "logging",
            "replay_ref",
        ],
        "node_record",
    )
    if payload["contract_name"] != "node_record":
        raise ContractError("node_record contract_name must be 'node_record'")
    if payload["state"] not in {"created", "running", "completed", "system_error"}:
        raise ContractError(f"invalid node state: {payload['state']}")
    if payload["final_action_type"] not in {
        "local_attempt",
        "local_replan",
        "recruit_help",
        "report_success",
        "report_problem",
    }:
        raise ContractError(f"invalid final_action_type: {payload['final_action_type']}")

    orchestration = payload["orchestration"]
    _require_keys(
        orchestration,
        [
            "turn_count",
            "initial_decision",
            "final_decision",
            "decision_notes",
            "helper_count",
        ],
        "node_record.orchestration",
    )
    allowed_decisions = {"execute_locally", "delegate", "report_problem"}
    if orchestration["initial_decision"] not in allowed_decisions:
        raise ContractError(f"invalid initial_decision: {orchestration['initial_decision']}")
    if orchestration["final_decision"] not in allowed_decisions:
        raise ContractError(f"invalid final_decision: {orchestration['final_decision']}")


def validate_node_authored_response(
    payload: Dict[str, Any],
    *,
    allowed_decisions: Iterable[str] | None = None,
) -> None:
    _require_keys(
        payload,
        [
            "schema_name",
            "schema_version",
            "orchestration_decision",
        ],
        "node_authored_response",
    )
    if payload["schema_name"] != "eywa_node_response":
        raise ContractError("node_authored_response schema_name must be 'eywa_node_response'")
    if payload["schema_version"] != "v1":
        raise ContractError("node_authored_response schema_version must be 'v1'")

    decision = payload["orchestration_decision"]
    valid_decisions = {
        "execute_locally",
        "delegate",
        "report_problem",
    }
    if decision not in valid_decisions:
        raise ContractError(f"invalid orchestration_decision: {decision}")

    if allowed_decisions is not None and decision not in set(allowed_decisions):
        raise ContractError(f"orchestration_decision not allowed this turn: {decision}")

    decision_notes = payload.get("decision_notes")
    if decision_notes is not None and not isinstance(decision_notes, str):
        raise ContractError("decision_notes must be a string when present")

    if decision == "execute_locally":
        response = payload.get("response")
        if not isinstance(response, str) or not response.strip():
            raise ContractError("execute_locally response must be a non-empty string")
        result_type = payload.get("result_type")
        if result_type is not None and not isinstance(result_type, str):
            raise ContractError("execute_locally result_type must be a string when present")
        return

    if decision == "report_problem":
        response = payload.get("response")
        if not isinstance(response, str) or not response.strip():
            raise ContractError("report_problem response must be a non-empty string")
        return

    helpers = payload.get("helpers")
    if not isinstance(helpers, list) or not helpers:
        raise ContractError("delegate helpers must be a non-empty list")

    synthesis_brief = payload.get("synthesis_brief")
    if synthesis_brief is not None and not isinstance(synthesis_brief, str):
        raise ContractError("delegate synthesis_brief must be a string when present")

    for helper in helpers:
        if not isinstance(helper, dict):
            raise ContractError("delegate helper entries must be objects")
        instructions = helper.get("instructions")
        if not isinstance(instructions, str) or not instructions.strip():
            raise ContractError("delegate helper instructions must be a non-empty string")
        label = helper.get("label")
        if label is not None and not isinstance(label, str):
            raise ContractError("delegate helper label must be a string when present")
        variable_overrides = helper.get("variable_overrides")
        if variable_overrides is not None and not isinstance(variable_overrides, dict):
            raise ContractError("delegate helper variable_overrides must be an object when present")

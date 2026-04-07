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


def validate_final_output(payload: Dict[str, Any]) -> None:
    _require_keys(
        payload,
        [
            "contract_name",
            "contract_version",
            "run_id",
            "created_at_utc",
            "source_node_id",
            "source_node_record_ref",
            "action_type",
            "terminal_result_destination",
            "result",
        ],
        "final_output",
    )
    if payload["contract_name"] != "final_output":
        raise ContractError("final_output contract_name must be 'final_output'")
    if payload["terminal_result_destination"] != "final_output":
        raise ContractError("final_output terminal_result_destination must be 'final_output'")
    if payload["action_type"] not in {"report_success", "report_problem"}:
        raise ContractError(f"invalid final_output action_type: {payload['action_type']}")
    result = payload["result"]
    if not isinstance(result, dict):
        raise ContractError("final_output result must be an object")
    _require_keys(result, ["result_type", "content", "attachment_refs"], "final_output.result")


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
        "final_output",
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
    allowed_decisions = {"execute_locally", "transmute", "delegate", "review", "report_problem"}
    if orchestration["initial_decision"] not in allowed_decisions:
        raise ContractError(f"invalid initial_decision: {orchestration['initial_decision']}")
    if orchestration["final_decision"] not in allowed_decisions:
        raise ContractError(f"invalid final_decision: {orchestration['final_decision']}")
    terminal_result_destination = orchestration.get("terminal_result_destination")
    if terminal_result_destination is not None and terminal_result_destination not in {"creator", "final_output"}:
        raise ContractError(
            f"invalid terminal_result_destination: {terminal_result_destination}"
        )
    awaited_child_results = orchestration.get("awaited_child_results")
    if awaited_child_results is not None and not isinstance(awaited_child_results, bool):
        raise ContractError("awaited_child_results must be a boolean when present")


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
        "transmute",
        "delegate",
        "review",
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
        artifacts = payload.get("artifacts")
        if artifacts is not None:
            if not isinstance(artifacts, list) or not artifacts:
                raise ContractError("execute_locally artifacts must be a non-empty list when present")
            for artifact in artifacts:
                if not isinstance(artifact, dict):
                    raise ContractError("execute_locally artifacts entries must be objects")
                _require_keys(artifact, ["path", "content"], "node_authored_response.execute_locally.artifact")
                if not isinstance(artifact["path"], str) or not artifact["path"].strip():
                    raise ContractError("execute_locally artifact path must be a non-empty string")
                if not isinstance(artifact["content"], str):
                    raise ContractError("execute_locally artifact content must be a string")
        return

    if decision == "report_problem":
        response = payload.get("response")
        if not isinstance(response, str) or not response.strip():
            raise ContractError("report_problem response must be a non-empty string")
        return

    if decision == "transmute":
        message = payload.get("message_for_next_agent")
        if not isinstance(message, str) or not message.strip():
            raise ContractError("transmute message_for_next_agent must be a non-empty string")
        next_node_overrides = payload.get("next_node_overrides")
        if next_node_overrides is not None and not isinstance(next_node_overrides, dict):
            raise ContractError("transmute next_node_overrides must be an object when present")
        return

    if decision == "review":
        draft_response = payload.get("draft_response")
        if not isinstance(draft_response, str) or not draft_response.strip():
            raise ContractError("review draft_response must be a non-empty string")
        message = payload.get("message_for_reviewer")
        if not isinstance(message, str) or not message.strip():
            raise ContractError("review message_for_reviewer must be a non-empty string")
        next_node_overrides = payload.get("next_node_overrides")
        if next_node_overrides is not None and not isinstance(next_node_overrides, dict):
            raise ContractError("review next_node_overrides must be an object when present")
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

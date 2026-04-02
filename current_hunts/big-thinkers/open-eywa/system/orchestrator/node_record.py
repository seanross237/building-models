from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable, Literal

AssignmentSource = Literal["default", "inherited", "manual", "random"]

ASSIGNMENT_SOURCES: tuple[AssignmentSource, ...] = (
    "default",
    "inherited",
    "manual",
    "random",
)

NODE_RECORD_SCHEMA_VERSION = 1


def node_record_path(target: Any) -> Path:
    if hasattr(target, "node_record_file"):
        return Path(getattr(target, "node_record_file")).expanduser().resolve()
    path = Path(target).expanduser().resolve()
    if path.name == "node.json":
        return path
    return path / "system" / "node.json"


def read_node_record(target: Any) -> dict[str, Any]:
    path = node_record_path(target)
    return json.loads(path.read_text(encoding="utf-8"))


def write_node_record(target: Any, record: dict[str, Any]) -> None:
    path = node_record_path(target)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def update_node_record(
    target: Any,
    updater: Callable[[dict[str, Any]], None],
) -> dict[str, Any]:
    record = read_node_record(target)
    updater(record)
    write_node_record(target, record)
    return record


def snapshot_node_record(target: Any, destination: str | Path) -> None:
    record = read_node_record(target)
    destination_path = Path(destination).expanduser().resolve()
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    destination_path.write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def build_initial_node_record(
    *,
    node_id: str,
    parent_node_id: str | None,
    task_source_name: str,
    task_source_path: str,
    initial_status: str,
    next_role: str | None,
    terminal_outcome: str | None,
    failure_reason: str | None,
    cancellation_reason: str | None,
    waiting_on_computation_note: str | None,
    model: str | None = None,
    variant: str | None = None,
    model_source: AssignmentSource | None = None,
    variant_source: AssignmentSource | None = None,
    experiment_id: str | None = None,
    assignment_mode: str | None = None,
    random_seed: int | None = None,
    dimensions: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "schema_version": NODE_RECORD_SCHEMA_VERSION,
        "identity": {
            "node_id": node_id,
            "parent_node_id": parent_node_id,
        },
        "task": {
            "source_name": task_source_name,
            "source_path": task_source_path,
        },
        "lifecycle": {
            "status": initial_status,
            "terminal_outcome": terminal_outcome,
            "failure_reason": failure_reason,
            "cancellation_reason": cancellation_reason,
            "waiting_on_computation_note": waiting_on_computation_note,
            "computation_result_note": None,
            "retry_count": 0,
        },
        "control": {
            "next_role": next_role,
            "next_action_after_child_report": None,
        },
        "parameters": {
            "resolved": {
                "model": model,
                "variant": variant,
            },
            "sources": {
                "model": model_source,
                "variant": variant_source,
            },
            "experiment": {
                "experiment_id": experiment_id,
                "assignment_mode": assignment_mode,
                "random_seed": random_seed,
                "dimensions": dict(dimensions or {}),
            },
        },
        "progression": {
            "current_step_index": None,
            "steps": [],
            "latest_child_report": None,
        },
    }


def node_status(target: Any) -> str | None:
    return read_node_record(target).get("lifecycle", {}).get("status")


def node_terminal_outcome(target: Any) -> str | None:
    return read_node_record(target).get("lifecycle", {}).get("terminal_outcome")


def node_failure_reason(target: Any) -> str | None:
    return read_node_record(target).get("lifecycle", {}).get("failure_reason")


def node_cancellation_reason(target: Any) -> str | None:
    return read_node_record(target).get("lifecycle", {}).get("cancellation_reason")


def node_waiting_on_computation_note(target: Any) -> str | None:
    return read_node_record(target).get("lifecycle", {}).get("waiting_on_computation_note")


def node_computation_result_note(target: Any) -> str | None:
    return read_node_record(target).get("lifecycle", {}).get("computation_result_note")


def node_retry_count(target: Any) -> int:
    retry_count = read_node_record(target).get("lifecycle", {}).get("retry_count")
    if isinstance(retry_count, int) and retry_count >= 0:
        return retry_count
    return 0


def node_next_role(target: Any) -> str | None:
    return read_node_record(target).get("control", {}).get("next_role")


def node_next_action_after_child_report(target: Any) -> str | None:
    return read_node_record(target).get("control", {}).get("next_action_after_child_report")

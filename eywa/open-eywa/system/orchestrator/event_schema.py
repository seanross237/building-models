from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import json
from typing import Any, Literal
from uuid import uuid4

EVENT_SCHEMA_VERSION = 1

EventType = Literal[
    "mission_drive_started",
    "mission_drive_completed",
    "mission_drive_failed",
    "node_created",
    "node_validated",
    "node_validation_failed",
    "node_status_changed",
    "node_completed",
    "node_escalated",
    "node_cancelled",
    "node_failed",
    "node_recovery_prepared",
    "run_started",
    "run_finished",
    "run_failed",
    "run_timed_out",
    "plan_parsed",
    "plan_step_registered",
    "plan_step_completed",
    "plan_step_failed",
    "child_node_created",
    "child_node_report_received",
    "parent_next_action_chosen",
    "artifact_written",
    "artifact_validated",
    "artifact_missing",
    "tool_called",
    "tool_finished",
    "tool_failed",
    "background_job_started",
    "background_job_finished",
    "background_job_failed",
    "usage_recorded",
    "cost_recorded",
]

EVENT_TYPES: tuple[EventType, ...] = (
    "mission_drive_started",
    "mission_drive_completed",
    "mission_drive_failed",
    "node_created",
    "node_validated",
    "node_validation_failed",
    "node_status_changed",
    "node_completed",
    "node_escalated",
    "node_cancelled",
    "node_failed",
    "node_recovery_prepared",
    "run_started",
    "run_finished",
    "run_failed",
    "run_timed_out",
    "plan_parsed",
    "plan_step_registered",
    "plan_step_completed",
    "plan_step_failed",
    "child_node_created",
    "child_node_report_received",
    "parent_next_action_chosen",
    "artifact_written",
    "artifact_validated",
    "artifact_missing",
    "tool_called",
    "tool_finished",
    "tool_failed",
    "background_job_started",
    "background_job_finished",
    "background_job_failed",
    "usage_recorded",
    "cost_recorded",
)

EVENT_PAYLOAD_REQUIRED_KEYS: dict[EventType, tuple[str, ...]] = {
    "mission_drive_started": ("mission_path", "root_node_id"),
    "mission_drive_completed": ("mission_path", "root_node_id", "final_status"),
    "mission_drive_failed": ("mission_path", "root_node_id", "failure_reason"),
    "node_status_changed": ("status_before", "status_after"),
    "node_completed": ("terminal_outcome",),
    "node_escalated": ("terminal_outcome",),
    "node_cancelled": ("terminal_outcome",),
    "node_failed": ("failure_reason",),
    "node_recovery_prepared": ("recovery_reason", "recovery_attempt", "previous_status"),
    "plan_parsed": ("step_count",),
    "plan_step_registered": ("step_index", "step_title", "child_name"),
    "plan_step_completed": ("step_index", "child_node_id"),
    "plan_step_failed": ("step_index", "child_node_id", "child_status"),
    "child_node_created": ("child_node_id", "child_node_path", "step_index", "step_title"),
    "child_node_report_received": ("child_node_id", "child_status"),
    "parent_next_action_chosen": ("child_node_id", "next_action"),
    "artifact_written": ("artifact_path",),
    "artifact_validated": ("artifact_path",),
    "artifact_missing": ("artifact_path",),
    "tool_called": ("tool_name",),
    "tool_finished": ("tool_name",),
    "tool_failed": ("tool_name",),
    "background_job_started": ("job_id",),
    "background_job_finished": ("job_id",),
    "background_job_failed": ("job_id",),
    "usage_recorded": ("usage",),
    "cost_recorded": ("cost",),
}


class EventSchemaError(ValueError):
    """Raised when an event record violates the canonical event schema."""


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class EventRecord:
    event_type: EventType
    mission_id: str
    node_id: str
    node_path: str
    event_version: int = EVENT_SCHEMA_VERSION
    event_id: str = field(default_factory=lambda: uuid4().hex)
    timestamp_utc: str = field(default_factory=utc_now_iso)
    parent_node_id: str | None = None
    run_id: str | None = None
    role: str | None = None
    model: str | None = None
    variant: str | None = None
    payload: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        validate_event_record(self)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def validate_event_record(record: EventRecord) -> None:
    if record.event_version != EVENT_SCHEMA_VERSION:
        raise EventSchemaError(
            f"Unsupported event version: {record.event_version!r}."
        )
    if record.event_type not in EVENT_TYPES:
        raise EventSchemaError(f"Unknown event type: {record.event_type!r}.")

    _require_non_empty_string(record.mission_id, "mission_id")
    _require_non_empty_string(record.node_id, "node_id")
    _require_non_empty_string(record.node_path, "node_path")
    _require_non_empty_string(record.event_id, "event_id")
    _require_non_empty_string(record.timestamp_utc, "timestamp_utc")

    if not isinstance(record.payload, dict):
        raise EventSchemaError("payload must be a dictionary.")

    required_payload_keys = EVENT_PAYLOAD_REQUIRED_KEYS.get(record.event_type, ())
    missing_keys = [key for key in required_payload_keys if key not in record.payload]
    if missing_keys:
        raise EventSchemaError(
            f"Event type {record.event_type!r} is missing payload keys: {missing_keys!r}."
        )

    try:
        json.dumps(record.to_dict())
    except TypeError as exc:
        raise EventSchemaError(
            "Event record must be JSON serializable."
        ) from exc


def event_from_dict(data: dict[str, Any]) -> EventRecord:
    return EventRecord(**data)


def _require_non_empty_string(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise EventSchemaError(f"{field_name} must be a non-empty string.")

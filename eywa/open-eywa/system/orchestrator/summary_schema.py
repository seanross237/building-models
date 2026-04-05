from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from .usage_schema import CostRecord, UsageRecord


@dataclass(frozen=True)
class RunSummary:
    run_id: str
    node_id: str
    role: str
    model: str | None
    variant: str | None
    started_at_utc: str
    finished_at_utc: str | None
    duration_seconds: float | None
    exit_reason: str
    artifacts_produced: tuple[str, ...] = ()
    tool_call_count: int = 0
    usage: UsageRecord = field(default_factory=UsageRecord)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class NodeSummary:
    mission_id: str
    node_id: str
    node_path: str
    status: str
    terminal_outcome: str | None
    failure_reason: str | None
    run_count: int
    retry_count: int
    roles_used: tuple[str, ...] = ()
    artifacts_written: tuple[str, ...] = ()
    total_duration_seconds: float | None = None
    waiting_duration_seconds: float | None = None
    validation_issue_count: int = 0
    usage: UsageRecord = field(default_factory=UsageRecord)
    cost: CostRecord = field(default_factory=CostRecord)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class MissionSummary:
    mission_id: str
    root_node_id: str
    final_status: str
    terminal_outcome: str | None
    failure_reason: str | None
    node_count: int
    completed_node_count: int
    escalated_node_count: int
    cancelled_node_count: int
    failed_node_count: int
    run_count: int
    total_duration_seconds: float | None = None
    usage: UsageRecord = field(default_factory=UsageRecord)
    cost: CostRecord = field(default_factory=CostRecord)
    roles_used: tuple[str, ...] = ()
    models_used: tuple[str, ...] = ()
    top_failure_reasons: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal, Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from system.orchestrator.summary_schema import RunSummary
    from system.orchestrator.usage_schema import UsageRecord

RunExitReason = Literal[
    "completed",
    "failed",
    "timed_out",
    "crashed",
    "no_progress",
    "cancelled",
]

RUN_EXIT_REASONS: tuple[RunExitReason, ...] = (
    "completed",
    "failed",
    "timed_out",
    "crashed",
    "no_progress",
    "cancelled",
)


class RuntimeContractError(ValueError):
    """Raised when runtime requests or results violate the runtime seam."""


def _default_usage() -> UsageRecord:
    from system.orchestrator.usage_schema import UsageRecord
    return UsageRecord()


@dataclass(frozen=True)
class RuntimeRequest:
    mission_id: str
    node_id: str
    node_path: str
    run_id: str
    role: str
    model: str | None = None
    variant: str | None = None
    prepared_inputs: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for field_name in ("mission_id", "node_id", "node_path", "run_id", "role"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise RuntimeContractError(f"{field_name} must be a non-empty string.")
        if not isinstance(self.prepared_inputs, tuple):
            raise RuntimeContractError("prepared_inputs must be a tuple.")
        if not isinstance(self.metadata, dict):
            raise RuntimeContractError("metadata must be a dictionary.")

    @property
    def node_root(self) -> Path:
        return Path(self.node_path).expanduser().resolve()


@dataclass(frozen=True)
class RuntimeResult:
    mission_id: str
    node_id: str
    node_path: str
    run_id: str
    role: str
    exit_reason: RunExitReason
    started_at_utc: str
    finished_at_utc: str
    duration_seconds: float
    model: str | None = None
    variant: str | None = None
    artifacts_produced: tuple[str, ...] = ()
    tool_call_count: int = 0
    usage: UsageRecord = field(default_factory=_default_usage)
    details: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for field_name in (
            "mission_id",
            "node_id",
            "node_path",
            "run_id",
            "role",
            "started_at_utc",
            "finished_at_utc",
        ):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise RuntimeContractError(f"{field_name} must be a non-empty string.")
        if self.exit_reason not in RUN_EXIT_REASONS:
            raise RuntimeContractError(f"Unknown runtime exit reason: {self.exit_reason!r}.")
        if self.duration_seconds < 0:
            raise RuntimeContractError("duration_seconds must be non-negative.")
        if not isinstance(self.artifacts_produced, tuple):
            raise RuntimeContractError("artifacts_produced must be a tuple.")
        if not isinstance(self.tool_call_count, int) or self.tool_call_count < 0:
            raise RuntimeContractError("tool_call_count must be a non-negative integer.")
        if not isinstance(self.details, dict):
            raise RuntimeContractError("details must be a dictionary.")

    def to_run_summary(self) -> RunSummary:
        from system.orchestrator.summary_schema import RunSummary
        return RunSummary(
            run_id=self.run_id,
            node_id=self.node_id,
            role=self.role,
            model=self.model,
            variant=self.variant,
            started_at_utc=self.started_at_utc,
            finished_at_utc=self.finished_at_utc,
            duration_seconds=self.duration_seconds,
            exit_reason=self.exit_reason,
            artifacts_produced=self.artifacts_produced,
            tool_call_count=self.tool_call_count,
            usage=self.usage,
        )


class RuntimeAdapter(Protocol):
    def run(self, request: RuntimeRequest) -> RuntimeResult:
        """Execute one runtime request and return a structured result."""

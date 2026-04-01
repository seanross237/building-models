from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any, Literal

from system.orchestrator.usage_schema import UsageRecord
from .runtime_interface import RUN_EXIT_REASONS, RunExitReason

ScenarioActionType = Literal["write_text", "touch_file", "delete_file", "call_tool", "noop"]

SCENARIO_ACTION_TYPES: tuple[ScenarioActionType, ...] = (
    "write_text",
    "touch_file",
    "delete_file",
    "call_tool",
    "noop",
)


class ScenarioScenarioError(ValueError):
    """Raised when a simulated scenario fixture is malformed."""


@dataclass(frozen=True)
class ScenarioAction:
    type: ScenarioActionType
    path: str | None = None
    content: str | None = None
    tool_name: str | None = None
    arguments: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        if self.type not in SCENARIO_ACTION_TYPES:
            raise ScenarioScenarioError(f"Unknown scenario action type: {self.type!r}.")
        if self.type in ("write_text", "touch_file", "delete_file"):
            if not isinstance(self.path, str) or not self.path.strip():
                raise ScenarioScenarioError(
                    f"Action type {self.type!r} requires a non-empty path."
                )
        if self.type == "write_text" and self.content is None:
            raise ScenarioScenarioError("write_text actions require content.")
        if self.type == "call_tool":
            if not isinstance(self.tool_name, str) or not self.tool_name.strip():
                raise ScenarioScenarioError("call_tool actions require a non-empty tool_name.")
            if self.arguments is not None and not isinstance(self.arguments, dict):
                raise ScenarioScenarioError("call_tool arguments must be a dictionary.")


@dataclass(frozen=True)
class SimulatedScenario:
    name: str
    actions: tuple[ScenarioAction, ...] = ()
    exit_reason: RunExitReason = "completed"
    usage: UsageRecord = field(default_factory=UsageRecord)
    details: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ScenarioScenarioError("Scenario name must be a non-empty string.")
        if self.exit_reason not in RUN_EXIT_REASONS:
            raise ScenarioScenarioError(f"Unknown scenario exit reason: {self.exit_reason!r}.")
        if not isinstance(self.actions, tuple):
            raise ScenarioScenarioError("actions must be a tuple.")
        if not isinstance(self.details, dict):
            raise ScenarioScenarioError("details must be a dictionary.")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SimulatedScenario":
        actions = tuple(ScenarioAction(**action) for action in data.get("actions", ()))
        usage_data = data.get("usage", {})
        usage = UsageRecord(**usage_data)
        return cls(
            name=data["name"],
            actions=actions,
            exit_reason=data.get("exit_reason", "completed"),
            usage=usage,
            details=data.get("details", {}),
        )


def load_scenario(path: str | Path) -> SimulatedScenario:
    fixture_path = Path(path).expanduser().resolve()
    data = json.loads(fixture_path.read_text(encoding="utf-8"))
    return SimulatedScenario.from_dict(data)

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import re
from typing import Callable

from .mission_contract import create_mission
from .mission_driver import MissionDriveResult, MissionDriver
from .node_contract import node_layout
from .node_record import update_node_record
from .orchestrator_progression import NodeProgressionEngine

DEFAULT_LIVE_CANARY_GOAL = (
    "Write a short operator note explaining what Open-Eywa is, why the node is the durable "
    "unit of work, and which mission files a human should inspect first."
)


@dataclass(frozen=True)
class LiveCanaryConfig:
    mission_path: str
    goal_text: str
    root_agent_mode: str = "worker"
    mission_id: str | None = None
    max_iterations: int = 40


def build_default_live_canary_mission_path(
    project_root: str | Path,
    *,
    label: str = "tiny-live-canary",
    now: datetime | None = None,
) -> Path:
    root = Path(project_root).expanduser().resolve()
    current_time = now or datetime.now()
    timestamp = current_time.strftime("%Y%m%d-%H%M%S")
    if now is None:
        timestamp = f"{timestamp}-{current_time.microsecond:06d}"
    slug = _slugify(label)
    base_name = f"{timestamp}-{slug}"
    candidate = root / "missions" / "live-canaries" / base_name
    suffix = 1
    while candidate.exists():
        candidate = root / "missions" / "live-canaries" / f"{base_name}-{suffix:03d}"
        suffix += 1
    return candidate


def run_live_canary(
    progression_engine: NodeProgressionEngine,
    config: LiveCanaryConfig,
) -> MissionDriveResult:
    mission_path = Path(config.mission_path).expanduser().resolve()
    create_mission(mission_path, goal_text=config.goal_text)

    root_layout = node_layout(mission_path / "tree" / "root")
    update_node_record(
        root_layout,
        lambda record: record.setdefault("control", {}).__setitem__(
            "next_role", config.root_agent_mode.strip()
        ),
    )

    return MissionDriver(progression_engine).drive_until_stable(
        mission_path,
        mission_id=config.mission_id,
        max_iterations=config.max_iterations,
    )


def _slugify(text: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "-", text).strip("-").lower()
    return slug or "live-canary"

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import re
from typing import Callable

from .mission_contract import create_mission
from .mission_driver import MissionDriveResult, MissionDriver
from .node_contract import node_layout, write_text
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
    slug = _slugify(label)
    return root / "missions" / "live-canaries" / f"{timestamp}-{slug}"


def run_live_canary(
    progression_engine: NodeProgressionEngine,
    config: LiveCanaryConfig,
) -> MissionDriveResult:
    mission_path = Path(config.mission_path).expanduser().resolve()
    create_mission(mission_path, goal_text=config.goal_text)

    root_layout = node_layout(mission_path / "tree" / "root")
    write_text(root_layout.agent_mode_file, config.root_agent_mode.strip() + "\n")

    return MissionDriver(progression_engine).drive_until_stable(
        mission_path,
        mission_id=config.mission_id,
        max_iterations=config.max_iterations,
    )


def _slugify(text: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "-", text).strip("-").lower()
    return slug or "live-canary"

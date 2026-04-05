from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .node_contract import create_node, write_text


@dataclass(frozen=True)
class MissionLayout:
    root: Path

    @property
    def mission_goal_file(self) -> Path:
        return self.root / "mission-goal.md"

    @property
    def tree_dir(self) -> Path:
        return self.root / "tree"

    @property
    def root_node_dir(self) -> Path:
        return self.tree_dir / "root"

    @property
    def system_dir(self) -> Path:
        return self.root / "system"

    @property
    def mission_events_log_file(self) -> Path:
        return self.system_dir / "mission-events.jsonl"

    @property
    def mission_summary_file(self) -> Path:
        return self.system_dir / "mission-summary.json"


def mission_layout(mission_path: str | Path) -> MissionLayout:
    return MissionLayout(Path(mission_path).expanduser().resolve())


def create_mission(
    mission_path: str | Path,
    *,
    goal_text: str,
) -> MissionLayout:
    layout = mission_layout(mission_path)
    layout.root.mkdir(parents=True, exist_ok=True)
    layout.tree_dir.mkdir(parents=True, exist_ok=True)
    layout.system_dir.mkdir(parents=True, exist_ok=True)
    write_text(layout.mission_goal_file, goal_text.rstrip() + "\n")

    if not layout.root_node_dir.exists():
        create_node(
            layout.root_node_dir,
            task_source_name="goal",
            task_text=goal_text,
        )
    return layout

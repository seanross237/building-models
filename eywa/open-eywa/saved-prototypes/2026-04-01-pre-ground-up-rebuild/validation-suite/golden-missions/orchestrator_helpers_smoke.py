#!/usr/bin/env python3
from __future__ import annotations

import sys
import tempfile
from pathlib import Path


def bootstrap() -> Path:
    repo_root = Path(__file__).resolve().parents[2]
    system_root = repo_root / "system"
    if str(system_root) not in sys.path:
        sys.path.insert(0, str(system_root))
    return repo_root


def main() -> int:
    bootstrap()
    from orchestrator.main import Orchestrator

    with tempfile.TemporaryDirectory() as tmp:
        mission_dir = Path(tmp) / "mission"
        mission_dir.mkdir(parents=True, exist_ok=True)
        (mission_dir / "mission-goal.md").write_text("Test mission goal", encoding="utf-8")

        orchestrator = Orchestrator(mission_dir)
        orchestrator._bootstrap_mission()
        root = mission_dir / "tree" / "root"
        assert (root / "input" / "goal.md").exists()
        assert (root / "for-orchestrator" / "agent-mode").read_text(encoding="utf-8").strip() == "planner"

        plan = """## Plan
Status: approved
Review: low

### Step 1: first-task
Goal: Do the first task clearly.
Complexity: 3
Importance: 4
Dependencies: none
Independent: yes
Confidence: medium
Verifiable: yes
"""
        (root / "output").mkdir(exist_ok=True)
        (root / "output" / "plan.md").write_text(plan, encoding="utf-8")
        next_step = orchestrator.parse_next_step(root)
        assert next_step is not None
        orchestrator.create_child(root, *next_step)
        child = root / "children" / "step-01-first-task"
        assert child.exists()
        assert (child / "input" / "parent-instructions.md").exists()
        assert (child / "for-orchestrator" / "agent-mode").read_text(encoding="utf-8").strip() in {"worker", "planner"}

    print("orchestrator_helpers_smoke: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

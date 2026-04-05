#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


def bootstrap() -> None:
    system_root = Path(__file__).resolve().parents[1]
    if str(system_root) not in sys.path:
        sys.path.insert(0, str(system_root))


def main() -> int:
    bootstrap()
    from orchestrator.main import main as orchestrator_main

    if len(sys.argv) != 2:
        raise SystemExit("Usage: run_mission.py <mission_dir>")
    mission_dir = Path(sys.argv[1]).resolve()
    return orchestrator_main(str(mission_dir))


if __name__ == "__main__":
    raise SystemExit(main())

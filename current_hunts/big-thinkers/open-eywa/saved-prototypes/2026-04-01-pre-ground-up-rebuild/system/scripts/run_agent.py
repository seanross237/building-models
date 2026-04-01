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
    from runtime.agent_runner import run_agent

    if len(sys.argv) != 4:
        raise SystemExit("Usage: run_agent.py <role> <node_path> <mission_dir>")
    role = sys.argv[1]
    node_path = Path(sys.argv[2])
    mission_dir = Path(sys.argv[3])
    return run_agent(role, node_path, mission_dir)


if __name__ == "__main__":
    raise SystemExit(main())

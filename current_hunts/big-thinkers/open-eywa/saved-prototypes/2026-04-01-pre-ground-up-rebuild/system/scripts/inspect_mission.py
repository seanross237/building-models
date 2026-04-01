#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


def summarize(mission_dir: Path) -> dict:
    tree_root = mission_dir / "tree"
    nodes = list(tree_root.rglob("this-nodes-current-status"))
    statuses: dict[str, int] = {}
    for status_file in nodes:
        status = status_file.read_text(encoding="utf-8").strip()
        statuses[status] = statuses.get(status, 0) + 1
    usage_path = mission_dir / "usage.jsonl"
    usage_entries = 0
    total_tokens = 0
    total_cost = 0.0
    if usage_path.exists():
        for line in usage_path.read_text(encoding="utf-8").splitlines():
            entry = json.loads(line)
            usage_entries += 1
            usage = entry.get("usage", {})
            total_tokens += usage.get("total_tokens", 0)
            total_cost += float(usage.get("cost", 0.0))
    return {
        "mission": mission_dir.name,
        "node_count": len(nodes),
        "statuses": statuses,
        "usage_entries": usage_entries,
        "total_tokens": total_tokens,
        "total_cost": round(total_cost, 6),
    }


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: inspect_mission.py <mission_dir>")
    mission_dir = Path(sys.argv[1]).resolve()
    print(json.dumps(summarize(mission_dir), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

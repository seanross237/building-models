from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from system.orchestrator import (
    DEFAULT_LIVE_CANARY_GOAL,
    LiveCanaryConfig,
    NodeProgressionEngine,
    build_default_live_canary_mission_path,
    run_live_canary,
)
from system.runtime import (
    LIVE_CANARY_DEFAULT_MODEL,
    LiveCanaryRuntimeSettings,
    build_openrouter_runtime_for_live_canary,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a tiny live Open-Eywa canary mission.")
    parser.add_argument(
        "--goal",
        default=DEFAULT_LIVE_CANARY_GOAL,
        help="Mission goal text for the canary.",
    )
    parser.add_argument(
        "--mission-path",
        default=None,
        help="Optional mission directory path. Defaults to missions/live-canaries/<timestamp>-tiny-live-canary.",
    )
    parser.add_argument(
        "--model",
        default=LIVE_CANARY_DEFAULT_MODEL,
        help="Cheap non-Chinese model to use for all current canary roles.",
    )
    parser.add_argument(
        "--root-role",
        default="worker",
        help="Role to run at the root for the tiny canary. Defaults to worker.",
    )
    parser.add_argument(
        "--mission-id",
        default=None,
        help="Optional explicit mission id.",
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=40,
        help="Maximum mission-driving iterations before failing.",
    )
    parser.add_argument(
        "--referer-url",
        default=None,
        help="Optional HTTP-Referer header for OpenRouter.",
    )
    parser.add_argument(
        "--title",
        default="Open-Eywa Canary",
        help="Optional X-Title header for OpenRouter.",
    )
    parser.add_argument(
        "--no-generation-stats",
        action="store_true",
        help="Skip follow-up generation stats requests.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    mission_path = (
        Path(args.mission_path).expanduser().resolve()
        if args.mission_path
        else build_default_live_canary_mission_path(PROJECT_ROOT)
    )

    runtime = build_openrouter_runtime_for_live_canary(
        LiveCanaryRuntimeSettings(
            model_name=args.model,
            referer_url=args.referer_url,
            title=args.title,
            fetch_generation_stats=not args.no_generation_stats,
        )
    )
    progression_engine = NodeProgressionEngine(runtime)
    result = run_live_canary(
        progression_engine,
        LiveCanaryConfig(
            mission_path=str(mission_path),
            goal_text=args.goal,
            root_agent_mode=args.root_role,
            mission_id=args.mission_id,
            max_iterations=args.max_iterations,
        ),
    )

    summary_path = mission_path / "system" / "mission-summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8")) if summary_path.exists() else {}
    output = {
        "mission_path": str(mission_path),
        "mission_id": result.mission_id,
        "root_node_path": result.root_node_path,
        "final_status": result.final_status,
        "terminal_outcome": result.terminal_outcome,
        "failure_reason": result.failure_reason,
        "node_count": result.node_count,
        "run_count": result.run_count,
        "summary_path": str(summary_path),
        "summary": summary,
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

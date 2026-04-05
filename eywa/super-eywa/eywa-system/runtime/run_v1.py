#!/usr/bin/env python3
"""Run the Super-Eywa v1 scaffold."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from eywa_runtime.engine import EywaEngine


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the Super-Eywa v1 runtime.")
    parser.add_argument("--task", required=True, help="Top-level task text to run.")
    parser.add_argument("--run-id", help="Optional explicit run ID.")
    parser.add_argument(
        "--runtime-provider",
        choices=["deterministic", "openrouter"],
        help="Optional runtime provider override.",
    )
    parser.add_argument(
        "--model",
        help="Optional model override.",
    )
    parser.add_argument(
        "--variables-json",
        help="Optional JSON object of run-level variable overrides.",
    )
    parser.add_argument(
        "--run-history-root",
        default=str(Path(__file__).resolve().parents[2] / "data-system" / "run-history"),
        help="Directory where run folders should be written.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    variable_overrides = json.loads(args.variables_json) if args.variables_json else {}
    if args.runtime_provider:
        variable_overrides["runtime_provider"] = args.runtime_provider
    if args.model:
        variable_overrides["model"] = args.model
    engine = EywaEngine(Path(args.run_history_root))
    result = engine.run(
        task_text=args.task,
        run_id=args.run_id,
        run_level_variables=variable_overrides or None,
    )

    print(f"run_id={result.run_id}")
    print(f"run_dir={result.run_dir}")
    print(f"root_node_id={result.root_node_id}")
    print(f"node_count={result.node_count}")
    print(f"timeline_path={result.timeline_path}")
    print(f"summary_path={result.summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Validate a stored Super-Eywa v1 run folder."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


THIS_DIR = Path(__file__).resolve().parent
RUNTIME_DIR = THIS_DIR.parents[1] / "eywa-system" / "runtime"
if str(RUNTIME_DIR) not in sys.path:
    sys.path.insert(0, str(RUNTIME_DIR))

from eywa_runtime.validation import RunValidationError, validate_run_directory  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate a stored Super-Eywa v1 run.")
    parser.add_argument("run_dir", help="Path to the run directory.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    run_dir = Path(args.run_dir).resolve()
    try:
        summary = validate_run_directory(run_dir)
    except RunValidationError as exc:
        print(f"invalid: {exc}")
        return 1

    print(f"valid run: {summary['run_id']}")
    print(f"root_node_id={summary['root_node_id']}")
    print(f"node_count={summary['node_count']}")
    print(f"status={summary['status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

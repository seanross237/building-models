#!/usr/bin/env python3
"""Launch one supervised MX1 worker per question/family pair for a benchmark."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys


THIS_DIR = Path(__file__).resolve().parent
REPO_ROOT = THIS_DIR.parents[1]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Launch a supervised MX1 benchmark fanout.")
    parser.add_argument("--benchmark-file", required=True)
    parser.add_argument("--loop-label", required=True)
    parser.add_argument("--logs-root", default=str(THIS_DIR / "mx1-logs"))
    parser.add_argument("--runtime-provider", default="openrouter")
    parser.add_argument("--model", default="google/gemma-4-26b-a4b-it")
    parser.add_argument("--sync-supabase", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    benchmark_path = Path(args.benchmark_file).resolve()
    benchmark = json.loads(benchmark_path.read_text(encoding="utf-8"))
    log_root = Path(args.logs_root).resolve() / args.loop_label
    log_root.mkdir(parents=True, exist_ok=True)

    launched: list[dict[str, object]] = []
    for question_entry in list(benchmark.get("questions") or []):
        question_id = str(question_entry.get("question_id") or "").strip()
        iterations_target = question_entry.get("iterations_target")
        exploration_iterations = question_entry.get("exploration_iterations")
        for family in list(benchmark.get("families") or []):
            family_name = str(family).strip()
            log_path = log_root / f"{question_id}__{family_name}.log"
            handle = log_path.open("ab")
            command = [
                sys.executable,
                str(THIS_DIR / "run_mx1_supervised_worker_v1.py"),
                "--benchmark-file",
                str(benchmark_path),
                "--question-id",
                question_id,
                "--family",
                family_name,
                "--loop-label",
                args.loop_label,
                "--runtime-provider",
                args.runtime_provider,
                "--model",
                args.model,
            ]
            if iterations_target is not None:
                command.extend(["--iterations-target", str(int(iterations_target))])
            if exploration_iterations is not None:
                command.extend(["--exploration-iterations", str(int(exploration_iterations))])
            if args.sync_supabase:
                command.append("--sync-supabase")

            proc = subprocess.Popen(
                command,
                stdout=handle,
                stderr=subprocess.STDOUT,
                cwd=str(REPO_ROOT),
                start_new_session=True,
            )
            launched.append(
                {
                    "question_id": question_id,
                    "family": family_name,
                    "pid": proc.pid,
                    "log_path": str(log_path),
                    "iterations_target": iterations_target,
                }
            )

    print(json.dumps({"launched": launched}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Keep one MX1 question/family loop running until the manifest reaches completion."""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path


THIS_DIR = Path(__file__).resolve().parent
REPO_ROOT = THIS_DIR.parents[1]
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from mx1_loop_v1 import build_loop_id, build_loop_manifest_path, load_json  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Supervise one MX1 question/family worker until complete.")
    parser.add_argument("--benchmark-file", default=str(THIS_DIR / "benchmarks" / "mx1-three-question-v1.json"))
    parser.add_argument("--question-id", required=True)
    parser.add_argument("--family", required=True)
    parser.add_argument("--loop-label", required=True)
    parser.add_argument("--loops-root", default=str(THIS_DIR / "mx1-loops"))
    parser.add_argument("--run-history-root", default=str(REPO_ROOT / "data-system" / "run-history"))
    parser.add_argument("--grading-runs-root", default=str(THIS_DIR / "runs"))
    parser.add_argument("--tutoring-root", default=str(THIS_DIR / "mx1-tutoring"))
    parser.add_argument("--runtime-provider", default="openrouter")
    parser.add_argument("--model", default="google/gemma-4-26b-a4b-it")
    parser.add_argument("--execute-prompt-file", default=str(THIS_DIR / "prompt-experiments" / "mx1-pilot-v1" / "execute_prompt_v1.txt"))
    parser.add_argument("--iterations-target", type=int)
    parser.add_argument("--exploration-iterations", type=int)
    parser.add_argument("--sync-supabase", action="store_true")
    parser.add_argument("--retry-delay-seconds", type=int, default=15)
    parser.add_argument("--max-retries", type=int, default=0, help="0 means retry forever.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    manifest_path = build_loop_manifest_path(
        question_id=args.question_id,
        family=args.family,
        loop_id=build_loop_id(args.question_id, args.family, args.loop_label),
        loops_root=Path(args.loops_root).resolve(),
    )

    retries = 0
    while True:
        if _is_complete(manifest_path, args.iterations_target):
            print(f"complete manifest={manifest_path}")
            return 0

        command = _build_command(args)
        print(f"launching question_id={args.question_id} family={args.family} retries={retries}")
        result = subprocess.run(command, cwd=str(REPO_ROOT))

        if _is_complete(manifest_path, args.iterations_target):
            print(f"complete manifest={manifest_path}")
            return 0

        retries += 1
        if args.max_retries and retries > args.max_retries:
            print(f"max_retries_exceeded question_id={args.question_id} family={args.family}", file=sys.stderr)
            return result.returncode or 1

        print(
            f"retrying question_id={args.question_id} family={args.family} "
            f"exit_code={result.returncode} delay_seconds={args.retry_delay_seconds}"
        )
        time.sleep(max(1, int(args.retry_delay_seconds)))


def _is_complete(manifest_path: Path, iterations_target: int | None) -> bool:
    if not manifest_path.exists():
        return False
    manifest = load_json(manifest_path)
    summary = manifest.get("history_summary") or {}
    target = int(iterations_target or manifest.get("iterations_target") or 0)
    return int(summary.get("iterations_completed") or 0) >= target > 0


def _build_command(args: argparse.Namespace) -> list[str]:
    command = [
        sys.executable,
        str(THIS_DIR / "run_mx1_sweep_v1.py"),
        "--benchmark-file",
        str(Path(args.benchmark_file).resolve()),
        "--question-id",
        args.question_id,
        "--family",
        args.family,
        "--loop-label",
        args.loop_label,
        "--loops-root",
        str(Path(args.loops_root).resolve()),
        "--run-history-root",
        str(Path(args.run_history_root).resolve()),
        "--grading-runs-root",
        str(Path(args.grading_runs_root).resolve()),
        "--tutoring-root",
        str(Path(args.tutoring_root).resolve()),
        "--runtime-provider",
        args.runtime_provider,
        "--model",
        args.model,
        "--execute-prompt-file",
        str(Path(args.execute_prompt_file).resolve()),
        "--skip-complete",
    ]
    if args.iterations_target:
        command.extend(["--iterations-target", str(args.iterations_target)])
    if args.exploration_iterations:
        command.extend(["--exploration-iterations", str(args.exploration_iterations)])
    if args.sync_supabase:
        command.append("--sync-supabase")
    return command


if __name__ == "__main__":
    raise SystemExit(main())

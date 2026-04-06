#!/usr/bin/env python3
"""Run a full MX1 loop end to end for one question and one family."""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from mx1_loop_v1 import build_loop_id, build_loop_manifest_path, load_json  # noqa: E402
from grading_methods.simple_grade_v1 import parse_question_file  # noqa: E402


RUN_PILOT = THIS_DIR / "run_mx1_pilot_v1.py"
RUN_TUTOR = THIS_DIR / "run_mx1_tutor_v1.py"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a full MX1 loop end to end.")
    parser.add_argument("--question-file", required=True)
    parser.add_argument("--family", required=True, choices=["transmute", "delegate"])
    parser.add_argument("--loop-label", required=True)
    parser.add_argument("--runtime-provider", default="openrouter", choices=["deterministic", "openrouter"])
    parser.add_argument("--model", default="google/gemma-4-26b-a4b-it")
    parser.add_argument("--tutor-provider", default="same", choices=["same", "deterministic", "openrouter"])
    parser.add_argument("--iterations-target", type=int, default=10)
    parser.add_argument("--retry-count", type=int, default=2)
    parser.add_argument("--sync-supabase", action="store_true")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    question_path = Path(args.question_file).resolve()
    question_case = parse_question_file(question_path)
    loop_id = build_loop_id(question_case.question_id, args.family, args.loop_label)
    manifest_path = build_loop_manifest_path(
        question_id=question_case.question_id,
        family=args.family,
        loop_id=loop_id,
    )

    _run_with_retry(
        [
            "python3",
            str(RUN_PILOT),
            "--action",
            "init",
            "--question-file",
            str(question_path),
            "--family",
            args.family,
            "--loop-label",
            args.loop_label,
            "--runtime-provider",
            args.runtime_provider,
            "--model",
            args.model,
            "--iterations-target",
            str(args.iterations_target),
            *(_sync_flag(args.sync_supabase)),
        ],
        retry_count=args.retry_count,
    )

    manifest = load_json(manifest_path)
    if not any(str(attempt.get("kind") or "") == "baseline" for attempt in manifest.get("attempts") or []):
        stdout = _run_with_retry(
            [
                "python3",
                str(RUN_PILOT),
                "--action",
                "baseline",
                "--question-file",
                str(question_path),
                "--family",
                args.family,
                "--loop-label",
                args.loop_label,
                "--runtime-provider",
                args.runtime_provider,
                "--model",
                args.model,
                *(_sync_flag(args.sync_supabase)),
            ],
            retry_count=args.retry_count,
        )
        _print_compact("BASELINE", stdout)

    while True:
        manifest = load_json(manifest_path)
        summary = manifest.get("history_summary") or {}
        if int(summary.get("iterations_completed") or 0) >= args.iterations_target:
            break

        stdout = _run_with_retry(
            [
                "python3",
                str(RUN_PILOT),
                "--action",
                "iterate",
                "--question-file",
                str(question_path),
                "--family",
                args.family,
                "--loop-label",
                args.loop_label,
                "--runtime-provider",
                args.runtime_provider,
                "--model",
                args.model,
                *(_sync_flag(args.sync_supabase)),
            ],
            retry_count=args.retry_count,
        )
        _print_compact("ITER", stdout)

        manifest = load_json(manifest_path)
        summary = manifest.get("history_summary") or {}
        if int(summary.get("iterations_completed") or 0) >= args.iterations_target:
            break

        stdout = _run_with_retry(
            [
                "python3",
                str(RUN_TUTOR),
                "--manifest",
                str(manifest_path),
                "--tutor-provider",
                args.tutor_provider,
                *(_sync_flag(args.sync_supabase)),
            ],
            retry_count=args.retry_count,
        )
        _print_compact("TUTOR", stdout)

    final_manifest = load_json(manifest_path)
    print(f"manifest={manifest_path}")
    print(f"status={final_manifest.get('status')}")
    print(f"iterations_completed={(final_manifest.get('history_summary') or {}).get('iterations_completed')}")
    print(f"best_iteration_index={(final_manifest.get('history_summary') or {}).get('best_iteration_index')}")
    print(f"best_score={(final_manifest.get('history_summary') or {}).get('best_score')}")
    return 0


def _sync_flag(sync_supabase: bool) -> list[str]:
    return ["--sync-supabase"] if sync_supabase else []


def _run_with_retry(command: list[str], *, retry_count: int) -> str:
    last_error: subprocess.CalledProcessError | None = None
    for attempt in range(1, retry_count + 1):
        try:
            completed = subprocess.run(
                command,
                cwd=THIS_DIR.parents[1],
                check=True,
                capture_output=True,
                text=True,
            )
            return completed.stdout
        except subprocess.CalledProcessError as exc:
            last_error = exc
            print(f"retry={attempt}/{retry_count} failed command={' '.join(command)}", file=sys.stderr)
            if exc.stderr.strip():
                print(exc.stderr.strip()[-1200:], file=sys.stderr)
            time.sleep(2)
    raise last_error if last_error is not None else RuntimeError("Command failed without error details.")


def _parse_stdout(stdout: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for line in stdout.splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        parsed[key.strip()] = value.strip()
    return parsed


def _print_compact(prefix: str, stdout: str) -> None:
    parsed = _parse_stdout(stdout)
    if prefix == "TUTOR":
        print(
            f"{prefix}: iteration={parsed.get('iteration_index')} action={parsed.get('recommendation_action')} "
            f"new_prompt_text={parsed.get('new_prompt_text')}"
        )
        return
    print(
        f"{prefix}: run_id={parsed.get('run_id')} score={parsed.get('score')} correct={parsed.get('correct')} "
        f"tokens={parsed.get('total_tokens')} ms={parsed.get('total_wall_time_ms')}"
    )


if __name__ == "__main__":
    raise SystemExit(main())

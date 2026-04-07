#!/usr/bin/env python3
"""Keep one MX1 question-family loop advancing until completion."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import time


THIS_DIR = Path(__file__).resolve().parent
REPO_ROOT = THIS_DIR.parents[1]
RUNTIME_DIR = REPO_ROOT / "eywa-system" / "runtime"
MX1_RESULTS_DIR = REPO_ROOT / "data-system" / "derived-views" / "mx1-results"
if str(RUNTIME_DIR) not in sys.path:
    sys.path.insert(0, str(RUNTIME_DIR))
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))
if str(MX1_RESULTS_DIR) not in sys.path:
    sys.path.insert(0, str(MX1_RESULTS_DIR))

from build_mx1_results_page import build_results_page  # noqa: E402
from mx1_loop_v1 import build_loop_id, build_loop_manifest_path, load_json  # noqa: E402
from question_bank_v1 import load_question_case  # noqa: E402
from run_mx1_pilot_v1 import DEFAULT_EXECUTE_PROMPT_FILE  # noqa: E402
from run_mx1_sweep_v1 import DEFAULT_BENCHMARK_FILE, _run_one_loop  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run one MX1 question-family loop resiliently.")
    parser.add_argument("--benchmark-file", default=str(DEFAULT_BENCHMARK_FILE))
    parser.add_argument("--question-id", required=True)
    parser.add_argument("--family", required=True)
    parser.add_argument("--loop-label", required=True)
    parser.add_argument("--loops-root", default=str(THIS_DIR / "mx1-loops"))
    parser.add_argument("--run-history-root", default=str(REPO_ROOT / "data-system" / "run-history"))
    parser.add_argument("--grading-runs-root", default=str(THIS_DIR / "runs"))
    parser.add_argument("--tutoring-root", default=str(THIS_DIR / "mx1-tutoring"))
    parser.add_argument("--runtime-provider")
    parser.add_argument("--model")
    parser.add_argument("--execute-prompt-file", default=str(DEFAULT_EXECUTE_PROMPT_FILE))
    parser.add_argument("--iterations-target", type=int)
    parser.add_argument("--exploration-iterations", type=int)
    parser.add_argument("--sync-supabase", action="store_true")
    parser.add_argument("--retry-delay-seconds", type=float, default=10.0)
    parser.add_argument("--max-retries", type=int, default=0, help="0 means unlimited retries.")
    parser.add_argument("--build-view-on-exit", action="store_true")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    benchmark = json.loads(Path(args.benchmark_file).resolve().read_text(encoding="utf-8"))
    loop_label = str(args.loop_label)
    runtime_provider = str(args.runtime_provider or benchmark.get("runtime_provider") or "openrouter")
    model = str(args.model or benchmark.get("model") or "google/gemma-4-26b-a4b-it")
    iterations_target = int(args.iterations_target or benchmark.get("iterations_target") or 20)
    exploration_iterations = int(args.exploration_iterations or benchmark.get("exploration_iterations") or 3)
    loops_root = Path(args.loops_root).resolve()
    run_history_root = Path(args.run_history_root).resolve()
    grading_runs_root = Path(args.grading_runs_root).resolve()
    tutoring_root = Path(args.tutoring_root).resolve()
    execute_prompt_path = Path(args.execute_prompt_file).resolve()
    execute_prompt_text = execute_prompt_path.read_text(encoding="utf-8").strip()
    question_case = load_question_case(question_id=args.question_id)
    question_path = question_case.source_path
    manifest_path = build_loop_manifest_path(
        question_id=question_case.question_id,
        family=args.family,
        loop_id=build_loop_id(question_case.question_id, args.family, loop_label),
        loops_root=loops_root,
    )

    retries = 0
    while True:
        manifest = load_json(manifest_path) if manifest_path.exists() else None
        completed = int(((manifest or {}).get("history_summary") or {}).get("iterations_completed") or 0)
        if completed >= iterations_target:
            break
        try:
            manifest = _run_one_loop(
                question_case=question_case,
                question_path=question_path,
                family=args.family,
                loop_label=loop_label,
                loops_root=loops_root,
                run_history_root=run_history_root,
                grading_runs_root=grading_runs_root,
                tutoring_root=tutoring_root,
                runtime_provider=runtime_provider,
                model=model,
                execute_prompt_text=execute_prompt_text,
                execute_prompt_path=execute_prompt_path,
                iterations_target=iterations_target,
                exploration_iterations=exploration_iterations,
                sync_supabase=args.sync_supabase,
                skip_complete=False,
            )
            completed = int((manifest.get("history_summary") or {}).get("iterations_completed") or 0)
            if completed >= iterations_target:
                break
        except KeyboardInterrupt:
            raise
        except Exception as exc:
            retries += 1
            print(
                json.dumps(
                    {
                        "event": "mx1_resilient_retry",
                        "question_id": args.question_id,
                        "family": args.family,
                        "loop_label": loop_label,
                        "retry_count": retries,
                        "error": repr(exc),
                    }
                ),
                flush=True,
            )
            if args.max_retries and retries >= args.max_retries:
                raise
            time.sleep(max(args.retry_delay_seconds, 1.0))

    final_manifest = load_json(manifest_path)
    if args.build_view_on_exit:
        build_results_page(
            benchmark_path=Path(args.benchmark_file).resolve(),
            loops_root=loops_root,
            output_path=REPO_ROOT / "data-system" / "derived-views" / "mx1-results" / "index.html",
            loop_label=loop_label,
        )
    print(
        json.dumps(
            {
                "event": "mx1_resilient_complete",
                "question_id": args.question_id,
                "family": args.family,
                "loop_label": loop_label,
                "status": final_manifest.get("status"),
                "iterations_completed": (final_manifest.get("history_summary") or {}).get("iterations_completed"),
                "best_score": (final_manifest.get("history_summary") or {}).get("best_score"),
                "manifest_path": str(manifest_path),
            },
            indent=2,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

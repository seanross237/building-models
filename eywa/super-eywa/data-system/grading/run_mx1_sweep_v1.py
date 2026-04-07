#!/usr/bin/env python3
"""Run a full MX1 sweep across a benchmark manifest."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from types import SimpleNamespace
from typing import Any


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

try:  # noqa: E402
    from build_mx1_results_page import build_results_page
except ModuleNotFoundError:  # pragma: no cover - optional convenience only
    build_results_page = None
from mx1_loop_v1 import build_loop_id, build_loop_manifest_path, load_json, write_json  # noqa: E402
from question_bank_v1 import load_question_case  # noqa: E402
from run_mx1_pilot_v1 import (  # noqa: E402
    DEFAULT_EXECUTE_PROMPT_FILE,
    DEFAULT_LOOPS_ROOT,
    _current_prompt_path,
    _load_or_create_manifest,
    _resolve_starter_prompt_path,
    _run_family_iteration,
)
from run_mx1_tutor_v1 import (  # noqa: E402
    DEFAULT_TUTORING_ROOT,
    _apply_tutor_result,
    _apply_tutor_result_to_grading_record,
)
from mx1_tutor_v1 import run_mx1_tutor  # noqa: E402
from sync_to_supabase_v1 import load_supabase_config, sync_grading_record  # noqa: E402


DEFAULT_BENCHMARK_FILE = THIS_DIR / "benchmarks" / "mx1-three-question-v1.json"
DEFAULT_RESULTS_PAGE = REPO_ROOT / "data-system" / "derived-views" / "mx1-results" / "index.html"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the MX1 sweep across one or more questions/families.")
    parser.add_argument("--benchmark-file", default=str(DEFAULT_BENCHMARK_FILE))
    parser.add_argument("--question-id", action="append", dest="question_ids")
    parser.add_argument("--family", action="append", dest="families")
    parser.add_argument("--loop-label")
    parser.add_argument("--loops-root", default=str(DEFAULT_LOOPS_ROOT))
    parser.add_argument("--run-history-root", default=str(REPO_ROOT / "data-system" / "run-history"))
    parser.add_argument("--grading-runs-root", default=str(THIS_DIR / "runs"))
    parser.add_argument("--tutoring-root", default=str(DEFAULT_TUTORING_ROOT))
    parser.add_argument("--runtime-provider", choices=["deterministic", "openrouter"])
    parser.add_argument("--model")
    parser.add_argument("--execute-prompt-file", default=str(DEFAULT_EXECUTE_PROMPT_FILE))
    parser.add_argument("--iterations-target", type=int)
    parser.add_argument("--exploration-iterations", type=int)
    parser.add_argument("--sync-supabase", action="store_true")
    parser.add_argument("--skip-complete", action="store_true")
    parser.add_argument("--build-view", action="store_true")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    benchmark = json.loads(Path(args.benchmark_file).resolve().read_text(encoding="utf-8"))
    question_ids = set(args.question_ids or [])
    family_filters = set(args.families or [])
    loop_label = str(args.loop_label or benchmark.get("benchmark_id") or "mx1_sweep_v1")
    runtime_provider = str(args.runtime_provider or benchmark.get("runtime_provider") or "openrouter")
    model = str(args.model or benchmark.get("model") or "google/gemma-4-26b-a4b-it")
    default_iterations_target = int(args.iterations_target or benchmark.get("iterations_target") or 20)
    default_exploration_iterations = int(args.exploration_iterations or benchmark.get("exploration_iterations") or 3)
    loops_root = Path(args.loops_root).resolve()
    run_history_root = Path(args.run_history_root).resolve()
    grading_runs_root = Path(args.grading_runs_root).resolve()
    tutoring_root = Path(args.tutoring_root).resolve()
    execute_prompt_path = Path(args.execute_prompt_file).resolve()
    execute_prompt_text = execute_prompt_path.read_text(encoding="utf-8").strip()

    completed_loops: list[dict[str, Any]] = []
    for question_entry in list(benchmark.get("questions") or []):
        question_id = str(question_entry.get("question_id") or "").strip()
        if question_ids and question_id not in question_ids:
            continue
        question_case = load_question_case(question_id=question_id)
        question_path = question_case.source_path
        iterations_target = int(question_entry.get("iterations_target") or default_iterations_target)
        exploration_iterations = int(question_entry.get("exploration_iterations") or default_exploration_iterations)
        for family in list(benchmark.get("families") or []):
            family_name = str(family).strip()
            if family_filters and family_name not in family_filters:
                continue

            manifest = _run_one_loop(
                question_case=question_case,
                question_path=question_path,
                family=family_name,
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
                skip_complete=args.skip_complete,
            )
            completed_loops.append(
                {
                    "question_id": question_id,
                    "family": family_name,
                    "manifest_path": str(
                        build_loop_manifest_path(
                            question_id=question_id,
                            family=family_name,
                            loop_id=build_loop_id(question_id, family_name, loop_label),
                            loops_root=loops_root,
                        )
                    ),
                    "status": manifest.get("status"),
                    "iterations_completed": (manifest.get("history_summary") or {}).get("iterations_completed"),
                    "best_score": (manifest.get("history_summary") or {}).get("best_score"),
                }
            )

    if args.build_view:
        if build_results_page is None:
            raise RuntimeError("build_mx1_results_page.py is not available, so --build-view cannot run.")
        build_results_page(
            benchmark_path=Path(args.benchmark_file).resolve(),
            loops_root=loops_root,
            output_path=DEFAULT_RESULTS_PAGE,
        )
        print(f"results_page={DEFAULT_RESULTS_PAGE}")

    print(json.dumps({"completed_loops": completed_loops}, indent=2))
    return 0


def _run_one_loop(
    *,
    question_case: Any,
    question_path: Path,
    family: str,
    loop_label: str,
    loops_root: Path,
    run_history_root: Path,
    grading_runs_root: Path,
    tutoring_root: Path,
    runtime_provider: str,
    model: str,
    execute_prompt_text: str,
    execute_prompt_path: Path,
    iterations_target: int,
    exploration_iterations: int,
    sync_supabase: bool,
    skip_complete: bool,
) -> dict[str, Any]:
    manifest_path = build_loop_manifest_path(
        question_id=question_case.question_id,
        family=family,
        loop_id=build_loop_id(question_case.question_id, family, loop_label),
        loops_root=loops_root,
    )
    starter_prompt_path = _resolve_starter_prompt_path(family, "")
    starter_prompt_text = starter_prompt_path.read_text(encoding="utf-8").strip()
    manifest = _load_or_create_manifest(
        manifest_path=manifest_path,
        question_case=question_case,
        question_path=question_path,
        family=family,
        runtime_provider=runtime_provider,
        model=model,
        starter_prompt_text=starter_prompt_text,
        execute_prompt_text=execute_prompt_text,
        starter_prompt_file=str(starter_prompt_path),
        execute_prompt_file=str(execute_prompt_path),
        loop_label=loop_label,
        iterations_target=iterations_target,
        exploration_iterations=exploration_iterations,
    )

    if skip_complete and (manifest.get("history_summary") or {}).get("iterations_completed", 0) >= iterations_target:
        return manifest

    while int((manifest.get("history_summary") or {}).get("iterations_completed") or 0) < iterations_target:
        args = SimpleNamespace(
            family=family,
            loop_id=manifest.get("loop_id"),
            loops_root=str(loops_root),
            run_history_root=str(run_history_root),
            grading_runs_root=str(grading_runs_root),
            runtime_provider=runtime_provider,
            model=model,
            label_prefix="mx1",
            max_depth=None,
            max_helpers=None,
            prompt_text=None,
            iteration_index=None,
            sync_supabase=sync_supabase,
        )
        _run_family_iteration(
            args=args,
            question_case=question_case,
            question_path=question_path,
            manifest_path=manifest_path,
            manifest=manifest,
            execute_prompt_text=execute_prompt_text,
            execute_prompt_path=execute_prompt_path,
        )
        manifest = load_json(manifest_path)
        if int((manifest.get("history_summary") or {}).get("iterations_completed") or 0) >= iterations_target:
            break

        latest_attempt = _latest_family_attempt(manifest, family=family)
        grading_record_path = Path(str(latest_attempt["grading_record_path"]))
        tutor_record = run_mx1_tutor(
            manifest_path=manifest_path,
            grading_record_path=grading_record_path,
            tutoring_root=tutoring_root,
            tutor_provider="same",
            tutor_model=None,
        )
        manifest = _apply_tutor_result(manifest, tutor_record)
        write_json(manifest_path, manifest)

        grading_record = load_json(grading_record_path)
        grading_record = _apply_tutor_result_to_grading_record(grading_record, manifest, tutor_record)
        write_json(grading_record_path, grading_record)
        if sync_supabase:
            supabase_config = load_supabase_config()
            sync_grading_record(config=supabase_config, grading_record_path=grading_record_path)

    return load_json(manifest_path)


def _latest_family_attempt(manifest: dict[str, Any], *, family: str) -> dict[str, Any]:
    matching = [
        attempt
        for attempt in list(manifest.get("attempts") or [])
        if str(attempt.get("kind") or "") == family
    ]
    if not matching:
        raise ValueError(f"No attempts found for family={family} in manifest {manifest.get('loop_id')}")
    return sorted(matching, key=lambda item: int(item.get("iteration_index") or 0))[-1]


if __name__ == "__main__":
    raise SystemExit(main())

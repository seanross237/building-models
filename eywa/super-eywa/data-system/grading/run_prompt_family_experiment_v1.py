#!/usr/bin/env python3
"""Run the first prompt-family experiment loop for Super-Eywa grading questions."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any


THIS_DIR = Path(__file__).resolve().parent
REPO_ROOT = THIS_DIR.parents[1]
RUNTIME_DIR = REPO_ROOT / "eywa-system" / "runtime"
if str(RUNTIME_DIR) not in sys.path:
    sys.path.insert(0, str(RUNTIME_DIR))
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from eywa_runtime.ids import make_run_id, utc_now_iso  # noqa: E402
from run_test_question_v1 import run_question_case  # noqa: E402
from sync_to_supabase_v1 import load_supabase_config, sync_experiment_summary  # noqa: E402


DEFAULT_BENCHMARK_FILE = THIS_DIR / "benchmarks" / "transmute-three-failures-v1.json"
DEFAULT_EXECUTE_PROMPT_FILE = THIS_DIR / "prompt-experiments" / "transmute-search-v1" / "execute_prompt_v1.txt"
DEFAULT_TRANSMUTE_PROMPT_FILE = (
    THIS_DIR / "prompt-experiments" / "transmute-search-v1" / "root_transmute_prompt_v1.txt"
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the first prompt-family experiment batch.")
    parser.add_argument("--benchmark-file", default=str(DEFAULT_BENCHMARK_FILE))
    parser.add_argument("--execute-prompt-file", default=str(DEFAULT_EXECUTE_PROMPT_FILE))
    parser.add_argument("--transmute-prompt-file", default=str(DEFAULT_TRANSMUTE_PROMPT_FILE))
    parser.add_argument("--runtime-provider", default="deterministic", choices=["deterministic", "openrouter"])
    parser.add_argument("--model", default="google/gemma-4-26b-a4b-it")
    parser.add_argument("--run-history-root", default=str(REPO_ROOT / "data-system" / "run-history"))
    parser.add_argument("--grading-runs-root", default=str(THIS_DIR / "runs"))
    parser.add_argument("--experiment-runs-root", default=str(THIS_DIR / "experiment-runs"))
    parser.add_argument("--experiment-label", default="starter")
    parser.add_argument("--run-id", help="Optional explicit experiment run id.")
    parser.add_argument("--sync-supabase", action="store_true")
    return parser


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def compute_variant_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    graded = [record for record in records if record["grading"]["score"] is not None]
    total_score = sum(float(record["grading"]["score"] or 0.0) for record in graded)
    correct_count = sum(1 for record in graded if record["grading"]["correct"] is True)
    return {
        "question_count": len(records),
        "graded_count": len(graded),
        "correct_count": correct_count,
        "total_score": total_score,
        "average_score": (total_score / len(graded)) if graded else None,
    }


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    benchmark_path = Path(args.benchmark_file).resolve()
    execute_prompt_path = Path(args.execute_prompt_file).resolve()
    transmute_prompt_path = Path(args.transmute_prompt_file).resolve()
    benchmark = load_json(benchmark_path)
    execute_prompt_text = execute_prompt_path.read_text(encoding="utf-8").strip()
    transmute_prompt_text = transmute_prompt_path.read_text(encoding="utf-8").strip()

    experiment_run_id = args.run_id or f"{benchmark['benchmark_id']}__{args.experiment_label}__{make_run_id()}"
    run_history_root = Path(args.run_history_root)
    grading_runs_root = Path(args.grading_runs_root)
    experiment_runs_root = Path(args.experiment_runs_root)

    baseline_variant = {
        "variant_id": "baseline_execute",
        "title": "Baseline Execute",
        "prompt_family": "execute",
        "selected_prompt_text": execute_prompt_text,
        "base_header_prompt": "",
        "budget_policy": {
            "max_depth": 0,
            "max_helpers_per_node": 0,
            "max_turns_per_node": 1,
        },
    }
    transmute_variant = {
        "variant_id": "transmute_candidate",
        "title": "Root Transmute Then Child Execute",
        "prompt_family": "transmute",
        "selected_prompt_text": transmute_prompt_text,
        "base_header_prompt": "",
        "child_prompt_family": "execute",
        "child_selected_prompt_text": execute_prompt_text,
        "child_base_header_prompt": "",
        "budget_policy": {
            "max_depth": 1,
            "max_helpers_per_node": 1,
            "max_turns_per_node": 4,
        },
    }

    question_results: list[dict[str, Any]] = []
    baseline_records: list[dict[str, Any]] = []
    transmute_records: list[dict[str, Any]] = []
    for index, question in enumerate(benchmark["questions"], start=1):
        question_path = (REPO_ROOT / question["question_file"]).resolve()
        question_stub = f"q{index:02d}"

        baseline_record = run_question_case(
            question_path=question_path,
            label=f"{args.experiment_label}_baseline_execute",
            runtime_provider=args.runtime_provider,
            model=args.model,
            run_history_root=run_history_root,
            grading_runs_root=grading_runs_root,
            max_depth=0,
            max_helpers=0,
            run_id=f"{experiment_run_id}__baseline_execute__{question_stub}",
            sync_supabase=args.sync_supabase,
            extra_variable_overrides=baseline_variant,
        )
        transmute_record = run_question_case(
            question_path=question_path,
            label=f"{args.experiment_label}_transmute_candidate",
            runtime_provider=args.runtime_provider,
            model=args.model,
            run_history_root=run_history_root,
            grading_runs_root=grading_runs_root,
            max_depth=1,
            max_helpers=1,
            run_id=f"{experiment_run_id}__transmute_candidate__{question_stub}",
            sync_supabase=args.sync_supabase,
            extra_variable_overrides=transmute_variant,
        )

        baseline_records.append(baseline_record)
        transmute_records.append(transmute_record)
        question_results.append(
            {
                "question_id": question["question_id"],
                "question_file": question["question_file"],
                "domain": question.get("domain"),
                "why_included": question.get("why_included"),
                "baseline_execute": baseline_record,
                "transmute_candidate": transmute_record,
            }
        )

    summary = {
        "experiment_run_id": experiment_run_id,
        "created_at_utc": utc_now_iso(),
        "benchmark": benchmark,
        "runtime_provider": args.runtime_provider,
        "model": args.model,
        "reviewer_provider": None,
        "reviewer_model": None,
        "execute_prompt_file": str(execute_prompt_path),
        "transmute_prompt_file": str(transmute_prompt_path),
        "variants": {
            "baseline_execute": baseline_variant,
            "transmute_candidate": transmute_variant,
        },
        "question_results": question_results,
        "aggregate": {
            "baseline_execute": compute_variant_summary(baseline_records),
            "transmute_candidate": compute_variant_summary(transmute_records),
        },
    }

    summary_dir = experiment_runs_root / benchmark["benchmark_id"]
    summary_dir.mkdir(parents=True, exist_ok=True)
    summary_path = summary_dir / f"{experiment_run_id}.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    if args.sync_supabase:
        supabase_config = load_supabase_config()
        sync_experiment_summary(config=supabase_config, summary_path=summary_path)

    print(f"experiment_run_id={experiment_run_id}")
    print(f"benchmark_id={benchmark['benchmark_id']}")
    print(f"summary_path={summary_path}")
    print(f"baseline_total_score={summary['aggregate']['baseline_execute']['total_score']}")
    print(f"transmute_total_score={summary['aggregate']['transmute_candidate']['total_score']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Run a cleaner Gemma benchmark on the Super-Eywa grading bank."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any


THIS_DIR = Path(__file__).resolve().parent
REPO_ROOT = THIS_DIR.parents[1]
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from coding_packets_v1 import coding_packet_exists  # noqa: E402
from run_test_question_v1 import run_question_case  # noqa: E402


DEFAULT_PROMPT_FILE = THIS_DIR / "prompt-experiments" / "benchmark-clean-v1" / "execute_prompt_v1.txt"

BENCHMARK_INCOMPLETE = {
    "architecture-derived-B1-constraint-first-planning-ceramic-sintering": (
        "Prompt references answer choices A-F, but the choices are not present in the stored question."
    ),
    "architecture-derived-B3-ambiguity-detection-pronoun-disambiguation": (
        "Prompt references five answer choices, but the choices are not present in the stored question."
    ),
    "architecture-derived-B7-sarcasm-classification": (
        "Prompt references three Reddit replies, but the actual replies are not present in the stored question."
    ),
    "architecture-derived-B8-stack-based-bracket-matching": (
        "Prompt references derivation steps, but the actual bracket sequence and steps are not present."
    ),
    "architecture-derived-B12-knowledge-gated-domain-question-ftir-gelation": (
        "Prompt references nine answer choices, but the choices are not present in the stored question."
    ),
}

HARNESS_MISSING = {
    "coding-B1-usaco-2024-us-open-platinum-identity-theft": (
        "Binary hidden-test task; the stored question is only a short descriptor and has no runnable harness here."
    ),
    "coding-B2-usaco-2023-us-open-gold-tree-merging": (
        "Binary hidden-test task; the stored question is only a short descriptor and has no runnable harness here."
    ),
    "coding-B3-usaco-2024-february-gold-bessla-motors": (
        "Binary hidden-test task; the stored question is only a short descriptor and has no runnable harness here."
    ),
    "coding-S1-ahc001-atcoder-ad": (
        "Score-gradient task; the stored question has no benchmark instance bundle or scorer in this repo."
    ),
    "coding-S2-ahc012-atcoder-10th-anniversary": (
        "Score-gradient task; the stored question has no benchmark instance bundle or scorer in this repo."
    ),
    "coding-S3-ahc024-topological-map": (
        "Score-gradient task; the stored question has no benchmark instance bundle or scorer in this repo."
    ),
    "coding-S4-ahc030-polyomino-mining": (
        "Score-gradient task; the stored question has no benchmark instance bundle or scorer in this repo."
    ),
    "coding-S5-ahc032-mod-stamp": (
        "Score-gradient task; the stored question has no benchmark instance bundle or scorer in this repo."
    ),
    "coding-S6-ahc037-soda": (
        "Score-gradient task; the stored question has no benchmark instance bundle or scorer in this repo."
    ),
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the clean Super-Eywa grading benchmark.")
    parser.add_argument("--label", default="gemma426b_clean_benchmark_v1")
    parser.add_argument("--runtime-provider", default="openrouter", choices=["deterministic", "openrouter"])
    parser.add_argument("--model", default="google/gemma-4-26b-a4b-it")
    parser.add_argument("--question-root", default=str(THIS_DIR / "test-questions"))
    parser.add_argument("--prompt-file", default=str(DEFAULT_PROMPT_FILE))
    parser.add_argument("--run-history-root", default=str(REPO_ROOT / "data-system" / "run-history"))
    parser.add_argument("--grading-runs-root", default=str(THIS_DIR / "runs"))
    parser.add_argument("--summary-path")
    parser.add_argument("--provider-max-tokens", type=int, default=1400)
    parser.add_argument("--provider-temperature", type=float, default=0.2)
    return parser


def load_question_paths(question_root: Path) -> list[Path]:
    return sorted(
        path
        for path in question_root.glob("*.md")
        if path.name not in {"README.md", "questions-thoughts.md"}
    )


def classify_question(question_id: str) -> tuple[str, str]:
    if question_id in BENCHMARK_INCOMPLETE:
        return "benchmark_incomplete", BENCHMARK_INCOMPLETE[question_id]
    if question_id.startswith("coding-") and not coding_packet_exists(question_id):
        return "harness_missing", HARNESS_MISSING.get(
            question_id,
            "Coding task has no runnable packet bundle here yet.",
        )
    if question_id in HARNESS_MISSING and not question_id.startswith("coding-"):
        return "harness_missing", HARNESS_MISSING[question_id]
    return "runnable", ""


def summarize(records: list[dict[str, Any]]) -> dict[str, Any]:
    aggregate: dict[str, Any] = {
        "total_questions": len(records),
        "runnable_questions": sum(1 for item in records if item["classification"] == "runnable"),
        "completed_runs": sum(1 for item in records if item["status"] == "completed"),
        "benchmark_incomplete": sum(1 for item in records if item["classification"] == "benchmark_incomplete"),
        "harness_missing": sum(1 for item in records if item["classification"] == "harness_missing"),
        "graded_correct": 0,
        "graded_wrong": 0,
        "graded_total": 0,
        "ungraded_completed": 0,
        "total_tokens_completed": 0,
        "total_wall_time_ms_completed": 0,
        "total_cost_usd_completed": 0.0,
    }

    for item in records:
        if item["status"] != "completed":
            continue
        aggregate["total_tokens_completed"] += int(item.get("total_tokens") or 0)
        aggregate["total_wall_time_ms_completed"] += int(item.get("total_wall_time_ms") or 0)
        aggregate["total_cost_usd_completed"] += float(item.get("total_cost_usd") or 0.0)
        if item.get("grading_status") == "graded":
            aggregate["graded_total"] += 1
            if item.get("correct") is True:
                aggregate["graded_correct"] += 1
            elif item.get("correct") is False:
                aggregate["graded_wrong"] += 1
        elif item["classification"] == "runnable":
            aggregate["ungraded_completed"] += 1

    completed_count = aggregate["completed_runs"]
    aggregate["average_tokens_completed"] = (
        aggregate["total_tokens_completed"] / completed_count if completed_count else None
    )
    aggregate["average_wall_time_ms_completed"] = (
        aggregate["total_wall_time_ms_completed"] / completed_count if completed_count else None
    )
    aggregate["average_cost_usd_completed"] = (
        aggregate["total_cost_usd_completed"] / completed_count if completed_count else None
    )
    return aggregate


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    question_root = Path(args.question_root).resolve()
    prompt_path = Path(args.prompt_file).resolve()
    prompt_text = prompt_path.read_text(encoding="utf-8").strip()
    run_history_root = Path(args.run_history_root).resolve()
    grading_runs_root = Path(args.grading_runs_root).resolve()

    records: list[dict[str, Any]] = []
    for question_path in load_question_paths(question_root):
        question_id = question_path.stem
        classification, reason = classify_question(question_id)
        if classification != "runnable":
            records.append(
                {
                    "question_id": question_id,
                    "question_file": str(question_path),
                    "classification": classification,
                    "classification_reason": reason,
                    "status": "skipped",
                    "runtime_provider": args.runtime_provider,
                    "model": args.model,
                    "run_id": None,
                    "run_dir": None,
                    "grading_record_path": None,
                    "node_count": None,
                    "validation_status": None,
                    "grading_status": None,
                    "correct": None,
                    "score": None,
                    "total_tokens": None,
                    "total_wall_time_ms": None,
                    "total_cost_usd": None,
                }
            )
            continue

        grading_record = run_question_case(
            question_path=question_path,
            label=args.label,
            runtime_provider=args.runtime_provider,
            model=args.model,
            run_history_root=run_history_root,
            grading_runs_root=grading_runs_root,
            max_depth=0,
            max_helpers=0,
            run_id=None,
            extra_variable_overrides={
                "prompt_family": "execute",
                "selected_prompt_text": prompt_text,
                "provider_max_tokens": args.provider_max_tokens,
                "provider_temperature": args.provider_temperature,
                "budget_policy": {
                    "max_depth": 0,
                    "max_helpers_per_node": 0,
                    "max_turns_per_node": 1,
                },
            },
        )
        records.append(
            {
                "question_id": question_id,
                "question_file": str(question_path),
                "classification": classification,
                "classification_reason": reason,
                "status": "completed",
                "runtime_provider": args.runtime_provider,
                "model": args.model,
                "run_id": grading_record.get("run_id"),
                "run_dir": grading_record.get("run_dir"),
                "grading_record_path": grading_record.get("grading_record_path"),
                "node_count": grading_record.get("node_count"),
                "validation_status": grading_record.get("validation_status"),
                "grading_status": (grading_record.get("grading") or {}).get("grading_status"),
                "correct": (grading_record.get("grading") or {}).get("correct"),
                "score": (grading_record.get("grading") or {}).get("score"),
                "total_tokens": grading_record.get("total_tokens"),
                "total_wall_time_ms": grading_record.get("total_wall_time_ms"),
                "total_cost_usd": grading_record.get("total_cost_usd"),
                "root_result_excerpt": grading_record.get("root_result_excerpt"),
            }
        )

    summary = {
        "benchmark_label": args.label,
        "runtime_provider": args.runtime_provider,
        "model": args.model,
        "prompt_file": str(prompt_path),
        "provider_max_tokens": args.provider_max_tokens,
        "provider_temperature": args.provider_temperature,
        "aggregate": summarize(records),
        "entries": records,
    }

    summary_path = (
        Path(args.summary_path).resolve()
        if args.summary_path
        else grading_runs_root / f"{args.label}__summary.json"
    )
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"summary_path={summary_path}")
    print(f"total_questions={summary['aggregate']['total_questions']}")
    print(f"runnable_questions={summary['aggregate']['runnable_questions']}")
    print(f"completed_runs={summary['aggregate']['completed_runs']}")
    print(f"graded_total={summary['aggregate']['graded_total']}")
    print(f"graded_correct={summary['aggregate']['graded_correct']}")
    print(f"ungraded_completed={summary['aggregate']['ungraded_completed']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Build a clean benchmark summary for one run label using current grading logic."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any


THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from grading_methods.simple_grade_v1 import grade_result, parse_question_file  # noqa: E402
from run_clean_benchmark_v1 import classify_question, summarize  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build a clean benchmark summary from stored run records.")
    parser.add_argument("--label", required=True)
    parser.add_argument("--question-root", default=str(THIS_DIR / "test-questions"))
    parser.add_argument("--grading-runs-root", default=str(THIS_DIR / "runs"))
    parser.add_argument("--summary-path")
    return parser


def load_question_paths(question_root: Path) -> list[Path]:
    return sorted(
        path
        for path in question_root.glob("*.md")
        if path.name not in {"README.md", "questions-thoughts.md"}
    )


def find_latest_record(grading_runs_root: Path, question_id: str, label: str) -> Path | None:
    question_dir = grading_runs_root / question_id
    matches = sorted(question_dir.glob(f"{label}__*.json"))
    return matches[-1] if matches else None


def load_result_text(grading_record: dict[str, Any]) -> str:
    final_result_path = grading_record.get("final_result_path")
    if isinstance(final_result_path, str) and final_result_path:
        path = Path(final_result_path)
        if path.exists():
            payload = json.loads(path.read_text(encoding="utf-8"))
            if path.name == "final-output.json":
                return str((payload.get("result") or {}).get("content") or "")
            results = payload.get("results") or []
            if results:
                return str(results[0].get("content") or "")

    run_dir = grading_record.get("run_dir")
    final_result_node_id = grading_record.get("final_result_node_id")
    if isinstance(run_dir, str) and run_dir:
        run_path = Path(run_dir)
        final_output_path = run_path / "final-output.json"
        if final_output_path.exists():
            payload = json.loads(final_output_path.read_text(encoding="utf-8"))
            return str((payload.get("result") or {}).get("content") or "")
        node_id = str(final_result_node_id or "node_root")
        node_record_path = run_path / "nodes" / node_id / "node_record.json"
        if node_record_path.exists():
            payload = json.loads(node_record_path.read_text(encoding="utf-8"))
            results = payload.get("results") or []
            if results:
                return str(results[0].get("content") or "")
    return ""


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    question_root = Path(args.question_root).resolve()
    grading_runs_root = Path(args.grading_runs_root).resolve()

    entries: list[dict[str, Any]] = []
    model = None
    runtime_provider = None
    for question_path in load_question_paths(question_root):
        question_id = question_path.stem
        classification, reason = classify_question(question_id)
        record_path = find_latest_record(grading_runs_root, question_id, args.label)
        if record_path is None:
            entries.append(
                {
                    "question_id": question_id,
                    "question_file": str(question_path),
                    "classification": classification,
                    "classification_reason": reason,
                    "status": "missing",
                    "runtime_provider": None,
                    "model": None,
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

        grading_record = json.loads(record_path.read_text(encoding="utf-8"))
        runtime_provider = runtime_provider or grading_record.get("runtime_provider")
        model = model or grading_record.get("model")

        refreshed_grading = grading_record.get("grading") or {}
        if classification == "runnable":
            refreshed_grading = grade_result(parse_question_file(question_path), load_result_text(grading_record))

        entries.append(
            {
                "question_id": question_id,
                "question_file": str(question_path),
                "classification": classification,
                "classification_reason": reason,
                "status": "completed" if classification == "runnable" else "skipped",
                "runtime_provider": grading_record.get("runtime_provider"),
                "model": grading_record.get("model"),
                "run_id": grading_record.get("run_id"),
                "run_dir": grading_record.get("run_dir"),
                "grading_record_path": str(record_path),
                "node_count": grading_record.get("node_count"),
                "validation_status": grading_record.get("validation_status"),
                "grading_status": refreshed_grading.get("grading_status"),
                "correct": refreshed_grading.get("correct"),
                "score": refreshed_grading.get("score"),
                "total_tokens": grading_record.get("total_tokens"),
                "total_wall_time_ms": grading_record.get("total_wall_time_ms"),
                "total_cost_usd": grading_record.get("total_cost_usd"),
                "root_result_excerpt": grading_record.get("root_result_excerpt"),
                "grading": refreshed_grading,
            }
        )

    summary = {
        "benchmark_label": args.label,
        "runtime_provider": runtime_provider,
        "model": model,
        "aggregate": summarize(entries),
        "entries": entries,
    }

    summary_path = (
        Path(args.summary_path).resolve()
        if args.summary_path
        else grading_runs_root / f"{args.label}__summary_rebuilt.json"
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

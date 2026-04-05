#!/usr/bin/env python3
"""Run one grading-bank question through Super-Eywa v1 and score it."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


THIS_DIR = Path(__file__).resolve().parent
RUNTIME_DIR = THIS_DIR.parents[1] / "eywa-system" / "runtime"
if str(RUNTIME_DIR) not in sys.path:
    sys.path.insert(0, str(RUNTIME_DIR))
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from eywa_runtime.engine import EywaEngine  # noqa: E402
from eywa_runtime.ids import make_run_id  # noqa: E402
from eywa_runtime.validation import RunValidationError, validate_run_directory  # noqa: E402
from grading_methods.simple_grade_v1 import (  # noqa: E402
    build_task_prompt,
    grade_result,
    parse_question_file,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run one grading-bank question through Super-Eywa v1.")
    parser.add_argument("--question-file", required=True, help="Path to the markdown question file.")
    parser.add_argument("--label", default="main", help="Free-form run label, e.g. main or baseline.")
    parser.add_argument("--runtime-provider", default="openrouter", choices=["deterministic", "openrouter"])
    parser.add_argument("--model", default="openai/gpt-4.1-mini")
    parser.add_argument(
        "--run-history-root",
        default=str(THIS_DIR.parents[1] / "data-system" / "run-history"),
    )
    parser.add_argument(
        "--grading-runs-root",
        default=str(THIS_DIR / "runs"),
    )
    parser.add_argument("--max-depth", type=int)
    parser.add_argument("--max-helpers", type=int, default=3)
    parser.add_argument("--run-id", help="Optional explicit run id.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    question_path = Path(args.question_file).resolve()
    question_case = parse_question_file(question_path)
    task_text = build_task_prompt(question_case)

    max_depth = args.max_depth
    if max_depth is None:
        max_depth = 0 if args.label == "baseline" else 3

    run_id = args.run_id or f"{question_case.question_id}__{args.label}__{make_run_id()}"
    variable_overrides = {
        "runtime_provider": args.runtime_provider,
        "model": args.model,
        "budget_policy": {
            "max_depth": max_depth,
            "max_helpers_per_node": args.max_helpers,
        },
    }

    engine = EywaEngine(Path(args.run_history_root))
    result = engine.run(
        task_text=task_text,
        run_id=run_id,
        run_level_variables=variable_overrides,
        task_source=str(question_path.relative_to(THIS_DIR.parents[1])),
    )

    run_dir = result.run_dir
    try:
        validation_summary = validate_run_directory(run_dir)
        validation_status = "valid"
    except RunValidationError as exc:
        validation_summary = {"error": str(exc)}
        validation_status = "invalid"

    root_record = json.loads((run_dir / "nodes" / result.root_node_id / "node_record.json").read_text(encoding="utf-8"))
    result_text = root_record["results"][0]["content"] if root_record["results"] else ""
    grading = grade_result(question_case, result_text)

    grading_record = {
        "question_id": question_case.question_id,
        "title": question_case.title,
        "question_file": str(question_path),
        "label": args.label,
        "run_id": result.run_id,
        "run_dir": str(run_dir),
        "runtime_provider": args.runtime_provider,
        "model": args.model,
        "task_text": task_text,
        "node_count": result.node_count,
        "root_result_excerpt": result_text[:400],
        "validation_status": validation_status,
        "validation_summary": validation_summary,
        "grading": grading,
    }

    runs_root = Path(args.grading_runs_root)
    question_run_dir = runs_root / question_case.question_id
    question_run_dir.mkdir(parents=True, exist_ok=True)
    record_path = question_run_dir / f"{args.label}__{result.run_id}.json"
    record_path.write_text(json.dumps(grading_record, indent=2), encoding="utf-8")

    print(f"question_id={question_case.question_id}")
    print(f"label={args.label}")
    print(f"run_id={result.run_id}")
    print(f"run_dir={run_dir}")
    print(f"grading_record={record_path}")
    print(f"node_count={result.node_count}")
    print(f"validation_status={validation_status}")
    print(f"grading_status={grading['grading_status']}")
    print(f"correct={grading['correct']}")
    print(f"score={grading['score']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

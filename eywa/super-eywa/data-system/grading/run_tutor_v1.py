#!/usr/bin/env python3
"""Run the manual tutor step for one graded Super-Eywa benchmark run."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any


THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from reviewer_v1 import review_grading_record  # noqa: E402
from sync_to_supabase_v1 import load_supabase_config, sync_grading_record  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the manual tutor step for one grading record.")
    parser.add_argument("--grading-record", required=True, help="Path to one grading record JSON.")
    parser.add_argument("--tutoring-root", default=str(THIS_DIR / "tutoring"))
    parser.add_argument(
        "--tutor-provider",
        default="same",
        choices=["same", "deterministic", "openrouter"],
    )
    parser.add_argument("--tutor-model", help="Optional explicit tutor model. Defaults to the run model.")
    parser.add_argument("--sync-supabase", action="store_true")
    return parser


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    grading_record_path = Path(args.grading_record).resolve()
    tutoring_root = Path(args.tutoring_root).resolve()
    grading_record = load_json(grading_record_path)

    runtime_provider = str(grading_record.get("runtime_provider") or "deterministic")
    model = str(grading_record.get("model") or "deterministic-local-v1")
    tutor_provider = runtime_provider if args.tutor_provider == "same" else args.tutor_provider
    tutor_model = args.tutor_model or model

    tutor_record = review_grading_record(
        question_id=str(grading_record["question_id"]),
        title=str(grading_record["title"]),
        question_file=str(grading_record["question_file"]),
        label=str(grading_record["label"]),
        run_id=str(grading_record["run_id"]),
        run_dir=str(grading_record["run_dir"]),
        runtime_provider=runtime_provider,
        model=model,
        task_text=str(grading_record.get("task_text") or ""),
        root_result_excerpt=str(grading_record.get("root_result_excerpt") or ""),
        grading=grading_record.get("grading") or {},
        root_variables=grading_record.get("root_variables") or {},
        root_orchestration=grading_record.get("root_orchestration") or {},
        reviews_root=tutoring_root,
        reviewer_provider=tutor_provider,
        reviewer_model=tutor_model,
    )

    grading_record["tutor_record_path"] = tutor_record["review_record_path"]
    write_json(grading_record_path, grading_record)

    if args.sync_supabase:
        supabase_config = load_supabase_config()
        sync_grading_record(config=supabase_config, grading_record_path=grading_record_path)

    print(f"question_id={grading_record['question_id']}")
    print(f"run_id={grading_record['run_id']}")
    print(f"grading_record={grading_record_path}")
    print(f"tutor_record={tutor_record['review_record_path']}")
    print(f"tutor_provider={tutor_provider}")
    print(f"tutor_model={tutor_model}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

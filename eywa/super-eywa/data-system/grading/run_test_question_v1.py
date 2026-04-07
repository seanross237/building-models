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
from grading_methods.agent_grade_v1 import grade_result as agent_grade_result  # noqa: E402
from grading_methods.simple_grade_v1 import (  # noqa: E402
    build_task_prompt,
    parse_question_file,
)
from coding_repair_v1 import maybe_repair_invalid_coding_submission  # noqa: E402
from sync_to_supabase_v1 import load_supabase_config, sync_grading_record, sync_question_bank  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run one grading-bank question through Super-Eywa v1.")
    parser.add_argument("--question-file", required=True, help="Path to the markdown question file.")
    parser.add_argument("--label", default="main", help="Free-form run label, e.g. main or baseline.")
    parser.add_argument("--runtime-provider", default="openrouter", choices=["deterministic", "openrouter"])
    parser.add_argument("--model", default="google/gemma-4-26b-a4b-it")
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
    parser.add_argument(
        "--variables-json",
        help="Optional JSON object of extra run-level variable overrides.",
    )
    parser.add_argument(
        "--grading-provider",
        default="same",
        choices=["same", "deterministic", "openrouter"],
        help="How grading is performed. 'same' follows the runtime provider.",
    )
    parser.add_argument(
        "--grading-model",
        help="Optional explicit grading model. Defaults to the run model for live runs.",
    )
    parser.add_argument(
        "--coding-repair-attempts",
        type=int,
        default=2,
        help="For coding tasks, bounded same-model repair attempts after invalid contestant output.",
    )
    parser.add_argument("--sync-supabase", action="store_true")
    return parser


def run_question_case(
    *,
    question_path: Path,
    label: str,
    runtime_provider: str,
    model: str,
    run_history_root: Path,
    grading_runs_root: Path,
    max_depth: int | None,
    max_helpers: int,
    run_id: str | None,
    grading_provider: str = "same",
    grading_model: str | None = None,
    coding_repair_attempts: int = 2,
    sync_supabase: bool = False,
    extra_variable_overrides: dict[str, object] | None = None,
) -> dict[str, object]:
    question_path = question_path.resolve()
    question_case = parse_question_file(question_path)
    task_text = build_task_prompt(question_case)

    if max_depth is None:
        max_depth = 0 if label == "baseline" else 3

    resolved_run_id = run_id or f"{question_case.question_id}__{label}__{make_run_id()}"
    variable_overrides = {
        "runtime_provider": runtime_provider,
        "model": model,
        "budget_policy": {
            "max_depth": max_depth,
            "max_helpers_per_node": max_helpers,
        },
    }
    if question_case.entry_type == "coding":
        variable_overrides.update(
            {
                "submission_contract_type": "coding_single_file_python",
                "submission_entry_file": "main.py",
            }
        )
    if extra_variable_overrides:
        variable_overrides.update(extra_variable_overrides)
        budget_override = dict(variable_overrides.get("budget_policy") or {})
        budget_override.setdefault("max_depth", max_depth)
        budget_override.setdefault("max_helpers_per_node", max_helpers)
        variable_overrides["budget_policy"] = budget_override

    engine = EywaEngine(run_history_root)
    result = engine.run(
        task_text=task_text,
        run_id=resolved_run_id,
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

    run_summary = json.loads((run_dir / "run_summary.json").read_text(encoding="utf-8"))
    root_record = json.loads((run_dir / "nodes" / result.root_node_id / "node_record.json").read_text(encoding="utf-8"))
    root_result_text = root_record["results"][0]["content"] if root_record["results"] else ""
    final_output_path = run_dir / "final-output.json"
    final_output = None
    if final_output_path.exists():
        final_output = json.loads(final_output_path.read_text(encoding="utf-8"))
        result_payload = final_output.get("result") or {}
        result_text = str(result_payload.get("content") or "")
        final_result_node_id = str(final_output.get("source_node_id") or result.root_node_id)
        final_result_path = str(final_output_path)
    else:
        result_text = root_record["results"][0]["content"] if root_record["results"] else ""
        final_result_node_id = result.root_node_id
        final_result_path = str(run_dir / "nodes" / result.root_node_id / "node_record.json")

    resolved_grading_provider = _resolve_grading_provider(grading_provider, runtime_provider)
    resolved_grading_model = _resolve_grading_model(
        grading_provider=resolved_grading_provider,
        grading_model=grading_model,
        runtime_model=model,
    )
    grading, grading_trace = agent_grade_result(
        question_case,
        result_text,
        grading_provider=resolved_grading_provider,
        grading_model=resolved_grading_model,
        run_dir=run_dir,
        final_output=final_output if final_output_path.exists() else None,
    )
    coding_repair_attempt_log: list[dict[str, object]] = []
    repaired = maybe_repair_invalid_coding_submission(
        question_case=question_case,
        runtime_provider=runtime_provider,
        model=model,
        run_dir=run_dir,
        grading=grading,
        grading_trace=grading_trace,
        max_attempts=coding_repair_attempts,
    )
    if repaired is not None:
        grading, grading_trace = repaired
        coding_repair_attempt_log = list(grading_trace.get("repair_attempts") or [])
    grading_trace_path = _write_grading_trace(
        grading_runs_root=grading_runs_root,
        question_id=question_case.question_id,
        label=label,
        run_id=result.run_id,
        trace_payload={
            "schema_name": "eywa_grading_trace",
            "schema_version": "v1",
            "question_id": question_case.question_id,
            "run_id": result.run_id,
            "label": label,
            "grader_provider": resolved_grading_provider,
            "grader_model": resolved_grading_model,
            "grading": grading,
            "provider_payload": grading_trace,
            "coding_repair_attempts": coding_repair_attempt_log,
        },
    )

    grading_record = {
        "question_id": question_case.question_id,
        "title": question_case.title,
        "question_file": str(question_path),
        "label": label,
        "run_id": result.run_id,
        "run_dir": str(run_dir),
        "runtime_provider": runtime_provider,
        "model": model,
        "task_text": task_text,
        "node_count": result.node_count,
        "total_tokens": run_summary.get("total_tokens"),
        "total_wall_time_ms": run_summary.get("total_wall_time_ms"),
        "total_cost_usd": run_summary.get("total_cost_usd"),
        "root_result_excerpt": root_result_text[:400],
        "final_result_excerpt": result_text[:400],
        "final_result_node_id": final_result_node_id,
        "final_result_path": final_result_path,
        "run_level_variable_overrides": variable_overrides,
        "root_variables": root_record["variables"],
        "root_orchestration": root_record["orchestration"],
        "validation_status": validation_status,
        "validation_summary": validation_summary,
        "grader_provider": resolved_grading_provider,
        "grader_model": resolved_grading_model,
        "grading_method": grading.get("grading_method"),
        "task_correct": grading.get("task_correct"),
        "task_score": grading.get("task_score"),
        "submission_compliance": grading.get("submission_compliance"),
        "recovery_used": grading.get("recovery_used"),
        "submission_source": grading.get("submission_source"),
        "recovery_notes": grading.get("recovery_notes"),
        "grading_trace_path": str(grading_trace_path),
        "submission_artifact_refs": (
            list((grading_trace.get("submission") or {}).get("artifact_refs") or [])
            if isinstance(grading_trace, dict)
            else []
        ),
        "coding_execution": grading_trace.get("execution") if isinstance(grading_trace, dict) else None,
        "coding_repair_attempts": coding_repair_attempt_log,
        "grading": grading,
        "review_record_path": None,
        "reviewer_provider": None,
        "reviewer_model": None,
        "tutor_record_path": None,
    }

    question_run_dir = grading_runs_root / question_case.question_id
    question_run_dir.mkdir(parents=True, exist_ok=True)
    record_path = question_run_dir / f"{label}__{result.run_id}.json"
    record_path.write_text(json.dumps(grading_record, indent=2), encoding="utf-8")
    grading_record["grading_record_path"] = str(record_path)
    record_path.write_text(json.dumps(grading_record, indent=2), encoding="utf-8")

    if sync_supabase:
        supabase_config = load_supabase_config()
        sync_question_bank(config=supabase_config)
        sync_grading_record(config=supabase_config, grading_record_path=record_path)
    return grading_record


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    extra_variable_overrides = json.loads(args.variables_json) if args.variables_json else None
    grading_record = run_question_case(
        question_path=Path(args.question_file),
        label=args.label,
        runtime_provider=args.runtime_provider,
        model=args.model,
        run_history_root=Path(args.run_history_root),
        grading_runs_root=Path(args.grading_runs_root),
        max_depth=args.max_depth,
        max_helpers=args.max_helpers,
        run_id=args.run_id,
        grading_provider=args.grading_provider,
        grading_model=args.grading_model,
        coding_repair_attempts=args.coding_repair_attempts,
        sync_supabase=args.sync_supabase,
        extra_variable_overrides=extra_variable_overrides,
    )

    print(f"question_id={grading_record['question_id']}")
    print(f"label={grading_record['label']}")
    print(f"run_id={grading_record['run_id']}")
    print(f"run_dir={grading_record['run_dir']}")
    print(f"grading_record={grading_record['grading_record_path']}")
    print(f"node_count={grading_record['node_count']}")
    print(f"total_tokens={grading_record['total_tokens']}")
    print(f"total_wall_time_ms={grading_record['total_wall_time_ms']}")
    print(f"total_cost_usd={grading_record['total_cost_usd']}")
    print(f"validation_status={grading_record['validation_status']}")
    print(f"grader_provider={grading_record['grader_provider']}")
    print(f"grader_model={grading_record['grader_model']}")
    print(f"grading_method={grading_record['grading_method']}")
    print(f"task_score={grading_record['task_score']}")
    print(f"task_correct={grading_record['task_correct']}")
    print(f"submission_compliance={grading_record['submission_compliance']}")
    print(f"recovery_used={grading_record['recovery_used']}")
    print(f"submission_source={grading_record['submission_source']}")
    print(f"grading_trace={grading_record['grading_trace_path']}")
    print(f"coding_repair_attempts={len(grading_record['coding_repair_attempts'])}")
    print(f"grading_status={grading_record['grading']['grading_status']}")
    print(f"correct={grading_record['grading']['correct']}")
    print(f"score={grading_record['grading']['score']}")
    return 0


def _resolve_grading_provider(grading_provider: str, runtime_provider: str) -> str:
    resolved = str(grading_provider or "same").strip()
    if resolved == "same":
        return "openrouter" if runtime_provider == "openrouter" else "deterministic"
    return resolved


def _resolve_grading_model(*, grading_provider: str, grading_model: str | None, runtime_model: str) -> str:
    explicit = str(grading_model or "").strip()
    if explicit:
        return explicit
    if grading_provider == "openrouter":
        return runtime_model
    return "deterministic-agent-grader-v1"


def _write_grading_trace(
    *,
    grading_runs_root: Path,
    question_id: str,
    label: str,
    run_id: str,
    trace_payload: dict[str, object],
) -> Path:
    trace_root = grading_runs_root.resolve().parent / "grading-traces"
    trace_path = trace_root / question_id / f"{label}__{run_id}.json"
    trace_path.parent.mkdir(parents=True, exist_ok=True)
    trace_path.write_text(json.dumps(trace_payload, indent=2), encoding="utf-8")
    return trace_path


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Mirror Super-Eywa grading artifacts into Supabase."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


THIS_DIR = Path(__file__).resolve().parent
REPO_ROOT = THIS_DIR.parents[1]
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from grading_methods.simple_grade_v1 import parse_question_file  # noqa: E402


AUTO_GRADED_QUESTION_IDS = {
    "architecture-derived-B4-hensel-lifting-verification",
    "architecture-derived-B5-combinatorial-probability-random-chords",
    "architecture-derived-B6-binary-representation-minimization",
    "architecture-derived-B10-mean-field-lattice-gas-occupancy",
    "architecture-derived-B11-board-game-rule-chaining",
}


class SupabaseSyncError(RuntimeError):
    """Raised when local config or remote sync fails."""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Sync Super-Eywa grading artifacts to Supabase.")
    parser.add_argument("--apply-schema", action="store_true")
    parser.add_argument("--sync-question-bank", action="store_true")
    parser.add_argument("--sync-grading-record")
    parser.add_argument("--sync-experiment-summary")
    parser.add_argument("--backfill-all", action="store_true")
    parser.add_argument(
        "--schema-file",
        default=str(THIS_DIR / "supabase" / "schema_v1.sql"),
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    config = load_supabase_config()

    if args.apply_schema:
        apply_schema(config=config, schema_file=Path(args.schema_file))

    if args.sync_question_bank or args.backfill_all:
        sync_question_bank(config=config)

    if args.sync_grading_record:
        sync_grading_record(config=config, grading_record_path=Path(args.sync_grading_record))

    if args.sync_experiment_summary:
        sync_experiment_summary(config=config, summary_path=Path(args.sync_experiment_summary))

    if args.backfill_all:
        backfill_all(config=config)

    return 0


def load_supabase_config() -> dict[str, str]:
    env = dict(os.environ)
    for path in (
        REPO_ROOT / ".env.local",
        REPO_ROOT / ".env",
        REPO_ROOT.parents[1] / ".env.local",
        REPO_ROOT.parents[1] / ".env",
    ):
        if path.exists():
            env.update(load_env_file(path))

    config = {
        "url": env.get("SUPABASE_URL", "").strip(),
        "service_role_key": env.get("SUPABASE_SERVICE_ROLE_KEY", "").strip(),
        "database_url": env.get("SUPABASE_DATABASE_URL", "").strip(),
        "pooler_url": env.get("SUPABASE_POOLER_URL", "").strip(),
    }
    if not config["url"]:
        raise SupabaseSyncError("SUPABASE_URL was not found in env or .env.local")
    if not config["service_role_key"]:
        raise SupabaseSyncError("SUPABASE_SERVICE_ROLE_KEY was not found in env or .env.local")
    return config


def load_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def apply_schema(*, config: dict[str, str], schema_file: Path) -> None:
    database_url = config["database_url"] or config["pooler_url"]
    if not database_url:
        raise SupabaseSyncError("SUPABASE_DATABASE_URL or SUPABASE_POOLER_URL is required to apply schema.")
    completed = subprocess.run(
        ["psql", database_url, "-v", "ON_ERROR_STOP=1", "-f", str(schema_file)],
        check=True,
        capture_output=True,
        text=True,
    )
    if completed.stdout.strip():
        print(completed.stdout.strip())


def sync_question_bank(*, config: dict[str, str]) -> None:
    rows = build_question_bank_rows()
    upsert_rows(
        config=config,
        table="benchmark_questions",
        rows=rows,
        on_conflict="question_id",
    )
    print(f"synced benchmark_questions={len(rows)}")


def build_question_bank_rows() -> list[dict[str, Any]]:
    question_dir = THIS_DIR / "test-questions"
    rows: list[dict[str, Any]] = []
    for path in sorted(question_dir.glob("*.md")):
        if path.name in {"README.md", "questions-thoughts.md"}:
            continue
        question = parse_question_file(path)
        grading_text = question.sections.get("grading", "")
        rows.append(
            {
                "question_id": question.question_id,
                "title": question.title,
                "family": infer_question_family(path.name),
                "question_file": str(path),
                "has_question": "question" in question.sections,
                "has_task": "task" in question.sections,
                "has_correct_answer": bool(question.sections.get("correct_answer", "").strip()),
                "grading_text": grading_text,
                "intended_grading_mode": infer_intended_grading_mode(grading_text),
                "currently_auto_graded": question.question_id in AUTO_GRADED_QUESTION_IDS,
                "source_json": {
                    "sections": question.sections,
                },
            }
        )
    return rows


def sync_grading_record(*, config: dict[str, str], grading_record_path: Path) -> None:
    sync_question_bank(config=config)
    grading_record = load_json(grading_record_path)
    review_like_record_path = (
        grading_record.get("mx1_tutor_record_path")
        or grading_record.get("tutor_record_path")
        or grading_record.get("review_record_path")
    )
    review_record = load_json(Path(str(review_like_record_path))) if review_like_record_path else {}
    tutor_record = review_record.get("tutor") or review_record.get("review") or {}
    row = {
        "run_id": grading_record["run_id"],
        "question_id": grading_record["question_id"],
        "label": grading_record["label"],
        "runtime_provider": grading_record["runtime_provider"],
        "model": grading_record["model"],
        "reviewer_provider": grading_record.get("reviewer_provider"),
        "reviewer_model": grading_record.get("reviewer_model"),
        "validation_status": grading_record.get("validation_status"),
        "grading_status": grading_record.get("grading", {}).get("grading_status"),
        "correct": grading_record.get("grading", {}).get("correct"),
        "score": grading_record.get("grading", {}).get("score"),
        "node_count": grading_record.get("node_count"),
        "total_tokens": grading_record.get("total_tokens"),
        "total_wall_time_ms": grading_record.get("total_wall_time_ms"),
        "total_cost_usd": grading_record.get("total_cost_usd"),
        "task_text": grading_record.get("task_text"),
        "root_result_excerpt": grading_record.get("root_result_excerpt"),
        "final_result_excerpt": grading_record.get("final_result_excerpt"),
        "final_result_node_id": grading_record.get("final_result_node_id"),
        "final_result_path": grading_record.get("final_result_path"),
        "run_dir": grading_record.get("run_dir"),
        "grading_record_path": str(grading_record_path),
        "review_record_path": grading_record.get("review_record_path"),
        "tutor_record_path": grading_record.get("tutor_record_path"),
        "mx1_loop_id": grading_record.get("mx1_loop_id"),
        "mx1_family": grading_record.get("mx1_family"),
        "mx1_iteration_index": grading_record.get("mx1_iteration_index"),
        "mx1_iteration_kind": grading_record.get("mx1_iteration_kind"),
        "mx1_prompt_text": grading_record.get("mx1_prompt_text"),
        "mx1_prompt_file": grading_record.get("mx1_prompt_file"),
        "mx1_child_prompt_family": grading_record.get("mx1_child_prompt_family"),
        "mx1_child_prompt_text": grading_record.get("mx1_child_prompt_text"),
        "mx1_tutor_record_path": grading_record.get("mx1_tutor_record_path"),
        "mx1_loop_manifest_path": grading_record.get("mx1_loop_manifest_path"),
        "mx1_is_best": grading_record.get("mx1_is_best"),
        "mx1_best_iteration_index": grading_record.get("mx1_best_iteration_index"),
        "mx1_best_run_id": grading_record.get("mx1_best_run_id"),
        "mx1_best_score": grading_record.get("mx1_best_score"),
        "mx1_best_prompt_text": grading_record.get("mx1_best_prompt_text"),
        "run_level_variable_overrides": grading_record.get("run_level_variable_overrides") or {},
        "root_variables": grading_record.get("root_variables") or {},
        "root_orchestration": grading_record.get("root_orchestration") or {},
        "grading": grading_record.get("grading") or {},
        "review": review_record.get("review") or grading_record.get("review") or {},
        "tutor": tutor_record or grading_record.get("tutor") or {},
        "mx1": grading_record.get("mx1") or {},
        "source_json": grading_record,
    }
    upsert_rows(
        config=config,
        table="graded_runs",
        rows=[row],
        on_conflict="run_id",
    )
    print(f"synced graded_run={grading_record['run_id']}")


def sync_experiment_summary(*, config: dict[str, str], summary_path: Path) -> None:
    summary = load_json(summary_path)
    sync_question_bank(config=config)

    question_case_rows: list[dict[str, Any]] = []
    for question_result in summary.get("question_results") or []:
        question_id = question_result["question_id"]
        for variant_id, variant_config in (summary.get("variants") or {}).items():
            grading_record_path = question_result.get(variant_id, {}).get("grading_record_path")
            if grading_record_path:
                sync_grading_record(config=config, grading_record_path=Path(str(grading_record_path)))
            grading_record = question_result.get(variant_id) or {}
            question_case_rows.append(
                {
                    "experiment_run_id": summary["experiment_run_id"],
                    "question_id": question_id,
                    "variant_id": variant_id,
                    "variant_title": (variant_config or {}).get("title"),
                    "question_file": question_result.get("question_file"),
                    "domain": question_result.get("domain"),
                    "why_included": question_result.get("why_included"),
                    "run_id": grading_record.get("run_id"),
                    "score": grading_record.get("grading", {}).get("score"),
                    "correct": grading_record.get("grading", {}).get("correct"),
                    "grading_status": grading_record.get("grading", {}).get("grading_status"),
                    "review_assessment": (grading_record.get("review") or {}).get("correctness_assessment"),
                    "row_json": grading_record,
                }
            )

    experiment_row = {
        "experiment_run_id": summary["experiment_run_id"],
        "benchmark_id": summary.get("benchmark", {}).get("benchmark_id"),
        "runtime_provider": summary.get("runtime_provider"),
        "model": summary.get("model"),
        "reviewer_provider": summary.get("reviewer_provider"),
        "reviewer_model": summary.get("reviewer_model"),
        "execute_prompt_file": summary.get("execute_prompt_file"),
        "transmute_prompt_file": summary.get("transmute_prompt_file"),
        "summary_path": str(summary_path),
        "benchmark": summary.get("benchmark") or {},
        "variants": summary.get("variants") or {},
        "aggregate": summary.get("aggregate") or {},
        "source_json": summary,
    }

    upsert_rows(
        config=config,
        table="experiment_runs",
        rows=[experiment_row],
        on_conflict="experiment_run_id",
    )
    upsert_rows(
        config=config,
        table="experiment_run_cases",
        rows=question_case_rows,
        on_conflict="experiment_run_id,question_id,variant_id",
    )
    print(f"synced experiment_run={summary['experiment_run_id']}")


def backfill_all(*, config: dict[str, str]) -> None:
    sync_question_bank(config=config)

    runs_root = THIS_DIR / "runs"
    for grading_record_path in sorted(runs_root.glob("*/*.json")):
        sync_grading_record(config=config, grading_record_path=grading_record_path)

    experiment_root = THIS_DIR / "experiment-runs"
    for summary_path in sorted(experiment_root.glob("*/*.json")):
        sync_experiment_summary(config=config, summary_path=summary_path)


def infer_question_family(filename: str) -> str:
    if filename.startswith("architecture-derived-"):
        return "architecture-derived"
    if filename.startswith("atlas-derived-"):
        return "atlas-derived"
    if filename.startswith("coding-"):
        return "coding"
    return "other"


def infer_intended_grading_mode(grading_text: str) -> str:
    text = str(grading_text or "").lower()
    if "higher is better" in text or "lower probing cost is better" in text or "contest score is derived" in text:
        return "continuous"
    if "hidden-test acceptance" in text:
        return "binary_hidden_test"
    if "single letter" in text or "3-bit string" in text or 'correct conclusion is "unknown"' in text:
        return "exact_discrete"
    if "within 0.01" in text:
        return "numeric_tolerance"
    if "exact numerical match" in text or "numerical match" in text:
        return "exact_numeric"
    if "formula match" in text or "algebraic identity" in text:
        return "formula_or_identity"
    if text.startswith("binary:") or "correct conclusion" in text:
        return "binary_reasoning"
    return "structured_open"


def upsert_rows(*, config: dict[str, str], table: str, rows: list[dict[str, Any]], on_conflict: str) -> list[dict[str, Any]]:
    if not rows:
        return []
    query = urlencode({"on_conflict": on_conflict})
    url = f"{config['url'].rstrip('/')}/rest/v1/{table}?{query}"
    headers = {
        "apikey": config["service_role_key"],
        "Authorization": f"Bearer {config['service_role_key']}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates,return=representation",
    }
    payload = json.dumps(rows).encode("utf-8")
    request = Request(url=url, method="POST", headers=headers, data=payload)
    response_body = ""
    for attempt in range(3):
        try:
            with urlopen(request, timeout=60) as response:
                response_body = response.read().decode("utf-8")
            break
        except HTTPError as exc:
            error_body = exc.read().decode("utf-8", errors="replace")
            if exc.code == 400 and "schema cache" in error_body and attempt < 2:
                time.sleep(2 * (attempt + 1))
                continue
            raise SupabaseSyncError(f"Supabase upsert failed for {table}: HTTP {exc.code}: {error_body}") from exc
        except URLError as exc:
            raise SupabaseSyncError(f"Supabase upsert failed for {table}: {exc.reason}") from exc
        except OSError as exc:
            raise SupabaseSyncError(f"Supabase upsert failed for {table}: {exc}") from exc

    if not response_body.strip():
        return []
    return json.loads(response_body)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    raise SystemExit(main())

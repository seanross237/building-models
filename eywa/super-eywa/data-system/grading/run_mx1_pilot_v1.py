#!/usr/bin/env python3
"""Stepwise pilot runner for Mission Exploration 1."""

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

from eywa_runtime.ids import make_run_id  # noqa: E402
from grading_methods.simple_grade_v1 import parse_question_file  # noqa: E402
from mx1_loop_v1 import (  # noqa: E402
    append_attempt,
    build_loop_id,
    build_loop_manifest_path,
    create_manifest,
    load_json,
    update_grading_record_mx1,
    write_json,
)
from run_test_question_v1 import run_question_case  # noqa: E402
from sync_to_supabase_v1 import load_supabase_config, sync_grading_record  # noqa: E402


DEFAULT_STARTER_PROMPT_FILE = THIS_DIR / "prompt-experiments" / "mx1-pilot-v1" / "starter_transmute_prompt_v1.txt"
DEFAULT_DELEGATE_PROMPT_FILE = THIS_DIR / "prompt-experiments" / "mx1-pilot-v1" / "starter_delegate_prompt_v1.txt"
DEFAULT_REVIEW_PROMPT_FILE = THIS_DIR / "prompt-experiments" / "mx1-pilot-v1" / "starter_review_prompt_v1.txt"
DEFAULT_EXECUTE_PROMPT_FILE = THIS_DIR / "prompt-experiments" / "mx1-pilot-v1" / "execute_prompt_v1.txt"
DEFAULT_LOOPS_ROOT = THIS_DIR / "mx1-loops"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the MX1 pilot loop stepwise.")
    parser.add_argument("--action", required=True, choices=["init", "baseline", "iterate", "status"])
    parser.add_argument("--question-file", required=True)
    parser.add_argument("--family", default="transmute")
    parser.add_argument("--loop-label", default="pilot_v1")
    parser.add_argument("--loop-id")
    parser.add_argument("--loops-root", default=str(DEFAULT_LOOPS_ROOT))
    parser.add_argument("--run-history-root", default=str(REPO_ROOT / "data-system" / "run-history"))
    parser.add_argument("--grading-runs-root", default=str(THIS_DIR / "runs"))
    parser.add_argument("--runtime-provider", default="openrouter", choices=["deterministic", "openrouter"])
    parser.add_argument("--model", default="google/gemma-4-26b-a4b-it")
    parser.add_argument("--starter-prompt-file", default=str(DEFAULT_STARTER_PROMPT_FILE))
    parser.add_argument("--execute-prompt-file", default=str(DEFAULT_EXECUTE_PROMPT_FILE))
    parser.add_argument("--iterations-target", type=int, default=10)
    parser.add_argument("--exploration-iterations", type=int, default=3)
    parser.add_argument("--iteration-index", type=int)
    parser.add_argument("--prompt-text")
    parser.add_argument("--label-prefix", default="mx1")
    parser.add_argument("--max-depth", type=int)
    parser.add_argument("--max-helpers", type=int)
    parser.add_argument("--sync-supabase", action="store_true")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    question_path = Path(args.question_file).resolve()
    question_case = parse_question_file(question_path)
    loops_root = Path(args.loops_root).resolve()
    manifest_path = build_loop_manifest_path(
        question_id=question_case.question_id,
        family=args.family,
        loop_id=args.loop_id or build_loop_id(question_case.question_id, args.family, args.loop_label),
        loops_root=loops_root,
    )
    starter_prompt_path = _resolve_starter_prompt_path(args.family, args.starter_prompt_file)
    execute_prompt_path = Path(args.execute_prompt_file).resolve()
    starter_prompt_text = starter_prompt_path.read_text(encoding="utf-8").strip()
    execute_prompt_text = execute_prompt_path.read_text(encoding="utf-8").strip()

    manifest = _load_or_create_manifest(
        manifest_path=manifest_path,
        question_case=question_case,
        question_path=question_path,
        family=args.family,
        runtime_provider=args.runtime_provider,
        model=args.model,
        starter_prompt_text=starter_prompt_text,
        execute_prompt_text=execute_prompt_text,
        starter_prompt_file=str(starter_prompt_path),
        execute_prompt_file=str(execute_prompt_path),
        loop_label=args.loop_label,
        iterations_target=args.iterations_target,
        exploration_iterations=args.exploration_iterations,
    )

    if args.action == "init":
        _save_manifest(manifest_path, manifest)
        _print_manifest_summary(manifest_path, manifest)
        return 0

    if args.action == "status":
        _print_manifest_summary(manifest_path, manifest)
        return 0

    if args.action == "baseline":
        record = _run_baseline(
            args=args,
            question_case=question_case,
            question_path=question_path,
            manifest_path=manifest_path,
            manifest=manifest,
            execute_prompt_text=execute_prompt_text,
            execute_prompt_path=execute_prompt_path,
        )
    else:
        record = _run_family_iteration(
            args=args,
            question_case=question_case,
            question_path=question_path,
            manifest_path=manifest_path,
            manifest=manifest,
            execute_prompt_text=execute_prompt_text,
            execute_prompt_path=execute_prompt_path,
        )

    _print_attempt_result(record)
    _print_manifest_summary(manifest_path, load_json(manifest_path))
    return 0


def _load_or_create_manifest(
    *,
    manifest_path: Path,
    question_case: Any,
    question_path: Path,
    family: str,
    runtime_provider: str,
    model: str,
    starter_prompt_text: str,
    execute_prompt_text: str,
    starter_prompt_file: str,
    execute_prompt_file: str,
    loop_label: str,
    iterations_target: int,
    exploration_iterations: int,
) -> dict[str, Any]:
    if manifest_path.exists():
        manifest = load_json(manifest_path)
        manifest["iterations_target"] = iterations_target
        manifest["exploration_iterations"] = exploration_iterations
        _save_manifest(manifest_path, manifest)
        return manifest

    manifest = create_manifest(
        question_id=question_case.question_id,
        question_title=question_case.title,
        question_file=str(question_path),
        family=family,
        runtime_provider=runtime_provider,
        model=model,
        starter_prompt_text=starter_prompt_text,
        child_prompt_text=execute_prompt_text,
        loop_label=loop_label,
        starter_prompt_file=starter_prompt_file,
        child_prompt_file=execute_prompt_file,
        iterations_target=iterations_target,
        exploration_iterations=exploration_iterations,
    )
    _save_manifest(manifest_path, manifest)
    return manifest


def _run_baseline(
    *,
    args: argparse.Namespace,
    question_case: Any,
    question_path: Path,
    manifest_path: Path,
    manifest: dict[str, Any],
    execute_prompt_text: str,
    execute_prompt_path: Path,
) -> dict[str, Any]:
    label = f"{args.label_prefix}_baseline"
    run_id = f"{manifest['loop_id']}__baseline__{make_run_id()}"
    record = run_question_case(
        question_path=question_path,
        label=label,
        runtime_provider=args.runtime_provider,
        model=args.model,
        run_history_root=Path(args.run_history_root),
        grading_runs_root=Path(args.grading_runs_root),
        max_depth=0,
        max_helpers=0,
        run_id=run_id,
        sync_supabase=False,
        extra_variable_overrides={
            "prompt_family": "execute",
            "selected_prompt_text": execute_prompt_text,
            "base_header_prompt": "",
            "child_prompt_family": "execute",
            "child_selected_prompt_text": "",
            "child_base_header_prompt": "",
            "review_prompt_family": "",
            "review_selected_prompt_text": "",
            "review_base_header_prompt": "",
            "budget_policy": {
                "max_depth": 0,
                "max_helpers_per_node": 0,
                "max_turns_per_node": 1,
            },
        },
    )
    return _record_attempt(
        args=args,
        manifest_path=manifest_path,
        manifest=manifest,
        record=record,
        question_case=question_case,
        question_path=question_path,
        kind="baseline",
        iteration_index=0,
        label=label,
        prompt_text=execute_prompt_text,
        prompt_file=str(execute_prompt_path),
        prompt_family="execute",
        child_prompt_text=execute_prompt_text,
        child_prompt_family="execute",
        max_depth=0,
        max_helpers=0,
    )


def _run_family_iteration(
    *,
    args: argparse.Namespace,
    question_case: Any,
    question_path: Path,
    manifest_path: Path,
    manifest: dict[str, Any],
    execute_prompt_text: str,
    execute_prompt_path: Path,
) -> dict[str, Any]:
    family = str(manifest.get("family") or args.family or "transmute").strip()
    if family not in {"execute", "transmute", "delegate", "review"}:
        raise ValueError(f"Unsupported MX1 family: {family}")

    iteration_index = int(args.iteration_index or manifest.get("next_iteration_index") or 1)
    prompt_text = str(args.prompt_text or manifest.get("current_prompt_text") or manifest.get("starter_prompt_text") or "").strip()
    if not prompt_text:
        raise ValueError(f"No starter prompt text is available for family={family}.")
    is_coding = str(getattr(question_case, "entry_type", "") or "").strip() == "coding"
    effective_prompt_text = _effective_family_prompt_text(
        family=family,
        prompt_text=prompt_text,
        is_coding=is_coding,
    )
    effective_execute_prompt_text = _effective_child_execute_prompt_text(
        family=family,
        execute_prompt_text=execute_prompt_text,
        is_coding=is_coding,
    )

    family_config = _family_iteration_config(family)

    label = f"{args.label_prefix}_{family}_{iteration_index:02d}"
    run_id = f"{manifest['loop_id']}__{family}__{iteration_index:02d}__{make_run_id()}"
    record = run_question_case(
        question_path=question_path,
        label=label,
        runtime_provider=args.runtime_provider,
        model=args.model,
        run_history_root=Path(args.run_history_root),
        grading_runs_root=Path(args.grading_runs_root),
        max_depth=family_config["max_depth"],
        max_helpers=family_config["max_helpers"],
        run_id=run_id,
        sync_supabase=False,
        extra_variable_overrides=_family_variable_overrides(
            family=family,
            prompt_text=effective_prompt_text,
            execute_prompt_text=effective_execute_prompt_text,
            family_config=family_config,
        ),
    )
    return _record_attempt(
        args=args,
        manifest_path=manifest_path,
        manifest=manifest,
        record=record,
        question_case=question_case,
        question_path=question_path,
        kind=family,
        iteration_index=iteration_index,
        label=label,
        prompt_text=effective_prompt_text,
        prompt_file=None if args.prompt_text else _current_prompt_path(manifest),
        prompt_family=family,
        child_prompt_text=effective_execute_prompt_text,
        child_prompt_family="execute",
        max_depth=family_config["max_depth"],
        max_helpers=family_config["max_helpers"],
    )


def _record_attempt(
    *,
    args: argparse.Namespace,
    manifest_path: Path,
    manifest: dict[str, Any],
    record: dict[str, Any],
    question_case: Any,
    question_path: Path,
    kind: str,
    iteration_index: int,
    label: str,
    prompt_text: str,
    prompt_file: str | None,
    prompt_family: str,
    child_prompt_text: str,
    child_prompt_family: str,
    max_depth: int,
    max_helpers: int,
) -> dict[str, Any]:
    grading_record_path = Path(str(record["grading_record_path"]))
    grading_record = load_json(grading_record_path)

    attempt = {
        "iteration_index": iteration_index,
        "kind": kind,
        "label": label,
        "run_id": record["run_id"],
        "run_dir": record["run_dir"],
        "question_id": question_case.question_id,
        "question_file": str(question_path),
        "prompt_family": prompt_family,
        "prompt_text": prompt_text,
        "prompt_file": prompt_file,
        "child_prompt_family": child_prompt_family,
        "child_prompt_text": child_prompt_text,
        "score": grading_record.get("grading", {}).get("score"),
        "correct": grading_record.get("grading", {}).get("correct"),
        "total_tokens": grading_record.get("total_tokens"),
        "total_wall_time_ms": grading_record.get("total_wall_time_ms"),
        "total_cost_usd": grading_record.get("total_cost_usd"),
        "grading_record_path": str(grading_record_path),
        "tutor_record_path": None,
        "loop_manifest_path": str(manifest_path),
        "created_at_utc": grading_record.get("created_at_utc"),
        "max_depth": max_depth,
        "max_helpers": max_helpers,
        "root_orchestration": grading_record.get("root_orchestration"),
        "root_result_excerpt": grading_record.get("root_result_excerpt"),
        "final_result_excerpt": grading_record.get("final_result_excerpt"),
    }

    manifest = append_attempt(manifest, attempt)
    saved_attempt = _find_attempt(manifest, record["run_id"], iteration_index, kind)
    grading_record = update_grading_record_mx1(
        grading_record=grading_record,
        manifest=manifest,
        attempt=saved_attempt,
        tutor_record_path=saved_attempt.get("tutor_record_path"),
    )
    write_json(grading_record_path, grading_record)
    _save_manifest(manifest_path, manifest)
    if args.sync_supabase:
        supabase_config = load_supabase_config()
        sync_grading_record(config=supabase_config, grading_record_path=grading_record_path)
    return grading_record


def _current_prompt_path(manifest: dict[str, Any]) -> str | None:
    current = manifest.get("current_prompt_file")
    if current:
        return str(current)
    if manifest.get("current_prompt_source") == "starter":
        starter = manifest.get("starter_prompt_file")
        return str(starter) if starter else None
    return None


def _resolve_starter_prompt_path(family: str, starter_prompt_file: str) -> Path:
    family_name = str(family or "transmute").strip()
    if str(starter_prompt_file or "").strip():
        candidate = Path(starter_prompt_file).resolve()
        default_map = {
            "execute": DEFAULT_EXECUTE_PROMPT_FILE.resolve(),
            "delegate": DEFAULT_DELEGATE_PROMPT_FILE.resolve(),
            "review": DEFAULT_REVIEW_PROMPT_FILE.resolve(),
            "transmute": DEFAULT_STARTER_PROMPT_FILE.resolve(),
        }
        default_path = default_map.get(family_name, DEFAULT_STARTER_PROMPT_FILE.resolve())
        if candidate == default_path or candidate not in set(default_map.values()):
            return candidate
    if family_name == "delegate":
        return DEFAULT_DELEGATE_PROMPT_FILE.resolve()
    if family_name == "review":
        return DEFAULT_REVIEW_PROMPT_FILE.resolve()
    if family_name == "execute":
        return DEFAULT_EXECUTE_PROMPT_FILE.resolve()
    return DEFAULT_STARTER_PROMPT_FILE.resolve()


def _family_iteration_config(family: str) -> dict[str, int]:
    if family == "execute":
        return {
            "max_depth": 0,
            "max_helpers": 0,
            "max_turns_per_node": 1,
        }
    if family == "delegate":
        return {
            "max_depth": 1,
            "max_helpers": 2,
            "max_turns_per_node": 4,
        }
    if family == "review":
        return {
            "max_depth": 1,
            "max_helpers": 1,
            "max_turns_per_node": 4,
        }
    return {
        "max_depth": 1,
        "max_helpers": 1,
        "max_turns_per_node": 4,
    }


def _family_variable_overrides(
    *,
    family: str,
    prompt_text: str,
    execute_prompt_text: str,
    family_config: dict[str, int],
    ) -> dict[str, Any]:
    return {
        "prompt_family": family,
        "selected_prompt_text": prompt_text,
        "base_header_prompt": "",
        "child_prompt_family": "execute",
        "child_selected_prompt_text": execute_prompt_text,
        "child_base_header_prompt": "",
        "review_prompt_family": "",
        "review_selected_prompt_text": "",
        "review_base_header_prompt": "",
        "budget_policy": {
            "max_depth": family_config["max_depth"],
            "max_helpers_per_node": family_config["max_helpers"],
            "max_turns_per_node": family_config["max_turns_per_node"],
        },
    }


def _effective_family_prompt_text(*, family: str, prompt_text: str, is_coding: bool) -> str:
    if not is_coding:
        return prompt_text
    if family == "execute":
        return _coding_execute_prompt_text(prompt_text)
    return prompt_text


def _effective_child_execute_prompt_text(*, family: str, execute_prompt_text: str, is_coding: bool) -> str:
    if not is_coding:
        return execute_prompt_text
    if family == "transmute":
        return _coding_execute_prompt_text(execute_prompt_text)
    return execute_prompt_text


def _coding_execute_prompt_text(prompt_text: str) -> str:
    guidance = _strip_json_scaffold(prompt_text).strip()
    if not guidance:
        guidance = "Solve the coding problem and maximize the objective score while preserving output validity."
    return (
        f"{guidance}\n\n"
        "When orchestration_decision is 'execute_locally', you MUST submit exactly one Python file in the artifacts list:\n"
        "- path: main.py\n"
        "- content: the full Python source code as one escaped string\n\n"
        "The response field should be only a brief submission summary. Do not put contestant stdout in the response field.\n"
        "Your main.py must read from stdin and print only the contestant output required by the problem.\n"
        "Do not print explanations, labels, debug text, or estimated scores.\n"
        "If the Output section requires a leading count/header line, print it exactly.\n"
        "Prefer a simple valid baseline over malformed ambitious output.\n\n"
        "Return exactly one JSON object in this format:\n"
        "{\n"
        '  "schema_name": "eywa_node_response",\n'
        '  "schema_version": "v1",\n'
        '  "orchestration_decision": "execute_locally",\n'
        '  "decision_notes": "optional string",\n'
        '  "response": "brief submission summary",\n'
        '  "result_type": "code_submission",\n'
        '  "artifacts": [\n'
        "    {\n"
        '      "path": "main.py",\n'
        '      "content": "full Python file contents as one escaped string"\n'
        "    }\n"
        "  ]\n"
        "}"
    )


def _strip_json_scaffold(prompt_text: str) -> str:
    marker = "Return exactly one JSON object in this format:"
    if marker not in prompt_text:
        return prompt_text
    return prompt_text.split(marker, 1)[0].rstrip()


def _find_attempt(manifest: dict[str, Any], run_id: str, iteration_index: int, kind: str) -> dict[str, Any]:
    for attempt in manifest.get("attempts") or []:
        if attempt.get("run_id") == run_id and int(attempt.get("iteration_index") or 0) == iteration_index and attempt.get("kind") == kind:
            return attempt
    raise KeyError(f"Could not find attempt {run_id} / {kind} / {iteration_index} in manifest.")


def _save_manifest(manifest_path: Path, manifest: dict[str, Any]) -> None:
    write_json(manifest_path, manifest)


def _print_manifest_summary(manifest_path: Path, manifest: dict[str, Any]) -> None:
    summary = manifest.get("history_summary") or {}
    print(f"manifest_path={manifest_path}")
    print(f"loop_id={manifest.get('loop_id')}")
    print(f"question_id={manifest.get('question_id')}")
    print(f"family={manifest.get('family')}")
    print(f"status={manifest.get('status')}")
    print(f"current_prompt_source={manifest.get('current_prompt_source')}")
    print(f"current_prompt_text={manifest.get('current_prompt_text')}")
    print(f"next_iteration_index={manifest.get('next_iteration_index')}")
    print(f"best_iteration_index={summary.get('best_iteration_index')}")
    print(f"best_score={summary.get('best_score')}")
    print(f"best_prompt_text={summary.get('best_prompt_text')}")
    print(f"plateau_streak={summary.get('plateau_streak')}")
    print(f"needs_new_direction={summary.get('needs_new_direction')}")
    print(f"iterations_completed={summary.get('iterations_completed')}")


def _print_attempt_result(record: dict[str, Any]) -> None:
    print(f"question_id={record['question_id']}")
    print(f"label={record['label']}")
    print(f"run_id={record['run_id']}")
    print(f"run_dir={record['run_dir']}")
    print(f"grading_record={record['grading_record_path']}")
    print(f"node_count={record['node_count']}")
    print(f"total_tokens={record['total_tokens']}")
    print(f"total_wall_time_ms={record['total_wall_time_ms']}")
    print(f"total_cost_usd={record['total_cost_usd']}")
    print(f"validation_status={record['validation_status']}")
    print(f"grading_status={record['grading']['grading_status']}")
    print(f"correct={record['grading']['correct']}")
    print(f"score={record['grading']['score']}")


if __name__ == "__main__":
    raise SystemExit(main())

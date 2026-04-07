"""Helpers for Mission Exploration 1 loop manifests and attempt tracking."""

from __future__ import annotations

import json
import os
from pathlib import Path
import sys
import tempfile
from typing import Any, Dict, Iterable, List


THIS_DIR = Path(__file__).resolve().parent
RUNTIME_DIR = THIS_DIR.parents[1] / "eywa-system" / "runtime"
if str(RUNTIME_DIR) not in sys.path:
    sys.path.insert(0, str(RUNTIME_DIR))

from eywa_runtime.ids import utc_now_iso

DEFAULT_MX1_LOOPS_ROOT = THIS_DIR / "mx1-loops"

MX1_SCHEMA_NAME = "mx1_loop_manifest"
MX1_SCHEMA_VERSION = "v1"
DEFAULT_ITERATIONS_TARGET = 10
DEFAULT_EXPLORATION_ITERATIONS = 3
DEFAULT_PLATEAU_THRESHOLD = 0.10
DEFAULT_PLATEAU_PATIENCE = 2


def build_loop_id(question_id: str, family: str, loop_label: str = "pilot_v1") -> str:
    return f"{question_id}__{family}__{loop_label}"


def build_loop_manifest_path(
    *,
    question_id: str,
    family: str,
    loop_id: str | None = None,
    loops_root: Path | None = None,
) -> Path:
    resolved_loop_id = loop_id or build_loop_id(question_id, family)
    root = (loops_root or DEFAULT_MX1_LOOPS_ROOT).resolve()
    return root / question_id / family / f"{resolved_loop_id}.json"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(payload, indent=2)
    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=str(path.parent),
        delete=False,
    ) as handle:
        handle.write(serialized)
        temp_path = Path(handle.name)
    os.replace(temp_path, path)


def create_manifest(
    *,
    question_id: str,
    question_title: str,
    question_file: str,
    family: str,
    runtime_provider: str,
    model: str,
    starter_prompt_text: str,
    child_prompt_text: str,
    loop_label: str = "pilot_v1",
    loop_id: str | None = None,
    starter_prompt_file: str | None = None,
    child_prompt_file: str | None = None,
    base_header_prompt: str = "",
    child_prompt_family: str = "execute",
    child_base_header_prompt: str = "",
    iterations_target: int = DEFAULT_ITERATIONS_TARGET,
    exploration_iterations: int = DEFAULT_EXPLORATION_ITERATIONS,
    plateau_threshold: float = DEFAULT_PLATEAU_THRESHOLD,
    plateau_patience: int = DEFAULT_PLATEAU_PATIENCE,
) -> dict[str, Any]:
    resolved_loop_id = loop_id or build_loop_id(question_id, family, loop_label=loop_label)
    return {
        "schema_name": MX1_SCHEMA_NAME,
        "schema_version": MX1_SCHEMA_VERSION,
        "loop_id": resolved_loop_id,
        "loop_label": loop_label,
        "question_id": question_id,
        "question_title": question_title,
        "question_file": question_file,
        "family": family,
        "runtime_provider": runtime_provider,
        "model": model,
        "base_header_prompt": base_header_prompt,
        "starter_prompt_text": starter_prompt_text,
        "starter_prompt_file": starter_prompt_file,
        "execute_prompt_text": child_prompt_text,
        "execute_prompt_file": child_prompt_file,
        "current_prompt_text": starter_prompt_text,
        "current_prompt_source": "starter",
        "current_prompt_file": starter_prompt_file,
        "child_prompt_family": child_prompt_family,
        "child_prompt_text": child_prompt_text,
        "child_prompt_file": child_prompt_file,
        "child_base_header_prompt": child_base_header_prompt,
        "iterations_target": iterations_target,
        "exploration_iterations": exploration_iterations,
        "plateau_policy": {
            "efficiency_improvement_threshold": plateau_threshold,
            "patience": plateau_patience,
        },
        "created_at_utc": utc_now_iso(),
        "status": "initialized",
        "next_iteration_index": 0,
        "attempts": [],
        "best_attempt": None,
        "history_summary": {
            "best_iteration_index": None,
            "best_run_id": None,
            "best_score": None,
            "best_prompt_text": None,
            "best_total_tokens": None,
            "best_total_wall_time_ms": None,
            "best_total_cost_usd": None,
            "latest_iteration_index": None,
            "plateau_streak": 0,
            "needs_new_direction": False,
            "iterations_completed": 0,
        },
    }


def append_attempt(manifest: dict[str, Any], attempt: dict[str, Any]) -> dict[str, Any]:
    attempts = list(manifest.get("attempts") or [])
    preferred_kind = str(manifest.get("family") or "").strip() or None
    key = (attempt.get("iteration_index"), attempt.get("kind"))
    filtered = [
        item
        for item in attempts
        if (item.get("iteration_index"), item.get("kind")) != key
    ]
    filtered.append(dict(attempt))
    filtered.sort(key=_attempt_sort_key)
    manifest["attempts"] = filtered
    best_attempt = _choose_best_attempt(filtered, preferred_kind=preferred_kind)
    manifest["best_attempt"] = best_attempt
    manifest["attempts"] = [
        _with_best_flag(item, best_attempt)
        for item in filtered
    ]
    manifest["best_attempt"] = _choose_best_attempt(manifest["attempts"], preferred_kind=preferred_kind)
    manifest["history_summary"] = _build_history_summary(manifest)
    manifest["next_iteration_index"] = _next_iteration_index(filtered, preferred_kind=preferred_kind)
    manifest["status"] = _derive_status(manifest)
    return manifest


def _attempt_sort_key(attempt: dict[str, Any]) -> tuple[int, int, str]:
    kind_rank = 0 if attempt.get("kind") == "baseline" else 1
    return (
        int(attempt.get("iteration_index") or 0),
        kind_rank,
        str(attempt.get("run_id") or ""),
    )


def _with_best_flag(attempt: dict[str, Any], best_attempt: dict[str, Any] | None) -> dict[str, Any]:
    updated = dict(attempt)
    updated["is_best"] = bool(
        best_attempt
        and updated.get("iteration_index") == best_attempt.get("iteration_index")
        and updated.get("kind") == best_attempt.get("kind")
        and updated.get("run_id") == best_attempt.get("run_id")
    )
    return updated


def _choose_best_attempt(
    attempts: List[dict[str, Any]],
    *,
    preferred_kind: str | None = None,
) -> dict[str, Any] | None:
    scoped_attempts = list(attempts)
    if preferred_kind:
        preferred = [attempt for attempt in scoped_attempts if str(attempt.get("kind") or "") == preferred_kind]
        if preferred:
            scoped_attempts = preferred
    scored = [attempt for attempt in scoped_attempts if attempt.get("score") is not None]
    if not scored:
        return scoped_attempts[-1] if scoped_attempts else None
    max_score = max(float(attempt.get("score") or 0.0) for attempt in scored)
    if max_score <= 0.0:
        return sorted(scored, key=_attempt_sort_key)[-1]
    return sorted(scored, key=_best_attempt_sort_key, reverse=True)[0]


def _best_attempt_sort_key(attempt: dict[str, Any]) -> tuple[float, float, float, int]:
    score = float(attempt.get("score") or 0.0)
    total_tokens = float(attempt.get("total_tokens") or 0.0)
    wall_time = float(attempt.get("total_wall_time_ms") or 0.0)
    iteration_index = int(attempt.get("iteration_index") or 0)
    return (score, -total_tokens, -wall_time, -iteration_index)


def _build_history_summary(manifest: dict[str, Any]) -> dict[str, Any]:
    attempts = list(manifest.get("attempts") or [])
    preferred_kind = str(manifest.get("family") or "").strip() or None
    best_attempt = manifest.get("best_attempt") or _choose_best_attempt(attempts, preferred_kind=preferred_kind)
    plateau_streak, needs_new_direction = _compute_plateau_state(attempts, manifest)
    family_attempts = [
        attempt for attempt in attempts if str(attempt.get("kind") or "") == preferred_kind
    ] if preferred_kind else list(attempts)
    summary = {
        "best_iteration_index": best_attempt.get("iteration_index") if best_attempt else None,
        "best_run_id": best_attempt.get("run_id") if best_attempt else None,
        "best_score": best_attempt.get("score") if best_attempt else None,
        "best_prompt_text": best_attempt.get("prompt_text") if best_attempt else None,
        "best_total_tokens": best_attempt.get("total_tokens") if best_attempt else None,
        "best_total_wall_time_ms": best_attempt.get("total_wall_time_ms") if best_attempt else None,
        "best_total_cost_usd": best_attempt.get("total_cost_usd") if best_attempt else None,
        "latest_iteration_index": attempts[-1].get("iteration_index") if attempts else None,
        "plateau_streak": plateau_streak,
        "needs_new_direction": needs_new_direction,
        "iterations_completed": len(family_attempts),
    }
    return summary


def _compute_plateau_state(
    attempts: List[dict[str, Any]],
    manifest: dict[str, Any],
) -> tuple[int, bool]:
    threshold = float((manifest.get("plateau_policy") or {}).get("efficiency_improvement_threshold", 0.10))
    patience = int((manifest.get("plateau_policy") or {}).get("patience", 2))
    family = str(manifest.get("family") or "").strip()
    ordered = sorted(attempts, key=_attempt_sort_key)
    if len(ordered) < 2:
        return 0, False

    streak = 0
    for previous, current in zip(ordered[:-1], ordered[1:]):
        if family and str(current.get("kind") or "") != family:
            continue
        if _is_plateau(previous, current, threshold):
            streak += 1
        else:
            streak = 0
    return streak, streak >= patience


def _is_plateau(
    previous: dict[str, Any],
    current: dict[str, Any],
    threshold: float,
) -> bool:
    previous_score = float(previous.get("score") or 0.0)
    current_score = float(current.get("score") or 0.0)
    if current_score < previous_score:
        return False
    if current_score <= 0.0 and previous_score <= 0.0:
        return True

    previous_tokens = float(previous.get("total_tokens") or 0.0)
    current_tokens = float(current.get("total_tokens") or 0.0)
    previous_time = float(previous.get("total_wall_time_ms") or 0.0)
    current_time = float(current.get("total_wall_time_ms") or 0.0)

    tokens_improvement = _relative_improvement(previous_tokens, current_tokens)
    time_improvement = _relative_improvement(previous_time, current_time)
    return tokens_improvement < threshold and time_improvement < threshold


def _relative_improvement(previous: float, current: float) -> float:
    if previous <= 0:
        return 0.0
    return max(0.0, (previous - current) / previous)


def _next_iteration_index(
    attempts: List[dict[str, Any]],
    *,
    preferred_kind: str | None = None,
) -> int:
    relevant_iterations = [
        int(attempt.get("iteration_index") or 0)
        for attempt in attempts
        if not preferred_kind or str(attempt.get("kind") or "") == preferred_kind
    ]
    if not relevant_iterations:
        return 1
    return max(relevant_iterations) + 1


def _derive_status(manifest: dict[str, Any]) -> str:
    summary = manifest.get("history_summary") or {}
    if summary.get("iterations_completed", 0) >= int(manifest.get("iterations_target") or 0):
        return "complete"
    if not manifest.get("attempts"):
        return "initialized"
    if summary.get("needs_new_direction"):
        return "plateau"
    return "in_progress"


def update_grading_record_mx1(
    *,
    grading_record: dict[str, Any],
    manifest: dict[str, Any],
    attempt: dict[str, Any],
    tutor_record_path: str | None = None,
) -> dict[str, Any]:
    summary = manifest.get("history_summary") or {}
    grading_record = dict(grading_record)
    mx1_payload = {
        "loop_id": manifest.get("loop_id"),
        "loop_label": manifest.get("loop_label"),
        "question_id": manifest.get("question_id"),
        "family": manifest.get("family"),
        "iteration_index": attempt.get("iteration_index"),
        "kind": attempt.get("kind"),
        "prompt_text": attempt.get("prompt_text"),
        "prompt_file": attempt.get("prompt_file"),
        "child_prompt_family": manifest.get("child_prompt_family"),
        "child_prompt_text": manifest.get("child_prompt_text"),
        "tutor_record_path": tutor_record_path or attempt.get("tutor_record_path"),
        "loop_manifest_path": attempt.get("loop_manifest_path"),
        "best_iteration_index": summary.get("best_iteration_index"),
        "best_run_id": summary.get("best_run_id"),
        "best_score": summary.get("best_score"),
        "best_prompt_text": summary.get("best_prompt_text"),
        "needs_new_direction": summary.get("needs_new_direction"),
        "plateau_streak": summary.get("plateau_streak"),
        "is_best": attempt.get("is_best"),
    }
    grading_record["mx1"] = mx1_payload
    grading_record["mx1_loop_id"] = mx1_payload["loop_id"]
    grading_record["mx1_family"] = mx1_payload["family"]
    grading_record["mx1_iteration_index"] = mx1_payload["iteration_index"]
    grading_record["mx1_iteration_kind"] = mx1_payload["kind"]
    grading_record["mx1_prompt_text"] = mx1_payload["prompt_text"]
    grading_record["mx1_prompt_file"] = mx1_payload["prompt_file"]
    grading_record["mx1_child_prompt_family"] = mx1_payload["child_prompt_family"]
    grading_record["mx1_child_prompt_text"] = mx1_payload["child_prompt_text"]
    grading_record["mx1_tutor_record_path"] = mx1_payload["tutor_record_path"]
    grading_record["mx1_loop_manifest_path"] = mx1_payload["loop_manifest_path"]
    grading_record["mx1_best_iteration_index"] = mx1_payload["best_iteration_index"]
    grading_record["mx1_best_run_id"] = mx1_payload["best_run_id"]
    grading_record["mx1_best_score"] = mx1_payload["best_score"]
    grading_record["mx1_best_prompt_text"] = mx1_payload["best_prompt_text"]
    grading_record["mx1_needs_new_direction"] = mx1_payload["needs_new_direction"]
    grading_record["mx1_plateau_streak"] = mx1_payload["plateau_streak"]
    grading_record["mx1_is_best"] = mx1_payload["is_best"]
    return grading_record

#!/usr/bin/env python3
"""Run the MX1 prompt-optimization tutor for one loop attempt."""

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

from mx1_loop_v1 import load_json, update_grading_record_mx1, write_json  # noqa: E402
from mx1_tutor_v1 import looks_question_specific, run_mx1_tutor  # noqa: E402
from sync_to_supabase_v1 import load_supabase_config, sync_grading_record  # noqa: E402


DEFAULT_TUTORING_ROOT = THIS_DIR / "mx1-tutoring"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the MX1 tutor for one loop attempt.")
    parser.add_argument("--manifest", required=True, help="Path to the MX1 loop manifest JSON.")
    parser.add_argument("--grading-record", help="Optional explicit grading record path.")
    parser.add_argument("--tutoring-root", default=str(DEFAULT_TUTORING_ROOT))
    parser.add_argument(
        "--tutor-provider",
        default="same",
        choices=["same", "deterministic", "openrouter"],
    )
    parser.add_argument("--tutor-model", help="Optional explicit tutor model. Defaults to the run model.")
    parser.add_argument("--iteration-index", type=int, help="Optional attempt index to tutor.")
    parser.add_argument("--sync-supabase", action="store_true")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    manifest_path = Path(args.manifest).resolve()
    manifest = load_json(manifest_path)
    target_attempt = _resolve_target_attempt(manifest, args.iteration_index)
    grading_record_path = Path(
        args.grading_record
        or target_attempt.get("grading_record_path")
        or ""
    ).resolve()
    tutoring_root = Path(args.tutoring_root).resolve()

    tutor_record = run_mx1_tutor(
        manifest_path=manifest_path,
        grading_record_path=grading_record_path,
        tutoring_root=tutoring_root,
        tutor_provider=args.tutor_provider,
        tutor_model=args.tutor_model,
    )

    grading_record = load_json(grading_record_path)
    manifest = load_json(manifest_path)
    updated_manifest = _apply_tutor_result(manifest, tutor_record)
    write_json(manifest_path, updated_manifest)

    grading_record = _apply_tutor_result_to_grading_record(grading_record, updated_manifest, tutor_record)
    write_json(grading_record_path, grading_record)

    if args.sync_supabase:
        supabase_config = load_supabase_config()
        sync_grading_record(config=supabase_config, grading_record_path=grading_record_path)

    print(f"manifest={manifest_path}")
    print(f"grading_record={grading_record_path}")
    print(f"tutor_record={tutor_record['tutor_record_path']}")
    print(f"question_id={manifest.get('question_id')}")
    print(f"family={manifest.get('family')}")
    print(f"iteration_index={target_attempt.get('iteration_index')}")
    print(f"new_prompt_text={tutor_record['tutor']['recommendation']['new_prompt_text']}")
    print(f"recommendation_action={tutor_record['tutor']['recommendation']['action']}")
    return 0


def _resolve_target_attempt(manifest: dict[str, Any], iteration_index: int | None) -> dict[str, Any]:
    attempts = list(manifest.get("attempts") or [])
    if not attempts:
        raise ValueError("The MX1 manifest does not contain any attempts.")
    if iteration_index is None:
        return sorted(
            attempts,
            key=lambda item: (int(item.get("iteration_index") or 0), str(item.get("kind") or "")),
        )[-1]
    for attempt in attempts:
        if int(attempt.get("iteration_index") or 0) == iteration_index:
            return attempt
    raise ValueError(f"Could not find iteration_index={iteration_index} in the manifest.")


def _apply_tutor_result(manifest: dict[str, Any], tutor_record: dict[str, Any]) -> dict[str, Any]:
    manifest = dict(manifest)
    attempts = list(manifest.get("attempts") or [])
    target_iteration = int(tutor_record.get("iteration_index") or 0)
    raw_recommendation = dict((tutor_record.get("tutor") or {}).get("recommendation") or {})
    raw_prompt_text = raw_recommendation.get("new_prompt_text")
    applied_prompt_text, normalization_reason = _normalize_family_prompt_text(manifest, raw_prompt_text)
    updated_attempts = []
    for attempt in attempts:
        if int(attempt.get("iteration_index") or 0) == target_iteration:
            updated = dict(attempt)
            updated["tutor_record_path"] = tutor_record.get("tutor_record_path")
            updated["tutor"] = tutor_record.get("tutor") or {}
            updated["recommendation"] = {
                **raw_recommendation,
                "applied_prompt_text": applied_prompt_text,
                "normalization_reason": normalization_reason,
            }
            updated["next_prompt_text"] = applied_prompt_text
            updated_attempts.append(updated)
            continue
        updated_attempts.append(attempt)
    manifest["attempts"] = updated_attempts
    if applied_prompt_text:
        manifest["current_prompt_text"] = applied_prompt_text
        manifest["current_prompt_source"] = "tutor"
        manifest["current_prompt_file"] = None
    manifest["status"] = "awaiting_next_iteration"
    return manifest


def _normalize_family_prompt_text(manifest: dict[str, Any], prompt_text: str | None) -> tuple[str, str | None]:
    text = str(prompt_text or "").strip()
    if not text:
        return "", None
    starter_text = str(manifest.get("starter_prompt_text") or "").strip()
    canonical_scaffold = _extract_prompt_scaffold(starter_text)
    starter_guidance = _remove_prompt_scaffold(starter_text).strip()
    if not canonical_scaffold:
        return text, None
    leading_guidance = _remove_prompt_scaffold(text).strip()
    if not leading_guidance:
        return canonical_scaffold, None
    if looks_question_specific(leading_guidance):
        fallback_guidance = starter_guidance or leading_guidance
        return f"{fallback_guidance}\n\n{canonical_scaffold}", "coerced_to_family_level_prompt"
    return f"{leading_guidance}\n\n{canonical_scaffold}", None


def _remove_prompt_scaffold(prompt_text: str) -> str:
    marker = "Return exactly one JSON object in this format:"
    if marker not in prompt_text:
        return prompt_text
    return prompt_text.split(marker, 1)[0].rstrip()


def _extract_prompt_scaffold(prompt_text: str) -> str:
    marker = "Return exactly one JSON object in this format:"
    if marker not in prompt_text:
        return ""
    return marker + prompt_text.split(marker, 1)[1]


def _apply_tutor_result_to_grading_record(
    grading_record: dict[str, Any],
    manifest: dict[str, Any],
    tutor_record: dict[str, Any],
) -> dict[str, Any]:
    grading_record = dict(grading_record)
    current_attempt = _resolve_target_attempt(manifest, tutor_record.get("iteration_index"))
    grading_record["mx1_tutor_record_path"] = tutor_record.get("tutor_record_path")
    grading_record["mx1_tutor"] = tutor_record.get("tutor") or {}
    grading_record["mx1"] = {
        **(grading_record.get("mx1") or {}),
        "tutor_record_path": tutor_record.get("tutor_record_path"),
        "tutor": tutor_record.get("tutor") or {},
        "current_prompt_text": manifest.get("current_prompt_text"),
        "current_prompt_source": manifest.get("current_prompt_source"),
        "next_prompt_text": (tutor_record.get("tutor") or {}).get("recommendation", {}).get("new_prompt_text"),
        "best_iteration_index": (manifest.get("history_summary") or {}).get("best_iteration_index"),
        "best_run_id": (manifest.get("history_summary") or {}).get("best_run_id"),
        "best_score": (manifest.get("history_summary") or {}).get("best_score"),
    }
    grading_record = update_grading_record_mx1(
        grading_record=grading_record,
        manifest=manifest,
        attempt=current_attempt,
        tutor_record_path=tutor_record.get("tutor_record_path"),
    )
    return grading_record


if __name__ == "__main__":
    raise SystemExit(main())

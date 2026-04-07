#!/usr/bin/env python3
"""Compare two MX1 loop labels across the benchmark matrix."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


THIS_DIR = Path(__file__).resolve().parent
DEFAULT_BENCHMARK_FILE = THIS_DIR / "benchmarks" / "mx1-three-question-v1.json"
DEFAULT_LOOPS_ROOT = THIS_DIR / "mx1-loops"
DEFAULT_OUTPUT_ROOT = THIS_DIR / "comparisons"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compare two MX1 loop labels.")
    parser.add_argument("--benchmark-file", default=str(DEFAULT_BENCHMARK_FILE))
    parser.add_argument("--loops-root", default=str(DEFAULT_LOOPS_ROOT))
    parser.add_argument("--old-label", required=True)
    parser.add_argument("--new-label", required=True)
    parser.add_argument("--output")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    benchmark_path = Path(args.benchmark_file).resolve()
    loops_root = Path(args.loops_root).resolve()
    benchmark = json.loads(benchmark_path.read_text(encoding="utf-8"))
    payload = build_comparison_payload(
        benchmark=benchmark,
        loops_root=loops_root,
        old_label=args.old_label,
        new_label=args.new_label,
    )

    output_path = Path(args.output).resolve() if args.output else (
        DEFAULT_OUTPUT_ROOT / f"{args.old_label}__vs__{args.new_label}.json"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"output={output_path}")
    return 0


def build_comparison_payload(
    *,
    benchmark: dict[str, Any],
    loops_root: Path,
    old_label: str,
    new_label: str,
) -> dict[str, Any]:
    questions = list(benchmark.get("questions") or [])
    families = [str(f).strip() for f in list(benchmark.get("families") or [])]
    rows: list[dict[str, Any]] = []
    for question_entry in questions:
        question_id = str(question_entry.get("question_id") or "").strip()
        for family in families:
            old_manifest = load_manifest(loops_root, question_id, family, old_label)
            new_manifest = load_manifest(loops_root, question_id, family, new_label)
            rows.append(
                {
                    "question_id": question_id,
                    "family": family,
                    "old": summarize_manifest(old_manifest),
                    "new": summarize_manifest(new_manifest),
                    "score_delta": _score_delta(old_manifest, new_manifest),
                    "iterations_delta": _iterations_delta(old_manifest, new_manifest),
                }
            )

    return {
        "schema_name": "mx1_label_comparison",
        "schema_version": "v1",
        "benchmark_id": benchmark.get("benchmark_id"),
        "old_label": old_label,
        "new_label": new_label,
        "aggregate": {
            "old": aggregate_side(rows, "old"),
            "new": aggregate_side(rows, "new"),
        },
        "rows": rows,
    }


def load_manifest(loops_root: Path, question_id: str, family: str, label: str) -> dict[str, Any] | None:
    path = loops_root / question_id / family / f"{question_id}__{family}__{label}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def summarize_manifest(manifest: dict[str, Any] | None) -> dict[str, Any] | None:
    if manifest is None:
        return None
    summary = dict(manifest.get("history_summary") or {})
    return {
        "status": manifest.get("status"),
        "iterations_completed": summary.get("iterations_completed"),
        "best_score": summary.get("best_score"),
        "best_iteration_index": summary.get("best_iteration_index"),
        "best_run_id": summary.get("best_run_id"),
        "best_total_tokens": summary.get("best_total_tokens"),
        "best_total_wall_time_ms": summary.get("best_total_wall_time_ms"),
        "best_total_cost_usd": summary.get("best_total_cost_usd"),
    }


def aggregate_side(rows: list[dict[str, Any]], side: str) -> dict[str, Any]:
    manifests = [row[side] for row in rows if row.get(side)]
    scores = [float(item.get("best_score") or 0.0) for item in manifests]
    completed = [item for item in manifests if item.get("status") == "complete"]
    return {
        "manifest_count": len(manifests),
        "completed_count": len(completed),
        "average_best_score": (sum(scores) / len(scores)) if scores else None,
        "nonzero_best_score_count": len([score for score in scores if score > 0.0]),
    }


def _score_delta(old_manifest: dict[str, Any] | None, new_manifest: dict[str, Any] | None) -> float | None:
    if old_manifest is None or new_manifest is None:
        return None
    old_score = float(((old_manifest.get("history_summary") or {}).get("best_score")) or 0.0)
    new_score = float(((new_manifest.get("history_summary") or {}).get("best_score")) or 0.0)
    return new_score - old_score


def _iterations_delta(old_manifest: dict[str, Any] | None, new_manifest: dict[str, Any] | None) -> int | None:
    if old_manifest is None or new_manifest is None:
        return None
    old_iterations = int(((old_manifest.get("history_summary") or {}).get("iterations_completed")) or 0)
    new_iterations = int(((new_manifest.get("history_summary") or {}).get("iterations_completed")) or 0)
    return new_iterations - old_iterations


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Run a small live grading batch with baseline and main variants."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


THIS_DIR = Path(__file__).resolve().parent
RUNNER = THIS_DIR / "run_test_question_v1.py"

DEFAULT_QUESTION_FILES = [
    "data-system/grading/test-questions/architecture-derived-B4-hensel-lifting-verification.md",
    "data-system/grading/test-questions/architecture-derived-B5-combinatorial-probability-random-chords.md",
    "data-system/grading/test-questions/architecture-derived-B6-binary-representation-minimization.md",
    "data-system/grading/test-questions/architecture-derived-B10-mean-field-lattice-gas-occupancy.md",
    "data-system/grading/test-questions/architecture-derived-B11-board-game-rule-chaining.md",
]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the default live grading batch for Super-Eywa v1.")
    parser.add_argument("--runtime-provider", default="openrouter", choices=["deterministic", "openrouter"])
    parser.add_argument("--model", default="openai/gpt-4.1-mini")
    parser.add_argument("--run-history-root", default=str(THIS_DIR.parents[1] / "data-system" / "run-history"))
    parser.add_argument("--grading-runs-root", default=str(THIS_DIR / "runs"))
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    repo_root = THIS_DIR.parents[1]
    batch_results = []
    for relative_question_file in DEFAULT_QUESTION_FILES:
        question_path = repo_root / relative_question_file
        for label, max_depth in [("baseline", "0"), ("main", "3")]:
            completed = subprocess.run(
                [
                    "python3",
                    str(RUNNER),
                    "--question-file",
                    str(question_path),
                    "--label",
                    label,
                    "--runtime-provider",
                    args.runtime_provider,
                    "--model",
                    args.model,
                    "--run-history-root",
                    args.run_history_root,
                    "--grading-runs-root",
                    args.grading_runs_root,
                    "--max-depth",
                    max_depth,
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            parsed = parse_stdout(completed.stdout)
            batch_results.append(parsed)

    batch_record = {
        "runtime_provider": args.runtime_provider,
        "model": args.model,
        "question_files": DEFAULT_QUESTION_FILES,
        "results": batch_results,
    }
    batch_path = Path(args.grading_runs_root) / "live-batch-v1-summary.json"
    batch_path.write_text(json.dumps(batch_record, indent=2), encoding="utf-8")
    print(f"batch_summary={batch_path}")
    print(f"result_count={len(batch_results)}")
    return 0


def parse_stdout(stdout: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for line in stdout.splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        parsed[key.strip()] = value.strip()
    return parsed


if __name__ == "__main__":
    raise SystemExit(main())

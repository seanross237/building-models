#!/usr/bin/env python3
"""Generate the canonical Super-Eywa grading question-bank catalog."""

from __future__ import annotations

import argparse
from pathlib import Path

from question_bank_v1 import DEFAULT_QUESTION_BANK_PATH, TEST_QUESTIONS_DIR, write_question_bank_catalog


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build the canonical Super-Eywa question bank catalog.")
    parser.add_argument("--question-dir", default=str(TEST_QUESTIONS_DIR))
    parser.add_argument("--output", default=str(DEFAULT_QUESTION_BANK_PATH))
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    output_path = write_question_bank_catalog(
        question_dir=Path(args.question_dir),
        output_path=Path(args.output),
    )
    print(f"question_bank={output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

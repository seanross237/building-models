#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


SCRIPTS = [
    "validation-suite/tool-tests/filesystem_and_jobs_smoke.py",
    "validation-suite/math-tests/math_tools_smoke.py",
    "validation-suite/golden-missions/orchestrator_helpers_smoke.py",
]


def main() -> int:
    repo_root = Path(__file__).resolve().parents[2]
    failures = 0
    for relative in SCRIPTS:
        script = repo_root / relative
        print(f"[validation] {relative}")
        completed = subprocess.run([sys.executable, str(script)], cwd=str(repo_root), check=False)
        if completed.returncode != 0:
            failures += 1
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

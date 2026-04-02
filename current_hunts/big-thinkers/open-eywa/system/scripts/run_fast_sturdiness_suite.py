from __future__ import annotations

import py_compile
from pathlib import Path
import subprocess
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONTRACT_TESTS_DIR = PROJECT_ROOT / "validation-suite" / "contract-tests"
ADVERSARIAL_TESTS_DIR = PROJECT_ROOT / "validation-suite" / "adversarial-tests"
SYSTEM_DIR = PROJECT_ROOT / "system"


def compile_system_modules() -> list[str]:
    failures: list[str] = []
    for path in sorted(SYSTEM_DIR.rglob("*.py")):
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError as exc:
            failures.append(f"{path}: {exc.msg}")
    return failures


def run_suite(start_dir: Path) -> int:
    command = [
        sys.executable,
        "-m",
        "unittest",
        "discover",
        "-s",
        str(start_dir),
        "-p",
        "test_*.py",
    ]
    completed = subprocess.run(command, cwd=str(PROJECT_ROOT))
    return completed.returncode


def main() -> int:
    print("Running contract tests...")
    contract_exit = run_suite(CONTRACT_TESTS_DIR)
    print("\nRunning adversarial tests...")
    adversarial_exit = run_suite(ADVERSARIAL_TESTS_DIR)

    print("\nCompiling system modules...")
    compile_failures = compile_system_modules()
    if compile_failures:
        for failure in compile_failures:
            print(failure)
    else:
        print("compile check passed")

    if contract_exit == 0 and adversarial_exit == 0 and not compile_failures:
        print("\nfast sturdiness suite passed")
        return 0

    print("\nfast sturdiness suite failed")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

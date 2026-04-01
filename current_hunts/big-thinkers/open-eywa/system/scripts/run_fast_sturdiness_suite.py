from __future__ import annotations

import py_compile
from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONTRACT_TESTS_DIR = PROJECT_ROOT / "validation-suite" / "contract-tests"
ADVERSARIAL_TESTS_DIR = PROJECT_ROOT / "validation-suite" / "adversarial-tests"
SYSTEM_DIR = PROJECT_ROOT / "system"


def discover_suite(start_dir: Path) -> unittest.TestSuite:
    return unittest.defaultTestLoader.discover(
        start_dir=str(start_dir),
        pattern="test_*.py",
    )


def compile_system_modules() -> list[str]:
    failures: list[str] = []
    for path in sorted(SYSTEM_DIR.rglob("*.py")):
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError as exc:
            failures.append(f"{path}: {exc.msg}")
    return failures


def main() -> int:
    suite = unittest.TestSuite(
        [
            discover_suite(CONTRACT_TESTS_DIR),
            discover_suite(ADVERSARIAL_TESTS_DIR),
        ]
    )

    print("Running fast sturdiness suite...")
    result = unittest.TextTestRunner(verbosity=2).run(suite)

    print("\nCompiling system modules...")
    compile_failures = compile_system_modules()
    if compile_failures:
        for failure in compile_failures:
            print(failure)
    else:
        print("compile check passed")

    if result.wasSuccessful() and not compile_failures:
        print("\nfast sturdiness suite passed")
        return 0

    print("\nfast sturdiness suite failed")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

import sys
import tempfile
from pathlib import Path


def bootstrap() -> Path:
    repo_root = Path(__file__).resolve().parents[2]
    system_root = repo_root / "system"
    if str(system_root) not in sys.path:
        sys.path.insert(0, str(system_root))
    return repo_root


def main() -> int:
    repo_root = bootstrap()
    from tools.registry import ToolRegistry

    with tempfile.TemporaryDirectory(dir=repo_root / "validation-suite" / "math-tests") as tmp:
        mission_dir = Path(tmp) / "mission"
        node_dir = mission_dir / "tree" / "root"
        for subdir in ["input", "output", "for-orchestrator", "system"]:
            (node_dir / subdir).mkdir(parents=True, exist_ok=True)
        registry = ToolRegistry(
            repo_root=repo_root,
            mission_dir=mission_dir,
            node_path=node_dir,
            role="worker",
            tool_names=["run_python", "run_sage", "run_lean"],
            preview_chars=800,
        )

        py_result = registry.execute("run_python", {"code": "print(2 + 2)"})
        assert py_result["returncode"] == 0
        assert "4" in py_result["stdout"]

        sage_result = registry.execute("run_sage", {"code": "print(factor(12))"})
        assert sage_result["returncode"] == 0
        assert "3" in sage_result["stdout"]

        lean_result = registry.execute(
            "run_lean",
            {"code": "example : 1 = 1 := rfl\n", "timeout_seconds": 5},
        )
        assert lean_result["returncode"] in {0, 124}

    print("math_tools_smoke: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

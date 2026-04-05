#!/usr/bin/env python3
from __future__ import annotations

import sys
import tempfile
import time
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

    with tempfile.TemporaryDirectory(dir=repo_root / "validation-suite" / "tool-tests") as tmp:
        mission_dir = Path(tmp) / "mission"
        node_dir = mission_dir / "tree" / "root"
        for subdir in ["input", "output", "for-orchestrator", "system"]:
            (node_dir / subdir).mkdir(parents=True, exist_ok=True)
        registry = ToolRegistry(
            repo_root=repo_root,
            mission_dir=mission_dir,
            node_path=node_dir,
            role="worker",
            tool_names=[
                "read_file",
                "write_file",
                "edit_file",
                "glob",
                "grep",
                "start_background_job",
                "check_background_job",
            ],
            preview_chars=800,
        )

        registry.execute("write_file", {"path": "output/example.txt", "content": "alpha\nbeta\n"})
        read_result = registry.execute("read_file", {"path": "output/example.txt"})
        assert "alpha" in read_result["content"]

        registry.execute(
            "edit_file",
            {
                "path": "output/example.txt",
                "find_text": "beta",
                "replace_text": "gamma",
            },
        )
        grep_result = registry.execute("grep", {"pattern": "gamma", "path": "output"})
        assert grep_result["matches"], "grep should find the edited line"

        glob_result = registry.execute("glob", {"pattern": "output/*.txt"})
        assert glob_result["matches"], "glob should find the written file"

        registry.execute(
            "start_background_job",
            {
                "command": "python3 -c \"from pathlib import Path; Path('job-output.txt').write_text('done')\"",
                "label": "smoke-job",
            },
        )
        time.sleep(1.5)
        status = registry.execute("check_background_job", {"job_id": "smoke-job"})
        assert status["status"] in {"completed", "failed"}, status
        assert (node_dir / "for-orchestrator" / "computation_result").exists()

    print("filesystem_and_jobs_smoke: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

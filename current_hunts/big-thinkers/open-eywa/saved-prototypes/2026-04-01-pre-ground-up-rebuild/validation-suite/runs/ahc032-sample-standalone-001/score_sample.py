#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


MOD = 998244353


def parse_input(path: Path) -> tuple[int, int, int, list[list[int]], list[list[list[int]]]]:
    nums = list(map(int, path.read_text(encoding="utf-8").split()))
    ptr = 0
    n, m, k = nums[ptr], nums[ptr + 1], nums[ptr + 2]
    ptr += 3
    board = []
    for _ in range(n):
        board.append(nums[ptr : ptr + n])
        ptr += n
    stamps = []
    for _ in range(m):
        stamp = []
        for _ in range(3):
            stamp.append(nums[ptr : ptr + 3])
            ptr += 3
        stamps.append(stamp)
    return n, m, k, board, stamps


def score_solver(solver_path: Path, sample_input: Path) -> dict[str, object]:
    n, m, k, board, stamps = parse_input(sample_input)
    run = subprocess.run(
        [sys.executable, str(solver_path)],
        input=sample_input.read_text(encoding="utf-8"),
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )
    if run.returncode != 0:
        return {
            "valid": False,
            "error": "solver_nonzero_exit",
            "returncode": run.returncode,
            "stderr": run.stderr[-2000:],
        }
    lines = [line.strip() for line in run.stdout.splitlines() if line.strip()]
    if not lines:
        return {"valid": False, "error": "empty_output"}
    try:
        l = int(lines[0])
    except ValueError:
        return {"valid": False, "error": "bad_first_line", "stdout": run.stdout[-2000:]}
    if not (0 <= l <= k):
        return {"valid": False, "error": "operation_count_out_of_range", "operations": l}
    if len(lines) != l + 1:
        return {"valid": False, "error": "wrong_line_count", "expected": l + 1, "actual": len(lines)}
    work = [row[:] for row in board]
    ops = []
    try:
        for i in range(1, l + 1):
            mm, p, q = map(int, lines[i].split())
            if not (0 <= mm < m and 0 <= p <= n - 3 and 0 <= q <= n - 3):
                return {"valid": False, "error": "operation_out_of_range", "line": i, "op": [mm, p, q]}
            stamp = stamps[mm]
            for di in range(3):
                for dj in range(3):
                    work[p + di][q + dj] += stamp[di][dj]
            ops.append([mm, p, q])
    except Exception as exc:  # noqa: BLE001
        return {"valid": False, "error": "parse_failure", "message": str(exc)}
    score = sum(cell % MOD for row in work for cell in row)
    return {
        "valid": True,
        "score": score,
        "operations": l,
        "returncode": run.returncode,
        "stderr": run.stderr[-2000:],
        "ops_preview": ops[:10],
    }


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: score_sample.py <solver.py>")
    solver_path = Path(sys.argv[1]).resolve()
    sample_input = Path(__file__).with_name("sample_input.txt")
    result = score_solver(solver_path, sample_input)
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0 if result.get("valid") else 1


if __name__ == "__main__":
    raise SystemExit(main())

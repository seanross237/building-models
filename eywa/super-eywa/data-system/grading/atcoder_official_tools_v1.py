"""Helpers for running official AtCoder local tools in coding packets."""

from __future__ import annotations

import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from typing import Any


class AtCoderOfficialToolError(RuntimeError):
    """Raised when an official AtCoder tool cannot be built or executed."""


def find_cargo_bin() -> str:
    cargo = shutil.which("cargo")
    if cargo:
        return cargo
    candidate = Path.home() / ".cargo" / "bin" / "cargo"
    if candidate.exists():
        return str(candidate)
    raise AtCoderOfficialToolError(
        "cargo is not available. Install Rust or add ~/.cargo/bin to PATH."
    )


def cargo_env() -> dict[str, str]:
    env = dict(os.environ)
    cargo_bin_dir = str(Path(find_cargo_bin()).resolve().parent)
    existing = env.get("PATH", "")
    if cargo_bin_dir not in existing.split(":"):
        env["PATH"] = f"{cargo_bin_dir}:{existing}" if existing else cargo_bin_dir
    env.setdefault("RUST_BACKTRACE", "1")
    return env


def ensure_official_tool_binary(*, tool_dir: Path, bin_name: str) -> Path:
    tool_dir = tool_dir.resolve()
    bin_path = tool_dir / "target" / "release" / bin_name
    if bin_path.exists():
        return bin_path
    completed = subprocess.run(
        [find_cargo_bin(), "build", "--release", "--bin", bin_name],
        cwd=tool_dir,
        capture_output=True,
        text=True,
        timeout=600.0,
        env=cargo_env(),
    )
    if completed.returncode != 0:
        raise AtCoderOfficialToolError(
            f"failed to build official tool {bin_name}: "
            f"{completed.stderr.strip() or completed.stdout.strip() or 'unknown error'}"
        )
    if not bin_path.exists():
        raise AtCoderOfficialToolError(f"built {bin_name} but binary was not produced at {bin_path}")
    return bin_path


def run_atcoder_vis(
    *,
    tool_dir: Path,
    input_path: Path,
    output_path: Path,
    artifact_dir: Path,
    timeout_seconds: float,
) -> dict[str, Any]:
    artifact_dir.mkdir(parents=True, exist_ok=True)
    vis_bin = ensure_official_tool_binary(tool_dir=tool_dir, bin_name="vis")
    try:
        completed = subprocess.run(
            [str(vis_bin), str(input_path), str(output_path)],
            cwd=artifact_dir,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            env=cargo_env(),
        )
    except subprocess.TimeoutExpired as exc:
        return {
            "ok": False,
            "status": "timeout",
            "score": 0.0,
            "notes": "Official visualizer timed out.",
            "stdout": str(exc.stdout or ""),
            "stderr": str(exc.stderr or ""),
            "artifact_paths": _collect_visual_artifacts(tool_dir=tool_dir, artifact_dir=artifact_dir),
        }
    score = parse_atcoder_score(completed.stdout, completed.stderr)
    notes = ""
    status = "ok"
    ok = completed.returncode == 0 and score is not None
    invalid_output_note = _extract_invalid_candidate_output_note(completed.stdout, completed.stderr)
    if completed.returncode != 0:
        if _looks_like_invalid_candidate_output(completed.stdout, completed.stderr) or invalid_output_note:
            status = "candidate_output_invalid"
            ok = True
            notes = invalid_output_note or completed.stderr.strip() or completed.stdout.strip() or "Candidate output was invalid for the official visualizer."
        else:
            status = "tool_error"
            notes = completed.stderr.strip() or completed.stdout.strip() or "Official visualizer failed."
    elif invalid_output_note:
        status = "candidate_output_invalid"
        ok = True
        notes = invalid_output_note
    elif score is None:
        notes = "Official visualizer did not expose a parseable score."
    return {
        "ok": ok,
        "status": status,
        "score": float(score or 0.0),
        "notes": notes,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "artifact_paths": _collect_visual_artifacts(tool_dir=tool_dir, artifact_dir=artifact_dir),
    }


def run_atcoder_tester_and_vis(
    *,
    tool_dir: Path,
    input_path: Path,
    submission_path: Path,
    artifact_dir: Path,
    timeout_seconds: float,
) -> dict[str, Any]:
    artifact_dir.mkdir(parents=True, exist_ok=True)
    tester_bin = ensure_official_tool_binary(tool_dir=tool_dir, bin_name="tester")
    ensure_official_tool_binary(tool_dir=tool_dir, bin_name="vis")
    candidate_path = artifact_dir / submission_path.name
    shutil.copy2(submission_path, candidate_path)
    output_path = artifact_dir / "candidate.out"
    try:
        completed = subprocess.run(
            [str(tester_bin), sys.executable, str(candidate_path)],
            input=input_path.read_text(encoding="utf-8"),
            cwd=artifact_dir,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            env=cargo_env(),
        )
    except subprocess.TimeoutExpired as exc:
        output_path.write_text(str(exc.stdout or ""), encoding="utf-8")
        return {
            "ok": False,
            "status": "timeout",
            "score": 0.0,
            "notes": "Official tester timed out.",
            "stdout": str(exc.stdout or ""),
            "stderr": str(exc.stderr or ""),
            "candidate_output_path": str(output_path),
            "artifact_paths": [str(output_path)],
        }

    output_path.write_text(completed.stdout, encoding="utf-8")
    vis_payload = run_atcoder_vis(
        tool_dir=tool_dir,
        input_path=input_path,
        output_path=output_path,
        artifact_dir=artifact_dir,
        timeout_seconds=timeout_seconds,
    )
    score = parse_atcoder_score(completed.stderr, completed.stdout)
    if score is None:
        score = float(vis_payload.get("score") or 0.0)
    notes = completed.stderr.strip() or completed.stdout.strip()
    artifact_paths = [str(output_path)]
    artifact_paths.extend(list(vis_payload.get("artifact_paths") or []))
    return {
        "ok": completed.returncode == 0,
        "status": "ok" if completed.returncode == 0 else "tool_error",
        "score": float(score or 0.0),
        "notes": notes,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "candidate_output_path": str(output_path),
        "visualizer_payload": vis_payload,
        "artifact_paths": artifact_paths,
    }


def parse_atcoder_score(*texts: str | None) -> float | None:
    for raw in texts:
        text = str(raw or "")
        match = re.search(r"Score\s*=\s*(-?\d+(?:\.\d+)?)", text, flags=re.IGNORECASE)
        if match:
            return float(match.group(1))
        numeric_lines = [line.strip() for line in text.splitlines() if line.strip()]
        for line in reversed(numeric_lines):
            if re.fullmatch(r"-?\d+(?:\.\d+)?", line):
                return float(line)
    return None


def _collect_visual_artifacts(*, tool_dir: Path, artifact_dir: Path) -> list[str]:
    artifact_paths: list[str] = []
    for name in ("vis.html", "out.svg"):
        path = artifact_dir / name
        if path.exists():
            artifact_paths.append(str(path))
    template = tool_dir / "vis.html"
    svg_path = artifact_dir / "out.svg"
    if svg_path.exists() and template.exists() and not (artifact_dir / "vis.html").exists():
        shutil.copy2(template, artifact_dir / "vis.html")
        artifact_paths.append(str(artifact_dir / "vis.html"))
    return artifact_paths


def _looks_like_invalid_candidate_output(*texts: str | None) -> bool:
    haystack = "\n".join(str(text or "") for text in texts).lower()
    markers = (
        "parseinterror",
        "cannot parse",
        "failed to parse",
        "invalid digit",
        "index out of bounds",
        "called `option::unwrap()` on a `none` value",
        "assertion failed",
        "panicked at",
    )
    return any(marker in haystack for marker in markers)


def _extract_invalid_candidate_output_note(*texts: str | None) -> str:
    for raw in texts:
        lines = [line.strip() for line in str(raw or "").splitlines() if line.strip()]
        for line in lines:
            lowered = line.lower()
            if lowered.startswith("score"):
                continue
            if any(
                marker in lowered
                for marker in (
                    "out of range",
                    "too many outputs",
                    "too few outputs",
                    "parse",
                    "invalid",
                    "unexpected",
                    "error",
                )
            ):
                return line
    return ""

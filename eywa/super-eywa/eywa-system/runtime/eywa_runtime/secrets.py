"""Secret loading helpers."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess


def _load_env_file_value(key: str, dotenv_path: Path) -> str:
    if not dotenv_path.exists():
        return ""
    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        current_key, value = line.split("=", 1)
        if current_key.strip() != key:
            continue
        return value.strip().strip("'").strip('"')
    return ""


def load_openrouter_api_key() -> str:
    env_value = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if env_value:
        return env_value

    repo_root = Path(__file__).resolve().parents[3]
    for dotenv_path in (
        repo_root / ".env",
        repo_root.parent / "open-eywa" / ".env",
    ):
        dotenv_value = _load_env_file_value("OPENROUTER_API_KEY", dotenv_path)
        if dotenv_value:
            return dotenv_value

    user = os.environ.get("USER", "")
    if not user:
        return ""

    try:
        completed = subprocess.run(
            ["security", "find-generic-password", "-a", user, "-s", "OPENROUTER_API_KEY", "-w"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return ""

    return completed.stdout.strip()

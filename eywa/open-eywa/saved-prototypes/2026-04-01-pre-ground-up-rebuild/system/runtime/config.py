from __future__ import annotations

import os
import json
from pathlib import Path
from typing import Any


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def system_root() -> Path:
    return repo_root() / "system"


def load_config() -> dict[str, Any]:
    override = os.environ.get("OPEN_EYWA_CONFIG", "").strip()
    json_path = Path(override).expanduser().resolve() if override else system_root() / "configs" / "defaults.json"
    if json_path.exists():
        with json_path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    raise RuntimeError(f"Config file not found: {json_path}")


def openrouter_api_key() -> str:
    value = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not value:
        raise RuntimeError(
            "OPENROUTER_API_KEY is not set. Export it before running Open-Eywa missions."
        )
    return value


def role_model(role: str, config: dict[str, Any]) -> str:
    return config["roles"][role]


def role_tools(role: str, config: dict[str, Any]) -> list[str]:
    assignment = config["tool_assignment"][role]
    return list(config["tool_profiles"][assignment]["tools"])

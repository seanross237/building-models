"""ID helpers."""

from __future__ import annotations

from datetime import datetime, timezone


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def make_run_id() -> str:
    now = datetime.now(timezone.utc)
    return now.strftime("run_%Y_%m_%d_%H%M%S")


def make_root_node_id() -> str:
    return "node_root"


def make_helper_node_id(parent_node_id: str, index: int) -> str:
    return f"{parent_node_id}_helper_{index:02d}"

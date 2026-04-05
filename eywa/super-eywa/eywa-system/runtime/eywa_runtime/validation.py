"""Validation helpers for stored v1 runs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

from .contracts import (
    ContractError,
    validate_node_packet,
    validate_node_record,
    validate_run_packet,
)


class RunValidationError(ValueError):
    """Raised when a stored run does not satisfy the expected v1 layout."""


def validate_run_directory(run_dir: Path) -> Dict[str, object]:
    if not run_dir.exists():
        raise RunValidationError(f"run directory does not exist: {run_dir}")

    required_paths = [
        run_dir / "run_packet.json",
        run_dir / "run_summary.json",
        run_dir / "events" / "run-events.jsonl",
        run_dir / "derived" / "timeline.json",
        run_dir / "derived" / "timeline.md",
        run_dir / "derived" / "simple-run-row.json",
        run_dir / "nodes",
        run_dir / "replay",
    ]
    for path in required_paths:
        if not path.exists():
            raise RunValidationError(f"missing required path: {path}")

    run_packet = json.loads((run_dir / "run_packet.json").read_text(encoding="utf-8"))
    validate_run_packet(run_packet)

    node_dirs = sorted(path for path in (run_dir / "nodes").iterdir() if path.is_dir())
    if not node_dirs:
        raise RunValidationError("run has no node directories")

    node_count = 0
    for node_dir in node_dirs:
        packet_path = node_dir / "node_packet.json"
        record_path = node_dir / "node_record.json"
        events_path = node_dir / "events.jsonl"
        edges_path = node_dir / "edges.json"
        for path in [packet_path, record_path, events_path, edges_path]:
            if not path.exists():
                raise RunValidationError(f"missing required node path: {path}")

        node_packet = json.loads(packet_path.read_text(encoding="utf-8"))
        node_record = json.loads(record_path.read_text(encoding="utf-8"))
        try:
            validate_node_packet(node_packet)
            validate_node_record(node_record)
        except ContractError as exc:
            raise RunValidationError(str(exc)) from exc

        replay_ref = node_record["replay_ref"]
        replay_dir = run_dir / replay_ref
        if not replay_dir.exists():
            raise RunValidationError(f"missing replay directory for node {node_dir.name}: {replay_dir}")
        for replay_path in [
            replay_dir / "raw-model.json",
            replay_dir / "prompt-snapshot.json",
            replay_dir / "tool-transcript.jsonl",
        ]:
            if not replay_path.exists():
                raise RunValidationError(f"missing replay artifact: {replay_path}")

        node_count += 1

    run_summary = json.loads((run_dir / "run_summary.json").read_text(encoding="utf-8"))
    if run_summary["node_count"] != node_count:
        raise RunValidationError(
            f"run_summary node_count {run_summary['node_count']} does not match actual node count {node_count}"
        )

    return {
        "run_id": run_summary["run_id"],
        "node_count": node_count,
        "root_node_id": run_summary["root_node_id"],
        "status": run_summary["status"],
    }

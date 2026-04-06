"""Validation helpers for stored v1 runs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

from .contracts import (
    ContractError,
    validate_final_output,
    validate_node_authored_response,
    validate_node_output,
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
        run_dir / "final-output.json",
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
    final_output = json.loads((run_dir / "final-output.json").read_text(encoding="utf-8"))
    try:
        validate_final_output(final_output)
    except ContractError as exc:
        raise RunValidationError(str(exc)) from exc

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

        raw_model = json.loads((replay_dir / "raw-model.json").read_text(encoding="utf-8"))
        if not isinstance(raw_model.get("steps"), list) or not raw_model["steps"]:
            raise RunValidationError(f"raw-model.json missing non-empty steps list for node {node_dir.name}")
        for step in raw_model["steps"]:
            if not isinstance(step, dict):
                raise RunValidationError(f"raw-model.json step must be an object for node {node_dir.name}")
            authored_response = step.get("authored_response")
            output = step.get("output")
            if not isinstance(authored_response, dict):
                raise RunValidationError(
                    f"raw-model.json step missing authored_response object for node {node_dir.name}"
                )
            if not isinstance(output, dict):
                raise RunValidationError(f"raw-model.json step missing output object for node {node_dir.name}")
            try:
                validate_node_authored_response(authored_response)
                validate_node_output(output)
            except ContractError as exc:
                raise RunValidationError(str(exc)) from exc

        prompt_snapshot = json.loads((replay_dir / "prompt-snapshot.json").read_text(encoding="utf-8"))
        for key in ["initial_prompt", "final_prompt", "turns"]:
            if key not in prompt_snapshot:
                raise RunValidationError(f"prompt-snapshot.json missing key {key} for node {node_dir.name}")
        if not isinstance(prompt_snapshot["turns"], list) or not prompt_snapshot["turns"]:
            raise RunValidationError(f"prompt-snapshot.json turns must be a non-empty list for node {node_dir.name}")
        for turn in prompt_snapshot["turns"]:
            if not isinstance(turn, dict):
                raise RunValidationError(f"prompt snapshot turn must be an object for node {node_dir.name}")
            if "turn_index" not in turn or "snapshot_text" not in turn:
                raise RunValidationError(
                    f"prompt snapshot turn missing turn_index or snapshot_text for node {node_dir.name}"
                )

        node_count += 1

    run_summary = json.loads((run_dir / "run_summary.json").read_text(encoding="utf-8"))
    if run_summary["node_count"] != node_count:
        raise RunValidationError(
            f"run_summary node_count {run_summary['node_count']} does not match actual node count {node_count}"
        )
    final_result_refs = run_summary.get("final_result_refs") or []
    if not isinstance(final_result_refs, list) or not final_result_refs:
        raise RunValidationError("run_summary final_result_refs must be a non-empty list")
    for ref in final_result_refs:
        resolved = run_dir / str(ref)
        if not resolved.exists():
            raise RunValidationError(f"run_summary final_result_ref does not exist: {ref}")

    return {
        "run_id": run_summary["run_id"],
        "node_count": node_count,
        "root_node_id": run_summary["root_node_id"],
        "status": run_summary["status"],
    }

"""Minimal Super-Eywa v1 engine."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from time import perf_counter
from typing import Any, Dict, List, Optional

from .contracts import (
    validate_node_packet,
    validate_node_record,
    validate_run_packet,
)
from .defaults import DEFAULT_RUN_LEVEL_VARIABLES
from .executor import ExecutionStep, build_executor
from .ids import make_helper_node_id, make_root_node_id, make_run_id, utc_now_iso
from .prompting import render_prompt_text
from .storage import relative_ref, write_json, write_jsonl
from .story import build_timeline, timeline_markdown


@dataclass
class RunResult:
    run_id: str
    run_dir: Path
    root_node_id: str
    node_count: int
    timeline_path: Path
    summary_path: Path


class EywaEngine:
    """A minimal file-first engine aligned to the v1 contracts."""

    HARD_MAX_DEPTH = 3

    def __init__(self, run_history_root: Path) -> None:
        self.run_history_root = run_history_root
        self.events: List[Dict[str, Any]] = []

    def run(
        self,
        *,
        task_text: str,
        run_id: Optional[str] = None,
        run_level_variables: Optional[Dict[str, Any]] = None,
        task_source: str = "manual_cli",
    ) -> RunResult:
        self.events = []
        run_id = run_id or make_run_id()
        run_dir = self.run_history_root / run_id
        nodes_dir = run_dir / "nodes"
        events_dir = run_dir / "events"
        replay_dir = run_dir / "replay"
        derived_dir = run_dir / "derived"

        root_node_id = make_root_node_id()
        merged_run_variables = dict(DEFAULT_RUN_LEVEL_VARIABLES)
        if run_level_variables:
            merged_run_variables.update(run_level_variables)
        merged_run_variables["budget_policy"] = self._resolved_budget_policy(
            merged_run_variables.get("budget_policy") or {}
        )
        executor = build_executor(merged_run_variables)

        run_packet = {
            "contract_name": "run_packet",
            "contract_version": "v1",
            "run_id": run_id,
            "created_at_utc": utc_now_iso(),
            "root_node_id": root_node_id,
            "task": {
                "raw_task_text": task_text,
                "task_source": task_source,
                "constraints": [],
                "success_criteria": [],
                "attachment_refs": [],
            },
            "run_level_variables": merged_run_variables,
            "top_level_context": {
                "context_refs": [],
            },
            "root_setup": {
                "root_input_summary": task_text,
                "notes": [],
            },
        }
        validate_run_packet(run_packet)
        write_json(run_dir / "run_packet.json", run_packet)

        self._event(run_id, root_node_id, "run_started", f"Run started for task: {task_text}")
        node_count = self._execute_node(
            run_id=run_id,
            run_dir=run_dir,
            nodes_dir=nodes_dir,
            replay_dir=replay_dir,
            executor=executor,
            node_id=root_node_id,
            creation_parent_node_id=None,
            created_by_action_type=None,
            instructions=task_text,
            run_level_variables=merged_run_variables,
            node_level_overrides={},
            depth=0,
        )

        write_jsonl(events_dir / "run-events.jsonl", self.events)

        timeline = build_timeline(self.events)
        total_tokens = 0
        total_cost = 0.0
        total_wall_time = 0
        for node_dir in sorted(nodes_dir.iterdir()):
            node_record = json.loads((node_dir / "node_record.json").read_text(encoding="utf-8"))
            metrics = node_record["logging"]["metrics"]
            total_tokens += metrics["total_tokens"]
            total_cost += metrics["cost_usd"]
            total_wall_time += metrics["wall_time_ms"]

        run_summary = {
            "run_id": run_id,
            "root_node_id": root_node_id,
            "status": "completed",
            "node_count": node_count,
            "final_result_refs": [
                relative_ref(nodes_dir / root_node_id / "node_record.json", run_dir)
            ],
            "total_tokens": total_tokens,
            "total_cost_usd": round(total_cost, 6),
            "total_wall_time_ms": total_wall_time,
        }
        write_json(run_dir / "run_summary.json", run_summary)
        write_json(
            derived_dir / "simple-run-row.json",
            {
                "run_id": run_id,
                "task": task_text,
                "variables_json": merged_run_variables,
                "scores_json": {
                    "status": "ungraded",
                    "score": None,
                },
            },
        )
        self._event(run_id, root_node_id, "run_completed", f"Run completed with {node_count} node(s)")
        timeline = build_timeline(self.events)
        write_json(derived_dir / "timeline.json", {"timeline": timeline})
        (derived_dir / "timeline.md").write_text(timeline_markdown(timeline), encoding="utf-8")
        write_jsonl(events_dir / "run-events.jsonl", self.events)

        return RunResult(
            run_id=run_id,
            run_dir=run_dir,
            root_node_id=root_node_id,
            node_count=node_count,
            timeline_path=derived_dir / "timeline.md",
            summary_path=run_dir / "run_summary.json",
        )

    def _execute_node(
        self,
        *,
        run_id: str,
        run_dir: Path,
        nodes_dir: Path,
        replay_dir: Path,
        executor: Any,
        node_id: str,
        creation_parent_node_id: Optional[str],
        created_by_action_type: Optional[str],
        instructions: str,
        run_level_variables: Dict[str, Any],
        node_level_overrides: Dict[str, Any],
        depth: int,
    ) -> int:
        resolved_variables = dict(run_level_variables)
        resolved_variables.update(node_level_overrides)
        resolved_variables["budget_policy"] = self._resolved_budget_policy(
            resolved_variables.get("budget_policy") or {}
        )
        node_packet = {
            "contract_name": "node_packet",
            "contract_version": "v1",
            "run_id": run_id,
            "node_id": node_id,
            "created_at_utc": utc_now_iso(),
            "creation_parent_node_id": creation_parent_node_id,
            "input": {
                "instructions": instructions,
                "provided_context_refs": [],
                "attachment_refs": [],
            },
            "variable_resolution": {
                "run_level_defaults": run_level_variables,
                "node_level_overrides": node_level_overrides,
                "resolved_variables": resolved_variables,
            },
            "node_setup": {
                "created_by_action_type": created_by_action_type,
                "notes": [],
            },
        }
        validate_node_packet(node_packet)

        node_dir = nodes_dir / node_id
        write_json(node_dir / "node_packet.json", node_packet)
        node_events: List[Dict[str, Any]] = []
        node_edges: List[Dict[str, Any]] = []
        replay_steps: List[Dict[str, Any]] = []
        child_summaries: List[Dict[str, str]] = []

        prompt_text = render_prompt_text(node_packet)
        node_events.append({"event_type": "node_started", "node_id": node_id, "message": f"Node started: {instructions}"})
        self._event(run_id, node_id, "node_started", f"Node started: {instructions}")

        budget_policy = resolved_variables.get("budget_policy", {})
        max_depth = int(budget_policy.get("max_depth", 1))
        max_helpers = int(budget_policy.get("max_helpers_per_node", 3))
        subtasks = executor.split_instructions(instructions, max_helpers)
        node_started_at = perf_counter()

        total_child_count = 0
        if depth < max_depth and subtasks:
            helper_node_ids = [make_helper_node_id(node_id, index + 1) for index in range(len(subtasks))]
            recruit_step = executor.recruit_help(
                run_id=run_id,
                node_id=node_id,
                helper_node_ids=helper_node_ids,
                subtasks=subtasks,
            )
            replay_steps.append(self._replay_step(1, recruit_step))
            node_events.append(
                {
                    "event_type": "node_recruited_help",
                    "node_id": node_id,
                    "message": f"Node recruited {len(subtasks)} helper(s)",
                }
            )
            self._event(run_id, node_id, "node_recruited_help", f"Node recruited {len(subtasks)} helper(s)")

            for helper_node_id, subtask in zip(helper_node_ids, subtasks):
                node_edges.append(
                    {"edge_type": "created_by", "from_node_id": node_id, "to_node_id": helper_node_id}
                )
                node_edges.append(
                    {"edge_type": "sends_output_to", "from_node_id": helper_node_id, "to_node_id": node_id}
                )
                node_edges.append(
                    {"edge_type": "depends_on", "from_node_id": node_id, "to_node_id": helper_node_id}
                )
                child_count = self._execute_node(
                    run_id=run_id,
                    run_dir=run_dir,
                    nodes_dir=nodes_dir,
                    replay_dir=replay_dir,
                    executor=executor,
                    node_id=helper_node_id,
                    creation_parent_node_id=node_id,
                    created_by_action_type="recruit_help",
                    instructions=subtask,
                    run_level_variables=run_level_variables,
                    node_level_overrides={},
                    depth=depth + 1,
                )
                total_child_count += child_count
                child_record = json.loads((nodes_dir / helper_node_id / "node_record.json").read_text(encoding="utf-8"))
                child_summary = child_record["results"][0]["content"]
                child_summaries.append({"node_id": helper_node_id, "summary": child_summary})
            final_prompt_text = render_prompt_text(node_packet, child_summaries)
            final_step = executor.report_success(
                run_id=run_id,
                node_id=node_id,
                creation_parent_node_id=creation_parent_node_id,
                instructions=instructions,
                child_summaries=child_summaries,
            )
            replay_steps.append(self._replay_step(2, final_step))
            final_output = final_step.output
        elif "impossible" in instructions.lower() or "unachievable" in instructions.lower():
            final_prompt_text = prompt_text
            final_step = executor.report_problem(
                run_id=run_id,
                node_id=node_id,
                creation_parent_node_id=creation_parent_node_id,
                message=f"Runtime marked this task as a problem case: {instructions}",
            )
            replay_steps.append(self._replay_step(1, final_step))
            final_output = final_step.output
        else:
            final_prompt_text = prompt_text
            final_step = executor.report_success(
                run_id=run_id,
                node_id=node_id,
                creation_parent_node_id=creation_parent_node_id,
                instructions=instructions,
                child_summaries=None,
            )
            replay_steps.append(self._replay_step(1, final_step))
            final_output = final_step.output

        node_events.append(
            {
                "event_type": "node_completed",
                "node_id": node_id,
                "message": f"Node completed with action {final_output['action_type']}",
            }
        )
        self._event(run_id, node_id, "node_completed", f"Node completed with action {final_output['action_type']}")

        write_jsonl(node_dir / "events.jsonl", node_events)
        write_json(node_dir / "edges.json", {"edges": node_edges})

        replay_node_dir = replay_dir / node_id
        write_json(
            replay_node_dir / "raw-model.json",
            {
                "provider": getattr(executor, "provider_name", "unknown"),
                "note": "Per-step provider payloads and usage are recorded here.",
                "steps": replay_steps,
            },
        )
        write_json(
            replay_node_dir / "prompt-snapshot.json",
            {
                "initial_prompt": prompt_text,
                "final_prompt": final_prompt_text,
            },
        )
        write_jsonl(replay_node_dir / "tool-transcript.jsonl", [])

        usage = self._aggregate_usage(replay_steps)
        wall_time_ms = int((perf_counter() - node_started_at) * 1000)
        metrics = {
            "input_tokens": int(usage.get("prompt_tokens", 0) or self._rough_token_count(prompt_text)),
            "output_tokens": int(usage.get("completion_tokens", 0) or self._rough_token_count(final_output["results"][0]["content"])),
            "total_tokens": int(usage.get("total_tokens", 0) or (self._rough_token_count(prompt_text) + self._rough_token_count(final_output["results"][0]["content"]))),
            "cost_usd": round(float(usage.get("cost_usd", 0.0) or 0.0), 8),
            "wall_time_ms": wall_time_ms,
            "provider_details": usage.get("provider_details", {}),
            "reasoning_tokens": int(usage.get("reasoning_tokens", 0) or 0),
            "cached_prompt_tokens": int(usage.get("cached_prompt_tokens", 0) or 0),
        }
        node_record = {
            "contract_name": "node_record",
            "contract_version": "v1",
            "run_id": run_id,
            "node_id": node_id,
            "state": "completed",
            "input": node_packet["input"],
            "variables": resolved_variables,
            "prompt": {
                "rendered_prompt_text": final_prompt_text,
                "prompt_artifact_refs": [],
            },
            "results": final_output["results"],
            "logging": {
                "metrics": metrics,
                "events_ref": "events.jsonl",
                "edges_ref": "edges.json",
            },
            "replay_ref": relative_ref(replay_node_dir, run_dir),
            "final_action_type": final_output["action_type"],
        }
        validate_node_record(node_record)
        write_json(node_dir / "node_record.json", node_record)
        return 1 + total_child_count

    def _event(self, run_id: str, node_id: str, event_type: str, message: str) -> None:
        self.events.append(
            {
                "run_id": run_id,
                "node_id": node_id,
                "event_type": event_type,
                "message": message,
                "timestamp_utc": utc_now_iso(),
            }
        )

    @staticmethod
    def _rough_token_count(text: str) -> int:
        return max(1, len(text.split()))

    def _resolved_budget_policy(self, budget_policy: Dict[str, Any]) -> Dict[str, Any]:
        resolved = dict(budget_policy)
        requested_depth = int(resolved.get("max_depth", DEFAULT_RUN_LEVEL_VARIABLES["budget_policy"]["max_depth"]))
        resolved["max_depth"] = min(requested_depth, self.HARD_MAX_DEPTH)
        resolved["max_helpers_per_node"] = int(
            resolved.get(
                "max_helpers_per_node",
                DEFAULT_RUN_LEVEL_VARIABLES["budget_policy"]["max_helpers_per_node"],
            )
        )
        return resolved

    @staticmethod
    def _replay_step(step_index: int, step: ExecutionStep) -> Dict[str, Any]:
        return {
            "step": step_index,
            "note": step.note,
            "output": step.output,
            "provider_payload": step.provider_payload,
            "usage": step.usage,
        }

    @staticmethod
    def _aggregate_usage(replay_steps: List[Dict[str, Any]]) -> Dict[str, Any]:
        totals: Dict[str, Any] = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "reasoning_tokens": 0,
            "cached_prompt_tokens": 0,
            "total_tokens": 0,
            "cost_usd": 0.0,
            "provider_details": {"responses": []},
        }
        for step in replay_steps:
            usage = dict(step.get("usage") or {})
            totals["prompt_tokens"] += int(usage.get("prompt_tokens", 0) or 0)
            totals["completion_tokens"] += int(usage.get("completion_tokens", 0) or 0)
            totals["reasoning_tokens"] += int(usage.get("reasoning_tokens", 0) or 0)
            totals["cached_prompt_tokens"] += int(usage.get("cached_prompt_tokens", 0) or 0)
            totals["total_tokens"] += int(usage.get("total_tokens", 0) or 0)
            totals["cost_usd"] += float(usage.get("cost_usd", 0.0) or 0.0)
            responses = (usage.get("provider_details") or {}).get("responses", [])
            totals["provider_details"]["responses"].extend(responses)
        return totals

"""Minimal Super-Eywa v1 engine."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from time import perf_counter
from typing import Any, Dict, List, Optional

from .contracts import (
    validate_node_output,
    validate_node_packet,
    validate_node_record,
    validate_run_packet,
)
from .defaults import DEFAULT_RUN_LEVEL_VARIABLES
from .executor import ExecutionStep, build_executor
from .ids import make_helper_node_id, make_root_node_id, make_run_id, utc_now_iso
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
    HARD_MAX_TURNS_PER_NODE = 6

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
            node_id=root_node_id,
            creation_parent_node_id=None,
            created_by_action_type=None,
            instructions=task_text,
            run_level_variables=merged_run_variables,
            node_level_overrides={},
            depth=0,
        )

        write_jsonl(events_dir / "run-events.jsonl", self.events)

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
        executor = build_executor(resolved_variables)
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
        prompt_turns: List[str] = []

        node_events.append({"event_type": "node_started", "node_id": node_id, "message": f"Node started: {instructions}"})
        self._event(run_id, node_id, "node_started", f"Node started: {instructions}")

        budget_policy = resolved_variables.get("budget_policy", {})
        max_depth = int(budget_policy.get("max_depth", 1))
        max_helpers = int(budget_policy.get("max_helpers_per_node", 3))
        max_turns = int(budget_policy.get("max_turns_per_node", 4))
        workflow_structure = str(resolved_variables.get("workflow_structure", "sequential_parent_review"))
        node_started_at = perf_counter()

        total_child_count = 0
        helper_counter = 0
        turn_index = 0
        final_output: Dict[str, Any] | None = None
        final_turn: ExecutionStep | None = None
        final_prompt_text = ""
        initial_turn: ExecutionStep | None = None
        synthesis_brief = ""

        while turn_index < max_turns:
            turn_index += 1
            allowed_decisions = self._allowed_decisions(
                depth=depth,
                max_depth=max_depth,
                max_helpers=max_helpers,
                turn_index=turn_index,
                max_turns=max_turns,
                workflow_structure=workflow_structure,
                child_review=bool(child_summaries),
            )
            turn = executor.author_node_response(
                node_packet=node_packet,
                depth=depth,
                turn_index=turn_index,
                allowed_decisions=allowed_decisions,
                child_summaries=child_summaries or None,
                synthesis_brief=synthesis_brief or None,
            )
            if initial_turn is None:
                initial_turn = turn
            prompt_turns.append(turn.prompt_snapshot)
            final_prompt_text = turn.prompt_snapshot

            helper_specs = list(turn.authored_response.get("helpers", []))
            helper_node_ids: List[str] | None = None
            if turn.authored_response["orchestration_decision"] == "delegate":
                helper_node_ids = [
                    make_helper_node_id(node_id, helper_counter + index + 1)
                    for index in range(len(helper_specs))
                ]

            output = self._materialize_node_output(
                run_id=run_id,
                node_id=node_id,
                creation_parent_node_id=creation_parent_node_id,
                authored_response=turn.authored_response,
                helper_node_ids=helper_node_ids,
            )
            replay_steps.append(self._replay_step(turn_index, turn, output))

            if turn.authored_response["orchestration_decision"] != "delegate":
                final_output = output
                final_turn = turn
                break

            node_events.append(
                {
                    "event_type": "node_recruited_help",
                    "node_id": node_id,
                    "message": f"Node recruited {len(helper_specs)} helper(s)",
                }
            )
            self._event(run_id, node_id, "node_recruited_help", f"Node recruited {len(helper_specs)} helper(s)")

            synthesis_brief = str(turn.authored_response.get("synthesis_brief", ""))
            helper_counter += len(helper_specs)

            new_child_summaries: List[Dict[str, str]] = []
            for helper_node_id, helper_spec in zip(helper_node_ids or [], helper_specs):
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
                    node_id=helper_node_id,
                    creation_parent_node_id=node_id,
                    created_by_action_type="recruit_help",
                    instructions=str(helper_spec["instructions"]),
                    run_level_variables=run_level_variables,
                    node_level_overrides=dict(helper_spec.get("variable_overrides") or {}),
                    depth=depth + 1,
                )
                total_child_count += child_count
                child_record = json.loads((nodes_dir / helper_node_id / "node_record.json").read_text(encoding="utf-8"))
                child_summary = child_record["results"][0]["content"] if child_record["results"] else ""
                new_child_summaries.append({"node_id": helper_node_id, "summary": child_summary})
            child_summaries.extend(new_child_summaries)

        if final_output is None:
            fallback_turn = ExecutionStep(
                authored_response={
                    "schema_name": "eywa_node_response",
                    "schema_version": "v1",
                    "orchestration_decision": "report_problem",
                    "decision_notes": "Runtime stopped the node after it exhausted max_turns_per_node.",
                    "response": f"Node exhausted max_turns_per_node={max_turns} without reaching a terminal decision.",
                },
                note="runtime stopped node after max turns were exhausted",
                prompt_snapshot=final_prompt_text,
                provider_payload={
                    "provider": getattr(executor, "provider_name", "unknown"),
                    "runtime_generated": True,
                },
                usage=getattr(executor, "_zero_usage", lambda: {"provider_details": {"responses": []}})(),
            )
            prompt_turns.append(fallback_turn.prompt_snapshot)
            final_turn = fallback_turn
            final_output = self._materialize_node_output(
                run_id=run_id,
                node_id=node_id,
                creation_parent_node_id=creation_parent_node_id,
                authored_response=fallback_turn.authored_response,
                helper_node_ids=None,
            )
            replay_steps.append(self._replay_step(turn_index + 1, fallback_turn, final_output))

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
                "note": "Per-turn provider payloads, authored JSON, and compiled outputs are recorded here.",
                "steps": replay_steps,
            },
        )
        turn_dicts = [
            {
                "turn_index": index + 1,
                "snapshot_text": prompt_snapshot,
            }
            for index, prompt_snapshot in enumerate(prompt_turns)
        ]
        write_json(
            replay_node_dir / "prompt-snapshot.json",
            {
                "initial_prompt": prompt_turns[0] if prompt_turns else "",
                "final_prompt": prompt_turns[-1] if prompt_turns else "",
                "turns": turn_dicts,
            },
        )
        write_jsonl(replay_node_dir / "tool-transcript.jsonl", [])

        usage = self._aggregate_usage(replay_steps)
        prompt_text = "\n\n".join(prompt_turns)
        wall_time_ms = int((perf_counter() - node_started_at) * 1000)
        final_result_text = final_output["results"][0]["content"] if final_output["results"] else ""
        metrics = {
            "input_tokens": int(usage.get("prompt_tokens", 0) or self._rough_token_count(prompt_text)),
            "output_tokens": int(usage.get("completion_tokens", 0) or self._rough_token_count(final_result_text)),
            "total_tokens": int(
                usage.get("total_tokens", 0)
                or (self._rough_token_count(prompt_text) + self._rough_token_count(final_result_text))
            ),
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
            "orchestration": self._build_orchestration_summary(
                initial_turn=initial_turn or final_turn,
                final_turn=final_turn,
                turn_count=len(prompt_turns),
                helper_count=helper_counter,
            ),
            "prompt": {
                "rendered_prompt_text": prompt_turns[-1] if prompt_turns else "",
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

    def _materialize_node_output(
        self,
        *,
        run_id: str,
        node_id: str,
        creation_parent_node_id: Optional[str],
        authored_response: Dict[str, Any],
        helper_node_ids: List[str] | None,
    ) -> Dict[str, Any]:
        decision = authored_response["orchestration_decision"]

        if decision == "delegate":
            helper_specs = list(authored_response.get("helpers", []))
            if helper_node_ids is None:
                raise ValueError("helper_node_ids must be provided for delegate outputs")
            packets = []
            plan_lines = []
            if authored_response.get("decision_notes"):
                plan_lines.append(str(authored_response["decision_notes"]))
            for helper_node_id, helper_spec in zip(helper_node_ids, helper_specs):
                packets.append(
                    {
                        "message_type": "helper_assignment",
                        "target": {
                            "target_type": "new_helper",
                            "target_ref": helper_node_id,
                        },
                        "message": helper_spec["instructions"],
                        "attachment_refs": [],
                    }
                )
                plan_lines.append(f"{helper_node_id} ({helper_spec['label']}): {helper_spec['instructions']}")
            payload = {
                "contract_name": "node_output",
                "contract_version": "v1",
                "run_id": run_id,
                "node_id": node_id,
                "action_type": "recruit_help",
                "results": [
                    {
                        "result_type": "plan",
                        "content": "\n".join(plan_lines) if plan_lines else f"Delegated to {len(helper_specs)} helper(s).",
                        "attachment_refs": [],
                    }
                ],
                "outgoing_packets": packets,
            }
            validate_node_output(payload)
            return payload

        if decision == "report_problem":
            message = authored_response["response"]
            packets = []
            if creation_parent_node_id is not None:
                packets.append(
                    {
                        "message_type": "problem_report",
                        "target": {
                            "target_type": "creating_parent",
                            "target_ref": creation_parent_node_id,
                        },
                        "message": message,
                        "attachment_refs": [],
                    }
                )
            payload = {
                "contract_name": "node_output",
                "contract_version": "v1",
                "run_id": run_id,
                "node_id": node_id,
                "action_type": "report_problem",
                "results": [
                    {
                        "result_type": "failure_explanation",
                        "content": message,
                        "attachment_refs": [],
                    }
                ],
                "outgoing_packets": packets,
            }
            validate_node_output(payload)
            return payload

        response = authored_response["response"]
        packets = []
        if creation_parent_node_id is not None:
            packets.append(
                {
                    "message_type": "success_report",
                    "target": {
                        "target_type": "creating_parent",
                        "target_ref": creation_parent_node_id,
                    },
                    "message": response,
                    "attachment_refs": [],
                }
            )
        payload = {
            "contract_name": "node_output",
            "contract_version": "v1",
            "run_id": run_id,
            "node_id": node_id,
            "action_type": "report_success",
            "results": [
                {
                    "result_type": str(authored_response.get("result_type") or "summary"),
                    "content": response,
                    "attachment_refs": [],
                }
            ],
            "outgoing_packets": packets,
        }
        validate_node_output(payload)
        return payload

    def _allowed_decisions(
        self,
        *,
        depth: int,
        max_depth: int,
        max_helpers: int,
        turn_index: int,
        max_turns: int,
        workflow_structure: str,
        child_review: bool,
    ) -> List[str]:
        allowed = ["execute_locally", "report_problem"]
        can_delegate = depth < max_depth and max_helpers > 0 and turn_index < max_turns
        if workflow_structure == "single_delegation_then_synthesize" and child_review:
            can_delegate = False
        if can_delegate:
            allowed.insert(1, "delegate")
        return allowed

    def _build_orchestration_summary(
        self,
        *,
        initial_turn: ExecutionStep | None,
        final_turn: ExecutionStep | None,
        turn_count: int,
        helper_count: int,
    ) -> Dict[str, Any]:
        initial_response = initial_turn.authored_response if initial_turn else {}
        final_response = final_turn.authored_response if final_turn else {}
        return {
            "turn_count": turn_count,
            "initial_decision": initial_response.get("orchestration_decision"),
            "final_decision": final_response.get("orchestration_decision"),
            "decision_notes": str(final_response.get("decision_notes", "")),
            "helper_count": helper_count,
        }

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
        requested_turns = int(
            resolved.get(
                "max_turns_per_node",
                DEFAULT_RUN_LEVEL_VARIABLES["budget_policy"].get("max_turns_per_node", 4),
            )
        )
        resolved["max_turns_per_node"] = min(requested_turns, self.HARD_MAX_TURNS_PER_NODE)
        return resolved

    @staticmethod
    def _replay_step(step_index: int, turn: ExecutionStep, output: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "step": step_index,
            "note": turn.note,
            "prompt_snapshot": turn.prompt_snapshot,
            "authored_response": turn.authored_response,
            "output": output,
            "provider_payload": turn.provider_payload,
            "usage": turn.usage,
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

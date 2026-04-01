from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

from .node_contract import NodeLayout, read_trimmed_text, write_text


@dataclass(frozen=True)
class PreparedNodeContextResult:
    packet_path: str
    included_sections: tuple[str, ...]


def prepare_node_context_packet(
    layout: NodeLayout,
    *,
    run_id: str,
    role: str,
) -> PreparedNodeContextResult:
    packet_path = layout.run_prepared_node_context_file(run_id)
    packet = {
        "role": role,
        "node": {
            "path": str(layout.root),
            "status": read_trimmed_text(layout.status_file),
            "agent_mode": read_trimmed_text(layout.agent_mode_file),
        },
        "task_source": _task_source_section(layout),
        "focus_sections": _focus_sections_for_role(role),
        "available_sections": _available_sections(layout),
        "progression": _progression_section(layout),
        "children": _child_summaries(layout),
    }
    write_text(packet_path, json.dumps(packet, indent=2, sort_keys=True) + "\n")
    return PreparedNodeContextResult(
        packet_path=str(packet_path),
        included_sections=tuple(packet["available_sections"].keys()),
    )


def _task_source_section(layout: NodeLayout) -> dict[str, Any]:
    if layout.goal_file.exists():
        path = layout.goal_file
        task_source_name = "goal"
    else:
        path = layout.parent_instructions_file
        task_source_name = "parent-instructions"
    return {
        "task_source_name": task_source_name,
        "path": str(path.relative_to(layout.root)),
        "text": path.read_text(encoding="utf-8"),
    }


def _available_sections(layout: NodeLayout) -> dict[str, Any]:
    sections: dict[str, Any] = {}
    maybe_add_text_section(sections, layout, "retrieved_knowledge", layout.retrieved_knowledge_file)
    maybe_add_text_section(sections, layout, "plan", layout.plan_file)
    maybe_add_text_section(sections, layout, "review", layout.review_file)
    maybe_add_text_section(sections, layout, "state", layout.state_file)
    maybe_add_text_section(sections, layout, "final_output", layout.final_output_file)
    maybe_add_text_section(sections, layout, "escalation", layout.escalation_file)
    if layout.latest_child_node_report_file.exists():
        sections["latest_child_report"] = {
            "path": str(layout.latest_child_node_report_file.relative_to(layout.root)),
            "json": json.loads(layout.latest_child_node_report_file.read_text(encoding="utf-8")),
        }
    if layout.progression_state_file.exists():
        sections["progression_state"] = {
            "path": str(layout.progression_state_file.relative_to(layout.root)),
            "json": json.loads(layout.progression_state_file.read_text(encoding="utf-8")),
        }
    return sections


def maybe_add_text_section(
    sections: dict[str, Any],
    layout: NodeLayout,
    section_name: str,
    path: Path,
) -> None:
    if not path.exists():
        return
    sections[section_name] = {
        "path": str(path.relative_to(layout.root)),
        "text": path.read_text(encoding="utf-8"),
    }


def _progression_section(layout: NodeLayout) -> dict[str, Any]:
    return {
        "next_action_after_child_report": read_trimmed_text(
            layout.next_action_after_child_report_file
        ),
        "terminal_outcome": read_trimmed_text(layout.terminal_outcome_file),
        "failure_reason": read_trimmed_text(layout.failure_reason_file),
        "cancellation_reason": read_trimmed_text(layout.cancellation_reason_file),
        "waiting_on_computation_note": read_trimmed_text(layout.waiting_marker_file),
    }


def _child_summaries(layout: NodeLayout) -> list[dict[str, Any]]:
    summaries: list[dict[str, Any]] = []
    if not layout.children_dir.exists():
        return summaries
    for child_root in sorted(path for path in layout.children_dir.iterdir() if path.is_dir()):
        child_layout = NodeLayout(child_root)
        summary = {
            "child_name": child_root.name,
            "path": str(child_root.relative_to(layout.root)),
            "status": read_trimmed_text(child_layout.status_file),
            "terminal_outcome": read_trimmed_text(child_layout.terminal_outcome_file),
            "failure_reason": read_trimmed_text(child_layout.failure_reason_file),
            "has_final_output": child_layout.final_output_file.exists(),
            "has_escalation": child_layout.escalation_file.exists(),
        }
        if child_layout.final_output_file.exists():
            summary["final_output_path"] = str(
                child_layout.final_output_file.relative_to(layout.root)
            )
            summary["final_output_text"] = child_layout.final_output_file.read_text(
                encoding="utf-8"
            )
        if child_layout.escalation_file.exists():
            summary["escalation_path"] = str(
                child_layout.escalation_file.relative_to(layout.root)
            )
            summary["escalation_text"] = child_layout.escalation_file.read_text(
                encoding="utf-8"
            )
        summaries.append(summary)
    return summaries


def _focus_sections_for_role(role: str) -> tuple[str, ...]:
    role_to_sections: dict[str, tuple[str, ...]] = {
        "planner": ("task_source", "retrieved_knowledge"),
        "worker": ("task_source", "retrieved_knowledge", "plan", "state"),
        "mid-plan-evaluator": (
            "task_source",
            "plan",
            "state",
            "latest_child_report",
            "progression_state",
        ),
        "synthesizer": (
            "task_source",
            "plan",
            "state",
            "children",
            "progression_state",
        ),
        "librarian": ("task_source",),
        "plan-reviewer": ("task_source", "plan", "retrieved_knowledge"),
        "plan-decider": ("task_source", "plan", "review"),
    }
    return role_to_sections.get(role, ("task_source", "state"))

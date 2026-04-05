"""Story/timeline helpers."""

from __future__ import annotations

from typing import Dict, List


def build_timeline(events: List[Dict[str, object]]) -> List[Dict[str, object]]:
    timeline = []
    for index, event in enumerate(events, start=1):
        timeline.append(
            {
                "step": index,
                "event_type": event["event_type"],
                "node_id": event.get("node_id"),
                "message": event.get("message"),
            }
        )
    return timeline


def timeline_markdown(timeline: List[Dict[str, object]]) -> str:
    lines = ["# Run Timeline", ""]
    for item in timeline:
        lines.append(f"{item['step']}. [{item['node_id']}] {item['message']}")
    lines.append("")
    return "\n".join(lines)

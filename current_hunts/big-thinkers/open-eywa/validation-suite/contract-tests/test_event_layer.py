from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from system.orchestrator import (
    AppendOnlyJsonlWriter,
    CostRecord,
    EventRecord,
    EventSchemaError,
    MissionSummary,
    NodeSummary,
    RunSummary,
    UsageRecord,
)


class EventLayerTests(unittest.TestCase):
    def test_event_record_validates_required_payload_keys(self) -> None:
        with self.assertRaises(EventSchemaError):
            EventRecord(
                event_type="node_status_changed",
                mission_id="mission-001",
                node_id="root",
                node_path="/tmp/root",
                payload={"status_before": "pending"},
            )

    def test_event_writer_appends_multiple_events_without_overwriting(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            event_path = Path(temp_dir) / "events.jsonl"
            writer = AppendOnlyJsonlWriter(event_path)

            writer.append_event(
                EventRecord(
                    event_type="node_created",
                    mission_id="mission-001",
                    node_id="root",
                    node_path="/tmp/root",
                )
            )
            writer.append_event(
                EventRecord(
                    event_type="node_status_changed",
                    mission_id="mission-001",
                    node_id="root",
                    node_path="/tmp/root",
                    payload={"status_before": "pending", "status_after": "active"},
                )
            )

            lines = event_path.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 2)
            first = json.loads(lines[0])
            second = json.loads(lines[1])
            self.assertEqual(first["event_type"], "node_created")
            self.assertEqual(second["event_type"], "node_status_changed")

    def test_usage_record_computes_total_tokens(self) -> None:
        usage = UsageRecord(
            prompt_tokens=10,
            completion_tokens=5,
            reasoning_tokens=2,
            cached_prompt_tokens=3,
            total_cost_usd=0.12,
        )

        self.assertEqual(usage.total_tokens, 15)
        self.assertEqual(usage.total_cost_usd, 0.12)

    def test_cost_record_computes_total_cost(self) -> None:
        cost = CostRecord(direct_usd=1.5, children_usd=0.25)

        self.assertEqual(cost.total_usd, 1.75)
        self.assertEqual(cost.currency, "USD")

    def test_summary_schemas_serialize_cleanly(self) -> None:
        usage = UsageRecord(prompt_tokens=4, completion_tokens=6, total_cost_usd=0.03)
        run_summary = RunSummary(
            run_id="run-001",
            node_id="root",
            role="planner",
            model="demo-model",
            variant="variant-a",
            started_at_utc="2026-04-01T00:00:00Z",
            finished_at_utc="2026-04-01T00:00:05Z",
            duration_seconds=5.0,
            exit_reason="completed",
            artifacts_produced=("output/plan.md",),
            tool_call_count=2,
            usage=usage,
        )
        node_summary = NodeSummary(
            mission_id="mission-001",
            node_id="root",
            node_path="/tmp/root",
            status="finished",
            terminal_outcome="completed",
            failure_reason=None,
            run_count=1,
            retry_count=0,
            roles_used=("planner",),
            artifacts_written=("output/plan.md",),
            total_duration_seconds=5.0,
            waiting_duration_seconds=0.0,
            usage=usage,
            cost=CostRecord(direct_usd=0.03),
        )
        mission_summary = MissionSummary(
            mission_id="mission-001",
            root_node_id="root",
            final_status="finished",
            terminal_outcome="completed",
            failure_reason=None,
            node_count=1,
            completed_node_count=1,
            escalated_node_count=0,
            cancelled_node_count=0,
            failed_node_count=0,
            run_count=1,
            total_duration_seconds=5.0,
            usage=usage,
            cost=CostRecord(direct_usd=0.03),
            roles_used=("planner",),
            models_used=("demo-model",),
            top_failure_reasons=(),
        )

        self.assertEqual(run_summary.to_dict()["usage"]["total_tokens"], 10)
        self.assertEqual(node_summary.to_dict()["cost"]["total_usd"], 0.03)
        self.assertEqual(mission_summary.to_dict()["completed_node_count"], 1)


if __name__ == "__main__":
    unittest.main()

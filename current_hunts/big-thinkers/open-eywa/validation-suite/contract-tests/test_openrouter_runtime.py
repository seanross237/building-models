from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from system.orchestrator import create_node
from system.orchestrator.node_preparation import prepare_node_context_packet
from system.runtime import (
    OpenRouterRuntime,
    OpenRouterRuntimeConfig,
    RuntimeRequest,
)


class FakeOpenRouterClient:
    def __init__(self, responses: list[dict[str, object]], generation_costs: dict[str, float] | None = None):
        self.responses = list(responses)
        self.generation_costs = dict(generation_costs or {})
        self.requests: list[dict[str, object]] = []

    def create_chat_completion(
        self,
        *,
        model: str,
        messages: list[dict[str, object]],
        tools: list[dict[str, object]] | None = None,
        tool_choice: str | dict[str, object] | None = "auto",
        max_tokens: int | None = None,
        temperature: float | None = None,
    ) -> dict[str, object]:
        self.requests.append(
            {
                "model": model,
                "messages": messages,
                "tools": tools,
                "tool_choice": tool_choice,
                "max_tokens": max_tokens,
                "temperature": temperature,
            }
        )
        if not self.responses:
            raise AssertionError("Fake client ran out of responses.")
        return self.responses.pop(0)

    def get_generation_stats(self, generation_id: str) -> dict[str, object]:
        return {
            "data": {
                "id": generation_id,
                "total_cost": self.generation_costs.get(generation_id, 0.0),
                "tokens_prompt": 0,
                "tokens_completion": 0,
                "provider_name": "fake-provider",
                "latency": 12,
            }
        }


class OpenRouterRuntimeTests(unittest.TestCase):
    def test_worker_tool_loop_writes_artifacts_and_records_usage(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            node_path = Path(temp_dir) / "root"
            layout = create_node(
                node_path,
                task_source_name="goal",
                task_text="Write a simple answer.",
                agent_mode="worker",
            )
            prepared = prepare_node_context_packet(layout, run_id="run-001", role="worker")

            fake_client = FakeOpenRouterClient(
                responses=[
                    {
                        "id": "gen-001",
                        "model": "openai/gpt-4.1-mini",
                        "choices": [
                            {
                                "message": {
                                    "role": "assistant",
                                    "tool_calls": [
                                        {
                                            "id": "call-1",
                                            "type": "function",
                                            "function": {
                                                "name": "write_file",
                                                "arguments": json.dumps(
                                                    {
                                                        "path": "output/final-output.md",
                                                        "content": "Hello from the live runtime.\n",
                                                    }
                                                ),
                                            },
                                        },
                                        {
                                            "id": "call-2",
                                            "type": "function",
                                            "function": {
                                                "name": "write_file",
                                                "arguments": json.dumps(
                                                    {
                                                        "path": "output/state.md",
                                                        "content": "Worker completed.\n",
                                                    }
                                                ),
                                            },
                                        },
                                    ],
                                },
                                "finish_reason": "tool_calls",
                            }
                        ],
                        "usage": {
                            "prompt_tokens": 11,
                            "completion_tokens": 8,
                            "total_tokens": 19,
                            "prompt_tokens_details": {"cached_tokens": 0},
                            "completion_tokens_details": {"reasoning_tokens": 2},
                        },
                    },
                    {
                        "id": "gen-002",
                        "model": "openai/gpt-4.1-mini",
                        "choices": [
                            {
                                "message": {
                                    "role": "assistant",
                                    "content": "Done.",
                                },
                                "finish_reason": "stop",
                            }
                        ],
                        "usage": {
                            "prompt_tokens": 7,
                            "completion_tokens": 2,
                            "total_tokens": 9,
                            "prompt_tokens_details": {"cached_tokens": 1},
                            "completion_tokens_details": {"reasoning_tokens": 1},
                        },
                    },
                ],
                generation_costs={"gen-001": 0.0011, "gen-002": 0.0004},
            )

            runtime = OpenRouterRuntime(
                OpenRouterRuntimeConfig(
                    api_key="test-key",
                    default_models={"worker": "openai/gpt-4.1-mini"},
                    fetch_generation_stats=True,
                ),
                client=fake_client,
            )

            result = runtime.run(
                RuntimeRequest(
                    mission_id="mission-001",
                    node_id="root",
                    node_path=str(node_path),
                    run_id="run-001",
                    role="worker",
                    prepared_inputs=(prepared.packet_path,),
                )
            )

            self.assertEqual(result.exit_reason, "completed")
            self.assertEqual(result.tool_call_count, 2)
            self.assertEqual(
                set(result.artifacts_produced),
                {"output/final-output.md", "output/state.md"},
            )
            self.assertEqual(result.usage.prompt_tokens, 18)
            self.assertEqual(result.usage.completion_tokens, 10)
            self.assertEqual(result.usage.reasoning_tokens, 3)
            self.assertEqual(result.usage.cached_prompt_tokens, 1)
            self.assertAlmostEqual(result.usage.total_cost_usd, 0.0015, places=6)
            self.assertTrue((node_path / "output" / "final-output.md").exists())
            self.assertEqual(
                (node_path / "output" / "final-output.md").read_text(encoding="utf-8"),
                "Hello from the live runtime.\n",
            )
            event_log = (node_path / "system" / "events.jsonl").read_text(encoding="utf-8")
            self.assertIn("tool_called", event_log)
            self.assertIn("tool_finished", event_log)
            self.assertEqual(len(fake_client.requests), 2)
            first_user_message = fake_client.requests[0]["messages"][1]["content"]
            self.assertIn("Prepared context packet", first_user_message)

    def test_runtime_fails_cleanly_on_tool_boundary_violation(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            node_path = Path(temp_dir) / "root"
            layout = create_node(
                node_path,
                task_source_name="goal",
                task_text="Do not escape the node.",
                agent_mode="worker",
            )
            prepared = prepare_node_context_packet(layout, run_id="run-001", role="worker")

            fake_client = FakeOpenRouterClient(
                responses=[
                    {
                        "id": "gen-err-001",
                        "model": "openai/gpt-4.1-mini",
                        "choices": [
                            {
                                "message": {
                                    "role": "assistant",
                                    "tool_calls": [
                                        {
                                            "id": "call-escape",
                                            "type": "function",
                                            "function": {
                                                "name": "write_file",
                                                "arguments": json.dumps(
                                                    {
                                                        "path": "../escape.txt",
                                                        "content": "bad\n",
                                                    }
                                                ),
                                            },
                                        }
                                    ],
                                },
                                "finish_reason": "tool_calls",
                            }
                        ],
                        "usage": {
                            "prompt_tokens": 5,
                            "completion_tokens": 3,
                            "total_tokens": 8,
                            "completion_tokens_details": {"reasoning_tokens": 1},
                        },
                    }
                ],
                generation_costs={"gen-err-001": 0.0007},
            )

            runtime = OpenRouterRuntime(
                OpenRouterRuntimeConfig(
                    api_key="test-key",
                    default_models={"worker": "openai/gpt-4.1-mini"},
                    fetch_generation_stats=True,
                ),
                client=fake_client,
            )

            result = runtime.run(
                RuntimeRequest(
                    mission_id="mission-002",
                    node_id="root",
                    node_path=str(node_path),
                    run_id="run-001",
                    role="worker",
                    prepared_inputs=(prepared.packet_path,),
                )
            )

            self.assertEqual(result.exit_reason, "failed")
            self.assertEqual(result.tool_call_count, 0)
            self.assertIn("Path escapes the node boundary", result.details["error"])
            self.assertFalse((Path(temp_dir) / "escape.txt").exists())
            event_log = (node_path / "system" / "events.jsonl").read_text(encoding="utf-8")
            self.assertIn("tool_called", event_log)
            self.assertIn("tool_failed", event_log)


if __name__ == "__main__":
    unittest.main()

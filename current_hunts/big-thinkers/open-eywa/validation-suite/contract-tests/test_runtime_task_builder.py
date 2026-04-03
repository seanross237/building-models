from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from system.runtime.prompt_loader import PromptBundle
from system.runtime.runtime_interface import RuntimeRequest
from system.runtime.runtime_task_builder import (
    RuntimeTaskBuildError,
    build_runtime_task_content,
    load_prepared_packet,
)


def _make_request(**overrides: object) -> RuntimeRequest:
    defaults = {
        "mission_id": "m-001",
        "node_id": "n-001",
        "node_path": "/tmp/test-node",
        "run_id": "r-001",
        "role": "worker",
    }
    defaults.update(overrides)
    return RuntimeRequest(**defaults)


def _make_bundle(**overrides: object) -> PromptBundle:
    defaults = {
        "role": "worker",
        "system_prompt": "You are a worker node.",
        "support_documents": (),
        "source_paths": ("stuff-for-agents/worker/system-prompt.md",),
    }
    defaults.update(overrides)
    return PromptBundle(**defaults)


class TestBuildRuntimeTaskContent(unittest.TestCase):
    def test_contains_role_and_run_id(self) -> None:
        request = _make_request(role="planner", run_id="r-42")
        bundle = _make_bundle(role="planner")
        content = build_runtime_task_content(request, bundle, [], provider_name="claude")
        self.assertIn("planner", content)
        self.assertIn("r-42", content)

    def test_contains_system_prompt(self) -> None:
        bundle = _make_bundle(system_prompt="Do the thing carefully.")
        content = build_runtime_task_content(_make_request(), bundle, [], provider_name="codex")
        self.assertIn("Do the thing carefully.", content)

    def test_contains_support_documents(self) -> None:
        bundle = _make_bundle(
            support_documents=(("plan-design.md", "Plan design rules here."),),
        )
        content = build_runtime_task_content(_make_request(), bundle, [], provider_name="claude")
        self.assertIn("plan-design.md", content)
        self.assertIn("Plan design rules here.", content)

    def test_contains_prepared_context(self) -> None:
        packets = [{"goal": "test goal", "parent_output": "some output"}]
        content = build_runtime_task_content(_make_request(), _make_bundle(), packets, provider_name="claude")
        self.assertIn("test goal", content)
        self.assertIn("some output", content)

    def test_contains_provider_name(self) -> None:
        content = build_runtime_task_content(_make_request(), _make_bundle(), [], provider_name="codex")
        self.assertIn("codex", content)

    def test_contains_instructions_section(self) -> None:
        content = build_runtime_task_content(_make_request(), _make_bundle(), [], provider_name="claude")
        self.assertIn("## Instructions", content)
        self.assertIn("output/escalation.md", content)

    def test_no_support_docs_section_when_empty(self) -> None:
        content = build_runtime_task_content(_make_request(), _make_bundle(), [], provider_name="claude")
        self.assertNotIn("## Supporting Documents", content)


class TestLoadPreparedPacket(unittest.TestCase):
    def test_loads_valid_json(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"key": "value"}, f)
            path = f.name
        try:
            result = load_prepared_packet(path)
            self.assertEqual(result, {"key": "value"})
        finally:
            os.unlink(path)

    def test_raises_on_missing_file(self) -> None:
        with self.assertRaises(RuntimeTaskBuildError):
            load_prepared_packet("/nonexistent/path.json")

    def test_raises_on_invalid_json(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("not json")
            path = f.name
        try:
            with self.assertRaises(RuntimeTaskBuildError):
                load_prepared_packet(path)
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main()

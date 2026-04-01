from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from system.orchestrator import create_node
from system.tools import FileToolExecutor, ToolExecutionError


class FileToolExecutorTests(unittest.TestCase):
    def test_write_and_read_file_stay_within_node_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            node_path = Path(temp_dir) / "root"
            create_node(node_path, task_source_name="goal", task_text="Test tools.")

            tools = FileToolExecutor()
            write_result = tools.execute(
                node_path,
                "write_file",
                {"path": "output/final-output.md", "content": "hello\n"},
            )
            read_result = tools.execute(
                node_path,
                "read_file",
                {"path": "output/final-output.md"},
            )

            self.assertEqual(write_result.artifact_paths, ("output/final-output.md",))
            self.assertEqual(read_result.output["content"], "hello\n")

    def test_edit_file_replaces_requested_text(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            node_path = Path(temp_dir) / "root"
            create_node(node_path, task_source_name="goal", task_text="Test tools.")

            tools = FileToolExecutor()
            tools.execute(
                node_path,
                "write_file",
                {"path": "output/state.md", "content": "status: draft\n"},
            )
            result = tools.execute(
                node_path,
                "edit_file",
                {
                    "path": "output/state.md",
                    "find_text": "draft",
                    "replace_text": "final",
                },
            )

            self.assertEqual(result.output["replacement_count"], 1)
            self.assertEqual((node_path / "output" / "state.md").read_text(encoding="utf-8"), "status: final\n")

    def test_glob_and_grep_return_relative_matches(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            node_path = Path(temp_dir) / "root"
            create_node(node_path, task_source_name="goal", task_text="Test tools.")

            tools = FileToolExecutor()
            tools.execute(
                node_path,
                "write_file",
                {"path": "output/alpha.txt", "content": "hello world\n"},
            )
            tools.execute(
                node_path,
                "write_file",
                {"path": "output/beta.txt", "content": "goodbye world\n"},
            )

            glob_result = tools.execute(node_path, "glob", {"pattern": "output/*.txt"})
            grep_result = tools.execute(node_path, "grep", {"pattern": "world", "start_path": "output"})

            self.assertEqual(glob_result.output["match_count"], 2)
            self.assertEqual(grep_result.output["match_count"], 2)
            self.assertTrue(
                all(match["path"].startswith("output/") for match in grep_result.output["matches"])
            )

    def test_write_file_rejects_paths_outside_node(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            node_path = Path(temp_dir) / "root"
            create_node(node_path, task_source_name="goal", task_text="Test tools.")

            with self.assertRaises(ToolExecutionError):
                FileToolExecutor().execute(
                    node_path,
                    "write_file",
                    {"path": "../outside.txt", "content": "bad\n"},
                )


if __name__ == "__main__":
    unittest.main()

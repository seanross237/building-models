from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[3]
GRADING_DIR = REPO_ROOT / "data-system" / "grading"
if str(GRADING_DIR) not in sys.path:
    sys.path.insert(0, str(GRADING_DIR))

RUN_PILOT = REPO_ROOT / "data-system" / "grading" / "run_mx1_pilot_v1.py"
RUN_TUTOR = REPO_ROOT / "data-system" / "grading" / "run_mx1_tutor_v1.py"
QUESTION_FILE = (
    REPO_ROOT
    / "data-system"
    / "grading"
    / "test-questions"
    / "architecture-derived-B6-binary-representation-minimization.md"
)
STARTER_PROMPT_FILE = (
    REPO_ROOT
    / "data-system"
    / "grading"
    / "prompt-experiments"
    / "mx1-pilot-v1"
    / "starter_transmute_prompt_v1.txt"
)
EXECUTE_PROMPT_FILE = (
    REPO_ROOT
    / "data-system"
    / "grading"
    / "prompt-experiments"
    / "mx1-pilot-v1"
    / "execute_prompt_v1.txt"
)


def parse_stdout(stdout: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for line in stdout.splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        parsed[key.strip()] = value.strip()
    return parsed


class MX1PilotV1Tests(unittest.TestCase):
    def test_tutor_applied_prompt_keeps_family_scaffold(self) -> None:
        import run_mx1_tutor_v1

        manifest = {
            "starter_prompt_text": (
                "starter guidance\n\n"
                "Return exactly one JSON object in this format:\n"
                "{\n"
                '  "schema_name": "eywa_node_response",\n'
                '  "schema_version": "v1",\n'
                '  "orchestration_decision": "transmute"\n'
                "}"
            )
        }
        recommended = (
            "new guidance\n\n"
            "Return exactly one JSON object in this format:\n"
            "{\n"
            '  "schema_name": "eywa_node_response",\n'
            '  "schema_version": "v1",\n'
            '  "orchestration_decision": "execute_locally"\n'
            "}"
        )

        normalized = run_mx1_tutor_v1._normalize_family_prompt_text(manifest, recommended)
        self.assertIn('"orchestration_decision": "transmute"', normalized)
        self.assertNotIn('"orchestration_decision": "execute_locally"', normalized)
        self.assertTrue(normalized.startswith("new guidance"))

    def test_current_prompt_path_does_not_fall_back_after_tutor_update(self) -> None:
        import run_mx1_pilot_v1

        manifest = {
            "current_prompt_source": "tutor",
            "current_prompt_file": None,
            "starter_prompt_file": "starter.txt",
        }
        self.assertIsNone(run_mx1_pilot_v1._current_prompt_path(manifest))

    def test_manifest_helpers_track_best_and_plateau(self) -> None:
        from mx1_loop_v1 import append_attempt, create_manifest

        manifest = create_manifest(
            question_id="q1",
            question_title="Question One",
            question_file="q1.md",
            family="transmute",
            runtime_provider="deterministic",
            model="deterministic-local-v1",
            starter_prompt_text="starter",
            child_prompt_text="execute",
            starter_prompt_file="starter.txt",
            child_prompt_file="execute.txt",
        )

        manifest = append_attempt(
            manifest,
            {
                "iteration_index": 0,
                "kind": "baseline",
                "run_id": "run-baseline",
                "score": 0.0,
                "total_tokens": 100,
                "total_wall_time_ms": 100,
                "prompt_text": "execute",
            },
        )
        manifest = append_attempt(
            manifest,
            {
                "iteration_index": 1,
                "kind": "transmute",
                "run_id": "run-1",
                "score": 0.0,
                "total_tokens": 120,
                "total_wall_time_ms": 120,
                "prompt_text": "prompt-1",
            },
        )
        manifest = append_attempt(
            manifest,
            {
                "iteration_index": 2,
                "kind": "transmute",
                "run_id": "run-2",
                "score": 0.0,
                "total_tokens": 130,
                "total_wall_time_ms": 130,
                "prompt_text": "prompt-2",
            },
        )

        self.assertEqual(manifest["best_attempt"]["run_id"], "run-2")
        self.assertEqual(manifest["history_summary"]["plateau_streak"], 2)
        self.assertTrue(manifest["history_summary"]["needs_new_direction"])
        self.assertEqual(manifest["next_iteration_index"], 3)

    def test_delegate_family_advances_iteration_index(self) -> None:
        from mx1_loop_v1 import append_attempt, create_manifest

        manifest = create_manifest(
            question_id="q2",
            question_title="Question Two",
            question_file="q2.md",
            family="delegate",
            runtime_provider="deterministic",
            model="deterministic-local-v1",
            starter_prompt_text="starter",
            child_prompt_text="execute",
            starter_prompt_file="starter.txt",
            child_prompt_file="execute.txt",
        )
        manifest = append_attempt(
            manifest,
            {
                "iteration_index": 1,
                "kind": "delegate",
                "run_id": "run-delegate-1",
                "score": 0.0,
                "total_tokens": 100,
                "total_wall_time_ms": 100,
                "prompt_text": "prompt-1",
            },
        )
        self.assertEqual(manifest["next_iteration_index"], 2)
        self.assertEqual(manifest["history_summary"]["iterations_completed"], 1)

    def test_delegate_family_uses_delegate_starter_prompt(self) -> None:
        import run_mx1_pilot_v1

        resolved = run_mx1_pilot_v1._resolve_starter_prompt_path(
            "delegate",
            str(run_mx1_pilot_v1.DEFAULT_STARTER_PROMPT_FILE),
        )
        self.assertEqual(resolved, run_mx1_pilot_v1.DEFAULT_DELEGATE_PROMPT_FILE.resolve())

    def test_stepwise_pilot_and_tutor_flow_updates_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            common_args = [
                "--question-file",
                str(QUESTION_FILE),
                "--family",
                "transmute",
                "--loops-root",
                str(root / "mx1-loops"),
                "--run-history-root",
                str(root / "run-history"),
                "--grading-runs-root",
                str(root / "grading-runs"),
                "--runtime-provider",
                "deterministic",
                "--model",
                "deterministic-local-v1",
                "--starter-prompt-file",
                str(STARTER_PROMPT_FILE),
                "--execute-prompt-file",
                str(EXECUTE_PROMPT_FILE),
            ]

            init_completed = subprocess.run(
                ["python3", str(RUN_PILOT), "--action", "init", *common_args],
                check=True,
                capture_output=True,
                text=True,
            )
            init_parsed = parse_stdout(init_completed.stdout)
            manifest_path = Path(init_parsed["manifest_path"])
            self.assertTrue(manifest_path.exists())

            baseline_completed = subprocess.run(
                ["python3", str(RUN_PILOT), "--action", "baseline", *common_args],
                check=True,
                capture_output=True,
                text=True,
            )
            baseline_parsed = parse_stdout(baseline_completed.stdout)
            baseline_grading_record = Path(baseline_parsed["grading_record"])
            self.assertTrue(baseline_grading_record.exists())

            baseline_record = json.loads(baseline_grading_record.read_text(encoding="utf-8"))
            self.assertEqual(baseline_record["mx1_family"], "transmute")
            self.assertEqual(baseline_record["mx1_iteration_index"], 0)
            self.assertEqual(baseline_record["mx1_prompt_text"], EXECUTE_PROMPT_FILE.read_text(encoding="utf-8").strip())
            self.assertIsNone(baseline_record["mx1_tutor_record_path"])

            iterate_completed = subprocess.run(
                ["python3", str(RUN_PILOT), "--action", "iterate", *common_args],
                check=True,
                capture_output=True,
                text=True,
            )
            iterate_parsed = parse_stdout(iterate_completed.stdout)
            iterate_grading_record = Path(iterate_parsed["grading_record"])
            self.assertTrue(iterate_grading_record.exists())

            iterate_record = json.loads(iterate_grading_record.read_text(encoding="utf-8"))
            self.assertEqual(iterate_record["mx1_family"], "transmute")
            self.assertEqual(iterate_record["mx1_iteration_index"], 1)
            self.assertEqual(iterate_record["mx1_prompt_text"], STARTER_PROMPT_FILE.read_text(encoding="utf-8").strip())
            self.assertIsNone(iterate_record["mx1_tutor_record_path"])
            self.assertIn("final_result_excerpt", iterate_record)

            tutor_completed = subprocess.run(
                [
                    "python3",
                    str(RUN_TUTOR),
                    "--manifest",
                    str(manifest_path),
                    "--tutoring-root",
                    str(root / "mx1-tutoring"),
                    "--tutor-provider",
                    "deterministic",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            tutor_parsed = parse_stdout(tutor_completed.stdout)
            tutor_record_path = Path(tutor_parsed["tutor_record"])
            self.assertTrue(tutor_record_path.exists())

            updated_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(updated_manifest["current_prompt_source"], "tutor")
            self.assertTrue(updated_manifest["current_prompt_text"])

            updated_iterate_record = json.loads(iterate_grading_record.read_text(encoding="utf-8"))
            self.assertEqual(updated_iterate_record["mx1_tutor_record_path"], str(tutor_record_path))
            self.assertIn("mx1_tutor", updated_iterate_record)
            self.assertIn("recommendation", updated_iterate_record["mx1_tutor"])


if __name__ == "__main__":
    unittest.main()

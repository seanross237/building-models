from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path
import sys
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[3]
GRADING_DIR = REPO_ROOT / "data-system" / "grading"
if str(GRADING_DIR) not in sys.path:
    sys.path.insert(0, str(GRADING_DIR))


class CodingGradeV1Tests(unittest.TestCase):
    def _build_toy_binary_packet(self, root: Path) -> tuple[Path, object]:
        from question_bank_v1 import QuestionCase

        packet_root = root / "coding-packets" / "coding-toy-sum"
        tests_root = packet_root / "tests"
        tests_root.mkdir(parents=True)
        (packet_root / "problem.md").write_text("Add two integers.", encoding="utf-8")
        (tests_root / "sample_1.in").write_text("2 3\n", encoding="utf-8")
        (tests_root / "sample_1.out").write_text("5\n", encoding="utf-8")
        (packet_root / "manifest.json").write_text(
            json.dumps(
                {
                    "schema_name": "eywa_coding_packet",
                    "schema_version": "v1",
                    "question_id": "coding-toy-sum",
                    "language": "python",
                    "entry_file": "main.py",
                    "problem_statement_path": "problem.md",
                    "checker_type": "binary_public_tests",
                    "time_limit_seconds": 1.0,
                    "public_tests": [
                        {
                            "name": "sample_1",
                            "stdin_path": "tests/sample_1.in",
                            "expected_stdout_path": "tests/sample_1.out",
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        question_case = QuestionCase(
            question_id="coding-toy-sum",
            title="Toy Sum",
            source_path=root / "toy.md",
            family="coding",
            entry_type="coding",
            domain="",
            subtype="",
            grader_type="binary_hidden_tests",
            grader_config={},
            source_label="",
            sections={"problem": "Add two integers.", "grading": "Binary public tests."},
            metadata={},
            coding_packet_manifest=packet_root / "manifest.json",
            coding_packet_exists=True,
            coding_checker_type="binary_public_tests",
        )
        return packet_root, question_case

    def test_b1_packet_exists(self) -> None:
        from coding_packets_v1 import load_coding_packet

        packet = load_coding_packet(question_id="coding-B1-usaco-2024-us-open-platinum-identity-theft")
        self.assertEqual(packet.checker_type, "binary_public_tests")
        self.assertEqual(len(packet.public_tests), 5)

    def test_s5_packet_uses_official_atcoder_vis(self) -> None:
        from coding_packets_v1 import load_coding_packet

        packet = load_coding_packet(question_id="coding-S5-ahc032-mod-stamp")
        self.assertEqual(packet.checker_type, "continuous_public_simulator")
        self.assertEqual(packet.official_tool_mode, "atcoder_vis")
        self.assertIsNotNone(packet.official_tool_path)
        self.assertEqual(len(packet.instances), 3)

    def test_parse_atcoder_score_handles_both_formats(self) -> None:
        from atcoder_official_tools_v1 import parse_atcoder_score

        self.assertEqual(parse_atcoder_score("Score = 12345"), 12345.0)
        self.assertEqual(parse_atcoder_score("987654321\n"), 987654321.0)

    def test_toy_binary_packet_grades_correct_submission(self) -> None:
        from grading_methods.coding_grade_v1 import maybe_grade_coding_submission

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _, question_case = self._build_toy_binary_packet(root)

            run_dir = root / "run"
            artifact_path = run_dir / "artifacts" / "node_root" / "turn_01" / "main.py"
            artifact_path.parent.mkdir(parents=True)
            artifact_path.write_text(
                "import sys\n"
                "a, b = map(int, sys.stdin.read().split())\n"
                "print(a + b)\n",
                encoding="utf-8",
            )

            with mock.patch("coding_packets_v1.CODING_PACKETS_DIR", root / "coding-packets"):
                grading, trace = maybe_grade_coding_submission(
                    question_case,
                    run_dir=run_dir,
                    final_output={
                        "result": {
                            "attachment_refs": [
                                "artifacts/node_root/turn_01/main.py"
                            ]
                        }
                    },
                )

            self.assertEqual(grading["grading_status"], "graded")
            self.assertTrue(grading["correct"])
            self.assertEqual(grading["score"], 1.0)
            self.assertEqual(grading["task_score"], 1.0)
            self.assertEqual(grading["submission_compliance"], "clean")
            self.assertEqual(grading["submission_source"], "attachment")
            self.assertFalse(grading["recovery_used"])
            self.assertEqual(trace["execution"]["case_results"][0]["matched"], True)

    def test_toy_binary_packet_recovers_from_fenced_code(self) -> None:
        from grading_methods.coding_grade_v1 import maybe_grade_coding_submission

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _, question_case = self._build_toy_binary_packet(root)
            run_dir = root / "run"
            run_dir.mkdir(parents=True)
            response_text = (
                "Here is my solution.\n"
                "```python\n"
                "import sys\n"
                "a, b = map(int, sys.stdin.read().split())\n"
                "print(a + b)\n"
                "```\n"
            )
            with mock.patch("coding_packets_v1.CODING_PACKETS_DIR", root / "coding-packets"):
                grading, trace = maybe_grade_coding_submission(
                    question_case,
                    run_dir=run_dir,
                    final_output={"result": {"content": response_text, "attachment_refs": []}},
                )

            self.assertEqual(grading["score"], 1.0)
            self.assertEqual(grading["submission_compliance"], "recovered_from_fenced_code")
            self.assertEqual(grading["submission_source"], "fenced_code")
            self.assertTrue(grading["recovery_used"])
            recovered = Path(trace["submission"]["submission_path"])
            self.assertTrue(recovered.exists())

    def test_toy_binary_packet_recovers_from_plain_text(self) -> None:
        from grading_methods.coding_grade_v1 import maybe_grade_coding_submission

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _, question_case = self._build_toy_binary_packet(root)
            run_dir = root / "run"
            run_dir.mkdir(parents=True)
            response_text = (
                "import sys\n"
                "a, b = map(int, sys.stdin.read().split())\n"
                "print(a + b)\n"
            )
            with mock.patch("coding_packets_v1.CODING_PACKETS_DIR", root / "coding-packets"):
                grading, _ = maybe_grade_coding_submission(
                    question_case,
                    run_dir=run_dir,
                    final_output={"result": {"content": response_text, "attachment_refs": []}},
                )

            self.assertEqual(grading["score"], 1.0)
            self.assertEqual(grading["submission_compliance"], "recovered_from_plain_text")
            self.assertEqual(grading["submission_source"], "plain_text")
            self.assertTrue(grading["recovery_used"])

    def test_toy_binary_packet_hard_fails_on_ambiguous_fenced_code(self) -> None:
        from grading_methods.coding_grade_v1 import maybe_grade_coding_submission

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _, question_case = self._build_toy_binary_packet(root)
            run_dir = root / "run"
            run_dir.mkdir(parents=True)
            response_text = (
                "```python\nimport sys\nprint('one')\n```\n"
                "```python\nimport sys\nprint('two')\n```\n"
            )
            with mock.patch("coding_packets_v1.CODING_PACKETS_DIR", root / "coding-packets"):
                grading, _ = maybe_grade_coding_submission(
                    question_case,
                    run_dir=run_dir,
                    final_output={"result": {"content": response_text, "attachment_refs": []}},
                )

            self.assertEqual(grading["grading_status"], "graded")
            self.assertEqual(grading["score"], 0.0)
            self.assertEqual(grading["submission_compliance"], "ambiguous_submission")
            self.assertIn("ambiguous", grading["grading_notes"].lower())

    def test_toy_continuous_packet_grades_via_public_scorer(self) -> None:
        from grading_methods.coding_grade_v1 import maybe_grade_coding_submission
        from question_bank_v1 import QuestionCase

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            packet_root = root / "coding-packets" / "coding-toy-double"
            instances_root = packet_root / "instances"
            instances_root.mkdir(parents=True)
            (packet_root / "problem.md").write_text("Double one integer.", encoding="utf-8")
            (instances_root / "sample_1.in").write_text("4\n", encoding="utf-8")
            (packet_root / "scorer.py").write_text(
                "from __future__ import annotations\n"
                "import argparse, json\n"
                "from pathlib import Path\n"
                "p=argparse.ArgumentParser(); p.add_argument('--input'); p.add_argument('--output'); a=p.parse_args()\n"
                "expected = int(Path(a.input).read_text().strip()) * 2\n"
                "got = int(Path(a.output).read_text().strip())\n"
                "print(json.dumps({'score': 100.0 if got == expected else 0.0, 'notes': 'ok' if got == expected else 'wrong'}))\n",
                encoding="utf-8",
            )
            (packet_root / "manifest.json").write_text(
                json.dumps(
                    {
                        "schema_name": "eywa_coding_packet",
                        "schema_version": "v1",
                        "question_id": "coding-toy-double",
                        "language": "python",
                        "entry_file": "main.py",
                        "problem_statement_path": "problem.md",
                        "checker_type": "continuous_public_simulator",
                        "time_limit_seconds": 1.0,
                        "aggregate_method": "mean",
                        "scorer": {"path": "scorer.py"},
                        "instances": [
                            {
                                "name": "sample_1",
                                "stdin_path": "instances/sample_1.in",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            run_dir = root / "run"
            artifact_path = run_dir / "artifacts" / "node_root" / "turn_01" / "main.py"
            artifact_path.parent.mkdir(parents=True)
            artifact_path.write_text(
                "import sys\n"
                "n = int(sys.stdin.read().strip())\n"
                "print(n * 2)\n",
                encoding="utf-8",
            )

            question_case = QuestionCase(
                question_id="coding-toy-double",
                title="Toy Double",
                source_path=root / "toy.md",
                family="coding",
                entry_type="coding",
                domain="",
                subtype="",
                grader_type="continuous_score",
                grader_config={},
                source_label="",
                sections={"problem": "Double one integer.", "grading": "Continuous score."},
                metadata={},
                coding_packet_manifest=packet_root / "manifest.json",
                coding_packet_exists=True,
                coding_checker_type="continuous_public_simulator",
            )

            with mock.patch("coding_packets_v1.CODING_PACKETS_DIR", root / "coding-packets"):
                grading, trace = maybe_grade_coding_submission(
                    question_case,
                    run_dir=run_dir,
                    final_output={
                        "result": {
                            "attachment_refs": [
                                "artifacts/node_root/turn_01/main.py"
                            ]
                        }
                    },
                )

            self.assertEqual(grading["grading_status"], "graded")
            self.assertEqual(grading["score"], 100.0)
            self.assertEqual(grading["task_score"], 100.0)
            self.assertEqual(trace["execution"]["instance_results"][0]["score"], 100.0)

    def test_official_vis_softens_invalid_candidate_output(self) -> None:
        from atcoder_official_tools_v1 import run_atcoder_vis

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            tool_dir = root / "tools"
            tool_dir.mkdir(parents=True)
            (tool_dir / "target" / "release").mkdir(parents=True)
            vis_bin = tool_dir / "target" / "release" / "vis"
            vis_bin.write_text("", encoding="utf-8")
            input_path = root / "sample.in"
            output_path = root / "candidate.out"
            input_path.write_text("dummy\n", encoding="utf-8")
            output_path.write_text("", encoding="utf-8")
            artifact_dir = root / "artifacts"
            artifact_dir.mkdir()
            with mock.patch("atcoder_official_tools_v1.ensure_official_tool_binary", return_value=vis_bin):
                with mock.patch("subprocess.run") as run_mock:
                    run_mock.return_value = subprocess.CompletedProcess(
                        args=["vis"],
                        returncode=101,
                        stdout="",
                        stderr="thread 'main' panicked at 'called `Option::unwrap()` on a `None` value'",
                    )
                    payload = run_atcoder_vis(
                        tool_dir=tool_dir,
                        input_path=input_path,
                        output_path=output_path,
                        artifact_dir=artifact_dir,
                        timeout_seconds=5.0,
                    )

            self.assertTrue(payload["ok"])
            self.assertEqual(payload["status"], "candidate_output_invalid")
            self.assertEqual(payload["score"], 0.0)


if __name__ == "__main__":
    unittest.main()

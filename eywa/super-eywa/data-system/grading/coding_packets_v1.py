"""Helpers for packetized coding benchmarks."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any


THIS_DIR = Path(__file__).resolve().parent
CODING_PACKETS_DIR = THIS_DIR / "coding-packets"
SUPPORTED_CHECKER_TYPES = {"binary_public_tests", "binary_public_checker", "continuous_public_simulator"}
SUPPORTED_OFFICIAL_TOOL_MODES = {"atcoder_vis", "atcoder_tester_then_vis"}


@dataclass(frozen=True)
class BinaryPublicTest:
    name: str
    stdin_path: Path
    expected_stdout_path: Path


@dataclass(frozen=True)
class ContinuousInstance:
    name: str
    stdin_path: Path


@dataclass(frozen=True)
class CodingPacket:
    question_id: str
    packet_dir: Path
    manifest_path: Path
    problem_statement_path: Path
    language: str
    entry_file: str
    checker_type: str
    time_limit_seconds: float
    public_tests: tuple[BinaryPublicTest, ...]
    instances: tuple[ContinuousInstance, ...]
    checker_path: Path | None
    scorer_path: Path | None
    official_tool_mode: str | None
    official_tool_path: Path | None
    official_tool_timeout_seconds: float
    aggregate_method: str
    notes: str
    valid_baseline_hint: str


class CodingPacketError(ValueError):
    """Raised when a coding packet is missing or malformed."""


def packet_dir_for_question_id(question_id: str) -> Path:
    return CODING_PACKETS_DIR / str(question_id).strip()


def manifest_path_for_question_id(question_id: str) -> Path:
    return packet_dir_for_question_id(question_id) / "manifest.json"


def coding_packet_exists(question_id: str) -> bool:
    return manifest_path_for_question_id(question_id).exists()


def load_coding_packet(*, question_id: str, strict: bool = True) -> CodingPacket | None:
    manifest_path = manifest_path_for_question_id(question_id)
    if not manifest_path.exists():
        if strict:
            raise CodingPacketError(f"missing coding packet manifest for {question_id}")
        return None

    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise CodingPacketError(f"invalid coding packet manifest JSON for {question_id}") from exc

    if payload.get("schema_name") != "eywa_coding_packet":
        raise CodingPacketError(f"invalid coding packet schema_name for {question_id}")
    if payload.get("schema_version") != "v1":
        raise CodingPacketError(f"invalid coding packet schema_version for {question_id}")

    packet_dir = manifest_path.parent
    checker_type = str(payload.get("checker_type") or "").strip()
    if checker_type not in SUPPORTED_CHECKER_TYPES:
        raise CodingPacketError(f"unsupported coding packet checker_type for {question_id}: {checker_type}")

    problem_statement_path = packet_dir / str(payload.get("problem_statement_path") or "problem.md")
    if not problem_statement_path.exists():
        raise CodingPacketError(f"missing problem statement for coding packet {question_id}")

    entry_file = str(payload.get("entry_file") or "main.py").strip() or "main.py"
    language = str(payload.get("language") or "python").strip().lower() or "python"
    time_limit_seconds = float(payload.get("time_limit_seconds") or 2.0)
    aggregate_method = str(payload.get("aggregate_method") or "mean").strip() or "mean"
    notes = str(payload.get("notes") or "").strip()
    valid_baseline_hint = str(payload.get("valid_baseline_hint") or "").strip()

    public_tests: list[BinaryPublicTest] = []
    for raw in payload.get("public_tests") or []:
        if not isinstance(raw, dict):
            continue
        name = str(raw.get("name") or "case").strip() or "case"
        stdin_path = packet_dir / str(raw.get("stdin_path") or "")
        expected_stdout_path = packet_dir / str(raw.get("expected_stdout_path") or "")
        if not stdin_path.exists() or not expected_stdout_path.exists():
            raise CodingPacketError(f"missing public test files for {question_id}:{name}")
        public_tests.append(
            BinaryPublicTest(
                name=name,
                stdin_path=stdin_path,
                expected_stdout_path=expected_stdout_path,
            )
        )

    instances: list[ContinuousInstance] = []
    for raw in payload.get("instances") or []:
        if not isinstance(raw, dict):
            continue
        name = str(raw.get("name") or "instance").strip() or "instance"
        stdin_path = packet_dir / str(raw.get("stdin_path") or "")
        if not stdin_path.exists():
            raise CodingPacketError(f"missing continuous instance file for {question_id}:{name}")
        instances.append(ContinuousInstance(name=name, stdin_path=stdin_path))

    checker_path: Path | None = None
    checker = payload.get("checker") or {}
    if isinstance(checker, dict) and checker.get("path"):
        checker_path = packet_dir / str(checker.get("path"))
        if not checker_path.exists():
            raise CodingPacketError(f"missing checker file for coding packet {question_id}")

    scorer_path: Path | None = None
    scorer = payload.get("scorer") or {}
    if isinstance(scorer, dict) and scorer.get("path"):
        scorer_path = packet_dir / str(scorer.get("path"))
        if not scorer_path.exists():
            raise CodingPacketError(f"missing scorer file for coding packet {question_id}")

    official_tool_mode: str | None = None
    official_tool_path: Path | None = None
    official_tool_timeout_seconds = max(time_limit_seconds, 30.0)
    official_tool = payload.get("official_tool") or {}
    if isinstance(official_tool, dict) and official_tool.get("mode"):
        official_tool_mode = str(official_tool.get("mode") or "").strip()
        if official_tool_mode not in SUPPORTED_OFFICIAL_TOOL_MODES:
            raise CodingPacketError(
                f"unsupported official_tool.mode for coding packet {question_id}: {official_tool_mode}"
            )
        official_tool_path = packet_dir / str(official_tool.get("path") or "tools")
        if not official_tool_path.exists():
            raise CodingPacketError(f"missing official tool directory for coding packet {question_id}")
        official_tool_timeout_seconds = float(
            official_tool.get("timeout_seconds") or official_tool_timeout_seconds
        )

    return CodingPacket(
        question_id=question_id,
        packet_dir=packet_dir,
        manifest_path=manifest_path,
        problem_statement_path=problem_statement_path,
        language=language,
        entry_file=entry_file,
        checker_type=checker_type,
        time_limit_seconds=time_limit_seconds,
        public_tests=tuple(public_tests),
        instances=tuple(instances),
        checker_path=checker_path,
        scorer_path=scorer_path,
        official_tool_mode=official_tool_mode,
        official_tool_path=official_tool_path,
        official_tool_timeout_seconds=official_tool_timeout_seconds,
        aggregate_method=aggregate_method,
        notes=notes,
        valid_baseline_hint=valid_baseline_hint,
    )

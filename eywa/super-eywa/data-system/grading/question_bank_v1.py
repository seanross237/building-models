"""Canonical question-bank loader and catalog generator for Super-Eywa grading."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any

from coding_packets_v1 import coding_packet_exists, load_coding_packet


THIS_DIR = Path(__file__).resolve().parent
TEST_QUESTIONS_DIR = THIS_DIR / "test-questions"
DEFAULT_QUESTION_BANK_PATH = THIS_DIR / "question-bank-v1.json"
NON_BENCHMARK_FILENAMES = {"README.md", "questions-thoughts.md"}


AUTO_GRADED_SPECS: dict[str, dict[str, Any]] = {
    "architecture-derived-B2-sign-sensitive-derivation-exciton-rydberg-energy": {
        "grader_type": "numeric_tolerance",
        "expected": -0.08,
        "tolerance": 0.005,
    },
    "architecture-derived-B4-hensel-lifting-verification": {
        "grader_type": "exact_numeric_hensel_target",
        "expected": 110,
    },
    "architecture-derived-B5-combinatorial-probability-random-chords": {
        "grader_type": "exact_numeric",
        "expected": 204,
    },
    "architecture-derived-B6-binary-representation-minimization": {
        "grader_type": "exact_numeric",
        "expected": 3,
    },
    "architecture-derived-B10-mean-field-lattice-gas-occupancy": {
        "grader_type": "numeric_tolerance",
        "expected": 0.424,
        "tolerance": 0.01,
    },
    "architecture-derived-B11-board-game-rule-chaining": {
        "grader_type": "exact_normalized_string",
        "expected": "unknown",
    },
}


@dataclass(frozen=True)
class QuestionCase:
    question_id: str
    title: str
    source_path: Path
    family: str
    entry_type: str
    domain: str
    subtype: str
    grader_type: str
    grader_config: dict[str, Any]
    source_label: str
    sections: dict[str, str]
    metadata: dict[str, Any]
    coding_packet_manifest: Path | None
    coding_packet_exists: bool
    coding_checker_type: str


def build_question_bank_catalog(question_dir: Path | None = None) -> dict[str, Any]:
    root = (question_dir or TEST_QUESTIONS_DIR).resolve()
    questions = [
        build_question_entry_from_markdown(path)
        for path in sorted(root.glob("*.md"))
        if path.name not in NON_BENCHMARK_FILENAMES
    ]
    return {
        "schema_name": "eywa_question_bank",
        "schema_version": "v1",
        "generated_at_utc": _utc_now(),
        "question_count": len(questions),
        "questions": questions,
    }


def write_question_bank_catalog(
    *,
    question_dir: Path | None = None,
    output_path: Path | None = None,
) -> Path:
    destination = (output_path or DEFAULT_QUESTION_BANK_PATH).resolve()
    payload = build_question_bank_catalog(question_dir=question_dir)
    destination.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return destination


def ensure_question_bank_catalog(
    *,
    question_dir: Path | None = None,
    output_path: Path | None = None,
) -> Path:
    root = (question_dir or TEST_QUESTIONS_DIR).resolve()
    destination = (output_path or DEFAULT_QUESTION_BANK_PATH).resolve()
    if not destination.exists() or _catalog_is_stale(destination, root):
        write_question_bank_catalog(question_dir=root, output_path=destination)
    return destination


def load_question_bank_catalog(
    *,
    question_dir: Path | None = None,
    output_path: Path | None = None,
) -> dict[str, Any]:
    destination = ensure_question_bank_catalog(question_dir=question_dir, output_path=output_path)
    return json.loads(destination.read_text(encoding="utf-8"))


def load_question_case(*, source_path: Path | None = None, question_id: str | None = None) -> QuestionCase:
    catalog = load_question_bank_catalog()
    normalized_source = None
    if source_path is not None:
        raw_source = Path(source_path)
        if raw_source.is_absolute() or raw_source.exists():
            normalized_source = raw_source.resolve()
        else:
            grading_relative = (Path(__file__).resolve().parent / raw_source).resolve()
            repo_relative = (Path(__file__).resolve().parents[2] / raw_source).resolve()
            if grading_relative.exists():
                normalized_source = grading_relative
            elif repo_relative.exists():
                normalized_source = repo_relative
            else:
                normalized_source = raw_source.resolve()
    for question in catalog.get("questions") or []:
        if question_id and question.get("question_id") == question_id:
            return _question_case_from_entry(question)
        if normalized_source and Path(str(question.get("source_file"))).resolve() == normalized_source:
            return _question_case_from_entry(question)
    if normalized_source is not None:
        if not normalized_source.exists():
            raise ValueError(f"Unknown question source path: {source_path}")
        return _question_case_from_entry(build_question_entry_from_markdown(normalized_source))
    if question_id:
        raise ValueError(f"Unknown question_id: {question_id}")
    raise ValueError("Either source_path or question_id is required.")


def build_question_entry_from_markdown(path: Path) -> dict[str, Any]:
    raw_text = path.read_text(encoding="utf-8")
    lines = raw_text.splitlines()
    title = path.stem
    if lines and lines[0].startswith("# "):
        title = lines[0][2:].strip()

    metadata_lines: list[str] = []
    section_lines: list[str] = []
    in_sections = False
    for line in lines[1:]:
        if line.startswith("## "):
            in_sections = True
        if in_sections:
            section_lines.append(line)
        else:
            metadata_lines.append(line)

    metadata = _parse_metadata_lines(metadata_lines)
    sections = _parse_section_lines(section_lines)
    problem_text = sections.get("problem", "")
    correct_answer = sections.get("correct_answer", "")
    grading_text = sections.get("grading", "")
    why_text = sections.get("why_it_discriminates", "")
    notes_text = sections.get("notes", "")
    family = _normalize_family(path, metadata)
    entry_type = _normalize_entry_type(metadata, family)
    grader_type = _normalize_grader_type(path.stem, metadata, grading_text, bool(correct_answer.strip()))
    grader_config = _build_grader_config(path.stem, grader_type)
    packet_manifest = None
    packet_exists = False
    packet_checker_type = ""
    if entry_type == "coding":
        packet_exists = coding_packet_exists(path.stem)
        packet_manifest = str((Path(__file__).resolve().parent / "coding-packets" / path.stem / "manifest.json").resolve())
        if packet_exists:
            try:
                packet_checker_type = load_coding_packet(question_id=path.stem, strict=True).checker_type
            except Exception:
                packet_checker_type = ""

    return {
        "question_id": path.stem,
        "title": title,
        "source_file": str(path.resolve()),
        "family": family,
        "entry_type": entry_type,
        "domain": metadata.get("domain", ""),
        "subtype": metadata.get("subtype", ""),
        "grader_type": grader_type,
        "grader_config": grader_config,
        "source_label": metadata.get("source", ""),
        "auto_graded_now": path.stem in AUTO_GRADED_SPECS or (entry_type == "coding" and packet_exists and bool(packet_checker_type)),
        "coding_packet_manifest": packet_manifest,
        "coding_packet_exists": packet_exists,
        "coding_checker_type": packet_checker_type,
        "problem_text": problem_text,
        "correct_answer": correct_answer,
        "grading_text": grading_text,
        "why_it_discriminates": why_text,
        "notes_text": notes_text,
        "sections": sections,
        "metadata": metadata,
    }


def _parse_metadata_lines(lines: list[str]) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for raw_line in lines:
        line = raw_line.strip()
        if not line.startswith("- ") or ":" not in line:
            continue
        key, value = line[2:].split(":", 1)
        metadata[_slugify_metadata_key(key)] = value.strip()
    return metadata


def _parse_section_lines(lines: list[str]) -> dict[str, str]:
    sections: dict[str, str] = {}
    current_section: str | None = None
    buffer: list[str] = []

    def flush() -> None:
        nonlocal buffer, current_section
        if current_section is not None:
            sections[current_section] = "\n".join(buffer).strip()
        buffer = []

    for line in lines:
        if line.startswith("## "):
            flush()
            current_section = _normalize_section_name(line[3:].strip())
            continue
        if current_section is None:
            continue
        buffer.append(line)
    flush()
    return sections


def _normalize_section_name(name: str) -> str:
    normalized = name.lower().replace(" ", "_")
    if normalized in {"question", "task"}:
        return "problem"
    return normalized


def _normalize_family(path: Path, metadata: dict[str, str]) -> str:
    raw = (metadata.get("family") or metadata.get("type") or "").strip().lower()
    if raw:
        return raw.replace(" ", "-")
    stem = path.stem
    if stem.startswith("architecture-derived-"):
        return "architecture-derived"
    if stem.startswith("atlas-derived-"):
        return "atlas-derived"
    if stem.startswith("coding-"):
        return "coding"
    return "unknown"


def _normalize_entry_type(metadata: dict[str, str], family: str) -> str:
    raw = (metadata.get("entry_type") or "").strip().lower()
    if raw:
        return raw
    return "coding" if family == "coding" else "reasoning"


def _normalize_grader_type(
    question_id: str,
    metadata: dict[str, str],
    grading_text: str,
    has_correct_answer: bool,
) -> str:
    if question_id in AUTO_GRADED_SPECS:
        return str(AUTO_GRADED_SPECS[question_id]["grader_type"])
    explicit = (metadata.get("grader_type") or "").strip().lower()
    if explicit:
        return explicit
    lowered = grading_text.strip().lower()
    if "binary hidden-test acceptance" in lowered:
        return "binary_hidden_tests"
    if any(
        marker in lowered
        for marker in (
            "continuous score",
            "higher is better",
            "lower probing cost is better",
            "round(10^6",
            "score is ",
        )
    ):
        return "continuous_score"
    if "exact match on the single letter" in lowered:
        return "exact_choice_letter"
    if "exact match on the single bitstring" in lowered or "exact match on the bitstring" in lowered:
        return "exact_string"
    if "exact numerical match" in lowered:
        return "exact_numeric"
    if lowered.startswith("binary:"):
        return "binary_reasoning"
    if has_correct_answer:
        return "manual_exact"
    return "manual_review"


def _build_grader_config(question_id: str, grader_type: str) -> dict[str, Any]:
    config = dict(AUTO_GRADED_SPECS.get(question_id) or {})
    config.setdefault("grader_type", grader_type)
    return config


def _question_case_from_entry(entry: dict[str, Any]) -> QuestionCase:
    sections = dict(entry.get("sections") or {})
    if "problem" not in sections:
        sections["problem"] = str(entry.get("problem_text") or "")
    if "correct_answer" not in sections:
        sections["correct_answer"] = str(entry.get("correct_answer") or "")
    if "grading" not in sections:
        sections["grading"] = str(entry.get("grading_text") or "")
    if "why_it_discriminates" not in sections and entry.get("why_it_discriminates") is not None:
        sections["why_it_discriminates"] = str(entry.get("why_it_discriminates") or "")
    if "notes" not in sections and entry.get("notes_text") is not None:
        sections["notes"] = str(entry.get("notes_text") or "")

    return QuestionCase(
        question_id=str(entry["question_id"]),
        title=str(entry["title"]),
        source_path=Path(str(entry["source_file"])),
        family=str(entry.get("family") or ""),
        entry_type=str(entry.get("entry_type") or ""),
        domain=str(entry.get("domain") or ""),
        subtype=str(entry.get("subtype") or ""),
        grader_type=str(entry.get("grader_type") or ""),
        grader_config=dict(entry.get("grader_config") or {}),
        source_label=str(entry.get("source_label") or ""),
        sections=sections,
        metadata=dict(entry.get("metadata") or {}),
        coding_packet_manifest=Path(str(entry["coding_packet_manifest"])) if entry.get("coding_packet_manifest") else None,
        coding_packet_exists=bool(entry.get("coding_packet_exists")),
        coding_checker_type=str(entry.get("coding_checker_type") or ""),
    )


def _catalog_is_stale(catalog_path: Path, question_dir: Path) -> bool:
    try:
        catalog_mtime = catalog_path.stat().st_mtime
    except FileNotFoundError:
        return True
    for path in question_dir.glob("*.md"):
        if path.name in NON_BENCHMARK_FILENAMES:
            continue
        if path.stat().st_mtime > catalog_mtime:
            return True
    coding_packets_root = Path(__file__).resolve().parent / "coding-packets"
    if coding_packets_root.exists():
        for path in coding_packets_root.rglob("*"):
            if not path.is_file():
                continue
            if path.stat().st_mtime > catalog_mtime:
                return True
    return False


def _slugify_metadata_key(key: str) -> str:
    return key.strip().lower().replace(" ", "_")


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

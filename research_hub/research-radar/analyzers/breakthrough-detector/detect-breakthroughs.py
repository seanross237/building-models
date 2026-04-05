#!/usr/bin/env python3
"""Scan analyzed Research Radar summaries for science breakthroughs and write
atlas-mission manifests that downstream pipelines can pick up."""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CRITERIA_FILE = ROOT / "config" / "breakthrough-criteria.yaml"
TOPICS_FILE = ROOT / "config" / "topics-we-care-about.yaml"
SUMMARIES_GLOB = "data/topics/*/summaries/items/*.md"
QUEUE_DIR = ROOT / "data" / "queues" / "atlas-missions"

LOG_PREFIX = "[detect-breakthroughs]"


# ---------------------------------------------------------------------------
# Lightweight YAML helpers — avoids external dependency
# ---------------------------------------------------------------------------

def _parse_yaml_list(lines: list[str], start: int) -> tuple[list[str], int]:
    """Parse a YAML list starting at *start* (the line after the key).
    Returns the list and the index of the first non-list line."""
    items: list[str] = []
    idx = start
    while idx < len(lines):
        stripped = lines[idx].strip()
        if stripped.startswith("- "):
            items.append(stripped[2:].strip().strip('"').strip("'"))
            idx += 1
        elif stripped == "" or stripped.startswith("#"):
            idx += 1
        else:
            break
    return items, idx


def load_criteria() -> dict[str, Any]:
    """Load breakthrough-criteria.yaml without PyYAML."""
    text = CRITERIA_FILE.read_text(encoding="utf-8")
    lines = text.splitlines()
    cfg: dict[str, Any] = {}
    idx = 0
    while idx < len(lines):
        line = lines[idx]
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            idx += 1
            continue
        if ":" not in stripped:
            idx += 1
            continue
        key, _, value = stripped.partition(":")
        key = key.strip()
        value = value.strip()
        if value == "" or value.startswith("#"):
            # Next lines should be a list
            items, idx = _parse_yaml_list(lines, idx + 1)
            cfg[key] = items
        else:
            # Remove inline comments
            if " #" in value:
                value = value[: value.index(" #")].strip()
            # Attempt numeric conversion
            try:
                cfg[key] = int(value)
            except ValueError:
                try:
                    cfg[key] = float(value)
                except ValueError:
                    cfg[key] = value.strip('"').strip("'")
            idx += 1
    return cfg


def load_topic_source_contexts() -> dict[str, list[str]]:
    """Return {slug: [source_context_values]} from topics-we-care-about.yaml."""
    text = TOPICS_FILE.read_text(encoding="utf-8")
    result: dict[str, list[str]] = {}
    current_slug: str | None = None
    in_source_context = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- slug:"):
            current_slug = stripped.split(":", 1)[1].strip()
            in_source_context = False
        elif stripped == "source_context:":
            in_source_context = True
        elif in_source_context and stripped.startswith("- "):
            if current_slug is not None:
                result.setdefault(current_slug, []).append(stripped[2:].strip())
        elif in_source_context and not stripped.startswith("- ") and stripped:
            in_source_context = False
    return result


# ---------------------------------------------------------------------------
# Summary file parsing
# ---------------------------------------------------------------------------

def strip_ticks(value: str) -> str:
    return value.strip().strip("`")


def parse_summary_metadata(text: str) -> dict[str, str]:
    """Extract ``- Key: `value` `` metadata from the header of a summary file."""
    metadata: dict[str, str] = {}
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("- ") or ":" not in stripped:
            continue
        label, value = stripped[2:].split(":", 1)
        metadata[label.strip().lower()] = strip_ticks(value.strip())
    return metadata


def parse_title(text: str) -> str:
    first_line = text.splitlines()[0].strip() if text.splitlines() else "Untitled"
    return first_line.removeprefix("# ").strip() or "Untitled"


def extract_section(text: str, heading: str) -> str:
    pattern = rf"^{re.escape(heading)}\n\n(.*?)(?=^## |\Z)"
    match = re.search(pattern, text, flags=re.MULTILINE | re.DOTALL)
    if not match:
        return ""
    return match.group(1).strip()


def load_source_item_context(source_item_rel: str) -> str:
    """Read the source item file and return the Source context value."""
    source_path = ROOT / source_item_rel
    if not source_path.exists():
        return ""
    try:
        text = source_path.read_text(encoding="utf-8")
    except OSError:
        return ""
    metadata = parse_summary_metadata(text)
    return metadata.get("source context", "")


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def compute_breakthrough_score(
    relevance_score: int,
    topic_slug: str,
    analysis_mode: str,
    searchable_text: str,
    source_context: str,
    criteria: dict[str, Any],
) -> tuple[float, list[str]]:
    """Return (score, reasons) for a single item."""
    score = float(relevance_score)
    reasons: list[str] = []

    atlas_topics: list[str] = criteria.get("atlas_topic_slugs", [])
    if topic_slug in atlas_topics:
        score += float(criteria.get("atlas_source_context_bonus", 1))
        reasons.append("atlas-tagged topic")

    source_parts = [s.strip().lower() for s in source_context.split(",")]
    if "atlas" in source_parts:
        score += float(criteria.get("atlas_item_context_bonus", 1))
        reasons.append("atlas in item source_context")

    keywords: list[str] = criteria.get("breakthrough_keywords", [])
    keyword_bonus_per = float(criteria.get("keyword_bonus_per_match", 0.5))
    keyword_cap = float(criteria.get("keyword_bonus_cap", 2.0))
    haystack = searchable_text.lower()
    kw_bonus = 0.0
    matched_kw: list[str] = []
    for kw in keywords:
        if kw.lower() in haystack:
            kw_bonus += keyword_bonus_per
            matched_kw.append(kw)
            if kw_bonus >= keyword_cap:
                kw_bonus = keyword_cap
                break
    if kw_bonus > 0:
        score += kw_bonus
        reasons.append(f"keyword matches: {', '.join(matched_kw)}")

    if analysis_mode == "fallback":
        penalty = float(criteria.get("fallback_mode_penalty", 1.0))
        score -= penalty
        reasons.append("fallback mode penalty")

    if relevance_score >= int(criteria.get("minimum_relevance_score", 8)):
        reasons.append("high relevance")

    return round(score, 2), reasons


# ---------------------------------------------------------------------------
# Manifest helpers
# ---------------------------------------------------------------------------

def manifest_filename(topic_slug: str, item_type: str, item_id: str) -> str:
    return f"{topic_slug}--{item_type}--{item_id}.json"


def build_source_url(item_type: str, item_id: str, metadata: dict[str, str]) -> str:
    """Reconstruct the source URL from metadata or conventions."""
    url = metadata.get("source url", "")
    if url:
        return url
    if item_type == "paper":
        return f"https://arxiv.org/abs/{item_id}"
    if item_type == "youtube":
        return f"https://www.youtube.com/watch?v={item_id}"
    return ""


def write_manifest(manifest: dict[str, Any]) -> Path:
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    filename = manifest_filename(
        manifest["topic_slug"], manifest["item_type"], manifest["item_id"]
    )
    path = QUEUE_DIR / filename
    path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return path


# ---------------------------------------------------------------------------
# Main scanning logic
# ---------------------------------------------------------------------------

def iter_summary_files() -> list[Path]:
    """Return all summary item files sorted by path."""
    return sorted((ROOT).glob(SUMMARIES_GLOB))


def process_summary(
    summary_path: Path,
    criteria: dict[str, Any],
    topic_contexts: dict[str, list[str]],
    force: bool,
) -> dict[str, Any] | None:
    """Evaluate a single summary file. Returns the manifest dict if it qualifies,
    or None if it does not."""
    text = summary_path.read_text(encoding="utf-8")
    metadata = parse_summary_metadata(text)

    # --- Extract fields ---
    topic_slug = metadata.get("topic slug", "")
    item_type = metadata.get("item type", "")
    analysis_mode = metadata.get("analysis mode", "unknown")
    title = parse_title(text)

    # Derive item_id from filename: "paper--2604.02268v1.md" -> "2604.02268v1"
    stem = summary_path.stem  # e.g. "paper--2604.02268v1"
    parts = stem.split("--", 1)
    item_id = parts[1] if len(parts) == 2 else stem

    # --- Relevance gate ---
    try:
        relevance_score = int(metadata.get("relevance score", "0"))
    except ValueError:
        relevance_score = 0

    min_score = int(criteria.get("minimum_relevance_score", 8))
    if relevance_score < min_score:
        return None

    # --- Idempotency check ---
    manifest_file = QUEUE_DIR / manifest_filename(topic_slug, item_type, item_id)
    if manifest_file.exists() and not force:
        return None

    # --- Build searchable text for keyword matching ---
    summary_section = extract_section(text, "## Summary")
    why_section = extract_section(text, "## Why It Matters Now")
    takeaways_section = extract_section(text, "## Key Takeaways")
    searchable_text = f"{title} {summary_section} {why_section} {takeaways_section}"

    # --- Resolve source_context ---
    # Prefer per-item source context from the source item file, fall back to
    # the topic-level source_context from the config.
    source_item_rel = metadata.get("source item", "")
    source_context = load_source_item_context(source_item_rel)
    if not source_context:
        ctx_list = topic_contexts.get(topic_slug, [])
        source_context = ", ".join(ctx_list)

    # --- Score ---
    breakthrough_score, reasons = compute_breakthrough_score(
        relevance_score=relevance_score,
        topic_slug=topic_slug,
        analysis_mode=analysis_mode,
        searchable_text=searchable_text,
        source_context=source_context,
        criteria=criteria,
    )

    threshold = float(criteria.get("breakthrough_threshold", 8.5))
    if breakthrough_score < threshold:
        return None

    # --- Only high-confidence analysis mode items qualify ---
    high_conf = str(criteria.get("high_confidence_analysis_mode", "claude"))
    if analysis_mode != high_conf:
        return None

    # --- Build manifest ---
    source_url = build_source_url(item_type, item_id, metadata)

    # Derive the source_item_path relative to ROOT
    source_item_path = source_item_rel
    if not source_item_path:
        # Attempt conventional path
        type_dir = "papers" if item_type == "paper" else "youtube"
        source_item_path = f"data/topics/{topic_slug}/{type_dir}/items/{item_id}.md"

    manifest = {
        "item_id": item_id,
        "item_type": item_type,
        "topic_slug": topic_slug,
        "title": title,
        "source_url": source_url,
        "relevance_score": relevance_score,
        "breakthrough_score": breakthrough_score,
        "breakthrough_reasons": reasons,
        "summary_path": str(summary_path.relative_to(ROOT)),
        "source_item_path": source_item_path,
        "detected_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "mission_status": "pending",
    }
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Detect science breakthroughs from analyzed Research Radar summaries and write atlas-mission manifests."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show which items would produce manifests without writing anything.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Stop after detecting N breakthroughs. Use 0 for no limit.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-evaluate items even if a manifest already exists.",
    )
    args = parser.parse_args()

    # --- Load config ---
    if not CRITERIA_FILE.exists():
        print(f"{LOG_PREFIX} criteria file missing: {CRITERIA_FILE}", file=sys.stderr)
        return 1

    criteria = load_criteria()
    topic_contexts = load_topic_source_contexts()

    # --- Scan summaries ---
    summary_files = iter_summary_files()
    if not summary_files:
        print(f"{LOG_PREFIX} no summary files found")
        return 0

    detected = 0
    skipped = 0
    errors = 0

    for summary_path in summary_files:
        if 0 < args.limit <= detected:
            break

        try:
            manifest = process_summary(
                summary_path, criteria, topic_contexts, force=args.force
            )
        except Exception as exc:
            errors += 1
            rel = summary_path.relative_to(ROOT)
            print(f"{LOG_PREFIX} error processing {rel}: {exc}", file=sys.stderr)
            continue

        if manifest is None:
            skipped += 1
            continue

        if args.dry_run:
            rel = summary_path.relative_to(ROOT)
            print(
                f"{LOG_PREFIX} dry-run: {rel} "
                f"score={manifest['breakthrough_score']} "
                f"reasons={manifest['breakthrough_reasons']}"
            )
            detected += 1
            continue

        manifest_path = write_manifest(manifest)
        rel_manifest = manifest_path.relative_to(ROOT)
        print(
            f"{LOG_PREFIX} "
            f"topic={manifest['topic_slug']} "
            f"item={manifest['item_id']} "
            f"breakthrough_score={manifest['breakthrough_score']} "
            f"manifest={rel_manifest}"
        )
        detected += 1

    mode_label = "dry-run " if args.dry_run else ""
    print(
        f"{LOG_PREFIX} completed {mode_label}"
        f"detected={detected} skipped={skipped} errors={errors}"
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

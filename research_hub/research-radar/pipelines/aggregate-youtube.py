#!/usr/bin/env python3
"""Aggregate today's YouTube items into a single daily markdown table.

Runs AFTER the existing YouTube collector (collect-youtube.sh).
Scans all YouTube item files in data/topics/*/youtube/items/*.md that were
collected today, and produces data/daily/YYYY-MM-DD/youtube_aggregated.md.
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT / "data"
TOPICS_ROOT = DATA_ROOT / "topics"
DAILY_ROOT = DATA_ROOT / "daily"

PREFIX = "[aggregate-youtube]"


def parse_metadata(text: str) -> dict[str, str]:
    """Extract ``- Key: `value`` or ``- Key: value`` lines into a dict."""
    metadata: dict[str, str] = {}
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("- ") or ": " not in stripped:
            continue
        label, value = stripped[2:].split(": ", 1)
        metadata[label.strip().lower()] = value.strip()
    return metadata


def strip_ticks(value: str) -> str:
    return value.strip().strip("`")


def parse_title(text: str) -> str:
    first_line = text.splitlines()[0].strip() if text.splitlines() else "Untitled"
    return first_line.removeprefix("# ").strip() or "Untitled"


def extract_section(text: str, heading: str) -> str:
    pattern = rf"^{re.escape(heading)}\n\n(.*?)(?=^## |\Z)"
    match = re.search(pattern, text, flags=re.MULTILINE | re.DOTALL)
    if not match:
        return ""
    return match.group(1).strip()


def collected_on_date(metadata: dict[str, str], target_date: str) -> bool:
    """Return True if the item's Collected at UTC timestamp matches target_date (YYYY-MM-DD)."""
    raw = strip_ticks(metadata.get("collected at utc", ""))
    if not raw:
        return False
    try:
        collected_dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        return collected_dt.strftime("%Y-%m-%d") == target_date
    except (ValueError, TypeError):
        return False


def iter_youtube_items(target_date: str) -> list[dict[str, str]]:
    """Scan all topic directories for YouTube items collected on target_date."""
    items: list[dict[str, str]] = []

    if not TOPICS_ROOT.exists():
        return items

    for topic_dir in sorted(p for p in TOPICS_ROOT.iterdir() if p.is_dir()):
        items_dir = topic_dir / "youtube" / "items"
        if not items_dir.exists():
            continue
        for item_path in sorted(items_dir.glob("*.md")):
            if item_path.name == ".gitkeep":
                continue
            text = item_path.read_text(encoding="utf-8")
            metadata = parse_metadata(text)
            if not collected_on_date(metadata, target_date):
                continue

            title = parse_title(text)
            video_id = strip_ticks(metadata.get("video id", item_path.stem))
            channel = strip_ticks(metadata.get("channel", "Unknown"))
            duration = strip_ticks(metadata.get("duration", "-"))
            views = strip_ticks(metadata.get("views", "-"))
            topic = topic_dir.name
            transcript_status = strip_ticks(metadata.get("transcript status", "unknown"))

            transcript_text = extract_section(text, "## Transcript")
            has_transcript = (
                transcript_status == "ready"
                and bool(transcript_text)
                and "Transcript fetch" not in transcript_text
                and "not extracted" not in transcript_text.lower()
            )

            items.append({
                "title": title,
                "channel": channel,
                "duration": duration,
                "views": views,
                "topic": topic,
                "video_id": video_id,
                "has_transcript": "yes" if has_transcript else "no",
                "transcript_text": transcript_text if has_transcript else "",
                "item_path": str(item_path),
            })

    return items


def deduplicate_items(items: list[dict[str, str]]) -> list[dict[str, str]]:
    """Deduplicate by video_id, keeping the first occurrence."""
    seen: set[str] = set()
    unique: list[dict[str, str]] = []
    for item in items:
        vid = item["video_id"]
        if vid not in seen:
            seen.add(vid)
            unique.append(item)
    return unique


def build_aggregated_md(target_date: str, items: list[dict[str, str]]) -> str:
    """Build the markdown table for youtube_aggregated.md."""
    lines = [
        f"# YouTube Videos \u2014 {target_date}",
        "",
        "| # | Title | Channel | Duration | Views | Topic | Transcript | Relevance | Novelty | Summary |",
        "|---|-------|---------|----------|-------|-------|-----------|-----------|---------|---------|",
    ]
    for idx, item in enumerate(items, start=1):
        title = item["title"].replace("|", "\\|")
        channel = item["channel"].replace("|", "\\|")
        row = (
            f"| {idx} "
            f"| {title} "
            f"| {channel} "
            f"| {item['duration']} "
            f"| {item['views']} "
            f"| {item['topic']} "
            f"| {item['has_transcript']} "
            f"| - "
            f"| - "
            f"| - |"
        )
        lines.append(row)

    lines.append("")
    return "\n".join(lines)


def copy_transcripts(target_date: str, items: list[dict[str, str]]) -> int:
    """Copy transcript content to data/daily/YYYY-MM-DD/transcripts/<video-id>.txt."""
    transcripts_dir = DAILY_ROOT / target_date / "transcripts"
    copied = 0

    for item in items:
        if item["has_transcript"] != "yes" or not item["transcript_text"]:
            continue
        transcripts_dir.mkdir(parents=True, exist_ok=True)
        dest = transcripts_dir / f"{item['video_id']}.txt"
        dest.write_text(item["transcript_text"], encoding="utf-8")
        copied += 1

    return copied


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Aggregate today's YouTube items into a daily markdown table."
    )
    parser.add_argument(
        "--date",
        default=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        help="Date to aggregate (YYYY-MM-DD). Default: today UTC.",
    )
    args = parser.parse_args()
    target_date: str = args.date

    print(f"{PREFIX} scanning for YouTube items collected on {target_date}")

    items = iter_youtube_items(target_date)
    items = deduplicate_items(items)

    if not items:
        print(f"{PREFIX} no YouTube items found for {target_date}")
        return 0

    print(f"{PREFIX} found {len(items)} YouTube items for {target_date}")

    day_dir = DAILY_ROOT / target_date
    day_dir.mkdir(parents=True, exist_ok=True)

    aggregated_path = day_dir / "youtube_aggregated.md"
    aggregated_md = build_aggregated_md(target_date, items)
    aggregated_path.write_text(aggregated_md, encoding="utf-8")
    print(f"{PREFIX} wrote {aggregated_path.relative_to(ROOT)}")

    copied = copy_transcripts(target_date, items)
    print(f"{PREFIX} copied {copied} transcripts to {(day_dir / 'transcripts').relative_to(ROOT)}")

    print(f"{PREFIX} completed items={len(items)} transcripts={copied}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

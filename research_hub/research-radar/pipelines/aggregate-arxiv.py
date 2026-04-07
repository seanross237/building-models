#!/usr/bin/env python3
"""Aggregate today's arXiv paper items into a single daily markdown table.

Runs AFTER the existing paper collector (collect-papers.sh).
Scans all paper item files in data/topics/*/papers/items/*.md that were
collected today, and produces data/daily/YYYY-MM-DD/arxiv_aggregated.md.
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT / "data"
TOPICS_ROOT = DATA_ROOT / "topics"
DAILY_ROOT = DATA_ROOT / "daily"

PREFIX = "[aggregate-arxiv]"


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


def truncate_authors(authors_raw: str, max_authors: int = 3) -> str:
    """Shorten author list to 'First et al.' if too many."""
    authors_raw = strip_ticks(authors_raw)
    if not authors_raw:
        return "Unknown"
    parts = [a.strip() for a in authors_raw.split(",")]
    if len(parts) <= max_authors:
        return ", ".join(parts)
    return f"{parts[0]} et al."


def iter_paper_items(target_date: str) -> list[dict[str, str]]:
    """Scan all topic directories for paper items collected on target_date."""
    items: list[dict[str, str]] = []

    if not TOPICS_ROOT.exists():
        return items

    for topic_dir in sorted(p for p in TOPICS_ROOT.iterdir() if p.is_dir()):
        items_dir = topic_dir / "papers" / "items"
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
            paper_id = strip_ticks(metadata.get("paper id", item_path.stem))
            authors = truncate_authors(metadata.get("authors", "Unknown"))
            topic = topic_dir.name
            primary_category = strip_ticks(metadata.get("primary category", "-"))

            items.append({
                "title": title,
                "authors": authors,
                "topic": topic,
                "category": primary_category,
                "paper_id": paper_id,
                "full_text": text,
                "item_path": str(item_path),
            })

    return items


def deduplicate_items(items: list[dict[str, str]]) -> list[dict[str, str]]:
    """Deduplicate by paper_id, keeping the first occurrence."""
    seen: set[str] = set()
    unique: list[dict[str, str]] = []
    for item in items:
        pid = item["paper_id"]
        if pid not in seen:
            seen.add(pid)
            unique.append(item)
    return unique


def build_aggregated_md(target_date: str, items: list[dict[str, str]]) -> str:
    """Build the markdown table for arxiv_aggregated.md."""
    lines = [
        f"# arXiv Papers \u2014 {target_date}",
        "",
        "| # | Title | Authors | Topic | Category | Relevance | Novelty | Summary |",
        "|---|-------|---------|-------|----------|-----------|---------|---------|",
    ]
    for idx, item in enumerate(items, start=1):
        title = item["title"].replace("|", "\\|")
        authors = item["authors"].replace("|", "\\|")
        row = (
            f"| {idx} "
            f"| {title} "
            f"| {authors} "
            f"| {item['topic']} "
            f"| {item['category']} "
            f"| - "
            f"| - "
            f"| - |"
        )
        lines.append(row)

    lines.append("")
    return "\n".join(lines)


def copy_papers(target_date: str, items: list[dict[str, str]]) -> int:
    """Copy full paper content to data/daily/YYYY-MM-DD/papers/<paper-id>.md."""
    papers_dir = DAILY_ROOT / target_date / "papers"
    copied = 0

    for item in items:
        papers_dir.mkdir(parents=True, exist_ok=True)
        dest = papers_dir / f"{item['paper_id']}.md"
        dest.write_text(item["full_text"], encoding="utf-8")
        copied += 1

    return copied


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Aggregate today's arXiv paper items into a daily markdown table."
    )
    parser.add_argument(
        "--date",
        default=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        help="Date to aggregate (YYYY-MM-DD). Default: today UTC.",
    )
    args = parser.parse_args()
    target_date: str = args.date

    print(f"{PREFIX} scanning for arXiv papers collected on {target_date}")

    items = iter_paper_items(target_date)
    items = deduplicate_items(items)

    if not items:
        print(f"{PREFIX} no arXiv papers found for {target_date}")
        return 0

    print(f"{PREFIX} found {len(items)} arXiv papers for {target_date}")

    day_dir = DAILY_ROOT / target_date
    day_dir.mkdir(parents=True, exist_ok=True)

    aggregated_path = day_dir / "arxiv_aggregated.md"
    aggregated_md = build_aggregated_md(target_date, items)
    aggregated_path.write_text(aggregated_md, encoding="utf-8")
    print(f"{PREFIX} wrote {aggregated_path.relative_to(ROOT)}")

    copied = copy_papers(target_date, items)
    print(f"{PREFIX} copied {copied} papers to {(day_dir / 'papers').relative_to(ROOT)}")

    print(f"{PREFIX} completed items={len(items)} papers={copied}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
